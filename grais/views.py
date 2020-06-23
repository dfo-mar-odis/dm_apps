import csv
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db.models import TextField
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.utils import timezone

from django.views.generic import UpdateView, DeleteView, CreateView, DetailView, TemplateView, FormView
from django.urls import reverse_lazy, reverse
from django_filters.views import FilterView

from lib.templatetags.custom_filters import nz
from . import models
from . import forms
from . import filters
from . import reports


def in_grais_group(user):
    if user:
        return user.groups.filter(name='grais_access').count() != 0


def in_grais_admin_group(user):
    if user:
        return user.groups.filter(name='grais_admin').count() != 0


class GraisAccessRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return in_grais_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class GraisAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return in_grais_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class IndexView(GraisAccessRequiredMixin, TemplateView):
    template_name = 'grais/index.html'


class DataFlowTemplateView(GraisAccessRequiredMixin, TemplateView):
    template_name = 'grais/dataflow.html'


class CloserTemplateView(GraisAccessRequiredMixin, TemplateView):
    template_name = 'grais/close_me.html'


# SAMPLE #
##########
class SampleListView(GraisAccessRequiredMixin, FilterView):
    filterset_class = filters.SampleFilter
    template_name = "grais/sample_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["random_object"] = models.Sample.objects.first()
        field_list = [
            'id|Sample #',
            'station',
            'date_deployed',
            'date_retrieved',
            'sample_type',
            'weeks_deployed|Weeks deployed',
            'has_invasive_spp|Has invasive species?',

        ]
        context["field_list"] = field_list

        return context

    # def get_filterset_kwargs(self, filterset_class):
    #     kwargs = super().get_filterset_kwargs(filterset_class)
    #     if kwargs["data"] is None:
    #         kwargs["data"] = {"SeasonExact": timezone.now().year-2 }
    #     return kwargs


class SampleDetailView(GraisAccessRequiredMixin, DetailView):
    model = models.Sample

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY
        context["field_list"] = [
            'station',
            'date_deployed',
            'date_retrieved',
            'weeks_deployed|Weeks deployed',
            'samplers',
            'sample_type',
            'has_invasive_spp|Has invasive species?',
            'last_modified',
            'last_modified_by',
        ]

        sampler_field_list = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'organization',

        ]
        context["sampler_field_list"] = sampler_field_list

        context["random_probe_object"] = models.ProbeMeasurement.objects.first()
        probe_field_list = [
            'time_date',
            'probe',
            'temp_c',
            'sal_ppt',
            'o2_percent',
            'o2_mgl',
            'sp_cond_ms',
            'spc_ms',
        ]
        context["probe_field_list"] = probe_field_list

        return context


class SampleUpdateView(GraisAdminRequiredMixin, UpdateView):
    model = models.Sample
    form_class = forms.SampleForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class SampleCreateView(GraisAdminRequiredMixin, CreateView):
    model = models.Sample
    form_class = forms.SampleForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class SampleDeleteView(GraisAdminRequiredMixin, DeleteView):
    model = models.Sample
    success_url = reverse_lazy('grais:sample_list')
    success_message = 'The sample was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# SAMPLE NOTE #
##############

class SampleNoteUpdateView(GraisAccessRequiredMixin, UpdateView):
    model = models.SampleNote
    form_class = forms.SampleNoteForm


class SampleNoteCreateView(GraisAccessRequiredMixin, CreateView):
    model = models.SampleNote
    form_class = forms.SampleNoteForm

    def get_context_data(self, **kwargs):
        context = super(SampleNoteCreateView, self).get_context_data(**kwargs)
        context["sample"] = models.Sample.objects.get(pk=self.kwargs["sample"])
        return context

    def get_initial(self):
        sample = models.Sample.objects.get(pk=self.kwargs["sample"])
        return {
            "sample": sample,
            "author": self.request.user
        }


@login_required(login_url='/accounts/login/')
@user_passes_test(in_grais_admin_group, login_url='/accounts/denied/')
def sample_note_delete(request, pk):
    note = models.SampleNote.objects.get(pk=pk)
    note.delete()
    messages.success(request, "The note has been successfully deleted.")
    return HttpResponseRedirect(reverse_lazy("grais:sample_detail", kwargs={"pk": note.sample_id}))


# STATION #
###########

class StationListView(GraisAccessRequiredMixin, FilterView):
    filterset_class = filters.StationFilter
    template_name = "grais/station_list.html"


class StationUpdateView(GraisAdminRequiredMixin, UpdateView):
    # permission_required = "__all__"
    raise_exception = True
    model = models.Station
    form_class = forms.StationForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class StationCreateView(GraisAdminRequiredMixin, CreateView):
    model = models.Station
    form_class = forms.StationForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class StationDetailView(GraisAccessRequiredMixin, UpdateView):
    model = models.Station
    fields = ('__all__')
    template_name = 'grais/station_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY
        return context


class StationDeleteView(GraisAdminRequiredMixin, DeleteView):
    model = models.Station
    success_url = reverse_lazy('grais:station_list')
    success_message = 'The station was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# PERSON #
##########

class PersonUpdateView(GraisAdminRequiredMixin, UpdateView):
    model = models.Sampler
    fields = ('__all__')
    template_name = 'grais/person_form_popout.html'
    success_url = reverse_lazy("grais:close_me")


class PersonCreateView(GraisAdminRequiredMixin, CreateView):
    model = models.Sampler
    fields = ('__all__')
    template_name = 'grais/person_form_popout.html'
    success_url = reverse_lazy("grais:close_me")


class PersonDetailView(GraisAccessRequiredMixin, UpdateView):
    model = models.Sampler
    template_name = 'grais/person_detail_popout.html'
    fields = ('__all__')


# PROBE DATA #
##############

class ProbeMeasurementCreateView(GraisAdminRequiredMixin, CreateView):
    model = models.ProbeMeasurement
    form_class = forms.ProbeMeasurementForm
    template_name = 'grais/probe_measurement_form.html'

    def get_initial(self):
        sample = models.Sample.objects.get(pk=self.kwargs['sample'])
        return {
            'sample': sample,
            'last_modified_by': self.request.user,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sample'] = models.Sample.objects.get(pk=self.kwargs["sample"])
        return context


class ProbeMeasurementDetailView(GraisAccessRequiredMixin, UpdateView):
    model = models.ProbeMeasurement
    form_class = forms.ProbeMeasurementForm
    template_name = 'grais/probe_measurement_detail.html'


class ProbeMeasurementUpdateView(GraisAdminRequiredMixin, UpdateView):
    model = models.ProbeMeasurement
    form_class = forms.ProbeMeasurementForm
    template_name = 'grais/probe_measurement_form.html'

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class ProbeMeasurementDeleteView(GraisAdminRequiredMixin, DeleteView):
    model = models.ProbeMeasurement
    template_name = "grais/probe_measurement_confirm_delete.html"
    success_message = 'The probe measurement was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('grais:sample_detail', kwargs={'pk': self.object.sample.id})


# LINES #
#########

class LineCreateView(GraisAdminRequiredMixin, CreateView):
    model = models.Line
    form_class = forms.LineCreateForm
    template_name = 'grais/line_form.html'

    def get_initial(self):
        sample = models.Sample.objects.get(pk=self.kwargs['sample'])
        return {
            'sample': sample,
            'number_plates': 2,
            'number_petris': 3,
            'last_modified_by': self.request.user
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sample'] = models.Sample.objects.get(pk=self.kwargs["sample"])
        return context

    def form_valid(self, form):
        self.object = form.save()
        petris = form.cleaned_data['number_petris']
        plates = form.cleaned_data['number_plates']
        if petris + plates > 0:
            # create instances of surfaces on the collector lines
            # create iterable
            for i in range(petris):
                s = models.Surface.objects.create(line=self.object, surface_type='pe', label="Petri dish {}".format(i + 1))
                s.save()
            for i in range(plates):
                s = models.Surface.objects.create(line=self.object, surface_type='pl', label="Plate {}".format(i + 1))
                s.save()
        return HttpResponseRedirect(self.get_success_url())


class LineDetailView(GraisAccessRequiredMixin, DetailView):
    model = models.Line
    template_name = 'grais/line_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY
        return context


class LineUpdateView(GraisAdminRequiredMixin, UpdateView):
    model = models.Line
    form_class = forms.LineForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class LineDeleteView(GraisAdminRequiredMixin, DeleteView):
    model = models.Line
    template_name = "grais/line_confirm_delete.html"
    success_message = 'The line was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('grais:sample_detail', kwargs={'pk': self.object.sample.id})


# SPECIES #
###########

class SpeciesListView(GraisAccessRequiredMixin, FilterView):
    template_name = "grais/species_list.html"
    filterset_class = filters.SpeciesFilter
    queryset = models.Species.objects.annotate(
        search_term=Concat('id', 'common_name', 'scientific_name', 'abbrev', output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'id',
            'common_name',
            'common_name_fra',
            'scientific_name',
            'abbrev',
            'tsn|ITIS TSN',
            'aphia_id',
            'color_morph',
            'invasive',
            'Has occurred in db?',
        ]
        return context


class SpeciesDetailView(GraisAccessRequiredMixin, DetailView):
    model = models.Species
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'id',
            'common_name',
            'common_name_fra',
            'scientific_name',
            'abbrev',
            'epibiont_type',
            'color_morph',
            'invasive',
        ]
        return context


class SpeciesUpdateView(GraisAdminRequiredMixin, UpdateView):
    model = models.Species
    form_class = forms.SpeciesForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class SpeciesCreateView(GraisAdminRequiredMixin, CreateView):
    model = models.Species
    form_class = forms.SpeciesForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class SpeciesCreatePopoutView(GraisAdminRequiredMixin, CreateView):
    model = models.Species
    form_class = forms.SpeciesForm
    template_name = 'grais/species_form_popout.html'

    def get_initial(self):
        return {'last_modified_by': self.request.user}

    def form_valid(self, form):
        self.object = form.save()
        self.request.session['temp_msg'] = "The new species has been added to the list."

        return HttpResponseRedirect(reverse('grais:close_me'))


class SpeciesDeleteView(GraisAdminRequiredMixin, DeleteView):
    model = models.Species
    success_url = reverse_lazy('grais:species_list')
    success_message = 'The species was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# SURFACES #
############

class SurfaceDetailView(GraisAccessRequiredMixin, UpdateView):
    model = models.Surface
    form_class = forms.SurfaceImageForm
    template_name = 'grais/surface_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        surface = self.kwargs['pk']
        surface_spp = models.Surface.objects.get(id=surface).surface_spp.all()
        total_coverage = 0
        for sp in surface_spp:
            total_coverage += sp.percent_coverage

        context['total_coverage'] = total_coverage
        return context


class SurfaceUpdateView(GraisAdminRequiredMixin, UpdateView):
    model = models.Surface
    form_class = forms.SurfaceForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class SurfaceCreateView(GraisAdminRequiredMixin, CreateView):
    model = models.Surface
    form_class = forms.SurfaceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["line"] = models.Line.objects.get(pk=self.kwargs['line'])
        return context

    def get_initial(self):
        line = models.Line.objects.get(pk=self.kwargs['line'])
        return {
            'line': line,
            'last_modified_by': self.request.user
        }


class SurfaceDeleteView(GraisAdminRequiredMixin, DeleteView):
    model = models.Surface
    template_name = "grais/surface_confirm_delete.html"
    success_message = 'The surface was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('grais:line_detail', kwargs={'pk': self.object.line.id})


# SPECIES OBSERVATIONS (for sample and line level obs) #
########################################################

# this is shared between SampleSpecies and LineSpecies
class SpeciesObservationInsertView(GraisAdminRequiredMixin, TemplateView):
    template_name = "grais/species_obs_insert.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type = self.kwargs['type']
        pk = self.kwargs['pk']

        if type == "sample":
            sample = models.Sample.objects.get(pk=pk)
            context['sample'] = sample
            spp_list = sample.sample_spp.all()
            context['spp_list'] = spp_list
        elif type == "line":
            line = models.Line.objects.get(pk=pk)
            context['line'] = line
            spp_list = line.line_spp.all()
            context['spp_list'] = spp_list

        # get a list of species
        species_list = []
        for obj in models.Species.objects.all():
            if type == "sample":
                url = reverse("grais:spp_obs_new_pop", kwargs={"type": "sample", "pk": sample.id, "species": obj.id}),
            elif type == "line":
                url = reverse("grais:spp_obs_new_pop", kwargs={"type": "line", "pk": line.id, "species": obj.id}),

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


class SpeciesObservationCreatePopoutView(GraisAdminRequiredMixin, CreateView):
    template_name = 'grais/species_obs_form_popout.html'
    form_class = forms.SurfaceSpeciesForm

    def get_form_class(self):
        if self.kwargs["type"] == "sample":
            return forms.SampleSpeciesForm
        elif self.kwargs["type"] == "line":
            return forms.LineSpeciesForm

    def get_queryset(self):
        if self.kwargs["type"] == "sample":
            return models.Sample.objects.all()
        elif self.kwargs["type"] == "line":
            return models.Line.objects.all()

    def get_initial(self):
        my_dict = {}

        if self.kwargs["type"] == "sample":
            my_dict["sample"] = models.Sample.objects.get(pk=self.kwargs['pk'])
            my_dict['observation_date'] = my_dict["sample"].date_retrieved
        elif self.kwargs["type"] == "line":
            my_dict["line"] = models.Line.objects.get(pk=self.kwargs['pk'])
            my_dict['observation_date'] = my_dict["line"].sample.date_retrieved
        my_dict["species"] = models.Species.objects.get(pk=self.kwargs['species'])

        return my_dict

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs["type"] == "sample":
            context['sample'] = models.Sample.objects.all
        elif self.kwargs["type"] == "line":
            context['line'] = models.Line.objects.all

        species = models.Species.objects.get(id=self.kwargs['species'])
        context['species'] = species

        return context

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('grais:close_me'))


class SpeciesObservationUpdatePopoutView(GraisAdminRequiredMixin, UpdateView):
    template_name = 'grais/species_obs_form_popout.html'

    def get_form_class(self):
        if self.kwargs["type"] == "sample":
            return forms.SampleSpeciesForm
        elif self.kwargs["type"] == "line":
            return forms.LineSpeciesForm

    def get_queryset(self):
        if self.kwargs["type"] == "sample":
            return models.SampleSpecies.objects.all()
        elif self.kwargs["type"] == "line":
            return models.LineSpecies.objects.all()

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('grais:close_me'))


@login_required(login_url='/accounts/login/')
@user_passes_test(in_grais_admin_group, login_url='/accounts/denied/')
def species_observation_delete(request, type, pk, backto):
    if type == "sample":
        object = models.SampleSpecies.objects.get(pk=pk)
        linked_object = object.sample
        detail_url_name = "grais:sample_detail"
    elif type == "line":
        object = models.LineSpecies.objects.get(pk=pk)
        linked_object = object.line
        detail_url_name = "grais:line_detail"

    object.delete()
    messages.success(request, "The species has been successfully deleted from {}.".format(linked_object))

    if backto == "detail":
        return HttpResponseRedirect(reverse_lazy(detail_url_name, kwargs={"pk": linked_object.id}))
    else:
        return HttpResponseRedirect(reverse_lazy("grais:spp_obs_insert", kwargs={"type": type, "pk": linked_object.id}))


# SURFACE SPECIES #
###################

class SurfacaeSpeciesInsertView(GraisAdminRequiredMixin, TemplateView):
    template_name = "grais/surface_species_insert.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        surface = models.Surface.objects.get(pk=self.kwargs['surface'])
        context['surface'] = surface
        surface_spp = models.Surface.objects.get(pk=surface.id).surface_spp.all()
        context['surface_spp'] = surface_spp

        # get a list of species
        species_list = []
        for obj in models.Species.objects.all():
            html_insert = '<a class="add-btn btn btn-outline-dark" href="#" target-url="{}"> <img src="{}" alt=""></a><span style="margin-left: 10px;">{} / <em>{}</em> / {}</span>'.format(
                reverse("grais:surface_spp_new_pop", kwargs={"surface": surface.id, "species": obj.id}),
                static("admin/img/icon-addlink.svg"),
                obj.common_name,
                obj.scientific_name,
                obj.abbrev
            )
            species_list.append(html_insert)
        context['species_list'] = species_list

        total_coverage = 0
        for sp in surface_spp:
            total_coverage += sp.percent_coverage
        context['total_coverage'] = total_coverage

        return context


class SurfaceSpeciesCreatePopoutView(GraisAdminRequiredMixin, CreateView):
    model = models.SurfaceSpecies
    template_name = 'grais/surface_species_form_popout.html'
    form_class = forms.SurfaceSpeciesForm

    def get_initial(self):
        surface = models.Surface.objects.get(pk=self.kwargs['surface'])
        species = models.Species.objects.get(pk=self.kwargs['species'])
        return {
            'surface': surface,
            'species': species,
            'last_modified_by': self.request.user,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        species = models.Species.objects.get(id=self.kwargs['species'])
        context['species'] = species
        surface = models.Surface.objects.get(id=self.kwargs['surface'])
        context['surface'] = surface
        return context

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('grais:close_me'))


class SurfaceSpeciesUpdatePopoutView(GraisAdminRequiredMixin, UpdateView):
    model = models.SurfaceSpecies
    template_name = 'grais/surface_species_form_popout.html'
    form_class = forms.SurfaceSpeciesForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('grais:close_me'))


def surface_species_delete(request, pk, backto):
    object = models.SurfaceSpecies.objects.get(pk=pk)
    object.delete()
    messages.success(request, "The species has been successfully deleted from {}.".format(object.surface))

    if backto == "detail":
        return HttpResponseRedirect(reverse_lazy("grais:surface_detail", kwargs={"pk": object.surface.id}))
    else:
        return HttpResponseRedirect(reverse_lazy("grais:surface_spp_insert", kwargs={"surface": object.surface.id}))


# CSVs #
########

def export_csv_1(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response


# INCIDENTAL REPORT #
#####################

class ReportListView(GraisAccessRequiredMixin, FilterView):
    filterset_class = filters.ReportFilter
    template_name = "grais/report_list.html"


class ReportUpdateView(GraisAccessRequiredMixin, UpdateView):
    model = models.IncidentalReport
    form_class = forms.ReportForm
    template_name = "grais/report_form.html"

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class ReportCreateView(GraisAccessRequiredMixin, CreateView):
    model = models.IncidentalReport
    form_class = forms.ReportForm
    template_name = "grais/report_form.html"

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class ReportDetailView(GraisAccessRequiredMixin, DetailView):
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


class ReportDeleteView(GraisAccessRequiredMixin, DeleteView):
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

class FollowUpUpdateView(GraisAccessRequiredMixin, UpdateView):
    model = models.FollowUp
    form_class = forms.FollowUpForm
    template_name = 'grais/followup_form_popout.html'
    success_url = reverse_lazy("grais:close_me")


class FollowUpCreateView(GraisAccessRequiredMixin, CreateView):
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
@user_passes_test(in_grais_admin_group, login_url='/accounts/denied/')
def follow_up_delete(request, pk):
    followup = models.FollowUp.objects.get(pk=pk)
    followup.delete()
    messages.success(request, "The followup has been successfully deleted.")
    return HttpResponseRedirect(reverse_lazy("grais:report_detail", kwargs={"pk": followup.incidental_report_id}))


# ESTUARY #
###########

class EstuaryListView(GraisAccessRequiredMixin, FilterView):
    filterset_class = filters.EstuaryFilter
    template_name = "grais/estuary_list.html"


class EstuaryUpdateView(GraisAdminRequiredMixin, UpdateView):
    # permission_required = "__all__"
    raise_exception = True

    model = models.Estuary
    form_class = forms.EstuaryForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class EstuaryCreateView(GraisAdminRequiredMixin, CreateView):
    model = models.Estuary

    form_class = forms.EstuaryForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class EstuaryDetailView(GraisAccessRequiredMixin, DetailView):
    model = models.Estuary

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY

        field_list = [
            "id",
            "name",
            "province",
            "description",
        ]
        context['field_list'] = field_list

        site_list = [[site.code, site.latitude_n, site.longitude_w] for site in self.object.sites.all() if
                     site.latitude_n and site.longitude_w]
        context['site_list'] = site_list

        return context


class EstuaryDeleteView(GraisAdminRequiredMixin, DeleteView):
    model = models.Estuary
    success_url = reverse_lazy('grais:estuary_list')
    success_message = 'The sstuary was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# SITE #
########

class SiteUpdateView(GraisAdminRequiredMixin, UpdateView):
    # permission_required = "__all__"
    raise_exception = True

    model = models.Site
    form_class = forms.SiteForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}

    def get_success_url(self):
        return reverse_lazy('grais:estuary_detail', kwargs={'pk': self.object.estuary.id})


class SiteCreateView(GraisAdminRequiredMixin, CreateView):
    model = models.Site

    form_class = forms.SiteForm

    def get_initial(self):
        return {
            'estuary': self.kwargs['estuary'],
            'last_modified_by': self.request.user,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['estuary'] = models.Estuary.objects.get(pk=self.kwargs['estuary'])
        except KeyError:
            pass
        return context

    def get_success_url(self):
        return reverse_lazy('grais:estuary_detail', kwargs={'pk': self.object.estuary.id})


class SiteDetailView(GraisAccessRequiredMixin, DetailView):
    model = models.Site

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        field_list = [
            'estuary',
            'code',
            'name',
            'latitude_n',
            'longitude_w',
            'description',
        ]
        context['field_list'] = field_list
        return context


class SiteDeleteView(GraisAdminRequiredMixin, DeleteView):
    model = models.Site
    success_url = reverse_lazy('grais:site_list')
    success_message = 'The site was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('grais:estuary_detail', kwargs={'pk': self.object.estuary.id})


# SAMPLE #
##########
class GCSampleListView(GraisAccessRequiredMixin, FilterView):
    filterset_class = filters.GCSampleFilter
    template_name = "grais/gcsample_list.html"
    model = models.GCSample

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.GCSample.objects.first()
        context["field_list"] = [
            'season',
            'site',
            'traps_set|Traps set',
            'traps_fished|Traps fished',
        ]
        return context


class GCSampleDetailView(GraisAccessRequiredMixin, DetailView):
    model = models.GCSample

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY
        context["field_list"] = [
            'site',
            'traps_set',
            'traps_fished',
            'samplers',
            'eelgrass_assessed',
            'eelgrass_percent_coverage',
            'vegetation_species',
            'sediment',
            'season',
            'last_modified',
            'last_modified_by',
            'notes',
        ]
        return context


class GCSampleUpdateView(GraisAdminRequiredMixin, UpdateView):
    model = models.GCSample
    form_class = forms.GCSampleForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse_lazy("grais:gcsample_detail", kwargs={"pk": object.id}))


class GCSampleCreateView(GraisAdminRequiredMixin, CreateView):
    model = models.GCSample
    form_class = forms.GCSampleForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse_lazy("grais:gcsample_detail", kwargs={"pk": object.id}))


class GCSampleDeleteView(GraisAdminRequiredMixin, DeleteView):
    model = models.GCSample
    success_url = reverse_lazy('grais:gcsample_list')
    success_message = 'The sample was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# GC PROBE DATA #
##############

class GCProbeMeasurementCreateView(GraisAdminRequiredMixin, CreateView):
    model = models.GCProbeMeasurement
    form_class = forms.GCProbeMeasurementForm
    template_name = 'grais/gcprobe_measurement_form.html'

    def get_initial(self):
        gcsample = models.GCSample.objects.get(pk=self.kwargs['gcsample'])
        return {
            'sample': gcsample,
            'last_modified_by': self.request.user,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gcsample'] = models.GCSample.objects.get(pk=self.kwargs["gcsample"])
        return context

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse_lazy("grais:gcprobe_measurement_detail", kwargs={"pk": object.id}))


class GCProbeMeasurementDetailView(GraisAdminRequiredMixin, UpdateView):
    model = models.GCProbeMeasurement
    form_class = forms.GCProbeMeasurementForm
    template_name = 'grais/gcprobe_measurement_detail.html'


class GCProbeMeasurementUpdateView(GraisAdminRequiredMixin, UpdateView):
    model = models.GCProbeMeasurement
    form_class = forms.GCProbeMeasurementForm
    template_name = 'grais/gcprobe_measurement_form.html'

    def get_initial(self):
        return {'last_modified_by': self.request.user}

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse_lazy("grais:gcprobe_measurement_detail", kwargs={"pk": object.id}))


class GCProbeMeasurementDeleteView(GraisAdminRequiredMixin, DeleteView):
    model = models.GCProbeMeasurement
    template_name = "grais/gcprobe_measurement_confirm_delete.html"
    success_message = 'The probe measurement was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('grais:gcsample_detail', kwargs={'pk': self.object.sample.id})


# TRAP #
#########

class TrapCreateView(GraisAdminRequiredMixin, CreateView):
    model = models.Trap
    form_class = forms.TrapForm

    def get_initial(self):
        sample = models.GCSample.objects.get(pk=self.kwargs['gcsample'])
        return {
            'sample': sample,
            'last_modified_by': self.request.user
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gcsample'] = models.GCSample.objects.get(pk=self.kwargs["gcsample"])
        return context

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse_lazy("grais:trap_detail", kwargs={"pk": object.id}))


class TrapDetailView(GraisAccessRequiredMixin, DetailView, FormView):
    model = models.Trap
    form_class = forms.TrapSpeciesForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY
        context["field_list"] = [
            # 'sample',
            'trap_number',
            'trap_type',
            'bait_type',
            'depth_at_set_m',
            'latitude_n',
            'longitude_w',
            'gps_waypoint',
            'notes',
            'total_green_crab_wt_kg',
        ]

        context["crab_field_list"] = [
            'species',
            'width',
            'sex',
            'carapace_color',
            'abdomen_color',
            'egg_color',
            'notes',
        ]
        context["bycatch_field_list"] = [
            'species',
            'count',
            'notes',
        ]
        context["random_catch_object"] = models.Catch.objects.first
        # get a list of species

        return context


class TrapUpdateView(GraisAdminRequiredMixin, UpdateView):
    model = models.Trap
    form_class = forms.TrapForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse_lazy("grais:trap_detail", kwargs={"pk": object.id}))


class TrapDeleteView(GraisAdminRequiredMixin, DeleteView):
    model = models.Trap
    success_message = 'The trap was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('grais:gcsample_detail', kwargs={'pk': self.object.sample.id})


# CATCH #
#########

class CatchCreateViewPopout(GraisAdminRequiredMixin, FormView):
    template_name = 'grais/catch_form_popout.html'
    form_class = forms.NewCatchForm
    model = models.Catch

    def get_initial(self):
        my_dict = {}
        my_trap = models.Trap.objects.get(pk=self.kwargs['trap'])
        my_species = models.Species.objects.get(pk=self.kwargs['species'])
        my_dict["species"] = my_species
        my_dict["trap"] = my_trap
        # my_dict["last_modified_by"] = self.request.user.id

        # if this is a bycatch sp, let's look up the previous entry
        if not my_species.green_crab_monitoring:
            try:
                my_catch = models.Catch.objects.get(
                    species=my_species,
                    trap=my_trap,
                )
            except models.Catch.DoesNotExist:
                pass
            else:
                my_dict["notes"] = my_catch.notes
                my_dict["count"] = my_catch.count

        return my_dict

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_species = models.Species.objects.get(id=self.kwargs['species'])
        my_trap = models.Trap.objects.get(id=self.kwargs['trap'])
        context['species'] = my_species
        context['trap'] = my_trap
        return context

    def form_valid(self, form):
        my_species = models.Species.objects.get(id=self.kwargs['species'])
        my_trap = models.Trap.objects.get(id=self.kwargs['trap'])

        # if the species is a bycatch species, save all the data as a catch instance
        if not my_species.green_crab_monitoring:
            if form.cleaned_data.get("count"):
                my_catch, created = models.Catch.objects.get_or_create(
                    species=my_species,
                    trap=my_trap,
                )
                my_catch.count = form.cleaned_data.get("count")
                my_catch.notes = form.cleaned_data.get("notes")
                my_catch.last_modified_by = self.request.user
                my_catch.save()

        # if targeted species, lets create x number of blank entries
        else:
            for i in range(0, form.cleaned_data.get("count")):
                print("creating catch")
                models.Catch.objects.create(
                    species=my_species,
                    trap=my_trap,
                    last_modified_by=self.request.user,
                )

        return HttpResponseRedirect(reverse('grais:close_me'))


class CatchUpdateViewPopout(GraisAdminRequiredMixin, UpdateView):
    template_name = 'grais/catch_form_popout.html'
    form_class = forms.CatchForm
    model = models.Catch

    def get_initial(self):
        return {'last_modified_by': self.request.user.id}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('grais:close_me'))


@login_required(login_url='/accounts/login/')
@user_passes_test(in_grais_admin_group, login_url='/accounts/denied/')
def catch_delete(request, pk):
    my_catch = models.Catch.objects.get(pk=pk)
    my_catch.delete()
    messages.success(request, "The catch item has been successfully removed from this trap.")
    return HttpResponseRedirect(reverse_lazy("grais:trap_detail", kwargs={"pk": my_catch.trap.id}))


@login_required(login_url='/accounts/login/')
@user_passes_test(in_grais_admin_group, login_url='/accounts/denied/')
def manage_catch(request, trap, type):
    qs = models.Catch.objects.filter(trap_id=trap)
    context = dict()
    context["my_object"] = qs.first()
    context["trap"] = qs.first().trap

    if type == "invasive":
        qs = qs.filter(species__invasive=True, species__green_crab_monitoring=True)
        crab = True
    elif type == "noninvasive":
        qs = qs.filter(species__invasive=False, species__green_crab_monitoring=True)
        crab = True
    elif type == "bycatch":
        qs = qs.filter(species__green_crab_monitoring=False)
        crab = False

    if crab:
        context["field_list"] = [
            'width',
            'sex',
            'carapace_color',
            'abdomen_color',
            'egg_color',
            'notes',
        ]
    else:
        context["field_list"] = [
            'count',
            'notes',
        ]

    if request.method == 'POST':
        formset = forms.CatchFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "Items have been successfully updated")
            return HttpResponseRedirect(reverse("grais:manage_catch", kwargs={"trap": trap, "type": type}))
    else:
        formset = forms.CatchFormSet(queryset=qs)

    context['title'] = "Manage Catch"
    context['formset'] = formset
    return render(request, 'grais/manage_catch.html', context)


#
# # Bycatch #
# #########
#
# class BycatchCreateViewPopout(GraisAdminRequiredMixin, CreateView):
#     template_name = 'grais/crab_form_popout.html'
#     form_class = forms.BycatchForm
#     model = models.Catch
#
#     def get_initial(self):
#         my_dict = {}
#         my_dict["trap"] = models.Trap.objects.get(pk=self.kwargs['trap'])
#         my_dict["species"] = models.Species.objects.get(pk=self.kwargs['species'])
#         my_dict["last_modified_by"] = self.request.user.id
#         return my_dict
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         trap = models.Trap.objects.get(id=self.kwargs['trap'])
#         species = models.Species.objects.get(id=self.kwargs['species'])
#         context['species'] = species
#         context['trap'] = trap
#         return context
#
#     def form_valid(self, form):
#         self.object = form.save()
#         return HttpResponseRedirect(reverse('grais:close_me'))
#
#
# class BycatchUpdateViewPopout(GraisAdminRequiredMixin, CreateView):
#     template_name = 'grais/crab_form_popout.html'
#     form_class = forms.BycatchForm
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
# @user_passes_test(in_grais_admin_group, login_url='/accounts/denied/')
# def bycatch_delete(request, pk):
#     bycatch = models.Catch.objects.get(pk=pk)
#     bycatch.delete()
#     messages.success(request, "The bycatch has been successfully removed from this trap.")
#     return HttpResponseRedirect(reverse_lazy("grais:trap_detail", kwargs={"pk": bycatch.trap.id}))


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
