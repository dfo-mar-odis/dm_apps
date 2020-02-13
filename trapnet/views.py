import unicodecsv as csv
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db.models import Count, TextField, Value
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView, TemplateView, FormView
from easy_pdf.views import PDFTemplateView
from django_filters.views import FilterView
from shared_models import models as shared_models
from . import models
from . import forms
from . import filters
from . import reports
from lib.functions.custom_functions import nz, listrify
from django.utils.encoding import smart_str


# open basic access up to anybody who is logged in
def in_trapnet_group(user):
    if user:
        return user.groups.filter(name='trapnet_access').count() != 0


class TrapNetAccessRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return in_trapnet_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


def in_trapnet_admin_group(user):
    if user:
        return user.groups.filter(name='trapnet_admin').count() != 0


class TrapNetAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return in_trapnet_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class IndexTemplateView(TrapNetAccessRequiredMixin, TemplateView):
    template_name = 'trapnet/index.html'


# SPECIES #
###########

class SpeciesListView(TrapNetAccessRequiredMixin, FilterView):
    template_name = "trapnet/species_list.html"
    filterset_class = filters.SpeciesFilter
    queryset = models.Species.objects.annotate(
        search_term=Concat('common_name_eng', 'common_name_fre', 'scientific_name', 'code', 'abbrev', output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_object'] = models.Species.objects.first()
        context["field_list"] = [
            'code',
            'full_name|Species',
            'scientific_name',
            'abbrev',
            'tsn',
            'aphia_id',
        ]
        return context


class SpeciesDetailView(TrapNetAccessRequiredMixin, DetailView):
    model = models.Species

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY
        context["field_list"] = [
            'code',
            'common_name_eng',
            'common_name_fre',
            'life_stage',
            'abbrev',
            'scientific_name',
            'tsn',
            'aphia_id',
            'notes',
        ]

        return context


class SpeciesUpdateView(TrapNetAdminRequiredMixin, UpdateView):
    model = models.Species

    form_class = forms.SpeciesForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class SpeciesCreateView(TrapNetAdminRequiredMixin, CreateView):
    model = models.Species

    form_class = forms.SpeciesForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class SpeciesDeleteView(TrapNetAdminRequiredMixin, DeleteView):
    model = models.Species
    permission_required = "__all__"
    success_url = reverse_lazy('trapnet:species_list')
    success_message = 'The species was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# RIVER #
#########

class RiverListView(TrapNetAccessRequiredMixin, FilterView):
    filterset_class = filters.RiverFilter
    template_name = 'trapnet/river_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        field_list = [
            'name',
            'fishing_area_code',
            'maritime_river_code',
            'old_maritime_river_code',
            'cgndb',
            'parent_cgndb_id',
            'nbadw_water_body_id',
            'display_hierarchy|River hierarchy',
        ]
        context['field_list'] = field_list
        context['my_object'] = shared_models.River.objects.first()
        return context


class RiverUpdateView(TrapNetAdminRequiredMixin, UpdateView):
    model = shared_models.River
    form_class = forms.RiverForm
    template_name = 'trapnet/river_form.html'

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class RiverCreateView(TrapNetAdminRequiredMixin, CreateView):
    model = shared_models.River
    form_class = forms.RiverForm
    template_name = 'trapnet/river_form.html'

    def get_initial(self):
        return {'last_modified_by': self.request.user}

    def form_valid(self, form):
        my_object = form.save()
        return HttpResponseRedirect(reverse_lazy("trapnet:river_detail", kwargs={"pk": my_object.id}))


class RiverDetailView(TrapNetAccessRequiredMixin, DetailView):
    model = shared_models.River
    template_name = 'trapnet/river_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY

        field_list = [
            'name',
            'fishing_area_code',
            'maritime_river_code',
            'old_maritime_river_code',
            'cgndb',
            'parent_cgndb_id',
            'nbadw_water_body_id',
            'display_anchored_hierarchy|River hierarchy',

        ]
        context['field_list'] = field_list

        context['site_field_list'] = [
            'name',
            'stream_order',
            'elevation_m',
            'province.abbrev_eng',
            'latitude_n',
            'longitude_w',
            'directions',
        ]
        context['my_site_object'] = models.RiverSite.objects.first()

        site_list = [[obj.name, obj.latitude_n, obj.longitude_w] for obj in self.object.river_sites.all() if
                     obj.latitude_n and obj.longitude_w]
        context['site_list'] = site_list

        return context


class RiverDeleteView(TrapNetAdminRequiredMixin, DeleteView):
    model = shared_models.River
    success_url = reverse_lazy('trapnet:river_list')
    success_message = 'The river was successfully deleted!'
    template_name = 'trapnet/river_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# SITE #
########

class RiverSiteUpdateView(TrapNetAdminRequiredMixin, UpdateView):
    model = models.RiverSite
    form_class = forms.RiverSiteForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}

    def form_valid(self, form):
        my_object = form.save()
        return HttpResponseRedirect(reverse_lazy("trapnet:site_detail", kwargs={"pk": my_object.id}))


class RiverSiteCreateView(TrapNetAdminRequiredMixin, CreateView):
    model = models.RiverSite

    form_class = forms.RiverSiteForm

    def get_initial(self):
        return {'river': self.kwargs.get("river")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get("river"):
            river = shared_models.River.objects.get(pk=self.kwargs["river"])
            context['river'] = river
        return context

    def form_valid(self, form):
        my_object = form.save()
        return HttpResponseRedirect(reverse_lazy("trapnet:site_detail", kwargs={"pk": my_object.id}))


class RiverSiteDetailView(TrapNetAdminRequiredMixin, DetailView):
    model = models.RiverSite

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY

        field_list = [
            'name',
            'river',
            'stream_order',
            'elevation_m',
            'province.abbrev_eng',
            'latitude_n',
            'longitude_w',
            'directions',
            'exclude_data_from_site',
        ]
        context['field_list'] = field_list

        return context


class RiverSiteDeleteView(TrapNetAdminRequiredMixin, DeleteView):
    model = models.RiverSite
    success_message = 'The river site was successfully deleted!'

    def get_success_url(self):
        return reverse_lazy("trapnet:site_detail", kwargs={"pk": self.object.site.id})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# SAMPLE #
##########

class SampleListView(TrapNetAccessRequiredMixin, FilterView):
    filterset_class = filters.SampleFilter
    template_name = 'trapnet/sample_list.html'
    queryset = models.Sample.objects.filter(site__exclude_data_from_site=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        field_list = [
            'season',
            'sample_type',
            'site',
            'arrival_date',
            'departure_date',
        ]
        context['field_list'] = field_list
        context['my_object'] = models.Sample.objects.first()
        return context


class SampleUpdateView(TrapNetAdminRequiredMixin, UpdateView):
    model = models.Sample
    form_class = forms.SampleForm
    template_name = 'trapnet/sample_form.html'

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class SampleCreateView(TrapNetAdminRequiredMixin, CreateView):
    model = models.Sample
    form_class = forms.SampleForm
    template_name = 'trapnet/sample_form.html'

    def get_initial(self):
        return {
            'last_modified_by': self.request.user,
        }

    def form_valid(self, form):
        my_object = form.save()
        return HttpResponseRedirect(reverse_lazy("trapnet:trap_detail", kwargs={"pk": my_object.id}))


class SampleDetailView(TrapNetAccessRequiredMixin, DetailView):
    model = models.Sample
    template_name = 'trapnet/sample_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY

        field_list = [
            'site',
            'sample_type',
            'arrival_date',
            'departure_date',
            'air_temp_arrival',
            'min_air_temp',
            'max_air_temp',
            'percent_cloud_cover',
            'precipitation_category',
            'precipitation_comment',
            'wind_speed',
            'wind_direction',
            'water_depth_m',
            'water_level_delta_m',
            'discharge_m3_sec',
            'water_temp_shore_c',
            'water_temp_trap_c',
            'rpm_arrival',
            'rpm_departure',
            'operating_condition',
            'operating_condition_comment',
            'notes',
            'season',
            'last_modified',
            'last_modified_by',
        ]
        context['field_list'] = field_list

        context['obs_field_list'] = [
            'species',
            'status',
            'origin',
            'frequency',
            'fork_length',
            'total_length',
        ]
        context['my_obs_object'] = models.Entry.objects.first()

        return context


class SampleDeleteView(TrapNetAdminRequiredMixin, DeleteView):
    model = models.Sample
    success_url = reverse_lazy('trapnet:trap_list')
    success_message = 'The sample was successfully deleted!'
    template_name = 'trapnet/sample_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# OBSERVATIONS #
################

class EntryInsertView(TrapNetAccessRequiredMixin, TemplateView):
    template_name = "trapnet/obs_insert.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sample = models.Sample.objects.get(pk=self.kwargs['sample'])
        context['sample'] = sample

        queryset = models.Species.objects.all()
        # get a list of species
        species_list = []
        for obj in queryset:
            html_insert = '<a class="add-btn btn btn-outline-dark" href="#" target-url="{}"> <img src="{}" alt=""></a><span style="margin-left: 10px;">{} - {} - <em>{}</em> </span>'.format(
                reverse("trapnet:obs_new", kwargs={"sample": sample.id, "species": obj.id}),
                static("admin/img/icon-addlink.svg"),
                obj.code,
                str(obj),
                obj.scientific_name,
            )
            species_list.append(html_insert)
        context['species_list'] = species_list
        context['obs_field_list'] = [
            'species',
            'first_tag',
            'last_tag',
            'status',
            'origin',
            'frequency',
            'fork_length',
            'total_length',
            'weight',
            'sex',
            'smolt_age',
            'location_tagged',
            'date_tagged',
            'scale_id_number',
            'tags_removed',
            'notes',
        ]
        context['my_obs_object'] = models.Entry.objects.first()
        return context


class EntryCreateView(TrapNetAccessRequiredMixin, CreateView):
    model = models.Entry
    template_name = 'trapnet/obs_form_popout.html'
    form_class = forms.EntryForm

    def get_initial(self):
        sample = models.Sample.objects.get(pk=self.kwargs['sample'])
        species = models.Species.objects.get(pk=self.kwargs['species'])
        return {
            'sample': sample,
            'species': species,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        species = models.Species.objects.get(id=self.kwargs['species'])
        sample = models.Sample.objects.get(id=self.kwargs['sample'])
        context['species'] = species
        context['sample'] = sample
        return context

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('shared_models:close_me'))


class EntryUpdateView(TrapNetAccessRequiredMixin, UpdateView):
    model = models.Entry
    template_name = 'trapnet/obs_form_popout.html'
    form_class = forms.EntryForm

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('shared_models:close_me'))


def species_observation_delete(request, pk, backto):
    object = models.Entry.objects.get(pk=pk)
    object.delete()
    messages.success(request, "The species has been successfully deleted from {}.".format(object.sample))

    if backto == "detail":
        return HttpResponseRedirect(reverse_lazy("trapnet:sample_detail", kwargs={"pk": object.sample.id}))
    else:
        return HttpResponseRedirect(reverse_lazy("trapnet:species_obs_search", kwargs={"sample": object.sample.id}))


# REPORTS #
###########

class ReportSearchFormView(TrapNetAccessRequiredMixin, FormView):
    template_name = 'trapnet/report_search.html'
    form_class = forms.ReportSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        # ais_species_list = str(form.cleaned_data["ais_species"]).replace("[", "").replace("]", "").replace(" ", "").replace("'","").replace('"',"")

        report = int(form.cleaned_data["report"])
        my_year = form.cleaned_data["year"] if form.cleaned_data["year"] else "None"
        my_sites = listrify(form.cleaned_data["sites"]) if len(form.cleaned_data["sites"]) > 0 else "None"

        if report == 1:
            return HttpResponseRedirect(reverse("trapnet:sample_report", kwargs={"year": my_year, "sites": my_sites}))
        elif report == 2:
            return HttpResponseRedirect(reverse("trapnet:entry_report", kwargs={"year": my_year, "sites": my_sites}))
        elif report == 3:
            return HttpResponseRedirect(reverse("trapnet:od1_report", kwargs={"year": my_year, "sites": my_sites}))
        elif report == 4:
            return HttpResponseRedirect(reverse("trapnet:od1_dictionary"))
        elif report == 7:
            return HttpResponseRedirect(reverse("trapnet:od_spp_list"))
        elif report == 5:
            return HttpResponseRedirect(reverse("trapnet:od1_wms", kwargs={"lang": 1}))
        elif report == 6:
            return HttpResponseRedirect(reverse("trapnet:od1_wms", kwargs={"lang": 2}))
        else:
            messages.error(self.request, "Report is not available. Please select another report.")
            return HttpResponseRedirect(reverse("trapnet:report_search"))


def export_sample_data(request, year, sites):
    response = reports.generate_sample_report(year, sites)
    return response


def export_entry_data(request, year, sites):
    response = reports.generate_entry_report(year, sites)
    return response


def export_open_data_ver1(request, year, sites):
    response = reports.generate_open_data_ver_1_report(year, sites)
    return response

def export_open_data_ver1_dictionary(request):
    response = reports.generate_open_data_ver_1_data_dictionary()
    return response

def export_spp_list(request):
    response = reports.generate_spp_list()
    return response


def export_open_data_ver1_wms(request, lang):
    response = reports.generate_open_data_ver_1_wms_report(lang)
    return response

#
# def report_species_count(request, species_list):
#     reports.generate_species_count_report(species_list)
#     # find the name of the file
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     target_dir = os.path.join(base_dir, 'templates', 'camp', 'temp')
#     for root, dirs, files in os.walk(target_dir):
#         for file in files:
#             if "report_temp" in file:
#                 my_file = "trapnet/temp/{}".format(file)
#
#     return render(request, "trapnet/report_display.html", {"report_path": my_file})
#
#
# def report_species_richness(request, site=None):
#     if site:
#         reports.generate_species_richness_report(site)
#     else:
#         reports.generate_species_richness_report()
#
#     return render(request, "trapnet/report_display.html")
#
#
# class AnnualWatershedReportTemplateView(PDFTemplateView):
#     template_name = 'trapnet/report_watershed_display.html'
#
#     def get_pdf_filename(self):
#         site = models.trapnet.objects.get(pk=self.kwargs['site']).site
#         return "{} Annual Report {}.pdf".format(self.kwargs['year'], site)
#
#     def get_context_data(self, **kwargs):
#         reports.generate_annual_watershed_report(self.kwargs["site"], self.kwargs["year"])
#         site = models.trapnet.objects.get(pk=self.kwargs['site']).site
#         return super().get_context_data(
#             pagesize="A4 landscape",
#             title="Annual Report for {}_{}".format(site, self.kwargs['year']),
#             **kwargs
#         )
#
#
# def annual_watershed_spreadsheet(request, site, year):
#     my_site = models.trapnet.objects.get(pk=site)
#     file_url = reports.generate_annual_watershed_spreadsheet(my_site, year)
#
#     if os.path.exists(file_url):
#         with open(file_url, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#             response['Content-Disposition'] = 'inline; filename="CAMP Data for {}_{}.xlsx"'.format(my_site.site, year)
#             return response
#     raise Http404
#
#
# def fgp_export(request):
#     response = reports.generate_fgp_export()
#     return response
#
#
# def ais_export(request, species_list):
#     response = reports.generate_ais_spreadsheet(species_list)
#     return response


#
# # SAMPLE #
# ##########
#
# class SearchFormView(TrapNetAccessRequiredMixin, FormView):
#     template_name = 'trapnet/sample_search.html'
#
#     form_class = forms.SearchForm
#
#     # def get_initial(self):
#     #     return {'year':timezone.now().year-1}
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         station_list = []
#         for obj in models.Station.objects.all():
#             station_list.append({"site": obj.site_id, "val": obj.id, "text": obj.name})
#
#         context["station_list"] = station_list
#         return context
#
#     def form_valid(self, form):
#         year = form.cleaned_data["year"]
#         month = form.cleaned_data["month"]
#         site = nz(form.cleaned_data["site"], None)
#         station = nz(form.cleaned_data["station"], None)
#         species = nz(form.cleaned_data["species"], None)
#
#         # check to see how many results will be returned
#         qs = models.Sample.objects.all()
#         if year:
#             qs = qs.filter(year=year)
#         if month:
#             qs = qs.filter(month=month)
#         if station:
#             qs = qs.filter(station=station)
#         if site and not station:
#             qs = qs.filter(station__site=site)
#         if species:
#             qs = qs.filter(sample_spp__species=species)
#
#         if qs.count() < 1000:
#             return HttpResponseRedirect(reverse("trapnet:sample_list",
#                                                 kwargs={"year": year, "month": month, "site": site, "station": station,
#                                                         "species": species, }))
#         else:
#             messages.error(self.request, "The search requested has returned too many results. Please try again.")
#             return HttpResponseRedirect(reverse("trapnet:sample_search"))
#
#
# # class CloserTemplateView(TemplateView):
# #     template_name = 'grais/close_me.html'
#
#
# class SampleListView(TrapNetAccessRequiredMixin, ListView):
#     template_name = "trapnet/sample_list.html"
#
#
#     def get_queryset(self):
#         year = nz(self.kwargs["year"])
#         month = nz(self.kwargs["month"])
#         site = nz(self.kwargs["site"])
#         station = nz(self.kwargs["station"])
#         species = nz(self.kwargs["species"])
#
#         qs = models.Sample.objects.all()
#         try:
#             qs = qs.filter(year=year)
#         except ValueError:
#             pass
#         try:
#             qs = qs.filter(month=month)
#         except ValueError:
#             pass
#         try:
#             qs = qs.filter(station=station)
#         except ValueError:
#             pass
#         try:
#             qs = qs.filter(station__site=site)
#         except ValueError:
#             pass
#         try:
#             qs = qs.filter(sample_spp__species=species)
#         except ValueError:
#             pass
#
#         return qs
#
#
# class SampleFilterView(TrapNetAccessRequiredMixin, FilterView):
#     filterset_class = filters.SampleFilter
#     template_name = "trapnet/sample_filter.html"
#
#
#     def get_filterset_kwargs(self, filterset_class):
#         kwargs = super().get_filterset_kwargs(filterset_class)
#         if kwargs["data"] is None:
#             kwargs["data"] = {"SeasonExact": timezone.now().year - 1}
#         return kwargs
#
#
# class SampleDetailView(TrapNetAccessRequiredMixin, DetailView):
#     model = models.Sample
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['google_api_key'] = settings.GOOGLE_API_KEY
#
#         context["field_list"] = [
#             'nutrient_sample_id',
#             'station',
#             'timezone',
#             'start_date',
#             'end_date',
#             'weather_notes',
#             'rain_past_24_hours',
#             'h2o_temperature_c',
#             'salinity',
#             'dissolved_o2',
#             'water_turbidity',
#             'tide_state',
#             'tide_direction',
#             'samplers',
#             'percent_sand',
#             'percent_gravel',
#             'percent_rock',
#             'percent_mud',
#             'visual_sediment_obs',
#             'sav_survey_conducted',
#             'excessive_green_algae_water',
#             'excessive_green_algae_shore',
#             'unsampled_vegetation_inside',
#             'unsampled_vegetation_outside',
#             "notes",
#         ]
#         context["non_sav_count"] = models.SpeciesObservation.objects.filter(sample=self.object).filter(
#             species__sav=False).count
#         context["sav_count"] = models.SpeciesObservation.objects.filter(sample=self.object).filter(
#             species__sav=True).count
#         return context
#
#
# class SampleUpdateView(TrapNetAdminRequiredMixin, UpdateView):
#     model = models.Sample
#     form_class = forms.SampleForm
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         # get a list of Stations
#         station_list = []
#         for s in models.Station.objects.all():
#             html_insert = '<a href="#" class="station_insert" code={id}>{station}</a>'.format(id=s.id, station=s)
#             station_list.append(html_insert)
#         context['station_list'] = station_list
#         return context
#
#
# class SampleCreateView(TrapNetAdminRequiredMixin, CreateView):
#     model = models.Sample
#     form_class = forms.SampleCreateForm
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         # get a list of Stations
#         station_list = []
#         for s in models.Station.objects.all():
#             html_insert = '<a href="#" class="station_insert" code={id}>{station}</a>'.format(id=s.id, station=s)
#             station_list.append(html_insert)
#         context['station_list'] = station_list
#         return context
#
#     # def form_valid(self, form):
#     #     do_another = form.cleaned_data['do_another']
#     #     if do_another:
#     #         return HttpResponseRedirect(reverse_lazy(""))
#
#
# class SampleDeleteView(TrapNetAdminRequiredMixin, DeleteView):
#     model = models.Sample
#     success_url = reverse_lazy('trapnet:sample_filter')
#     success_message = 'The sample was successfully deleted!'
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
#
#
#
#
#
# # SPECIES OBSERVATIONS #
# ########################
#
# class SpeciesObservationInsertView(TrapNetAdminRequiredMixin, TemplateView):
#     template_name = "trapnet/species_obs_insert.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         sample = models.Sample.objects.get(pk=self.kwargs['sample'])
#         context['sample'] = sample
#         sample_spp = models.Sample.objects.get(pk=sample.id).sample_spp.all()
#         context['sample_spp'] = sample_spp
#
#         queryset = models.Species.objects.annotate(
#             search_term=Concat('common_name_eng', 'common_name_fre', 'scientific_name', 'code',
#                                output_field=TextField()))
#
#         # get a list of species
#         species_list = []
#         for obj in queryset:
#             # html_insert = '<a href="#" class="district_insert" code={p}{d}>{p}{d}</a> - {l}, {prov}'.format(
#             #         p=d.province_id, d=d.district_id, l=l.replace("'", ""), prov=d.get_province_id_display().upper())
#             html_insert = '<a class="add-btn btn btn-outline-dark" href="#" target-url="{}"> <img src="{}" alt=""></a><span style="margin-left: 10px;">{} / {} / <em>{}</em> / {}</span>'.format(
#                 reverse("trapnet:species_obs_new", kwargs={"sample": sample.id, "species": obj.id}),
#                 static("admin/img/icon-addlink.svg"),
#                 obj.common_name_eng,
#                 obj.common_name_fre,
#                 obj.scientific_name,
#                 obj.code
#             )
#             species_list.append(html_insert)
#         context['species_list'] = species_list
#         context["non_sav_count"] = models.SpeciesObservation.objects.filter(sample=sample).filter(
#             species__sav=False).count
#         context["sav_count"] = models.SpeciesObservation.objects.filter(sample=sample).filter(
#             species__sav=True).count
#
#         return context
#
#
# class SpeciesObservationCreateView(TrapNetAdminRequiredMixin, CreateView):
#     model = models.SpeciesObservation
#     template_name = 'trapnet/species_obs_form_popout.html'
#
#
#     def get_form_class(self):
#         species = models.Species.objects.get(pk=self.kwargs['species'])
#         if species.sav:
#             return forms.SAVObservationForm
#         else:
#             return forms.NonSAVObservationForm
#
#     def get_initial(self):
#         sample = models.Sample.objects.get(pk=self.kwargs['sample'])
#         species = models.Species.objects.get(pk=self.kwargs['species'])
#         return {
#             'sample': sample,
#             'species': species,
#         }
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         species = models.Species.objects.get(id=self.kwargs['species'])
#         sample = models.Sample.objects.get(id=self.kwargs['sample'])
#         context['species'] = species
#         context['sample'] = sample
#         return context
#
#     def form_valid(self, form):
#         self.object = form.save()
#         return HttpResponseRedirect(reverse('shared_models:close_me'))
#
#
# class SpeciesObservationUpdateView(TrapNetAccessRequiredMixin, UpdateView):
#     model = models.SpeciesObservation
#     template_name = 'trapnet/species_obs_form_popout.html'
#
#     def get_form_class(self):
#         species = self.object.species
#         if species.sav:
#             return forms.SAVObservationForm
#         else:
#             return forms.NonSAVObservationForm
#
#     def form_valid(self, form):
#         self.object = form.save()
#         return HttpResponseRedirect(reverse('shared_models:close_me'))
#
#
# def species_observation_delete(request, pk, backto):
#     object = models.SpeciesObservation.objects.get(pk=pk)
#     object.delete()
#     messages.success(request, "The species has been successfully deleted from {}.".format(object.sample))
#
#     if backto == "detail":
#         return HttpResponseRedirect(reverse_lazy("trapnet:sample_detail", kwargs={"pk": object.sample.id}))
#     else:
#         return HttpResponseRedirect(reverse_lazy("trapnet:species_obs_search", kwargs={"sample": object.sample.id}))
#
#
