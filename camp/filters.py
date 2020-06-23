import django_filters
from . import models
from django import forms


class SampleFilter(django_filters.FilterSet):
    SeasonExact = django_filters.NumberFilter(field_name='year', label="From year", lookup_expr='exact')
    MonthExact = django_filters.NumberFilter(field_name='month', label="From month", lookup_expr='exact')

    class Meta:
        model = models.Sample
        fields = {
            'id': ['exact'],
            'station__site': ['exact'],
            'station': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters.get("station__site").label = "Site"


#
# class StationFilter(django_filters.FilterSet):
#     class Meta:
#         model = models.Station
#         fields = {
#             'station_name':['icontains'],
#             'province':['exact'],
#         }
#
#

class SiteFilter(django_filters.FilterSet):
    class Meta:
        model = models.Site
        fields = {
            'site': ['icontains'],
            'province': ['exact'],
        }


# class ReportFilter(django_filters.FilterSet):
#     class Meta:
#         model = models.IncidentalReport
#         fields = {
#             'season':['exact'],
#             'report_type':['exact'],
#         }
#
#
# class SpeciesFilter(django_filters.FilterSet):
#     class Meta:
#         model = models.Species
#         fields = {
#             'common_name_eng': ['icontains'],
#             'common_name_fre': ['icontains'],
#             'code': ['icontains'],
#         }
#


class SpeciesFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(field_name='search_term', label="Species (any part of name...)", lookup_expr='icontains',
                                            widget=forms.TextInput())
