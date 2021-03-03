# from accounts import models as account_models
# from  import gettext as _
import django_filters
from django import forms
from django.utils.translation import gettext as _

chosen_js = {"class": "chosen-select-contains"}


class UserFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(field_name='search_term', label=_("Name contains"), lookup_expr='icontains',
                                            widget=forms.TextInput())
