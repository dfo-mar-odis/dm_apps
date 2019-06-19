import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, CreateView, DetailView
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from django.utils.translation import gettext as _

from django.db.models import Q
from shared_models import models as shared_models

from . import forms
from . import models
from . import filters


plan_field_list = [
    "fiscal_year", "section", "name", "employee_class_level", "responsibility_center", "staffing_plan_status",
    "funding_type", "work_location", "position_staffing_option", "position_tenure", "position_security",
    "position_linguistic", "position_employment_equity", "position_number", "position_title", "is_key_position",
    "employee_last_name", "employee_first_name", "reports_to", "estimated_start_date", "start_date", "end_date",
    "duration_temporary_coverage", "potential_rollover_date", "allocation", "rd_approval_number",
    "description", "date_last_modified", "last_modified_by",
]


def get_section_choices(all=False, full_name=True):
    if full_name:
        my_attr = "full_name"
    else:
        my_attr = _("name")

    return [(s.id, getattr(s, my_attr)) for s in
            shared_models.Section.objects.all().order_by("division__branch__region", "division__branch", "division",
            "name") if s.projects.count() > 0] if not all else [(s.id, getattr(s, my_attr)) for s in
                                                                shared_models.Section.objects.filter(
                  division__branch__name__icontains="science").order_by(
                  "division__branch__region",
                  "division__branch",
                  "division",
                  "name"
            )]


def get_division_choices(all=False):
    if all:
        division_list = set([shared_models.Section.objects.get(pk=s[0]).division for s in get_section_choices(all=True)])
    else:
        division_list = set([shared_models.Section.objects.get(pk=s[0]).division for s in get_section_choices()])
    q_objects = Q()  # Create an empty Q object to start with
    for d in division_list:
        q_objects |= Q(id=d.id)  # 'or' the Q objects together

    return [(d.id, str(d)) for d in
            shared_models.Division.objects.filter(q_objects).order_by(
                "branch__region",
                "name"
            )]


def get_region_choices(all=False):
    if all:
        region_list = set([shared_models.Division.objects.get(pk=d[0]).branch.region for d in get_division_choices(all=True)])
    else:
        region_list = set([shared_models.Division.objects.get(pk=d[0]).branch.region for d in get_division_choices()])
    q_objects = Q()  # Create an empty Q object to start with
    for r in region_list:
        q_objects |= Q(id=r.id)  # 'or' the Q objects together

    return [(r.id, str(r)) for r in
            shared_models.Region.objects.filter(q_objects).order_by(
                "name",
            )]


# Create your views here.
class IndexTemplateView(FilterView):
    filterset_class = filters.StaffingPlanFilter
    template_name = 'staff/index.html'


class CreateFunding(LoginRequiredMixin, CreateView):
    model = models.StaffingPlanFunding
    form_class = forms.FundingForm
    success_url = reverse_lazy("staff:index")

    def get_initial(self):
        ret = {'last_modified_by': self.request.user}

        if self.kwargs['pk'] and self.kwargs['pk'] != 0:
            ret['object'] = models.StaffingPlan.objects.get(id=self.kwargs['pk'])

        return ret

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context["min_allotment"] = 0
        context["max_allotment"] = 10
        return context


class DetailPlan(LoginRequiredMixin, DetailView):
    model = models.StaffingPlan
    login_url = '/accounts/login_required/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = plan_field_list

        print(context)

        return context


class CreatePlan(LoginRequiredMixin, CreateView):
    model = models.StaffingPlan
    login_url = '/accounts/login_required/'
    form_class = forms.NewStaffingForm

    def get_initial(self):
        ret = {'last_modified_by': self.request.user}

        return ret

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['help_text_dict'] = help_text_dict

        # here are the option objects we want to send in through context
        # only from the science branches of each region

        division_dict = {}
        for d in get_division_choices(all=True):
            my_division = shared_models.Division.objects.get(pk=d[0])
            division_dict[my_division.id] = {}
            division_dict[my_division.id]["display"] = "{} - {}".format(
                getattr(my_division.branch, _("name")),
                getattr(my_division, _("name")),
            )
            division_dict[my_division.id]["region_id"] = my_division.branch.region_id

        section_dict = {}
        for s in get_section_choices(all=True):
            my_section = shared_models.Section.objects.get(pk=s[0])
            section_dict[my_section.id] = {}
            section_dict[my_section.id]["display"] = str(my_section)
            section_dict[my_section.id]["division_id"] = my_section.division_id
        context['division_json'] = json.dumps(division_dict)
        context['section_json'] = json.dumps(section_dict)

        return context

    def form_valid(self, form):
        object = form.save()

        return HttpResponseRedirect(reverse_lazy("staff:detail_plan", kwargs={"pk": object.id}))


class UpdatePlan(LoginRequiredMixin, UpdateView):
    model = models.StaffingPlan
    login_url = '/accounts/login_required/'
    form_class = forms.NewStaffingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        if self.kwargs['pk'] and self.kwargs['pk'] != 0:
            context['object'] = models.StaffingPlan.objects.get(id=self.kwargs['pk'])

        return context

    def get_initial(self):
        ret = {'last_modified_by': self.request.user}

        if self.kwargs['pk'] and self.kwargs['pk'] != 0:
            ret['object'] = models.StaffingPlan.objects.get(id=self.kwargs['pk'])

        return ret

    def form_valid(self, form):
        object = form.save()

        return HttpResponseRedirect(reverse_lazy("staff:detail_plan", kwargs={"pk": object.id}))
