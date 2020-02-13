import django
import django_filters

from . import models


class PrjFilter(django_filters.FilterSet):
    prj_name = django_filters.CharFilter(field_name='prj_name', lookup_expr='icontains')
    prj_description = django_filters.CharFilter(field_name='prj_description', lookup_expr='icontains')

    class Meta:
        model = models.PrjProject
        fields = []


class StnFilter(django_filters.FilterSet):
    stn_name = django_filters.CharFilter(field_name='stn_name', lookup_expr='icontains')
    stn_code = django_filters.ChoiceFilter(field_name='stn_code')
    stn_revision = django_filters.NumberFilter(field_name='stn_revision', lookup_expr='exact',
                                               widget=django.forms.NumberInput(attrs={'style': "width: 4em"}))

    class Meta:
        model = models.StnStation
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        code_list = [(sc['stn_code'], sc['stn_code']) for sc in models.StnStation.objects.values('stn_code').distinct()]

        self.filters['stn_code'] = django_filters.ChoiceFilter(field_name='stn_code', lookup_expr='exact',
                                                               choices=code_list)


class MorFilter(django_filters.FilterSet):
    mor_name = django_filters.CharFilter(field_name='mor_name', lookup_expr='icontains')
    mor_max_depth = django_filters.NumberFilter(field_name='mor_max_depth', lookup_expr='icontains')

    class Meta:
        model = models.MorMooringSetup
        fields = []
