import datetime
import os

import textile
from django.conf import settings
from django.contrib.auth.models import User as AuthUser
from django.db import models
from django.db.models import Q, Sum
from django.dispatch import receiver
from django.template.defaultfilters import pluralize, date
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _, gettext

from lib.templatetags.verbose_names import get_verbose_label
from shared_models import models as shared_models
from lib.templatetags.custom_filters import nz, currency
from lib.functions.custom_functions import fiscal_year, listrify
from shared_models.models import Lookup, SimpleLookup
from . import utils

YES_NO_CHOICES = (
    (True, _("Yes")),
    (False, _("No")),
)


class DefaultReviewer(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.DO_NOTHING, related_name="travel_default_reviewers",
                                verbose_name=_("DM Apps user"))
    sections = models.ManyToManyField(shared_models.Section, verbose_name=_("reviewer on which DFO section(s)"), blank=True,
                                      related_name="travel_default_reviewers")
    branches = models.ManyToManyField(shared_models.Branch, verbose_name=_("reviewer on which DFO branch(es)"), blank=True,
                                      related_name="travel_default_reviewers")
    reviewer_roles = models.ManyToManyField("ReviewerRole", verbose_name=_("Do they have any special roles?"), blank=True,
                                            related_name="travel_default_reviewers", limit_choices_to={"id__in": [3, 4, 5]})
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.user)

    class Meta:
        ordering = ["user", ]


class NJCRates(SimpleLookup):
    amount = models.FloatField()
    last_modified = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.last_modified = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['id', ]


class ProcessStep(Lookup):
    stage_choices = (
        (1, _("Travel request process outline")),
        (2, _("Review process outline")),
    )
    stage = models.IntegerField(blank=True, null=True, choices=stage_choices)


class CostCategory(SimpleLookup):
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['order', 'id']


class Cost(SimpleLookup):
    cost_category = models.ForeignKey(CostCategory, on_delete=models.DO_NOTHING, related_name="costs", verbose_name=_("category"))

    class Meta:
        ordering = ['cost_category', 'name']


class Role(SimpleLookup):
    pass


class TripCategory(SimpleLookup):
    days_when_eligible_for_review = models.IntegerField(verbose_name=_(
        "Number days before earliest date that is eligible for review"))  # overflowing this since we DO NOT want it to be unique=True


class TripSubcategory(Lookup):
    name = models.CharField(max_length=255, verbose_name=_("name (en)"))  # overflowing this since we DO NOT want it to be unique=True
    trip_category = models.ForeignKey(TripCategory, on_delete=models.DO_NOTHING, related_name="subcategories")

    def __str__(self):
        return f"{self.trip_category} - {self.tname}"

    class Meta:
        ordering = ["trip_category", _("name")]


class Reason(SimpleLookup):
    pass


# THE HOPE IS TO DELETE THIS MODEL
class Purpose(Lookup):
    pass


class Status(SimpleLookup):
    # choices for used_for
    TR_REVIEWERS = 1
    TRIP_REVIEWERS = 3
    TRIP_REQUESTS = 2
    TRIPS = 4
    USED_FOR_CHOICES = (
        (TR_REVIEWERS, "Request Reviewer status"),
        (TRIP_REQUESTS, "Trip Request status"),
        (TRIP_REVIEWERS, "Trip Reviewer status"),
        (TRIPS, "Trip status"),
    )
    name = models.CharField(max_length=255)  # overflowing this since we DO NOT want it to be unique=True
    used_for = models.IntegerField(choices=USED_FOR_CHOICES)
    order = models.IntegerField(blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        ordering = ['used_for', 'order', 'name', ]

    @property
    def status_colored_span(self):
        return mark_safe(f'<span style="background-color:{self.color}">{self.tname}</span>')


class Conference(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("trip title (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("trip title (French)"))
    trip_subcategory = models.ForeignKey(TripSubcategory, on_delete=models.DO_NOTHING, verbose_name=_("trip purpose"),
                                         related_name="trips", null=True)
    is_adm_approval_required = models.BooleanField(default=False, choices=YES_NO_CHOICES, verbose_name=_(
        "does attendance to this require ADM approval?"))
    location = models.CharField(max_length=1000, blank=False, null=True, verbose_name=_("location (city, province, country)"))
    lead = models.ForeignKey(shared_models.Region, on_delete=models.DO_NOTHING, verbose_name=_("Which region is the lead on this trip?"),
                             related_name="meeting_leads", blank=False, null=True)
    has_event_template = models.NullBooleanField(default=False, verbose_name=_(
        "Is there an event template being completed for this conference or meeting?"))
    number = models.IntegerField(blank=True, null=True, verbose_name=_("event number"))
    start_date = models.DateTimeField(verbose_name=_("start date of event"))
    end_date = models.DateTimeField(verbose_name=_("end date of event"))
    meeting_url = models.URLField(verbose_name=_("meeting URL"), blank=True, null=True)
    abstract_deadline = models.DateTimeField(verbose_name=_("abstract submission deadline"), blank=True, null=True)
    registration_deadline = models.DateTimeField(verbose_name=_("registration deadline"), blank=True, null=True)
    notes = models.TextField(blank=True, null=True, verbose_name=_("general notes"))
    fiscal_year = models.ForeignKey(shared_models.FiscalYear, on_delete=models.DO_NOTHING, verbose_name=_("fiscal year"),
                                    blank=True, null=True, related_name="trips")
    is_verified = models.BooleanField(default=False, verbose_name=_("verified?"))
    verified_by = models.ForeignKey(AuthUser, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="trips_verified_by",
                                    verbose_name=_("verified by"))
    cost_warning_sent = models.DateTimeField(blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name="trips",
                               limit_choices_to={"used_for": 4}, verbose_name=_("trip status"), default=30)
    admin_notes = models.TextField(blank=True, null=True, verbose_name=_("Administrative notes"))
    review_start_date = models.DateTimeField(verbose_name=_("start date of the ADM review"), blank=True, null=True)
    adm_review_deadline = models.DateTimeField(verbose_name=_("ADM Office review deadline"), blank=True, null=True)
    date_eligible_for_adm_review = models.DateTimeField(verbose_name=_("Date when eligible for ADM Office review"), blank=True, null=True)
    last_modified = models.DateTimeField(verbose_name=_("last modified"), auto_now=True, editable=False)
    last_modified_by = models.ForeignKey(AuthUser, on_delete=models.DO_NOTHING, related_name="trips_last_modified_by",
                                         verbose_name=_("last_modified_by"), blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            my_str = "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            my_str = "{}".format(self.name)
        return "{}, {} ({} {} {})".format(my_str, self.location, self.start_date.strftime("%d-%b-%Y"), _("to"),
                                          self.end_date.strftime("%d-%b-%Y"))

    @property
    def closest_date(self):
        """determine the nearest date: abstract, registration, start_date"""
        abs_date = nz(self.abstract_deadline, self.start_date)
        reg_date = nz(self.registration_deadline, self.start_date)
        start_date = self.start_date
        return min([abs_date, reg_date, start_date])

    @property
    def days_until_eligible_for_adm_review(self):
        if self.is_adm_approval_required:
            # when was the deadline?
            deadline = self.date_eligible_for_adm_review
            # how many days until the deadline?
            return (deadline - timezone.now()).days

    @property
    def days_until_adm_review_deadline(self):
        if self.is_adm_approval_required:
            # when was the deadline?
            deadline = self.adm_review_deadline
            # how many days until the deadline?
            return (deadline - timezone.now()).days

    @property
    def admin_notes_html(self):
        return textile.textile(self.admin_notes)

    @property
    def html_block(self):
        my_str = "<b>English name:</b> {}<br>" \
                 "<b>French name:</b> {}<br>" \
                 "<b>Location:</b> {}<br>" \
                 "<b>Start date (yyyy-mm-dd):</b> {}<br>" \
                 "<b>End date (yyyy-mm-dd):</b> {}<br>" \
                 "<b>Meeting URL:</b> {}<br>" \
                 "<b>ADM approval required:</b> {}<br>" \
                 "<b>Verified:</b> {}<br>" \
                 "<b>Verified By:</b> {}<br>" \
                 "<br><a href='{}' target='_blank' class='btn btn-primary btn-sm'>View Details</a>".format(
            self.name, self.nom, self.location,
            self.start_date.strftime("%Y-%m-%d"),
            self.end_date.strftime("%Y-%m-%d"),
            "<a href='(click here)' target='_blank'>{}</a>".format(self.meeting_url) if self.meeting_url else "n/a",
            "<span class='green-font'>YES</span>" if self.is_adm_approval_required else "<span class='red-font'>NO</span>",
            "<span class='green-font'>YES</span>" if self.is_verified else "<span class='red-font'>NO</span>",
            self.verified_by if self.verified_by else "----",
            reverse("travel:trip_detail", kwargs={"pk": self.id, "type": "verify"}),
        )

        return mark_safe(my_str)

    class Meta:
        ordering = ['start_date', ]
        verbose_name = "trip"
        verbose_name_plural = "trips"

    # def get_absolute_url(self):
    #     return reverse('travel:trip_detail', kwargs={'pk': self.id, "type":""})

    @property
    def bta_traveller_list(self):
        # create a list of all TMS users going
        legit_traveller_list = self.traveller_list
        bta_travellers = []
        # exclude reqeusts that are denied (id=10), cancelled (id=22), draft (id=8)
        for trip_request in self.trip_requests.filter(~Q(status_id__in=[10, 22, 8])):
            # lets look at the list of BTA travels and add them all
            for bta_user in trip_request.bta_attendees.all():
                # if this user for some reason turns up to be a real traveller on this trip
                # (i.e. the assertion that they are a BTA traveller is wrong, they should not be added)
                if bta_user not in legit_traveller_list:
                    bta_travellers.append(bta_user)
        # return a set of all users
        return list(set(bta_travellers))

    @property
    def traveller_list(self):
        trip_requests = self.get_connected_active_requests()  # a list of individual and child requests connected to this trip
        my_list = [tr.user for tr in trip_requests if tr.user]
        # now those without names...
        blurb = _("not a DM Apps user")
        my_list.extend([f"{tr.requester_name} ({blurb})" for tr in trip_requests if not tr.user])
        return set(my_list)

    @property
    def number_of_days(self):
        return (self.end_date - self.start_date).days

    @property
    def dates(self):
        my_str = "{}".format(
            self.start_date.strftime("%Y-%m-%d"),
        )
        if self.end_date:
            my_str += " &rarr; {}".format(
                self.end_date.strftime("%Y-%m-%d"),
            )
        return my_str

    @property
    def total_traveller_list(self):
        travellers = self.bta_traveller_list
        travellers.extend(self.traveller_list)
        return list(set(travellers))

    @property
    def travellers(self):
        return listrify(self.total_traveller_list)

    @property
    def total_cost(self):
        # from travel.models import Event
        # must factor in group and non-group...

        # start simple... non-group
        # exclude reqeusts that are denied (id=10), cancelled (id=22), draft (id=8)
        my_list = [trip_request.total_dfo_funding for trip_request in
                   self.trip_requests.filter(~Q(status_id__in=[10, 22, 8])).filter(is_group_request=False)]
        # group travellers
        my_list.extend(
            [trip_request.total_dfo_funding for trip_request in
             TripRequest.objects.filter(parent_request__trip=self).filter(~Q(status_id__in=[10, 22, 8]))])

        return sum(my_list)

    @property
    def non_res_total_cost(self):
        # from travel.models import Event
        # must factor in group and non-group...

        # start simple... non-group
        my_list = [trip_request.total_dfo_funding for trip_request in
                   self.trip_requests.filter(~Q(status_id__in=[10, 22, 8])).filter(is_group_request=False, is_research_scientist=False)]
        # group travellers
        my_list.extend(
            [trip_request.total_dfo_funding for trip_request in
             TripRequest.objects.filter(parent_request__trip=self).filter(~Q(status_id__in=[10, 22, 8])).filter(
                 is_research_scientist=False)])

        return sum(my_list)

    @property
    def tname(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            my_str = "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            my_str = "{}".format(self.name)
        return my_str

    def save(self, *args, **kwargs):
        self.fiscal_year = shared_models.FiscalYear.objects.get(pk=fiscal_year(next=False, date=self.start_date, sap_style=True))
        # ensure the process order makes sense
        count = 1
        for reviewer in self.reviewers.all():  # use the default sorting
            reviewer.order = count
            reviewer.save()
            count += 1

        if self.is_adm_approval_required and self.trip_subcategory:
            # trips must be reviewed by ADMO before two weeks to the closest date
            self.adm_review_deadline = self.closest_date - datetime.timedelta(days=21)  # 14 business days -- > 21 calendar days?

            # This is a business rule: if trip category == conference, the admo can start review 90 days in advance of closest date
            # else they can start the review closer to the date: eight business weeks (60 days)
            # this is stored in the table
            self.date_eligible_for_adm_review = self.closest_date - datetime.timedelta(
                days=self.trip_subcategory.trip_category.days_when_eligible_for_review)

        super().save(*args, **kwargs)

    def get_connected_requests(self):
        """
        gets a qs of all connected trip request, excluding any parent requests (for group travel only)
        """
        # from travel.models import Event
        # must factor in group and non-group...

        my_id_list = [trip_request.id for trip_request in self.trip_requests.all().filter(is_group_request=False)]
        # self.trip_requests.filter(~Q(status_id__in=[10, 22])).filter(is_group_request=False)]
        # group requests
        my_id_list.extend(
            [trip_request.id for trip_request in TripRequest.objects.filter(parent_request__trip=self).all()])
        return TripRequest.objects.filter(id__in=my_id_list)

    def get_connected_active_requests(self):
        """
        gets a qs of all connected trip request, excluding any parent requests (for group travel only)
        and excluding trips that have been denied=10, cancelled=22 or that are in draft=8
        """
        # from travel.models import Event
        # must factor in group and non-group...

        my_id_list = [trip_request.id for trip_request in
                      self.trip_requests.filter(~Q(status_id__in=[10, 22, 8])).filter(is_group_request=False)]
        # group requests
        my_id_list.extend(
            [trip_request.id for trip_request in
             TripRequest.objects.filter(parent_request__trip=self).filter(~Q(parent_request__status_id__in=[10, 22, 8])).filter(
                 ~Q(status_id=10))])
        return TripRequest.objects.filter(id__in=my_id_list)

    @property
    def get_summary_dict(self):
        """
        This method is used to return a dictionary of users attending a trip, as well as the number of
        trips or international meetings they have attended.

        UPDATE: this will also be a way to get to a trip request from a traveller
        """
        my_dict = {}

        for traveller in self.total_traveller_list:
            my_dict[traveller] = {}
            total_list = []

            # if this is not a real User instance, there is nothing to do.
            try:
                # there are two things we have to do to get this list...
                # 1) get all non group travel
                qs = traveller.user_trip_requests.filter(trip__is_adm_approval_required=True).filter(is_group_request=False)
                total_list.extend([trip.id for trip in qs])

                # 2) get all group travel - the trick part is that we have to grab the parent trip
                qs = traveller.user_trip_requests.filter(parent_request__trip__is_adm_approval_required=True)
                total_list.extend([trip_request.parent_request.id for trip_request in qs])

                my_dict[traveller]["total_list"] = TripRequest.objects.filter(id__in=total_list).order_by("-start_date")

            except AttributeError:
                # This is the easy part
                my_dict[traveller]["total_list"] = "---"

            # also, let's get the trip request for the traveller. if group request, we will want the child record
            for tr in self.get_connected_requests():
                if type(traveller) is AuthUser:
                    if traveller in tr.travellers:
                        my_dict[traveller]["trip_request"] = tr
                else:
                    for name in tr.traveller_names:
                        if name in traveller:
                            my_dict[traveller]["trip_request"] = tr
                            break
        return my_dict

    @property
    def get_cost_comparison_dict(self):
        """
        This method is used to return a dictionary of trip requests and will compare cost across all of them.
        """
        my_dict = dict()
        trip_requests = self.get_connected_active_requests()
        tr_costs = TripRequestCost.objects.filter(trip_request_id__in=[tr.id for tr in trip_requests], amount_cad__gt=0)
        costs = Cost.objects.filter(id__in=[tr_cost.cost_id for tr_cost in tr_costs])
        my_dict["trip_requests"] = dict()
        my_dict["costs"] = dict()
        for cost in costs:
            my_dict["costs"][cost] = 0
            my_dict["costs"]["total"] = 0

        for tr in trip_requests:
            my_dict["trip_requests"][tr] = dict()
            my_dict["trip_requests"][tr]["total"] = 0
            for cost in costs:
                if tr.trip_request_costs.filter(cost=cost, amount_cad__gt=0).count() > 0:
                    my_dict["trip_requests"][tr][cost] = tr.trip_request_costs.get(cost=cost).amount_cad
                    my_dict["trip_requests"][tr]["total"] += my_dict["trip_requests"][tr][cost]
                    my_dict["costs"][cost] += my_dict["trip_requests"][tr][cost]
                    my_dict["costs"]["total"] += my_dict["trip_requests"][tr][cost]

        return my_dict

    @property
    def current_reviewer(self):
        """Send back the first reviewer whose status is 'pending' """
        return self.reviewers.filter(status_id=25).first()

    @property
    def status_string(self):
        my_status = self.status
        #  if the status is not 'draft' or 'approved' AND there is a current_reviewer
        status_str = "{}".format(my_status)
        if my_status.id == 31 and self.current_reviewer:
            status_str += " {} {}".format(_("by"), self.current_reviewer.user)
        return status_str

    @property
    def is_adm_approved(self):
        """method to determine if all linked trip requests have been reviewed by the ADM"""
        return


class TripRequest(models.Model):
    fiscal_year = models.ForeignKey(shared_models.FiscalYear, on_delete=models.DO_NOTHING, verbose_name=_("fiscal year"),
                                    default=fiscal_year(sap_style=True), blank=True, null=True, related_name="trip_requests")
    # traveller info
    user = models.ForeignKey(AuthUser, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="user_trip_requests",
                             verbose_name=_("DM Apps user"))
    is_public_servant = models.BooleanField(default=True, choices=YES_NO_CHOICES, verbose_name=_("Is the traveller a public servant?"))
    region = models.ForeignKey(shared_models.Region, on_delete=models.DO_NOTHING, verbose_name=_("Traveller belongs to which DFO region"),
                               related_name="trip_requests",
                               null=True, blank=True)
    section = models.ForeignKey(shared_models.Section, on_delete=models.DO_NOTHING, null=True,
                                verbose_name=_("under which DFO section is this request being made"), related_name="trip_requests")
    is_research_scientist = models.BooleanField(default=False, choices=YES_NO_CHOICES,
                                                verbose_name=_("Is the traveller a research scientist (RES)?"))
    first_name = models.CharField(max_length=100, verbose_name=_("first name"), blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name=_("last name"), blank=True, null=True)
    address = models.CharField(max_length=1000, verbose_name=_("address"),
                               blank=True, null=True)
    phone = models.CharField(max_length=1000, verbose_name=_("phone"), blank=True, null=True)
    email = models.EmailField(verbose_name=_("email"), blank=True, null=True)
    company_name = models.CharField(max_length=255, verbose_name=_("company name"), blank=True, null=True)

    # Trip Details
    is_group_request = models.BooleanField(default=False,
                                           verbose_name=_("Is this a group request (i.e., a request for multiple individuals)?"))
    # purpose = models.ForeignKey(Purpose, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("purpose of travel"))
    trip = models.ForeignKey(Conference, on_delete=models.DO_NOTHING, null=True, verbose_name=_("trip"), related_name="trip_requests")

    departure_location = models.CharField(max_length=1000, verbose_name=_("departure location (city, province, country)"), blank=True,
                                          null=True)
    destination = models.CharField(max_length=1000, verbose_name=_("destination location (city, province, country)"), blank=True,
                                   null=True)
    start_date = models.DateTimeField(verbose_name=_("start date of travel"), null=True, blank=True)
    end_date = models.DateTimeField(verbose_name=_("end date of travel"), null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("role of traveller"))

    # purpose
    role_of_participant = models.TextField(blank=True, null=True, verbose_name=_("role description"))
    objective_of_event = models.TextField(blank=True, null=True, verbose_name=_("objective of the trip"))
    benefit_to_dfo = models.TextField(blank=True, null=True, verbose_name=_("benefit to DFO"))
    multiple_conferences_rationale = models.TextField(blank=True, null=True,
                                                      verbose_name=_("rationale for individual attending multiple conferences"))
    bta_attendees = models.ManyToManyField(AuthUser, blank=True, verbose_name=_("Other attendees covered under BTA"))
    # multiple_attendee_rationale = models.TextField(blank=True, null=True, verbose_name=_(
    #     "rationale for multiple travelers"))
    late_justification = models.TextField(blank=True, null=True, verbose_name=_("Justification for late submissions"))
    funding_source = models.TextField(blank=True, null=True, verbose_name=_("funding source"))
    notes = models.TextField(blank=True, null=True, verbose_name=_("optional notes"))
    # total_cost = models.FloatField(blank=True, null=True, verbose_name=_("total cost (DFO)"))
    non_dfo_costs = models.FloatField(blank=True, null=True, verbose_name=_("Amount of non-DFO funding (CAD)"))
    non_dfo_org = models.CharField(max_length=1000, verbose_name=_("full name(s) of organization providing non-DFO funding"), blank=True,
                                   null=True)

    submitted = models.DateTimeField(verbose_name=_("date submitted"), blank=True, null=True)
    original_submission_date = models.DateTimeField(verbose_name=_("original submission date"), blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name="trip_requests",
                               limit_choices_to={"used_for": 2}, verbose_name=_("trip request status"), default=8)
    parent_request = models.ForeignKey("TripRequest", on_delete=models.CASCADE, related_name="children_requests", blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True, verbose_name=_("Administrative notes"))
    exclude_from_travel_plan = models.BooleanField(default=False, verbose_name=_("Exclude this traveller from the travel plan?"))

    created_by = models.ForeignKey(AuthUser, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="trip_requests_created_by",
                                   verbose_name=_("created by"))

    @property
    def dates(self):
        my_str = date(self.start_date)
        if self.end_date:
            my_str += f" &rarr; {date(self.end_date)}"
        return mark_safe(my_str)

    @property
    def to_from(self):
        my_str = f"{self.departure_location} &rarr; {self.smart_destination}"
        return mark_safe(my_str)

    @property
    def long_role(self):
        mystr = str(self.role)
        if self.role_of_participant:
            mystr += f" &mdash; {self.role_of_participant}"
        return mark_safe(mystr)

    @property
    def admin_notes_html(self):
        return textile.textile(self.admin_notes)

    @property
    def request_title(self):
        group_status = " - {}".format(gettext("Group Request")) if self.is_group_request else ""

        my_str = "{} {}{}".format(
            self.first_name,
            self.last_name,
            group_status,
        )
        if self.trip:
            my_str += " - {}".format(self.trip.tname)
        if self.destination:
            my_str += " - {}".format(self.destination)
        return my_str

    def __str__(self):
        return "{}".format(self.request_title)

    class Meta:
        ordering = ["-start_date", "last_name"]
        unique_together = [("user", "parent_request"), ("user", "trip"), ]

    # def get_absolute_url(self):
    #     return reverse('travel:request_detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        # if the start and end dates are null, but there is a trip, use those.. to populate
        if self.trip and not self.start_date:
            # print("adding start date from trip")
            self.start_date = self.trip.start_date
        if self.trip and not self.end_date:
            # print("adding end date from trip")
            self.end_date = self.trip.end_date

        if self.start_date:
            self.fiscal_year_id = fiscal_year(date=self.start_date, sap_style=True)

        # If this is a group request, the parent record should not have any costs
        if self.is_group_request:
            self.trip_request_costs.all().delete()

        # If this is a child request, it should not have any assigned reviewers -> unless it is an ADM reviewer
        if self.parent_request:
            self.reviewers.filter(~Q(role_id=5)).delete()

        # ensure the process order makes sense
        count = 1
        for reviewer in self.reviewers.all():  # use the default sorting
            reviewer.order = count
            reviewer.save()
            count += 1

        return super().save(*args, **kwargs)

    @property
    def reviewer_order_message(self):
        last_reviewer = None
        for reviewer in self.reviewers.all():
            # basically, each subsequent reviewer should have a role that is further down in order than the previous
            if last_reviewer:
                if last_reviewer.role.order > reviewer.role.order:
                    return "WARNING: The roles of the reviewers are out of order!"
            last_reviewer = reviewer

    @property
    def cost_breakdown(self):
        """used for CFTS and travel plan"""
        my_str = ""
        for tr_cost in self.trip_request_costs.all():
            if tr_cost.rate_cad:
                my_str += "{}: ${:,.2f} ({} x {:,.2f}); ".format(
                    tr_cost.cost,
                    nz(tr_cost.rate_cad, 0),
                    nz(tr_cost.number_of_days, 0),
                    nz(tr_cost.amount_cad, 0),
                )
            else:
                my_str += "{}: ${:,.2f}; ".format(tr_cost.cost, tr_cost.amount_cad)

        if nz(self.non_dfo_costs, 0) > 0:
            my_str += str(_('NOTE: This trip request contains non-DFO funding sources from {}. '
                            'Total DFO funding: ${:,.2f} | Total non-DFO funding: ${:,.2f}'.format(
                self.non_dfo_org,
                self.total_dfo_funding,
                self.total_non_dfo_funding,
            )))

        return my_str

    @property
    def cost_breakdown_html(self):
        """used for display on group traveller detail page"""
        my_str = ""
        for tr_cost in self.trip_request_costs.all():
            if tr_cost.amount_cad:
                if tr_cost.rate_cad:
                    my_str += "<b>{}</b>: ${:,.2f}  ({} x {:,.2f})<br>".format(
                        tr_cost.cost,
                        nz(tr_cost.amount_cad, 0),
                        nz(tr_cost.number_of_days, 0),
                        nz(tr_cost.rate_cad, 0),
                    )
                else:
                    my_str += "<b>{}</b>: ${:,.2f}<br> ".format(tr_cost.cost, tr_cost.amount_cad)
        return my_str

    @property
    def cost_table(self):
        cost_list = [
            "air",
            "rail",
            "rental_motor_vehicle",
            "personal_motor_vehicle",
            "taxi",
            "other_transport",
            "accommodations",
            "breakfasts",
            "lunches",
            "suppers",
            "incidentals",
            "registration",
            "other",
        ]

        # style #1 - costs as headers
        # my_str = "<table class='table table-sm table-bordered plainjane'><tr>"
        # for cost in cost_list:
        #     my_str += "<th class='plainjane'>{}</th>".format(get_verbose_label(self, cost))
        # my_str += "</tr><tr>"
        # for cost in cost_list:
        #     my_str += "<td class='plainjane'>{}</td>".format(nz(currency(getattr(self, cost)),"---"))
        # my_str += "</tr></table>"

        # style # 2 - 2 columns
        my_str = "<table class='plainjane' style='width: 40%'>"
        my_str += "<tr class='plainjane'><th class='plainjane'>{}</th><th class='plainjane'>{}</td></tr>".format(
            _("Cost category"), _("Amount (CAD)"))
        for cost in cost_list:
            if cost in ("breakfasts", "lunches", "suppers", "incidentals"):
                my_str += "<tr><td class='plainjane'>{}</td><td class='plainjane'>{} ({} &times; {})</td></tr>".format(
                    get_verbose_label(self, cost),
                    nz(currency(getattr(self, cost)), "---"),
                    nz(getattr(self, "no_" + cost), "---"),
                    nz(currency(getattr(self, cost + "_rate")), "---"),
                )
            else:
                my_str += "<tr><td class='plainjane'>{}</td><td class='plainjane'>{}</td></tr>".format(
                    get_verbose_label(self, cost), nz(currency(getattr(self, cost)), "---"))

        my_str += "<tr><th class='plainjane'>{}</th><th class='plainjane'>{}</td></tr>".format(
            _("TOTAL"), nz(currency(self.total_request_cost), "---"))
        my_str += "</table>"
        return mark_safe(my_str)

    @property
    def total_cost(self):
        """ this is the total cost for the request. Does not include any children"""
        object_list = self.trip_request_costs.all()
        return nz(object_list.values("amount_cad").order_by("amount_cad").aggregate(dsum=Sum("amount_cad"))['dsum'], 0)

    @property
    def total_request_cost(self):
        """ this is the total cost for the request; including any children"""
        if self.is_group_request:
            object_list = self.children_requests.all()
            summed_costs = sum([item.total_cost for item in object_list])
        else:
            summed_costs = self.total_cost
        return summed_costs

    @property
    def total_non_dfo_funding(self):
        """
        this is the total non dfo funding. for individual requests, it is simply the non_dfo_costs field.
        for group request, it is this summed over all children requests
        """
        if self.is_group_request:
            object_list = self.children_requests.all()
            return sum([nz(item.non_dfo_costs, 0) for item in object_list])
        else:
            return nz(self.non_dfo_costs, 0)

    @property
    def total_dfo_funding(self):
        """
        this will return the portion of funding to be paid by DFO.
        The amount will be whatever is leftover when you subtract non-dfo funding from total costs
        """
        return nz(self.total_request_cost, 0) - nz(self.total_non_dfo_funding, 0)

    @property
    def total_non_dfo_funding_sources(self):
        """
        this is a comprehensive list of the non-dfo funding sources
        """
        if self.is_group_request:
            object_list = self.children_requests.all()
            return listrify(set([item.non_dfo_org for item in object_list]))
        else:
            return nz(self.non_dfo_org, "----")

    @property
    def travellers(self):
        if self.is_group_request:
            return [tr.user for tr in self.children_requests.all()]
        else:
            return [self.user]

    @property
    def traveller_names(self):
        if self.is_group_request:
            return [tr.requester_name for tr in self.children_requests.all()]
        else:
            return [self.requester_name]

    @property
    def purpose_long(self):
        my_str = ""
        if self.role_of_participant:
            my_str += "<em>Role of Participant:</em> {}".format(self.role_of_participant)
        if self.objective_of_event:
            my_str += "<br><em>Objective of Event:</em> {}".format(self.objective_of_event)
        if self.benefit_to_dfo:
            my_str += "<br><em>Benefit to DFO:</em> {}".format(self.benefit_to_dfo)
        if self.multiple_conferences_rationale:
            my_str += "<br><em>Rationale for attending multiple conferences:</em> {}".format(self.multiple_conferences_rationale)
        if self.funding_source:
            my_str += "<br><em>Funding source:</em> {}".format(self.funding_source)

        return my_str

    @property
    def purpose_long_text(self):
        """
        For CFTS report
        """
        my_str = "{}: {}".format("ROLE OF PARTICIPANT", nz(self.role_of_participant, "No description provided"))

        my_str += "\n\n{}: {}".format("OBJECTIVE OF EVENT", nz(self.objective_of_event, "n/a"))

        my_str += "\n\n{}: {}".format("BENEFIT TO DFO", nz(self.benefit_to_dfo, "n/a"))

        my_str += "\n\n{}: {}".format(
            "Rationale for attending multiple conferences".upper(), nz(self.multiple_conferences_rationale, "n/a"))

        return my_str

    @property
    def current_reviewer(self):
        """Send back the first reviewer whose status is 'pending' """
        return self.reviewers.filter(status_id=1).first()

    @property
    def status_string(self):
        if self.parent_request:
            my_status = self.parent_request.status
            #  if the status is not 'draft' or 'approved' AND there is a current_reviewer
            status_str = "{}".format(my_status)
            if my_status.id not in [11, 8, ] and self.parent_request.current_reviewer:
                status_str += " {} {}".format(_("by"), self.parent_request.current_reviewer.user)
        else:
            my_status = self.status
            #  if the status is not 'draft' or 'approved' AND there is a current_reviewer
            status_str = "{}".format(my_status)
            if my_status.id not in [11, 8, ] and self.current_reviewer:
                status_str += " {} {}".format(_("by"), self.current_reviewer.user)
        return status_str

    @property
    def adm(self):
        return self.reviewers.filter(role_id=5).first()

    @property
    def rdg(self):
        return self.reviewers.filter(role_id=6).first()

    @property
    def recommenders(self):
        return self.reviewers.filter(role_id=2)

    @property
    def processing_time(self):
        # if draft
        if self.status.id == 8 or not self.original_submission_date:
            my_var = "---"
        # if approved, denied
        elif self.status.id in [10, 11]:
            my_var = self.reviewers.filter(status_date__isnull=False).last().status_date - self.original_submission_date
            my_var = "{} {}{}".format(my_var.days, _('day'), pluralize(my_var.days))
        else:
            my_var = timezone.now() - self.original_submission_date
            my_var = "{} {}{}".format(my_var.days, _('day'), pluralize(my_var.days))
        return my_var

    @property
    def requester_name(self):
        if self.user:
            return str(self.user)
        else:
            return f'{self.first_name} {self.last_name}'

    @property
    def requester_info(self):
        mystr = ""
        if not self.is_public_servant:
            mystr += _("Company: ") + nz(self.company_name, "<span class='red-font'>missing company name</span>") + "<br>"
        mystr += _("Address: ") + nz(self.address, "<span class='red-font'>missing address</span>") + "<br>"
        mystr += _("Phone: ") + nz(self.phone, "<span class='red-font'>missing phone</span>") + "<br>"
        mystr += _("Email: ") + nz(f'<a href="mailto:{self.email}?subject=travel request {self.id}">{self.email}</a>',
                                   "<span class='red-font'>missing email address</span>") + "<br>"
        return mark_safe(mystr)

    @property
    def smart_start_date(self):
        return self.trip.start_date if self.parent_request else self.end_date

    @property
    def smart_status(self):
        return self.parent_request.status if self.parent_request else self.status

    @property
    def smart_trip(self):
        return self.parent_request.trip if self.parent_request else self.trip

    @property
    def smart_objective_of_event(self):
        return self.parent_request.objective_of_event if self.parent_request else self.objective_of_event

    @property
    def smart_benefit_to_dfo(self):
        return self.parent_request.benefit_to_dfo if self.parent_request else self.benefit_to_dfo

    @property
    def smart_funding_source(self):
        return self.parent_request.funding_source if self.parent_request else self.funding_source

    @property
    def smart_section(self):
        return self.parent_request.section if self.parent_request else self.section

    @property
    def smart_reviewers(self):
        return self.parent_request.reviewers if self.parent_request else self.reviewers

    @property
    def smart_destination(self):
        return self.parent_request.destination if self.parent_request else self.destination

    @property
    def smart_recommendation_notes(self):
        my_str = ""
        reviewers = self.smart_reviewers
        for r in reviewers.filter(role_id=2):
            if r.status_id == 2 and r.comments:
                my_str += f'<u>{r.user}</u>: {r.comments}<br>'
        return mark_safe(my_str)


class TripRequestCost(models.Model):
    trip_request = models.ForeignKey(TripRequest, on_delete=models.CASCADE, related_name="trip_request_costs",
                                     verbose_name=_("trip request"))
    cost = models.ForeignKey(Cost, on_delete=models.DO_NOTHING, related_name="trip_request_costs", verbose_name=_("cost"))
    rate_cad = models.FloatField(verbose_name=_("daily rate (CAD/day)"), blank=True, null=True)
    number_of_days = models.FloatField(verbose_name=_("number of days"), blank=True, null=True)
    amount_cad = models.FloatField(default=0, verbose_name=_("amount (CAD)"), blank=True, null=True)

    def __str__(self):
        return f'{self.cost} - {self.amount_cad}'

    class Meta:
        unique_together = (("trip_request", "cost"),)

    def save(self, *args, **kwargs):
        # if a user is providing a rate and number of days, we use this to calc the total amount.
        if (self.rate_cad and self.rate_cad != 0) and (self.number_of_days and self.number_of_days != 0):
            self.amount_cad = self.rate_cad * self.number_of_days

        super().save(*args, **kwargs)


class ReviewerRole(SimpleLookup):
    order = models.IntegerField()

    class Meta:
        ordering = ["order", "id"]


class Reviewer(models.Model):
    trip_request = models.ForeignKey(TripRequest, on_delete=models.CASCADE, related_name="reviewers")
    order = models.IntegerField(null=True, verbose_name=_("process order"))
    user = models.ForeignKey(AuthUser, on_delete=models.DO_NOTHING, related_name="reviewers", verbose_name=_("DM Apps user"))
    role = models.ForeignKey(ReviewerRole, on_delete=models.DO_NOTHING, verbose_name=_("role"))
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, limit_choices_to={"used_for": 1},
                               verbose_name=_("review status"), default=4)
    status_date = models.DateTimeField(verbose_name=_("status date"), blank=True, null=True)
    comments = models.TextField(null=True, verbose_name=_("Comments"))

    def __str__(self):
        return gettext("Reviewer") + f' - {self.user}'

    class Meta:
        unique_together = ['trip_request', 'user', 'role', ]
        ordering = ['trip_request', 'order', ]

    @property
    def comments_html(self):
        if self.comments:
            return textile.textile(self.comments)
        else:
            return "---"

    def save(self, *args, **kwargs):
        # If the trip request is currently under review but changes have been requested, add this reviewer directly in the queue

        if self.trip_request.status_id != 8 and self.status_id == 4:
            self.status_id = 20
        return super().save(*args, **kwargs)

    @property
    def status_string(self):

        if self.status.id in [1, 4, 5]:
            status = "{}".format(
                self.status
            )
        else:
            status = "{} {} {}".format(
                self.status,
                _("on"),
                self.status_date.strftime("%Y-%m-%d"),
            )

        my_str = "<span style='background-color:{}'>{} ({})</span>".format(
            self.status.color,
            self.user,
            status,
        )
        return mark_safe(my_str)


class TripReviewer(models.Model):
    trip = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name="reviewers")
    order = models.IntegerField(null=True, verbose_name=_("process order"))
    user = models.ForeignKey(AuthUser, on_delete=models.DO_NOTHING, related_name="trip_reviewers", verbose_name=_("DM Apps user"))
    role = models.ForeignKey(ReviewerRole, on_delete=models.DO_NOTHING, verbose_name=_("role"))
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, limit_choices_to={"used_for": 3},
                               verbose_name=_("review status"), default=23)
    status_date = models.DateTimeField(verbose_name=_("status date"), blank=True, null=True)
    comments = models.TextField(null=True, verbose_name=_("Comments"))

    class Meta:
        unique_together = ['trip', 'user', 'role', ]
        ordering = ['trip', 'order', ]

    @property
    def comments_html(self):
        if self.comments:
            return textile.textile(self.comments)
        else:
            return "---"

    @property
    def status_string(self):

        if self.status.id in [1, 4, 5]:
            status = "{}".format(
                self.status
            )
        else:
            status = "{} {} {}".format(
                self.status,
                _("on"),
                self.status_date.strftime("%Y-%m-%d"),
            )

        my_str = "<span style='background-color:{}'>{} ({})</span>".format(
            self.status.color,
            self.user,
            status,
        )
        return mark_safe(my_str)

    # def save(self, *args, **kwargs):
    #     # If the trip is currently under review add this reviewer directly in the queue
    #
    #     if self.trip.status_id == 31:
    #         self.status_id = 24
    #     return super().save(*args, **kwargs)


def file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'travel/trip_{0}/{1}'.format(instance.trip_request.id, filename)


class File(models.Model):
    trip_request = models.ForeignKey(TripRequest, related_name="files", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name=_("caption"))
    file = models.FileField(upload_to=file_directory_path, null=True, verbose_name=_("file attachment"))
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['trip_request', 'date_created']

    def __str__(self):
        return self.name


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=File)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = File.objects.get(pk=instance.pk).file
    except File.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class HelpText(models.Model):
    field_name = models.CharField(max_length=255)
    eng_text = models.TextField(verbose_name=_("English text"))
    fra_text = models.TextField(blank=True, null=True, verbose_name=_("French text"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("eng_text"))):
            return "{}".format(getattr(self, str(_("eng_text"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.eng_text)

    class Meta:
        ordering = ['field_name', ]
