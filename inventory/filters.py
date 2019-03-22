# from accounts import models as account_models
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext as _
from . import models
import django_filters
from shared_models import models as shared_models


class ResourceFilter(django_filters.FilterSet):
    STATUS_CHOICES = [(s.id, str(s)) for s in models.Status.objects.all()]
    SECTION_CHOICES = [(s.id, s.full_name) for s in
                       shared_models.Section.objects.all().order_by("division__branch__region", "division__branch", "division", "name")]

    search_term = django_filters.CharFilter(field_name='search_term', label=_("Search term"), lookup_expr='icontains',
                                            widget=forms.TextInput())
    region = django_filters.ModelChoiceFilter(field_name="section__division__branch__region", label=_("Region"), lookup_expr='exact',
                                              queryset=shared_models.Region.objects.all())
    section = django_filters.ModelChoiceFilter(field_name="section", label=_("Section"), lookup_expr='exact',
                                               queryset=shared_models.Section.objects.all())
    person = django_filters.ModelChoiceFilter(field_name="people", label=_("Person"), lookup_expr='exact',
                                              queryset=models.Person.objects.all())
    status = django_filters.ChoiceFilter(field_name="status", label=_("Status"), lookup_expr='exact', choices=STATUS_CHOICES)
    percent_complete = django_filters.NumberFilter(field_name="completedness_rating", label=_("Percent complete"), lookup_expr='gte',
                                                   widget=forms.NumberInput(attrs={"placeholder": "between 0 and 1"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if there is a filter on section, filter the people filter accordingly
        try:
            if self.data["section"] != "":
                self.filters["person"].queryset = models.Person.objects.filter(resource__section_id=self.data["section"]).distinct()
            elif self.data["region"] != "":
                self.filters["section"].queryset = shared_models.Section.objects.filter(division__branch__region_id=self.data["region"]).distinct()
                self.filters["person"].queryset = models.Person.objects.filter(
                    resource__section__division__branch__region=self.data["region"]).distinct()
        except KeyError:
            print('no data in filter')


class PersonFilter(django_filters.FilterSet):
    class Meta:
        model = models.Person
        fields = {
            'full_name': ['icontains'],
        }


class KeywordFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(label="Keyword Search Term", lookup_expr='icontains')


class CitationFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(label="Citation Search Term", lookup_expr='icontains')
