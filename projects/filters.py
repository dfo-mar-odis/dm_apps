from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from shared_models import models as shared_models
import django_filters
from . import views
from . import models

chosen_js = {"class": "chosen-select-contains"}


class ProjectFilter(django_filters.FilterSet):
    project_id = django_filters.NumberFilter(field_name='id', lookup_expr='exact')
    fiscal_year = django_filters.ChoiceFilter(field_name='year', lookup_expr='exact')
    project_title = django_filters.CharFilter(field_name='project_title', lookup_expr='icontains')
    tags = django_filters.ModelChoiceFilter(field_name='tags__name', lookup_expr='icontains', label=_("Tags / Keywords"),
                                            queryset=models.Tag.objects.all())
    region = django_filters.ChoiceFilter(field_name="section__division__branch__region", label=_("Region"), lookup_expr='exact')
    division = django_filters.ChoiceFilter(field_name='section__division', lookup_expr='exact', label=_("Division"))
    section = django_filters.ChoiceFilter(field_name='section', lookup_expr='exact', label=_("Section"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        region_choices = views.get_region_choices()
        division_choices = views.get_division_choices()
        section_choices = views.get_section_choices()
        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all() if fy.projects.count() > 0]
        yes_no_choices = [(True, "Yes"), (False, "No"), ]

        self.filters['fiscal_year'] = django_filters.ChoiceFilter(field_name='year', lookup_expr='exact', choices=fy_choices,
                                                                  label=_("Fiscal year"))
        self.filters['section'] = django_filters.ChoiceFilter(field_name="section", label=_("Section"),
                                                              lookup_expr='exact', choices=section_choices)
        self.filters['region'] = django_filters.ChoiceFilter(field_name="section__division__branch__region", label=_("Region"),
                                                             lookup_expr='exact', choices=region_choices)
        self.filters['division'] = django_filters.ChoiceFilter(field_name="section__division", label=_("Division"),
                                                               lookup_expr='exact', choices=division_choices)
        # self.filters['division'] = django_filters.ChoiceFilter(field_name='section__division', lookup_expr='exact', choices=div_choices)

        try:
            # if there is a filter on region, filter the division and section filter accordingly
            if self.data["region"] != "":
                my_region_id = int(self.data["region"])
                division_choices = [my_set for my_set in views.get_division_choices() if
                                    shared_models.Division.objects.get(pk=my_set[0]).branch.region_id == my_region_id]
                self.filters['division'] = django_filters.ChoiceFilter(field_name="section__division", label=_("Division"),
                                                                       lookup_expr='exact', choices=division_choices)

                section_choices = [my_set for my_set in views.get_section_choices() if
                                   shared_models.Section.objects.get(pk=my_set[0]).division.branch.region_id == my_region_id]
                self.filters['section'] = django_filters.ChoiceFilter(field_name="section", label=_("Section"),
                                                                      lookup_expr='exact', choices=section_choices)

            # if there is a filter on division, filter the section filter accordingly
            if self.data["division"] != "":
                my_division_id = int(self.data["division"])

                section_choices = [my_set for my_set in views.get_section_choices() if
                                   shared_models.Section.objects.get(pk=my_set[0]).division_id == my_division_id]
                self.filters['section'] = django_filters.ChoiceFilter(field_name="section", label=_("Section"),
                                                                      lookup_expr='exact', choices=section_choices)

        except KeyError:
            print('no data in filter')


class StaffFilter(django_filters.FilterSet):
    fiscal_year = django_filters.ChoiceFilter(field_name='project__year', lookup_expr='exact')
    region = django_filters.ChoiceFilter(field_name="project__section__division__branch__region", label=_("Region"), lookup_expr='exact')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        region_choices = views.get_region_choices()
        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all() if fy.projects.count() > 0]
        yes_no_choices = [(True, "Yes"), (False, "No"), ]
        self.filters['fiscal_year'] = django_filters.ChoiceFilter(field_name='project__year', lookup_expr='exact', choices=fy_choices)
        self.filters['region'] = django_filters.ChoiceFilter(field_name="project__section__division__branch__region", label=_("Region"),
                                                             lookup_expr='exact', choices=region_choices)
        self.filters['project__submitted'].label = "Has the project been submitted?"

    class Meta:
        model = models.Staff
        fields = {
            'employee_type': ['exact'],
            'lead': ['exact'],
            'project__submitted': ['exact'],
        }


class AdminProjectProgramFilter(django_filters.FilterSet):
    # fiscal_year = django_filters.ChoiceFilter(field_name='_year', lookup_expr='exact')
    # region = django_filters.ChoiceFilter(field_name="section__division__branch__region", label=_("Region"), lookup_expr='exact')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        region_choices = views.get_region_choices()
        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all() if fy.projects.count() > 0]
        yes_no_choices = [(True, "Yes"), (False, "No"), ]
        self.filters['year'] = django_filters.ChoiceFilter(field_name='year', lookup_expr='exact', choices=fy_choices)
        self.filters['section__division__branch__region'] = django_filters.ChoiceFilter(field_name="section__division__branch__region",
                                                                                        label=_("Region"),
                                                                                        lookup_expr='exact', choices=region_choices)
        self.filters['submitted'].label = "Submitted?"
        self.filters['approved'].label = "Approved by section head?"

    class Meta:
        model = models.Project
        fields = {
            'year': ['exact'],
            'section__division__branch__region': ['exact'],
            'project_title': ['icontains'],
            'submitted': ['exact'],
            'approved': ['exact'],
        }


class AdminSubmittedUnapprovedFilter(django_filters.FilterSet):
    # fiscal_year = django_filters.ChoiceFilter(field_name='_year', lookup_expr='exact')
    # region = django_filters.ChoiceFilter(field_name="section__division__branch__region", label=_("Region"), lookup_expr='exact')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        region_choices = views.get_region_choices()
        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all() if fy.projects.count() > 0]
        yes_no_choices = [(True, "Yes"), (False, "No"), ]
        self.filters['year'] = django_filters.ChoiceFilter(field_name='year', lookup_expr='exact', choices=fy_choices)
        self.filters['section__division__branch__region'] = django_filters.ChoiceFilter(field_name="section__division__branch__region",
                                                                                        label=_("Region"),
                                                                                        lookup_expr='exact', choices=region_choices)

    class Meta:
        model = models.Project
        fields = {
            'year': ['exact'],
            'section__division__branch__region': ['exact'],
        }


class MySectionFilter(django_filters.FilterSet):
    fiscal_year = django_filters.ChoiceFilter(field_name='year', lookup_expr='exact')
    project_title = django_filters.CharFilter(field_name='project_title', lookup_expr='icontains')
    staff = django_filters.ChoiceFilter(field_name='staff_members__user', lookup_expr='exact', label="Staff member")
    submitted = django_filters.ChoiceFilter(field_name='submitted', lookup_expr='exact', label="Submitted?")

    # approved = django_filters.ChoiceFilter(field_name='approved', lookup_expr='exact', label="Approved by me?")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all() if fy.projects.count() > 0]
        user_choices = [(u.id, "{}, {}".format(u.last_name, u.first_name)) for u in User.objects.all().order_by("last_name", "first_name")]
        yes_no_choices = [(True, "Yes"), (False, "No"), ]

        self.filters['fiscal_year'] = django_filters.ChoiceFilter(field_name='year', lookup_expr='exact', choices=fy_choices)
        self.filters['staff'] = django_filters.ChoiceFilter(field_name='staff_members__user', lookup_expr='exact', choices=user_choices,
                                                            widget=forms.Select(attrs=chosen_js))
        self.filters['submitted'] = django_filters.ChoiceFilter(field_name='submitted', lookup_expr='exact', choices=yes_no_choices)

        if "my-section" in str(kwargs["request"]):
            self.filters['approved'] = django_filters.ChoiceFilter(field_name='approved', lookup_expr='exact',
                                                                   label="Approved by me?", choices=yes_no_choices)
        elif "my-division" in str(kwargs["request"]):
            self.filters['sh_approved'] = django_filters.ChoiceFilter(field_name='approved', lookup_expr='exact',
                                                                      label="Approved by section head?", choices=yes_no_choices)
            self.filters['approved'] = django_filters.ChoiceFilter(field_name='manager_approved', lookup_expr='exact',
                                                                   label="Approved by me?", choices=yes_no_choices)
        elif "my-branch" in str(kwargs["request"]):
            self.filters['dm_approved'] = django_filters.ChoiceFilter(field_name='manager_approved', lookup_expr='exact',
                                                                      label="Approved by division manager?", choices=yes_no_choices)
            self.filters['approved'] = django_filters.ChoiceFilter(field_name='rds_approved', lookup_expr='exact',
                                                                   label="Approved by me?", choices=yes_no_choices)


class SectionFilter(django_filters.FilterSet):
    class Meta:
        model = models.Project
        fields = {
            'year': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all() if fy.projects.count() > 0]
        self.filters['year'] = django_filters.ChoiceFilter(field_name='year', lookup_expr='exact', choices=fy_choices,
                                                           label=_("Please select a fiscal year:"))


class MyProjectFilter(django_filters.FilterSet):
    class Meta:
        model = models.Project
        fields = {
            'year': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all() if fy.projects.count() > 0]
        self.filters['year'] = django_filters.ChoiceFilter(field_name='year', lookup_expr='exact', choices=fy_choices,
                                                           label=_("Please select a fiscal year:"))


class FunctionalGroupFilter(django_filters.FilterSet):
    class Meta:
        model = models.FunctionalGroup
        fields = {
            'name': ['exact'],
            'theme': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all() if fy.projects.count() > 0]
        self.filters['name'] = django_filters.CharFilter(field_name='search_term', label=_("Name"), lookup_expr='icontains',
                                            widget=forms.TextInput())