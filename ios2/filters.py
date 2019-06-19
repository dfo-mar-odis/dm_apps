from django.contrib.auth.models import User
from shared_models import models as shared_models

from . import models
import django_filters
from django import forms

chosen_js = {"class":"chosen-select-contains"}
# chosen_js = {"class":"chosen-select-contains", 'Select multiple': True}
# chosen_js = {"class":"chosen-select-contains"}


class InstrumentFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        YES_NO_CHOICES = [(True, "Yes"), (False, "No"), ]

        type_choices = models.Instrument.TYPE_CHOICES
        asset_choices = [(str(at.asset_tag), str(at.asset_tag)) for at in models.Instrument.objects.all()]

        self.filters["project_title"] = django_filters.CharFilter(field_name='project_title', lookup_expr='icontains')

        self.filters["instrument_type"] = django_filters.MultipleChoiceFilter(field_name='instrument_type', lookup_expr='exact',
                                                              choices=type_choices,
                                                              widget=forms.SelectMultiple(attrs=chosen_js))
        self.filters["location"] = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
        self.filters["is_sensor"] = django_filters.ChoiceFilter(field_name='is_sensor', lookup_expr='exact',
                                                label="Is Sensor?", choices=YES_NO_CHOICES)
        self.filters["asset_tag"] = django_filters.MultipleChoiceFilter(field_name='asset_tag', lookup_expr='exact',
                                                        choices=asset_choices,
                                                        widget=forms.SelectMultiple(attrs=chosen_js))




class MooringFilter(django_filters.FilterSet):
    # FY_CHOICES = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all()]
    # DIVISION_CHOICES = [(d.id, str(d)) for d in shared_models.Division.objects.filter(branch=1)]
    # SECTION_CHOICES = [(s.id, str(s)) for s in shared_models.Section.objects.filter(division__branch=1)]
    # TYPE_CHOICES = [('CTD', 'CTD'), ('ADCP', 'ADCP')]
    # LOC_CHOICES = models.Mooring.TYPE_CHOICES
    YES_NO_CHOICES = [(True, "Yes"), (False, "No"), ]

    mooring = django_filters.CharFilter(field_name='mooring', lookup_expr='icontains')
    mooring_number = django_filters.CharFilter(field_name='mooring_number', lookup_expr='exact')
    # mooring_number = django_filters.ChoiceFilter(field_name='mooring_number', lookup_expr='exact',
    #                                                   # label=_'mooring_number',
    #                                                   #    queryset=models.Mooring.objects.all(),
    #                                                      widget=forms.SelectMultiple(attrs=chosen_js))
    # mooring = django_filters.CharFilter(field_name='mooring', lookup_expr='icontains')
    # mooring_number = django_filters.ModelChoiceFilter(queryset=Deployment.objects.all)#, lookup_expr='exact')
    # fiscal_year = django_filters.ChoiceFilter(field_name='year', lookup_expr='exact', choices=FY_CHOICES)
    # division = django_filters.ChoiceFilter(field_name='section__division', lookup_expr='exact', label="Division", choices=DIVISION_CHOICES)
    # section = django_filters.ChoiceFilter(field_name='section', lookup_expr='exact', label="Section", choices=SECTION_CHOICES)
    # submitted = django_filters.ChoiceFilter(field_name='submitted', lookup_expr='exact',
    #                                         label="Submitted?", choices=YES_NO_CHOICES)
    # def get_queryset(self):
    #     return django_filters.MooringFilter(self.request.GET, queryset=models.Mooring.objects.exclude(mooring='HOME IOS'))
