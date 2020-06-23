import django_filters
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from shared_models import models as shared_models
from . import models
from . import forms as ticket_forms

try:
    from dm_apps import my_conf as local_conf
except (ModuleNotFoundError, ImportError):
    from dm_apps import default_conf as local_conf

chosen_js = {"class": "chosen-select-contains"}


class TicketFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(field_name='search_term', label="Search term (Id, title, etc.):",
                                            lookup_expr='icontains', widget=forms.TextInput())
    app = django_filters.ChoiceFilter(
        field_name="app",
        widget=forms.Select(attrs=chosen_js),
    )
    status = django_filters.ModelChoiceFilter(
        field_name="status",
        queryset=models.Status.objects.all(),
        widget=forms.Select(attrs=chosen_js),
    )
    section = django_filters.ChoiceFilter(field_name="section")
    dm_assigned = django_filters.ChoiceFilter(field_name="dm_assigned")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # choices for app
        APP_CHOICES = [(app_key, local_conf.APP_DICT[app_key]) for app_key in local_conf.APP_DICT]
        APP_CHOICES.insert(0, ("esee", "ESEE (not part of site)"))
        APP_CHOICES.insert(0, ("plankton", "Plankton Net (not part of site)"))
        APP_CHOICES.insert(0, ("tickets", "Data Management Tickets"))
        APP_CHOICES.sort()
        APP_CHOICES.insert(0, ("general", "n/a"))
        self.filters['app'] = django_filters.ChoiceFilter(
            field_name="app",
            choices=APP_CHOICES,
            widget=forms.Select(attrs=chosen_js),
        )

        section_choices = [(s.id, s.shortish_name) for s in shared_models.Section.objects.all().order_by(
            "division__branch__region", "division__branch", "division", "name")]
        staff_choices = [(dm.id, "{} {}".format(dm.first_name, dm.last_name)) for dm in User.objects.filter(is_staff=True)]
        self.filters['section'] = django_filters.ChoiceFilter(
            field_name="section",
            choices=section_choices,
            widget=forms.Select(attrs=chosen_js),
        )
        self.filters['dm_assigned'] = django_filters.ChoiceFilter(
            field_name="dm_assigned",
            choices=staff_choices,
            label="Ticket assigned to",
            widget=forms.Select(attrs=chosen_js),
        )


class MyTicketFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(field_name='search_term', label="Search term (Id, title, etc.):",
                                            lookup_expr='icontains', widget=forms.TextInput())
    app = django_filters.ChoiceFilter(
        field_name="app",
        widget=forms.Select(attrs={"class": "chosen-select-contains"}),
    )

    status = django_filters.ModelChoiceFilter(
        field_name="status",
        queryset=models.Status.objects.all(),
        widget=forms.Select(attrs={"class": "chosen-select-contains"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        APP_CHOICES = [(app_key, local_conf.APP_DICT[app_key]) for app_key in local_conf.APP_DICT]
        APP_CHOICES.insert(0, ("esee", "ESEE (not part of site)"))
        APP_CHOICES.insert(0, ("plankton", "Plankton Net (not part of site)"))
        APP_CHOICES.insert(0, ("tickets", "Data Management Tickets"))
        APP_CHOICES.sort()
        APP_CHOICES.insert(0, ("general", "n/a"))
        self.filters['app'] = django_filters.ChoiceFilter(
            field_name="app",
            choices=APP_CHOICES,
            widget=forms.Select(attrs=chosen_js),
        )


class FiscalFilter(django_filters.FilterSet):
    fiscal_year = django_filters.ChoiceFilter(field_name='fiscal_year', lookup_expr='exact')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all()]
        self.filters['fiscal_year'] = django_filters.ChoiceFilter(field_name='fiscal_year', lookup_expr='exact',
                                                                  choices=fy_choices)
