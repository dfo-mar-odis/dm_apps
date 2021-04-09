import django_filters
from . import models
from django import forms
from django.utils.translation import gettext as _


attr_fp_date = {"class": "fp-date", "placeholder": "Click to select a date.."}


class SpeciesFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(field_name='search_term', label="Items (any part of name...)",
                                            lookup_expr='icontains', widget=forms.TextInput())


class ObservationPlatformFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(field_name='search_term', label="Items (any part of name...)",
                                            lookup_expr='icontains', widget=forms.TextInput())


class InstrumentFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(field_name='search_term', label="Items (any part of name...)",
                                            lookup_expr='icontains', widget=forms.TextInput())


class OutingFilter(django_filters.FilterSet):
    date = django_filters.DateTimeFromToRangeFilter(
        field_name='start_date',
        label=_('With start date between'),
        # lookup_type='contains',  # use contains
        widget=django_filters.widgets.RangeWidget(attrs=attr_fp_date)
    )

    class Meta:
        model = models.Outing
        fields = {
            'observation_platform': ['exact'],
            'region': ['exact'],
            'purpose': ['exact'],

        }


class PersonFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(field_name='search_term', label="Items (any part of name...)",
                                            lookup_expr='icontains', widget=forms.TextInput())


class ObservationFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(field_name='search_term', label="Items (any part of name...)",
                                            lookup_expr='icontains', widget=forms.TextInput())


class UserFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(field_name='search_term', label=_("Name contains"), lookup_expr='icontains',
                                            widget=forms.TextInput())
