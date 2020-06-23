import unicodecsv as csv
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db.models import Count, TextField
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView, TemplateView, FormView
from easy_pdf.views import PDFTemplateView
from django_filters.views import FilterView
from . import models
from . import forms
from . import filters
from . import reports
from lib.functions.custom_functions import nz
from django.utils.encoding import smart_str


class CloserTemplateView(TemplateView):
    template_name = 'camp/close_me.html'


# open basic access up to anybody who is logged in
def in_camp_group(user):
    if user:
        # return user.groups.filter(name='camp_access').count() != 0
        return True


class CampAccessRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):


    def test_func(self):
        return in_camp_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)



def in_camp_admin_group(user):
    if user:
        return user.groups.filter(name='camp_admin').count() != 0


class CampAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):


    def test_func(self):
        return in_camp_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class IndexTemplateView(CampAccessRequiredMixin, TemplateView):
    template_name = 'camp/index.html'


# SAMPLE #
##########
#
# class SearchFormView(CampAccessRequiredMixin, FormView):
#     template_name = 'camp/sample_search.html'
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
#         sample_id = form.cleaned_data["sample_id"]
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
#         if sample_id:
#             qs = qs.filter(id__icontains=sample_id)
#         if station:
#             qs = qs.filter(station=station)
#         if site and not station:
#             qs = qs.filter(station__site=site)
#         if species:
#             qs = qs.filter(sample_spp__species=species)
#
#         return HttpResponseRedirect(reverse("camp:sample_list",
#                                                 kwargs={"year": year, "month": month, "site": site, "station": station,
#                                                         "species": species, }))


# class CloserTemplateView(TemplateView):
#     template_name = 'grais/close_me.html'


# class SampleListView(CampAccessRequiredMixin, FilterView):
#     template_name = "camp/sample_list.html"
#     filterset_class = filters.SampleFilter
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


class SampleFilterView(CampAccessRequiredMixin, FilterView):
    filterset_class = filters.SampleFilter
    template_name = "camp/sample_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['random_object'] = models.Sample.objects.first()
        context["field_list"] = [
            'id',
            'nutrient_sample_id',
            'station.site|Site',
            'station',
            'start_date|Start date',
            'sample_spp.count|Sample count',
        ]
        return context




class SampleDetailView(CampAccessRequiredMixin, DetailView):
    model = models.Sample


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY

        context["field_list"] = [
            'nutrient_sample_id',
            'station',
            'timezone',
            'start_date',
            'end_date',
            'weather_notes',
            'rain_past_24_hours',
            'h2o_temperature_c',
            'salinity',
            'dissolved_o2',
            'water_turbidity',
            'tide_state',
            'tide_direction',
            'samplers',
            'percent_sand',
            'percent_gravel',
            'percent_rock',
            'percent_mud',
            'visual_sediment_obs',
            'sav_survey_conducted',
            'excessive_green_algae_water',
            'excessive_green_algae_shore',
            'unsampled_vegetation_inside',
            'unsampled_vegetation_outside',
            "notes",
        ]
        context["non_sav_count"] = models.SpeciesObservation.objects.filter(sample=self.object).filter(
            species__sav=False).count
        context["sav_count"] = models.SpeciesObservation.objects.filter(sample=self.object).filter(
            species__sav=True).count
        return context


class SampleUpdateView(CampAdminRequiredMixin, UpdateView):
    model = models.Sample
    form_class = forms.SampleForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get a list of Stations
        station_list = []
        for s in models.Station.objects.all():
            html_insert = '<a href="#" class="station_insert" code={id}>{station}</a>'.format(id=s.id, station=s)
            station_list.append(html_insert)
        context['station_list'] = station_list
        return context


class SampleCreateView(CampAdminRequiredMixin, CreateView):
    model = models.Sample
    form_class = forms.SampleCreateForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get a list of Stations
        station_list = []
        for s in models.Station.objects.all():
            html_insert = '<a href="#" class="station_insert" code={id}>{station}</a>'.format(id=s.id, station=s)
            station_list.append(html_insert)
        context['station_list'] = station_list
        return context

    # def form_valid(self, form):
    #     do_another = form.cleaned_data['do_another']
    #     if do_another:
    #         return HttpResponseRedirect(reverse_lazy(""))


class SampleDeleteView(CampAdminRequiredMixin, DeleteView):
    model = models.Sample
    success_url = reverse_lazy('camp:sample_list')
    success_message = 'The sample was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# SITE #
########

class SiteListView(CampAccessRequiredMixin, FilterView):
    filterset_class = filters.SiteFilter
    template_name = "camp/site_list.html"



class SiteUpdateView(CampAdminRequiredMixin, UpdateView):
    # permission_required = "__all__"
    raise_exception = True

    model = models.Site
    form_class = forms.SiteForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class SiteCreateView(CampAdminRequiredMixin, CreateView):
    model = models.Site

    form_class = forms.SiteForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class SiteDetailView(CampAccessRequiredMixin, DetailView):
    model = models.Site


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY

        field_list = [
            "site",
            "code",
            "province",
            "description",
        ]
        context['field_list'] = field_list

        station_list = []
        for obj in self.object.stations.all():
            if obj.latitude_n and obj.longitude_w:
                station_list.append(
                    [obj.name, obj.latitude_n, obj.longitude_w]
                )
        context['station_list'] = station_list

        return context


class SiteDeleteView(CampAdminRequiredMixin, DeleteView):
    model = models.Site
    success_url = reverse_lazy('camp:site_list')
    success_message = 'The site was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# STATION #
###########

class StationUpdateView(CampAdminRequiredMixin, UpdateView):
    # permission_required = "__all__"
    raise_exception = True

    model = models.Station
    form_class = forms.StationForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class StationCreateView(CampAdminRequiredMixin, CreateView):
    model = models.Station

    form_class = forms.StationForm

    def get_initial(self):
        return {'site': self.kwargs["site"]}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = models.Site.objects.get(pk=self.kwargs["site"])
        context['site'] = site
        return context


class NoSiteStationCreateView(CampAccessRequiredMixin, CreateView):
    model = models.Station

    form_class = forms.NoSiteStationForm
    success_url = reverse_lazy("camp:close_me")


class StationDetailView(CampAdminRequiredMixin, DetailView):
    model = models.Station


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY

        field_list = [
            "name",
            "site",
            "station_number",
            "latitude_n",
            "longitude_w",
            "description",
        ]
        context['field_list'] = field_list

        return context


class StationDeleteView(CampAdminRequiredMixin, DeleteView):
    model = models.Station
    success_message = 'The station was successfully deleted!'

    def get_success_url(self):
        return reverse_lazy("camp:site_detail", kwargs={"pk": self.object.site.id})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# SPECIES #
###########

class SpeciesListView(CampAccessRequiredMixin, FilterView):
    template_name = "camp/species_list.html"
    filterset_class = filters.SpeciesFilter

    queryset = models.Species.objects.annotate(
        search_term=Concat('common_name_eng', 'common_name_fre', 'scientific_name', 'code', output_field=TextField()))


class SpeciesDetailView(CampAccessRequiredMixin, DetailView):
    model = models.Species


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY
        context["field_list"] = [
            'common_name_eng',
            'common_name_fre',
            'scientific_name',
            'ais',
            'code',
            'tsn',
            'aphia_id',
            'notes',
        ]

        # get a list of x,y coords for the species
        locations = []

        # i want a queryset that has [species, station name, lat, lon, count of stn]

        qs = models.SpeciesObservation.objects.filter(species=self.object).values(
            'species_id',
            'sample__station__id',
            'sample__station__name',
            'sample__station__site__site',
            'sample__station__latitude_n',
            'sample__station__longitude_w'
        ).distinct().annotate(dcount=Count('sample__station__id'))

        for obj in qs:
            if obj["sample__station__latitude_n"] and obj["sample__station__longitude_w"]:
                year_last_seen = models.SpeciesObservation.objects.filter(species=self.object.id).filter(
                    sample__station=obj["sample__station__id"]).order_by(
                    "-sample__start_date").first().sample.start_date.year
                locations.append(
                    [
                        "{} ({})".format(obj["sample__station__name"], obj["sample__station__site__site"]),
                        obj["sample__station__latitude_n"],
                        obj["sample__station__longitude_w"],
                        obj["dcount"],
                        year_last_seen,
                    ]
                )

        context["locations"] = locations

        return context


class SpeciesUpdateView(CampAdminRequiredMixin, UpdateView):
    model = models.Species

    form_class = forms.SpeciesForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class SpeciesCreateView(CampAdminRequiredMixin, CreateView):
    model = models.Species

    form_class = forms.SpeciesForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class SpeciesDeleteView(CampAdminRequiredMixin, CampAccessRequiredMixin, DeleteView):
    model = models.Species
    permission_required = "__all__"
    success_url = reverse_lazy('camp:species_list')
    success_message = 'The species was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# SPECIES OBSERVATIONS #
########################

class SpeciesObservationInsertView(CampAdminRequiredMixin, TemplateView):
    template_name = "camp/species_obs_insert.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sample = models.Sample.objects.get(pk=self.kwargs['sample'])
        context['sample'] = sample
        sample_spp = models.Sample.objects.get(pk=sample.id).sample_spp.all()
        context['sample_spp'] = sample_spp

        queryset = models.Species.objects.annotate(
            search_term=Concat('common_name_eng', 'common_name_fre', 'scientific_name', 'code',
                               output_field=TextField()))

        # get a list of species
        species_list = []
        for obj in queryset:
            # html_insert = '<a href="#" class="district_insert" code={p}{d}>{p}{d}</a> - {l}, {prov}'.format(
            #         p=d.province_id, d=d.district_id, l=l.replace("'", ""), prov=d.get_province_id_display().upper())
            html_insert = '<a class="add-btn btn btn-outline-dark" href="#" target-url="{}"> <img src="{}" alt=""></a><span style="margin-left: 10px;">{} / {} / <em>{}</em> / {}</span>'.format(
                reverse("camp:species_obs_new", kwargs={"sample": sample.id, "species": obj.id}),
                static("admin/img/icon-addlink.svg"),
                obj.common_name_eng,
                obj.common_name_fre,
                obj.scientific_name,
                obj.code
            )
            species_list.append(html_insert)
        context['species_list'] = species_list
        context["non_sav_count"] = models.SpeciesObservation.objects.filter(sample=sample).filter(
            species__sav=False).count
        context["sav_count"] = models.SpeciesObservation.objects.filter(sample=sample).filter(
            species__sav=True).count

        return context


class SpeciesObservationCreateView(CampAdminRequiredMixin, CreateView):
    model = models.SpeciesObservation
    template_name = 'camp/species_obs_form_popout.html'


    def get_form_class(self):
        species = models.Species.objects.get(pk=self.kwargs['species'])
        if species.sav:
            return forms.SAVObservationForm
        else:
            return forms.NonSAVObservationForm

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
        return HttpResponseRedirect(reverse('camp:close_me'))


class SpeciesObservationUpdateView(CampAccessRequiredMixin, UpdateView):
    model = models.SpeciesObservation
    template_name = 'camp/species_obs_form_popout.html'

    def get_form_class(self):
        species = self.object.species
        if species.sav:
            return forms.SAVObservationForm
        else:
            return forms.NonSAVObservationForm

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('camp:close_me'))


def species_observation_delete(request, pk, backto):
    object = models.SpeciesObservation.objects.get(pk=pk)
    object.delete()
    messages.success(request, "The species has been successfully deleted from {}.".format(object.sample))

    if backto == "detail":
        return HttpResponseRedirect(reverse_lazy("camp:sample_detail", kwargs={"pk": object.sample.id}))
    else:
        return HttpResponseRedirect(reverse_lazy("camp:species_obs_search", kwargs={"sample": object.sample.id}))


# REPORTS #
###########

class ReportSearchFormView(CampAccessRequiredMixin, FormView):
    template_name = 'camp/report_search.html'
    form_class = forms.ReportSearchForm

    def get_initial(self):
        # default the year to the year of the latest samples

        # 2019/04/03 - P. Upson
        # I've added a check here to see if there's any data in the DB before retrieving the .first() cursor
        # If the DB is empty calling:
        #    models.Sample.objects.all().order_by("-start_date").first().start_date.year
        # will cause an error (essentially a null pointer exception)

        res = models.Sample.objects.all().order_by("-start_date")
        return {"year": res.first().start_date.year if res.exists() else ""}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        species_list = str(form.cleaned_data["species"]).replace("[", "").replace("]", "").replace(" ", "")
        ais_species_list = str(form.cleaned_data["ais_species"]).replace("[", "").replace("]", "").replace(" ", "").replace("'","").replace('"',"")
        report = int(form.cleaned_data["report"])

        if report == 1:
            return HttpResponseRedirect(reverse("camp:species_report", kwargs={"species_list": species_list}))
        elif report == 2:
            try:
                site = int(form.cleaned_data["site"])
            except:
                site = None
                print("no site provided")

            if site:
                return HttpResponseRedirect(reverse("camp:species_richness", kwargs={"site": site}))
            else:
                return HttpResponseRedirect(reverse("camp:species_richness"))
        elif report == 3:
            site = int(form.cleaned_data["site"])
            year = int(form.cleaned_data["year"])
            return HttpResponseRedirect(reverse("camp:watershed_report", kwargs={"site": site, "year": year}))

        elif report == 4:
            site = int(form.cleaned_data["site"])
            year = int(form.cleaned_data["year"])
            return HttpResponseRedirect(reverse("camp:watershed_xlsx", kwargs={"site": site, "year": year}))

        elif report == 5:
            return HttpResponseRedirect(reverse("camp:od1_report"))

        elif report == 7:
            return HttpResponseRedirect(reverse("camp:od_dict"))

        elif report == 8:
            return HttpResponseRedirect(reverse("camp:od_wms", kwargs={"lang":1}))

        elif report == 13:
            return HttpResponseRedirect(reverse("camp:od_wms", kwargs={"lang":2}))

        elif report == 11:
            return HttpResponseRedirect(reverse("camp:od_spp_list"))

        elif report == 6:
            return HttpResponseRedirect(reverse("camp:ais_export", kwargs={
                'species_list': ais_species_list,
            }))
        elif report == 9:
            return HttpResponseRedirect(reverse("camp:od2_report"))

        elif report == 12:
            return HttpResponseRedirect(reverse("camp:od3_report"))

        # elif report == 10:
        #     return HttpResponseRedirect(reverse("camp:od_dict"))

        else:
            messages.error(self.request, "Report is not available. Please select another report.")
            return HttpResponseRedirect(reverse("ihub:report_search"))


def report_species_count(request, species_list):
    reports.generate_species_count_report(species_list)
    # find the name of the file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(base_dir, 'templates', 'camp', 'temp')
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if "report_temp" in file:
                my_file = "camp/temp/{}".format(file)

    return render(request, "camp/report_display.html", {"report_path": my_file})


def report_species_richness(request, site=None):
    if site:
        reports.generate_species_richness_report(site)
    else:
        reports.generate_species_richness_report()

    return render(request, "camp/report_display.html")


class AnnualWatershedReportTemplateView(PDFTemplateView):
    template_name = 'camp/report_watershed_display.html'

    def get_pdf_filename(self):
        site = models.Site.objects.get(pk=self.kwargs['site']).site
        return "{} Annual Report {}.pdf".format(self.kwargs['year'], site)

    def get_context_data(self, **kwargs):
        reports.generate_annual_watershed_report(self.kwargs["site"], self.kwargs["year"])
        site = models.Site.objects.get(pk=self.kwargs['site']).site
        return super().get_context_data(
            pagesize="A4 landscape",
            title="Annual Report for {}_{}".format(site, self.kwargs['year']),
            **kwargs
        )


def annual_watershed_spreadsheet(request, site, year):
    my_site = models.Site.objects.get(pk=site)
    file_url = reports.generate_annual_watershed_spreadsheet(my_site, year)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename="CAMP Data for {}_{}.xlsx"'.format(my_site.site, year)
            return response
    raise Http404


def od1_export(request):
    response = reports.generate_od1_report()
    return response


def od_dict_export(request):
    response = reports.generate_od_dict()
    return response


def ais_export(request, species_list):
    response = reports.generate_ais_spreadsheet(species_list)
    return response


def export_open_data_wms(request, lang):
    response = reports.generate_open_data_wms_report(lang)
    return response


def export_open_data_spp_list(request):
    response = reports.generate_open_data_species_list()
    return response

def od2_export(request):
    response = reports.generate_od2_report()
    return response

def od3_export(request):
    response = reports.generate_od3_report()
    return response