from copy import deepcopy

from django.contrib.auth.models import User
from django.db.models import Q
from pandas import date_range
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, ListAPIView, \
    RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dm_apps.utils import custom_send_mail
from shared_models import models as shared_models
from shared_models.utils import get_labels
from . import permissions, pagination
from . import serializers
from .. import models, stat_holidays, emails
from ..utils import financial_project_year_summary_data, financial_project_summary_data, get_user_fte_breakdown, can_modify_project, \
    get_manageable_sections, multiple_financial_project_year_summary_data, is_section_head
from ..utils import is_management_or_admin


# USER
#######
class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.UserDisplaySerializer(instance=request.user)
        data = serializer.data
        if request.query_params.get("project"):
            data.update(can_modify_project(request.user, request.query_params.get("project"), True))

        if request.query_params.get("status_report"):
            status_report = get_object_or_404(models.StatusReport, pk=request.query_params.get("status_report"))
            data.update(can_modify_project(request.user, status_report.project_year.project_id, True))
            data.update(dict(is_section_head=is_section_head(request.user, status_report.project_year.project)))
        return Response(data)


class FTEBreakdownAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # if there are no project year ids, do this
        if not request.query_params.get("ids"):
            # if no user is specified, we will assume it is the request user
            if not request.query_params.get("user"):
                my_user = request.user
            else:
                my_user = get_object_or_404(User, pk=request.query_params.get("user"))

            # if there is no fiscal year specified, let's get all years
            if not request.query_params.get("year"):
                # need a list of fiscal years
                fy_qs = shared_models.FiscalYear.objects.filter(projectyear__staff__user=my_user).distinct()
                data = list()
                for fy in fy_qs:
                    data.append(get_user_fte_breakdown(my_user, fiscal_year_id=fy.id))
            else:
                data = get_user_fte_breakdown(my_user, fiscal_year_id=request.query_params.get("year"))
            return Response(data, status.HTTP_200_OK)
        else:
            if not request.query_params.get("year"):
                return Response({"error": "must supply a fiscal year"}, status.HTTP_400_BAD_REQUEST)

            data = list()
            ids = request.query_params.get("ids").split(",")
            year = request.query_params.get("year")
            # now we need a user list for any users in the above list
            users = User.objects.filter(staff_instances2__project_year_id__in=ids).distinct().order_by("last_name")

            for u in users:
                my_dict = get_user_fte_breakdown(u, fiscal_year_id=year)
                staff_instances = models.Staff.objects.filter(user=u, project_year__fiscal_year_id=year).distinct()
                my_dict["staff_instances"] = serializers.StaffSerializer(staff_instances, many=True).data
                data.append(my_dict)

            return Response(data, status.HTTP_200_OK)


class GetDatesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        fiscal_year = self.request.query_params.get("year")  # to be formatted as follows: YYYY; SAP style
        if fiscal_year:
            fiscal_year = int(fiscal_year)
            # create a pandas date_range object for upcoming fiscal year
            start = f"{fiscal_year - 1}-04-01"
            end = f"{fiscal_year}-03-31"
            datelist = date_range(start=start, end=end).tolist()

            date_format = "%d-%B-%Y"
            short_date_format = "%d-%b-%Y"
            # get a list of statutory holidays
            holiday_list = [d.strftime(date_format) for d in stat_holidays.stat_holiday_list]

            data = list()
            # create a dict for the response
            for dt in datelist:
                is_stat = dt.strftime(date_format) in holiday_list
                weekday = dt.strftime("%A")
                int_weekday = dt.strftime("%w")
                obj = dict(
                    formatted_date=dt.strftime(date_format),
                    formatted_short_date=dt.strftime(short_date_format),
                    weekday=weekday,
                    short_weekday=f'{dt.strftime("%a")}.',
                    int_weekday=int_weekday,
                    is_stat=is_stat,
                    pay_rate=2 if is_stat or int_weekday == 0 else 1.5
                )
                data.append(obj)
            return Response(data, status.HTTP_200_OK)
        raise ValidationError("missing query parameter 'year'")


class ProjectRetrieveAPIView(RetrieveAPIView):
    queryset = models.Project.objects.all().order_by("-created_at")
    serializer_class = serializers.ProjectSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]


class ProjectListAPIView(ListAPIView):
    pagination_class = pagination.StandardResultsSetPagination
    serializer_class = serializers.ProjectSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        qs = models.Project.objects.order_by("id")
        if not is_management_or_admin(self.request.user):
            qs = qs.filter(is_hidden=False)
        return qs


class AddProjectReferenceAPIView(APIView):
    permission_classes = [permissions.CanModifyOrReadOnly]

    def post(self, request, pk, action):
        citation = get_object_or_404(shared_models.Citation, pk=request.data["citation"])
        project = get_object_or_404(models.Project, pk=pk)
        if action == "add":
            project.references.add(citation)
        elif action == "remove":
            project.references.remove(citation)
        return Response(serializers.CitationSerializer(citation).data, status=status.HTTP_200_OK)


# PROJECT YEAR
##############

class ProjectYearListAPIView(ListAPIView):
    pagination_class = pagination.StandardResultsSetPagination
    serializer_class = serializers.ProjectYearSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        qs = models.ProjectYear.objects.order_by("start_date")
        qp = self.request.query_params

        filter_list = [
            "user",
            "is_hidden",
            "title",
            "id",
            'staff',
            'fiscal_year',
            'tag',
            'theme',
            'functional_group',
            'funding_source',
            'region',
            'division',
            'section',
            'status',
        ]
        for filter in filter_list:
            input = qp.get(filter)
            if input == "true":
                input = True
            elif input == "false":
                input = False
            elif input == "null" or input == "":
                input = None

            if input:
                if filter == "user":
                    qs = qs.filter(project__section__in=get_manageable_sections(self.request.user)).order_by("fiscal_year", "project_id")
                elif filter == "is_hidden":
                    qs = qs.filter(project__is_hidden=True)
                elif filter == "status":
                    qs = qs.filter(status=input)
                elif filter == "title":
                    qs = qs.filter(project__title__icontains=input)
                elif filter == "id":
                    qs = qs.filter(project__id=input)
                elif filter == "staff":
                    qs = qs.filter(project__staff_search_field__icontains=input)
                elif filter == "fiscal_year":
                    qs = qs.filter(fiscal_year_id=input)
                elif filter == "tag":
                    qs = qs.filter(project__tags=input)
                elif filter == "theme":
                    qs = qs.filter(project__functional_group__theme_id=input)
                elif filter == "functional_group":
                    qs = qs.filter(project__functional_group_id=input)
                elif filter == "funding_source":
                    qs = qs.filter(project__default_funding_source_id=input)
                elif filter == "region":
                    qs = qs.filter(project__section__division__branch__region_id=input)
                elif filter == "division":
                    qs = qs.filter(project__section__division_id=input)
                elif filter == "section":
                    qs = qs.filter(project__section_id=input)

        # if a regular user is making the request, show only approved projects (and not hidden projects)
        if not is_management_or_admin(self.request.user):
            qs = qs.filter(project__is_hidden=False, status=4)
        return qs.distinct()


class ProjectYearRetrieveAPIView(RetrieveAPIView):
    queryset = models.ProjectYear.objects.all().order_by("-created_at")
    serializer_class = serializers.ProjectYearSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]


class ProjectYearSubmitAPIView(APIView):
    queryset = models.ProjectYear.objects.all().order_by("-created_at")
    serializer_class = serializers.ProjectYearSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def post(self, request, project_year):
        project_year = get_object_or_404(models.ProjectYear, pk=project_year)
        project_year.submit(request)

        # create a new email object
        email = emails.ProjectYearSubmissionEmail(project_year, request)
        # send the email object
        custom_send_mail(
            subject=email.subject,
            html_message=email.message,
            from_email=email.from_email,
            recipient_list=email.to_list
        )
        return Response(serializers.ProjectYearSerializer(project_year).data, status.HTTP_200_OK)


class ProjectYearUnsubmitAPIView(APIView):
    queryset = models.ProjectYear.objects.all().order_by("-created_at")
    serializer_class = serializers.ProjectYearSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def post(self, request, project_year):
        project_year = get_object_or_404(models.ProjectYear, pk=project_year)
        project_year.unsubmit(request)
        return Response(serializers.ProjectYearSerializer(project_year).data, status.HTTP_200_OK)


# STAFF
#######
class StaffListCreateAPIView(ListCreateAPIView):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        year = models.ProjectYear.objects.get(pk=self.kwargs.get("project_year"))
        return year.staff_set.all()

    def perform_create(self, serializer):
        staff = serializer.save(project_year_id=self.kwargs.get("project_year"))
        staff.project_year.update_modified_by(self.request.user)
        if staff.user and staff.user.email:
            email = emails.StaffEmail(staff, "add", self.request)
            custom_send_mail(
                subject=email.subject,
                html_message=email.message,
                from_email=email.from_email,
                recipient_list=email.to_list
            )


class StaffRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.project_year.update_modified_by(self.request.user)

    def perform_update(self, serializer):
        staff = get_object_or_404(models.Staff, pk=self.kwargs.get("pk"))
        old_lead_status = staff.is_lead
        staff = serializer.save()
        staff.project_year.update_modified_by(self.request.user)
        if (old_lead_status is False and staff.is_lead) and (staff.user and staff.user.email):
            email = emails.StaffEmail(staff, "add", self.request)
            custom_send_mail(
                subject=email.subject,
                html_message=email.message,
                from_email=email.from_email,
                recipient_list=email.to_list
            )
        super().perform_update(serializer)


# O&M
#######
class OMCostListCreateAPIView(ListCreateAPIView):
    queryset = models.OMCost.objects.all()
    serializer_class = serializers.OMCostSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        year = models.ProjectYear.objects.get(pk=self.kwargs.get("project_year"))
        return year.omcost_set.all()

    def perform_create(self, serializer):
        obj = serializer.save(project_year_id=self.kwargs.get("project_year"))
        obj.project_year.update_modified_by(self.request.user)


class OMCostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.OMCost.objects.all()
    serializer_class = serializers.OMCostSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.project_year.update_modified_by(self.request.user)

    def perform_update(self, serializer):
        obj = serializer.save()
        obj.project_year.update_modified_by(self.request.user)


class AddAllCostsAPIView(APIView):
    permission_classes = [permissions.CanModifyOrReadOnly]

    def post(self, request, project_year):
        year = models.ProjectYear.objects.get(pk=self.kwargs.get("project_year"))
        year.add_all_om_costs()
        year.update_modified_by(request.user)
        serializer = serializers.OMCostSerializer(instance=year.omcost_set.all(), many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class RemoveEmptyCostsAPIView(APIView):
    permission_classes = [permissions.CanModifyOrReadOnly]

    def post(self, request, project_year):
        year = models.ProjectYear.objects.get(pk=self.kwargs.get("project_year"))
        year.clear_empty_om_costs()
        year.update_modified_by(request.user)
        serializer = serializers.OMCostSerializer(instance=year.omcost_set.all(), many=True)
        return Response(serializer.data, status.HTTP_200_OK)


# CAPITAL
#########
class CapitalCostListCreateAPIView(ListCreateAPIView):
    queryset = models.CapitalCost.objects.all()
    serializer_class = serializers.CapitalCostSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        year = models.ProjectYear.objects.get(pk=self.kwargs.get("project_year"))
        return year.capitalcost_set.all()

    def perform_create(self, serializer):
        obj = serializer.save(project_year_id=self.kwargs.get("project_year"))
        obj.project_year.update_modified_by(self.request.user)


class CapitalCostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.CapitalCost.objects.all()
    serializer_class = serializers.CapitalCostSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.project_year.update_modified_by(self.request.user)

    def perform_update(self, serializer):
        obj = serializer.save()
        obj.project_year.update_modified_by(self.request.user)


# MILESTONE
###########
class ActivityListCreateAPIView(ListCreateAPIView):
    queryset = models.Activity.objects.all()
    serializer_class = serializers.ActivitySerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        year = models.ProjectYear.objects.get(pk=self.kwargs.get("project_year"))
        return year.activities.all()

    def perform_create(self, serializer):
        obj = serializer.save(project_year_id=self.kwargs.get("project_year"))
        obj.project_year.update_modified_by(self.request.user)


class ActivityRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.Activity.objects.all()
    serializer_class = serializers.ActivitySerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.project_year.update_modified_by(self.request.user)

    def perform_update(self, serializer):
        obj = serializer.save()
        obj.project_year.update_modified_by(self.request.user)

    def post(self, request, pk):
        # we only allow this method when we are changing statuses
        qp = request.GET
        action = qp.get("action")
        clone = qp.get("clone")
        if action == "complete" or action == "incomplete":
            activity = get_object_or_404(models.Activity, pk=pk)
            # get or create a status report
            qs = models.StatusReport.objects.filter(project_year=activity.project_year)
            if qs:
                status_report = qs.order_by("id").last()
            else:
                status_report = models.StatusReport.objects.create(project_year=activity.project_year)
            # now we get or create the activity update
            update, create = models.ActivityUpdate.objects.get_or_create(
                status_report=status_report,
                activity=activity,
            )
            if action == "complete":
                update.status = 8
            else:
                update.status = 7
            update.notes = request.data
            update.save()
            # if all the

            return Response(serializers.ActivitySerializer(activity).data, status=status.HTTP_200_OK)
        elif clone:
            old_activity = get_object_or_404(models.Activity, pk=pk)
            new_activity = deepcopy(old_activity)
            new_activity.pk = None
            new_activity.save()
            return Response(serializers.ActivitySerializer(new_activity).data, status=status.HTTP_200_OK)
        raise ValidationError("sorry, I am missing the query param for 'action' or 'clone'")

# COLLABORATION
##############
class CollaborationListCreateAPIView(ListCreateAPIView):
    queryset = models.Collaboration.objects.all()
    serializer_class = serializers.CollaborationSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        year = models.ProjectYear.objects.get(pk=self.kwargs.get("project_year"))
        return year.collaborations.all()

    def perform_create(self, serializer):
        obj = serializer.save(project_year_id=self.kwargs.get("project_year"))
        obj.project_year.update_modified_by(self.request.user)


class CollaborationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.Collaboration.objects.all()
    serializer_class = serializers.CollaborationSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.project_year.update_modified_by(self.request.user)

    def perform_update(self, serializer):
        obj = serializer.save()
        obj.project_year.update_modified_by(self.request.user)


# CITATIONS
##############
class CitationListCreateAPIView(ListCreateAPIView):
    queryset = shared_models.Citation.objects.all()
    serializer_class = serializers.CitationSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        if self.request.query_params.get("project"):
            project = get_object_or_404(models.Project, pk=self.request.query_params.get("project"))
            qs = project.references.all()
        else:
            if self.request.query_params.get("search"):
                term = self.request.query_params.get("search")
                qs = shared_models.Citation.objects.filter(
                    Q(name__icontains=term) | Q(nom__icontains=term) | Q(abstract_en__icontains=term) | Q(abstract_fr__icontains=term) | Q(
                        authors__icontains=term))
            else:
                qs = shared_models.Citation.objects.all()

        if qs.count() > 100:
            qs = shared_models.Citation.objects.filter(id__in=[item.id for item in qs[:100]])

        return qs

    def perform_create(self, serializer):
        obj = serializer.save()

        if self.request.data.get("new_publication") and self.request.data.get("new_publication") != "":
            pub, created = shared_models.Publication.objects.get_or_create(name=self.request.data.get("new_publication"))
            obj.publication = pub
            obj.save()

        if self.request.query_params.get("project"):
            project = get_object_or_404(models.Project, pk=self.request.query_params.get("project"))
            project.references.add(obj)
            project.modified_by = self.request.user
            project.save()


class CitationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = shared_models.Citation.objects.all()
    serializer_class = serializers.CitationSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        obj = serializer.save()
        # if there is a new publication being passed in... create it and then add it to citation
        if self.request.data.get("new_publication") and self.request.data.get("new_publication") != "":
            pub, created = shared_models.Publication.objects.get_or_create(name=self.request.data.get("new_publication"))
            obj.publication = pub
            obj.save()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


# Publications
##############
class PublicationListAPIView(ListAPIView):
    queryset = shared_models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]


# STATUS REPORTS
##############

class StatusReportListCreateAPIView(ListCreateAPIView):
    queryset = models.StatusReport.objects.all()
    serializer_class = serializers.StatusReportSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        year = models.ProjectYear.objects.get(pk=self.kwargs.get("project_year"))
        return year.reports.all()

    def perform_create(self, serializer):
        obj = serializer.save(project_year_id=self.kwargs.get("project_year"))
        obj.project_year.update_modified_by(self.request.user)


class StatusReportRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.StatusReport.objects.all()
    serializer_class = serializers.StatusReportSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def perform_update(self, serializer):
        obj = serializer.save(modified_by=self.request.user)
        obj.project_year.update_modified_by(self.request.user)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.project_year.update_modified_by(self.request.user)


# Activity Updates


class ActivityUpdateListAPIView(ListAPIView):
    queryset = models.StatusReport.objects.all()
    serializer_class = serializers.ActivityUpdateSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        status_report = get_object_or_404(models.StatusReport, pk=self.kwargs.get("status_report"))
        return status_report.updates.all()


class ActivityUpdateRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = models.ActivityUpdate.objects.all()
    serializer_class = serializers.ActivityUpdateSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def perform_update(self, serializer):
        obj = serializer.save()
        obj.status_report.project_year.update_modified_by(self.request.user)


# FILES / Supporting Resources
##############
class FileListCreateAPIView(ListCreateAPIView):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        year = models.ProjectYear.objects.get(pk=self.kwargs.get("project_year"))
        qs = year.files.all()

        qp = self.request.query_params
        if qp.get("status_report"):
            qs = qs.filter(status_report=qp.get("status_report"))

        return qs

    def perform_create(self, serializer):
        year = get_object_or_404(models.ProjectYear, pk=self.kwargs.get("project_year"))
        kwargs = dict(project=year.project, project_year=year)
        qp = self.request.query_params
        if qp.get("status_report"):
            kwargs["status_report_id"] = qp.get("status_report")
        obj = serializer.save(**kwargs)
        obj.project_year.update_modified_by(self.request.user)


class FileRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.project_year.update_modified_by(self.request.user)

    def perform_update(self, serializer):
        obj = serializer.save()
        obj.project_year.update_modified_by(self.request.user)


# FINANCIALS
############


class FinancialsAPIView(APIView):
    permissions = [IsAuthenticated]

    def get(self, request, project_year=None, project=None):
        if not project_year and not project:
            # the we will be needing ids and year query_params
            qp = request.query_params
            if not qp.get("ids"):
                return Response(None, status.HTTP_400_BAD_REQUEST)
            else:

                ids = request.query_params.get("ids").split(",")

                # get project year list
                project_years = models.ProjectYear.objects.filter(id__in=ids)
                data = multiple_financial_project_year_summary_data(project_years)
                return Response(data, status.HTTP_200_OK)

        if project_year:
            obj = get_object_or_404(models.ProjectYear, pk=project_year)
            data = financial_project_year_summary_data(obj)

        else:  # must be supplied with a project
            obj = get_object_or_404(models.Project, pk=project)
            data = financial_project_summary_data(obj)

        return Response(data, status.HTTP_200_OK)


# LOOKUPS
##########


class FiscalYearListAPIView(ListAPIView):
    serializer_class = serializers.FiscalYearSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        qs = shared_models.FiscalYear.objects.filter(projectyear__isnull=False)

        if self.request.query_params.get("user") == 'true':
            qs = qs.filter(projectyear__project__section__in=get_manageable_sections(self.request.user))

        return qs.distinct()


class TagListAPIView(ListAPIView):
    serializer_class = serializers.TagSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        qs = models.Tag.objects.filter(projects__isnull=False)

        if self.request.query_params.get("user") == 'true':
            qs = qs.filter(projects__section__in=get_manageable_sections(self.request.user))

        return qs.distinct()


class ThemeListAPIView(ListAPIView):
    serializer_class = serializers.ThemeSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        qs = models.Theme.objects.all()
        if self.request.query_params.get("user") == 'true':
            qs = qs.filter(functional_groups__projects__section__in=get_manageable_sections(self.request.user))
        return qs.distinct()


class FunctionalGroupListAPIView(ListAPIView):
    serializer_class = serializers.FunctionalGroupSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        qs = models.FunctionalGroup.objects.all()

        if self.request.query_params.get("section"):
            qs = qs.filter(sections=self.request.query_params.get("section"))
        elif self.request.query_params.get("user") == 'true':
            qs = qs.filter(sections__in=get_manageable_sections(self.request.user))
        elif self.request.query_params.get("division"):
            qs = qs.filter(sections__division=self.request.query_params.get("division"))
        elif self.request.query_params.get("region"):
            qs = qs.filter(sections__division__branch__region=self.request.query_params.get("region"))
        return qs.distinct()


class FundingSourceListAPIView(ListAPIView):
    serializer_class = serializers.FundingSourceSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        qs = models.FundingSource.objects.all()
        if self.request.query_params.get("user") == 'true':
            qs = qs.filter(projects__section__in=get_manageable_sections(self.request.user))
        return qs.distinct()


class RegionListAPIView(ListAPIView):
    serializer_class = serializers.RegionSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        qs = shared_models.Region.objects.filter(branches__divisions__sections__projects2__isnull=False)

        # if there is a user param, further filter qs to what user can access
        if self.request.query_params.get("user"):
            qs = qs.filter(branches__divisions__sections__in=get_manageable_sections(self.request.user))
        return qs.distinct()


class DivisionListAPIView(ListAPIView):
    serializer_class = serializers.DivisionSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        qs = shared_models.Division.objects.filter(sections__projects2__isnull=False).distinct()
        # if there is a user param, further filter qs to what user can access
        if self.request.query_params.get("user"):
            qs = qs.filter(sections__in=get_manageable_sections(self.request.user))

        if self.request.query_params.get("region"):
            qs = qs.filter(branch__region_id=self.request.query_params.get("region"))

        return qs.distinct()


class SectionListAPIView(ListAPIView):
    serializer_class = serializers.SectionSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        qs = shared_models.Section.objects.filter(projects2__isnull=False).distinct()
        if self.request.query_params.get("division"):
            qs = qs.filter(division_id=self.request.query_params.get("division"))
        elif self.request.query_params.get("region"):
            qs = qs.filter(division__branch__region_id=self.request.query_params.get("region"))

        # if there is a user param, further filter qs to what user can access
        if self.request.query_params.get("user"):
            qs = qs.filter(id__in=[s.id for s in get_manageable_sections(self.request.user)])
        return qs


# Reviews
##############
class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        year = models.ProjectYear.objects.get(pk=self.kwargs.get("project_year"))
        return year.agreements.all()

    def perform_create(self, serializer):
        my_review = serializer.save(
            project_year_id=self.kwargs.get("project_year"),
            last_modified_by=self.request.user
        )

        if self.request.data.get("approval_email_update"):
            my_review.send_approval_email(self.request)

        if self.request.data.get("review_email_update"):
            my_review.send_review_email(self.request)


class ReviewRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def perform_update(self, serializer):
        my_review = serializer.save(
            last_modified_by=self.request.user
        )

        if self.request.data.get("approval_email_update"):
            my_review.send_approval_email(self.request)

        if self.request.data.get("review_email_update"):
            my_review.send_review_email(self.request)


class ActivityModelMetaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    model = models.Activity

    def get(self, request):
        data = dict()
        data['labels'] = get_labels(self.model)
        data['type_choices'] = [dict(text=item[1], value=item[0]) for item in models.Activity.type_choices]
        data['likelihood_choices'] = [dict(text=item[1], value=item[0]) for item in models.Activity.likelihood_choices]
        data['impact_choices'] = [dict(text=item[1], value=item[0]) for item in models.Activity.impact_choices]
        data['risk_rating_choices'] = [dict(text=item[1], value=item[0]) for item in models.Activity.risk_rating_choices]
        return Response(data)


class OMCostModelMetaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    model = models.OMCost

    def get(self, request):
        data = dict()
        data['labels'] = get_labels(self.model)
        data['om_category_choices'] = [dict(text=item.id, value=str(item)) for item in models.OMCategory.objects.all()]
        return Response(data)
