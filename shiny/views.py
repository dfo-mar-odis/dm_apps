from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, TextField
from django.db.models.functions import Concat
from django.shortcuts import render

# Create your views here.
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext as _, gettext_lazy
from django.views.generic import TemplateView, ListView, DeleteView, CreateView, UpdateView

from shared_models.views import CommonFilterView, CommonUpdateView, CommonCreateView, CommonDeleteView
from . import models
from . import forms
from . import filters


class IndexTemplateView(CommonFilterView):
    template_name = 'shiny/index.html'
    model = models.App
    filterset_class = filters.AppFilter
    h1 = gettext_lazy("DFO Shiny Apps Repository")
    new_object_url_name = "shiny:create"
    # container_class = "container-fluid"

    field_list = [
        {"name": 'thumbnail| ', "class": "", "width": "150px"},
        {"name": 'ttitle|{}'.format(_("title")), "class": "", "width": ""},
        {"name": "tdescription|{}".format(_("description")), "class": "", "width": ""},
        {"name": 'owner', "class": "", "width": "150px"},
        {"name": 'last_modified', "class": "", "width": "100px"},
        {"name": "github_url|{}".format("link to github"), "class": "center-col", "width": "100px"},
    ]

    def get_queryset(self):
        return models.App.objects.all().annotate(search_term=Concat(
            'title_en',
            Value(" "),
            'title_fr',
            Value(" "),
            'description_en',
            Value(" "),
            'description_fr',
            output_field=TextField()
        ))


class AppUpdateView(LoginRequiredMixin, CommonUpdateView):
    model = models.App
    form_class = forms.AppForm
    success_url = reverse_lazy('shiny:index')
    template_name = 'shared_models/generic_form.html'
    home_url_name = "shiny:index"
    is_multipart_form_data = True


class AppCreateView(LoginRequiredMixin, CommonCreateView):
    model = models.App
    form_class = forms.AppForm
    success_url = reverse_lazy('shiny:index')
    template_name = 'shared_models/generic_form.html'
    home_url_name = "shiny:index"
    is_multipart_form_data = True

    def get_initial(self):
        return {
            "owner": self.request.user
        }


class AppDeleteView(LoginRequiredMixin, CommonDeleteView):
    model = models.App
    success_url = reverse_lazy('shiny:index')
    template_name = 'shared_models/generic_confirm_delete.html'
    home_url_name = "shiny:index"
