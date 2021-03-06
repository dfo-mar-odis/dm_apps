import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from shared_models.models import FiscalYear, Section, Branch, Region, Person
from . import models, utils
from .model_choices import request_status_choices

YES_NO_CHOICES = [(True, _("Yes")), (False, _("No")), ]
chosen_js = {"class": "chosen-select-contains"}


class UserFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(field_name='search_term', label=_("Name contains"), lookup_expr='icontains',
                                            widget=forms.TextInput())


class PersonFilter(django_filters.FilterSet):
    class Meta:
        model = Person
        fields = {
            'last_name': ['exact'],
            'affiliation': ['icontains'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["last_name"] = django_filters.CharFilter(field_name='search_term', label=_("Any part of name or email"),
                                                              lookup_expr='icontains', widget=forms.TextInput())


class CSASRequestFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(field_name='search_term', lookup_expr='icontains', label=_("Title / Reference Number"))
    request_id = django_filters.NumberFilter(field_name='id', lookup_expr='exact')
    fiscal_year = django_filters.ChoiceFilter(field_name='fiscal_year', lookup_expr='exact')
    region = django_filters.ChoiceFilter(field_name="section__division__branch__region", label=_("Region"), lookup_expr='exact')
    branch = django_filters.ChoiceFilter(field_name="section__division__branch", label=_("Branch / Sector"), lookup_expr='exact')
    has_process = django_filters.BooleanFilter(field_name='processes', lookup_expr='isnull', label=_("Has process?"), exclude=True)
    status = django_filters.MultipleChoiceFilter(field_name='status', lookup_expr='exact', label=_("Status"),
                                                 widget=forms.SelectMultiple(attrs=chosen_js), choices=request_status_choices)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        region_choices = utils.get_region_choices()
        branch_choices = utils.get_branch_choices()
        fy_choices = [(fy.id, str(fy)) for fy in FiscalYear.objects.filter(csas_requests__isnull=False).distinct()]

        self.filters['fiscal_year'] = django_filters.MultipleChoiceFilter(field_name='fiscal_year', lookup_expr='exact', choices=fy_choices,
                                                                          label=_("Fiscal year"), widget=forms.SelectMultiple(attrs=chosen_js))
        self.filters['region'] = django_filters.ChoiceFilter(field_name="section__division__branch__region", label=_("Region"), lookup_expr='exact',
                                                             choices=region_choices)
        self.filters['branch'] = django_filters.ChoiceFilter(field_name="section__division__branch", label=_("Branch / Sector"), lookup_expr='exact',
                                                             choices=branch_choices)

        try:
            if self.data["region"] != "":
                my_region_id = int(self.data["region"])
                branch_choices = [my_set for my_set in utils.get_branch_choices() if Branch.objects.get(pk=my_set[0]).region_id == my_region_id]
                self.filters['branch'] = django_filters.ChoiceFilter(field_name="section__division__branch", label=_("Branch / Sector"), lookup_expr='exact',
                                                                     choices=branch_choices)

                section_choices = [my_set for my_set in utils.get_section_choices() if
                                   Section.objects.get(pk=my_set[0]).division.branch.region_id == my_region_id]

        except KeyError:
            print('no data in filter')


class ProcessFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name='id', lookup_expr='exact', label=_("Process ID"))
    fiscal_year = django_filters.ChoiceFilter(field_name='fiscal_year', lookup_expr='exact')
    search_term = django_filters.CharFilter(field_name='search_term', lookup_expr='icontains', label=_("Title contains"))
    lead_region = django_filters.ChoiceFilter(field_name="lead_region", label=_("Lead Region"), lookup_expr='exact')
    is_posted = django_filters.ChoiceFilter(field_name="is_posted", label=_("Is Posted?"), lookup_expr='exact', empty_label=_("All"), choices=YES_NO_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fy_choices = [(fy.id, str(fy)) for fy in FiscalYear.objects.filter(processes__isnull=False).distinct()]
        region_choices = [(obj.id, str(obj)) for obj in Region.objects.filter(process_lead_regions__isnull=False).distinct()]

        self.filters['fiscal_year'] = django_filters.ChoiceFilter(field_name='fiscal_year', lookup_expr='exact', choices=fy_choices, label=_("Fiscal year"))
        self.filters['lead_region'] = django_filters.ChoiceFilter(field_name="lead_region", label=_("Lead Region"), lookup_expr='exact', choices=region_choices)

    class Meta:
        model = models.Process
        fields = {
            'type': ['exact'],
        }


class MeetingFilter(django_filters.FilterSet):
    process = django_filters.ChoiceFilter(field_name='process', lookup_expr='exact')
    search_term = django_filters.CharFilter(field_name='search_term', lookup_expr='icontains', label=_("Title contains"))
    region = django_filters.ChoiceFilter(field_name="section__division__branch__region", label=_("Region"), lookup_expr='exact')
    branch = django_filters.ChoiceFilter(field_name="section__division__branch", label=_("Branch / Sector"), lookup_expr='exact')
    has_process = django_filters.BooleanFilter(field_name='process', lookup_expr='isnull', label=_("Has process?"), exclude=True)


class DocumentFilter(django_filters.FilterSet):
    class Meta:
        model = models.Document
        fields = {
            'id': ['exact'],
            'document_type': ['exact'],
            'status': ['exact'],
            'translation_status': ['exact'],
            'process': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["id"] = django_filters.CharFilter(field_name='search_term', label=_("Title contains"),
                                                       lookup_expr='icontains', widget=forms.TextInput())
