from django.utils.translation import gettext as _

from lib.functions.custom_functions import listrify
from shared_models import models as shared_models
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db.models import Count, TextField
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView, TemplateView, FormView
from django_filters.views import FilterView
from . import models
from . import forms
from . import filters
from . import reports

class CloserTemplateView(TemplateView):
    template_name = 'vault/close_me.html'


def in_vault_group(user):
    if user:
        return True


class VaultAccessRequired(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/accounts/login_required/'

    def test_func(self):
        return in_vault_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_vault_group, login_url='/accounts/denied/')
def index(request):
    return render(request, 'vault/index.html')

# #
# # # SPECIES #
# # ###########
# #
#

class SpeciesListView(VaultAccessRequired, FilterView):
    template_name = "vault/species_list.html"
    filterset_class = filters.SpeciesFilter
    queryset = models.Species.objects.annotate(
        search_term=Concat('code', 'english_name', 'french_name', 'latin_name', 'id', output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.Species.objects.first()
        context["field_list"] = [
            'id',
            'code',
            'french_name',
            'english_name',
            'latin_name',
            'vor_code',
            'quebec_code',
            'aphia_id',
        ]
        return context

#
class SpeciesDetailView(VaultAccessRequired, DetailView):
    model = models.Species

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'id',
            'code',
            'english_name',
            'french_name',
            'latin_name',
            'vor_code',
            'quebec_code',
            'aphia_id',
        ]
        return context

#
class SpeciesUpdateView(VaultAccessRequired, UpdateView):
    model = models.Species
    form_class = forms.SpeciesForm

    def form_valid(self, form):
        messages.success(self.request, _("Species record successfully updated for : {}".format(self.object)))
        return super().form_valid(form)


class SpeciesCreateView(VaultAccessRequired, CreateView):
    model = models.Species
    form_class = forms.SpeciesForm

    def form_valid(self, form):
        messages.success(self.request, _("Species record successfully created for : {}".format(self.object)))
        return super().form_valid(form)

class SpeciesDeleteView(VaultAccessRequired, DeleteView):
    model = models.Species
    permission_required = "__all__"
    success_url = reverse_lazy('vault:species_list')
    success_message = 'The species was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

#
#
# #
# # # OBSERVATIONPLATFORM #
# # ###########
# #
#
class ObservationPlatformListView(VaultAccessRequired, FilterView):
    template_name = "vault/observationplatform_list.html"
    filterset_class = filters.ObservationPlatformFilter
    queryset = models.ObservationPlatform.objects.annotate(
        search_term=Concat('authority', 'owner', 'make_model', 'name', 'longname', 'id', output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.ObservationPlatform.objects.first()
        context["field_list"] = [
            'id',
            'observation_platform_type',
            'authority',
            'make_model',
            'owner',
            'name',
            'longname',
            'foldername|folder name'
        ]
        return context

#
class ObservationPlatformDetailView(VaultAccessRequired, DetailView):
    model = models.ObservationPlatform

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'id',
            'observation_platform_type',
            'authority',
            'make_model',
            'owner',
            'name',
            'longname',
        ]
        return context

#
class ObservationPlatformUpdateView(VaultAccessRequired, UpdateView):
    model = models.ObservationPlatform
    form_class = forms.ObservationPlatformForm

    def form_valid(self, form):
        messages.success(self.request, _("ObservationPlatform record successfully updated for : {}".format(self.object)))
        return super().form_valid(form)


class ObservationPlatformCreateView(VaultAccessRequired, CreateView):
    model = models.ObservationPlatform
    form_class = forms.ObservationPlatformForm

    def form_valid(self, form):
        messages.success(self.request, _("ObservationPlatform record successfully created for : {}".format(self.object)))
        return super().form_valid(form)


class ObservationPlatformDeleteView(VaultAccessRequired, DeleteView):
    model = models.ObservationPlatform
    permission_required = "__all__"
    success_url = reverse_lazy('vault:observationplatform_list')
    success_message = 'The observation plaform was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

# #
# # # INSTRUMENTS #
# # ###########
# #
#
class InstrumentListView(VaultAccessRequired, FilterView):
    template_name = "vault/instrument_list.html"
    filterset_class = filters.InstrumentFilter
    queryset = models.Instrument.objects.annotate(
        search_term=Concat('id', 'name', 'nom', output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.Instrument.objects.first()
        context["field_list"] = [
            'id',
            'instrument_type',
            'name',
            'nom',
            #'metadata',

        ]
        return context

#
class InstrumentDetailView(VaultAccessRequired, DetailView):
    model = models.Instrument

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'id',
            'name',
            'nom',
            # 'metadata',
            'instrument_type',

        ]
        return context

#
class InstrumentUpdateView(VaultAccessRequired, UpdateView):
    model = models.Instrument
    form_class = forms.InstrumentForm

    def form_valid(self, form):
        messages.success(self.request, _("Instrument record successfully updated for : {}".format(self.object)))
        return super().form_valid(form)


class InstrumentCreateView(VaultAccessRequired, CreateView):
    model = models.Instrument
    form_class = forms.InstrumentForm

    def form_valid(self, form):
        messages.success(self.request, _("Instrument record successfully created for : {}".format(self.object)))
        return super().form_valid(form)

class InstrumentDeleteView(VaultAccessRequired, DeleteView):
    model = models.Instrument
    permission_required = "__all__"
    success_url = reverse_lazy('vault:instrument_list')
    success_message = 'The instrument was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)