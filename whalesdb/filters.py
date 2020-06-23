import django
import django_filters
from django.utils.translation import gettext as _

from . import models


class DepFilter(django_filters.FilterSet):
    mor_name = django_filters.CharFilter(field_name='dep_name', lookup_expr='icontains')

    class Meta:
        model = models.DepDeployment
        fields = ['dep_name', 'dep_year', 'dep_month', 'stn', 'prj', 'mor']


class EmmFilter(django_filters.FilterSet):

    class Meta:
        model = models.EmmMakeModel
        fields = ['eqt', 'emm_make', 'emm_model', 'emm_depth_rating']


class EqpFilter(django_filters.FilterSet):

    class Meta:
        model = models.EqpEquipment
        fields = ['emm', 'eqp_serial', 'eqp_date_purchase', 'eqo_owned_by', 'eqp_retired', 'eqp_deployed']


class MorFilter(django_filters.FilterSet):
    mor_name = django_filters.CharFilter(field_name='mor_name', lookup_expr='icontains')
    mor_max_depth = django_filters.NumberFilter(field_name='mor_max_depth', lookup_expr='icontains')

    class Meta:
        model = models.MorMooringSetup
        fields = []


class PrjFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name=_("name"), lookup_expr='icontains')
    description = django_filters.CharFilter(field_name=_("description_en"), lookup_expr='icontains')

    class Meta:
        model = models.PrjProject
        fields = []


class RecFilter(django_filters.FilterSet):

    class Meta:
        model = models.RecDataset
        fields = ['eda_id', 'rsc_id', 'rec_start_date', 'rec_end_date']


class RscFilter(django_filters.FilterSet):
    rsc_name = django_filters.CharFilter(field_name='rsc_name', lookup_expr='icontains')

    class Meta:
        model = models.RscRecordingSchedule
        fields = []


class RttFilter(django_filters.FilterSet):
    rtt_name = django_filters.CharFilter(field_name='rtt_name', lookup_expr='icontains')

    class Meta:
        model = models.RttTimezoneCode
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


class TeaFilter(django_filters.FilterSet):
    tea_abb = django_filters.CharFilter(field_name='tea_abb', lookup_expr='icontains')
    tea_last_name = django_filters.CharFilter(field_name='tea_last_name', lookup_expr='icontains')
    tea_first_name = django_filters.CharFilter(field_name='tea_first_name', lookup_expr='icontains')

    class Meta:
        model = models.TeaTeamMember
        fields = []
