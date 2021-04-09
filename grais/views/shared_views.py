import os

from django.contrib import messages
from django.db.models import Value, TextField
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.views.generic import FormView

from grais import filters
from grais import forms
from grais import models
from grais import reports
from grais.mixins import GraisAccessRequiredMixin, GraisAdminRequiredMixin, GraisCRUDRequiredMixin
from grais.utils import is_grais_admin
from shared_models.views import CommonFormsetView, CommonHardDeleteView, CommonTemplateView, CommonFilterView, CommonUpdateView, CommonCreateView, \
    CommonDetailView, CommonDeleteView


class IndexView(GraisAccessRequiredMixin, CommonTemplateView):
    template_name = 'grais/index.html'
    h1 = "home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_admin"] = is_grais_admin(self.request.user)
        return context


# SETTINGS
class ProbeFormsetView(GraisAdminRequiredMixin, CommonFormsetView):
    template_name = 'shared_models/generic_formset.html'
    h1 = "Manage Probes"
    queryset = models.Probe.objects.all()
    formset_class = forms.ProbeFormset
    success_url_name = "grais:manage_probes"
    home_url_name = "grais:index"
    delete_url_name = "grais:delete_probe"


class ProbeHardDeleteView(GraisAdminRequiredMixin, CommonHardDeleteView):
    model = models.Probe
    success_url = reverse_lazy("grais:manage_probes")


class SamplerFormsetView(GraisAdminRequiredMixin, CommonFormsetView):
    template_name = 'grais/formset.html'
    h1 = "Manage Samplers"
    queryset = models.Sampler.objects.all()
    formset_class = forms.SamplerFormset
    success_url_name = "grais:manage_samplers"
    home_url_name = "grais:index"
    delete_url_name = "grais:delete_sampler"


class SamplerHardDeleteView(GraisAdminRequiredMixin, CommonHardDeleteView):
    model = models.Sampler
    success_url = reverse_lazy("grais:manage_samplers")


# SPECIES #
###########

class SpeciesListView(GraisAccessRequiredMixin, CommonFilterView):
    template_name = 'grais/list.html'
    filterset_class = filters.SpeciesFilter
    home_url_name = "grais:index"
    new_object_url = reverse_lazy("grais:species_new")
    row_object_url_name = row_ = "grais:species_detail"
    container_class = "container-fluid"

    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'tname|{}'.format("common name"), "class": "", "width": ""},
        {"name": 'formatted_scientific|{}'.format("scientific name"), "class": "", "width": ""},
        {"name": 'abbrev', "class": "", "width": ""},
        {"name": 'tsn|ITIS TSN', "class": "", "width": ""},
        {"name": 'aphia_id|WoRMS Aphia ID', "class": "", "width": ""},
        {"name": 'color_morph', "class": "", "width": ""},
        {"name": 'invasive', "class": "", "width": ""},
        {"name": 'Has occurred in db?', "class": "", "width": ""},
    ]

    def get_queryset(self):
        return models.Species.objects.annotate(
            search_term=Concat('common_name', Value(" "), 'common_name_fra', Value(" "), 'scientific_name', output_field=TextField()))


class SpeciesUpdateView(GraisAdminRequiredMixin, CommonUpdateView):
    model = models.Species
    form_class = forms.SpeciesForm
    template_name = 'grais/form.html'
    home_url_name = "grais:index"
    grandparent_crumb = {"title": gettext_lazy("Species"), "url": reverse_lazy("grais:species_list")}

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse_lazy("grais:species_detail", args=[self.get_object().id])}

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.updated_by = self.request.user
        return super().form_valid(form)


class SpeciesCreateView(GraisCRUDRequiredMixin, CommonCreateView):
    model = models.Species
    form_class = forms.SpeciesForm
    success_url = reverse_lazy('grais:species_list')
    template_name = 'grais/form.html'
    home_url_name = "grais:index"
    parent_crumb = {"title": gettext_lazy("Species"), "url": reverse_lazy("grais:species_list")}

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.updated_by = self.request.user
        return super().form_valid(form)


class SpeciesDetailView(GraisAccessRequiredMixin, CommonDetailView):
    model = models.Species
    template_name = 'grais/biofouling/species_detail.html'
    home_url_name = "grais:index"
    parent_crumb = {"title": gettext_lazy("Species"), "url": reverse_lazy("grais:species_list")}
    field_list = [
        'id',
        'common_name',
        'common_name_fra',
        'scientific_name',
        'abbrev',
        'tsn',
        'aphia',
        'epibiont_type',
        'color_morph',
        'invasive',
        'database occurrences',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SpeciesDeleteView(GraisAdminRequiredMixin, CommonDeleteView):
    model = models.Species
    success_url = reverse_lazy('grais:species_list')
    success_message = 'The functional group was successfully deleted!'
    template_name = 'grais/confirm_delete.html'


# REPORTS #
###########

class ReportSearchFormView(GraisAccessRequiredMixin, FormView):
    template_name = 'grais/reports.html'
    form_class = forms.ReportSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        species_list = str(form.cleaned_data["species"]).replace("[", "").replace("]", "").replace(" ", "").replace("'", "")
        report = int(form.cleaned_data["report"])
        year = form.cleaned_data["year"] if form.cleaned_data["year"] else "None"

        if report == 1:
            return HttpResponseRedirect(reverse("grais:spp_sample_xlsx", kwargs={"species_list": species_list}))
        elif report == 2:
            return HttpResponseRedirect(reverse("grais:od1_report", kwargs={"year": year})) if form.cleaned_data[
                "year"] else HttpResponseRedirect(reverse("grais:od1_report"))
        elif report == 3:
            return HttpResponseRedirect(reverse("grais:od1_dictionary"))
        elif report == 4:
            return HttpResponseRedirect(reverse("grais:od1_wms", kwargs={"year": year, "lang": 1}))
        elif report == 5:
            return HttpResponseRedirect(reverse("grais:od1_wms", kwargs={"year": year, "lang": 2}))
        elif report == 6:
            return HttpResponseRedirect(reverse("grais:gc_cpue_report", kwargs={"year": year}))
        elif report == 7:
            return HttpResponseRedirect(reverse("grais:gc_envr_report", kwargs={"year": year}))
        elif report == 8:
            return HttpResponseRedirect(reverse("grais:gc_site_report"))
        elif report == 9:
            return HttpResponseRedirect(reverse("grais:biofouling_pa_xlsx") + f"?year={year}")
        else:
            messages.error(self.request, "Report is not available. Please select another report.")
            return HttpResponseRedirect(reverse("grais:report_search"))


def species_sample_spreadsheet_export(request, species_list):
    file_url = reports.generate_species_sample_spreadsheet(species_list)
    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename="grais export {}.xlsx"'.format(timezone.now().strftime("%Y-%m-%d"))
            return response
    raise Http404


def biofouling_presence_absence_spreadsheet_export(request):
    year = request.GET["year"] if request.GET["year"] != "None" else None

    file_url = reports.generate_biofouling_pa_spreadsheet(year)
    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename="biofouling presence absence {}.xlsx"'.format(timezone.now().strftime("%Y-%m-%d"))
            return response
    raise Http404


def export_open_data_ver1(request, year=None):
    response = reports.generate_open_data_ver_1_report(year)
    return response


def export_open_data_ver1_dictionary(request):
    response = reports.generate_open_data_ver_1_data_dictionary()
    return response


def export_open_data_ver1_wms(request, year, lang):
    response = reports.generate_open_data_ver_1_wms_report(year, lang)
    return response


def export_gc_cpue(request, year):
    file_url = reports.generate_gc_cpue_report(year)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename="{} green crab CPUE data.xlsx"'.format(year)
            return response
    raise Http404


def export_gc_envr(request, year):
    file_url = reports.generate_gc_envr_report(year)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename="{} green crab environmental data.xlsx"'.format(year)
            return response
    raise Http404


def export_gc_sites(request):
    file_url = reports.generate_gc_sites_report()

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename="green crab site descriptions.xlsx"'
            return response
    raise Http404
