import django
import django_filters
from django.utils.translation import gettext as _
from django.db.models import Q

from . import models
import shared_models.models as shared_models


class DepFilter(django_filters.FilterSet):
    mor_name = django_filters.CharFilter(field_name='dep_name', lookup_expr='icontains')

    class Meta:
        model = models.DepDeployment
        fields = ['dep_name', 'dep_year', 'dep_month', 'stn', 'prj', 'mor']


class EcaFilter(django_filters.FilterSet):

    eca_hydrophone = django_filters.ModelChoiceFilter(queryset=models.EqpEquipment.objects.filter(emm__eqt_id=4))
    class Meta:
        model = models.EcaCalibrationEvent
        fields = ['eca_date', 'eca_attachment', 'eca_hydrophone']


class EmmFilter(django_filters.FilterSet):

    class Meta:
        model = models.EmmMakeModel
        fields = ['eqt', 'emm_make', 'emm_model', 'emm_depth_rating']


class EqpFilter(django_filters.FilterSet):

    class Meta:
        model = models.EqpEquipment
        fields = ['emm', 'eqp_serial', 'eqp_date_purchase', 'eqo_owned_by', 'eqp_retired', 'eqp_deployed']


class EtrFilter(django_filters.FilterSet):

    recorder = django_filters.ChoiceFilter(label='Equipment Type', method='filter_recorder')
    eqp_f = django_filters.ChoiceFilter(label='Equipment', method='filter_eqp')

    class Meta:
        model = models.EtrTechnicalRepairEvent
        fields = ['etr_date', "recorder", 'eqp_f', 'etr_issue_desc', 'etr_repair_desc', 'etr_repaired_by', 'etr_dep_affe', 'etr_rec_affe' ]

    def filter_recorder(self, queryset, name, value):
        if value:
            return queryset.filter(eqp__emm__eqt_id=value)

        return queryset

    def filter_eqp(self, queryset, name, value):
        if value:
            return queryset.filter(eqp_id=value)

        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        eqt_code_list = [(eqt.pk, eqt.name) for eqt in models.EqtEquipmentTypeCode.objects.all()]

        # using a custom filter for equipment so we can filter equipment types based on the eqt field
        # if the recorder choice field is set filter the eqp_f field
        eqp_qry = models.EqpEquipment.objects.all()
        if kwargs['data'] is not None and 'recorder' in kwargs['data'].keys():
            eqp_qry = eqp_qry.filter(emm__eqt_id=kwargs['data']['recorder'])

        eqp_choice = [(eqp.pk, str(eqp)) for eqp in eqp_qry]

        self.filters['recorder'].field.choices = eqt_code_list
        self.filters['eqp_f'].field.choices = eqp_choice


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


class RetFilter(django_filters.FilterSet):

    class Meta:
        model = models.RetRecordingEventType
        fields = ['ret_name', 'ret_desc']


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


class CruFilter(django_filters.FilterSet):

    class Meta:
        model = shared_models.Cruise
        fields = ['start_date', 'end_date']
