import os

import textile
from django.conf import settings
from django.contrib.auth.models import User as AuthUser
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q, Sum
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _, gettext

from lib.templatetags.verbose_names import get_verbose_label
from shared_models import models as shared_models
from lib.templatetags.custom_filters import nz, currency
from lib.functions.custom_functions import fiscal_year, listrify
from . import utils

YES_NO_CHOICES = (
    (True, _("Yes")),
    (False, _("No")),
)


class NJCRates(models.Model):
    name = models.CharField(max_length=255)
    amount = models.FloatField()
    last_modified = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.last_modified = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['id', ]


class CostCategory(models.Model):
    name = models.CharField(max_length=255)
    nom = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    @property
    def tname(self):
        return str(self)


class Cost(models.Model):
    name = models.CharField(max_length=255)
    nom = models.CharField(max_length=255, blank=True, null=True)
    cost_category = models.ForeignKey(CostCategory, on_delete=models.DO_NOTHING, related_name="costs", verbose_name=_("category"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['cost_category', 'name']


class Role(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name (eng)"), blank=True, null=True)
    nom = models.CharField(max_length=100, verbose_name=_("name (fre)"), blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ["name", ]


class Reason(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name (eng)"), blank=True, null=True)
    nom = models.CharField(max_length=100, verbose_name=_("name (fre)"), blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ["name", ]


class Purpose(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name (eng)"), blank=True, null=True)
    nom = models.CharField(max_length=100, verbose_name=_("name (fre)"), blank=True, null=True)
    description_eng = models.CharField(max_length=1000, verbose_name=_("description (eng)"), blank=True, null=True)
    description_fre = models.CharField(max_length=1000, verbose_name=_("description (fre)"), blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ["name", ]


class Status(models.Model):
    # choices for used_for
    APPROVAL = 1
    TRIPS = 2
    USED_FOR_CHOICES = (
        (APPROVAL, "Reviewer status"),
        (TRIPS, "Trip status"),
    )

    used_for = models.IntegerField(choices=USED_FOR_CHOICES)
    name = models.CharField(max_length=255)
    nom = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):

            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['used_for', 'order', 'name', ]


class Conference(models.Model):
    name = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255, blank=True, null=True)
    is_adm_approval_required = models.BooleanField(default=False, choices=YES_NO_CHOICES, verbose_name=_(
        "does attendance to this require ADM approval?"))
    location = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("location (city, province, country)"))
    lead = models.ForeignKey(shared_models.Region, on_delete=models.DO_NOTHING, verbose_name=_("Which region is taking the lead?"),
                             related_name="meeting_leads", blank=True, null=True)
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
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(AuthUser, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="trips_verified_by")
    cost_warning_sent = models.DateTimeField(blank=True, null=True)


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
    def html_block(self):
        my_str = "<b>English name:</b> {}<br>" \
                 "<b>French name:</b> {}<br>" \
                 "<b>Location:</b> {}<br>" \
                 "<b>Start date (yyyy-mm-dd):</b> {}<br>" \
                 "<b>End date (yyyy-mm-dd):</b> {}<br>" \
                 "<b>Meeting URL:</b> {}<br>" \
                 "<b>Verified:</b> {}<br>" \
                 "<b>Verified By:</b> {}<br>" \
                 "<br><a href='{}' target='_blank' class='btn btn-primary btn-sm'>Go!</a>".format(
            self.name, self.nom, self.location,
            self.start_date.strftime("%Y-%m-%d"),
            self.end_date.strftime("%Y-%m-%d"),
            "<a href='(click here)' target='_blank'>{}</a>".format(self.meeting_url) if self.meeting_url else "n/a",
            "<span class='green-font'>YES</span>" if self.is_verified else "<span class='red-font'>NO</span>",
            self.verified_by if self.verified_by else "----",
            reverse("travel:trip_detail", kwargs={"pk": self.id}),
        )

        return mark_safe(my_str)

    class Meta:
        ordering = ['start_date', ]

    def get_absolute_url(self):
        return reverse('travel:trip_detail', kwargs={'pk': self.id})

    @property
    def bta_traveller_list(self):
        # create a list of all TMS users going
        legit_traveller_list = self.traveller_list
        travellers = []
        for trip_request in self.trip_requests.filter(~Q(status_id__in=[10, 22])):
            # lets look at the list of BTA travels and add them all
            for bta_user in trip_request.bta_attendees.all():
                # if this user for some reason turns up to be a real traveller on this trip
                # (i.e. the assertion that they are a BTA traveller is wrong, they should not be added)
                if bta_user not in legit_traveller_list:
                    travellers.append(bta_user)

        # return a set of all users
        return list(set(travellers))

    @property
    def traveller_list(self):
        # from travel.models import Event
        # must factor in group and non-group...

        # start simple... non-group
        my_list = [trip_request.user for trip_request in
                   self.trip_requests.filter(~Q(status_id__in=[10, 22])).filter(is_group_request=False) if
                   trip_request.user]
        # now those without names...
        my_list.extend(
            ["{} {} ({})".format(trip_request.first_name, trip_request.last_name, _("no DM Apps user connected")) for trip_request in
             self.trip_requests.filter(~Q(status_id__in=[10, 22])).filter(is_group_request=False) if not trip_request.user])

        # group travellers
        my_list.extend(
            [trip_request.user for trip_request in TripRequest.objects.filter(parent_request__trip=self).filter(~Q(status_id__in=[10, 22]))
             if
             trip_request.user])
        my_list.extend(
            ["{} {} ({})".format(trip_request.first_name, trip_request.last_name, _("no DM Apps user connected")) for trip_request in
             TripRequest.objects.filter(parent_request__trip=self).filter(~Q(status_id__in=[10, 22])) if not trip_request.user])

        return set(my_list)

    @property
    def number_of_days(self):
        if self.end_date:
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
        my_list = [trip_request.total_request_cost for trip_request in
                   self.trip_requests.filter(~Q(status_id__in=[10, 22])).filter(is_group_request=False)]
        # group travellers
        my_list.extend(
            [trip_request.total_request_cost for trip_request in
             TripRequest.objects.filter(parent_request__trip=self).filter(~Q(status_id__in=[10, 22]))])

        return sum(my_list)

    @property
    def non_res_total_cost(self):
        # from travel.models import Event
        # must factor in group and non-group...

        # start simple... non-group
        my_list = [trip_request.total_request_cost for trip_request in
                   self.trip_requests.filter(~Q(status_id__in=[10, 22])).filter(is_group_request=False, is_research_scientist=False)]
        # group travellers
        my_list.extend(
            [trip_request.total_request_cost for trip_request in
             TripRequest.objects.filter(parent_request__trip=self).filter(~Q(status_id__in=[10, 22])).filter(is_research_scientist=False)])

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
        super().save(*args, **kwargs)

    def get_connected_requests(self):
        """
        gets a qs of all connected trip request, excluding any parent requests (for group travel only)
        """
        # from travel.models import Event
        # must factor in group and non-group...

        my_id_list = [trip_request.id for trip_request in
                      self.trip_requests.filter(~Q(status_id__in=[10, 22])).filter(is_group_request=False)]
        # group requests
        my_id_list.extend(
            [trip_request.id for trip_request in TripRequest.objects.filter(parent_request__trip=self).filter(~Q(status_id__in=[10, 22]))])
        return TripRequest.objects.filter(id__in=my_id_list)

    @property
    def get_summary_dict(self):
        """
        This method is used to return a dictionary of users attending a trip, as well as the number of
        trips or international meetings they have attended.
        """
        my_dict = {}

        # get a trip list that will be used to get a list of users (sigh...)
        # my_trip_list = self.children_requests.all() if self.is_group_request else Trip.objects.filter(pk=self.id)

        # get the fiscal year of the trip
        fy = self.fiscal_year

        for traveller in self.total_traveller_list:
            total_list = []
            fy_list = []

            # if this is not a real User instance, there is nothing to do.
            try:

                # there are two things we have to do to get this list...
                # 1) get all non group travel
                qs = traveller.user_trip_requests.filter(trip__is_adm_approval_required=True).filter(is_group_request=False)
                total_list.extend([trip for trip in qs])
                fy_list.extend([trip for trip in qs.filter(fiscal_year=fy)])

                # 2) get all group travel - the trick part is that we have to grab the parent trip
                qs = traveller.user_trip_requests.filter(parent_request__trip__is_adm_approval_required=True)
                total_list.extend([trip_request.parent_request for trip_request in qs])
                fy_list.extend([trip_request.parent_request for trip_request in qs.filter(fiscal_year=fy)])

                my_dict[traveller] = {}
                my_dict[traveller]["total_list"] = list(set(total_list))
                my_dict[traveller]["fy_list"] = list(set(fy_list))

            except AttributeError:
                # This is the easy part
                my_dict[traveller] = {}
                my_dict[traveller]["total_list"] = "---"
                my_dict[traveller]["fy_list"] = "---"
        return my_dict


class TripRequest(models.Model):
    fiscal_year = models.ForeignKey(shared_models.FiscalYear, on_delete=models.DO_NOTHING, verbose_name=_("fiscal year"),
                                    default=fiscal_year(sap_style=True), blank=True, null=True, related_name="trip_requests")
    is_group_request = models.BooleanField(default=False,
                                           verbose_name=_("Is this a group request (i.e., a request for multiple individuals)?"))
    purpose = models.ForeignKey(Purpose, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("purpose of travel"))
    reason = models.ForeignKey(Reason, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("reason for travel"))
    trip = models.ForeignKey(Conference, on_delete=models.DO_NOTHING, null=True, verbose_name=_("trip"), related_name="trip_requests")

    # traveller info
    user = models.ForeignKey(AuthUser, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="user_trip_requests",
                             verbose_name=_("DM Apps user"))
    section = models.ForeignKey(shared_models.Section, on_delete=models.DO_NOTHING, null=True, verbose_name=_("DFO section"))
    first_name = models.CharField(max_length=100, verbose_name=_("first name"), blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name=_("last name"), blank=True, null=True)
    address = models.CharField(max_length=1000, verbose_name=_("address"),
                               blank=True, null=True)
    phone = models.CharField(max_length=1000, verbose_name=_("phone"), blank=True, null=True)
    email = models.EmailField(verbose_name=_("email"), blank=True, null=True)
    is_public_servant = models.BooleanField(default=True, choices=YES_NO_CHOICES, verbose_name=_("Is the traveller a public servant?"))
    is_research_scientist = models.BooleanField(default=False, choices=YES_NO_CHOICES,
                                                verbose_name=_("Is the traveller a research scientist (RES)?"))
    company_name = models.CharField(max_length=255, verbose_name=_("company name"), blank=True, null=True)
    region = models.ForeignKey(shared_models.Region, on_delete=models.DO_NOTHING, verbose_name=_("DFO region"),
                               related_name="trip_requests",
                               null=True, blank=True)
    # trip_title = models.CharField(max_length=1000, verbose_name=_("trip title"))
    departure_location = models.CharField(max_length=1000, verbose_name=_("departure location (city, province, country)"), blank=True,
                                          null=True)
    destination = models.CharField(max_length=1000, verbose_name=_("destination location (city, province, country)"), blank=True,
                                   null=True)
    start_date = models.DateTimeField(verbose_name=_("start date of travel"), null=True, blank=True)
    end_date = models.DateTimeField(verbose_name=_("end date of travel"), null=True, blank=True)

    #############
    # these two fields should be deleted eventually if the event planning peice happens through this app...
    # has_event_template = models.NullBooleanField(default=False,
    #                                              verbose_name=_(
    #                                                  "Is there an event template being completed for this trip or meeting?"))
    # event_lead = models.ForeignKey(shared_models.Region, on_delete=models.DO_NOTHING, verbose_name=_("Regional event lead"),
    #                                related_name="trip_events", blank=True, null=True)
    ################
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("role of traveller"))

    # purpose
    role_of_participant = models.TextField(blank=True, null=True, verbose_name=_("role description"))
    objective_of_event = models.TextField(blank=True, null=True, verbose_name=_("objective of the trip"))
    benefit_to_dfo = models.TextField(blank=True, null=True, verbose_name=_("benefit to DFO"))
    multiple_conferences_rationale = models.TextField(blank=True, null=True,
                                                      verbose_name=_("rationale for individual attending multiple conferences"))
    bta_attendees = models.ManyToManyField(AuthUser, blank=True, verbose_name=_("Other attendees covered under BTA"))
    multiple_attendee_rationale = models.TextField(blank=True, null=True, verbose_name=_(
        "rationale for multiple travelers"))
    late_justification = models.TextField(blank=True, null=True, verbose_name=_("Justification for late submissions"))
    funding_source = models.TextField(blank=True, null=True, verbose_name=_("funding source"))
    notes = models.TextField(blank=True, null=True, verbose_name=_("optional notes"))

    # costs
    air = models.FloatField(blank=True, null=True, verbose_name=_("air fare"))
    rail = models.FloatField(blank=True, null=True, verbose_name=_("rail"))
    rental_motor_vehicle = models.FloatField(blank=True, null=True, verbose_name=_("rental motor vehicles"))
    personal_motor_vehicle = models.FloatField(blank=True, null=True, verbose_name=_("personal motor vehicles"))
    taxi = models.FloatField(blank=True, null=True, verbose_name=_("taxi"))
    other_transport = models.FloatField(blank=True, null=True, verbose_name=_("other transport"))
    accommodations = models.FloatField(blank=True, null=True, verbose_name=_("accommodation"))
    # meals = models.FloatField(blank=True, null=True, verbose_name=_("meals"))
    no_breakfasts = models.IntegerField(blank=True, null=True, verbose_name=_("number of breakfasts"))
    breakfasts_rate = models.FloatField(blank=True, null=True, verbose_name=_("breakfast rate (CAD/day)"), default=20.35)
    breakfasts = models.FloatField(blank=True, null=True, verbose_name=_("breakfasts"))
    no_lunches = models.IntegerField(blank=True, null=True, verbose_name=_("number of lunches"))
    lunches_rate = models.FloatField(blank=True, null=True, verbose_name=_("lunch rate (CAD/day)"), default=20.60)
    lunches = models.FloatField(blank=True, null=True, verbose_name=_("lunches"))
    no_suppers = models.IntegerField(blank=True, null=True, verbose_name=_("number of suppers"))
    suppers_rate = models.FloatField(blank=True, null=True, verbose_name=_("supper rate (CAD/day)"), default=50.55)
    suppers = models.FloatField(blank=True, null=True, verbose_name=_("suppers"))
    no_incidentals = models.IntegerField(blank=True, null=True, verbose_name=_("number of incidentals"))
    incidentals_rate = models.FloatField(blank=True, null=True, verbose_name=_("incidental rate (CAD/day)"), default=17.30)
    incidentals = models.FloatField(blank=True, null=True, verbose_name=_("incidentals"))
    registration = models.FloatField(blank=True, null=True, verbose_name=_("registration"))
    other = models.FloatField(blank=True, null=True, verbose_name=_("other"))
    total_cost = models.FloatField(blank=True, null=True, verbose_name=_("total cost (DFO)"))
    non_dfo_costs = models.FloatField(blank=True, null=True, verbose_name=_("estimated non-DFO costs (CAD)"))
    non_dfo_org = models.CharField(max_length=1000, verbose_name=_("full name(s) of organization paying non-DFO costs"), blank=True,
                                   null=True)

    submitted = models.DateTimeField(verbose_name=_("date sumbitted"), blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name="trip_requests",
                               limit_choices_to={"used_for": 2}, verbose_name=_("trip status"), default=8)
    parent_request = models.ForeignKey("TripRequest", on_delete=models.CASCADE, related_name="children_requests", blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True, verbose_name=_("Administrative notes"))

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
        unique_together = [("user", "parent_request"), ]

    def get_absolute_url(self):
        return reverse('travel:request_detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):

        if self.start_date:
            self.fiscal_year_id = fiscal_year(date=self.start_date, sap_style=True)

        # if the start and end dates are null, but there is a trip, use those.. to populate
        if self.trip and not self.start_date:
            # print("adding start date from trip")
            self.start_date = self.trip.start_date
        if self.trip and not self.end_date:
            # print("adding end date from trip")
            self.end_date = self.trip.end_date

        # If this is a group request, the parent record should not have any costs
        if self.is_group_request:
            self.trip_request_costs.all().delete()

        # If this is a child request, it should not have any assigned reviewers
        if self.parent_request:
            self.reviewers.all().delete()

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
        return my_str

    @property
    def cost_breakdown_html(self):
        my_str = ""
        for tr_cost in self.trip_request_costs.all():
            if tr_cost.rate_cad:
                my_str += "<b>{}</b>: ${:,.2f} ({} x {:,.2f})<br>".format(
                    tr_cost.cost,
                    nz(tr_cost.rate_cad, 0),
                    nz(tr_cost.number_of_days, 0),
                    nz(tr_cost.amount_cad, 0),
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
            return sum([item.total_cost for item in object_list])

        else:
            return self.total_cost

    @property
    def travellers(self):
        if self.is_group_request:
            return [tr.user for tr in self.children_requests.all()]
        else:
            return self.user

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
        if self.multiple_attendee_rationale:
            my_str += "<br><em>Rationale for multiple attendees:</em> {}".format(self.multiple_attendee_rationale)
        if self.funding_source:
            my_str += "<br><em>Funding source:</em> {}".format(self.funding_source)

        return my_str

    @property
    def purpose_long_text(self):
        """
        For CFTS report
        """
        my_str = "{}: {}".format("OBJECTIVE OF EVENT", nz(self.objective_of_event, "n/a"))

        my_str += "\n\n{}: {}".format("BENEFIT TO DFO", nz(self.benefit_to_dfo, "n/a"))

        my_str += "\n\n{}: {}".format(
            "Rationale for attending multiple conferences".upper(), nz(self.multiple_conferences_rationale, "n/a"))

        my_str += "\n\n{}: {}".format(
            "Rationale for multiple attendees".upper(),
            nz(self.multiple_attendee_rationale, "n/a"))
        return my_str

    @property
    def current_reviewer(self):
        """Send back the first reviewer whose status is 'pending' """
        return self.reviewers.filter(status_id=1).first()

    @property
    def status_string(self):
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


class TripRequestCost(models.Model):
    trip_request = models.ForeignKey(TripRequest, on_delete=models.CASCADE, related_name="trip_request_costs",
                                     verbose_name=_("trip request"))
    cost = models.ForeignKey(Cost, on_delete=models.DO_NOTHING, related_name="trip_request_costs", verbose_name=_("cost"))
    rate_cad = models.FloatField(verbose_name=_("daily rate (CAD/day)"), blank=True, null=True)
    number_of_days = models.FloatField(verbose_name=_("number of days"), blank=True, null=True)
    amount_cad = models.FloatField(default=0, verbose_name=_("amount (CAD)"), blank=True, null=True)

    class Meta:
        unique_together = (("trip_request", "cost"),)

    def save(self, *args, **kwargs):
        # if a user is providing a rate and number of days, we use this to calc the total amount.
        if (self.rate_cad and self.rate_cad != 0) and (self.number_of_days and self.number_of_days != 0):
            self.amount_cad = self.rate_cad * self.number_of_days

        super().save(*args, **kwargs)


class ReviewerRole(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name (eng)"), blank=True, null=True)
    nom = models.CharField(max_length=100, verbose_name=_("name (fre)"), blank=True, null=True)
    order = models.IntegerField()

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

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

    class Meta:
        unique_together = ['trip_request', 'user', 'role', ]
        ordering = ['trip_request', 'order', ]

    @property
    def comments_html(self):
        if self.comments:
            return textile.textile(self.comments)

    def save(self, *args, **kwargs):
        # if not self.status:
        #     self.status_date = timezone.now()
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
