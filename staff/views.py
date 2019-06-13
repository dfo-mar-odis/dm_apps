from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import UpdateView, CreateView
from django_filters.views import FilterView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from . import forms
from . import models
from . import filters


# Create your views here.
class IndexTemplateView(FilterView):
    filterset_class = filters.StaffingPlanFilter
    template_name = 'staff/index.html'


class CreatePlan(LoginRequiredMixin, CreateView):
    model = models.StaffingPlan
    login_url = '/accounts/login_required/'
    form_class = forms.NewStaffingForm
    success_url = reverse_lazy("staff:index")

    def get_initial(self):
        ret = {'last_modified_by': self.request.user}

        return ret


class UpdatePlan(LoginRequiredMixin, UpdateView):
    model = models.StaffingPlan
    login_url = '/accounts/login_required/'
    form_class = forms.NewStaffingForm
    success_url = reverse_lazy("staff:index")

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