import django_filters
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from shared_models.models import FiscalYear
from shared_models.utils import get_labels
from . import models


class SpeciesFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(field_name='search_term', label=_("Search term"), lookup_expr='icontains',
                                            widget=forms.TextInput())


class CollectionFilter(django_filters.FilterSet):
    class Meta:
        model = models.Collection
        fields = {
            'fiscal_year': ['exact'],
            'contact_users': ['exact'],
            'region': ['exact'],
            'tags': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        labels = get_labels(models.Collection)
        user_choices = [(u.id, u.get_full_name()) for u in User.objects.filter(collection__isnull=False).distinct()]
        fy_choices = [(obj.id, str(obj)) for obj in FiscalYear.objects.filter(collections__isnull=False).distinct()]
        self.filters["contact_users"] = django_filters.ChoiceFilter(field_name="contact_users", choices=user_choices, label=labels["contact_users"])
        self.filters["fiscal_year"] = django_filters.ChoiceFilter(field_name="fiscal_year", choices=fy_choices, label=labels["fiscal_year"])


class FiltrationBatchFilter(django_filters.FilterSet):
    class Meta:
        model = models.FiltrationBatch
        fields = {
            'datetime': ['exact'],
        }


class ExtractionBatchFilter(django_filters.FilterSet):
    class Meta:
        model = models.ExtractionBatch
        fields = {
            'datetime': ['exact'],
        }


class PCRBatchFilter(django_filters.FilterSet):
    class Meta:
        model = models.PCRBatch
        fields = {
            'datetime': ['exact'],
        }
