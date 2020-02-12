import django_filters
from django import forms


class ItemsFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(field_name='search_term', label="Items (any part of name...)",
                                            lookup_expr='icontains', widget=forms.TextInput())
