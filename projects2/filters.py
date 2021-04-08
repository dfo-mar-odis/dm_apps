import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from shared_models import models as shared_models
from . import models
from . import utils

chosen_js = {"class": "chosen-select-contains"}


class StaffFilter(django_filters.FilterSet):
    fiscal_year = django_filters.ChoiceFilter(field_name='project_year__fiscal_year', lookup_expr='exact')
    region = django_filters.ChoiceFilter(field_name="project_year__project__section__division__branch__region", label=_("Region"), lookup_expr='exact')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        region_choices = utils.get_region_choices()
        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all() if fy.projectyear_set.count() > 0]
        yes_no_choices = [(True, "Yes"), (False, "No"), ]
        self.filters['fiscal_year'] = django_filters.ChoiceFilter(field_name='project_year__fiscal_year', lookup_expr='exact', choices=fy_choices)
        self.filters['region'] = django_filters.ChoiceFilter(field_name="project_year__project__section__division__branch__region", label=_("Region"),
                                                             lookup_expr='exact', choices=region_choices)
        # self.filters['project_year__submitted'].label = "Has the project been submitted?"

    class Meta:
        model = models.Staff
        fields = {
            # 'employee_type': ['exact'],
            'is_lead': ['exact'],
        }


class FunctionalGroupFilter(django_filters.FilterSet):
    class Meta:
        model = models.FunctionalGroup
        fields = {
            'name': ['exact'],
            'theme': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all() if fy.projectyear_set.exists()]
        self.filters['name'] = django_filters.CharFilter(field_name='search_term', label=_("Name"), lookup_expr='icontains',
                                                         widget=forms.TextInput())


class UserFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(field_name='search_term', label=_("Name contains"), lookup_expr='icontains',
                                            widget=forms.TextInput())


class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = models.Project
        fields = {
            'fiscal_years': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get("queryset"):
            fy_ids = [py.fiscal_year_id for py in models.ProjectYear.objects.filter(project__in=kwargs.get("queryset"))]
            fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.filter(id__in=fy_ids)]
        else:
            fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all() if fy.projectyear_set.exists()]
        self.filters['fiscal_years'] = django_filters.ChoiceFilter(field_name='fiscal_years', label=_("Fiscal year"), widget=forms.Select(), choices=fy_choices)
