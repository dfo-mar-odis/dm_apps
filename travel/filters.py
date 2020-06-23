# from accounts import models as account_models
# from  import gettext as _
from django.utils.translation import gettext as _
from django import forms
import django_filters
from django.contrib.auth.models import User
from django.db.models import Q

from shared_models import models as shared_models
from . import models

chosen_js = {"class": "chosen-select-contains"}


def get_section_choices(all=False, full_name=True):
    if full_name:
        my_attr = "full_name"
    else:
        my_attr = _("name")

    return [(s.id, getattr(s, my_attr)) for s in
            shared_models.Section.objects.all().order_by(
                "division__branch__region",
                "division__branch",
                "division",
                "name"
            ) if s.trip_requests.count() > 0] if not all else [(s.id, getattr(s, my_attr)) for s in
                                                               shared_models.Section.objects.filter(
                                                                   division__branch__name__icontains="science").order_by(
                                                                   "division__branch__region",
                                                                   "division__branch",
                                                                   "division",
                                                                   "name"
                                                               )]


def get_division_choices(all=False):
    if all:
        division_list = set([shared_models.Section.objects.get(pk=s[0]).division for s in get_section_choices(all=True)])
    else:
        division_list = set([shared_models.Section.objects.get(pk=s[0]).division for s in get_section_choices()])
    q_objects = Q()  # Create an empty Q object to start with
    for d in division_list:
        q_objects |= Q(id=d.id)  # 'or' the Q objects together

    return [(d.id, str(d)) for d in
            shared_models.Division.objects.filter(q_objects).order_by(
                "branch__region",
                "name"
            )]


def get_region_choices(all=False):
    if all:
        region_list = set([shared_models.Division.objects.get(pk=d[0]).branch.region for d in get_division_choices(all=True)])
    else:
        region_list = set([shared_models.Division.objects.get(pk=d[0]).branch.region for d in get_division_choices()])
    q_objects = Q()  # Create an empty Q object to start with
    for r in region_list:
        q_objects |= Q(id=r.id)  # 'or' the Q objects together

    return [(r.id, str(r)) for r in
            shared_models.Region.objects.filter(q_objects).order_by(
                "name",
            )]


class TripRequestFilter(django_filters.FilterSet):
    class Meta:
        model = models.TripRequest
        fields = {
            'fiscal_year': ['exact'],
            'trip': ['exact'],
            'status': ['exact'],
            # 'user': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_choices = [(u.id, "{}, {}".format(u.last_name, u.first_name)) for u in User.objects.all().order_by("last_name", "first_name")
                        if u.user_trip_requests.count() > 0]
        self.filters['user'] = django_filters.ChoiceFilter(field_name='user', lookup_expr='exact', choices=user_choices,
                                                           widget=forms.Select(attrs=chosen_js), label=_('User'))

        trip_choices = [(trip.id, f"{trip}") for trip in models.Conference.objects.all().order_by(_("name")) if
                        trip.trip_requests.count() > 0]
        self.filters['trip'] = django_filters.ChoiceFilter(field_name='trip', lookup_expr='exact', choices=trip_choices,
                                                           widget=forms.Select(attrs=chosen_js), label=_('Trip title'))

        region_choices = get_region_choices()
        division_choices = get_division_choices()
        section_choices = get_section_choices()
        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all() if fy.trip_requests.count() > 0]

        self.filters['fiscal_year'] = django_filters.ChoiceFilter(field_name='fiscal_year', lookup_expr='exact', choices=fy_choices,
                                                                  label=_("Fiscal year"))
        self.filters['region'] = django_filters.ChoiceFilter(field_name="section__division__branch__region", label=_("Region"),
                                                             lookup_expr='exact', choices=region_choices)
        self.filters['division'] = django_filters.ChoiceFilter(field_name="section__division", label=_("Division"),
                                                               lookup_expr='exact', choices=division_choices)
        self.filters['section'] = django_filters.ChoiceFilter(field_name="section", label=_("Section"),
                                                              lookup_expr='exact', choices=section_choices)

        try:
            # if there is a filter on region, filter the division and section filter accordingly
            if self.data["region"] != "":
                my_region_id = int(self.data["region"])
                division_choices = [my_set for my_set in get_division_choices() if
                                    shared_models.Division.objects.get(pk=my_set[0]).branch.region_id == my_region_id]
                self.filters['division'] = django_filters.ChoiceFilter(field_name="section__division", label=_("Division"),
                                                                       lookup_expr='exact', choices=division_choices)

                section_choices = [my_set for my_set in get_section_choices() if
                                   shared_models.Section.objects.get(pk=my_set[0]).division.branch.region_id == my_region_id]
                self.filters['section'] = django_filters.ChoiceFilter(field_name="section", label=_("Section"),
                                                                      lookup_expr='exact', choices=section_choices)

            # if there is a filter on division, filter the section filter accordingly
            if self.data["division"] != "":
                my_division_id = int(self.data["division"])

                section_choices = [my_set for my_set in get_section_choices() if
                                   shared_models.Section.objects.get(pk=my_set[0]).division_id == my_division_id]
                self.filters['section'] = django_filters.ChoiceFilter(field_name="section", label=_("Section"),
                                                                      lookup_expr='exact', choices=section_choices)

        except KeyError:
            pass


class TripFilter(django_filters.FilterSet):
    class Meta:
        model = models.Conference
        fields = {
            'name': ['exact'],
            'fiscal_year': ['exact'],
            'lead': ['exact'],
            'is_adm_approval_required': ['exact'],
            'status': ['exact'],
            'trip_subcategory': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all() if fy.trips.count() > 0]
        self.filters['fiscal_year'] = django_filters.ChoiceFilter(field_name='fiscal_year', lookup_expr='exact', choices=fy_choices,
                                                                  label=_("Fiscal year"))
        self.filters['name'] = django_filters.CharFilter(field_name='search_term', label=_("Trip Title"), lookup_expr='icontains',
                                                         widget=forms.TextInput())
        self.filters['lead'].label = _("Regional lead")
        self.filters['is_adm_approval_required'].label = _("ADM approval required?")


class TripRequestApprovalFilter(django_filters.FilterSet):
    class Meta:
        model = models.TripRequest
        fields = {
            # 'waiting_on': ['exact'],
        }
