import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Value, TextField
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.views.generic import FormView

from shared_models.views import CommonFormsetView, CommonHardDeleteView, CommonTemplateView, CommonFilterView, CommonUpdateView, CommonCreateView, \
    CommonDetailView, CommonDeleteView, CommonPopoutUpdateView, CommonPopoutCreateView, CommonPopoutDeleteView
from grais import filters
from grais import forms
from grais import models
from grais import reports
from grais.mixins import GraisAccessRequiredMixin, GraisAdminRequiredMixin, GraisCRUDRequiredMixin
from grais.utils import is_grais_admin


# STATION #
###########

class StationListView(GraisAccessRequiredMixin, CommonFilterView):
    model = models.Station
    template_name = 'grais/list.html'
    filterset_class = filters.StationFilter
    home_url_name = "grais:index"
    new_object_url = reverse_lazy("grais:station_new")
    row_object_url_name = row_ = "grais:station_detail"
    h1 = "Biofouling Stations"

    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'station_name|{}'.format("common name"), "class": "", "width": ""},
        {"name": 'province.abbrev_eng|{}'.format("province"), "class": "", "width": ""},
        {"name": 'sample_count|sample count', "class": "", "width": ""},
    ]


class StationUpdateView(GraisCRUDRequiredMixin, CommonUpdateView):
    model = models.Station
    form_class = forms.StationForm
    template_name = 'grais/form.html'
    home_url_name = "grais:index"
    grandparent_crumb = {"title": gettext_lazy("Stations"), "url": reverse_lazy("grais:station_list")}

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse_lazy("grais:station_detail", args=[self.get_object().id])}

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.updated_by = self.request.user
        return super().form_valid(form)


class StationCreateView(GraisCRUDRequiredMixin, CommonCreateView):
    model = models.Station
    form_class = forms.StationForm
    template_name = 'grais/form.html'
    home_url_name = "grais:index"
    parent_crumb = {"title": gettext_lazy("Stations"), "url": reverse_lazy("grais:station_list")}

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.updated_by = self.request.user
        return super().form_valid(form)


class StationDetailView(GraisAccessRequiredMixin, CommonDetailView):
    model = models.Station
    template_name = 'grais/biofouling/station_detail.html'
    home_url_name = "grais:index"
    parent_crumb = {"title": gettext_lazy("Stations"), "url": reverse_lazy("grais:station_list")}
    field_list = [
        'id',
        'name',
        'latitude',
        'longitude',
        'depth',
        'site_desc',
        'metadata',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sample_field_list"] = [
            "id",
            "season",
        ]
        context["mapbox_api_key"] = settings.MAPBOX_API_KEY
        return context


class StationDeleteView(GraisAdminRequiredMixin, CommonDeleteView):
    model = models.Station
    success_url = reverse_lazy('grais:station_list')
    success_message = 'The functional group was successfully deleted!'
    template_name = 'grais/confirm_delete.html'


# SAMPLE #
###########

class SampleListView(GraisAccessRequiredMixin, CommonFilterView):
    model = models.Sample
    template_name = 'grais/list.html'
    filterset_class = filters.SampleFilter
    paginate_by = 100
    home_url_name = "grais:index"
    new_object_url = reverse_lazy("grais:sample_new")
    row_object_url_name = row_ = "grais:sample_detail"
    h1 = "Biofouling Samples"

    field_list = [
        {"name": 'station', "class": "", "width": ""},
        {"name": 'date_deployed', "class": "", "width": ""},
        {"name": 'date_retrieved', "class": "", "width": ""},
        {"name": 'sample_type', "class": "", "width": ""},
        {"name": 'weeks_deployed|{}'.format("weeks deployed"), "class": "", "width": ""},
        {"name": 'has_invasive_spp|{}'.format("has invasive species?"), "class": "", "width": ""},
        {"name": 'line_count|{}'.format("lines"), "class": "", "width": ""},
        {"name": 'species_count|{}'.format("species count"), "class": "", "width": ""},
    ]


class SampleUpdateView(GraisCRUDRequiredMixin, CommonUpdateView):
    model = models.Sample
    form_class = forms.SampleForm
    template_name = 'grais/form.html'
    home_url_name = "grais:index"
    grandparent_crumb = {"title": gettext_lazy("Samples"), "url": reverse_lazy("grais:sample_list")}

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse_lazy("grais:sample_detail", args=[self.get_object().id])}

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.updated_by = self.request.user
        return super().form_valid(form)


class SampleCreateView(GraisCRUDRequiredMixin, CommonCreateView):
    model = models.Sample
    form_class = forms.SampleForm
    template_name = 'grais/form.html'
    home_url_name = "grais:index"
    parent_crumb = {"title": gettext_lazy("Samples"), "url": reverse_lazy("grais:sample_list")}

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.updated_by = self.request.user
        return super().form_valid(form)


class SampleDetailView(GraisCRUDRequiredMixin, CommonDetailView):
    model = models.Sample
    template_name = 'grais/biofouling/sample_detail/main.html'
    home_url_name = "grais:index"
    parent_crumb = {"title": gettext_lazy("Samples"), "url": reverse_lazy("grais:sample_list")}
    field_list = [
        'id',
        'station',
        'date_deployed',
        'date_retrieved',
        'weeks_deployed|Weeks deployed',
        'samplers',
        'sample_type',
        'has_invasive_spp|Has invasive species?',
        'metadata',
    ]
    container_class = "container-fluid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["probe_field_list"] = [
            'dt|Date/time',
            'probe',
            'probe_depth',
            'cloud_cover',
            'weather_notes',
            'temp_c',
            'sal_ppt',
            'o2_percent',
            'o2_mgl',
            'sp_cond_ms',
            'spc_ms',
            'ph',
            # 'metadata',
        ]
        context["line_field_list"] = [
            'collector|tag',
            'coordinates',
            'surface_count|surface count',
            'surface_species_count|species count',
            'has_invasive_spp|has invasive spp?',
            'is_lost',
        ]
        context["species_obs_field_list"] = [
            'species',
            'observation_date',
            'notes',
        ]
        context["mapbox_api_key"] = settings.MAPBOX_API_KEY
        return context


class SampleDeleteView(GraisCRUDRequiredMixin, CommonDeleteView):
    model = models.Sample
    success_url = reverse_lazy('grais:sample_list')
    success_message = 'The functional group was successfully deleted!'
    template_name = 'grais/confirm_delete.html'


# SAMPLE NOTE #
###############

class SampleNoteUpdateView(GraisAccessRequiredMixin, CommonPopoutUpdateView):
    model = models.SampleNote
    form_class = forms.SampleNoteForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.updated_by = self.request.user
        obj.save()
        return super().form_valid(form)


class SampleNoteCreateView(GraisAccessRequiredMixin, CommonPopoutCreateView):
    model = models.SampleNote
    form_class = forms.SampleNoteForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.sample = get_object_or_404(models.Sample, pk=self.kwargs.get("sample"))
        obj.created_by = self.request.user
        obj.save()
        return super().form_valid(form)


class SampleNoteDeleteView(GraisAccessRequiredMixin, CommonPopoutDeleteView):
    model = models.SampleNote


# PROBE MEASUREMENT #
#####################

class ProbeMeasurementUpdateView(GraisAccessRequiredMixin, CommonPopoutUpdateView):
    model = models.ProbeMeasurement
    form_class = forms.ProbeMeasurementForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.updated_by = self.request.user
        obj.save()
        return super().form_valid(form)


class ProbeMeasurementCreateView(GraisAccessRequiredMixin, CommonPopoutCreateView):
    model = models.ProbeMeasurement
    form_class = forms.ProbeMeasurementForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.sample = get_object_or_404(models.Sample, pk=self.kwargs.get("sample"))
        obj.created_by = self.request.user
        obj.save()
        return super().form_valid(form)


class ProbeMeasurementDeleteView(GraisAccessRequiredMixin, CommonPopoutDeleteView):
    model = models.ProbeMeasurement


# SPECIES OBSERVATIONS - VUE JS #
##################################

class SpeciesObservationTemplateView(GraisAccessRequiredMixin, CommonDetailView):
    template_name = 'grais/biofouling/species_observations.html'
    home_url_name = 'grais:index'
    greatgrandparent_crumb = {"title": gettext_lazy("Samples"), "url": reverse_lazy("grais:sample_list")}

    def get_object(self):
        if self.kwargs.get("type") == "samples":
            return get_object_or_404(models.Sample, pk=self.kwargs.get("pk"))
        elif self.kwargs.get("type") == "lines":
            return get_object_or_404(models.Line, pk=self.kwargs.get("pk"))
        elif self.kwargs.get("type") == "surfaces":
            return get_object_or_404(models.Surface, pk=self.kwargs.get("pk"))
        return Http404

    def get_parent_crumb(self):
        type_singular = self.kwargs.get("type")[:-1]
        return {"title": self.get_object(), "url": reverse_lazy(f"grais:{type_singular}_detail", args=[self.get_object().id])}

    def get_grandparent_crumb(self):
        if self.kwargs.get("type") == "lines":
            return {"title": self.get_object().sample, "url": reverse_lazy(f"grais:sample_detail", args=[self.get_object().sample.id])}
        if self.kwargs.get("type") == "surfaces":
            return {"title": self.get_object().line, "url": reverse_lazy(f"grais:line_detail", args=[self.get_object().line.id])}

    def get_greatgrandparent_crumb(self):
        if self.kwargs.get("type") == "surfaces":
            return {"title": self.get_object().line.sample, "url": reverse_lazy(f"grais:sample_detail", args=[self.get_object().line.sample.id])}

    def get_h1(self):
        if self.kwargs.get("type") == "samples":
            return "Sample-Level Species Observations"
        elif self.kwargs.get("type") == "lines":
            return "Line-Level Species Observations"
        elif self.kwargs.get("type") == "surfaces":
            return "Surface-Level Species Observations"


# LINE #
###########

class LineUpdateView(GraisCRUDRequiredMixin, CommonUpdateView):
    model = models.Line
    form_class = forms.LineForm
    template_name = 'grais/form.html'
    home_url_name = "grais:index"
    grandparent_crumb = {"title": gettext_lazy("Samples"), "url": reverse_lazy("grais:sample_list")}

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse_lazy("grais:line_detail", args=[self.get_object().id])}

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.updated_by = self.request.user
        return super().form_valid(form)


class LineCreateView(GraisCRUDRequiredMixin, CommonCreateView):
    model = models.Line
    form_class = forms.LineCreateForm
    template_name = 'grais/form.html'
    home_url_name = "grais:index"
    grandparent_crumb = {"title": gettext_lazy("Samples"), "url": reverse_lazy("grais:sample_list")}

    def get_parent_crumb(self):
        return {"title": self.get_sample(), "url": reverse_lazy("grais:sample_detail", args=[self.get_sample().id])}

    def get_sample(self):
        return get_object_or_404(models.Sample, pk=self.kwargs.get("sample"))

    def get_initial(self):
        return {
            'number_plates': 2,
            'number_petris': 3,
        }

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.sample = self.get_sample()
        obj.updated_by = self.request.user
        obj.save()
        petris = form.cleaned_data['number_petris']
        plates = form.cleaned_data['number_plates']
        if petris + plates > 0:
            # create instances of surfaces on the collector lines
            # create iterable
            for i in range(petris):
                s = models.Surface.objects.create(line=obj, surface_type='pe', label="Petri dish {}".format(i + 1))
                s.save()
            for i in range(plates):
                s = models.Surface.objects.create(line=obj, surface_type='pl', label="Plate {}".format(i + 1))
                s.save()
        return super().form_valid(form)


class LineDetailView(GraisCRUDRequiredMixin, CommonDetailView):
    model = models.Line
    template_name = 'grais/biofouling/line_detail/main.html'
    home_url_name = "grais:index"
    grandparent_crumb = {"title": gettext_lazy("Samples"), "url": reverse_lazy("grais:sample_list")}
    field_list = [
        'id',
        'collector',
        'coordinates',
        'species_list|surface species',
        'has_invasive_spp|has invasive spp?',
        'is_lost',
        'notes',
        'metadata',
    ]
    container_class = "container-fluid"

    def get_parent_crumb(self):
        return {"title": self.get_object().sample, "url": reverse_lazy("grais:sample_detail", args=[self.get_object().sample.id])}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["surface_field_list"] = [
            'display|surface',
            'surface_type',
            'species_list|species',
            'has_invasive_spp|has invasive spp?',
            'is_lost',
            'thumbnail',
        ]
        context["species_obs_field_list"] = [
            'species',
            'observation_date',
            'notes',
        ]
        context["mapbox_api_key"] = settings.MAPBOX_API_KEY
        return context


class LineDeleteView(GraisCRUDRequiredMixin, CommonDeleteView):
    model = models.Line
    success_message = 'The functional group was successfully deleted!'
    template_name = 'grais/confirm_delete.html'
    greatgrandparent_crumb = {"title": gettext_lazy("Samples"), "url": reverse_lazy("grais:sample_list")}

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse_lazy("grais:line_detail", args=[self.get_object().id])}

    def get_grandparent_crumb(self):
        return {"title": self.get_object().sample, "url": reverse_lazy("grais:sample_detail", args=[self.get_object().sample.id])}

    def get_success_url(self):
        return self.get_grandparent_crumb().get("url")

# SURFACES #
############

class SurfaceUpdateView(GraisCRUDRequiredMixin, CommonUpdateView):
    model = models.Surface
    form_class = forms.SurfaceForm
    template_name = 'grais/form.html'
    home_url_name = "grais:index"
    is_multipart_form_data = True

    def get_greatgrandparent_crumb(self):
        return {"title": self.get_object().line.sample, "url": reverse_lazy("grais:sample_detail", args=[self.get_object().line.sample.id])}

    def get_grandparent_crumb(self):
        return {"title": self.get_object().line, "url": reverse_lazy("grais:line_detail", args=[self.get_object().line.id])}

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse_lazy("grais:surface_detail", args=[self.get_object().id])}

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.updated_by = self.request.user
        return super().form_valid(form)


class SurfaceCreateView(GraisCRUDRequiredMixin, CommonCreateView):
    model = models.Surface
    form_class = forms.SurfaceForm
    template_name = 'grais/form.html'
    home_url_name = "grais:index"
    greatgrandparent_crumb = {"title": gettext_lazy("Samples"), "url": reverse_lazy("grais:sample_list")}
    is_multipart_form_data = True

    def get_grandparent_crumb(self):
        return {"title": self.get_line().sample, "url": reverse_lazy("grais:sample_detail", args=[self.get_line().sample.id])}

    def get_parent_crumb(self):
        return {"title": self.get_line(), "url": reverse_lazy("grais:line_detail", args=[self.get_line().id])}

    def get_line(self):
        return get_object_or_404(models.Line, pk=self.kwargs.get("line"))

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.line = self.get_line()
        obj.updated_by = self.request.user
        obj.save()
        return super().form_valid(form)


class SurfaceDetailView(GraisCRUDRequiredMixin, CommonDetailView):
    model = models.Surface
    template_name = 'grais/biofouling/surface_detail/main.html'
    home_url_name = "grais:index"
    field_list = [
        'id',
        'display|surface',
        'surface_type',
        'species_list|species',
        'total_coverage_display|total coverage',
        'has_invasive_spp|has invasive spp?',
        'notes',
        'is_lost',
        'metadata',

    ]
    container_class = "container-fluid"
    greatgrandparent_crumb = {"title": gettext_lazy("Samples"), "url": reverse_lazy("grais:sample_list")}

    def get_grandparent_crumb(self):
        return {"title": self.get_object().line.sample, "url": reverse_lazy("grais:sample_detail", args=[self.get_object().line.sample.id])}

    def get_parent_crumb(self):
        return {"title": self.get_object().line, "url": reverse_lazy("grais:line_detail", args=[self.get_object().line.id])}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["surface_field_list"] = [
            'id',
            'display|surface',
            'has_invasive_spp|has invasive spp.?',
            'species_count|total spp.',
            'thumbnail',
            'is_lost',
        ]
        context["species_obs_field_list"] = [
            'species',
            'invasive?',
            'coverage_display|percent coverage',
            'notes',
        ]
        context["mapbox_api_key"] = settings.MAPBOX_API_KEY
        return context


class SurfaceDeleteView(GraisCRUDRequiredMixin, CommonDeleteView):
    model = models.Surface
    success_message = 'The functional group was successfully deleted!'
    template_name = 'grais/confirm_delete.html'

    def get_success_url(self):
        return reverse('grais:line_detail', args=[self.get_object().line.id])


