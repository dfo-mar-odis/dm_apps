import os

from azure.storage.blob import BlockBlobService
from decouple import config
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from django.db.models import Sum, Q, Value, TextField
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_lazy
###
from easy_pdf.views import PDFTemplateView
from msrestazure.azure_active_directory import MSIAuthentication

from dm_apps.context_processor import my_envr
from dm_apps.utils import compare_strings
from lib.functions.custom_functions import fiscal_year
from lib.templatetags.custom_filters import nz
from shared_models import models as shared_models
from shared_models.views import CommonFormsetView, CommonHardDeleteView, CommonUpdateView, CommonFilterView, CommonFormView, \
    CommonPopoutFormView, CommonListView, CommonDetailView, CommonTemplateView, CommonCreateView, CommonDeleteView
from . import emails
from . import filters
from . import forms
from . import models
from . import reports
from . import utils
from .mixins import TravelAccessRequiredMixin, CanModifyMixin, TravelAdminRequiredMixin, AdminOrApproverRequiredMixin, TravelADMAdminRequiredMixin
from .utils import in_travel_admin_group, in_adm_admin_group, can_modify_request, is_approver, is_trip_approver, is_manager_or_assistant_or_admin


def get_file(request, file):
    if request.GET.get("reference"):
        my_file = models.ReferenceMaterial.objects.get(pk=int(file))
        blob_name = my_file.tfile
        export_file_name = blob_name
    elif request.GET.get("blob_name"):
        blob_name = file.replace("||", "/")
        export_file_name = blob_name.split("/")[-1]
        if request.GET.get("export_file_name"):
            export_file_name = request.GET.get("export_file_name")
    else:
        my_file = models.File.objects.get(pk=int(file))
        blob_name = my_file.file
        export_file_name = blob_name

    if settings.AZURE_STORAGE_ACCOUNT_NAME:
        AZURE_STORAGE_ACCOUNT_NAME = settings.AZURE_STORAGE_ACCOUNT_NAME
        AZURE_MSI_CLIENT_ID = config("AZURE_MSI_CLIENT_ID", cast=str, default="")
        account_key = config("AZURE_STORAGE_SECRET_KEY", default=None)
        try:
            token_credential = MSIAuthentication(resource=f'https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net', client_id=AZURE_MSI_CLIENT_ID)
        except Exception as E:
            print(E)
            token_credential = None
        blobService = BlockBlobService(account_name=AZURE_STORAGE_ACCOUNT_NAME, token_credential=token_credential, account_key=account_key)
        blob_file = blobService.get_blob_to_bytes("media", blob_name)
        response = HttpResponse(blob_file.content, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{export_file_name}"'
    else:
        response = HttpResponse(blob_name.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{export_file_name}"'

    return response


def get_conf_details(request):
    """ used exclusively for the request_form but should be phased out with REST Api"""
    conf_dict = {}
    qs = models.Trip.objects.filter(start_date__gte=timezone.now())
    for conf in qs:
        conf_dict[conf.id] = {}
        conf_dict[conf.id]['location'] = conf.location
        conf_dict[conf.id]['start_date'] = conf.start_date.strftime("%Y-%m-%d")
        conf_dict[conf.id]['end_date'] = conf.end_date.strftime("%Y-%m-%d")
        if conf.date_eligible_for_adm_review and timezone.now() > conf.date_eligible_for_adm_review:
            conf_dict[conf.id]['is_late_request'] = True
        else:
            conf_dict[conf.id]['is_late_request'] = False
    return JsonResponse(conf_dict)


class IndexTemplateView(TravelAccessRequiredMixin, CommonTemplateView):
    template_name = 'travel/index/main.html'
    active_page_name_crumb = gettext_lazy("Home")
    h1 = " "

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["processes"] = [
            models.ProcessStep.objects.filter(stage=1),
            models.ProcessStep.objects.filter(stage=2)
        ]
        context["information_sections"] = models.ProcessStep.objects.filter(stage=0, is_visible=True)
        # context["faqs"] = models.FAQ.objects.all()
        context["refs"] = models.ReferenceMaterial.objects.all()
        # context["region_tabs"] = [region.tname for region in shared_models.Region.objects.all()]

        context["is_admin"] = in_travel_admin_group(self.request.user)
        context["is_adm_admin"] = in_adm_admin_group(self.request.user)
        context["can_see_all_requests"] = is_manager_or_assistant_or_admin(self.request.user)
        return context


def get_help_text_dict():
    my_dict = {}
    for obj in models.HelpText.objects.all():
        my_dict[obj.field_name] = str(obj)

    return my_dict


# Requests #
################
class TripRequestListView(TravelAccessRequiredMixin, CommonTemplateView):
    template_name = 'travel/request_list/main.html'
    subtitle = gettext_lazy("Trip Requests")
    home_url_name = "travel:index"
    container_class = "container-fluid"
    row_object_url_name = "travel:request_detail"
    h1 = gettext_lazy("Trip Requests")
    field_list = [
        'fiscal_year',
        'created_by',
        'trip.tname|{}'.format(gettext_lazy("trip")),
        'trip.location|{}'.format(gettext_lazy("Destination")),
        'travellers|{}'.format(gettext_lazy("travellers")),
        'status',
        'section',
        'processing_time|{}'.format(gettext_lazy("Processing time")),
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = [dict(label=item[1], value=item[0]) for item in
                                     models.TripRequest.status_choices]  # when there is time, this should be replaced by api call
        return context

    def get_new_object_url(self):
        return reverse("travel:request_new")


class TripRequestDetailView(TravelAccessRequiredMixin, CommonDetailView):
    model = models.TripRequest
    template_name = 'travel/request_detail.html'
    home_url_name = "travel:index"

    def get_object(self, queryset=None):
        if self.kwargs.get("uuid"):
            return get_object_or_404(self.model, uuid=self.kwargs.get("uuid"))
        else:
            return super().get_object(queryset=None)

    def get_context_data(self, **kwargs):
        my_object = self.get_object()
        context = super().get_context_data(**kwargs)
        context["trip_request"] = self.get_object()
        # context['random_request_reviewer'] = models.Reviewer.objects.first()
        return context


class TripRequestUpdateView(CanModifyMixin, CommonUpdateView):
    model = models.TripRequest
    home_url_name = "travel:index"
    h1 = gettext_lazy("Edit Trip Request")
    template_name = 'travel/request_form.html'
    form_class = forms.TripRequestForm

    def get_initial(self):
        return {"reset_reviewers": False}

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("travel:request_detail", kwargs=self.kwargs) + self.get_query_string()}

    def form_valid(self, form):
        my_object = form.save(commit=False)
        # if by mistake there is no owner, assign one now
        if not my_object.created_by:
            my_object.created_by = self.request.user
        my_object.save()

        utils.manage_trip_warning(my_object.trip, self.request)

        # decide whether the reviewers should be reset
        if form.cleaned_data.get("reset_reviewers"):
            reset_request_reviewers(self.request, pk=my_object.pk)

        if form.cleaned_data.get("stay_on_page"):
            return HttpResponseRedirect(reverse_lazy("travel:request_edit", kwargs=self.kwargs) + self.get_query_string())
        else:
            return HttpResponseRedirect(reverse_lazy("travel:request_detail", kwargs=self.kwargs) + self.get_query_string())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()
        return context


class TripRequestCreateView(TravelAccessRequiredMixin, CommonCreateView):
    model = models.TripRequest
    home_url_name = "travel:index"
    h1 = gettext_lazy("New Trip Request")
    form_class = forms.TripRequestForm
    template_name = 'travel/request_form.html'

    def get_initial(self):
        if self.request.GET.get("trip"):
            return dict(trip=get_object_or_404(models.Trip, pk=self.request.GET.get("trip")))

    def form_valid(self, form):
        my_object = form.save(commit=False)
        my_object.created_by = self.request.user
        my_object.save()

        # add user as traveller if asked to
        if form.cleaned_data.get("is_traveller", None):
            # just make sure they are not already on another trip!!
            if not models.Traveller.objects.filter(request__trip=my_object.trip, user=self.request.user).exists():
                t = models.Traveller.objects.create(
                    request=my_object,
                    user=self.request.user,
                    start_date=my_object.trip.start_date,
                    end_date=my_object.trip.end_date,
                )
                utils.populate_traveller_costs(self.request, t)

        # add reviewers
        utils.get_request_reviewers(my_object)
        return HttpResponseRedirect(reverse_lazy("travel:request_detail", args=[my_object.id]) + self.get_query_string() + "#travellers_head")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()
        return context


class TripRequestDeleteView(CanModifyMixin, CommonDeleteView):
    model = models.TripRequest
    delete_protection = False
    home_url_name = "travel:index"
    template_name = 'travel/confirm_delete.html'

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("travel:request_detail", kwargs=self.kwargs) + self.get_query_string()}

    def get_success_url(self):
        return reverse("travel:request_list") + self.get_query_string()

    def delete(self, request, *args, **kwargs):
        my_object = self.get_object()
        my_object.delete()
        utils.manage_trip_warning(my_object.trip, self.request)
        return HttpResponseRedirect(self.get_success_url())


class TripRequestCloneUpdateView(TripRequestUpdateView):
    h1 = gettext_lazy("Clone a Trip Request")
    h2 = gettext_lazy("Please update the request details")

    def test_func(self):
        if self.request.user.id:
            return True

    def get_initial(self):
        my_object = models.TripRequest.objects.get(pk=self.kwargs["pk"])
        init = super().get_initial()
        init["year"] = fiscal_year(sap_style=True, next=True)
        init["user"] = self.request.user
        # init["created_by"] = self.request.user
        return init

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cloned"] = True
        return context

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        old_obj = models.TripRequest.objects.get(pk=new_obj.pk)
        new_obj.pk = None
        new_obj.status = 8
        new_obj.submitted = None
        new_obj.original_submission_date = None
        new_obj.created_by = self.request.user
        new_obj.admin_notes = None

        try:
            new_obj.save()
            utils.get_request_reviewers(new_obj)
        except IntegrityError:
            messages.error(self.request, _("sorry, cannot clone this trip because there is another trip request with the same user in the system"))
        return HttpResponseRedirect(reverse_lazy("travel:request_detail", kwargs={"pk": new_obj.id}) + self.get_query_string())


class TripRequestSubmitUpdateView(CanModifyMixin, CommonUpdateView):
    model = models.TripRequest
    form_class = forms.TripRequestTimestampUpdateForm
    template_name = 'travel/request_submit.html'
    submit_text = gettext_lazy("Proceed")
    home_url_name = "travel:index"

    def get_submit_text(self):
        my_object = self.get_object()
        if my_object.submitted or not my_object.is_late_request:
            return _("Proceed")
        else:
            return _("Proceed with late submission")

    def get_active_page_name_crumb(self):
        my_object = self.get_object()
        if my_object.submitted:
            return _("Un-submit request")
        else:
            return _("Re-submit request") if my_object.status == 16 else _("Submit request")

    def get_h1(self):
        my_object = self.get_object()

        if my_object.submitted:
            return _("Do you wish to un-submit the following request?")
        else:
            if not my_object.is_late_request:
                return _("Do you wish to re-submit the following request?") if my_object.status == 16 else _(
                    "Do you wish to submit the following request?")
            else:
                return _("Do you wish to re-submit the following late request?") if my_object.status == 16 else _(
                    "Do you wish to submit the following late request?")

    def get_h2(self):
        my_object = self.get_object()
        if my_object.submitted:
            return '<span class="red-font">WARNING: Un-submitting this request will reset the' \
                   ' status of any existing recommendations and/or approvals.</span>'

    def test_func(self):
        # This view is a little different. A trip owner should always be allowed to unsubmit
        return can_modify_request(self.request.user, self.kwargs.get("pk"), True)

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("travel:request_detail", kwargs=self.kwargs) + self.get_query_string()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip_request"] = self.get_object()
        return context

    def form_valid(self, form):
        my_object = form.save(commit=False)  # There is nothing really to save here. I am just using the machinery of UpdateView (djf)
        # figure out the current state of the request
        my_object.updated_by = self.request.user
        is_submitted = True if my_object.submitted else False

        # if submitted, then unsumbit but only if admin or owner
        if is_submitted:
            #  UNSUBMIT REQUEST
            if in_travel_admin_group(self.request.user) or my_object.created_by == self.request.user:
                my_object.unsubmit()
            else:
                messages.error(self.request, "sorry, only admins or owners can un-submit requests")
        else:
            if my_object.is_late_request:
                # if the user is submitting a late request, we have to tag NCR Travel Coordinator as the first reviewer
                ## get the NCR travel coordinator; reviewer_role = 3
                ncr_coord = models.DefaultReviewer.objects.filter(special_role=3).distinct().order_by("order")
                ## in the case that there is not an ncr travel coordinator, we cannot do this!
                if ncr_coord.exists():
                    reviewer, created = models.Reviewer.objects.get_or_create(
                        request=my_object,
                        user=ncr_coord.first().user,
                        role=3,
                    )
                    reviewer.order = -1000000
                    reviewer.save()

            #  SUBMIT REQUEST
            my_object.submit()

            # clean up any unused cost categories
            for traveller in my_object.travellers.all():
                utils.clear_empty_traveller_costs(traveller)

        # No matter what business was done, we will call this function to sort through reviewer and request statuses
        utils.approval_seeker(my_object, False, self.request)

        return HttpResponseRedirect(reverse("travel:request_detail", kwargs=self.kwargs) + self.get_query_string())


class TripRequestCancelUpdateView(TravelAdminRequiredMixin, CommonUpdateView):
    model = models.TripRequest
    form_class = forms.TripRequestAdminNotesForm
    template_name = 'travel/form.html'
    h1 = gettext_lazy("Do you wish to cancel the following trip request?")
    active_page_name_crumb = gettext_lazy("Cancel request")
    submit_text = gettext_lazy("Proceed")

    def get_h2(self):
        return "<span class='red-font blink-me'>" + \
               _("Please note that this action cannot be undone!!") + \
               "</span>"

    def get_h3(self):
        return str(self.get_object())

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("travel:request_detail", kwargs=self.kwargs) + self.get_query_string()}

    def get_context_data(self, **kwargs):
        my_object = self.get_object()
        # figure out the current state of the request
        # is_cancelled = True if my_object.status == 22 else False
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        my_trip_request = form.save(commit=False)
        my_trip_request.updated_by = self.request.user
        my_trip_request.save()

        # figure out the current state of the request
        is_cancelled = True if my_trip_request.status == 22 else False

        if is_cancelled:
            messages.warning(self.request, _("Sorry, it is currently not possible to cancel your cancellation "))
            return HttpResponseRedirect(reverse("travel:request_detail", kwargs=self.kwargs))

            # UN-CANCEL THE REQUEST
            # my_trip_request.status = 11
        else:
            #  CANCEL THE REQUEST
            my_trip_request.status = 22
            my_trip_request.save()

            # cancel any outstanding reviews:
            # but only those with the following statuses: PENDING = 1; QUEUED = 20;
            tr_reviewer_statuses_of_interest = [1, 20, ]
            for r in my_trip_request.reviewers.filter(status__in=tr_reviewer_statuses_of_interest):
                r.status = 5
                r.save()

            # send an email to the trip_request owner
            email = emails.StatusUpdateEmail(self.request, my_trip_request)
            email.send()
            return HttpResponseRedirect(reverse("travel:request_detail", kwargs=self.kwargs) + self.get_query_string())


# REQUEST REVIEWER #
####################

class RequestReviewerListView(TravelAccessRequiredMixin, CommonTemplateView):
    model = models.Reviewer
    template_name = 'travel/request_reviewer_list.html'
    home_url_name = "travel:index"
    h1 = " "
    active_page_name_crumb = gettext_lazy("Request reviews")

    def get_queryset(self):
        return utils.get_related_request_reviewers(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RequestReviewerUpdateView(AdminOrApproverRequiredMixin, CommonUpdateView):
    model = models.Reviewer
    form_class = forms.ReviewerApprovalForm
    template_name = 'travel/request_reviewer_update.html'
    home_url_name = "travel:index"

    def get_h1(self):
        if self.request.GET.get("rdg"):
            return _("Do you wish to approve on behalf of {user}".format(
                user=self.get_object().user,
            ))
        return _("Do you wish to approve the following request?")

    def get_h2(self):
        if self.request.GET.get("rdg"):
            return f"<span class='highlight py-1 px-1'>{self.get_object().get_role_display()}</span>"

    def get_parent_crumb(self):
        return {"title": _("Requests Awaiting Review"), "url": reverse("travel:request_reviewer_list") + self.get_query_string()}

    def test_func(self):
        reviewer = self.get_object()
        my_trip_request = reviewer.request
        my_user = self.request.user
        # if this is an rdg approval, then we make sure it is a travel admin
        if self.request.GET.get("rdg"):
            return in_travel_admin_group(my_user) and reviewer.role == 7
        # otherwise we make sure that this person is the current reviewer
        else:
            return is_approver(my_user, my_trip_request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip_request"] = self.get_object().request
        context['help_text_dict'] = get_help_text_dict()
        return context

    def form_valid(self, form):
        # don't save the reviewer yet because there are still changes to make
        my_reviewer = form.save(commit=True)

        approved = form.cleaned_data.get("approved")
        stay_on_page = form.cleaned_data.get("stay_on_page")
        changes_requested = form.cleaned_data.get("changes_requested")
        # first scenario: changes were requested for the request
        # in this case, the reviewer status does not change but the request status will
        if not stay_on_page:
            if changes_requested:
                my_reviewer.request.status = 16
                my_reviewer.request.submitted = None
                my_reviewer.request.save()
                # send an email to the request owner
                email = emails.ChangesRequestedEmail(self.request, my_reviewer.request)
                email.send()
                messages.success(self.request, _("Success! An email has been sent to the trip request owner."))

            # if it was approved, then we change the reviewer status to 'approved'
            elif approved:
                my_reviewer.status = 2
                my_reviewer.status_date = timezone.now()
                my_reviewer.save()
            # if it was not approved, then we change the reviewer status to 'denied'
            else:
                my_reviewer.status = 3
                my_reviewer.status_date = timezone.now()
                my_reviewer.save()

            # update any statuses if necessary
            utils.approval_seeker(my_reviewer.request, False, self.request)

        if stay_on_page:
            return HttpResponseRedirect(reverse("travel:request_reviewer_update", args=[my_reviewer.id]) + self.get_query_string() + "#id_comments")
        else:
            return HttpResponseRedirect(reverse("travel:request_reviewer_list") + self.get_query_string())


@login_required(login_url='/accounts/login/')
# @user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def reset_request_reviewers(request, pk):
    """this function will reset the reviewers on either a trip request"""
    my_obj = models.TripRequest.objects.get(pk=pk)
    if can_modify_request(request.user, pk):
        # This function should only ever be run if the TR is a draft
        if my_obj.status == 8:
            # first remove any existing reviewers
            my_obj.reviewers.all().delete()
            # next, re-add the defaults...
            utils.get_request_reviewers(my_obj)
        else:
            messages.error(request, _("This function can only be used when the trip request is still a draft"))
    else:
        messages.error(request, _("You do not have the permissions to reset the reviewer list"))
    return HttpResponseRedirect(reverse("travel:request_detail", args=(pk,)))


# TRIP #
########

class TripListView(TravelAccessRequiredMixin, CommonTemplateView):
    template_name = 'travel/trip_list/main.html'
    subtitle = gettext_lazy("Trips")
    home_url_name = "travel:index"
    container_class = "container-fluid"
    h1 = _("Trips")

    field_list = [
        'fiscal_year',
        'status',
        'trip_subcategory',
        'tname|{}'.format(gettext_lazy("title")),
        'location|{}'.format(_("location")),
        'lead|{}'.format(_("region")),
        'abstract_deadline|{}'.format(_("abstract deadline")),
        'registration_deadline',
        'dates|{}'.format(_("trip dates")),
        # 'is_adm_approval_required|{}'.format(_("ADM approval required?")),
        'date_eligible_for_adm_review',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["random_object"] = models.Trip.objects.first()
        context["status_choices"] = [dict(label=item[1], value=item[0]) for item in models.Trip.status_choices]
        context["subcategory_choices"] = [dict(label=item.tname, value=item.id) for item in models.TripSubcategory.objects.all()]
        return context

    def get_new_object_url(self):
        return reverse("travel:trip_new") + self.get_query_string()


class TripDetailView(TravelAccessRequiredMixin, CommonDetailView):
    model = models.Trip
    template_name = 'travel/trip_detail.html'
    home_url_name = "travel:index"

    def get_parent_crumb(self):
        return {"title": _("Trips"), "url": reverse_lazy("travel:trip_list") + self.get_query_string()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip"] = self.get_object()
        return context


class TripUpdateView(TravelAdminRequiredMixin, CommonUpdateView):
    model = models.Trip
    form_class = forms.TripForm
    home_url_name = "travel:index"

    def test_func(self):
        my_object = self.get_object()
        # this only user who should be able to modify an adm level trip is the travel_adm_admin
        if my_object.is_adm_approval_required:
            return utils.in_adm_admin_group(self.request.user)
        return utils.is_admin(self.request.user)

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse("travel:trip_detail", kwargs=self.kwargs) + self.get_query_string()}

    def get_template_names(self):
        return 'travel/trip_form_popout.html' if self.request.GET.get("pop") else 'travel/trip_form.html'

    def form_valid(self, form):
        my_object = form.save(commit=False)
        my_object.updated_by = self.request.user
        my_object.save()
        # This is a bit tricky here. Right now will work with the assumption that we do not ever want to reset the reviewers unless
        # the trip was ADM approval required, and now is not, OR if it wasn't and now it is.
        if my_object.is_adm_approval_required and my_object.reviewers.count() == 0 or not my_object.is_adm_approval_required:
            # Add any trip reviewers to the trip, if adm approval is required.
            # This function will also delete any reviewers if adm approval is not required
            utils.get_trip_reviewers(my_object)
        if self.request.GET.get("pop"):
            return HttpResponseRedirect(reverse("shared_models:close_me"))
        else:
            return HttpResponseRedirect(reverse('travel:trip_detail', kwargs=self.kwargs) + self.get_query_string())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()
        return context


class TripCloneView(TripUpdateView):
    h1 = gettext_lazy("Clone a Trip")
    h2 = gettext_lazy("Please update the trip details")

    def test_func(self):
        if self.request.user.id:
            return True

    def get_initial(self):
        my_object = models.Trip.objects.get(pk=self.kwargs["pk"])
        init = super().get_initial()
        init["name"] = "CLONE OF: " + my_object.name
        # init["created_by"] = self.request.user
        return init

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cloned"] = True
        return context

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        old_obj = models.Trip.objects.get(pk=new_obj.pk)
        new_obj.pk = None
        new_obj.verified_by = self.request.user
        new_obj.created_by = self.request.user
        new_obj.save()
        return HttpResponseRedirect(reverse_lazy("travel:trip_detail", args=[new_obj.id]) + self.get_query_string())


class TripCreateView(TravelAccessRequiredMixin, CommonCreateView):
    model = models.Trip
    form_class = forms.TripForm
    home_url_name = "travel:index"

    def get_template_names(self):
        return 'travel/trip_form_popout.html' if self.request.GET.get("pop") else 'travel/trip_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()
        return context

    def form_valid(self, form):
        my_object = form.save(commit=False)
        my_object.created_by = self.request.user
        my_object.save()
        # Add any trip reviewers to the trip, if adm approval is required
        utils.get_trip_reviewers(my_object)
        if self.request.GET.get("pop"):
            # create a new email object
            email = emails.NewTripEmail(self.request, my_object)
            email.send()
            return HttpResponseRedirect(reverse("shared_models:close_me_no_refresh"))
        else:
            return HttpResponseRedirect(reverse("travel:trip_detail", args=[my_object.id]) + self.get_query_string())


class TripDeleteView(TravelAdminRequiredMixin, CommonDeleteView):
    template_name = 'travel/confirm_delete.html'
    model = models.Trip
    success_message = 'The trip was deleted successfully!'
    delete_protection = False

    def test_func(self):
        my_object = self.get_object()
        # this only user who should be able to modify an adm level trip is the travel_adm_admin
        if my_object.is_adm_approval_required:
            return utils.in_adm_admin_group(self.request.user)
        return utils.is_admin(self.request.user)

    def get_success_url(self):
        return reverse("travel:index")


class TripReviewProcessUpdateView(TravelADMAdminRequiredMixin, CommonUpdateView):
    model = models.Trip
    form_class = forms.TripTimestampUpdateForm
    template_name = 'travel/form.html'
    submit_text = gettext_lazy("Proceed")

    def test_func(self):
        # make sure that this page can only be accessed for active trips (exclude those already reviewed and those canceled)
        return in_adm_admin_group(self.request.user) and not self.get_object().status in [43]

    def get_h1(self):
        if self.get_object().status in [30, 41]:
            return _("Do you wish to start a review on this trip?")
        elif self.get_object().status in [32]:
            return _("Do you wish to re-examine this trip?")
        else:
            return _("Do you wish to end the review of this trip?")

    def get_h2(self):
        if self.get_object().status in [30, 41]:
            return self.get_object()
        elif self.get_object().status in [32]:
            return '<span class="blue-font">Re-opening the review on this trip reset the reviewer statuses but ' \
                   'will keep any existing reviewer comments. <br><br> This process will NOT undo any trip request approvals that ' \
                   'have already been issued in the original review process.</span>'
        else:
            return '<span class="red-font">WARNING: <br><br> stopping the review on this trip will reset the' \
                   ' status of any existing recommendations and/or approvals.</span>'

    def get_subtitle(self):
        return _("Start a Review") if self.get_object().status in [30, 41] else _("End a Review")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip"] = self.get_object()
        return context

    def form_valid(self, form):
        my_trip = form.save()
        # figure out the current state of the request
        if my_trip.status in [30, 41]:
            is_under_review = False
        else:
            is_under_review = True

        if is_under_review:
            if my_trip.status == 32:
                utils.end_trip_review_process(my_trip, reset=True)
            else:
                utils.end_trip_review_process(my_trip, reset=False)
        else:
            # go and get approvals!!
            utils.start_trip_review_process(my_trip)
            # send out a warning email to all DFO science admins --> have to send emails individually because of aws limit
            to_list = utils.get_all_admins()
            for recip in to_list:
                email = emails.TripReviewEmail(self.request, my_trip, recip)
                email.send()

        # No matter what business what done, we will call this function to sort through reviewer and request statuses
        utils.trip_approval_seeker(my_trip, self.request)
        my_trip.save()

        # decide where to go. If the request user is the same as the active reviewer for the trip, go right to the review page.
        # otherwise go to the index
        if my_trip.current_reviewer and self.request.user == my_trip.current_reviewer.user:
            return HttpResponseRedirect(reverse("travel:trip_reviewer_update", args=[my_trip.current_reviewer.id]))
        else:
            return HttpResponseRedirect(reverse("travel:trip_detail", kwargs=self.kwargs) + self.get_query_string())


class TripVerifyUpdateView(TravelAdminRequiredMixin, CommonFormView):
    template_name = 'travel/trip_verification_form.html'
    model = models.Trip
    form_class = forms.TripTimestampUpdateForm
    home_url_name = "travel:index"
    h1 = gettext_lazy("Verify Trip")

    def test_func(self):
        my_object = models.Trip.objects.get(pk=self.kwargs.get("pk"))
        # this only user who should be able to modify an adm level trip is the travel_adm_admin
        if my_object.is_adm_approval_required:
            return utils.in_adm_admin_group(self.request.user)
        return utils.is_admin(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("accounts:denied_access", kwargs={
                "message": _("Sorry, only ADMO administrators can verify trips that require ADM approval.")}))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_trip = get_object_or_404(models.Trip, pk=self.kwargs.get("pk"))
        context["object"] = my_trip
        context["trip_field_list"] = utils.get_trip_field_list()
        context["trip_subcategories"] = models.TripSubcategory.objects.all()
        base_qs = models.Trip.objects.filter(~Q(id=my_trip.id)).filter(fiscal_year=my_trip.fiscal_year)
        context["same_day_trips"] = base_qs.filter(Q(start_date=my_trip.start_date) | Q(end_date=my_trip.end_date))
        context["same_location_trips"] = base_qs.filter(
            id__in=[trip.id for trip in base_qs if trip.location and my_trip.location and
                    compare_strings(trip.location, my_trip.location) < 3]
        )
        similar_fr_name_trips = [trip.id for trip in base_qs if
                                 trip.nom and compare_strings(trip.nom, trip.name) < 15] if my_trip.nom else []
        similar_en_name_trips = [trip.id for trip in base_qs if compare_strings(trip.name, my_trip.name) < 15]
        my_list = list()
        my_list.extend(similar_en_name_trips)
        my_list.extend(similar_fr_name_trips)
        context["same_name_trips"] = base_qs.filter(
            id__in=set(my_list)
        )
        return context

    def form_valid(self, form):
        my_trip = models.Trip.objects.get(pk=self.kwargs.get("pk"))
        my_trip.status = 41
        my_trip.verified_by = self.request.user
        my_trip.save()

        # DJF - there is potentially a problem here with the logic
        if self.get_query_string() == "":  # means they are coming from the trip detail page
            return HttpResponseRedirect(reverse("travel:trip_detail", args=[my_trip.id]))
        else:
            return HttpResponseRedirect(reverse("travel:trip_list") + self.get_query_string())


class TripSelectFormView(TravelAdminRequiredMixin, CommonFormView):
    template_name = 'travel/form.html'
    form_class = forms.TripSelectForm
    h1 = gettext_lazy("Please select a trip to re-assign:")
    h3 = gettext_lazy("(You will have a chance to review this action before it is carried out.)")
    submit_text = gettext_lazy("Proceed")

    def test_func(self):
        my_object = models.Trip.objects.get(pk=self.kwargs.get("pk"))
        # this only user who should be able to modify an adm level trip is the travel_adm_admin
        if my_object.is_adm_approval_required:
            return utils.in_adm_admin_group(self.request.user)
        return utils.is_admin(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("accounts:denied_access", kwargs={
                "message": _("Sorry, only ADMO administrators can verify trips that require ADM approval.")}))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        trip_a = self.kwargs.get("pk")
        trip_b = form.cleaned_data["trip"]
        return HttpResponseRedirect(reverse("travel:trip_reassign_confirm", kwargs={"trip_a": trip_a, "trip_b": trip_b, }))


class TripReassignConfirmView(TravelAdminRequiredMixin, CommonPopoutFormView):
    template_name = 'travel/trip_reassign_form.html'
    form_class = forms.forms.Form
    width = 1500
    height = 1500
    h1 = gettext_lazy("Please confirm the following:")
    submit_text = gettext_lazy("Confirm")
    field_list = [
        "name",
        "nome",
        'location',
        'lead',
        'start_date',
        'end_date',
        'meeting_url',
        'is_adm_approval_required',
        'status',
        'traveller_list|{}'.format("travellers"),
        'requests|{}'.format("linked trip requests"),
    ]

    def test_func(self):
        my_trip = models.Trip.objects.get(pk=self.kwargs.get("trip_a"))
        if my_trip.is_adm_approval_required:
            return utils.in_adm_admin_group(self.request.user)
        else:
            return utils.is_admin(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("accounts:denied_access", kwargs={
                "message": _("Sorry, only ADMO administrators can verify trips that require ADM approval.")}))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip_a = models.Trip.objects.get(pk=self.kwargs.get("trip_a"))
        trip_b = models.Trip.objects.get(pk=self.kwargs.get("trip_b"))

        context["trip_a"] = trip_a
        context["trip_b"] = trip_b
        context["trip_list"] = [trip_a, trip_b]

        # start out optimistic
        duplicate_ppl = list()
        # we have to sift through each tr that will be transferred to the new trip and ensure that there is no overlap with the new travellers
        traveller_users_from_trip_a = User.objects.filter(travellers__request__trip=trip_b).distinct()
        traveller_users_from_trip_b = User.objects.filter(travellers__request__trip=trip_a).distinct()

        for user in traveller_users_from_trip_a:
            if user in traveller_users_from_trip_b:
                duplicate_ppl.append(user)

        context["duplicate_ppl"] = duplicate_ppl
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            trip_a = models.Trip.objects.get(pk=self.kwargs.get("trip_a"))
            trip_b = models.Trip.objects.get(pk=self.kwargs.get("trip_b"))

            for tr in trip_a.requests.all():
                tr.trip = trip_b
                tr.save()
            messages.success(request,
                             _("All trips from {trip_a} have been reassigned to {trip_b}. You may now delete this trip.").format(trip_a=trip_a, trip_b=trip_b))
            return HttpResponseRedirect(reverse("travel:trip_verify", args=[trip_a.id]))


class TripCancelUpdateView(TravelAdminRequiredMixin, CommonUpdateView):
    # TODO: check permissions
    # TODO: cancel related trip requests and email clients
    # TODO: email travellers the change in their statuses

    model = models.Trip
    form_class = forms.TripAdminNotesForm
    template_name = 'travel/form.html'
    submit_text = _("Cancel the trip")
    h1 = _("Do you wish to undo your cancellation request for the following trip?")
    h2 = "<span class='red-font'>" + \
         _("Cancelling this trip will result in all linked requests to be 'cancelled'. "
           "The list of associated trip requests can be viewed below in the trip detail.") + \
         "</span><br><br>" + \
         "<span class='red-font blink-me'>" + \
         _("This action cannot be undone.") + \
         "</span>"
    active_page_name_crumb = _("Cancel Trip")

    # home_url_name = "travel:index"
    def test_func(self):
        my_object = self.get_object()
        # this only user who should be able to modify an adm level trip is the travel_adm_admin
        if my_object.is_adm_approval_required:
            return utils.in_adm_admin_group(self.request.user)
        return utils.is_admin(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip"] = self.get_object()
        return context

    def form_valid(self, form):
        my_trip = form.save()
        can_cancel = (my_trip.is_adm_approval_required and in_adm_admin_group(self.request.user)) or \
                     (not my_trip.is_adm_approval_required and in_travel_admin_group(self.request.user))

        # if user is allowed to cancel this request, proceed to do so.
        if can_cancel:
            # cancel any outstanding reviews:
            # but only those with the following statuses: PENDING = 1; QUEUED = 20;
            trip_reviewer_statuses_of_interest = [24, 25, ]
            for r in my_trip.reviewers.filter(status__in=trip_reviewer_statuses_of_interest):
                r.status = 44
                r.save()

            #  CANCEL THE TRIP
            my_trip.status = 43
            my_trip.save()

            # cycle through every trip request associated with this trip and cancel it
            # denied = 10; cancelled = 22; draft = 8;
            tr_statuses_to_skip = [10, 22, 8]
            for tr in my_trip.requests.filter(~Q(status__in=tr_statuses_to_skip)):
                # set status to cancelled = 22
                tr.status = 22
                # update the admin notes
                if tr.admin_notes:
                    tr.admin_notes = f'{my_trip.admin_notes}\n\n{tr.admin_notes}'
                else:
                    tr.admin_notes = f'{my_trip.admin_notes}'
                tr.save()

                # cancel any outstanding reviews:
                # but only those with the following statuses: PENDING = 1; QUEUED = 20;
                tr_reviewer_statuses_of_interest = [1, 20, ]
                for r in tr.reviewers.filter(status__in=tr_reviewer_statuses_of_interest):
                    r.status = 5
                    r.save()

                # send an email to the trip_request owner, if the user has an email address.
                if tr.created_by:
                    email = emails.StatusUpdateEmail(self.request, tr)
                    email.send()

            return HttpResponseRedirect(reverse("travel:trip_detail", kwargs=self.kwargs))
        else:
            return HttpResponseForbidden()


# Trip REVIEWER #
####################

class TripReviewerListView(TravelAccessRequiredMixin, CommonTemplateView):
    model = models.Reviewer
    template_name = 'travel/trip_reviewer_list.html'
    home_url_name = "travel:index"
    h1 = " "
    active_page_name_crumb = gettext_lazy("Trip reviews")

    def get_queryset(self):
        return utils.get_related_trip_reviewers(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TripReviewerUpdateView(AdminOrApproverRequiredMixin, CommonUpdateView):
    model = models.TripReviewer
    form_class = forms.TripReviewerApprovalForm
    template_name = 'travel/trip_reviewer_update.html'
    home_url_name = "travel:index"

    def get_h1(self):
        return _("Do you wish to approve the following trip?")

    def get_parent_crumb(self):
        return {"title": _("Trips Awaiting Review"), "url": reverse("travel:trip_reviewer_list") + self.get_query_string()}

    def test_func(self):
        my_trip = self.get_object().trip
        my_user = self.request.user
        if is_trip_approver(my_user, my_trip):
            return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip"] = self.get_object().trip
        return context

    def form_valid(self, form):
        my_reviewer = form.save()
        stay_on_page = form.cleaned_data.get("stay_on_page")
        reset = form.cleaned_data.get("reset")

        if not stay_on_page:
            if reset:
                utils.reset_trip_review_process(my_reviewer.trip)
            else:
                # if it was approved, then we change the reviewer status to 'approved'
                my_reviewer.status = 26
                my_reviewer.status_date = timezone.now()
                my_reviewer.save()

                # if this was the ADM and the trip has been approved, we need to approve all travellers who are have status 14 ("Pending ADM Approval")
                if my_reviewer.role == 5 and my_reviewer.status == 26 and utils.is_adm(self.request.user):
                    qs = models.Reviewer.objects.filter(request__trip=my_reviewer.trip, request__status=14, role=5)
                    for r in qs:
                        r.user = self.request.user
                        r.comments = "approved / approuvé"
                        r.status = 2
                        r.status_date = timezone.now()
                        r.save()
                        utils.approval_seeker(r.request, False, self.request)

            # update any statuses if necessary
            utils.trip_approval_seeker(my_reviewer.trip, self.request)
            return HttpResponseRedirect(reverse("travel:trip_reviewer_list"))

        else:
            my_kwargs = {"pk": my_reviewer.id}
            return HttpResponseRedirect(reverse("travel:trip_reviewer_update", kwargs=my_kwargs) + "#id_comments")


# REPORTS #
###########

class ReportFormView(TravelAdminRequiredMixin, CommonFormView):
    template_name = 'travel/reports.html'
    form_class = forms.ReportSearchForm
    h1 = gettext_lazy("Reports")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_initial(self):
        return {
            "fiscal_year": fiscal_year(sap_style=True),
        }

    def form_valid(self, form):
        report = int(form.cleaned_data["report"])
        fy = nz(form.cleaned_data["fiscal_year"], "None")
        region = nz(form.cleaned_data["region"], "None")
        trip = nz(form.cleaned_data["trip"], "None")
        user = nz(form.cleaned_data["user"], "None")
        from_date = nz(form.cleaned_data["from_date"], "None")
        to_date = nz(form.cleaned_data["to_date"], "None")
        adm = nz(form.cleaned_data["adm"], "None")

        if report == 1:
            return HttpResponseRedirect(reverse("travel:export_cfts_list") +
                                        f'?fy={fy};region={region};trip={trip};user={user};from_date={from_date};to_date={to_date};')
        elif report == 2:
            return HttpResponseRedirect(reverse("travel:export_trip_list") +
                                        f'?fy={fy};region={region};adm={adm};from_date={from_date};to_date={to_date};')
        else:
            messages.error(self.request, "Report is not available. Please select another report.")
            return HttpResponseRedirect(reverse("travel:reports"))


@login_required(login_url='/accounts/login/')
@user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def export_cfts_list(request):
    fy = request.GET.get("year")
    region = request.GET.get("region")
    trip = request.GET.get("trip")
    user = request.GET.get("user")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    file_url = reports.generate_cfts_spreadsheet(fiscal_year=fy, region=region, trip=trip, user=user, from_date=from_date, to_date=to_date)
    export_file_name = f'CFTS export {timezone.now().strftime("%Y-%m-%d")}.xlsx'

    if settings.AZURE_STORAGE_ACCOUNT_NAME:
        return HttpResponseRedirect(reverse("travel:get_file", args=[file_url.replace("/", "||")]) + f'?blob_name=true;export_file_name={export_file_name}')

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = f'inline; filename="{export_file_name}"'
            return response
    raise Http404


@login_required(login_url='/accounts/login/')
@user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def export_trip_list(request):
    fy = request.GET.get("year")
    region = request.GET.get("region")
    adm = request.GET.get("adm")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    site_url = my_envr(request)["SITE_FULL_URL"]
    file_url = reports.generate_trip_list(fiscal_year=fy, region=region, adm=adm, from_date=from_date, to_date=to_date, site_url=site_url)
    export_file_name = f'CTMS trip list {timezone.now().strftime("%Y-%m-%d")}.xlsx'

    if settings.AZURE_STORAGE_ACCOUNT_NAME:
        return HttpResponseRedirect(reverse("travel:get_file", args=[file_url.replace("/", "||")]) + f'?blob_name=true;export_file_name={export_file_name}')

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = f'inline; filename="{export_file_name}"'
            return response
    raise Http404


@login_required(login_url='/accounts/login/')
@user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def export_upcoming_trips(request):
    site_url = my_envr(request)["SITE_FULL_URL"]
    file_url = reports.generate_upcoming_trip_list(site_url)
    export_file_name = '{} {}.xlsx'.format(_("upcoming trips"), timezone.now().strftime("%Y-%m-%d"))

    if settings.AZURE_STORAGE_ACCOUNT_NAME:
        return HttpResponseRedirect(reverse("travel:get_file", args=[file_url.replace("/", "||")]) + f'?blob_name=true;export_file_name={export_file_name}')

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = f'inline; filename="{export_file_name}"'
            return response
    raise Http404


@login_required(login_url='/accounts/login/')
@user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def export_request_cfts(request, trip=None, trip_request=None):
    file_url = reports.generate_cfts_spreadsheet(trip_request=trip_request, trip=trip)
    export_file_name = f'CFTS export {timezone.now().strftime("%Y-%m-%d")}.xlsx'

    if settings.AZURE_STORAGE_ACCOUNT_NAME:
        return HttpResponseRedirect(reverse("travel:get_file", args=[file_url.replace("/", "||")]) + f'?blob_name=true;export_file_name={export_file_name}')

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename="CFTS export {}.xlsx"'.format(
                timezone.now().strftime("%Y-%m-%d"))
            return response
    raise Http404


class TravelPlanPDF(TravelAccessRequiredMixin, PDFTemplateView):
    def get_template_names(self):
        my_object = models.TripRequest.objects.get(id=self.kwargs['pk'])
        if my_object.travellers.count() > 1:
            template_name = "travel/traf/group.html"
        else:
            template_name = "travel/traf/single.html"
        return template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_object = models.TripRequest.objects.get(id=self.kwargs['pk'])
        context["parent"] = my_object
        context["SITE_FULL_URL"] = my_envr(self.request)["SITE_FULL_URL"]
        context["trip_category_list"] = models.TripCategory.objects.all()
        cost_categories = models.CostCategory.objects.all()
        my_dict = dict()
        my_dict["totals"] = dict()
        my_dict["totals"]["total"] = 0
        for obj in my_object.travellers.all():
            my_dict[obj] = dict()
            for cat in cost_categories:
                if not my_dict["totals"].get(cat):
                    my_dict["totals"][cat] = 0
                cat_amount = obj.costs.filter(cost__cost_category=cat).values("amount_cad").order_by("amount_cad").aggregate(
                    dsum=Sum("amount_cad"))['dsum']
                my_dict[obj][cat] = cat_amount
                my_dict["totals"][cat] += nz(cat_amount, 0)
                my_dict["totals"]["total"] += nz(cat_amount, 0)

        context['my_dict'] = my_dict
        return context


# SETTINGS #
############


class HelpTextHardDeleteView(TravelADMAdminRequiredMixin, CommonHardDeleteView):
    model = models.HelpText
    success_url = reverse_lazy("travel:manage_help_text")


class HelpTextFormsetView(TravelADMAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage HelpText"
    queryset = models.HelpText.objects.all()
    formset_class = forms.HelpTextFormset
    success_url = reverse_lazy("travel:manage_help_text")
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_help_text"


class CostCategoryHardDeleteView(TravelADMAdminRequiredMixin, CommonHardDeleteView):
    model = models.CostCategory
    success_url = reverse_lazy("travel:manage_cost_categories")


class CostCategoryFormsetView(TravelADMAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Cost Category"
    queryset = models.CostCategory.objects.all()
    formset_class = forms.CostCategoryFormset
    success_url = reverse_lazy("travel:manage_cost_categories")
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_cost_category"


class CostHardDeleteView(TravelADMAdminRequiredMixin, CommonHardDeleteView):
    model = models.Cost
    success_url = reverse_lazy("travel:manage_costs")


class CostFormsetView(TravelADMAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Cost"
    queryset = models.Cost.objects.all()
    formset_class = forms.CostFormset
    success_url = reverse_lazy("travel:manage_costs")
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_cost"


class NJCRatesFormsetView(TravelADMAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage NJCRates"
    queryset = models.NJCRates.objects.all()
    formset_class = forms.NJCRatesFormset
    success_url = reverse_lazy("travel:manage_njc_rates")
    home_url_name = "travel:index"


class TripCategoryFormsetView(TravelADMAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Trip Categories"
    queryset = models.TripCategory.objects.all()
    formset_class = forms.TripCategoryFormset
    success_url = reverse_lazy("travel:manage_trip_categories")
    home_url_name = "travel:index"


class TripSubcategoryFormsetView(TravelADMAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Trip Subcategories"
    queryset = models.TripSubcategory.objects.all()
    formset_class = forms.TripSubcategoryFormset
    success_url = reverse_lazy("travel:manage_trip_subcategories")
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_trip_subcategory"


class TripSubcategoryHardDeleteView(TravelADMAdminRequiredMixin, CommonHardDeleteView):
    model = models.TripSubcategory
    success_url = reverse_lazy("travel:manage_trip_subcategories")


class ProcessStepFormsetView(TravelADMAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Process Steps"
    queryset = models.ProcessStep.objects.all()
    formset_class = forms.ProcessStepFormset
    success_url = reverse_lazy("travel:manage_process_steps")
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_process_step"
    container_class = "container-fluid"


class ProcessStepHardDeleteView(TravelADMAdminRequiredMixin, CommonHardDeleteView):
    model = models.ProcessStep
    success_url = reverse_lazy("travel:manage_process_steps")


class FAQFormsetView(TravelADMAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage FAQs"
    queryset = models.FAQ.objects.all()
    formset_class = forms.FAQFormset
    success_url_name = "travel:manage_faqs"
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_faq"
    container_class = "container-fluid"


class FAQHardDeleteView(TravelADMAdminRequiredMixin, CommonHardDeleteView):
    model = models.FAQ
    success_url = reverse_lazy("travel:manage_faqs")


class OrganizationFormsetView(TravelADMAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Organizations"
    queryset = shared_models.Organization.objects.filter(is_dfo=True)
    formset_class = forms.OrganizationFormset
    success_url_name = "travel:manage_organizations"
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_organization"
    container_class = "container-fluid"


class OrganizationHardDeleteView(TravelADMAdminRequiredMixin, CommonHardDeleteView):
    model = shared_models.Organization
    success_url = reverse_lazy("travel:manage_organizations")


class RoleFormsetView(TravelADMAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Roles"
    queryset = models.Role.objects.all()
    formset_class = forms.RoleFormset
    success_url_name = "travel:manage_roles"
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_role"


class RoleHardDeleteView(TravelADMAdminRequiredMixin, CommonHardDeleteView):
    model = models.Role
    success_url = reverse_lazy("travel:manage_roles")


# Reference Materials
class ReferenceMaterialListView(TravelADMAdminRequiredMixin, CommonListView):
    template_name = "travel/list.html"
    model = models.ReferenceMaterial
    field_list = [
        {"name": "tname|{}".format(gettext_lazy("name")), "class": "", "width": ""},
        {"name": "turl|{}".format(gettext_lazy("URL")), "class": "", "width": ""},
        {"name": "tfile|{}".format(gettext_lazy("File")), "class": "", "width": ""},
        {"name": "created_at", "class": "", "width": ""},
        {"name": "updated_at", "class": "", "width": ""},
    ]
    new_object_url_name = "travel:ref_mat_new"
    row_object_url_name = "travel:ref_mat_edit"
    home_url_name = "travel:index"
    h1 = gettext_lazy("Reference Materials")
    container_class = "container bg-light curvy"


class ReferenceMaterialUpdateView(TravelADMAdminRequiredMixin, CommonUpdateView):
    model = models.ReferenceMaterial
    form_class = forms.ReferenceMaterialForm
    home_url_name = "travel:index"
    parent_crumb = {"title": _("Reference Materials"), "url": reverse_lazy("travel:ref_mat_list")}
    template_name = "travel/form.html"
    is_multipart_form_data = True
    container_class = "container bg-light curvy"

    def get_delete_url(self):
        return reverse("travel:ref_mat_delete", args=[self.get_object().id])


class ReferenceMaterialCreateView(TravelADMAdminRequiredMixin, CommonCreateView):
    model = models.ReferenceMaterial
    form_class = forms.ReferenceMaterialForm
    home_url_name = "travel:index"
    parent_crumb = {"title": _("Reference Materials"), "url": reverse_lazy("travel:ref_mat_list")}
    template_name = "travel/form.html"
    is_multipart_form_data = True
    container_class = "container bg-light curvy"


class ReferenceMaterialDeleteView(TravelADMAdminRequiredMixin, CommonDeleteView):
    model = models.ReferenceMaterial
    success_url = reverse_lazy('travel:ref_mat_list')
    home_url_name = "travel:index"
    parent_crumb = {"title": _("Reference Materials"), "url": reverse_lazy("travel:ref_mat_list")}
    template_name = "travel/confirm_delete.html"
    delete_protection = False
    container_class = "container bg-light curvy"


# Default Reviewer Settings

class DefaultReviewerListView(TravelADMAdminRequiredMixin, CommonListView):
    model = models.DefaultReviewer
    template_name = 'travel/default_reviewer/default_reviewer_list.html'
    h1 = gettext_lazy("Optional / Special Reviewers")
    h3 = gettext_lazy("Use this module to set the default reviewers that get added to a trip request.")
    new_object_url_name = "travel:default_reviewer_new"
    home_url_name = "travel:index"
    container_class = "container-fluid"
    field_list = [
        {"name": 'user', "class": "", "width": ""},
        {"name": 'sections', "class": "", "width": ""},
        {"name": 'divisions', "class": "", "width": ""},
        {"name": 'branches', "class": "", "width": ""},
        {"name": 'expenditure_initiation_region', "class": "", "width": ""},
        {"name": 'special_role', "class": "", "width": ""},
    ]


class DefaultReviewerUpdateView(TravelADMAdminRequiredMixin, CommonUpdateView):
    model = models.DefaultReviewer
    form_class = forms.DefaultReviewerForm
    success_url = reverse_lazy('travel:default_reviewer_list')
    template_name = 'travel/default_reviewer/default_reviewer_form.html'

    def form_valid(self, form):
        obj = form.save()
        if not obj.special_role and \
                not obj.sections.exists() and \
                not obj.divisions.exists() and \
                not obj.branches.exists() and \
                not obj.expenditure_initiation_region:
            obj.delete()
        return HttpResponseRedirect(self.get_success_url())


class DefaultReviewerCreateView(TravelADMAdminRequiredMixin, CommonCreateView):
    model = models.DefaultReviewer
    form_class = forms.DefaultReviewerForm
    success_url = reverse_lazy('travel:default_reviewer_list')
    template_name = 'travel/default_reviewer/default_reviewer_form.html'


class DefaultReviewerDeleteView(TravelADMAdminRequiredMixin, CommonDeleteView):
    model = models.DefaultReviewer
    success_url = reverse_lazy('travel:default_reviewer_list')
    success_message = 'The default reviewer was successfully deleted!'
    template_name = 'travel/default_reviewer/default_reviewer_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class UserListView(TravelADMAdminRequiredMixin, CommonFilterView):
    template_name = "travel/user_list.html"
    filterset_class = filters.UserFilter
    home_url_name = "travel:index"
    paginate_by = 25
    h1 = "Travel App User List"
    field_list = [
        {"name": 'first_name', "class": "", "width": ""},
        {"name": 'last_name', "class": "", "width": ""},
        {"name": 'email', "class": "", "width": ""},
        {"name": 'last_login|{}'.format(gettext_lazy("Last login to DM Apps")), "class": "", "width": ""},
    ]
    new_object_url = reverse_lazy("shared_models:user_new")

    def get_queryset(self):
        queryset = User.objects.order_by("first_name", "last_name").annotate(
            search_term=Concat('first_name', Value(""), 'last_name', Value(""), 'email', output_field=TextField())
        )
        if self.request.GET.get("travel_only"):
            queryset = queryset.filter(groups__in=[33, 36]).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["admin_group"] = Group.objects.get(name="travel_admin")
        context["adm_admin_group"] = Group.objects.get(name="travel_adm_admin")
        return context


@login_required(login_url='/accounts/login/')
@user_passes_test(in_adm_admin_group, login_url='/accounts/denied/')
def toggle_user(request, pk, type):
    my_user = get_object_or_404(User, pk=pk)
    admin_group = get_object_or_404(Group, name="travel_admin")
    adm_admin_group = get_object_or_404(Group, name="travel_adm_admin")
    if type == "admin":
        # if the user is in the admin group, remove them
        if admin_group in my_user.groups.all():
            my_user.groups.remove(admin_group)
        # otherwise add them
        else:
            my_user.groups.add(admin_group)
    elif type == "adm_admin":
        # if the user is in the edit group, remove them
        if adm_admin_group in my_user.groups.all():
            my_user.groups.remove(adm_admin_group)
        # otherwise add them
        else:
            my_user.groups.add(adm_admin_group)

    return HttpResponseRedirect("{}#user_{}".format(request.META.get('HTTP_REFERER'), my_user.id))
