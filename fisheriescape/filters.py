import django_filters
from django import forms
from django.db.models import Q

from . import models
from django.utils.translation import gettext as _

attr_fp_date = {"class": "fp-date", "placeholder": "Click to select a date.."}


class SpeciesFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(field_name='search_term', label="Species (any part of name or description)",
                                            lookup_expr='icontains', widget=forms.TextInput())


class FisheryAreaFilter(django_filters.FilterSet):
    class Meta:
        model = models.FisheryArea
        fields = {
            'name': ['icontains'],
            'region': ['exact'],

        }


class FisheryFilter(django_filters.FilterSet):
    # start_date = django_filters.DateFilter(field_name='start_date', lookup_expr='lt',
    #                                        label='Start date is before (mm/dd/yyyy):',
    #                                        widget=forms.DateInput(attrs=attr_fp_date))

    # had to add 'django_filters' to INSTALLED_APPS in settings.py
    # date_between = django_filters.DateFromToRangeFilter(field_name='start_date',
    #                                                     label='Season Start Date (Between)',
    #                                                     widget=django_filters.widgets.RangeWidget(attrs=attr_fp_date))

    date = django_filters.DateTimeFilter(method='date_filter', widget=forms.DateInput(attrs=attr_fp_date), label="Date of Interest")

    class Meta:
        model = models.Fishery
        fields = {
            'fishery_areas': ['exact'],
            'fishery_status': ['exact'],
            'gear_type': ['exact'],

        }

    def date_filter(self, queryset, name, value):
        return models.Fishery.objects.filter(
            Q(start_date__lte=value) & Q(end_date__gte=value)
        )

#TODO this doesn't currently work
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["species__icontains"] = django_filters.CharFilter(field_name='search_term',
                                                                            label="Species (any language)",
                                                                            lookup_expr='icontains',
                                                                            widget=forms.TextInput())


#TODO Something like what I want a custom filter to do:
# from datetime import datetime
# my_date= request.POST.get('my_date','') # for eg. 2019-10-26
# my_date = datetime.strptime(my_date, "%Y-%m-%d")
# date_between = Fishery.objects.filter(start_date__lt=my_date, end_date__gt=my_date).order_by('start_date')