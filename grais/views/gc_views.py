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




# INCIDENTAL REPORT #
#####################

class ReportListView(GraisAccessRequiredMixin, CommonFilterView):
    filterset_class = filters.ReportFilter
    template_name = "grais/report_list.html"


class ReportUpdateView(GraisAccessRequiredMixin, CommonUpdateView):
    model = models.IncidentalReport
    form_class = forms.ReportForm
    template_name = "grais/report_form.html"

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class ReportCreateView(GraisAccessRequiredMixin, CommonCreateView):
    model = models.IncidentalReport
    form_class = forms.ReportForm
    template_name = "grais/report_form.html"

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class ReportDetailView(GraisAccessRequiredMixin, CommonDetailView):
    model = models.IncidentalReport

    template_name = "grais/report_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["field_list"] = [
            "report_date",
            "requestor_name",
            "report_source",
            "language_of_report",
            "call_answered_by",
            "call_returned_by",
            "location_description",
            "latitude_n",
            "longitude_w",
            "specimens_retained",
            "sighting_description",
            "identified_by",
            "date_of_occurrence",
            "observation_type",
            "phone1",
            "phone2",
            "email",
            "notes",
            # "date_last_modified",
            # "last_modified_by",
        ]

        # get a list of species
        species_list = []
        for obj in models.Species.objects.all():
            url = reverse("grais:report_species_add", kwargs={"report": self.object.id, "species": obj.id}),
            html_insert = '<a class="add-btn btn btn-outline-dark" href="#" target-url="{}"> <img src="{}" alt=""></a><span style="margin-left: 10px;">{} / <em>{}</em> / {}</span>'.format(
                url[0],
                static("admin/img/icon-addlink.svg"),
                obj.common_name,
                obj.scientific_name,
                obj.abbrev
            )
            species_list.append(html_insert)
        context['species_list'] = species_list
        return context


class ReportDeleteView(GraisAccessRequiredMixin, CommonDeleteView):
    model = models.IncidentalReport
    success_url = reverse_lazy('grais:report_list')
    success_message = 'The report was successfully deleted!'
    template_name = "grais/report_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


def report_species_observation_delete(request, report, species):
    report = models.IncidentalReport.objects.get(pk=report)
    species = models.Species.objects.get(pk=species)
    report.species.remove(species)
    messages.success(request, "The species has been successfully removed from this report.")
    return HttpResponseRedirect(reverse_lazy("grais:report_detail", kwargs={"pk": report.id}))


def report_species_observation_add(request, report, species):
    report = models.IncidentalReport.objects.get(pk=report)
    species = models.Species.objects.get(pk=species)
    report.species.add(species)
    return HttpResponseRedirect(reverse_lazy("grais:report_detail", kwargs={"pk": report.id}))


# FOLLOWUP #
############

class FollowUpUpdateView(GraisAccessRequiredMixin, CommonUpdateView):
    model = models.FollowUp
    form_class = forms.FollowUpForm
    template_name = 'grais/followup_form_popout.html'
    success_url = reverse_lazy("grais:close_me")


class FollowUpCreateView(GraisAccessRequiredMixin, CommonCreateView):
    model = models.FollowUp
    form_class = forms.FollowUpForm
    template_name = 'grais/followup_form_popout.html'
    success_url = reverse_lazy("grais:close_me")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["report"] = models.IncidentalReport.objects.get(pk=self.kwargs["report"])
        return context

    def get_initial(self):
        report = models.IncidentalReport.objects.get(pk=self.kwargs["report"])
        return {
            "incidental_report": report,
            "author": self.request.user
        }


@login_required(login_url='/accounts/login/')
@user_passes_test(is_grais_admin, login_url='/accounts/denied/')
def follow_up_delete(request, pk):
    followup = models.FollowUp.objects.get(pk=pk)
    followup.delete()
    messages.success(request, "The followup has been successfully deleted.")
    return HttpResponseRedirect(reverse_lazy("grais:report_detail", kwargs={"pk": followup.incidental_report_id}))
#
#
# # ESTUARY #
# ###########
#
# class EstuaryListView(GraisAccessRequiredMixin, FilterView):
#     filterset_class = filters.EstuaryFilter
#     template_name = "grais/estuary_list.html"
#
#
# class EstuaryUpdateView(GraisAdminRequiredMixin, UpdateView):
#     # permission_required = "__all__"
#     raise_exception = True
#
#     model = models.Estuary
#     form_class = forms.EstuaryForm
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
#
# class EstuaryCreateView(GraisAdminRequiredMixin, CreateView):
#     model = models.Estuary
#
#     form_class = forms.EstuaryForm
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
#
# class EstuaryDetailView(GraisAccessRequiredMixin, DetailView):
#     model = models.Estuary
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['google_api_key'] = settings.GOOGLE_API_KEY
#
#         field_list = [
#             "id",
#             "name",
#             "province",
#             "description",
#         ]
#         context['field_list'] = field_list
#
#         site_list = [[site.code, site.latitude_n, site.longitude_w] for site in self.object.sites.all() if
#                      site.latitude_n and site.longitude_w]
#         context['site_list'] = site_list
#
#         return context
#
#
# class EstuaryDeleteView(GraisAdminRequiredMixin, DeleteView):
#     model = models.Estuary
#     success_url = reverse_lazy('grais:estuary_list')
#     success_message = 'The sstuary was successfully deleted!'
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
#
#
# # SITE #
# ########
#
# class SiteUpdateView(GraisAdminRequiredMixin, UpdateView):
#     # permission_required = "__all__"
#     raise_exception = True
#
#     model = models.Site
#     form_class = forms.SiteForm
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
#     def get_success_url(self):
#         return reverse_lazy('grais:estuary_detail', kwargs={'pk': self.object.estuary.id})
#
#
# class SiteCreateView(GraisAdminRequiredMixin, CreateView):
#     model = models.Site
#
#     form_class = forms.SiteForm
#
#     def get_initial(self):
#         return {
#             'estuary': self.kwargs['estuary'],
#             'last_modified_by': self.request.user,
#         }
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         try:
#             context['estuary'] = models.Estuary.objects.get(pk=self.kwargs['estuary'])
#         except KeyError:
#             pass
#         return context
#
#     def get_success_url(self):
#         return reverse_lazy('grais:estuary_detail', kwargs={'pk': self.object.estuary.id})
#
#
# class SiteDetailView(GraisAccessRequiredMixin, DetailView):
#     model = models.Site
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         field_list = [
#             'estuary',
#             'code',
#             'name',
#             'latitude_n',
#             'longitude_w',
#             'description',
#         ]
#         context['field_list'] = field_list
#         return context
#
#
# class SiteDeleteView(GraisAdminRequiredMixin, DeleteView):
#     model = models.Site
#     success_url = reverse_lazy('grais:site_list')
#     success_message = 'The site was successfully deleted!'
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
#
#     def get_success_url(self):
#         return reverse_lazy('grais:estuary_detail', kwargs={'pk': self.object.estuary.id})
#
#
# # SAMPLE #
# ##########
# class GCSampleListView(GraisAccessRequiredMixin, FilterView):
#     filterset_class = filters.GCSampleFilter
#     template_name = "grais/gcsample_list.html"
#     model = models.GCSample
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["my_object"] = models.GCSample.objects.first()
#         context["field_list"] = [
#             'season',
#             'site',
#             'traps_set|Traps set',
#             'traps_fished|Traps fished',
#         ]
#         return context
#
#
# class GCSampleDetailView(GraisAccessRequiredMixin, DetailView):
#     model = models.GCSample
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['google_api_key'] = settings.GOOGLE_API_KEY
#         context["field_list"] = [
#             'site',
#             'traps_set',
#             'traps_fished',
#             'samplers',
#             'eelgrass_assessed',
#             'eelgrass_percent_coverage',
#             'vegetation_species',
#             'sediment',
#             'season',
#             'last_modified',
#             'last_modified_by',
#             'notes',
#         ]
#         return context
#
#
# class GCSampleUpdateView(GraisAdminRequiredMixin, UpdateView):
#     model = models.GCSample
#     form_class = forms.GCSampleForm
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
#     def form_valid(self, form):
#         object = form.save()
#         return HttpResponseRedirect(reverse_lazy("grais:gcsample_detail", kwargs={"pk": object.id}))
#
#
# class GCSampleCreateView(GraisAdminRequiredMixin, CreateView):
#     model = models.GCSample
#     form_class = forms.GCSampleForm
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
#     def form_valid(self, form):
#         object = form.save()
#         return HttpResponseRedirect(reverse_lazy("grais:gcsample_detail", kwargs={"pk": object.id}))
#
#
# class GCSampleDeleteView(GraisAdminRequiredMixin, DeleteView):
#     model = models.GCSample
#     success_url = reverse_lazy('grais:gcsample_list')
#     success_message = 'The sample was successfully deleted!'
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
#
#
# # GC PROBE DATA #
# ##############
#
# class GCProbeMeasurementCreateView(GraisAdminRequiredMixin, CreateView):
#     model = models.GCProbeMeasurement
#     form_class = forms.GCProbeMeasurementForm
#     template_name = 'grais/gcprobe_measurement_form.html'
#
#     def get_initial(self):
#         gcsample = models.GCSample.objects.get(pk=self.kwargs['gcsample'])
#         return {
#             'sample': gcsample,
#             'last_modified_by': self.request.user,
#         }
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['gcsample'] = models.GCSample.objects.get(pk=self.kwargs["gcsample"])
#         return context
#
#     def form_valid(self, form):
#         object = form.save()
#         return HttpResponseRedirect(reverse_lazy("grais:gcprobe_measurement_detail", kwargs={"pk": object.id}))
#
#
# class GCProbeMeasurementDetailView(GraisAdminRequiredMixin, UpdateView):
#     model = models.GCProbeMeasurement
#     form_class = forms.GCProbeMeasurementForm
#     template_name = 'grais/gcprobe_measurement_detail.html'
#
#
# class GCProbeMeasurementUpdateView(GraisAdminRequiredMixin, UpdateView):
#     model = models.GCProbeMeasurement
#     form_class = forms.GCProbeMeasurementForm
#     template_name = 'grais/gcprobe_measurement_form.html'
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
#     def form_valid(self, form):
#         object = form.save()
#         return HttpResponseRedirect(reverse_lazy("grais:gcprobe_measurement_detail", kwargs={"pk": object.id}))
#
#
# class GCProbeMeasurementDeleteView(GraisAdminRequiredMixin, DeleteView):
#     model = models.GCProbeMeasurement
#     template_name = "grais/gcprobe_measurement_confirm_delete.html"
#     success_message = 'The probe measurement was successfully deleted!'
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
#
#     def get_success_url(self):
#         return reverse_lazy('grais:gcsample_detail', kwargs={'pk': self.object.sample.id})
#
#
# # TRAP #
# #########
#
# class TrapCreateView(GraisAdminRequiredMixin, CreateView):
#     model = models.Trap
#     form_class = forms.TrapForm
#
#     def get_initial(self):
#         sample = models.GCSample.objects.get(pk=self.kwargs['gcsample'])
#         return {
#             'sample': sample,
#             'last_modified_by': self.request.user
#         }
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['gcsample'] = models.GCSample.objects.get(pk=self.kwargs["gcsample"])
#         return context
#
#     def form_valid(self, form):
#         object = form.save()
#         return HttpResponseRedirect(reverse_lazy("grais:trap_detail", kwargs={"pk": object.id}))
#
#
# class TrapDetailView(GraisAccessRequiredMixin, DetailView, FormView):
#     model = models.Trap
#     form_class = forms.TrapSpeciesForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['google_api_key'] = settings.GOOGLE_API_KEY
#         context["field_list"] = [
#             # 'sample',
#             'trap_number',
#             'trap_type',
#             'bait_type',
#             'depth_at_set_m',
#             'latitude_n',
#             'longitude_w',
#             'gps_waypoint',
#             'notes',
#             'total_green_crab_wt_kg',
#         ]
#
#         context["crab_field_list"] = [
#             'species',
#             'width',
#             'sex',
#             'carapace_color',
#             'abdomen_color',
#             'egg_color',
#             'notes',
#         ]
#         context["bycatch_field_list"] = [
#             'species',
#             'count',
#             'notes',
#         ]
#         context["random_catch_object"] = models.Catch.objects.first
#         # get a list of species
#
#         return context
#
#
# class TrapUpdateView(GraisAdminRequiredMixin, UpdateView):
#     model = models.Trap
#     form_class = forms.TrapForm
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
#     def form_valid(self, form):
#         object = form.save()
#         return HttpResponseRedirect(reverse_lazy("grais:trap_detail", kwargs={"pk": object.id}))
#
#
# class TrapDeleteView(GraisAdminRequiredMixin, DeleteView):
#     model = models.Trap
#     success_message = 'The trap was successfully deleted!'
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
#
#     def get_success_url(self):
#         return reverse_lazy('grais:gcsample_detail', kwargs={'pk': self.object.sample.id})
#
#
# # CATCH #
# #########
#
# class CatchCreateViewPopout(GraisAdminRequiredMixin, FormView):
#     template_name = 'grais/catch_form_popout.html'
#     form_class = forms.NewCatchForm
#     model = models.Catch
#
#     def get_initial(self):
#         my_dict = {}
#         my_trap = models.Trap.objects.get(pk=self.kwargs['trap'])
#         my_species = models.Species.objects.get(pk=self.kwargs['species'])
#         my_dict["species"] = my_species
#         my_dict["trap"] = my_trap
#         # my_dict["last_modified_by"] = self.request.user.id
#
#         # if this is a bycatch sp, let's look up the previous entry
#         if not my_species.green_crab_monitoring:
#             try:
#                 my_catch = models.Catch.objects.get(
#                     species=my_species,
#                     trap=my_trap,
#                 )
#             except models.Catch.DoesNotExist:
#                 pass
#             else:
#                 my_dict["notes"] = my_catch.notes
#                 my_dict["count"] = my_catch.count
#
#         return my_dict
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         my_species = models.Species.objects.get(id=self.kwargs['species'])
#         my_trap = models.Trap.objects.get(id=self.kwargs['trap'])
#         context['species'] = my_species
#         context['trap'] = my_trap
#         return context
#
#     def form_valid(self, form):
#         my_species = models.Species.objects.get(id=self.kwargs['species'])
#         my_trap = models.Trap.objects.get(id=self.kwargs['trap'])
#
#         # if the species is a bycatch species, save all the data as a catch instance
#         if not my_species.green_crab_monitoring:
#             if form.cleaned_data.get("count"):
#                 my_catch, created = models.Catch.objects.get_or_create(
#                     species=my_species,
#                     trap=my_trap,
#                 )
#                 my_catch.count = form.cleaned_data.get("count")
#                 my_catch.notes = form.cleaned_data.get("notes")
#                 my_catch.last_modified_by = self.request.user
#                 my_catch.save()
#
#         # if targeted species, lets create x number of blank entries
#         else:
#             for i in range(0, form.cleaned_data.get("count")):
#                 print("creating catch")
#                 models.Catch.objects.create(
#                     species=my_species,
#                     trap=my_trap,
#                     last_modified_by=self.request.user,
#                 )
#
#         return HttpResponseRedirect(reverse('grais:close_me'))
#
#
# class CatchUpdateViewPopout(GraisAdminRequiredMixin, UpdateView):
#     template_name = 'grais/catch_form_popout.html'
#     form_class = forms.CatchForm
#     model = models.Catch
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user.id}
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
#
#     def form_valid(self, form):
#         self.object = form.save()
#         return HttpResponseRedirect(reverse('grais:close_me'))
#
#
# @login_required(login_url='/accounts/login/')
# @user_passes_test(is_grais_admin, login_url='/accounts/denied/')
# def catch_delete(request, pk):
#     my_catch = models.Catch.objects.get(pk=pk)
#     my_catch.delete()
#     messages.success(request, "The catch item has been successfully removed from this trap.")
#     return HttpResponseRedirect(reverse_lazy("grais:trap_detail", kwargs={"pk": my_catch.trap.id}))
#
#
# @login_required(login_url='/accounts/login/')
# @user_passes_test(is_grais_admin, login_url='/accounts/denied/')
# def manage_catch(request, trap, type):
#     qs = models.Catch.objects.filter(trap_id=trap)
#     context = dict()
#     context["my_object"] = qs.first()
#     context["trap"] = qs.first().trap
#
#     if type == "invasive":
#         qs = qs.filter(species__invasive=True, species__green_crab_monitoring=True)
#         crab = True
#     elif type == "noninvasive":
#         qs = qs.filter(species__invasive=False, species__green_crab_monitoring=True)
#         crab = True
#     elif type == "bycatch":
#         qs = qs.filter(species__green_crab_monitoring=False)
#         crab = False
#
#     if crab:
#         context["field_list"] = [
#             'width',
#             'sex',
#             'carapace_color',
#             'abdomen_color',
#             'egg_color',
#             'notes',
#         ]
#     else:
#         context["field_list"] = [
#             'count',
#             'notes',
#         ]
#
#     if request.method == 'POST':
#         formset = forms.CatchFormSet(request.POST, )
#         if formset.is_valid():
#             formset.save()
#             # do something with the formset.cleaned_data
#             messages.success(request, "Items have been successfully updated")
#             return HttpResponseRedirect(reverse("grais:manage_catch", kwargs={"trap": trap, "type": type}))
#     else:
#         formset = forms.CatchFormSet(queryset=qs)
#
#     context['title'] = "Manage Catch"
#     context['formset'] = formset
#     return render(request, 'grais/manage_catch.html', context)
#
#
# #
# # # Bycatch #
# # #########
# #
# # class BycatchCreateViewPopout(GraisAdminRequiredMixin, CreateView):
# #     template_name = 'grais/crab_form_popout.html'
# #     form_class = forms.BycatchForm
# #     model = models.Catch
# #
# #     def get_initial(self):
# #         my_dict = {}
# #         my_dict["trap"] = models.Trap.objects.get(pk=self.kwargs['trap'])
# #         my_dict["species"] = models.Species.objects.get(pk=self.kwargs['species'])
# #         my_dict["last_modified_by"] = self.request.user.id
# #         return my_dict
# #
# #     def get_context_data(self, **kwargs):
# #         context = super().get_context_data(**kwargs)
# #         trap = models.Trap.objects.get(id=self.kwargs['trap'])
# #         species = models.Species.objects.get(id=self.kwargs['species'])
# #         context['species'] = species
# #         context['trap'] = trap
# #         return context
# #
# #     def form_valid(self, form):
# #         self.object = form.save()
# #         return HttpResponseRedirect(reverse('grais:close_me'))
# #
# #
# # class BycatchUpdateViewPopout(GraisAdminRequiredMixin, CreateView):
# #     template_name = 'grais/crab_form_popout.html'
# #     form_class = forms.BycatchForm
# #     model = models.Catch
# #
# #     def get_initial(self):
# #         return {'last_modified_by': self.request.user.id}
# #
# #     def get_context_data(self, **kwargs):
# #         context = super().get_context_data(**kwargs)
# #         return context
# #
# #     def form_valid(self, form):
# #         self.object = form.save()
# #         return HttpResponseRedirect(reverse('grais:close_me'))
# #
# #
# # @login_required(login_url='/accounts/login/')
# # @user_passes_test(is_grais_admin, login_url='/accounts/denied/')
# # def bycatch_delete(request, pk):
# #     bycatch = models.Catch.objects.get(pk=pk)
# #     bycatch.delete()
# #     messages.success(request, "The bycatch has been successfully removed from this trap.")
# #     return HttpResponseRedirect(reverse_lazy("grais:trap_detail", kwargs={"pk": bycatch.trap.id}))
#
#

# REPORTS #
###########

class ReportSearchFormView(GraisAccessRequiredMixin, FormView):
    template_name = 'grais/report_search.html'
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
#
