from django.views.generic import TemplateView, FormView

from . import forms
from . import models

# Create your views here.
class IndexTemplateView(TemplateView):
    template_name = 'staff/index.html'


class CreatePlan(FormView):
    template_name = 'staff/create_plan.html'
    model = models.StaffingPlan
    login_url = '/accounts/login_required/'
    form_class = forms.NewStaffingForm

    fields = ['fiscal_year']