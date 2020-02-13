from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django_filters.views import FilterView
from django.utils.translation import gettext_lazy as _

import json
import datetime

from . import forms
from . import models
from . import filters


class IndexView(TemplateView):
    template_name = 'whalesdb/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['section'] = [
            {
                'title': 'Entry Forms',
                'forms': [
                    {
                        'title': _("Station List"),
                        'url': "whalesdb:list_stn",
                        'icon': "img/whales/station.svg",
                    },
                    {
                        'title': _("Project List"),
                        'url': "whalesdb:list_prj",
                        'icon': "img/whales/project.svg",
                    },
                    {
                        'title': _("Mooring Setup List"),
                        'url': "whalesdb:list_mor",
                        'icon': "img/whales/mooring.svg",
                    },
                ]
           },
        ]

        return context


class CloserTemplateView(TemplateView):
    template_name = 'whalesdb/close_me.html'


class CloserNoRefreshTemplateView(TemplateView):
    template_name = 'whalesdb/close_me_no_refresh.html'


class CreateCommon(LoginRequiredMixin, CreateView):
    login_url = reverse("accounts:login")


class CreatePrj(CreateCommon):
    model = models.PrjProject
    form_class = forms.PrjForm

    template_name = 'whalesdb/_entry_form.html'


class CreateStn(CreateCommon):
    model = models.StnStation
    form_class = forms.StnForm

    template_name = 'whalesdb/_entry_form.html'


class CreateMor(CreateCommon):
    model = models.MorMooringSetup
    form_class = forms.MorForm

    template_name = 'whalesdb/_entry_form.html'


class DetailsPrj(DetailView):
    model = models.PrjProject


class DetailsStn(DetailView):
    model = models.StnStation


class DetailsMor(DetailView):
    model = models.MorMooringSetup


class ListCommon(FilterView):
    template_name = 'whalesdb/whale_filter.html'
    fields = []
    title = None

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs)

        context['fields'] = self.fields
        context['title'] = self.title

        return context


class ListPrj(ListCommon):
    model = models.PrjProject
    filterset_class = filters.PrjFilter
    title = _("Project List")
    fields = ['prj_name', 'prj_description']


class ListStn(ListCommon):
    model = models.StnStation
    filterset_class = filters.StnFilter
    fields = ['stn_name', 'stn_code', 'stn_revision']
    title = _("Station List")


class ListMor(ListCommon):
    model = models.MorMooringSetup
    filterset_class = filters.MorFilter
    fields = ['mor_name', 'mor_max_depth', 'more_notes']
    title = _("Mooring Setup List")
