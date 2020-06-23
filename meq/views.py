# import csv
#
# from django.conf import settings
# from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# from django.contrib.staticfiles.templatetags.staticfiles import static
# from django.db.models import TextField, Value
# from django.db.models.functions import Concat
# from django.http import HttpResponse, HttpResponseRedirect
#
# from braces.views import GroupRequiredMixin
# from django.views.generic import ListView,  UpdateView, DeleteView, CreateView, DetailView, TemplateView
# from django.urls import reverse_lazy, reverse
# from django_filters.views import FilterView
# from django.utils import timezone
# from . import models
# from . import forms
# from . import filters
#
# class IndexView(GroupRequiredMixin,TemplateView):
#     template_name = 'grais/index.html'
#     group_required = [u"grais_access",]
#
#
#
# class DataFlowTemplateView(TemplateView):
#     template_name = 'grais/dataflow.html'
#
#
# # SAMPLE #
# ##########
# class CloserTemplateView(TemplateView):
#     template_name = 'grais/close_me.html'
#
#
# class SampleListView(LoginRequiredMixin, FilterView):
#     filterset_class = filters.SampleFilter
#     template_name = "grais/sample_list.html"
#
#
#     # def get_filterset_kwargs(self, filterset_class):
#     #     kwargs = super().get_filterset_kwargs(filterset_class)
#     #     if kwargs["data"] is None:
#     #         kwargs["data"] = {"SeasonExact": timezone.now().year-2 }
#     #     return kwargs
#
# class SampleDetailView(LoginRequiredMixin, DetailView):
#     model = models.Sample
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['google_api_key'] = settings.GOOGLE_API_KEY
#         sampler_field_list = [
#             'first_name',
#             'last_name',
#             'email',
#             'phone',
#             'organization',
#
#         ]
#         context["sampler_field_list"] = sampler_field_list
#         return context
#
# class SampleUpdateView(LoginRequiredMixin, UpdateView):
#     model = models.Sample
#     form_class = forms.SampleForm
#
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
# class SampleCreateView(LoginRequiredMixin, CreateView):
#     model = models.Sample
#     form_class = forms.SampleForm
#
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
# class SampleDeleteView(LoginRequiredMixin, DeleteView):
#     model = models.Sample
#     success_url = reverse_lazy('grais:sample_list')
#     success_message = 'The sample was successfully deleted!'
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
#
#
# # SAMPLE NOTE #
# ##############
#
# class SampleNoteUpdateView(LoginRequiredMixin, UpdateView):
#     model = models.SampleNote
#
#     form_class = forms.SampleNoteForm
#
#
# class SampleNoteCreateView(LoginRequiredMixin, CreateView):
#     model = models.SampleNote
#
#     form_class = forms.SampleNoteForm
#
#     def get_context_data(self, **kwargs):
#         context = super(SampleNoteCreateView, self).get_context_data(**kwargs)
#         context["sample"] = models.Sample.objects.get(pk=self.kwargs["sample"])
#         return context
#
#     def get_initial(self):
#         sample = models.Sample.objects.get(pk=self.kwargs["sample"])
#         return {
#             "sample":sample,
#             "author": self.request.user
#         }
#
#
# def sample_note_delete(request, pk):
#     note = models.SampleNote.objects.get(pk=pk)
#     note.delete()
#     messages.success(request, "The note has been successfully deleted.")
#     return HttpResponseRedirect(reverse_lazy("grais:sample_detail", kwargs={"pk":note.sample_id}))
#
#
# # STATION #
# ###########
#
# class StationListView(LoginRequiredMixin, FilterView):
#     filterset_class = filters.StationFilter
#     template_name = "grais/station_list.html"
#
#
# class StationUpdateView(LoginRequiredMixin,  UpdateView):
#     # permission_required = "__all__"
#     raise_exception = True
#
#     model = models.Station
#     form_class = forms.StationForm
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
# class StationCreateView(LoginRequiredMixin, CreateView):
#     model = models.Station
#
#     form_class = forms.StationForm
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
# class StationDetailView(LoginRequiredMixin, UpdateView):
#     model = models.Station
#
#     fields =('__all__')
#     template_name = 'grais/station_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['google_api_key'] = settings.GOOGLE_API_KEY
#         return context
#
# class StationDeleteView(LoginRequiredMixin, DeleteView):
#     model = models.Station
#     success_url = reverse_lazy('grais:station_list')
#     success_message = 'The station was successfully deleted!'
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
#
#
# # PERSON #
# ##########
#
# class PersonUpdateView(LoginRequiredMixin, UpdateView):
#     model = models.Sampler
#
#     fields =('__all__')
#     template_name = 'grais/person_form_popout.html'
#     success_url = reverse_lazy("grais:close_me")
#
# class PersonCreateView(LoginRequiredMixin, CreateView):
#     model = models.Sampler
#
#     fields =('__all__')
#     template_name = 'grais/person_form_popout.html'
#     success_url = reverse_lazy("grais:close_me")
#
#
# class PersonDetailView(LoginRequiredMixin, UpdateView):
#     model = models.Sampler
#
#     template_name = 'grais/person_detail_popout.html'
#     fields =('__all__')
#
#
# # PROBE DATA #
# ##############
#
# class ProbeMeasurementCreateView(LoginRequiredMixin, CreateView):
#     model = models.ProbeMeasurement
#     form_class = forms.ProbeMeasurementForm
#
#     template_name = 'grais/probe_measurement_form.html'
#
#     def get_initial(self):
#         sample = models.Sample.objects.get(pk=self.kwargs['sample'])
#         return {
#             'sample': sample,
#             'last_modified_by': self.request.user,
#             }
#
#
# class ProbeMeasurementDetailView(LoginRequiredMixin, UpdateView):
#     model = models.ProbeMeasurement
#     form_class = forms.ProbeMeasurementForm
#
#     template_name = 'grais/probe_measurement_detail.html'
#
# class ProbeMeasurementUpdateView(LoginRequiredMixin, UpdateView):
#     model = models.ProbeMeasurement
#     form_class = forms.ProbeMeasurementForm
#
#     template_name = 'grais/probe_measurement_form.html'
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
#
# class ProbeMeasurementDeleteView(LoginRequiredMixin, DeleteView):
#
#     model = models.ProbeMeasurement
#     template_name = "grais/probe_measurement_confirm_delete.html"
#     success_message = 'The probe measurement was successfully deleted!'
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
#
#     def get_success_url(self):
#         return reverse_lazy('grais:sample_detail', kwargs={'pk':self.object.sample.id})
#
#
# # LINES #
# #########
#
# class LineCreateView(LoginRequiredMixin, CreateView):
#     model = models.Line
#     form_class = forms.LineCreateForm
#
#     template_name = 'grais/line_form.html'
#
#     def get_initial(self):
#         sample = models.Sample.objects.get(pk=self.kwargs['sample'])
#         return {
#             'sample': sample,
#             'number_plates':2,
#             'number_petris':3,
#             'last_modified_by': self.request.user
#             }
#
#     def form_valid(self, form):
#         self.object = form.save()
#         petris = form.cleaned_data['number_petris']
#         plates = form.cleaned_data['number_plates']
#         if petris+plates > 0:
#             # create instances of surfaces on the collector lines
#             # create iterable
#             for i in range(petris):
#                 s = models.Surface.objects.create(line=self.object, surface_type = 'pe', label="Petri dish {}".format(i+1) )
#                 s.save()
#             for i in range(plates):
#                 s = models.Surface.objects.create(line=self.object, surface_type = 'pl', label="Plate {}".format(i+1) )
#                 s.save()
#         return HttpResponseRedirect(self.get_success_url())
#
# class LineDetailView(LoginRequiredMixin, DetailView):
#     model = models.Line
#
#     template_name = 'grais/line_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['google_api_key'] = settings.GOOGLE_API_KEY
#         return context
#
# class LineUpdateView(LoginRequiredMixin, UpdateView):
#     model = models.Line
#     form_class = forms.LineForm
#
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
#
# class LineDeleteView(LoginRequiredMixin, DeleteView):
#
#     model = models.Line
#     template_name = "grais/line_confirm_delete.html"
#     success_message = 'The line was successfully deleted!'
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
#
#     def get_success_url(self):
#         return reverse_lazy('grais:sample_detail', kwargs={'pk':self.object.sample.id})
#
#
#
# # SPECIES #
# ###########
#
# class SpeciesListView(LoginRequiredMixin, FilterView):
#     template_name = "grais/species_list.html"
#     filterset_class = filters.SpeciesFilter
#
#     queryset = models.Species.objects.annotate(
#         search_term=Concat('common_name', 'scientific_name', 'abbrev', output_field=TextField()))
#
# class SpeciesDetailView(LoginRequiredMixin, DetailView):
#     model = models.Species
#     fields = "__all__"
#
#
#     def get_context_data(self, **kwargs):
#         context = super(SpeciesDetailView, self).get_context_data(**kwargs)
#         context["field_list"] = [
#             'common_name',
#             'scientific_name',
#             'abbrev',
#             'epibiont_type',
#             'color_morph',
#             'invasive',
#         ]
#         return context
#
# class SpeciesUpdateView(LoginRequiredMixin, UpdateView):
#     model = models.Species
#
#     form_class = forms.SpeciesForm
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
# class SpeciesCreateView(LoginRequiredMixin, CreateView):
#     model = models.Species
#
#     form_class = forms.SpeciesForm
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
# class SpeciesCreatePopoutView(LoginRequiredMixin, CreateView):
#     model = models.Species
#
#     form_class = forms.SpeciesForm
#     template_name = 'grais/species_form_popout.html'
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
#     def form_valid(self, form):
#         self.object = form.save()
#         self.request.session['temp_msg'] = "The new species has been added to the list."
#
#         return HttpResponseRedirect(reverse('grais:close_me'))
#
# class SpeciesDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
#     model = models.Species
#     permission_required = "__all__"
#     success_url = reverse_lazy('grais:species_list')
#     success_message = 'The species was successfully deleted!'
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
#
# # SURFACES #
# ############
#
# class SurfaceDetailView(LoginRequiredMixin, UpdateView):
#     model = models.Surface
#     form_class = forms.SurfaceImageForm
#
#     template_name = 'grais/surface_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         surface = self.kwargs['pk']
#         surface_spp = models.Surface.objects.get(id=surface).surface_spp.all()
#         total_coverage = 0
#         for sp in surface_spp:
#             total_coverage += sp.percent_coverage
#
#         context['total_coverage']= total_coverage
#         return context
#
# class SurfaceUpdateView(LoginRequiredMixin, UpdateView):
#     model = models.Surface
#     form_class = forms.SurfaceForm
#
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
# class SurfaceCreateView(LoginRequiredMixin, CreateView):
#     model = models.Surface
#     form_class = forms.SurfaceForm
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["line"] = models.Line.objects.get(pk=self.kwargs['line'])
#         return context
#
#     def get_initial(self):
#         line = models.Line.objects.get(pk=self.kwargs['line'])
#         return {
#             'line': line,
#             'last_modified_by': self.request.user
#         }
#
# class SurfaceDeleteView(LoginRequiredMixin, DeleteView):
#
#     model = models.Surface
#     template_name = "grais/surface_confirm_delete.html"
#     success_message = 'The surface was successfully deleted!'
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
#
#     def get_success_url(self):
#         return reverse_lazy('grais:line_detail', kwargs={'pk':self.object.line.id})
#
#
# # SPECIES OBSERVATIONS (for sample and line level obs) #
# ########################################################
#
# # this is shared between SampleSpecies and LineSpecies
# class SpeciesObservationInsertView(TemplateView):
#     template_name = "grais/species_obs_insert.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         type = self.kwargs['type']
#         pk = self.kwargs['pk']
#
#         if type == "sample":
#             sample = models.Sample.objects.get(pk=pk)
#             context['sample'] = sample
#             spp_list = sample.sample_spp.all()
#             context['spp_list'] = spp_list
#         elif type == "line":
#             line = models.Line.objects.get(pk=pk)
#             context['line'] = line
#             spp_list = line.line_spp.all()
#             context['spp_list'] = spp_list
#
#
#
#
#         # get a list of species
#         species_list = []
#         for obj in models.Species.objects.all():
#             if type == "sample":
#                 url = reverse("grais:spp_obs_new_pop", kwargs={"type":"sample", "pk": sample.id, "species": obj.id}),
#             elif type == "line":
#                 url = reverse("grais:spp_obs_new_pop", kwargs={"type":"line","pk": line.id, "species": obj.id}),
#
#             html_insert = '<a class="add-btn btn btn-outline-dark" href="#" target-url="{}"> <img src="{}" alt=""></a><span style="margin-left: 10px;">{} / <em>{}</em> / {}</span>'.format(
#                 url[0],
#                 static("admin/img/icon-addlink.svg"),
#                 obj.common_name,
#                 obj.scientific_name,
#                 obj.abbrev
#             )
#             species_list.append(html_insert)
#         context['species_list'] = species_list
#
#         return context
#
#
# class SpeciesObservationCreatePopoutView(LoginRequiredMixin,CreateView):
#     template_name ='grais/species_obs_form_popout.html'
#
#     form_class = forms.SurfaceSpeciesForm
#
#     def get_form_class(self):
#         if self.kwargs["type"]=="sample":
#             return forms.SampleSpeciesForm
#         elif self.kwargs["type"]=="line":
#             return forms.LineSpeciesForm
#
#
#     def get_queryset(self):
#         if self.kwargs["type"]=="sample":
#             return models.Sample.objects.all()
#         elif self.kwargs["type"]=="line":
#             return models.Line.objects.all()
#
#     def get_initial(self):
#         my_dict = {}
#
#         if self.kwargs["type"]=="sample":
#             my_dict["sample"] = models.Sample.objects.get(pk=self.kwargs['pk'])
#             my_dict['observation_date'] = my_dict["sample"].date_retrieved
#         elif self.kwargs["type"]=="line":
#             my_dict["line"] = models.Line.objects.get(pk=self.kwargs['pk'])
#             my_dict['observation_date'] = my_dict["line"].sample.date_retrieved
#         my_dict["species"] = models.Species.objects.get(pk=self.kwargs['species'])
#
#         return my_dict
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         if self.kwargs["type"]=="sample":
#             context['sample'] = models.Sample.objects.all
#         elif self.kwargs["type"]=="line":
#             context['line'] = models.Line.objects.all
#
#         species = models.Species.objects.get(id=self.kwargs['species'])
#         context['species']= species
#
#         return context
#
#     def form_valid(self, form):
#         self.object = form.save()
#         return HttpResponseRedirect(reverse('grais:close_me'))
#
# class SpeciesObservationUpdatePopoutView(LoginRequiredMixin,UpdateView):
#     template_name ='grais/species_obs_form_popout.html'
#
#     def get_form_class(self):
#         if self.kwargs["type"]=="sample":
#             return forms.SampleSpeciesForm
#         elif self.kwargs["type"]=="line":
#             return forms.LineSpeciesForm
#
#     def get_queryset(self):
#         if self.kwargs["type"]=="sample":
#             return models.SampleSpecies.objects.all()
#         elif self.kwargs["type"]=="line":
#             return models.LineSpecies.objects.all()
#
#     def form_valid(self, form):
#         self.object = form.save()
#         return HttpResponseRedirect(reverse('grais:close_me'))
#
#
# def species_observation_delete(request,type,pk,backto):
#     if type == "sample":
#         object = models.SampleSpecies.objects.get(pk=pk)
#         linked_object = object.sample
#         detail_url_name = "grais:sample_detail"
#     elif type == "line":
#         object = models.LineSpecies.objects.get(pk=pk)
#         linked_object = object.line
#         detail_url_name = "grais:line_detail"
#
#     object.delete()
#     messages.success(request, "The species has been successfully deleted from {}.".format(linked_object))
#
#     if backto == "detail":
#         return HttpResponseRedirect(reverse_lazy(detail_url_name, kwargs={"pk": linked_object.id}))
#     else:
#         return HttpResponseRedirect(reverse_lazy("grais:spp_obs_insert", kwargs={"type":type, "pk":linked_object.id}))
#
#
#
# # SURFACE SPECIES #
# ###################
#
# class SurfacaeSpeciesInsertView(TemplateView):
#     template_name = "grais/surface_species_insert.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         surface = models.Surface.objects.get(pk=self.kwargs['surface'])
#         context['surface']= surface
#         surface_spp = models.Surface.objects.get(pk=surface.id).surface_spp.all()
#         context['surface_spp']= surface_spp
#
#         # get a list of species
#         species_list = []
#         for obj in models.Species.objects.all():
#             html_insert = '<a class="add-btn btn btn-outline-dark" href="#" target-url="{}"> <img src="{}" alt=""></a><span style="margin-left: 10px;">{} / <em>{}</em> / {}</span>'.format(
#                 reverse("grais:surface_spp_new_pop", kwargs={"surface":surface.id, "species":obj.id}),
#                 static("admin/img/icon-addlink.svg"),
#                 obj.common_name,
#                 obj.scientific_name,
#                 obj.abbrev
#             )
#             species_list.append(html_insert)
#         context['species_list'] = species_list
#
#         total_coverage = 0
#         for sp in surface_spp:
#             total_coverage += sp.percent_coverage
#         context['total_coverage']= total_coverage
#
#         return context
#
#
# class SurfaceSpeciesCreatePopoutView(LoginRequiredMixin,CreateView):
#     model = models.SurfaceSpecies
#     template_name ='grais/surface_species_form_popout.html'
#
#     form_class = forms.SurfaceSpeciesForm
#
#     def get_initial(self):
#         surface = models.Surface.objects.get(pk=self.kwargs['surface'])
#         species = models.Species.objects.get(pk=self.kwargs['species'])
#         return {
#             'surface': surface,
#             'species': species,
#             'last_modified_by': self.request.user,
#             }
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         species = models.Species.objects.get(id=self.kwargs['species'])
#         context['species']= species
#         surface = models.Surface.objects.get(id=self.kwargs['surface'])
#         context['surface'] = surface
#         return context
#
#     def form_valid(self, form):
#         self.object = form.save()
#         return HttpResponseRedirect(reverse('grais:close_me'))
#
# class SurfaceSpeciesUpdatePopoutView(LoginRequiredMixin,UpdateView):
#     model = models.SurfaceSpecies
#     template_name ='grais/surface_species_form_popout.html'
#     form_class = forms.SurfaceSpeciesForm
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
#     def form_valid(self, form):
#         self.object = form.save()
#         return HttpResponseRedirect(reverse('grais:close_me'))
#
#
# def surface_species_delete(request,pk,backto):
#     object = models.SurfaceSpecies.objects.get(pk=pk)
#     object.delete()
#     messages.success(request, "The species has been successfully deleted from {}.".format(object.surface))
#
#     if backto == "detail":
#         return HttpResponseRedirect(reverse_lazy("grais:surface_detail", kwargs={"pk": object.surface.id}))
#     else:
#         return HttpResponseRedirect(reverse_lazy("grais:surface_spp_insert", kwargs={"surface":object.surface.id}))
#
#
#
# # CSVs #
# ########
#
# def export_csv_1(request):
#     # Create the HttpResponse object with the appropriate CSV header.
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
#
#     writer = csv.writer(response)
#     writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
#     writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
#
#     return response
#
#
# # INCIDENTAL REPORT #
# #####################
#
# class ReportListView(LoginRequiredMixin, FilterView):
#     filterset_class = filters.ReportFilter
#     template_name = "grais/report_list.html"
#
#
#
# class ReportUpdateView(LoginRequiredMixin,  UpdateView):
#
#     model = models.IncidentalReport
#     form_class = forms.ReportForm
#     template_name = "grais/report_form.html"
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
#
# class ReportCreateView(LoginRequiredMixin, CreateView):
#     model = models.IncidentalReport
#
#     form_class = forms.ReportForm
#     template_name = "grais/report_form.html"
#
#     def get_initial(self):
#         return {'last_modified_by': self.request.user}
#
#
# class ReportDetailView(LoginRequiredMixin, DetailView):
#     model = models.IncidentalReport
#
#     template_name = "grais/report_detail.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['google_api_key'] = settings.GOOGLE_API_KEY
#
#         field_list = [
#             "report_date",
#             "requestor_name",
#             "report_source",
#             "language_of_report",
#             "call_answered_by",
#             "call_returned_by",
#             "location_description",
#             "latitude_n",
#             "longitude_w",
#             "specimens_retained",
#             "sighting_description",
#             "identified_by",
#             "date_of_occurrence",
#             "observation_type",
#             "phone",
#             "email",
#             "notes",
#             "date_last_modified",
#             "last_modified_by",
#         ]
#
#         context["field_list"] = field_list
#
#         return context
#
#
# class ReportDeleteView(LoginRequiredMixin, DeleteView):
#     model = models.IncidentalReport
#     success_url = reverse_lazy('grais:report_list')
#     success_message = 'The report was successfully deleted!'
#     template_name = "grais/report_confirm_delete.html"
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
#
