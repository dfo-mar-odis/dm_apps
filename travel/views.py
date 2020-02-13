import json
import os
from copy import deepcopy
from Levenshtein import distance

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Sum, Q
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView, ListView, TemplateView, FormView
###
from django_filters.views import FilterView
from easy_pdf.views import PDFTemplateView
from lib.functions.custom_functions import fiscal_year
from lib.templatetags.custom_filters import nz
from . import models
from . import forms
from . import reports
from . import emails
from . import filters
from . import utils

from shared_models import models as shared_models


# Create your views here.
class CloserTemplateView(TemplateView):
    template_name = 'travel/close_me.html'


def in_travel_admin_group(user):
    if user.id:
        return user.groups.filter(name='travel_admin').count() != 0


def in_adm_admin_group(user):
    if user.id:
        return user.groups.filter(name='travel_adm_admin').count() != 0


def is_approver(user, trip_request):
    if user == trip_request.current_reviewer.user:
        return True


def can_modify_request(user, trip_request_id):
    """
    returns True if user has permissions to delete or modify a request

    The answer of this question will depend on whether the trip is submitted.
    owners cannot edit a submitted trip
    """
    if user.id:
        my_trip_request = models.TripRequest.objects.get(pk=trip_request_id)

        # check to see if a travel_admin
        if in_travel_admin_group(user):
            return True

        # check to see if they are the active reviewer
        if my_trip_request.current_reviewer.user == user:
            return True

        # if the project is unsubmitted, the project lead is also able to edit the project... obviously
        # check to see if they are either the owner OR a traveller
        if not my_trip_request.submitted and (my_trip_request.user == user or user in my_trip_request.travellers):
            return True


class TravelAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):


    def test_func(self):
        return in_travel_admin_group(self.request.user)

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


class IndexTemplateView(TravelAccessRequiredMixin, TemplateView):
    template_name = 'travel/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["number_waiting"] = self.request.user.reviewers.filter(status_id=1).count()  # number of requests where review is pending
        context["admin_number_waiting"] = models.Reviewer.objects.filter(
            status_id=1,
            role_id__in=[5, 6],
        ).filter(
            ~Q(trip_request__status_id=16)
        ).count()  # number of requests where admin review is pending
        context["is_reviewer"] = True if self.request.user.reviewers.all().count() > 0 else False
        context["is_admin"] = in_travel_admin_group(self.request.user)
        context["unverified_trips"] = models.Conference.objects.filter(is_verified=False).count()
        return context


request_field_list = [
    'fiscal_year',
    'status_string|{}'.format(_("Request status")),
    'user',
    'section',
    'first_name',
    'last_name',
    'address',
    'phone',
    'email',
    'is_public_servant',
    'company_name',
    'region',
    'departure_location',
    'destination',
    'start_date',
    'end_date',
    'purpose',
    'reason',
    'trip',

    'role',
    'role_of_participant',
    'objective_of_event',
    'benefit_to_dfo',
    'multiple_conferences_rationale',
    'multiple_attendee_rationale',
    'late_justification',
    'bta_attendees',
    'notes',
    # 'cost_table|{}'.format(_("DFO costs")),
    'total_request_cost|{}'.format(_("Total cost (DFO)")),
    'non_dfo_costs',
    'non_dfo_org',
]

request_group_field_list = [
    'fiscal_year',
    'status_string|{}'.format(_("Request status")),
    'user',
    'section',
    'destination',
    'purpose',
    'reason',
    'trip',

    'objective_of_event',
    'benefit_to_dfo',
    'multiple_attendee_rationale',
    'funding_source',
    'bta_attendees',
    'late_justification',
    'notes',
    'total_request_cost|{}'.format(_("Total cost (DFO)")),
    'non_dfo_costs',
    'non_dfo_org',
]

request_child_field_list = [
    'first_name',
    'last_name',
    'is_public_servant',
    'is_research_scientist',
    'region',
    'start_date',
    'end_date',
    'departure_location',
    'role',
    'role_of_participant',
    'total_cost',
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
    'non_res_total_cost|{}'.format("Non-research scientist total cost (from all connected requests, excluding BTA travel)"),

    'total_cost|{}'.format("Total cost (from all connected requests, excluding BTA travel)"),
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
class TripRequestListView(TravelAccessRequiredMixin, FilterView):
    queryset = models.TripRequest.objects.filter(parent_request__isnull=True)
    filterset_class = filters.TripRequestFilter
    template_name = 'travel/trip_request_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.TripRequest.objects.first()
        context["field_list"] = [
            'fiscal_year',
            'is_group_request',
            'status',
            'section',
            'first_name',
            'last_name',
            'trip.tname',
            'destination',
            'start_date',
            'end_date',
            'total_request_cost|{}'.format(_("Total request cost (DFO)")),

        ]
        return context


class TripRequestReviewListView(TravelAccessRequiredMixin, ListView):
    model = models.TripRequest
    template_name = 'travel/trip_request_review_list.html'

    def get_queryset(self):
        if self.kwargs.get("which_ones") == "awaiting":
            qs = models.TripRequest.objects.filter(
                pk__in=[reviewer.trip_request.id for reviewer in self.request.user.reviewers.filter(status_id=1)])
        else:
            qs = models.TripRequest.objects.filter(pk__in=[reviewer.trip_request.id for reviewer in self.request.user.reviewers.all()])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.TripRequest.objects.first()
        context["awaiting"] = True if self.kwargs.get("which_ones") else False
        context["field_list"] = [
            'status_string|{}'.format(_("Request status")),
            'is_group_request',
            'first_name',
            'last_name',
            'trip',
            'destination',
            'start_date',
            'end_date',
            'total_request_cost|{}'.format(_("Total cost (DFO)")),
        ]
        return context


class TripRequestAdminApprovalListView(TravelAdminRequiredMixin, ListView):
    model = models.TripRequest
    template_name = 'travel/trip_request_review_list.html'

    def get_queryset(self):
        # return a list only of those awaiting ADM or RDG approval
        qs = models.TripRequest.objects.filter(
            parent_request__isnull=True,
        ).filter(status_id__in=[14, 15]).order_by("-submitted")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.TripRequest.objects.first()
        context["admin"] = True
        context["field_list"] = [
            'is_group_request',
            'first_name',
            'last_name',
            'trip',
            'destination',
            'start_date',
            'end_date',
            'total_request_cost|{}'.format(_("Total cost (DFO)")),
        ]
        return context


class TripRequestDetailView(TravelAccessRequiredMixin, DetailView):
    model = models.TripRequest
    template_name = 'travel/trip_request_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_object = self.get_object()
        context["field_list"] = request_field_list if not my_object.is_group_request else request_group_field_list
        my_request_child_field_list = deepcopy(request_child_field_list)
        context["child_field_list"] = my_request_child_field_list
        context["reviewer_field_list"] = reviewer_field_list
        context["conf_field_list"] = conf_field_list
        context["cost_field_list"] = cost_field_list
        context['help_text_dict'] = get_help_text_dict()
        context["fy"] = fiscal_year()
        context["is_admin"] = "travel_admin" in [group.name for group in self.request.user.groups.all()]
        context["is_owner"] = my_object.user == self.request.user

        if context["is_admin"]:
            is_current_reviewer = True
        else:
            is_current_reviewer = my_object.current_reviewer.user == self.request.user if my_object.current_reviewer else None

        context["is_current_reviewer"] = is_current_reviewer
        if my_object.submitted and not is_current_reviewer:
            context["report_mode"] = True

        return context


class TripRequestUpdateView(TravelAccessRequiredMixin, UpdateView):
    model = models.TripRequest

    def get_template_names(self):
        return 'travel/trip_request_form_popout.html' if self.kwargs.get("pop") else 'travel/trip_request_form.html'

    def get_form_class(self):
        return forms.ChildTripRequestForm if self.kwargs.get("pop") else forms.TripRequestForm

    def form_valid(self, form):
        my_object = form.save()

        if my_object.parent_request:
            my_trip = my_object.parent_request.trip
        else:
            my_trip = my_object.trip
        utils.manage_trip_warning(my_trip)

        if not my_object.parent_request:
            if form.cleaned_data.get("stay_on_page"):
                return HttpResponseRedirect(reverse_lazy("travel:request_edit", kwargs={"pk": my_object.id}))
            else:
                return HttpResponseRedirect(reverse_lazy("travel:request_detail", kwargs={"pk": my_object.id}))
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


class ReviewerApproveUpdateView(AdminOrApproverRequiredMixin, UpdateView):
    model = models.Reviewer
    form_class = forms.ReviewerApprovalForm
    template_name = 'travel/reviewer_approval_form.html'

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
        context["conf_field_list"] = conf_field_list
        context["cost_field_list"] = cost_field_list
        context['help_text_dict'] = get_help_text_dict()

        context["triprequest"] = my_object.trip_request
        context["report_mode"] = True
        if my_object.role_id in [5, 6, ]:
            context["admin"] = True

        return context

    def form_valid(self, form):
        my_reviewer = form.save(commit=False)

        approved = form.cleaned_data.get("approved")
        stay_on_page = form.cleaned_data.get("stay_on_page")
        changes_requested = form.cleaned_data.get("changes_requested")
        # print("stay on page", stay_on_page)
        # first scenario: changes were requested for the request
        # in this case, the reviewer status does not change but the request status will
        if not stay_on_page:
            if changes_requested:
                my_reviewer.trip_request.status_id = 16
                my_reviewer.trip_request.submitted = None
                my_reviewer.trip_request.save()
                # send an email to the request owner
                my_email = emails.ChangesRequestedEmail(my_reviewer.trip_request)
                # send the email object
                if settings.USE_EMAIL:
                    send_mail(message='', subject=my_email.subject, html_message=my_email.message, from_email=my_email.from_email,
                              recipient_list=my_email.to_list, fail_silently=False, )
                else:
                    print(my_email)
                messages.success(self.request, _("Success! An email has been sent to the trip request owner."))

            # if it was approved, then we change the reviewer status to 'approved'
            elif approved:
                my_reviewer.status_id = 2
                my_reviewer.status_date = timezone.now()
            # if it was approved, then we change the reviewer status to 'approved'
            else:
                my_reviewer.status_id = 3
                my_reviewer.status_date = timezone.now()

        # now we save the reviewer for real
        my_reviewer.save()

        # update any statuses if necessary
        utils.approval_seeker(my_reviewer.trip_request)

        if stay_on_page:
            return HttpResponseRedirect(reverse("travel:review_approve", kwargs={"pk": my_reviewer.id}))
        else:
            return HttpResponseRedirect(reverse("travel:index"))


class SkipReviewerUpdateView(TravelAdminRequiredMixin, UpdateView):
    model = models.Reviewer
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


class TripRequestSubmitUpdateView(TravelAccessRequiredMixin, FormView):
    model = models.TripRequest
    form_class = forms.TripRequestApprovalForm
    template_name = 'travel/trip_request_submission_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_object = models.TripRequest.objects.get(pk=self.kwargs.get("pk"))
        context["object"] = my_object
        context["triprequest"] = my_object
        context["field_list"] = request_field_list if not my_object.is_group_request else request_group_field_list
        context["child_field_list"] = request_child_field_list
        context["reviewer_field_list"] = reviewer_field_list
        context["conf_field_list"] = conf_field_list
        context["cost_field_list"] = cost_field_list
        context['help_text_dict'] = get_help_text_dict()
        context["report_mode"] = True

        return context

    def form_valid(self, form):
        my_trip_request = models.TripRequest.objects.get(pk=self.kwargs.get("pk"))
        # figure out the current state of the request
        is_submitted = True if my_trip_request.submitted else False

        # if submitted, then unsumbit but only if admin or owner
        if is_submitted:
            #  UNSUBMIT REQUEST
            if in_travel_admin_group(self.request.user) or my_trip_request.user == self.request.user:
                my_trip_request.submitted = None
                # reset all the reviewer statuses
                utils.end_review_process(my_trip_request)
            else:
                messages.error(self.request, "sorry, only admins or owners can unsubmit requests")
        else:
            #  SUBMIT REQUEST
            my_trip_request.submitted = timezone.now()
            # if the request is being resubmitted, this is a special case...
            if my_trip_request.status_id == 16:
                my_trip_request.status_id = 8
                my_trip_request.save()
            else:
                # set all the reviewer statuses to 'queued'
                utils.start_review_process(my_trip_request)
                # go and get approvals!!

        # No matter what business what done, we will call this function to sort through reviewer and request statuses
        utils.approval_seeker(my_trip_request)
        my_trip_request.save()

        # clean up any unused cost categories
        utils.clear_empty_trip_request_costs(my_trip_request)
        for child in my_trip_request.children_requests.all():
            utils.clear_empty_trip_request_costs(child)

        return HttpResponseRedirect(reverse("travel:request_detail", kwargs={"pk": my_trip_request.id}))


class TripRequestCancelUpdateView(TravelAdminRequiredMixin, UpdateView):
    model = models.TripRequest
    form_class = forms.TripRequestAdminNotesForm
    template_name = 'travel/trip_request_cancel_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_object = models.TripRequest.objects.get(pk=self.kwargs.get("pk"))
        context["object"] = my_object
        context["triprequest"] = my_object
        context["field_list"] = request_field_list if not my_object.is_group_request else request_group_field_list
        context["child_field_list"] = request_child_field_list
        context["reviewer_field_list"] = reviewer_field_list
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
            #  UN-CANCEL THE REQUEST
            my_trip_request.status_id = 11
        else:
            #  CANCEL THE REQUEST
            my_trip_request.status_id = 22

        my_trip_request.save()
        # send an email to the trip_request owner
        my_email = emails.StatusUpdateEmail(my_trip_request)
        # # send the email object
        if settings.USE_EMAIL:
            send_mail(message='', subject=my_email.subject, html_message=my_email.message, from_email=my_email.from_email,
                      recipient_list=my_email.to_list, fail_silently=False, )
        else:
            print(my_email)

        return HttpResponseRedirect(reverse("travel:request_detail", kwargs={"pk": my_trip_request.id}))


class TripRequestAdminNotesUpdateView(TravelAdminRequiredMixin, UpdateView):
    model = models.TripRequest
    form_class = forms.TripRequestAdminNotesForm
    template_name = 'travel/trip_request_admin_notes_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse("shared_models:close_me"))


class TripRequestCreateView(TravelAccessRequiredMixin, CreateView):
    model = models.TripRequest

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
            my_dict = {"parent_request": my_object, "stay_on_page": True}
        else:
            # if this is a new parent trip
            my_dict = {"user": self.request.user}
        return my_dict

    def form_valid(self, form):
        my_object = form.save()

        # if it is a group request, add the main user as a traveller
        if my_object.is_group_request:
            my_child_object = models.TripRequest.objects.create(
                user=self.request.user,
                first_name=self.request.user.first_name,
                last_name=self.request.user.last_name,
                email=self.request.user.email,
                parent_request=my_object,
            )
            # pre-populate the costs on the 'child' record
            utils.populate_trip_request_costs(self.request, my_child_object)
        else:
            # if the request is not a group request, we pre-populate the costs on the 'parent' record
            utils.populate_trip_request_costs(self.request, my_object)

        # add reviewers
        utils.get_reviewers(my_object)

        # if this is not a child record
        if not my_object.parent_request:
            if form.cleaned_data.get("stay_on_page"):
                return HttpResponseRedirect(reverse_lazy("travel:request_edit", kwargs={"pk": my_object.id}))
            else:
                return HttpResponseRedirect(reverse_lazy("travel:request_detail", kwargs={"pk": my_object.id}))
        # if this is a child record
        else:
            if form.cleaned_data.get("stay_on_page"):
                messages.success(self.request, _(
                    "{} has been added as a traveller to this request. Please add any costs associated with this traveller.".format(
                        my_object.user)))
                return HttpResponseRedirect(reverse("travel:request_edit", kwargs={"pk": my_object.id, "pop": "1"}))
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


class TripRequestDeleteView(TravelAccessRequiredMixin, DeleteView):
    model = models.TripRequest

    def get_template_names(self):
        if self.kwargs.get('pop'):
            template_name = 'travel/trip_request_confirm_delete_popout.html'
        else:
            template_name = 'travel/trip_request_confirm_delete.html'
        return template_name

    def get_success_url(self):
        if self.kwargs.get('pop'):
            success_url = reverse('shared_models:close_me')
        else:
            success_url = reverse_lazy('travel:request_list')
        return success_url

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
        utils.get_reviewers(new_obj)
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

        # # need to clone any children of the old object...
        # for child_request in old_obj.children_requests.all():
        #     child_request.pk = None
        #     child_request.parent_request = new_obj
        #     child_request.save()

        if form.cleaned_data.get("stay_on_page"):
            return HttpResponseRedirect(reverse_lazy("travel:request_edit", kwargs={"pk": new_obj.id}))
        else:
            return HttpResponseRedirect(reverse_lazy("travel:request_detail", kwargs={"pk": new_obj.id}))


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

        return HttpResponseRedirect(reverse_lazy("travel:request_edit", kwargs={"pk": new_obj.id, "pop": "1"}))

    def get_initial(self):
        init = super().get_initial()
        init["user"] = None
        return init

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cloned"] = True
        return context


@login_required(login_url='/accounts/login/')
# @user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def reset_reviewers(request, pk):
    my_obj = models.TripRequest.objects.get(pk=pk)
    # first remove any existing reviewers
    my_obj.reviewers.all().delete()
    # next, re-add the defaults...
    utils.get_reviewers(my_obj)
    return HttpResponseRedirect(reverse("travel:request_detail", kwargs={"pk": my_obj.id}))


# REVIEWER #
############
@login_required(login_url='/accounts/login/')
# @user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def delete_reviewer(request, pk):
    my_obj = models.Reviewer.objects.get(pk=pk)
    if my_obj.trip_request.submitted:
        messages.error(request, "Cannot modify reviewers while project is submitted")
        return HttpResponseRedirect(reverse("travel:request_detail", kwargs={"pk": my_obj.trip_request.id}))
    else:
        my_obj.delete()
        my_obj.trip_request.save()
        return HttpResponseRedirect(reverse("travel:manage_reviewers", kwargs={"trip_request": my_obj.trip_request.id}))


@login_required(login_url='/accounts/login/')
# @user_passes_test(is_superuser, login_url='/accounts/denied/')
def manage_reviewers(request, trip_request):
    my_trip_request = models.TripRequest.objects.get(pk=trip_request)
    if my_trip_request.submitted:
        messages.error(request, "Cannot modify reviewers while project is submitted")
        return HttpResponseRedirect(reverse("travel:request_detail", kwargs={"pk": my_trip_request.id}))
    else:
        qs = models.Reviewer.objects.filter(trip_request=my_trip_request)
        if request.method == 'POST':
            formset = forms.ReviewerFormSet(request.POST)

            if formset.is_valid():
                formset.save()

                my_trip_request.save()
                # do something with the formset.cleaned_data
                messages.success(request, _("The reviewer list has been successfully updated"))
                return HttpResponseRedirect(reverse("travel:manage_reviewers", kwargs={"trip_request": my_trip_request.id}))
        else:
            formset = forms.ReviewerFormSet(
                queryset=qs,
                initial=[{"trip_request": my_trip_request}],
            )

        context = {}
        context['triprequest'] = my_trip_request
        context['formset'] = formset
        context["my_object"] = models.Reviewer.objects.first()
        context["field_list"] = [
            'trip_request',
            'order',
            'user',
            'role',
        ]
        return render(request, 'travel/reviewer_formset.html', context)


# TRIP #
########

class TripListView(TravelAccessRequiredMixin, FilterView):
    model = models.Conference
    filterset_class = filters.TripFilter
    template_name = 'travel/trip_list.html'

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        if kwargs["data"] is None:
            kwargs["data"] = {"fiscal_year": fiscal_year(next=False, sap_style=True)}
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.Conference.objects.first()
        context["field_list"] = [
            'fiscal_year',
            'tname|{}'.format("Name"),
            'location|{}'.format(_("location")),
            'dates|{}'.format(_("dates")),
            'number_of_days|{}'.format(_("length (days)")),
            'is_adm_approval_required|{}'.format(_("ADM approval required?")),
        ]
        context["is_admin"] = in_travel_admin_group(self.request.user)
        return context


class TripDetailView(TravelAccessRequiredMixin, DetailView):
    model = models.Conference
    template_name = 'travel/trip_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["conf_field_list"] = conf_field_list
        context["trip"] = self.get_object()
        return context


class TripUpdateView(TravelAdminRequiredMixin, UpdateView):
    template_name = 'travel/trip_form.html'
    model = models.Conference
    form_class = forms.TripForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()

        return context


class TripCreateView(TravelAccessRequiredMixin, CreateView):
    model = models.Conference
    form_class = forms.TripForm

    def get_template_names(self):
        if self.kwargs.get("pop"):
            return 'travel/trip_form_popout.html'
        else:
            return 'travel/trip_form.html'

    def get_success_url(self):
        if self.kwargs.get("pop"):
            return reverse("shared_models:close_me")
        else:
            return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()

        return context

    def form_valid(self, form):
        my_object = form.save()
        if self.kwargs.get("pop"):
            # create a new email object
            email = emails.NewTripEmail(my_object)
            # send the email object
            if settings.USE_EMAIL:
                send_mail(message='', subject=email.subject, html_message=email.message, from_email=email.from_email,
                          recipient_list=email.to_list, fail_silently=False, )
            else:
                print(email)
            messages.success(self.request,
                             _("The trip has been added to the database!"))
        return super().form_valid(form)


class TripDeleteView(TravelAdminRequiredMixin, DeleteView):
    template_name = 'travel/trip_confirm_delete.html'
    model = models.Conference
    success_url = reverse_lazy('travel:trip_list')
    success_message = 'The event was deleted successfully!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class AdminTripVerificationListView(TravelAdminRequiredMixin, ListView):
    queryset = models.Conference.objects.filter(is_verified=False).order_by("is_adm_approval_required")
    template_name = 'travel/trip_verification_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.Conference.objects.first()
        context["field_list"] = [
            'fiscal_year',
            'tname|{}'.format("Name"),
            'location|{}'.format(_("location")),
            'dates|{}'.format(_("dates")),
            'number_of_days|{}'.format(_("length (days)")),
            'is_adm_approval_required|{}'.format(_("ADM approval required?")),
        ]
        return context


class TripVerifyUpdateView(TravelAdminRequiredMixin, FormView):
    template_name = 'travel/trip_verification_form.html'
    model = models.Conference
    form_class = forms.TripRequestApprovalForm

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
                "message": _("Sorry, only ADMO administrators can verify projects that require ADM approval.")}))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_trip = models.Conference.objects.get(pk=self.kwargs.get("pk"))
        context["object"] = my_trip
        context["conf_field_list"] = conf_field_list

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
        my_trip.is_verified = True
        my_trip.verified_by = self.request.user
        my_trip.save()
        return HttpResponseRedirect(reverse("travel:admin_trip_verification_list"))


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
        fy = form.cleaned_data["fiscal_year"]
        user = form.cleaned_data["user"]

        if report == 1:
            return HttpResponseRedirect(reverse("travel:export_cfts_list", kwargs={
                'fy': fy,
                'user': user,
            }))
        elif report == 2:
            email = form.cleaned_data["traveller"]
            return HttpResponseRedirect(reverse("travel:travel_plan", kwargs={
                'fy': fy,
                'email': email,
            }))

        else:
            messages.error(self.request, "Report is not available. Please select another report.")
            return HttpResponseRedirect(reverse("travel:report_search"))


def export_cfts_list(request, fy):
    file_url = reports.generate_cfts_spreadsheet(fiscal_year=fy)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename="custom master list export {}.xlsx"'.format(
                timezone.now().strftime("%Y-%m-%d"))
            return response
    raise Http404


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
        context["purpose_list"] = models.Purpose.objects.all()

        cost_categories = models.CostCategory.objects.all()
        my_dict = dict()

        # first, let's create an object list; if this is
        if my_object.is_group_request:
            object_list = my_object.children_requests.filter(
                Q(region=my_object.section.division.branch.region) | Q(region__isnull=True) | Q(is_public_servant=False))
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

@login_required(login_url='/accounts/login/')
@user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def delete_status(request, pk):
    my_obj = models.Status.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("travel:manage_statuses"))


@login_required(login_url='/accounts/login/')
@user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def manage_statuses(request):
    qs = models.Status.objects.all()
    if request.method == 'POST':
        formset = forms.StatusFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "Items have been successfully updated")
            return HttpResponseRedirect(reverse("travel:manage_statuses"))
    else:
        formset = forms.StatusFormSet(
            queryset=qs)
    context = {}
    context["my_object"] = qs.first()
    context["field_list"] = [
        'used_for',
        'name',
        'nom',
        'order',
        'color',
    ]
    context['title'] = "Manage Statuses"
    context['formset'] = formset
    return render(request, 'travel/manage_settings_small.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def delete_help_text(request, pk):
    my_obj = models.HelpText.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("travel:manage_help_text"))


@login_required(login_url='/accounts/login/')
@user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def manage_help_text(request):
    qs = models.HelpText.objects.all()
    if request.method == 'POST':
        formset = forms.HelpTextFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "Items have been successfully updated")
            return HttpResponseRedirect(reverse("travel:manage_help_text"))
    else:
        formset = forms.HelpTextFormSet(
            queryset=qs)
    context = {}
    context["my_object"] = qs.first()
    context["field_list"] = [
        'field_name',
        'eng_text',
        'fra_text',
    ]
    context['title'] = "Manage Help Text"
    context['formset'] = formset
    return render(request, 'travel/manage_settings_small.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def delete_cost_category(request, pk):
    my_obj = models.CostCategory.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("travel:manage_cost_categories"))


@login_required(login_url='/accounts/login/')
@user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def manage_cost_categories(request):
    qs = models.CostCategory.objects.all()
    if request.method == 'POST':
        formset = forms.CostCategoryFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "Items have been successfully updated")
            return HttpResponseRedirect(reverse("travel:manage_cost_categories"))
    else:
        formset = forms.CostCategoryFormSet(
            queryset=qs)
    context = {}
    context["my_object"] = qs.first()
    context["field_list"] = [
        'name',
        'nom',
        'order',
    ]
    context['title'] = "Manage Cost Categories"
    context['formset'] = formset
    return render(request, 'travel/manage_settings_small.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def delete_cost(request, pk):
    my_obj = models.Cost.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("travel:manage_costs"))


@login_required(login_url='/accounts/login/')
@user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def manage_costs(request):
    qs = models.Cost.objects.all()
    if request.method == 'POST':
        formset = forms.CostFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "Items have been successfully updated")
            return HttpResponseRedirect(reverse("travel:manage_costs"))
    else:
        formset = forms.CostFormSet(
            queryset=qs)
    context = {}
    context["my_object"] = qs.first()
    context["field_list"] = [
        'name',
        'nom',
        'cost_category',
    ]
    context['title'] = "Manage Costs"
    context['formset'] = formset
    return render(request, 'travel/manage_settings_small.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def delete_njc_rate(request, pk):
    my_obj = models.NJCRates.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("travel:manage_njc_rates"))


@login_required(login_url='/accounts/login/')
@user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def manage_njc_rates(request):
    qs = models.NJCRates.objects.all()
    if request.method == 'POST':
        formset = forms.NJCRatesFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "Items have been successfully updated")
            return HttpResponseRedirect(reverse("travel:manage_njc_rates"))
    else:
        formset = forms.NJCRatesFormSet(
            queryset=qs)
    context = {}
    context["my_object"] = qs.first()
    context["field_list"] = [
        'name',
        'amount',
    ]
    context['title'] = "Manage NJC Rates"
    context['formset'] = formset
    return render(request, 'travel/manage_settings_small.html', context)


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

        return HttpResponseRedirect(reverse('shared_models:close_me'))

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
