import django_filters
from . import models
from django import forms

chosen_js = {"class":"chosen-select-contains"}

class SampleFilter(django_filters.FilterSet):
    class Meta:
        model = models.Sample
        fields = {
            'id': ['exact'],
            'season': ['exact'],
            'station': ['exact'],
            'sample_type': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['station'] = django_filters.ModelChoiceFilter(
            field_name="station",
            queryset=models.Station.objects.all(),
            widget=forms.Select(attrs=chosen_js),
        )


class StationFilter(django_filters.FilterSet):
    class Meta:
        model = models.Station
        fields = {
            'station_name': ['icontains'],
            'province': ['exact'],
        }


class EstuaryFilter(django_filters.FilterSet):
    class Meta:
        model = models.Estuary
        fields = {
            'name': ['icontains'],
            'province': ['exact'],
        }


class GCSampleFilter(django_filters.FilterSet):
    class Meta:
        model = models.GCSample
        fields = {
            'id': ['exact'],
            'season': ['exact'],
            'site__estuary': ['exact'],
            'site': ['exact'],
        }


class ReportFilter(django_filters.FilterSet):
    class Meta:
        model = models.IncidentalReport
        fields = {
            'season': ['exact'],
            'report_source': ['exact'],
        }


class SpeciesFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(field_name='search_term', label="Species (any part of name...)", lookup_expr='icontains',
                                            widget=forms.TextInput())


class SpeciesFilterFull(django_filters.FilterSet):
    search_term = django_filters.CharFilter(field_name='search_term', label="Species (any part of name...)", lookup_expr='icontains',
                                            widget=forms.TextInput())

    class Meta:
        model = models.Species
        fields = {
            'tsn': ['exact'],
            'aphia_id': ['exact'],
            'epibiont_type': ['exact'],
            'invasive': ['exact'],
            'color_morph': ['exact'],
        }
        labels = {
            'tsn': "TSN",

        }
