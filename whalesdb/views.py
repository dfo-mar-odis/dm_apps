from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin

from django.urls import reverse, reverse_lazy
from django_filters.views import FilterView
from django.utils.translation import gettext_lazy as _


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


class CreateCommon(UserPassesTestMixin, CreateView):
    login_url = '/accounts/login_required/'
    title = None
    # create views are all intended to be pop out windows so upon success close the window
    success_url = reverse_lazy("whalesdb:close_me")
    template_name = 'whalesdb/_entry_form.html'

    def test_func(self):
        return self.request.user.groups.filter(name='whalesdb_admin').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.title:
            context["title"] = self.title

        return context


class CreatePrj(CreateCommon):
    model = models.PrjProject
    form_class = forms.PrjForm
    title = _("Create Project")


class CreateStn(CreateCommon):
    model = models.StnStation
    form_class = forms.StnForm
    title = _("Create Station")


class CreateMor(CreateCommon):
    model = models.MorMooringSetup
    form_class = forms.MorForm
    title = _("Create Mooring Setup")


class UpdateCommon(UserPassesTestMixin, UpdateView):
    login_url = '/accounts/login_required/'
    title = None
    # create views are all intended to be pop out windows so upon success close the window
    success_url = reverse_lazy("whalesdb:close_me")
    template_name = 'whalesdb/_entry_form.html'

    def test_func(self):
        return self.request.user.groups.filter(name='whalesdb_admin').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.title:
            context["title"] = self.title

        return context


class UpdateStn(UpdateCommon):
    model = models.StnStation
    form_class = forms.StnForm

    title = _("Update Station")


class UpdatePrj(UpdateCommon):
    model = models.PrjProject
    form_class = forms.PrjForm

    title = _("Update Project")


class UpdateMor(UpdateCommon):
    model = models.MorMooringSetup
    form_class = forms.MorForm

    title = _("Update Mooring Setup")


class DetailsCommon(DetailView):
    title = None
    template_name = "whalesdb/whales_detail.html"
    list_url = None
    update_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.title:
            context['title'] = self.title

        if self.fields:
            context['fields'] = self.fields

        if self.list_url:
            context['list_url'] = self.list_url

        if self.update_url:
            context['update_url'] = self.update_url

        return context


class DetailsPrj(DetailsCommon):
    model = models.PrjProject
    list_url = "whalesdb:list_prj"
    update_url = "whalesdb:update_prj"
    title = _("Project Details")
    fields = ['prj_name', 'prj_description', 'prj_url']


class DetailsStn(DetailsCommon):
    model = models.StnStation
    list_url = "whalesdb:list_stn"
    update_url = "whalesdb:update_stn"
    title = _("Station Details")
    template_name = 'whalesdb/stnstation_detail.html'
    fields = ['stn_name', 'stn_code', 'stn_revision', 'stn_planned_lat', 'stn_planned_lon',
              'stn_planned_depth', 'stn_notes']


class DetailsMor(DetailsCommon):
    model = models.MorMooringSetup
    list_url = "whalesdb:list_mor"
    update_url = "whalesdb:update_mor"
    title = _("Mooring Setup Details")
    template_name = "whalesdb/mormooringsetup_detail.html"
    fields = ['mor_name', 'mor_max_depth', 'mor_link_setup_image', 'mor_additional_equipment',
              'mor_general_moor_description', 'more_notes']


class ListCommon(FilterView):
    template_name = 'whalesdb/whale_filter.html'
    fields = []
    create_url = None
    details_url = None
    update_url = None
    title = None

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs)

        context['fields'] = self.fields

        if self.title:
            context['title'] = self.title

        if self.create_url:
            context['create_url'] = self.create_url

        if self.details_url:
            context['details_url'] = self.details_url

        if self.update_url:
            context['update_url'] = self.update_url

        context['auth'] = self.request.user.is_authenticated and \
                          self.request.user.groups.filter(name='whalesdb_admin').exists()

        return context


class ListPrj(ListCommon):
    model = models.PrjProject
    filterset_class = filters.PrjFilter
    create_url = "whalesdb:create_prj"
    details_url = "whalesdb:details_prj"
    update_url = "whalesdb:update_prj"
    title = _("Project List")
    fields = ['prj_name', 'prj_description']


class ListStn(ListCommon):
    model = models.StnStation
    filterset_class = filters.StnFilter
    create_url = "whalesdb:create_stn"
    details_url = "whalesdb:details_stn"
    update_url = "whalesdb:update_stn"
    fields = ['stn_name', 'stn_code', 'stn_revision']
    title = _("Station List")


class ListMor(ListCommon):
    model = models.MorMooringSetup
    filterset_class = filters.MorFilter
    create_url = "whalesdb:create_mor"
    details_url = "whalesdb:details_mor"
    update_url = "whalesdb:update_mor"
    fields = ['mor_name', 'mor_max_depth', 'more_notes']
    title = _("Mooring Setup List")
