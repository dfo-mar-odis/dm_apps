import json
import os
from copy import deepcopy

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, TextField, Q
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _, gettext_lazy

from shared_models import models as shared_models
from shared_models.views import CommonTemplateView, CommonCreateView, \
    CommonDetailView, CommonFilterView, CommonDeleteView, CommonUpdateView, CommonListView, CommonHardDeleteView, CommonFormsetView
from . import filters, forms, models, reports
from .mixins import CanModifyProjectRequiredMixin, AdminRequiredMixin, ManagerOrAdminRequiredMixin
from .utils import get_help_text_dict, \
    get_division_choices, get_section_choices, get_project_field_list, get_project_year_field_list, is_management_or_admin, \
    get_review_score_rubric, get_status_report_field_list, get_review_field_list


class IndexTemplateView(LoginRequiredMixin, CommonTemplateView):
    template_name = 'projects2/index.html'
    h1 = gettext_lazy("DFO Science Project Planning")
    active_page_name_crumb = gettext_lazy("Home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section_id_list = []
        if self.request.user.id:
            if self.request.user.groups.filter(name="projects_admin").count() > 0:
                section_id_list = [project.section_id for project in models.Project.objects.all()]
                section_list = shared_models.Section.objects.filter(id__in=section_id_list)
            else:
                pass
        context["is_management_or_admin"] = is_management_or_admin(self.request.user)
        context["reference_materials"] = models.ReferenceMaterial.objects.all()
        context["upcoming_dates"] = models.UpcomingDate.objects.filter(date__gte=timezone.now()).order_by("date")
        context["past_dates"] = models.UpcomingDate.objects.filter(date__lt=timezone.now()).order_by("date")
        context["upcoming_dates_field_list"] = [
            "date",
            "region",
            "tdescription|{}".format("description"),
        ]
        return context


# PROJECTS #
############


class ExploreProjectsTemplateView(LoginRequiredMixin, CommonTemplateView):
    h1 = gettext_lazy("Projects")
    template_name = 'projects2/explore_projects/main.html'
    home_url_name = "projects2:index"
    container_class = "container-fluid bg-light curvy"
    subtitle = gettext_lazy("Explore Projects")
    field_list = [
        'id',
        'title',
        'fiscal year',
        'status',
        # 'section',
        'default_funding_source',
        'functional_group',
        'lead_staff',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["random_project"] = models.Project.objects.first()
        context["status_choices"] = [dict(label=item[1], value=item[0]) for item in models.ProjectYear.status_choices]
        return context


class ManageProjectsTemplateView(ManagerOrAdminRequiredMixin, CommonTemplateView):
    h1 = gettext_lazy("Projects")
    template_name = 'projects2/manage_projects/main.html'
    home_url_name = "projects2:index"
    container_class = "container-fluid bg-light curvy"
    subtitle = gettext_lazy("Manage Projects")
    field_list = [
        'id',
        'fiscal year',
        'title',
        # 'section',
        'default_funding_source',
        'functional_group',
        'lead_staff',
        'status',
        'allocated_budget',
        'review_score_percentage',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["random_project"] = models.Project.objects.first()
        context["status_choices"] = [dict(label=item[1], value=item[0]) for item in models.ProjectYear.status_choices]
        context["review_form"] = forms.ReviewForm
        context["approval_form"] = forms.ApprovalForm
        context["review_score_rubric"] = json.dumps(get_review_score_rubric())
        return context


class MyProjectListView(LoginRequiredMixin, CommonListView):
    template_name = 'projects2/my_project_list.html'
    h1 = gettext_lazy("My Projects")
    home_url_name = "projects2:index"
    container_class = "container-fluid bg-light curvy"
    row_object_url_name = "projects2:project_detail"
    new_object_url = reverse_lazy("projects2:project_new")
    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'section', "class": "", "width": ""},
        {"name": 'title', "class": "", "width": ""},
        {"name": 'start_date', "class": "", "width": "150px"},
        {"name": 'lead_staff', "class": "", "width": ""},
        {"name": 'fiscal_years|{}'.format(_("fiscal years")), "class": "", "width": ""},
        {"name": 'has_unsubmitted_years|{}'.format("has unsubmitted years?"), "class": "", "width": ""},
        {"name": 'is_hidden|{}'.format(_("hidden?")), "class": "", "width": ""},
        {"name": 'updated_at', "class": "", "width": "150px"},
    ]

    def get_queryset(self):
        project_ids = [staff.project_year.project_id for staff in self.request.user.staff_instances2.all()]
        return models.Project.objects.filter(id__in=project_ids).order_by("-updated_at", "title")


class ProjectCreateView(LoginRequiredMixin, CommonCreateView):
    model = models.Project
    form_class = forms.NewProjectForm
    home_url_name = "projects2:index"
    template_name = 'projects2/project_form.html'
    container_class = "container bg-light curvy"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()

        # here are the option objects we want to send in through context
        # only from the science branches of each region

        division_dict = {}
        for d in get_division_choices(all=True):
            my_division = shared_models.Division.objects.get(pk=d[0])
            division_dict[my_division.id] = {}
            division_dict[my_division.id]["display"] = "{} - {}".format(
                getattr(my_division.branch, _("name")),
                getattr(my_division, _("name")),
            )
            division_dict[my_division.id]["region_id"] = my_division.branch.region_id

        section_dict = {}
        for s in get_section_choices(all=True):
            my_section = shared_models.Section.objects.get(pk=s[0])
            section_dict[my_section.id] = {}
            section_dict[my_section.id]["display"] = str(my_section)
            section_dict[my_section.id]["division_id"] = my_section.division_id
        context['division_json'] = json.dumps(division_dict)
        context['section_json'] = json.dumps(section_dict)

        return context

    def form_valid(self, form):
        my_object = form.save(commit=False)
        # modifications to project instance before saving
        my_object.modified_by = self.request.user
        my_object.save()
        messages.success(self.request,
                         mark_safe(_(
                             "<span class='h4'>Your new project was created successfully! To get started, <b class='highlight'>add a new project year</b>.</span>")))
        return HttpResponseRedirect(reverse_lazy("projects2:project_detail", kwargs={"pk": my_object.id}))

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class ProjectDetailView(LoginRequiredMixin, CommonDetailView):
    model = models.Project
    template_name = 'projects2/project_detail/main.html'
    home_url_name = "projects2:index"
    container_class = "container-fluid bg-light curvy"

    # parent_crumb = {"title": _("My Projects"), "url": reverse_lazy("projects2:my_project_list")}

    def get_active_page_name_crumb(self):
        return str(self.get_object())

    def get_h1(self):
        mystr = str(self.get_object())
        return mystr

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()

        # If this is a gulf region project, only show the gulf region fields
        context["project_field_list"] = get_project_field_list(project)
        context["project_year_field_list"] = get_project_year_field_list()

        context["random_review"] = models.Review.objects.first()
        context["review_field_list"] = get_review_field_list()

        context["staff_form"] = forms.StaffForm
        context["random_staff"] = models.Staff.objects.first()

        context["om_cost_form"] = forms.OMCostForm
        context["random_om_cost"] = models.OMCost.objects.first()

        context["capital_cost_form"] = forms.CapitalCostForm
        context["random_capital_cost"] = models.CapitalCost.objects.first()

        context["gc_cost_form"] = forms.GCCostForm
        context["random_gc_cost"] = models.GCCost.objects.first()

        context["activity_form"] = forms.ActivityForm
        context["random_activity"] = models.Activity.objects.first()

        context["collaborator_form"] = forms.CollaboratorForm
        context["random_collaborator"] = models.Collaborator.objects.first()

        context["agreement_form"] = forms.AgreementForm
        context["random_agreement"] = models.CollaborativeAgreement.objects.first()

        context["status_report_form"] = forms.StatusReportForm(initial={"user": self.request.user}, instance=project)
        context["random_status_report"] = models.StatusReport.objects.first()

        context["file_form"] = forms.FileForm
        context["random_file"] = models.File.objects.first()

        context["btn_class_1"] = "create-btn"
        # context["files"] = project.files.all()
        # context["financial_summary_dict"] = financial_summary_data(project)

        # Determine if the user will be able to edit the project.
        # context["can_edit"] = can_modify_project(self.request.user, project.id)
        # context["is_lead"] = self.request.user in [staff.user for staff in project.staff_members.filter(lead=True)]
        return context


class ProjectUpdateView(CanModifyProjectRequiredMixin, CommonUpdateView):
    model = models.Project
    form_class = forms.ProjectForm
    template_name = 'projects2/project_form.html'
    home_url_name = "projects2:index"
    container_class = "container bg-light curvy"

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse_lazy("projects2:project_detail", args=[self.get_object().id])}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()
        return context

    def get_initial(self):
        return dict(modified_by=self.request.user)


class ProjectDeleteView(CanModifyProjectRequiredMixin, CommonDeleteView):
    model = models.Project
    delete_protection = False
    home_url_name = "projects2:index"
    success_url = reverse_lazy("projects2:index")
    template_name = "projects2/confirm_delete.html"
    container_class = "container bg-light curvy"

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse_lazy("projects2:project_detail", args=[self.get_object().id])}


class ProjectCloneView(ProjectUpdateView):
    template_name = 'projects2/project_form.html'

    def get_h1(self):
        return _("Cloning: ") + str(self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cloning"] = True
        return context

    def test_func(self):
        return self.request.user.is_authenticated

    def get_initial(self):
        obj = self.get_object()
        init = super().get_initial()
        init["title"] = f"CLONE OF: {obj.title}"
        init["cloning"] = True
        return init

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        old_obj = models.Project.objects.get(pk=new_obj.pk)

        new_obj.project = new_obj
        new_obj.pk = None
        new_obj.save()

        for t in old_obj.tags.all():
            new_obj.tags.add(t)

        # for each year of old project, clone into new project...
        for old_year in old_obj.years.all():
            new_year = deepcopy(old_year)

            new_year.project = new_obj
            new_year.pk = None
            new_year.submitted = None
            new_year.status = 1
            new_year.approval_notification_email_sent = None
            new_year.save()

            # Now we need to replicate all the related records:
            # 1) staff
            for old_rel_obj in old_year.staff_set.all():
                new_rel_obj = deepcopy(old_rel_obj)
                new_rel_obj.pk = None
                new_rel_obj.project_year = new_year
                new_rel_obj.save()

            # we have to just make sure that the user is a lead on the project. Otherwise they will not be able to edit.
            my_staff, created = models.Staff.objects.get_or_create(
                user=self.request.user,
                project_year=new_year,
                employee_type_id=1,
            )
            my_staff.lead = True
            my_staff.save()

            # 2) O&M
            for old_rel_obj in old_year.omcost_set.all():
                new_rel_obj = deepcopy(old_rel_obj)
                new_rel_obj.pk = None
                new_rel_obj.project_year = new_year
                new_rel_obj.save()

            # 3) Capital
            for old_rel_obj in old_year.capitalcost_set.all():
                new_rel_obj = deepcopy(old_rel_obj)
                new_rel_obj.pk = None
                new_rel_obj.project_year = new_year
                new_rel_obj.save()

            # 4) G&C
            for old_rel_obj in old_year.gc_costs.all():
                new_rel_obj = deepcopy(old_rel_obj)
                new_rel_obj.pk = None
                new_rel_obj.project_year = new_year
                new_rel_obj.save()

            # 5) Collaborators and Partners
            for old_rel_obj in old_year.collaborators.all():
                new_rel_obj = deepcopy(old_rel_obj)
                new_rel_obj.pk = None
                new_rel_obj.project_year = new_year
                new_rel_obj.save()

            # 6) Collaborative Agreements
            for old_rel_obj in old_year.agreements.all():
                new_rel_obj = deepcopy(old_rel_obj)
                new_rel_obj.pk = None
                new_rel_obj.project_year = new_year
                new_rel_obj.save()

            # 7) Activities
            for old_rel_obj in old_year.activities.all():
                new_rel_obj = deepcopy(old_rel_obj)
                new_rel_obj.pk = None
                new_rel_obj.project_year = new_year
                new_rel_obj.target_date = None  # clear the target date
                new_rel_obj.save()

        return HttpResponseRedirect(reverse_lazy("projects2:project_detail", kwargs={"pk": new_obj.project.id}))


# PROJECT YEAR #
################


class ProjectYearCreateView(CanModifyProjectRequiredMixin, CommonCreateView):
    model = models.ProjectYear
    form_class = forms.ProjectYearForm
    home_url_name = "projects2:index"
    template_name = 'projects2/project_year_form.html'
    container_class = "container bg-light curvy"

    def get_initial(self):
        # this is an important method to keep since it is accessed by the Form class 
        # TODO: TEST ME
        return dict(project=self.get_project())

    def get_project(self):
        return models.Project.objects.get(pk=self.kwargs["project"])

    def get_parent_crumb(self):
        return {"title": self.get_project(), "url": reverse_lazy("projects2:project_detail", args=[self.get_project().id])}

    def form_valid(self, form):
        year = form.save(commit=False)
        year.modified_by = self.request.user
        year.save()

        # for good measure, we should add the current user as a staff to this year
        models.Staff.objects.create(
            project_year=year,
            user=self.request.user,
            employee_type=models.EmployeeType.objects.get(pk=1),
            is_lead=True,
        )

        return HttpResponseRedirect(
            super().get_success_url() + f"?project_year={year.id}"
        )


class ProjectYearUpdateView(CanModifyProjectRequiredMixin, CommonUpdateView):
    model = models.ProjectYear
    form_class = forms.ProjectYearForm
    home_url_name = "projects2:index"
    template_name = 'projects2/project_year_form.html'
    container_class = "container bg-light curvy"

    def get_h1(self):
        return _("Edit ") + str(self.get_object())

    def get_project(self):
        return self.get_object().project

    def get_parent_crumb(self):
        return {"title": self.get_project(), "url": reverse_lazy("projects2:project_detail", args=[self.get_project().id])}

    def form_valid(self, form):
        year = form.save(commit=False)
        year.modified_by = self.request.user
        year.save()
        return super().form_valid(form)

    def get_success_url(self):
        return super().get_success_url() + f"?project_year={self.get_object().id}"


class ProjectYearDeleteView(CanModifyProjectRequiredMixin, CommonDeleteView):
    model = models.ProjectYear
    delete_protection = False
    home_url_name = "projects2:index"
    template_name = "projects2/confirm_delete.html"
    container_class = "container bg-light curvy"

    def get_grandparent_crumb(self):
        return {"title": self.get_project(), "url": reverse("projects2:project_detail", args=[self.get_project().id])}

    def get_project(self):
        return self.get_object().project

    def delete(self, request, *args, **kwargs):
        project = self.get_project()
        self.get_object().delete()
        project.save()
        return HttpResponseRedirect(reverse("projects2:project_detail", args=[project.id]))


class ProjectYearCloneView(ProjectYearUpdateView):
    template_name = 'projects2/project_year_form.html'

    def get_h1(self):
        return _("Cloning: ") + str(self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cloning"] = True
        return context

    def test_func(self):
        return self.request.user.is_authenticated

    def get_initial(self):
        init = super().get_initial()
        init["start_date"] = timezone.now()
        init["cloning"] = True
        return init

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        old_obj = models.ProjectYear.objects.get(pk=new_obj.pk)

        new_obj.pk = None
        new_obj.submitted = None
        new_obj.status = 1
        new_obj.approval_notification_email_sent = None
        new_obj.save()

        # Now we need to replicate all the related records:
        # 1) staff
        for old_rel_obj in old_obj.staff_set.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project_year = new_obj
            new_rel_obj.save()

        # we have to just make sure that the user is a lead on the project. Otherwise they will not be able to edit.
        my_staff, created = models.Staff.objects.get_or_create(
            user=self.request.user,
            project_year=new_obj,
            employee_type_id=1,
        )
        my_staff.lead = True
        my_staff.save()

        # 2) O&M
        for old_rel_obj in old_obj.omcost_set.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project_year = new_obj
            new_rel_obj.save()

        # 3) Capital
        for old_rel_obj in old_obj.capitalcost_set.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project_year = new_obj
            new_rel_obj.save()

        # 4) G&C
        for old_rel_obj in old_obj.gc_costs.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project_year = new_obj
            new_rel_obj.save()

        # 5) Collaborators and Partners
        for old_rel_obj in old_obj.collaborators.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project_year = new_obj
            new_rel_obj.save()

        # 6) Collaborative Agreements
        for old_rel_obj in old_obj.agreements.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project_year = new_obj
            new_rel_obj.save()

        # 7) Activities
        for old_rel_obj in old_obj.activities.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project_year = new_obj
            new_rel_obj.target_date = None  # clear the target date
            new_rel_obj.save()

        return HttpResponseRedirect(reverse_lazy("projects2:project_detail", kwargs={"pk": new_obj.project.id}))


# FUNCTIONAL GROUPS #
#####################

class FunctionalGroupListView(AdminRequiredMixin, CommonFilterView):
    template_name = 'projects2/list.html'
    filterset_class = filters.FunctionalGroupFilter
    home_url_name = "projects2:index"
    new_object_url = reverse_lazy("projects2:group_new")
    row_object_url_name = row_ = "projects2:group_edit"
    container_class = "container-fluid bg-light curvy"

    field_list = [
        {"name": 'tname|{}'.format("name"), "class": "", "width": ""},
        {"name": 'theme', "class": "", "width": ""},
        {"name": 'sections', "class": "", "width": "600px"},
    ]

    def get_queryset(self):
        return models.FunctionalGroup.objects.annotate(
            search_term=Concat('name', Value(" "), 'nom', Value(" "), output_field=TextField()))


class FunctionalGroupUpdateView(AdminRequiredMixin, CommonUpdateView):
    model = models.FunctionalGroup
    form_class = forms.FunctionalGroupForm
    template_name = 'projects2/form.html'
    home_url_name = "projects2:index"
    parent_crumb = {"title": gettext_lazy("Functional Groups"), "url": reverse_lazy("projects2:group_list")}
    container_class = "container bg-light curvy"


class FunctionalGroupCreateView(AdminRequiredMixin, CommonCreateView):
    model = models.FunctionalGroup
    form_class = forms.FunctionalGroupForm
    success_url = reverse_lazy('projects2:group_list')
    template_name = 'projects2/form.html'
    home_url_name = "projects2:index"
    parent_crumb = {"title": gettext_lazy("Functional Groups"), "url": reverse_lazy("projects2:group_list")}
    container_class = "container bg-light curvy"


class FunctionalGroupDeleteView(AdminRequiredMixin, CommonDeleteView):
    model = models.FunctionalGroup
    success_url = reverse_lazy('projects2:group_list')
    success_message = 'The functional group was successfully deleted!'
    template_name = 'projects2/confirm_delete.html'
    container_class = "container bg-light curvy"


# SETTINGS #
############
class FundingSourceHardDeleteView(AdminRequiredMixin, CommonHardDeleteView):
    model = models.FundingSource
    success_url = reverse_lazy("projects2:manage_funding_sources")


class FundingSourceFormsetView(AdminRequiredMixin, CommonFormsetView):
    template_name = 'projects2/formset.html'
    h1 = "Manage Funding Source"
    queryset = models.FundingSource.objects.all()
    formset_class = forms.FundingSourceFormset
    success_url = reverse_lazy("projects2:manage_funding_sources")
    home_url_name = "projects2:index"
    delete_url_name = "projects2:delete_funding_source"
    container_class = "container bg-light curvy"


class OMCategoryHardDeleteView(AdminRequiredMixin, CommonHardDeleteView):
    model = models.OMCategory
    success_url = reverse_lazy("projects2:manage_om_cats")


class OMCategoryFormsetView(AdminRequiredMixin, CommonFormsetView):
    template_name = 'projects2/formset.html'
    h1 = "Manage OMCategory"
    queryset = models.OMCategory.objects.all()
    formset_class = forms.OMCategoryFormset
    success_url = reverse_lazy("projects2:manage_om_cats")
    home_url_name = "projects2:index"
    delete_url_name = "projects2:delete_om_cat"
    container_class = "container bg-light curvy"


class EmployeeTypeHardDeleteView(AdminRequiredMixin, CommonHardDeleteView):
    model = models.EmployeeType
    success_url = reverse_lazy("projects2:manage_employee_types")


class EmployeeTypeFormsetView(AdminRequiredMixin, CommonFormsetView):
    template_name = 'projects2/formset.html'
    h1 = "Manage Employee Type"
    queryset = models.EmployeeType.objects.all()
    formset_class = forms.EmployeeTypeFormset
    success_url = reverse_lazy("projects2:manage_employee_types")
    home_url_name = "projects2:index"
    delete_url_name = "projects2:delete_employee_type"
    container_class = "container bg-light curvy"


class TagHardDeleteView(AdminRequiredMixin, CommonHardDeleteView):
    model = models.Tag
    success_url = reverse_lazy("projects2:manage_tags")


class TagFormsetView(AdminRequiredMixin, CommonFormsetView):
    template_name = 'projects2/formset.html'
    h1 = "Manage Tag"
    queryset = models.Tag.objects.all()
    formset_class = forms.TagFormset
    success_url = reverse_lazy("projects2:manage_tags")
    home_url_name = "projects2:index"
    delete_url_name = "projects2:delete_tag"
    container_class = "container bg-light curvy"


class HelpTextHardDeleteView(AdminRequiredMixin, CommonHardDeleteView):
    model = models.HelpText
    success_url = reverse_lazy("projects2:manage_help_text")


class HelpTextFormsetView(AdminRequiredMixin, CommonFormsetView):
    template_name = 'projects2/formset.html'
    h1 = "Manage Help Text"
    queryset = models.HelpText.objects.all()
    formset_class = forms.HelpTextFormset
    success_url = reverse_lazy("projects2:manage_help_text")
    home_url_name = "projects2:index"
    delete_url_name = "projects2:delete_help_text"
    container_class = "container bg-light curvy"


class LevelHardDeleteView(AdminRequiredMixin, CommonHardDeleteView):
    model = models.Level
    success_url = reverse_lazy("projects2:manage_levels")


class LevelFormsetView(AdminRequiredMixin, CommonFormsetView):
    template_name = 'projects2/formset.html'
    h1 = "Manage Level"
    queryset = models.Level.objects.all()
    formset_class = forms.LevelFormset
    success_url = reverse_lazy("projects2:manage_levels")
    home_url_name = "projects2:index"
    delete_url_name = "projects2:delete_level"
    container_class = "container bg-light curvy"


class ActivityTypeHardDeleteView(AdminRequiredMixin, CommonHardDeleteView):
    model = models.ActivityType
    success_url = reverse_lazy("projects2:manage_activity_types")


class ActivityTypeFormsetView(AdminRequiredMixin, CommonFormsetView):
    template_name = 'projects2/formset.html'
    h1 = "Manage Activity Type"
    queryset = models.ActivityType.objects.all()
    formset_class = forms.ActivityTypeFormset
    success_url = reverse_lazy("projects2:manage_activity_types")
    home_url_name = "projects2:index"
    delete_url_name = "projects2:delete_activity_type"
    container_class = "container bg-light curvy"


class ThemeHardDeleteView(AdminRequiredMixin, CommonHardDeleteView):
    model = models.Theme
    success_url = reverse_lazy("projects2:manage_themes")


class ThemeFormsetView(AdminRequiredMixin, CommonFormsetView):
    template_name = 'projects2/formset.html'
    h1 = "Manage Theme"
    queryset = models.Theme.objects.all()
    formset_class = forms.ThemeFormset
    success_url = reverse_lazy("projects2:manage_themes")
    home_url_name = "projects2:index"
    delete_url_name = "projects2:delete_theme"
    container_class = "container bg-light curvy"


class UpcomingDateHardDeleteView(AdminRequiredMixin, CommonHardDeleteView):
    model = models.UpcomingDate
    success_url = reverse_lazy("projects2:manage-upcoming-dates")


class UpcomingDateFormsetView(AdminRequiredMixin, CommonFormsetView):
    template_name = 'projects2/formset.html'
    h1 = "Manage Upcoming Dates"
    queryset = models.UpcomingDate.objects.all()
    formset_class = forms.UpcomingDateFormset
    success_url = reverse_lazy("projects2:manage-upcoming-dates")
    home_url_name = "projects2:index"
    delete_url_name = "projects2:delete-upcoming-date"
    container_class = "container bg-light curvy"


# Reference Materials
class ReferenceMaterialListView(AdminRequiredMixin, CommonListView):
    template_name = "projects2/list.html"
    model = models.ReferenceMaterial
    field_list = [
        {"name": "tname|{}".format(gettext_lazy("name")), "class": "", "width": ""},
        {"name": "region", "class": "", "width": ""},
        {"name": "file_display_en|{}".format(gettext_lazy("File attachment (EN)")), "class": "", "width": ""},
        {"name": "file_display_fr|{}".format(gettext_lazy("File attachment (FR)")), "class": "", "width": ""},
        {"name": "date_created", "class": "", "width": ""},
        {"name": "date_modified", "class": "", "width": ""},
    ]
    new_object_url_name = "projects2:ref_mat_new"
    row_object_url_name = "projects2:ref_mat_edit"
    home_url_name = "projects2:index"
    h1 = gettext_lazy("Reference Materials")
    container_class = "container bg-light curvy"


class ReferenceMaterialUpdateView(AdminRequiredMixin, CommonUpdateView):
    model = models.ReferenceMaterial
    form_class = forms.ReferenceMaterialForm
    home_url_name = "projects2:index"
    parent_crumb = {"title": _("Reference Materials"), "url": reverse_lazy("projects2:ref_mat_list")}
    template_name = "projects2/form.html"
    is_multipart_form_data = True
    container_class = "container bg-light curvy"

    def get_delete_url(self):
        return reverse("projects2:ref_mat_delete", args=[self.get_object().id])


class ReferenceMaterialCreateView(AdminRequiredMixin, CommonCreateView):
    model = models.ReferenceMaterial
    form_class = forms.ReferenceMaterialForm
    home_url_name = "projects2:index"
    parent_crumb = {"title": _("Reference Materials"), "url": reverse_lazy("projects2:ref_mat_list")}
    template_name = "projects2/form.html"
    is_multipart_form_data = True
    container_class = "container bg-light curvy"


class ReferenceMaterialDeleteView(AdminRequiredMixin, CommonDeleteView):
    model = models.ReferenceMaterial
    success_url = reverse_lazy('projects2:ref_mat_list')
    home_url_name = "projects2:index"
    parent_crumb = {"title": _("Reference Materials"), "url": reverse_lazy("projects2:ref_mat_list")}
    template_name = "projects2/confirm_delete.html"
    delete_protection = False
    container_class = "container bg-light curvy"


# ADMIN


class AdminStaffListView(ManagerOrAdminRequiredMixin, CommonFilterView):
    template_name = 'projects2/admin_staff_list.html'

    filterset_class = filters.StaffFilter
    home_url_name = "projects2:index"
    h1 = gettext_lazy("Non-registered Staff List")
    h2 = gettext_lazy(
        "The purpose of this list view is to check if any DFO staff were listed on projects, but were not connected to their dmapps user accounts")
    field_list = [
        {"name": 'project_year.fiscal_year', "class": "", "width": ""},
        {"name": 'smart_name|staff name', "class": "", "width": ""},
        {"name": 'is_lead', "class": "", "width": ""},
        {"name": 'employee_type', "class": "", "width": ""},
    ]
    row_object_url_name = "projects2:admin_staff_edit"

    def get_queryset(self):
        qs = models.Staff.objects.filter(user__isnull=True, name__isnull=False).filter(~Q(name__icontains="unknown")).filter(~Q(name__icontains="tbd")).filter(
            ~Q(name__icontains="BI-")).filter(~Q(name__icontains="PC-")).filter(~Q(name__icontains="EG-")).filter(~Q(name__icontains="determined"))

        qs = qs.order_by('-project_year__fiscal_year', 'project_year__project__section__division', 'project_year__project__section',
                         'project_year__project__title')
        return qs


class AdminStaffUpdateView(ManagerOrAdminRequiredMixin, CommonUpdateView):
    '''This is really just for the admin view'''
    model = models.Staff
    template_name = 'projects2/admin_staff_form.html'
    form_class = forms.AdminStaffForm
    h1 = gettext_lazy("Edit Non-registered Staff Member")
    parent_crumb = {"title": _("Non-registered Staff List"), "url": reverse_lazy("projects2:admin_staff_list")}
    container_class = "container bg-light curvy"

    def form_valid(self, form):
        form.save()
        success_url = reverse("projects2:admin_staff_list")
        if self.request.META["QUERY_STRING"]:
            success_url += f"?{self.request.META['QUERY_STRING']}"
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()
        return context


# STATUS REPORT #
#################


class StatusReportDeleteView(CanModifyProjectRequiredMixin, CommonDeleteView):
    template_name = "projects2/confirm_delete.html"
    model = models.StatusReport
    container_class = "container bg-light curvy"
    delete_protection = False

    def get_project_year(self):
        return self.get_object().project_year

    def get_success_url(self, **kwargs):
        return reverse_lazy("shared_models:close_me")

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("projects2:report_detail", args=[self.get_object().id])}

    def get_grandparent_crumb(self):
        return {"title": str(self.get_project_year().project), "url": reverse_lazy("projects2:project_detail", args=[
            self.get_project_year().project.id]) + f"?project_year={self.get_project_year().id}"}


class StatusReportDetailView(LoginRequiredMixin, CommonDetailView):
    model = models.StatusReport
    home_url_name = "projects2:index"
    template_name = "projects2/status_report/main.html"
    field_list = get_status_report_field_list()

    def dispatch(self, request, *args, **kwargs):
        # when the view loads, let's make sure that all the activities are on the project.
        my_object = self.get_object()
        my_project_year = my_object.project_year
        for activity in my_project_year.activities.all():
            my_update, created = models.ActivityUpdate.objects.get_or_create(
                activity=activity,
                status_report=my_object
            )
            # if the update is being created, what should be the starting status?
            # to know, we would have to look and see if there is another report. if there is, we should grab the penultimate report and copy status from there.
            if created:
                # check to see if there is another update on the same activity. We can do this since activities are unique to projects.
                if activity.updates.count() > 1:
                    # if there are more than just 1 (i.e. the one we just created), it will be the second record we are interested in...
                    last_update = activity.updates.all()[1]
                    my_update.status = last_update.status
                    my_update.save()

        return super().dispatch(request, *args, **kwargs)

    def get_project_year(self):
        return self.get_object().project_year

    def get_parent_crumb(self):
        return {"title": str(self.get_project_year().project), "url": reverse_lazy("projects2:project_detail", args=[
            self.get_project_year().project.id]) + f"?project_year={self.get_project_year().id}"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_report = self.get_object()
        context['files'] = my_report.files.all()
        context['file_form'] = forms.FileForm
        context["random_file"] = models.File.objects.first()
        context['update_form'] = forms.ActivityUpdateForm
        context["random_update"] = models.ActivityUpdate.objects.first()

        return context


class StatusReportUpdateView(CanModifyProjectRequiredMixin, CommonUpdateView):
    model = models.StatusReport
    form_class = forms.StatusReportForm
    home_url_name = "projects2:index"
    parent_crumb = {"title": _("Reference Materials"), "url": reverse_lazy("projects2:report_list")}
    template_name = "projects2/form.html"
    is_multipart_form_data = True
    container_class = "container bg-light curvy"

    def get_project_year(self):
        return self.get_object().project_year

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("projects2:report_detail", args=[self.get_object().id])}

    def get_grandparent_crumb(self):
        return {"title": str(self.get_project_year().project), "url": reverse_lazy("projects2:project_detail", args=[
            self.get_project_year().project.id]) + f"?project_year={self.get_project_year().id}"}

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.modified_by = self.request.user
        obj.save()
        return super().form_valid(form)


class StatusReportReviewUpdateView(ManagerOrAdminRequiredMixin, StatusReportUpdateView):
    form_class = forms.StatusReportReviewForm
    h1 = gettext_lazy("Please provide review comments")
    container_class = "container-fluid"


class StatusReportPrintDetailView(LoginRequiredMixin, CommonDetailView):
    template_name = "projects2/status_report_pdf.html"
    model = models.StatusReport

    def get_h2(self):
        return f'{self.get_project_year().project} ({self.get_project_year()})'

    def get_project_year(self):
        return self.get_object().project_year

    def get_parent_crumb(self):
        return {"title": str(self.get_project_year().project), "url": reverse_lazy("projects2:project_detail", args=[
            self.get_project_year().project.id]) + f"?project_year={self.get_project_year().id}"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_report = get_object_or_404(models.StatusReport, pk=self.kwargs["pk"])
        context["object"] = my_report

        context["random_file"] = models.File.objects.first()
        context["random_update"] = models.ActivityUpdate.objects.first()

        return context


@login_required()
def export_acrdp_application(request, pk):
    project = get_object_or_404(models.Project, pk=pk)

    # check if the project lead's profile is up-to-date
    if not project.lead_staff.exists():
        messages.error(request, _("Warning: There are no lead staff on this project!!"))
    else:
        if not project.lead_staff.first().user.profile.tposition:
            messages.error(request, _("Warning: project lead's profile information is missing in DM Apps (position title)"))
        if not project.lead_staff.first().user.profile.phone:
            messages.error(request, _("Warning: project lead's profile information is missing in DM Apps (phone number)"))
    file_url = reports.generate_acrdp_application(project)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-word")
            response['Content-Disposition'] = f'inline; filename="ACRDP application (Project ID {project.id}).docx"'
            return response
    raise Http404


@login_required()
def export_acrdp_budget(request, pk):
    project = get_object_or_404(models.Project, pk=pk)

    # check if the project lead's profile is up-to-date
    if project.lead_staff.first() and not project.lead_staff.first().user.profile.tposition:
        messages.error(request, _("Warning: project lead's profile information is missing in DM Apps (position title)"))
    if project.lead_staff.first() and not project.lead_staff.first().user.profile.phone:
        messages.error(request, _("Warning: project lead's profile information is missing in DM Apps (phone number)"))
    file_url = reports.generate_acrdp_budget(project)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = f'inline; filename="ACRDP Budget (Project ID {project.id}).xls"'
            return response
    raise Http404
