import datetime
import json
import os
from copy import deepcopy

from azure.storage.blob import BlockBlobService
from decouple import config
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models.functions import Concat
from django.template.defaultfilters import pluralize
from django.utils.safestring import mark_safe
from msrestazure.azure_active_directory import MSIAuthentication

from dm_apps.utils import custom_send_mail
from django.db.models import Sum, Q, Value, TextField
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_lazy
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse, HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView, ListView, TemplateView, FormView
###
from django_filters.views import FilterView
from easy_pdf.views import PDFTemplateView
from lib.functions.custom_functions import fiscal_year
from lib.templatetags.custom_filters import nz
from shared_models.views import CommonFormsetView, CommonHardDeleteView, CommonUpdateView, CommonFilterView, CommonFormView, \
    CommonPopoutFormView, CommonPopoutUpdateView, CommonListView, CommonDetailView, CommonTemplateView, CommonCreateView, CommonDeleteView
from . import models
from . import forms
from . import reports
from . import emails
from . import filters
from . import utils

from shared_models import models as shared_models


def get_file(request, file):
    IN_PIPELINE = config("IN_PIPELINE", cast=bool, default=False)

    my_file = models.File.objects.get(pk=file)
    blob_name = my_file.file

    if settings.AZURE_STORAGE_ACCOUNT_NAME:
        AZURE_STORAGE_ACCOUNT_NAME = settings.AZURE_STORAGE_ACCOUNT_NAME
        # account_key = config("AZURE_STORAGE_SECRET_KEY", cast=str, default="")
        # blobService = BlockBlobService(account_name=AZURE_STORAGE_ACCOUNT_NAME, account_key=account_key)
        token_credential = MSIAuthentication(resource=f'https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net')
        blobService = BlockBlobService(account_name=AZURE_STORAGE_ACCOUNT_NAME, token_credential=token_credential)
        blob_file = blobService.get_blob_to_bytes("media", blob_name)
        response = HttpResponse(blob_file.content, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{blob_name}"'
    else:
        response = HttpResponse(my_file.file.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{blob_name}"'

    return response


def get_conf_details(request):
    conf_dict = {}
    for conf in models.Conference.objects.all():
        conf_dict[conf.id] = {}
        conf_dict[conf.id]['location'] = conf.location
        conf_dict[conf.id]['start_date'] = conf.start_date.strftime("%Y-%m-%d")
        conf_dict[conf.id]['end_date'] = conf.end_date.strftime("%Y-%m-%d")

    return JsonResponse(conf_dict)


def in_travel_admin_group(user):
    if user.id:
        return user.groups.filter(name='travel_admin').count() != 0


def in_adm_admin_group(user):
    if user.id:
        return user.groups.filter(name='travel_adm_admin').count() != 0


def is_approver(user, trip_request):
    if trip_request.current_reviewer and user == trip_request.current_reviewer.user:
        return True


def is_trip_approver(user, trip):
    if trip.current_reviewer and user == trip.current_reviewer.user:
        return True


def can_modify_request(user, trip_request_id, trip_request_unsubmit=False):
    """
    returns True if user has permissions to delete or modify a request

    The answer of this question will depend on whether the trip is submitted.
    owners cannot edit a submitted trip

    :param user:
    :param trip_request_id:
    :param trip_request_submit: If true, it means this function is being used to answer the question about whether a user can unsubmit a trip
    :return:
    """
    if user.id:
        my_trip_request = models.TripRequest.objects.get(pk=trip_request_id)

        # check to see if a travel_admin
        if in_travel_admin_group(user):
            return True

        # check to see if they are the active reviewer
        # determine if this is a child trip or not.
        if not my_trip_request.parent_request:
            if my_trip_request.current_reviewer and my_trip_request.current_reviewer.user == user:
                return True
        # This is a child trip request
        else:
            if my_trip_request.parent_request.current_reviewer and my_trip_request.parent_request.current_reviewer.user == user:
                return True
        # if the project is unsubmitted, the project lead is also able to edit the project... obviously
        # check to see if they are either the owner OR a traveller
        # SPECIAL CASE: sometimes we complete requests on behalf of somebody else.
        if not my_trip_request.submitted and \
                (not my_trip_request.user or  # anybody can edit
                 my_trip_request.user == user or  # the user is the traveller and / or requester
                 user in my_trip_request.travellers or  # the user is a traveller on the trip
                 (my_trip_request.parent_request and my_trip_request.parent_request.user == user)):  # the user is the requester
            return True

        if trip_request_unsubmit and user == my_trip_request.user:
            return True


class TravelAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return in_travel_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class TravelADMAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return in_adm_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class CanModifyMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return can_modify_request(self.request.user, self.kwargs.get("pk"))

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class AdminOrApproverRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        my_trip_request = models.TripRequest.objects.get(pk=self.kwargs.get("pk"))
        my_user = self.request.user
        if in_travel_admin_group(my_user) or is_approver(my_user, my_trip_request):
            return True

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


# This allows any logged in user to access the view
class TravelAccessRequiredMixin(LoginRequiredMixin):
    login_url = '/accounts/login/'


class IndexTemplateView(TravelAccessRequiredMixin, CommonTemplateView):
    template_name = 'travel/index.html'
    active_page_name_crumb = gettext_lazy("Home")
    h1 = " "

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["requests_awaiting_changes"] = utils.get_related_trips(self.request.user).filter(status_id=16).count()
        context["user_trip_requests"] = utils.get_related_trips(self.request.user).count()
        # show the number of reviews awaiting for the logged in user
        tr_reviews_waiting = self.request.user.reviewers.filter(status_id=1).filter(
            ~Q(trip_request__status_id__in=[16, 14,
                                            8])).count()  # number of requests where review is pending (excluding those that are drafts (from children), changes_requested and pending ADM approval)
        trip_reviews_waiting = self.request.user.trip_reviewers.filter(status_id=25).count()  # number of trips where review is pending
        context["tr_reviews_waiting"] = tr_reviews_waiting
        context["trip_reviews_waiting"] = trip_reviews_waiting
        context["reviews_waiting"] = trip_reviews_waiting + tr_reviews_waiting
        # this will be the dict to populate the tabs on the index page
        tab_dict = dict()
        for region in shared_models.Region.objects.all():
            tab_dict[region] = dict()
            # this will be the counter for any of the things that need dealing with

            # RDG
            rdg_number_waiting = models.Reviewer.objects.filter(
                status_id=1,
                role_id=6,
                trip_request__section__division__branch__region=region,
            ).filter(~Q(trip_request__status_id=16)).count()  # number of requests where admin review is pending
            rdg_approval_list_url = reverse('travel:admin_approval_list', kwargs={"type": 'rdg', "region": region.id})

            # ADM
            # adm_number_waiting = models.Reviewer.objects.filter(
            #     status_id=1,
            #     role_id=5,
            #     trip_request__section__division__branch__region=region,
            # ).filter(~Q(trip_request__status_id=16)).count()  # number of requests where admin review is pending
            # adm_approval_list_url = reverse('travel:admin_approval_list', kwargs={"type": 'adm', "region": region.id})

            # unverified trips
            unverified_trips = models.Conference.objects.filter(status_id=30, is_adm_approval_required=False, lead=region).count()
            trip_verification_list_url = reverse('travel:admin_trip_verification_list', kwargs={"adm": 0, "region": region.id})

            if unverified_trips > 0 and in_travel_admin_group(self.request.user):
                messages.error(self.request, mark_safe(
                    f"<b>ADMIN WARNING:</b> {region} Region has {unverified_trips} unverified trip{pluralize(unverified_trips)} requiring attention!!"))

            tab_dict[region]["rdg_number_waiting"] = rdg_number_waiting
            tab_dict[region]["rdg_approval_list_url"] = rdg_approval_list_url
            # tab_dict[region]["adm_number_waiting"] = adm_number_waiting
            # tab_dict[region]["adm_approval_list_url"] = adm_approval_list_url
            tab_dict[region]["unverified_trips"] = unverified_trips
            tab_dict[region]["trip_verification_list_url"] = trip_verification_list_url
            # tab_dict[region]["things_to_deal_with"] = rdg_number_waiting + adm_number_waiting + unverified_trips
            tab_dict[region]["things_to_deal_with"] = rdg_number_waiting + unverified_trips

        # Now for NCR
        admo_name = "ADM Office"
        tab_dict[admo_name] = dict()

        # unverified trips
        unverified_trips = models.Conference.objects.filter(status_id=30, is_adm_approval_required=True).count()
        trip_verification_list_url = reverse('travel:admin_trip_verification_list', kwargs={"adm": 1, "region": 0})

        if unverified_trips > 0 and in_adm_admin_group(self.request.user):
            messages.error(self.request, mark_safe(
                f"<b>ADMIN WARNING:</b> ADM Office has {unverified_trips} unverified trip{pluralize(unverified_trips)} requiring attention!!"))

        adm_ready_trips = utils.get_adm_eligible_trips().count()

        tab_dict[admo_name]["unverified_trips"] = unverified_trips
        tab_dict[admo_name]["trip_verification_list_url"] = trip_verification_list_url
        tab_dict[admo_name]["adm_trips_ready"] = adm_ready_trips
        tab_dict[admo_name]["things_to_deal_with"] = unverified_trips + adm_ready_trips  # placeholder :)

        number_of_reviews = self.request.user.reviewers.all().count() + self.request.user.trip_reviewers.all().count()
        context["is_reviewer"] = True if number_of_reviews > 0 else False
        context["is_tr_reviewer"] = True if self.request.user.reviewers.all().count() > 0 else False
        context["is_trip_reviewer"] = True if self.request.user.trip_reviewers.all().count() > 0 else False
        context["is_admin"] = in_travel_admin_group(self.request.user)
        context["is_adm_admin"] = in_adm_admin_group(self.request.user)
        context["tab_dict"] = tab_dict
        context["processes"] = [
            models.ProcessStep.objects.filter(stage=1),
            models.ProcessStep.objects.filter(stage=2)
        ]
        return context


request_field_list = [
    'fiscal_year',
    'trip',
    'requester_name|{}'.format(_("Traveller name")),
    'requester_info|{}'.format(_("Traveller information")),
    'is_public_servant',
    'status_string|{}'.format(_("Request status")),
    'section',
    'region',
    'to_from|{}'.format(_("Departure location / Destination")),
    'dates|{}'.format(_("Travel dates")),
    'objective_of_event',
    'benefit_to_dfo',
    # 'reason',
    'long_role|{}'.format(_("Role of participant")),
    'multiple_conferences_rationale',
    'late_justification',
    'bta_attendees',
    'total_dfo_funding|{}'.format(_("Total amount of DFO funding")),
    'funding_source',
    'total_non_dfo_funding|{}'.format(_("Total amount of non-DFO funding")),
    'total_non_dfo_funding_sources|{}'.format(_("Non-DFO funding sources")),
    'total_request_cost|{}'.format(_("Total costs")),
    'original_submission_date',
    'processing_time|{}'.format(_("Processing time")),
    'created_by',
    'notes',
]

traveller_field_list = [
    'requester_info|{}'.format(_("Traveller information")),
    'is_public_servant',
    'region',
    'is_research_scientist|{}'.format(_("RES?")),
    'objective_of_event',
    'benefit_to_dfo',
    'start_date',
    'end_date',
    'departure_location',
    # 'reason',
    'long_role|{}'.format("Role of participant"),
    'multiple_conferences_rationale',
    'funding_source',
    'total_dfo_funding|{}'.format(_("Total amount of DFO funding")),
    'total_non_dfo_funding|{}'.format(_("Total amount of non-DFO funding")),
    'total_non_dfo_funding_sources|{}'.format(_("Non-DFO funding sources")),
    'total_request_cost|{}'.format(_("Total costs")),
]

request_group_field_list = [
    'fiscal_year',
    'trip',
    'requester_name|{}'.format(_("Organizer name")),
    'status_string|{}'.format(_("Request status")),
    'section',
    'destination',

    'objective_of_event',
    'benefit_to_dfo',
    'bta_attendees',
    'late_justification',
    'funding_source',
    'total_dfo_funding|{}'.format(_("Total amount of DFO funding")),
    'total_non_dfo_funding_sources|{}'.format(_("Non-DFO funding sources")),
    'total_non_dfo_funding|{}'.format(_("Total amount of non-DFO funding")),
    'total_request_cost|{}'.format(_("Total cost")),
    'original_submission_date',
    'processing_time|{}'.format(_("Processing time")),
    'notes',
]

request_child_field_list = [
    'requester_name|{}'.format(_("Name")),
    # 'is_public_servant',
    'is_research_scientist|{}'.format(_("RES?")),
    'dates|{}'.format(_("Travel dates")),
    'departure_location',
    # 'reason',
    'role',
    # 'role_of_participant',
    'total_cost|{}'.format(_("Total cost")),
    'non_dfo_costs|{}'.format(_("non-DFO funding")),
]

reviewer_field_list = [
    'order',
    'user',
    'role',
    'status',
    'status_date',
    'comments_html|Comments',
]

conf_field_list = [
    'tname|{}'.format(_("Name")),
    'location',
    'trip_subcategory',
    'lead',
    'has_event_template',
    'number',
    'start_date',
    'end_date',
    'meeting_url',
    'abstract_deadline',
    'registration_deadline',
    'is_adm_approval_required',
    'notes',
    'status_string|{}'.format("status"),
    'date_eligible_for_adm_review',
    'adm_review_deadline',
    'total_cost|{}'.format("Total DFO cost (excluding BTA)"),
    'non_res_total_cost|{}'.format("Total DFO cost from non-RES travellers (excluding BTA)"),
]

cost_field_list = [
    "cost",
    "rate_cad",
    "number_of_days",
    "amount_cad",
]


def get_help_text_dict():
    my_dict = {}
    for obj in models.HelpText.objects.all():
        my_dict[obj.field_name] = str(obj)

    return my_dict


# TRIP REQUEST #
################
class TripRequestListView(TravelAccessRequiredMixin, CommonFilterView):
    filterset_class = filters.TripRequestFilter
    template_name = 'travel/trip_request_list.html'
    subtitle = gettext_lazy("Trip Requests")
    home_url_name = "travel:index"
    paginate_by = 25
    container_class = "container-fluid"
    row_object_url_name = "travel:request_detail"

    def get_new_object_url(self):
        return reverse("travel:request_new", kwargs=self.kwargs)

    def get_random_object(self):
        return models.TripRequest.objects.first()

    field_list = [
        {"name": 'fiscal_year', "width": "75px"},
        {"name": 'is_group_request|Type', },
        {"name": 'status', "width": "150px"},
        {"name": 'section|{}'.format(gettext_lazy("DFO section")), },
        {"name": 'requester_name|{}'.format(gettext_lazy("Requester name")), },
        {"name": 'trip.tname', "width": "400px"},
        {"name": 'destination|{}'.format(gettext_lazy("Destination")), },
        {"name": 'start_date|{}'.format(gettext_lazy("Departure date")), },
        {"name": 'processing_time|{}'.format(gettext_lazy("Processing time")), },
        {"name": 'created_by', },
    ]

    def get_queryset(self):
        if self.kwargs.get("type") == "all" and in_travel_admin_group(self.request.user):
            queryset = models.TripRequest.objects.filter(parent_request__isnull=True)
        else:
            queryset = utils.get_related_trips(self.request.user)
        return queryset

    def get_h1(self):
        subtitle = self.subtitle
        if self.kwargs.get("type") == "all" and in_travel_admin_group(self.request.user):
            return f"{subtitle}"
        else:
            return f"{subtitle} - {self.request.user}"


class TripRequestDetailView(TravelAccessRequiredMixin, CommonDetailView):
    model = models.TripRequest
    template_name = 'travel/trip_request_detail.html'
    home_url_name = "travel:index"

    def get_parent_crumb(self):
        kwargs = deepcopy(self.kwargs)
        del kwargs["pk"]
        return {"title": _("Trip Requests"), "url": reverse("travel:request_list", kwargs=kwargs)}

    def get_context_data(self, **kwargs):
        my_object = self.get_object()
        context = super().get_context_data(**kwargs)

        context["field_list"] = request_field_list if not my_object.is_group_request else request_group_field_list
        my_request_child_field_list = deepcopy(request_child_field_list)
        context["child_field_list"] = my_request_child_field_list
        context["reviewer_field_list"] = reviewer_field_list
        context["traveller_field_list"] = traveller_field_list

        context["conf_field_list"] = conf_field_list
        context["cost_field_list"] = cost_field_list
        context['help_text_dict'] = get_help_text_dict()
        context["fy"] = fiscal_year()
        context["is_admin"] = "travel_admin" in [group.name for group in self.request.user.groups.all()]
        context["is_owner"] = my_object.user == self.request.user
        context["now"] = timezone.now()
        context["trip"] = my_object.trip
        context["triprequest"] = my_object

        # Admins should be given the same permissions as a current reviewer; the two are synonymous
        if context["is_admin"]:
            is_current_reviewer = True
        else:
            is_current_reviewer = my_object.current_reviewer.user == self.request.user if my_object.current_reviewer else None

        context["is_reviewer"] = self.request.user in [r.user for r in self.get_object().reviewers.all()]
        context["is_current_reviewer"] = is_current_reviewer
        if my_object.submitted and not is_current_reviewer:
            context["report_mode"] = True

        # This might be a better thing to use for button disabling
        context["can_modify"] = can_modify_request(self.request.user, my_object.id)
        return context


class TripRequestUpdateView(CanModifyMixin, CommonUpdateView):
    model = models.TripRequest
    home_url_name = "travel:index"
    h1 = gettext_lazy("Edit Trip Request")

    def get_initial(self):
        return {"reset_reviewers": False}

    def get_template_names(self):
        return 'travel/trip_request_form_popout.html' if self.kwargs.get("type") == "pop" else 'travel/trip_request_form.html'

    def get_form_class(self):
        return forms.ChildTripRequestForm if self.kwargs.get("type") == "pop" else forms.TripRequestForm

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("travel:request_detail", kwargs=self.kwargs)}

    def get_grandparent_crumb(self):
        kwargs = deepcopy(self.kwargs)
        del kwargs["pk"]
        return {"title": _("Trip Requests"), "url": reverse("travel:request_list", kwargs=kwargs)}

    def form_valid(self, form):
        my_object = form.save()

        if my_object.parent_request:
            my_trip = my_object.parent_request.trip
        else:
            my_trip = my_object.trip
        utils.manage_trip_warning(my_trip)

        # decide whether the reviewers should be reset
        if form.cleaned_data.get("reset_reviewers"):
            reset_reviewers(self.request, type=self.kwargs.get("type"), triprequest=my_object.pk)

        if not my_object.parent_request:
            if form.cleaned_data.get("stay_on_page"):
                return HttpResponseRedirect(reverse_lazy("travel:request_edit", kwargs=self.kwargs))
            else:
                return HttpResponseRedirect(reverse_lazy("travel:request_detail", kwargs=self.kwargs))
        else:
            return HttpResponseRedirect(reverse("shared_models:close_me"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cost_field_list"] = cost_field_list

        user_dict = {}
        for user in User.objects.all():
            user_dict[user.id] = {}
            user_dict[user.id]['first_name'] = user.first_name
            user_dict[user.id]['last_name'] = user.last_name
            user_dict[user.id]['email'] = user.email

        user_json = json.dumps(user_dict)
        # send JSON file to template so that it can be used by js script
        context['user_json'] = user_json

        conf_dict = {}
        for conf in models.Conference.objects.all():
            conf_dict[conf.id] = {}
            conf_dict[conf.id]['location'] = conf.location
            conf_dict[conf.id]['start_date'] = conf.start_date.strftime("%Y-%m-%d")
            conf_dict[conf.id]['end_date'] = conf.end_date.strftime("%Y-%m-%d")

        conf_json = json.dumps(conf_dict)
        # send JSON file to template so that it can be used by js script
        context['conf_json'] = conf_json
        context['help_text_dict'] = get_help_text_dict()
        return context


class TripRequestCreateView(TravelAccessRequiredMixin, CommonCreateView):
    model = models.TripRequest
    home_url_name = "travel:index"

    def get_template_names(self):
        if self.kwargs.get("parent_request"):
            return 'travel/trip_request_form_popout.html'
        else:
            return 'travel/trip_request_form.html'

    def get_form_class(self):
        if self.kwargs.get("parent_request"):
            return forms.ChildTripRequestForm
        else:
            return forms.TripRequestForm

    def get_initial(self):
        if self.kwargs.get("parent_request"):
            my_object = models.TripRequest.objects.get(pk=self.kwargs.get("parent_request"))
            my_dict = {
                "parent_request": my_object,
                "stay_on_page": True,
                "start_date": my_object.trip.start_date,
                "end_date": my_object.trip.end_date,
            }
        else:
            # if this is a new parent trip
            my_dict = {"user": self.request.user}
        return my_dict

    def form_valid(self, form):
        my_object = form.save(commit=False)
        my_object.created_by = self.request.user
        my_object.save()

        # if it is a group request, add the main user as a traveller
        if my_object.is_group_request:
            my_child_object = models.TripRequest.objects.create(
                user=self.request.user,
                first_name=self.request.user.first_name,
                last_name=self.request.user.last_name,
                email=self.request.user.email,
                parent_request=my_object,
                start_date=my_object.trip.start_date,
                end_date=my_object.trip.end_date,
            )
            # pre-populate the costs on the 'child' record
            utils.populate_trip_request_costs(self.request, my_child_object)
        else:
            # if the request is not a group request, we pre-populate the costs on the 'parent' record
            utils.populate_trip_request_costs(self.request, my_object)

        # add reviewers
        utils.get_tr_reviewers(my_object)

        # if this is not a child record
        if not my_object.parent_request:
            if form.cleaned_data.get("stay_on_page"):
                return HttpResponseRedirect(
                    reverse_lazy("travel:request_edit", kwargs={"pk": my_object.id, "type": self.kwargs.get("type")}))
            else:
                return HttpResponseRedirect(
                    reverse_lazy("travel:request_detail", kwargs={"pk": my_object.id, "type": self.kwargs.get("type")}))
        # if this is a child record
        else:
            if form.cleaned_data.get("stay_on_page"):
                messages.success(self.request, _(
                    "{} has been added as a traveller to this request. Please add any costs associated with this traveller.".format(
                        my_object.requester_name)))
                return HttpResponseRedirect(reverse("travel:request_edit", kwargs={"pk": my_object.id, "type": "pop"}))
            else:
                return HttpResponseRedirect(reverse("shared_models:close_me"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_dict = {}
        for user in User.objects.all():
            user_dict[user.id] = {}
            user_dict[user.id]['first_name'] = user.first_name
            user_dict[user.id]['last_name'] = user.last_name
            user_dict[user.id]['email'] = user.email

        user_json = json.dumps(user_dict)
        # send JSON file to template so that it can be used by js script
        context['user_json'] = user_json

        conf_dict = {}
        for conf in models.Conference.objects.all():
            conf_dict[conf.id] = {}
            conf_dict[conf.id]['location'] = conf.location
            conf_dict[conf.id]['start_date'] = conf.start_date.strftime("%Y-%m-%d")
            conf_dict[conf.id]['end_date'] = conf.end_date.strftime("%Y-%m-%d")

        conf_json = json.dumps(conf_dict)
        # send JSON file to template so that it can be used by js script
        context['conf_json'] = conf_json
        context['help_text_dict'] = get_help_text_dict()

        return context


class TripRequestDeleteView(CanModifyMixin, CommonDeleteView):
    model = models.TripRequest
    delete_protection = False
    home_url_name = "travel:index"

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("travel:request_detail", kwargs=self.kwargs)}

    def get_grandparent_crumb(self):
        kwargs = deepcopy(self.kwargs)
        del kwargs["pk"]
        return {"title": _("Trip Requests"), "url": reverse("travel:request_list", kwargs=kwargs)}

    def get_template_names(self):
        return 'shared_models/generic_popout_form.html' if self.kwargs.get(
            'type') == "pop" else 'travel/confirm_delete.html'

    def get_success_url(self):
        return reverse('shared_models:close_me') if self.kwargs.get('type') == "pop" else self.get_grandparent_crumb().get("url")

    def delete(self, request, *args, **kwargs):
        my_object = self.get_object()
        my_object.delete()

        if my_object.parent_request:
            my_trip = my_object.parent_request.trip
        else:
            my_trip = my_object.trip
        utils.manage_trip_warning(my_trip)

        messages.success(self.request,
                         'The trip request for {} {} was deleted successfully!'.format(my_object.first_name, my_object.last_name))
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)


class TripRequestCloneUpdateView(TripRequestUpdateView):
    h1 = gettext_lazy("Create a Clone Trip Request")
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
        new_obj.submitted = None
        new_obj.save()

        # add the reviewers based on the new request info
        utils.get_tr_reviewers(new_obj)
        utils.approval_seeker(new_obj)

        if new_obj.is_group_request:
            my_child_object = models.TripRequest.objects.create(
                user=self.request.user,
                first_name=self.request.user.first_name,
                last_name=self.request.user.last_name,
                email=self.request.user.email,
                parent_request=new_obj,
            )
            # pre-populate the costs on the 'child' record
            utils.populate_trip_request_costs(self.request, my_child_object)
        else:
            # import from old record
            # costs
            for old_rel_obj in old_obj.trip_request_costs.all():
                new_rel_obj = deepcopy(old_rel_obj)
                new_rel_obj.pk = None
                new_rel_obj.trip_request = new_obj
                new_rel_obj.save()

        if form.cleaned_data.get("stay_on_page"):
            return HttpResponseRedirect(reverse_lazy("travel:request_edit", kwargs={"pk": new_obj.id, "type": self.kwargs.get("type")}))
        else:
            return HttpResponseRedirect(reverse_lazy("travel:request_detail", kwargs={"pk": new_obj.id, "type": self.kwargs.get("type")}))


class ChildTripRequestCloneUpdateView(TripRequestUpdateView):
    def test_func(self):
        if self.request.user.id:
            return True

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        old_obj = models.TripRequest.objects.get(pk=new_obj.pk)
        new_obj.pk = None
        new_obj.submitted = None
        new_obj.save()

        # costs
        for old_rel_obj in old_obj.trip_request_costs.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.trip_request = new_obj
            new_rel_obj.save()

        return HttpResponseRedirect(reverse_lazy("travel:request_edit", kwargs={"pk": new_obj.id, "type": "pop"}))

    def get_initial(self):
        init = super().get_initial()
        init["user"] = None
        return init

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cloned"] = True
        return context


class TripRequestSubmitUpdateView(CanModifyMixin, CommonUpdateView):
    model = models.TripRequest
    form_class = forms.TripRequestApprovalForm
    template_name = 'travel/trip_request_submission_form.html'
    submit_text = gettext_lazy("Proceed")
    home_url_name = "travel:index"

    def get_active_page_name_crumb(self):
        my_object = self.get_object()
        if my_object.submitted:
            return _("Un-submit request")
        else:
            return _("Re-submit request") if my_object.status_id == "16" else _("Submit request")

    def get_h1(self):
        my_object = self.get_object()
        if my_object.submitted:
            return _("Do you wish to un-submit the following request?")
        else:
            return _("Do you wish to re-submit the following request?") if my_object.status_id == 16 else _(
                "Do you wish to submit the following request?")

    def get_h2(self):
        my_object = self.get_object()
        if my_object.submitted:
            return '<span class="red-font">WARNING: Un-submitting this request will reset the' \
                   ' status of any exisitng recommendations and/or approvals.</span>'

    def test_func(self):
        # This view is a little different. A trip owner should always be allowed to unsubmit
        return can_modify_request(self.request.user, self.kwargs.get("pk"), True)

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("travel:request_detail", kwargs=self.kwargs)}

    def get_grandparent_crumb(self):
        kwargs = deepcopy(self.kwargs)
        del kwargs["pk"]
        return {"title": _("Trip Requests"), "url": reverse("travel:request_list", kwargs=kwargs)}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_object = self.get_object()
        context["triprequest"] = my_object
        context["field_list"] = request_field_list if not my_object.is_group_request else request_group_field_list
        context["child_field_list"] = request_child_field_list
        context["reviewer_field_list"] = reviewer_field_list
        context["traveller_field_list"] = traveller_field_list

        context["conf_field_list"] = conf_field_list
        context["cost_field_list"] = cost_field_list
        context['help_text_dict'] = get_help_text_dict()
        context["report_mode"] = True
        return context

    def form_valid(self, form):
        my_object = form.save(commit=False)  # There is nothing really to save here. I am just using the machinery of UpdateView (djf)
        # figure out the current state of the request
        is_submitted = True if my_object.submitted else False

        # if submitted, then unsumbit but only if admin or owner
        if is_submitted:
            #  UNSUBMIT REQUEST
            if in_travel_admin_group(self.request.user) or my_object.user == self.request.user:
                my_object.submitted = None
                my_object.status_id = 8
                my_object.save()
                # reset all the reviewer statuses
                utils.end_review_process(my_object)
            else:
                messages.error(self.request, "sorry, only admins or owners can unsubmit requests")
        else:
            if my_object.trip.status_id != 30 and my_object.trip.status_id != 41 and my_object.status_id != 16:
                messages.error(self.request, "sorry, the trip you are requesting to attend is not accepting additional requests.")
            else:

                #  SUBMIT REQUEST
                my_object.submitted = timezone.now()
                # if there is not an original submission date, add one
                if not my_object.original_submission_date:
                    my_object.original_submission_date = timezone.now()
                # if the request is being resubmitted, this is a special case...
                if my_object.status_id == 16:
                    my_object.status_id = 8  # it doesn't really matter what we set the status to. The approval_seeker func will handle this
                    my_object.save()
                else:
                    # set all the reviewer statuses to 'queued'
                    utils.start_review_process(my_object)
                    # go and get approvals!!

        # No matter what business was done, we will call this function to sort through reviewer and request statuses
        utils.approval_seeker(my_object)
        my_object.save()

        # clean up any unused cost categories
        utils.clear_empty_trip_request_costs(my_object)
        for child in my_object.children_requests.all():
            utils.clear_empty_trip_request_costs(child)

        return HttpResponseRedirect(reverse("travel:request_detail", kwargs=self.kwargs))


class TripRequestCancelUpdateView(TravelAdminRequiredMixin, CommonUpdateView):
    model = models.TripRequest
    form_class = forms.TripRequestAdminNotesForm
    template_name = 'travel/trip_request_cancel_form.html'
    h1 = gettext_lazy("Do you wish to cancel the following trip request?")
    active_page_name_crumb = gettext_lazy("Cancel request")
    submit_text = gettext_lazy("Proceed")

    def get_h2(self):
        return "<span class='red-font blink-me'>" + \
               _("Please note that this action cannot be undone!!") + \
               "</span>"

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("travel:request_detail", kwargs=self.kwargs)}

    def get_grandparent_crumb(self):
        kwargs = deepcopy(self.kwargs)
        del kwargs["pk"]
        return {"title": _("Trip Requests"), "url": reverse("travel:request_list", kwargs=kwargs)}

    def get_context_data(self, **kwargs):
        my_object = self.get_object()

        # figure out the current state of the request
        is_cancelled = True if my_object.status.id == 22 else False
        context = super().get_context_data(**kwargs)
        context["triprequest"] = my_object
        context["field_list"] = request_field_list if not my_object.is_group_request else request_group_field_list
        context["child_field_list"] = request_child_field_list
        context["reviewer_field_list"] = reviewer_field_list
        context["traveller_field_list"] = traveller_field_list

        context["conf_field_list"] = conf_field_list
        context["cost_field_list"] = cost_field_list
        context['help_text_dict'] = get_help_text_dict()
        context["report_mode"] = True
        return context

    def form_valid(self, form):
        my_trip_request = form.save()

        # figure out the current state of the request
        is_cancelled = True if my_trip_request.status.id == 22 else False

        if is_cancelled:
            messages.warning(self.request, _("sorry, un-cancelling a trip is currently not an option"))
            return HttpResponseRedirect(reverse("travel:request_detail", kwargs=self.kwargs))

            # UN-CANCEL THE REQUEST
            # my_trip_request.status_id = 11
        else:
            #  CANCEL THE REQUEST
            my_trip_request.status_id = 22
            my_trip_request.save()

            # cancel any outstanding reviews:
            # but only those with the following statuses: PENDING = 1; QUEUED = 20;
            tr_reviewer_statuses_of_interest = [1, 20, ]
            for r in my_trip_request.reviewers.filter(status_id__in=tr_reviewer_statuses_of_interest):
                r.status_id = 5
                r.save()

            # send an email to the trip_request owner
            email = emails.StatusUpdateEmail(my_trip_request)
            # # send the email object
            custom_send_mail(
                subject=email.subject,
                html_message=email.message,
                from_email=email.from_email,
                recipient_list=email.to_list
            )
            return HttpResponseRedirect(reverse("travel:request_detail", kwargs=self.kwargs))


class TripRequestAdminNotesUpdateView(TravelAdminRequiredMixin, CommonPopoutUpdateView):
    model = models.TripRequest
    form_class = forms.TripRequestAdminNotesForm
    h1 = _("Administrative Notes (Public)")


# TRIP REQUEST REVIEW #
#########################


class TripRequestReviewListView(TravelAccessRequiredMixin, CommonListView):
    model = models.TripRequest
    template_name = 'travel/trip_request_review_list.html'
    home_url_name = "travel:index"
    field_list = [
        {"name": 'status_string|{}'.format(_("Request status")), "class": "", "width": ""},
        {"name": 'is_group_request|type', "class": "", "width": ""},
        {"name": 'first_name', "class": "", "width": ""},
        {"name": 'last_name', "class": "", "width": ""},
        {"name": 'trip', "class": "", "width": ""},
        {"name": 'destination', "class": "", "width": ""},
        {"name": 'start_date', "class": "", "width": ""},
        {"name": 'end_date', "class": "", "width": ""},
        {"name": 'total_request_cost|{}'.format(_("Total cost (DFO)")), "class": "", "width": ""},
    ]

    def get_h1(self):
        if self.kwargs.get("type") == "awaiting":
            return _("Requests Awaiting Your Review")
        else:
            return _("Requests Assigned to You for Review")

    def get_queryset(self):
        if self.kwargs.get("which_ones") == "awaiting":
            qs = models.TripRequest.objects.filter(
                pk__in=[reviewer.trip_request.id for reviewer in self.request.user.reviewers.filter(status_id=1).filter(
                    ~Q(trip_request__status_id__in=[16, 14]))])
        else:
            qs = models.TripRequest.objects.filter(pk__in=[reviewer.trip_request.id for reviewer in self.request.user.reviewers.all()])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["awaiting"] = True if self.kwargs.get("which_ones") else False
        return context


class TripRequestAdminApprovalListView(TravelAdminRequiredMixin, CommonListView):
    model = models.TripRequest
    template_name = 'travel/trip_request_review_list.html'
    home_url_name = "travel:index"
    field_list = [
        {"name": 'is_group_request', "class": "", "width": ""},
        {"name": 'first_name', "class": "", "width": ""},
        {"name": 'last_name', "class": "", "width": ""},
        {"name": 'trip', "class": "", "width": ""},
        {"name": 'destination', "class": "", "width": ""},
        {"name": 'start_date', "class": "", "width": ""},
        {"name": 'end_date', "class": "", "width": ""},
        {"name": 'total_request_cost|{}'.format(_("Total cost (DFO)")), "class": "", "width": ""},
    ]

    def get_h1(self):
        return _("Admin Request Approval List") + ' ({})'.format(_(self.kwargs.get("type")).upper())

    def get_queryset(self):
        # return a list only of those awaiting ADM or RDG approval
        qs = models.TripRequest.objects.filter(parent_request__isnull=True).order_by("-submitted")
        if self.kwargs.get("type") == "adm":
            qs = qs.filter(status_id=14)
        elif self.kwargs.get("type") == "rdg":
            qs = qs.filter(status_id=15)
        if self.kwargs.get("region"):
            qs = qs.filter(section__division__branch__region_id=self.kwargs.get("region"))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["random_object"] = models.TripRequest.objects.first()
        context["admin"] = True
        context["type_bilingual"] = _(self.kwargs.get("type")).upper()
        return context


class TripRequestReviewerADMUpdateView(AdminOrApproverRequiredMixin, CommonPopoutUpdateView):
    model = models.Reviewer
    form_class = forms.ReviewerApprovalForm

    # template_name = 'travel/adm_reviewer_approval_form.html'

    def get_h1(self):
        if self.kwargs.get("approve") == 1:
            return _("Do you wish to approve the following request for {}".format(
                self.get_object().trip_request.requester_name
            ))
        else:
            return _("Do you wish to deny the following request for {}".format(
                self.get_object().trip_request.requester_name
            ))

    def get_h2(self):
        return "<span class='red-font'>{}</span>".format(_("These comments will be visible to the traveller"))

    def get_submit_text(self):
        return _("Approve") if self.kwargs.get("approve") == 1 else _("Deny")

    def get_submit_btn_class(self):
        return "btn-success" if self.kwargs.get("approve") == 1 else "btn-danger"

    def test_func(self):
        my_trip_request = self.get_object().trip_request
        my_user = self.request.user
        # print(in_travel_admin_group(my_user) or is_approver(my_user, my_trip_request))
        if in_travel_admin_group(my_user) or is_approver(my_user, my_trip_request):
            return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_object = self.get_object()
        return context

    def form_valid(self, form):
        # don't save the reviewer yet because there are still changes to make
        my_reviewer = form.save(commit=True)
        tr = my_reviewer.trip_request
        parent_request = tr.parent_request

        is_approved = True if self.kwargs.get("approve") == 1 else False

        # if it was approved, then we change the reviewer status to 'approved'
        if is_approved:
            my_reviewer.status_id = 2
        # if it was denied, then we change the reviewer status to 'denied'
        else:
            my_reviewer.status_id = 3

        my_reviewer.status_date = timezone.now()
        my_reviewer.save()
        # big fork in process here between individual and child requests...
        # 1) individual request:
        ################
        if not parent_request:
            # update any statuses if necessary; this is business as usual
            utils.approval_seeker(my_reviewer.trip_request)
        else:
            # if this is a child request,
            if my_reviewer.status_id == 3:
                tr.status_id = 10
            else:
                tr.status_id = 11
            tr.save()

            # now we must update the trip reviewer comments so that they are in sync with the child review comments
            # best to make from scratch to avoid complexities with duplicating information
            parent_reviewer = parent_request.adm  # let's hope there is only one
            # let's get all the approved or denied children requests and append the comments to the parent_reviewer
            comments = ""
            for child_request in parent_request.children_requests.filter(status_id__in=[10, 11]):
                comments += f'{child_request.requester_name} &rarr; {child_request.adm.comments}<br>'
            parent_reviewer.comments = comments
            parent_reviewer.save()

            # if we are at the point where all the children request have been approved or denied,
            # we are ready to make headway on the parent request
            if parent_request.children_requests.filter(status_id__in=[10, 11]).count() == parent_request.children_requests.all().count():
                # the parent request is approved if there is at least one approved traveller
                if parent_request.children_requests.filter(status_id=11).count() > 0:
                    parent_reviewer.status_id = 2
                else:
                    parent_reviewer.status_id = 3
                parent_reviewer.status_date = timezone.now()
                parent_reviewer.save()

                utils.approval_seeker(parent_request)

            #
            #             # We have to append any comments to the corresponding review of the parent request
            #             if  tr.smart_reviewers.filter(role_id=5, status_id=1).count() == 1: # if the parent request has a adm reviewer that is pending, here is our match!
            #                 parent_review = tr.smart_reviewers.get(role_id=5, status_id=1)
            #
            # # TODO: maybe the button should say something like "remove from group request"
            #
            #             parent_request = tr.parent_request
            #             if parent_request.comments:
            #                 pass

            # # send an email to the request owner
            # email = emails.ChangesRequestedEmail(my_reviewer.trip_request)
            # # send the email object
            # custom_send_mail(
            #     subject=email.subject,
            #     html_message=email.message,
            #     from_email=email.from_email,
            #     recipient_list=email.to_list
            # )
            pass

        return HttpResponseRedirect(self.get_success_url())


class TripRequestReviewerUpdateView(AdminOrApproverRequiredMixin, CommonUpdateView):
    model = models.Reviewer
    form_class = forms.ReviewerApprovalForm
    template_name = 'travel/reviewer_approval_form.html'
    home_url_name = "travel:index"

    def get_h1(self):
        if self.get_object().role_id in [5, 6, ]:
            return _("Do you wish to approve on behalf of {user} ({role})".format(
                user=self.get_object().trip_request.current_reviewer.user,
                role=self.get_object().trip_request.current_reviewer.role,
            ))
        else:
            if self.get_object().trip_request.is_group_request:
                return _("Do you wish to approve the following group request?")
            else:
                return _("Do you wish to approve the following request?")

    def get_parent_crumb(self):
        role = self.get_object().role
        if role.id in [5, 6, ]:
            txt = _("Admin Request Approval List") + f' ({self.get_object().role})'
            kwargs = {"type": self.get_object().role.name.lower(),
                      "region": self.get_object().trip_request.section.division.branch.region.id}
            return {"title": txt, "url": reverse("travel:admin_approval_list", kwargs=kwargs)}
        else:
            return {"title": _("Requests Awaiting Your Review"),
                    "url": reverse("travel:request_review_list", kwargs={"which_ones": "awaiting"})}

    def test_func(self):
        my_trip_request = self.get_object().trip_request
        my_user = self.request.user
        # print(in_travel_admin_group(my_user) or is_approver(my_user, my_trip_request))
        if in_travel_admin_group(my_user) or is_approver(my_user, my_trip_request):
            return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_object = self.get_object()
        context["field_list"] = request_field_list if not my_object.trip_request.is_group_request else request_group_field_list
        context["child_field_list"] = request_child_field_list
        context["reviewer_field_list"] = reviewer_field_list
        context["traveller_field_list"] = traveller_field_list

        context["conf_field_list"] = conf_field_list
        context["cost_field_list"] = cost_field_list
        context['help_text_dict'] = get_help_text_dict()
        context["is_reviewer"] = self.request.user in [r.user for r in self.get_object().trip_request.reviewers.all()]
        context["trip"] = my_object.trip_request.trip
        context["triprequest"] = my_object.trip_request
        context["report_mode"] = True
        if my_object.role_id in [5, 6, ]:
            context["admin"] = True
            context["type_bilingual"] = _(self.kwargs.get("type")).upper()
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
                my_reviewer.trip_request.status_id = 16
                my_reviewer.trip_request.submitted = None
                my_reviewer.trip_request.save()
                # send an email to the request owner
                email = emails.ChangesRequestedEmail(my_reviewer.trip_request)
                # send the email object
                custom_send_mail(
                    subject=email.subject,
                    html_message=email.message,
                    from_email=email.from_email,
                    recipient_list=email.to_list
                )
                messages.success(self.request, _("Success! An email has been sent to the trip request owner."))

            # if it was approved, then we change the reviewer status to 'approved'
            elif approved:
                my_reviewer.status_id = 2
                my_reviewer.status_date = timezone.now()
                my_reviewer.save()
            # if it was approved, then we change the reviewer status to 'approved'
            else:
                my_reviewer.status_id = 3
                my_reviewer.status_date = timezone.now()
                my_reviewer.save()

        # update any statuses if necessary
        utils.approval_seeker(my_reviewer.trip_request)

        if stay_on_page:
            return HttpResponseRedirect(reverse("travel:tr_review_update", kwargs=self.kwargs))
        else:
            # the answer lies in the parent crumb...
            parent_crumb_url = self.get_parent_crumb().get("url")
            return HttpResponseRedirect(parent_crumb_url)


class SkipReviewerUpdateView(TravelAdminRequiredMixin, CommonPopoutUpdateView):
    model = models.Reviewer
    form_class = forms.ReviewerSkipForm
    template_name = 'shared_models/generic_popout_form.html'

    def get_h1(self):
        return _("Are you certain you wish to skip the following user?")

    def get_h2(self):
        return str(self.get_object())

    def test_func(self):
        my_trip_request = self.get_object().trip_request
        my_user = self.request.user
        # print(in_travel_admin_group(my_user) or is_approver(my_user, my_trip_request))
        if in_travel_admin_group(my_user) or is_approver(my_user, my_trip_request):
            return True

    def form_valid(self, form):
        # if the form is submitted, that means the admin user has decided to go ahead with the manual skip
        my_reviewer = form.save(commit=False)
        my_reviewer.status_id = 21
        my_reviewer.status_date = timezone.now()
        my_reviewer.comments = "This reviewer was manually overridden by {} with the following rationale: \n\n {}".format(self.request.user,
                                                                                                                          my_reviewer.comments)
        # now we save the reviewer for real
        my_reviewer.save()
        # update any statuses if necessary
        utils.approval_seeker(my_reviewer.trip_request)

        return HttpResponseRedirect(reverse("shared_models:close_me"))


@login_required(login_url='/accounts/login/')
# @user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def reset_reviewers(request, type, triprequest=None, trip=None):
    """this function will reset the reviewers on either a trip request or trip
    """
    if triprequest:
        my_obj = models.TripRequest.objects.get(pk=triprequest)
        if can_modify_request(request.user, triprequest):
            # This function should only ever be run if the TR is a draft
            if my_obj.status.id == 8:
                # first remove any existing reviewers
                my_obj.reviewers.all().delete()
                # next, re-add the defaults...
                utils.get_tr_reviewers(my_obj)
            else:
                messages.error(request, _("This function can only be used when the trip request is still a draft"))
        else:
            messages.error(request, _("You do not have the permissions to reset the reviewer list"))
        return HttpResponseRedirect(reverse("travel:request_detail", args=(triprequest, type)))

    elif trip:
        # first, this should only ever be an ADM admin group
        if not in_adm_admin_group(request.user):
            return HttpResponseForbidden()
        else:
            my_obj = models.Conference.objects.get(pk=trip)
            # This function should only ever be run if the trip is unreviewed (30 = unverified, unreviewer; 41 = verified, reviewed)
            if my_obj.status.id in [30, 41]:
                # first remove any existing reviewers
                my_obj.reviewers.all().delete()
                # next, re-add the defaults...
                utils.get_trip_reviewers(my_obj)
            else:
                messages.error(request, _("This function can only with an unreviewed trip."))
            return HttpResponseRedirect(reverse("travel:trip_detail", args=(trip, type)))


# REVIEWER #
############

class TripRequestReviewerHardDeleteView(CanModifyMixin, CommonHardDeleteView):
    model = models.Reviewer

    def test_func(self):
        my_obj = models.Reviewer.objects.get(pk=self.kwargs.get("pk"))
        if can_modify_request(self.request.user, my_obj.trip_request.id):
            if my_obj.status_id not in [4, 20]:
                messages.error(self.request, _(f"Sorry, you cannot delete a reviewer who's status is set to {my_obj.status}"))
            else:
                return True


class TripReviewerHardDeleteView(TravelADMAdminRequiredMixin, CommonHardDeleteView):
    model = models.TripReviewer

    def test_func(self):
        my_obj = models.TripReviewer.objects.get(pk=self.kwargs.get("pk"))
        if in_travel_admin_group(self.request.user):
            if my_obj.status_id not in [23, 24]:
                messages.error(self.request, _(f"Sorry, you cannot delete a reviewer who's status is set to {my_obj.status}"))
            else:
                return True


@login_required(login_url='/accounts/login/')
# @user_passes_test(is_superuser, login_url='/accounts/denied/')
def manage_reviewers(request, type, triprequest=None, trip=None):
    if triprequest:
        my_trip_request = models.TripRequest.objects.get(pk=triprequest)
        if can_modify_request(request.user, my_trip_request.id):
            # if not my_trip_request.status_id in [8, 16]:
            #     messages.error(request, _("Sorry, you will have to unsubmit the trip in order to make this change"))
            #     return HttpResponseRedirect(reverse("travel:request_detail", kwargs={"pk": my_trip_request.id}))
            # else:
            qs = models.Reviewer.objects.filter(trip_request=my_trip_request)
            if request.method == 'POST':
                formset = forms.ReviewerFormset(request.POST)
                if formset.is_valid():
                    formset.save()

                    my_trip_request.save()
                    # do something with the formset.cleaned_data
                    messages.success(request, _("The reviewer list has been successfully updated"))
                    return HttpResponseRedirect(reverse("travel:manage_tr_reviewers", args=(triprequest, type)))
            else:
                formset = forms.ReviewerFormset(
                    queryset=qs,
                    initial=[{"trip_request": my_trip_request}],
                )

            context = dict()
            context['triprequest'] = my_trip_request
            context['formset'] = formset
            context['type'] = type
            context["my_object"] = models.Reviewer.objects.first()
            context["field_list"] = [
                'order',
                'user',
                'role',
            ]
            return render(request, 'travel/reviewer_formset.html', context)
        else:
            messages.error(request, _("You do not have the permissions to modify the reviewer list"))
            return HttpResponseRedirect(reverse("travel:request_detail", args=(triprequest, type)))
    elif trip:
        my_trip = models.Conference.objects.get(pk=trip)
        if not in_adm_admin_group(request.user):
            return HttpResponseForbidden()
        elif my_trip.status_id not in [30, 41]:
            messages.error(request, _("Sorry, you cannot modify the reviewers on a trip that is under review."))
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            qs = models.TripReviewer.objects.filter(trip=trip)
            if request.method == 'POST':
                formset = forms.TripReviewerFormset(request.POST)
                if formset.is_valid():
                    formset.save()

                    my_trip.save()
                    # do something with the formset.cleaned_data
                    messages.success(request, _("The reviewer list has been successfully updated"))
                    return HttpResponseRedirect(reverse("travel:manage_trip_reviewers", args=(trip, type)))
            else:
                formset = forms.TripReviewerFormset(
                    queryset=qs,
                    initial=[{"trip": my_trip}],
                )

            context = dict()
            context['trip'] = my_trip
            context['type'] = type
            context['formset'] = formset
            context["my_object"] = models.TripReviewer.objects.first()
            context["field_list"] = [
                'order',
                'user',
                'role',
            ]
            return render(request, 'travel/reviewer_formset.html', context)


# TRIP #
########

class TripListView(TravelAccessRequiredMixin, CommonFilterView):
    model = models.Conference
    filterset_class = filters.TripFilter
    template_name = 'travel/trip_list.html'
    row_object_url_name = "travel:trip_detail"
    container_class = "container-fluid"
    subtitle = _("Trips")
    home_url_name = "travel:index"

    def get_new_object_url(self):
        return reverse("travel:trip_new", kwargs=self.kwargs)

    def get_queryset(self):
        queryset = models.Conference.objects.annotate(
            search_term=Concat(
                'name',
                Value(" "),
                'nom',
                Value(" "),
                'location',
                output_field=TextField()))
        # the only list that a regular user will have access to is th upcomming list
        if self.kwargs.get("type") == "upcoming":
            queryset = queryset.filter(start_date__gte=timezone.now())
        else:
            # otherwise, they should be an admin user
            if in_travel_admin_group(self.request.user):
                if self.kwargs.get("type").startswith("region"):
                    queryset = queryset.filter(lead_id=self.kwargs.get("type").replace("region-", ""))
                elif self.kwargs.get("type") == "adm-hit-list":
                    queryset = utils.get_adm_eligible_trips().annotate(
                        search_term=Concat(
                            'name',
                            Value(" "),
                            'nom',
                            Value(" "),
                            'location',
                            output_field=TextField())).order_by("adm_review_deadline")
                elif self.kwargs.get("type") == "adm-all":
                    queryset = queryset.filter(is_adm_approval_required=True)
            else:
                queryset = None
        return queryset

    def get_field_list(self):
        field_list = [
            {"name": 'fiscal_year', "class": "", "width": "75px"},
            {"name": 'status_string|{}'.format("status"), "width": "150px", },
            {"name": 'trip_subcategory', "class": "", "width": "200px", },
            {"name": 'tname|{}'.format(_("Trip title")), "class": "", },
            {"name": 'location|{}'.format(_("location")), "class": "", },
            {"name": 'abstract_deadline|{}'.format(_("abstract deadline")), "class": "", "width": "100px"},
            {"name": 'registration_deadline', "class": "", "width": "100px"},
            {"name": 'dates|{}'.format(_("trip dates")), "class": "", "width": "170px"},
            # {"name": 'number_of_days|{}'.format(_("length (days)")), "class": "center-col", },
            # {"name": 'lead|{}'.format(_("Regional lead")), "class": "center-col", },
            {"name": 'is_adm_approval_required|{}'.format(_("ADM approval required?")), "class": "center-col", },
            {"name": 'total_travellers|{}'.format(_("Total travellers")), "class": "center-col", },
            {"name": 'date_eligible_for_adm_review', "class": "center-col", "width": "100px"},
            # {"name": 'connected_requests|{}'.format(_("Connected requests")), "class": "center-col", },
            # {"name": 'verified_by', "class": "", },
        ]
        if self.kwargs.get("type") == "adm-hit-list" or self.kwargs.get("type") == "adm-all":
            field_list.append(
                {"name": 'adm_review_deadline|{}'.format(_("ADM decision deadline")), "class": "", "width": "200px"}
            )
        return field_list

    def get_h1(self):
        if self.kwargs.get("type") == "adm-hit-list":
            h1 = _("Trips Eligible for ADM Review")
        elif self.kwargs.get("type") == "adm-all":
            h1 = _("All Trips Requiring ADM Approval")
        elif self.kwargs.get("type") == "upcoming":
            h1 = _("Upcoming Trips")
        elif self.kwargs.get("region"):
            region = shared_models.Region.objects.get(pk=self.kwargs.get("region"))
            h1 = _("Trips") + f' ({str(region)})'
        else:
            h1 = _("Trips")
        return h1

    def get_h3(self):
        if self.kwargs.get("type") == "adm-hit-list":
            return "<em>(" + _("i.e., Trips which are fair game for ADMO review to begin") + ")</em>"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["paginate_by"] = None if self.kwargs.get("type") == "adm-hit-list" else 50
        context["is_admin"] = in_travel_admin_group(self.request.user)
        return context


class TripDetailView(TravelAccessRequiredMixin, CommonDetailView):
    model = models.Conference
    template_name = 'travel/trip_detail.html'
    home_url_name = "travel:index"

    def get_parent_crumb(self):
        my_kwargs = deepcopy(self.kwargs)
        del my_kwargs["pk"]
        trips_url = reverse("travel:trip_list", kwargs=my_kwargs)
        trips_title = _("Trips")
        return {"title": trips_title, "url": trips_url}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["conf_field_list"] = conf_field_list
        context["reviewer_field_list"] = reviewer_field_list
        context["traveller_field_list"] = traveller_field_list
        context["trip"] = self.get_object()
        context["can_modify"] = (self.get_object().is_adm_approval_required and in_adm_admin_group(self.request.user)) or (
                not self.get_object().is_adm_approval_required and in_travel_admin_group(self.request.user))

        context["is_adm_admin"] = in_adm_admin_group(self.request.user)
        context["is_admin"] = in_travel_admin_group(self.request.user)
        context["is_reviewer"] = self.request.user in [r.user for r in self.get_object().reviewers.all()]

        return context


class TripAdminNotesUpdateView(TravelADMAdminRequiredMixin, CommonPopoutUpdateView):
    model = models.Conference
    form_class = forms.TripAdminNotesForm
    h1 = _("Administrative Notes (Public)")


class TripUpdateView(TravelAdminRequiredMixin, CommonUpdateView):
    model = models.Conference
    form_class = forms.TripForm
    home_url_name = "travel:index"

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse("travel:trip_detail", kwargs=self.kwargs)}

    def get_grandparent_crumb(self):
        my_kwargs = deepcopy(self.kwargs)
        del my_kwargs["pk"]
        trips_url = reverse("travel:trip_list", kwargs=my_kwargs)
        trips_title = _("Trips")
        return {"title": trips_title, "url": trips_url}

    def get_template_names(self):
        return 'travel/trip_form_popout.html' if self.kwargs.get("type") == "pop" else 'travel/trip_form.html'

    def form_valid(self, form):
        my_object = form.save()

        # This is a bit tricky here. Right now will work with the assumption that we do not ever want to reset the reviewers unless
        # the trip was ADM approval required, and now is not, OR if it wasn't and now it is.
        if my_object.is_adm_approval_required and my_object.reviewers.count() == 0 or not my_object.is_adm_approval_required:
            # Add any trip reviewers to the trip, if adm approval is required.
            # This function will also delete any reviewers if adm approval is not required
            utils.get_trip_reviewers(my_object)

        if self.kwargs.get("type") == "pop":
            return HttpResponseRedirect(reverse("shared_models:close_me"))
        else:
            return HttpResponseRedirect(reverse('travel:trip_detail', kwargs=self.kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()

        return context


class TripCreateView(TravelAccessRequiredMixin, CommonCreateView):
    model = models.Conference
    form_class = forms.TripForm
    home_url_name = "travel:index"

    def get_parent_crumb(self):
        trips_url = reverse("travel:trip_list", kwargs=self.kwargs)
        if self.kwargs.get("type") == "upcoming":
            trips_title = _("Upcoming Trips")
        elif self.kwargs.get("type") == "adm-hit-list":
            # trips_url = reverse("travel:trip_list", kwargs={"type": self.kwargs.get("type")})
            trips_title = _("Trips Eligible for ADM Review")
        elif self.kwargs.get("region"):
            region = shared_models.Region.objects.get(pk=self.kwargs.get("region"))
            # trips_url = reverse("travel:trip_list", kwargs={"region": self.kwargs.get("region")})
            trips_title = _("Trips") + f' ({str(region)})'
        else:
            return None
        return {"title": trips_title, "url": trips_url}

    def get_template_names(self):
        if self.kwargs.get("type") == "pop":
            return 'travel/trip_form_popout.html'
        else:
            return 'travel/trip_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()

        return context

    def form_valid(self, form):
        my_object = form.save()

        # Add any trip reviewers to the trip, if adm approval is required
        utils.get_trip_reviewers(my_object)

        if self.kwargs.get("type") == "pop":
            # create a new email object
            email = emails.NewTripEmail(my_object)
            # send the email object
            custom_send_mail(
                subject=email.subject,
                html_message=email.message,
                from_email=email.from_email,
                recipient_list=email.to_list
            )
            messages.success(self.request,
                             _("The trip has been added to the database!"))

            return HttpResponseRedirect(reverse("shared_models:close_me_no_refresh"))
        else:
            return HttpResponseRedirect(reverse("travel:trip_detail", kwargs={"pk": my_object.id, "type": "pop"}))


class TripDeleteView(TravelAdminRequiredMixin, CommonDeleteView):
    template_name = 'travel/confirm_delete.html'
    model = models.Conference
    success_message = 'The trip was deleted successfully!'
    delete_protection = False

    def get_success_url(self):
        if self.kwargs.get("type") == "back_to_verify":
            adm = 1 if self.get_object().is_adm_approval_required else 0
            region = self.get_object().lead.id if adm == 0 else 0
            success_url = reverse_lazy('travel:admin_trip_verification_list', kwargs={"adm": adm, "region": region})
        else:
            my_kwargs = self.kwargs
            del my_kwargs["pk"]
            success_url = reverse_lazy('travel:trip_list', kwargs=my_kwargs)
        return success_url


class TripReviewProcessUpdateView(TravelADMAdminRequiredMixin, CommonUpdateView):
    model = models.Conference
    form_class = forms.TripTimestampUpdateForm
    template_name = 'travel/trip_review_process_form.html'
    submit_text = _("Proceed")

    def test_func(self):
        # make sure that this page can only be accessed for active trips (exclude those already reviewed and those canceled)
        return in_adm_admin_group(self.request.user) and not self.get_object().status_id in [32, 43]

    def get_h1(self):
        if self.get_object().status_id in [30, 41]:
            return _("Do you wish to start a review on the following trip?")
        else:
            return _("Do you wish to end a review on the following trip?")

    def get_h2(self):
        if self.get_object().status_id in [30, 41]:
            return '<span class="blue-font">WARNING: starting a review on this trip will prevent any additional' \
                   ' travellers from adding themselves to it.</span>'
        else:
            return '<span class="red-font">WARNING: stopping the review on this trip will reset the' \
                   ' status of any exisitng recommendations and/or approvals.</span>'

    def get_subtitle(self):
        return _("Start a Review") if self.get_object().status_id in [30, 41] else _("End a Review")

    # def get_parent_crumb(self):
    #     return {"title":str(self.get_object()), "url": reverse("travel:trip_detail", kwargs=self.kwargs)}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip"] = self.get_object()
        context["traveller_field_list"] = traveller_field_list

        context["conf_field_list"] = conf_field_list
        context['help_text_dict'] = get_help_text_dict()
        return context

    def form_valid(self, form):
        my_trip = form.save()
        # figure out the current state of the request
        is_under_review = False if my_trip.status_id in [30, 41] else True

        if is_under_review:
            utils.end_trip_review_process(my_trip)
        else:
            utils.start_trip_review_process(my_trip)
            # go and get approvals!!

        # No matter what business what done, we will call this function to sort through reviewer and request statuses
        utils.trip_approval_seeker(my_trip)
        my_trip.save()

        # decide where to go. If the request user is the same as the active reviewer for the trip, go right to the review page.
        # otherwise go to the index
        if my_trip.current_reviewer and self.request.user == my_trip.current_reviewer.user:
            return HttpResponseRedirect(reverse("travel:trip_reviewer_update", kwargs={"pk": my_trip.current_reviewer.id}))
        else:
            my_kwargs = deepcopy(self.kwargs)
            my_kwargs["type"] = "all"
            return HttpResponseRedirect(reverse("travel:trip_detail", kwargs=my_kwargs))


class TripVerificationListView(TravelAdminRequiredMixin, CommonListView):
    template_name = 'travel/trip_verification_list.html'
    home_url_name = "travel:index"
    h1 = gettext_lazy("Trips Awaiting Verification")

    field_list = [
        {"name": 'fiscal_year', "class": "", "width": "75px"},
        {"name": 'tname|{}'.format("Name"), "class": "", "width": ""},
        {"name": 'trip_subcategory', "class": "", "width": ""},
        {"name": 'location|{}'.format(_("location")), "class": "", "width": ""},
        {"name": 'dates|{}'.format(_("dates")), "class": "", "width": "180px"},
        {"name": 'number_of_days|{}'.format(_("length (days)")), "class": "center-col", "width": ""},
        {"name": 'is_adm_approval_required|{}'.format(_("ADM approval required?")), "class": "center-col", "width": ""},
    ]

    def get_queryset(self):
        if self.kwargs.get("adm") == 1:
            queryset = models.Conference.objects.filter(status_id=30, is_adm_approval_required=True)
        else:
            queryset = models.Conference.objects.filter(
                status_id=30, lead_id=self.kwargs.get("region"), is_adm_approval_required=False
            )
        return queryset


class TripVerifyUpdateView(TravelAdminRequiredMixin, CommonFormView):
    template_name = 'travel/trip_verification_form.html'
    model = models.Conference
    form_class = forms.TripRequestApprovalForm
    home_url_name = "travel:index"
    h1 = gettext_lazy("Verify Trip")

    def get_parent_crumb(self):
        my_kwargs = deepcopy(self.kwargs)
        del my_kwargs["pk"]
        return {"title": _("Trips Awaiting Verfication"), "url": reverse_lazy("travel:admin_trip_verification_list", kwargs=my_kwargs)}

    def test_func(self):
        my_trip = models.Conference.objects.get(pk=self.kwargs.get("pk"))
        if my_trip.is_adm_approval_required:
            return in_adm_admin_group(self.request.user)
        else:
            return in_travel_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("accounts:denied_access", kwargs={
                "message": _("Sorry, only ADMO administrators can verify trips that require ADM approval.")}))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_trip = models.Conference.objects.get(pk=self.kwargs.get("pk"))
        context["object"] = my_trip
        context["conf_field_list"] = conf_field_list
        context["trip_subcategories"] = models.TripSubcategory.objects.all()

        base_qs = models.Conference.objects.filter(~Q(id=my_trip.id)).filter(fiscal_year=my_trip.fiscal_year)

        context["same_day_trips"] = base_qs.filter(Q(start_date=my_trip.start_date) | Q(end_date=my_trip.end_date))

        context["same_location_trips"] = base_qs.filter(
            id__in=[trip.id for trip in base_qs if trip.location and my_trip.location and
                    utils.compare_strings(trip.location, my_trip.location) < 3]
        )

        similar_fr_name_trips = [trip.id for trip in base_qs if
                                 trip.nom and utils.compare_strings(trip.nom, trip.name) < 15] if my_trip.nom else []
        similar_en_name_trips = [trip.id for trip in base_qs if utils.compare_strings(trip.name, my_trip.name) < 15]
        my_list = list()
        my_list.extend(similar_en_name_trips)
        my_list.extend(similar_fr_name_trips)
        context["same_name_trips"] = base_qs.filter(
            id__in=set(my_list)
        )
        return context

    def form_valid(self, form):
        my_trip = models.Conference.objects.get(pk=self.kwargs.get("pk"))
        my_trip.status_id = 41
        my_trip.verified_by = self.request.user
        my_trip.save()
        return HttpResponseRedirect(reverse("travel:admin_trip_verification_list",
                                            kwargs={"region": self.kwargs.get("region"),
                                                    "adm": self.kwargs.get("adm")}))


class TripSelectFormView(TravelAdminRequiredMixin, CommonPopoutFormView):
    form_class = forms.TripSelectForm
    h1 = _("Please select a trip to re-assign:")
    h3 = _("(You will have a chance to review this action before it is carried out.)")
    submit_text = _("Proceed")

    def test_func(self):
        my_trip = models.Conference.objects.get(pk=self.kwargs.get("pk"))
        if my_trip.is_adm_approval_required:
            return in_adm_admin_group(self.request.user)
        else:
            return in_travel_admin_group(self.request.user)

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
    h1 = _("Please confirm the following:")
    submit_text = _("Confirm")
    field_list = [
        "name",
        "nome",
        'location',
        'lead',
        'start_date',
        'end_date',
        'meeting_url',
        'is_adm_approval_required',
        'status_string|{}'.format("status"),
        'traveller_list|{}'.format("travellers"),
        'requests|{}'.format("linked trip requests"),
    ]

    def test_func(self):
        my_trip = models.Conference.objects.get(pk=self.kwargs.get("trip_a"))
        if my_trip.is_adm_approval_required:
            return in_adm_admin_group(self.request.user)
        else:
            return in_travel_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("accounts:denied_access", kwargs={
                "message": _("Sorry, only ADMO administrators can verify trips that require ADM approval.")}))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip_a = models.Conference.objects.get(pk=self.kwargs.get("trip_a"))
        trip_b = models.Conference.objects.get(pk=self.kwargs.get("trip_b"))

        context["trip_a"] = trip_a
        context["trip_b"] = trip_b
        context["trip_list"] = [trip_a, trip_b]

        # start out optimistic
        duplicate_ppl = list()
        # we have to sift through each tr that will be transferred to the new trip and ensure that there is no overlap with the new travellers
        request_users_from_trip_b = [tr.user for tr in trip_b.trip_requests.all() if
                                     tr.user]  # this will be only individual requests and parent group requests
        travellers_from_trip_b = trip_b.traveller_list
        for tr in trip_a.trip_requests.all():
            # if
            if tr.user and tr.user in request_users_from_trip_b:
                duplicate_ppl.append(tr.user)

            # now, depending on whether this request is a group request, our method will change.
            # if TR is a group request, we have to make sure there is no overlap in the travellers
            # but because of the traveller() method, we can just use one approach

            else:
                for traveller in tr.travellers:
                    if traveller in travellers_from_trip_b:
                        duplicate_ppl.append(traveller)

        context["duplicate_ppl"] = duplicate_ppl
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            trip_a = models.Conference.objects.get(pk=self.kwargs.get("trip_a"))
            trip_b = models.Conference.objects.get(pk=self.kwargs.get("trip_b"))

            for tr in trip_a.trip_requests.all():
                tr.trip = trip_b
                tr.save()

            # trip_a.delete()
            return HttpResponseRedirect(reverse("shared_models:close_me"))


class TripReviewListView(TravelAccessRequiredMixin, CommonListView):
    model = models.Conference
    template_name = 'travel/trip_review_list.html'
    home_url_name = "travel:index"
    field_list = [
        {"name": 'status_string|{}'.format(_("status")), "class": "", },
        {"name": 'tname|{}'.format(_("Trip title")), "class": "", },
        {"name": 'location|{}'.format(_("location")), "class": "", },
        {"name": 'dates|{}'.format(_("dates")), "class": "", "width": "180px"},
        {"name": 'number_of_days|{}'.format(_("length (days)")), "class": "center-col", },
        {"name": 'is_adm_approval_required|{}'.format(_("ADM approval required?")), "class": "center-col", },
        {"name": 'total_travellers|{}'.format(_("Total travellers")), "class": "center-col", },
        {"name": 'connected_requests|{}'.format(_("Connected requests")), "class": "center-col", },
        {"name": 'verified_by', "class": "", },
    ]

    def get_queryset(self):
        if self.kwargs.get("which_ones") == "awaiting":
            qs = models.Conference.objects.filter(
                pk__in=[reviewer.trip_id for reviewer in self.request.user.trip_reviewers.filter(status_id=25)])
        else:
            qs = models.Conference.objects.filter(pk__in=[reviewer.trip_id for reviewer in self.request.user.trip_reviewers.all()])
        return qs

    def get_h1(self):
        if self.kwargs.get("which_ones") == "awaiting":
            h1 = _("Trips Awaiting Your Review")
        else:
            h1 = _("Tagged Trips")
        return h1

    def get_row_object_url_name(self):
        if self.kwargs.get("which_ones") == "awaiting":
            return "travel:trip_reviewer_update"
        else:
            return "travel:trip_detail"


class TripReviewerUpdateView(TravelADMAdminRequiredMixin, CommonUpdateView):
    model = models.TripReviewer
    form_class = forms.ReviewerApprovalForm
    template_name = 'travel/trip_reviewer_approval_form.html'
    back_url = reverse_lazy("travel:trip_review_list")
    cancel_text = _("Cancel")
    home_url_name = "travel:index"
    parent_crumb = {"title": _("Trips Awaiting Your Review"),
                    "url": reverse_lazy("travel:trip_review_list", kwargs={"which_ones": "awaiting"})}

    def test_func(self):
        my_trip = self.get_object().trip
        my_user = self.request.user
        if is_trip_approver(my_user, my_trip):
            return True

    def get_h1(self):
        my_str = _("{}'s Trip Review".format(self.get_object().user.first_name))
        if self.get_object().role_id == 5:  # if ADM
            my_str += " ({})".format(_("ADM Level Review"))
        return my_str

    def get_submit_text(self):
        if self.get_object().role_id == 5:  # if ADM
            submit_text = _("Complete the review")
        else:
            submit_text = _("Submit your review")
        return submit_text

    def get_h3(self):
        return self.get_object().trip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["conf_field_list"] = conf_field_list
        context["trip"] = self.get_object().trip
        context["reviewer_field_list"] = reviewer_field_list
        context["traveller_field_list"] = traveller_field_list

        context["report_mode"] = True
        trip = self.get_object().trip
        context["is_adm_admin"] = in_adm_admin_group(self.request.user)
        context["is_admin"] = in_travel_admin_group(self.request.user)
        context["is_reviewer"] = self.request.user in [r.user for r in self.get_object().trip.reviewers.all()]

        # if this is the ADM looking at the page, we need to provide more data
        if self.get_object().role_id == 5:
            # prime a list of trip requests to run by the ADM. This will be a list of travellers (ie. ind TRs and child TRs; not parent records)
            adm_tr_list = list()
            # we need all the trip requests, excluding parents; start out with simple ones

            # get all ind TRs that are pending ADM, pending RDG, denied or accepted
            tr_id_list = [tr.id for tr in trip.trip_requests.filter(is_group_request=False, status_id__in=[14, 15, 10, 11])]

            # make a list of child requests whose parents are in the same status categories
            child_list = [child_tr.id for parent_tr in trip.trip_requests.filter(is_group_request=True, status_id__in=[14, 15, 10, 11]) for
                          child_tr in parent_tr.children_requests.all()]
            # extend the list
            tr_id_list.extend(child_list)
            # get a QS from the work done above
            trip_requests = models.TripRequest.objects.filter(id__in=tr_id_list)

            # go through each trip request
            for tr in trip_requests:
                # the child requests will be set as 'draft', change them to 'pending adm review'
                if tr.parent_request and tr.parent_request.status_id == 14 and tr.status_id == 8:
                    tr.status = tr.parent_request.status
                    tr.save()

                # get any adm reviewers of the trip request that is pending; it is important that we only look at parent requests for this
                # hence the use of `smart_reviewer` prop
                my_reviewer = tr.smart_reviewers.get(role_id=5) if tr.smart_reviewers.filter(role_id=5, status_id=1).count() == 1 else None

                # if there is a reviewer and the trip request is a child, we have to actually create a new trip request  reviewer for that child
                if my_reviewer and tr.parent_request:
                    # use get_or_create
                    status = my_reviewer.status
                    my_reviewer, created = models.Reviewer.objects.get_or_create(
                        trip_request=tr,
                        role=my_reviewer.role,
                        user=my_reviewer.user,
                    )
                    if created:
                        my_reviewer.status = status
                        my_reviewer.save()

                adm_tr_list.append({"trip_request": tr, "reviewer": my_reviewer})
            context["adm_tr_list"] = adm_tr_list
            # we need to create a variable that ensures the adm cannot submit her request unless all the trip requests have been actionned
            # basically, we want to make sure there is nothing that has a trip request status of 14

            context["adm_can_submit"] = bool(self.get_object().trip.trip_requests.filter(status_id=14).count()) is False
        else:
            # otherwise we can always submit the trip
            context["adm_tr_list"] = None
            context["adm_can_submit"] = True
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
                my_reviewer.status_id = 26
                my_reviewer.status_date = timezone.now()
                my_reviewer.save()

            # update any statuses if necessary
            utils.trip_approval_seeker(my_reviewer.trip)
            return HttpResponseRedirect(reverse("travel:trip_review_list", kwargs={"which_ones": "awaiting"}))

        else:
            my_kwargs = {"pk": my_reviewer.id}
            return HttpResponseRedirect(reverse("travel:trip_reviewer_update", kwargs=my_kwargs))


class SkipTripReviewerUpdateView(TravelAdminRequiredMixin, UpdateView):
    model = models.TripReviewer
    form_class = forms.ReviewerSkipForm
    template_name = 'travel/reviewer_skip_form.html'

    def test_func(self):
        my_trip_request = self.get_object().trip_request
        my_user = self.request.user
        # print(in_travel_admin_group(my_user) or is_approver(my_user, my_trip_request))
        if in_travel_admin_group(my_user) or is_approver(my_user, my_trip_request):
            return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_object = self.get_object()
        return context

    def form_valid(self, form):
        # if the form is submitted, that means the admin user has decided to go ahead with the manual skip
        my_reviewer = form.save(commit=False)
        my_reviewer.status_id = 21
        my_reviewer.status_date = timezone.now()
        my_reviewer.comments = "This step was manually overridden by {} with the following rationale: \n\n {}".format(self.request.user,
                                                                                                                      my_reviewer.comments)

        # now we save the reviewer for real
        my_reviewer.save()

        # update any statuses if necessary
        utils.approval_seeker(my_reviewer.trip_request)

        return HttpResponseRedirect(reverse("shared_models:close_me"))


class TripCancelUpdateView(TravelAdminRequiredMixin, CommonUpdateView):
    # TODO: check permissions
    # TODO: cancel related trip requests and email clients
    # TODO: email travellers the change in their statuses

    model = models.Conference
    form_class = forms.TripAdminNotesForm
    template_name = 'travel/trip_cancel_form.html'
    submit_text = _("Cancel the trip")
    h1 = _("Do you wish to un-cancel the following trip?")
    h2 = "<span class='red-font'>" + \
         _("Cancelling this trip will result in all linked requests to be 'cancelled'. "
           "This list of associated trip requests can be viewed below in the trip detail.") + \
         "</span><br><br>" + \
         "<span class='red-font blink-me'>" + \
         _("This action cannot be undone.") + \
         "</span>"
    active_page_name_crumb = _("Cancel Trip")

    # home_url_name = "travel:index"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["conf_field_list"] = conf_field_list
        context["trip"] = self.get_object()
        context["traveller_field_list"] = traveller_field_list

        context['help_text_dict'] = get_help_text_dict()
        context["report_mode"] = True
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
            for r in my_trip.reviewers.filter(status_id__in=trip_reviewer_statuses_of_interest):
                r.status_id = 44
                r.save()

            #  CANCEL THE TRIP
            my_trip.status_id = 43
            my_trip.save()

            # cycle through every trip request associated with this trip and cancel it
            # denied = 10; cancelled = 22; draft = 8;
            tr_statuses_to_skip = [10, 22, 8]
            for tr in my_trip.trip_requests.filter(~Q(status_id__in=tr_statuses_to_skip)):
                # set status to cancelled = 22
                tr.status_id = 22
                # update the admin notes
                if tr.admin_notes:
                    tr.admin_notes = f'{my_trip.admin_notes}\n\n{tr.admin_notes}'
                else:
                    tr.admin_notes = f'{my_trip.admin_notes}'
                tr.save()

                # cancel any outstanding reviews:
                # but only those with the following statuses: PENDING = 1; QUEUED = 20;
                tr_reviewer_statuses_of_interest = [1, 20, ]
                for r in tr.reviewers.filter(status_id__in=tr_reviewer_statuses_of_interest):
                    r.status_id = 5
                    r.save()

                # send an email to the trip_request owner, if the user has an email address.
                if tr.user:
                    email = emails.StatusUpdateEmail(tr)
                    # # send the email object
                    custom_send_mail(
                        subject=email.subject,
                        html_message=email.message,
                        from_email=email.from_email,
                        recipient_list=email.to_list
                    )

            return HttpResponseRedirect(reverse("travel:trip_detail", kwargs=self.kwargs))
        else:
            return HttpResponseForbidden()


# REPORTS #
###########

class ReportSearchFormView(TravelAccessRequiredMixin, FormView):
    template_name = 'travel/report_search.html'
    form_class = forms.ReportSearchForm

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
            return HttpResponseRedirect(reverse("travel:export_cfts_list", kwargs={
                'fy': fy,
                'region': region,
                'trip': trip,
                'user': user,
                'from_date': from_date,
                'to_date': to_date,
            }))
        elif report == 2:
            email = form.cleaned_data["traveller"]
            return HttpResponseRedirect(reverse("travel:travel_plan", kwargs={
                'fy': fy,
                'email': email,
            }))

        elif report == 3:
            return HttpResponseRedirect(reverse("travel:export_trip_list", kwargs={
                'fy': fy,
                'region': region,
                'adm': adm,
                'from_date': from_date,
                'to_date': to_date,
            }))

        else:
            messages.error(self.request, "Report is not available. Please select another report.")
            return HttpResponseRedirect(reverse("travel:report_search"))


@login_required()
def export_cfts_list(request, fy, region, trip, user, from_date, to_date):
    file_url = reports.generate_cfts_spreadsheet(fiscal_year=fy, region=region, trip=trip, user=user, from_date=from_date, to_date=to_date)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename="CFTS export {}.xlsx"'.format(
                timezone.now().strftime("%Y-%m-%d"))
            return response
    raise Http404


@login_required()
def export_trip_list(request, fy, region, adm, from_date, to_date):
    file_url = reports.generate_trip_list(fiscal_year=fy, region=region, adm=adm, from_date=from_date, to_date=to_date)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = f'inline; filename="export of trips {timezone.now().strftime("%Y-%m-%d")}.xlsx"'
            return response
    raise Http404


@login_required()
def export_request_cfts(request, trip=None, trip_request=None):
    # print(trip)
    file_url = reports.generate_cfts_spreadsheet(trip_request=trip_request, trip=trip)
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
        if my_object.is_group_request:
            template_name = "travel/group_travel_plan.html"
        else:
            template_name = "travel/travel_plan.html"
        return template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_object = models.TripRequest.objects.get(id=self.kwargs['pk'])
        context["parent"] = my_object
        context["trip_category_list"] = models.TripCategory.objects.all()

        cost_categories = models.CostCategory.objects.all()
        my_dict = dict()

        # first, let's create an object list;
        if my_object.is_group_request:
            object_list = my_object.children_requests.filter(exclude_from_travel_plan=False)
        else:
            object_list = models.TripRequest.objects.filter(pk=my_object.id)

        my_dict["totals"] = dict()
        my_dict["totals"]["total"] = 0
        for obj in object_list:
            my_dict[obj] = dict()

            for cat in cost_categories:
                if not my_dict["totals"].get(cat):
                    my_dict["totals"][cat] = 0

                cat_amount = obj.trip_request_costs.filter(cost__cost_category=cat).values("amount_cad").order_by("amount_cad").aggregate(
                    dsum=Sum("amount_cad"))['dsum']
                my_dict[obj][cat] = cat_amount
                my_dict["totals"][cat] += nz(cat_amount, 0)
                my_dict["totals"]["total"] += nz(cat_amount, 0)

        # print(my_dict)
        context['object_list'] = object_list
        context['my_dict'] = my_dict
        # context['key_list'] = cost_categories
        return context


# SETTINGS #
############

# class StatusHardDeleteView(TravelAdminRequiredMixin, CommonHardDeleteView):
#     model = models.Status
#     success_url = reverse_lazy("travel:manage_statuses")

class StatusFormsetView(TravelAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Status"
    queryset = models.Status.objects.all()
    formset_class = forms.StatusFormset
    success_url = reverse_lazy("travel:manage_statuses")
    home_url_name = "travel:index"
    container_class = "container-fluid"
    # delete_url_name = "travel:delete_status"


class HelpTextHardDeleteView(TravelAdminRequiredMixin, CommonHardDeleteView):
    model = models.HelpText
    success_url = reverse_lazy("travel:manage_help_text")


class HelpTextFormsetView(TravelAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage HelpText"
    queryset = models.HelpText.objects.all()
    formset_class = forms.HelpTextFormset
    success_url = reverse_lazy("travel:manage_help_text")
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_help_text"


class CostCategoryHardDeleteView(TravelAdminRequiredMixin, CommonHardDeleteView):
    model = models.CostCategory
    success_url = reverse_lazy("travel:manage_cost_categories")


class CostCategoryFormsetView(TravelAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Cost Category"
    queryset = models.CostCategory.objects.all()
    formset_class = forms.CostCategoryFormset
    success_url = reverse_lazy("travel:manage_cost_categories")
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_cost_category"


class CostHardDeleteView(TravelAdminRequiredMixin, CommonHardDeleteView):
    model = models.Cost
    success_url = reverse_lazy("travel:manage_costs")


class CostFormsetView(TravelAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Cost"
    queryset = models.Cost.objects.all()
    formset_class = forms.CostFormset
    success_url = reverse_lazy("travel:manage_costs")
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_cost"


#
# class NJCRatesHardDeleteView(TravelAdminRequiredMixin, CommonHardDeleteView):
#     model = models.NJCRates
#     success_url = reverse_lazy("travel:manage_njc_rates")


class NJCRatesFormsetView(TravelAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage NJCRates"
    queryset = models.NJCRates.objects.all()
    formset_class = forms.NJCRatesFormset
    success_url = reverse_lazy("travel:manage_njc_rates")
    home_url_name = "travel:index"


class TripCategoryFormsetView(TravelAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Trip Categories"
    queryset = models.TripCategory.objects.all()
    formset_class = forms.TripCategoryFormset
    success_url = reverse_lazy("travel:manage_trip_categories")
    home_url_name = "travel:index"


# class TripCategoryHardDeleteView(TravelAdminRequiredMixin, CommonHardDeleteView):
#     model = models.TripCategory
#     success_url = reverse_lazy("travel:manage_trip_categories")


class TripSubcategoryFormsetView(TravelAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Trip Subcategories"
    queryset = models.TripSubcategory.objects.all()
    formset_class = forms.TripSubcategoryFormset
    success_url = reverse_lazy("travel:manage_trip_subcategories")
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_trip_subcategory"


class TripSubcategoryHardDeleteView(TravelAdminRequiredMixin, CommonHardDeleteView):
    model = models.TripSubcategory
    success_url = reverse_lazy("travel:manage_trip_subcategories")



class ProcessStepFormsetView(TravelAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Process Steps"
    queryset = models.ProcessStep.objects.all()
    formset_class = forms.ProcessStepFormset
    success_url = reverse_lazy("travel:manage_process_steps")
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_process_step"


class ProcessStepHardDeleteView(TravelAdminRequiredMixin, CommonHardDeleteView):
    model = models.ProcessStep
    success_url = reverse_lazy("travel:manage_process_steps")


# Default Reviewer Settings

class DefaultReviewerListView(TravelAdminRequiredMixin, CommonListView):
    model = models.DefaultReviewer
    template_name = 'travel/default_reviewer_list.html'
    h1 = gettext_lazy("Default Reviewers")
    h3 = gettext_lazy("Use this module to set the default reviewers that get added to a trip request.")
    new_object_url_name = "travel:default_reviewer_new"
    home_url_name = "travel:index"
    field_list = [
        {"name": 'user', "class": "", "width": ""},
        {"name": 'sections', "class": "", "width": ""},
        {"name": 'branches', "class": "", "width": ""},
        {"name": 'reviewer_roles', "class": "", "width": ""},
    ]


class DefaultReviewerUpdateView(TravelAdminRequiredMixin, UpdateView):
    model = models.DefaultReviewer
    form_class = forms.DefaultReviewerForm
    success_url = reverse_lazy('travel:default_reviewer_list')
    template_name = 'travel/default_reviewer_form.html'


class DefaultReviewerCreateView(TravelAdminRequiredMixin, CreateView):
    model = models.DefaultReviewer
    form_class = forms.DefaultReviewerForm
    success_url = reverse_lazy('travel:default_reviewer_list')
    template_name = 'travel/default_reviewer_form.html'


class DefaultReviewerDeleteView(TravelAdminRequiredMixin, DeleteView):
    model = models.DefaultReviewer
    success_url = reverse_lazy('travel:default_reviewer_list')
    success_message = 'The default reviewer was successfully deleted!'
    template_name = 'travel/default_reviewer_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# FILES #
#########

class FileCreateView(TravelAccessRequiredMixin, CreateView):
    template_name = "travel/file_form.html"
    model = models.File
    form_class = forms.FileForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse("shared_models:close_me"))

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = True
        trip_request = models.TripRequest.objects.get(pk=self.kwargs['trip_request'])
        context["triprequest"] = trip_request
        return context

    def get_initial(self):
        trip_request = models.TripRequest.objects.get(pk=self.kwargs['trip_request'])
        # status_report = models.StatusReport.objects.get(pk=self.kwargs['status_report']) if self.kwargs.get('status_report') else None

        return {
            'trip_request': trip_request,
        }


class FileUpdateView(TravelAccessRequiredMixin, UpdateView):
    template_name = "travel/file_form.html"
    model = models.File
    form_class = forms.FileForm

    def get_success_url(self, **kwargs):
        return reverse_lazy("travel:file_detail", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = True
        return context


class FileDetailView(FileUpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editable"] = False
        return context


class FileDeleteView(TravelAccessRequiredMixin, DeleteView):
    template_name = "travel/file_confirm_delete.html"
    model = models.File

    def get_success_url(self, **kwargs):
        return reverse_lazy("shared_models:close_me")


# TRAVEL REQUEST COST #
#######################


class TRCostCreateView(LoginRequiredMixin, CreateView):
    model = models.TripRequestCost
    template_name = 'travel/tr_cost_form_popout.html'
    form_class = forms.TripRequestCostForm

    def get_initial(self):
        my_trip_request = models.TripRequest.objects.get(pk=self.kwargs['trip_request'])
        return {
            'trip_request': my_trip_request,
            # 'number_of_days': my_trip_request.trip.number_of_days,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_trip_request = models.TripRequest.objects.get(pk=self.kwargs['trip_request'])
        context['triprequest'] = my_trip_request
        return context

    def form_valid(self, form):
        my_object = form.save()
        if my_object.trip_request.trip:
            utils.manage_trip_warning(my_object.trip_request.trip)
        return HttpResponseRedirect(reverse('shared_models:close_me'))


class TRCostUpdateView(LoginRequiredMixin, UpdateView):
    model = models.TripRequestCost
    template_name = 'travel/tr_cost_form_popout.html'
    form_class = forms.TripRequestCostForm

    def form_valid(self, form):
        my_object = form.save()
        if my_object.trip_request.parent_request:
            my_trip = my_object.trip_request.parent_request.trip
        else:
            my_trip = my_object.trip_request.trip
        utils.manage_trip_warning(my_trip)

        return HttpResponseRedirect(reverse('shared_models:close_me_no_refresh'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def tr_cost_delete(request, pk):
    object = models.TripRequestCost.objects.get(pk=pk)
    if can_modify_request(request.user, object.trip_request.id):
        object.delete()
        messages.success(request, _("The cost has been successfully deleted."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('/accounts/denied/')


def tr_cost_clear(request, trip_request):
    my_trip_request = models.TripRequest.objects.get(pk=trip_request)
    if can_modify_request(request.user, my_trip_request.id):
        utils.clear_empty_trip_request_costs(my_trip_request)
        messages.success(request, _("All empty costs have been cleared."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('/accounts/denied/')


def tr_cost_populate(request, trip_request):
    my_trip_request = models.TripRequest.objects.get(pk=trip_request)
    if can_modify_request(request.user, my_trip_request.id):
        utils.populate_trip_request_costs(request, my_trip_request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('/accounts/denied/')
