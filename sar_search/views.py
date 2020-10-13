import requests
import unicodecsv as csv
from django.utils.translation import gettext as _
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import TextField
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView, TemplateView, FormView
from django_filters.views import FilterView
from shapely.geometry import box

from . import models
from . import forms
from . import filters


# open basic access up to anybody who is logged in
def in_sar_search_group(user):
    if user.id:
        # return user.groups.filter(name='sar_search_access').count() != 0
        return True


class SARSearchAccessRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return in_sar_search_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


def in_sar_search_admin_group(user):
    if user:
        return user.groups.filter(name='sar_search_admin').count() != 0


class SARSearchAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):


    def test_func(self):
        return in_sar_search_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class IndexTemplateView(SARSearchAccessRequiredMixin, TemplateView):
    template_name = 'sar_search/index.html'


class SARMapTemplateView(SARSearchAccessRequiredMixin, FormView):
    template_name = 'sar_search/sar_map.html'
    form_class = forms.MapForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['records'] = models.Record.objects.all()
        context['google_api_key'] = settings.GOOGLE_API_KEY

        # start by determining with spp do not have spatial data
        non_spatial_species_list = []
        for sp in models.Species.objects.all():
            spatial = False
            for record in sp.records.all():
                #  if has been labeled as spatial, exit the loop
                if spatial:
                    break
                # if there are coords associated with the record, it is spatial
                if record.coords():
                    spatial = True
                    break
                # check the regions...
                for region in record.regions.all():
                    if spatial:
                        break
                    for region_polygon in region.polygons.all():
                        if region_polygon.coords():
                            # then we have spatial data.
                            spatial = True
                            break
            # if checked through all records and nothing found, add to non-spatial list
            if not spatial:
                non_spatial_species_list.append(sp)

        context['non_spatial_species_list'] = non_spatial_species_list

        # if there are bounding coords, we look in the box
        region_list = []

        if self.kwargs.get("n"):

            bbox = box(
                float(self.kwargs.get("n")),
                float(self.kwargs.get("e")),
                float(self.kwargs.get("s")),
                float(self.kwargs.get("w")),
            )

            # determine which regions intersect with bbox
            for region_polygon in models.RegionPolygon.objects.all():
                # if the region has not already been added...
                if region_polygon.region not in region_list:
                    if region_polygon.get_polygon():
                        if region_polygon.get_polygon().intersects(bbox):
                            region_list.append(region_polygon.region)

            # for polygon_point in models.RegionPolygonPoint.objects.all():
            #     # if the region has not already been added...
            #     if polygon_point.region_polygon.region not in region_list:
            #         if bbox.contains(polygon_point.point):
            #             region_list.append(polygon_point.region_polygon.region)

            captured_species_list = []
            for sp in models.Species.objects.all():
                if sp not in non_spatial_species_list:
                    captured = False
                    for record in sp.records.all():
                        #  if has been labeled as spatial, exit the loop
                        if captured:
                            break
                        # check to see if the bbox overlaps with any record points
                        for obj in record.points.all():
                            if bbox.contains(obj.point):
                                captured = True
                                break
                        # it is possible that there is no point associated with a record..
                        # maybe there is a region associated with it that is in the region list
                        for region in record.regions.all():
                            if region in region_list:
                                captured = True
                                break
                    # if checked through all records and nothing found, add to non-spatial list
                    if captured:
                        captured_species_list.append(sp)
        else:
            captured_species_list = [sp for sp in models.Species.objects.all() if sp not in non_spatial_species_list]

        context['region_list'] = region_list
        context["captured_species_list"] = captured_species_list
        return context

    def get_initial(self, *args, **kwargs):
        return {
            "north": self.kwargs.get("n"),
            "south": self.kwargs.get("s"),
            "east": self.kwargs.get("e"),
            "west": self.kwargs.get("w"),
        }

    def form_valid(self, form):
        print(form.cleaned_data)
        return HttpResponseRedirect(reverse("sar_search:map", kwargs={
            "n": form.cleaned_data.get("north"),
            "s": form.cleaned_data.get("south"),
            "e": form.cleaned_data.get("east"),
            "w": form.cleaned_data.get("west"),
        }))


# REGION POLYGON #
##################

class RegionPolygonUpdateView(SARSearchAdminRequiredMixin, UpdateView):
    model = models.RegionPolygon
    form_class = forms.RegionPolygonForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}

    def form_valid(self, form):
        my_object = form.save()
        return HttpResponseRedirect(reverse_lazy("sar_search:region_detail", kwargs={"pk": my_object.id}))


class RegionPolygonCreateView(SARSearchAdminRequiredMixin, CreateView):
    model = models.RegionPolygon

    form_class = forms.RegionPolygonForm

    def get_initial(self):
        return {'species': self.kwargs.get("species")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get("species"):
            species = models.Species.objects.get(pk=self.kwargs["species"])
            context['species'] = species
        return context

    def form_valid(self, form):
        my_object = form.save()
        return HttpResponseRedirect(reverse_lazy("sar_search:region_detail", kwargs={"pk": my_object.id}))


class RegionPolygonDetailView(SARSearchAccessRequiredMixin, DetailView):
    model = models.RegionPolygon

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY

        field_list = [
            "id",
        ]
        context['field_list'] = field_list

        return context


class RegionPolygonDeleteView(SARSearchAdminRequiredMixin, DeleteView):
    model = models.RegionPolygon
    success_message = 'The region polygon was successfully deleted!'

    def get_success_url(self):
        return reverse_lazy("sar_search:region_detail", kwargs={"pk": self.object.region.id})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


@login_required(login_url='/accounts/login/')
@user_passes_test(in_sar_search_admin_group, login_url='/accounts/denied/')
def manage_rp_coords(request, region_polygon):
    qs = models.RegionPolygonPoint.objects.filter(region_polygon=region_polygon)
    my_region_polygon = models.RegionPolygon.objects.get(pk=region_polygon)
    if request.method == 'POST':
        formset = forms.RPCoordFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "coords have been successfully updated")
            return HttpResponseRedirect(reverse("sar_search:manage_rp_coords", kwargs={"region_polygon": region_polygon}))
    else:
        formset = forms.RPCoordFormSet(
            queryset=qs,
            initial=[{"region_polygon": region_polygon}],
        )
    context = {}
    context['title'] = "Manage Region Polygon Coordinates"
    context['formset'] = formset
    context["region_polygon"] = my_region_polygon
    context["my_object"] = models.RegionPolygonPoint.objects.first()
    context["field_list"] = [
        'latitude',
        'longitude',
        'order',
    ]
    return render(request, 'sar_search/manage_settings_small.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(in_sar_search_admin_group, login_url='/accounts/denied/')
def delete_rp_coord(request, pk):
    my_obj = models.RegionPolygonPoint.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("sar_search:manage_rp_coords", kwargs={"region_polygon": my_obj.region_polygon.id}))


class RegionPolygonImportFileView(SARSearchAdminRequiredMixin, UpdateView):
    model = models.Region
    fields = ["temp_file", ]
    template_name = 'sar_search/rp_points_file_import_form.html'

    def form_valid(self, form):
        my_object = form.save()
        # now we need to do some magic with the file...

        # load the file
        url = self.request.META.get("HTTP_ORIGIN") + my_object.temp_file.url
        r = requests.get(url)
        # print(r.text.splitlines())
        csv_reader = csv.DictReader(r.iter_lines())

        # make a new polygon
        my_region_polygon = models.RegionPolygon.objects.create(region=my_object)
        for row in csv_reader:
            if row["lat"] and row["long"]:
                if row.get("order"):
                    my_new_point = models.RegionPolygonPoint.objects.create(
                        region_polygon=my_region_polygon,
                        latitude=float(row["lat"]),
                        longitude=float(row["long"]),
                        order=int(row["order"]),
                    )
                else:
                    my_new_point = models.RegionPolygonPoint.objects.create(
                        region_polygon=my_region_polygon,
                        latitude=float(row["lat"]),
                        longitude=float(row["long"]),
                    )

        # clear the file in my object
        my_object.temp_file = None
        my_object.save()
        return HttpResponseRedirect(reverse_lazy('shared_models:close_me'))


# SPECIES #
###########

class SpeciesListView(SARSearchAccessRequiredMixin, FilterView):
    template_name = "sar_search/species_list.html"
    filterset_class = filters.SpeciesFilter

    def get_queryset(self):
        return models.Species.objects.annotate(
            search_term=Concat('common_name_eng', 'common_name_fre', 'scientific_name', output_field=TextField())).order_by(
            _("common_name_eng"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_object'] = models.Species.objects.first()
        context["field_list"] = [
            'full_name|Common name (population)',
            'scientific_name|Species',
            'taxon',
            'sara_status',
            'cosewic_status',
            'nb_status',
            'ns_status',
            'iucn_red_list_status',
            'sara_schedule',
            # 'tsn',
        ]
        return context


class SpeciesDetailView(SARSearchAccessRequiredMixin, DetailView):
    model = models.Species

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY
        context["field_list"] = [
            'tname|{}'.format(_("Common name")),
            'scientific_name',
            'tpopulation|{}'.format(_("Population")),
            'tsn',
            'taxon',
            'sara_status',
            'nb_status',
            'ns_status',
            'iucn_red_list_status',
            'cosewic_status',
            'sara_schedule',
            'cites_appendix',
            'province_range',
            'responsible_authority',
            'tnotes|{}'.format(_("Notes")),
        ]

        context["record_field_list"] = [
            'name',
            'regions',
            'record_type',
            'year|Sighting Date',
            'source',
        ]

        return context


class SpeciesUpdateView(SARSearchAdminRequiredMixin, UpdateView):
    model = models.Species

    form_class = forms.SpeciesForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class SpeciesCreateView(SARSearchAdminRequiredMixin, CreateView):
    model = models.Species

    form_class = forms.SpeciesForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class SpeciesDeleteView(SARSearchAdminRequiredMixin, DeleteView):
    model = models.Species
    permission_required = "__all__"
    success_url = reverse_lazy('sar_search:species_list')
    success_message = 'The species was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# RECORD #
#########

class RecordUpdateView(SARSearchAdminRequiredMixin, UpdateView):
    model = models.Record
    form_class = forms.RecordForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}

    def form_valid(self, form):
        my_object = form.save()
        return HttpResponseRedirect(reverse_lazy("sar_search:record_detail", kwargs={"pk": my_object.id}))


class RecordCreateView(SARSearchAdminRequiredMixin, CreateView):
    model = models.Record

    form_class = forms.RecordForm

    def get_initial(self):
        return {'species': self.kwargs.get("species")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get("species"):
            species = models.Species.objects.get(pk=self.kwargs["species"])
            context['species'] = species
        return context

    def form_valid(self, form):
        my_object = form.save()
        return HttpResponseRedirect(reverse_lazy("sar_search:record_detail", kwargs={"pk": my_object.id}))


class RecordDetailView(SARSearchAccessRequiredMixin, DetailView):
    model = models.Record

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY

        field_list = [
            'name',
            'regions',
            'record_type',
            'source',
            'year',
            'notes',
            'last_modified_by',
            'date_last_modified',
        ]
        context['field_list'] = field_list

        return context


class RecordDeleteView(SARSearchAdminRequiredMixin, DeleteView):
    model = models.Record
    success_message = 'The record was successfully deleted!'

    def get_success_url(self):
        return reverse_lazy("sar_search:species_detail", kwargs={"pk": self.object.species.id})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


@login_required(login_url='/accounts/login/')
@user_passes_test(in_sar_search_admin_group, login_url='/accounts/denied/')
def manage_coords(request, record):
    qs = models.RecordPoints.objects.filter(record=record)
    my_record = models.Record.objects.get(pk=record)
    if request.method == 'POST':
        formset = forms.CoordFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "coords have been successfully updated")
            return HttpResponseRedirect(reverse("sar_search:manage_coords", kwargs={"record": record}))
    else:
        print(my_record.record_type)
        if my_record.record_type == 1 and my_record.points.count() >= 1:
            formset = forms.CoordFormSet(
                queryset=qs,
                initial=[{"record": record}],
            )
        else:
            formset = forms.CoordFormSet(
                queryset=qs,
                initial=[{"record": record}],
            )
    context = {}
    context['title'] = "Manage Record Coordinates"
    context['formset'] = formset
    context["record"] = my_record
    context["my_object"] = models.RecordPoints.objects.first()
    context["field_list"] = [
        'name',
        'latitude_n',
        'longitude_w',
    ]
    return render(request, 'sar_search/manage_settings_small.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(in_sar_search_admin_group, login_url='/accounts/denied/')
def delete_coord(request, pk):
    my_obj = models.RecordPoints.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("sar_search:manage_coords", kwargs={"record": my_obj.record.id}))


class RecordImportFileView(SARSearchAdminRequiredMixin, UpdateView):
    model = models.Species
    fields = ["temp_file", ]
    template_name = 'sar_search/points_file_import_form.html'

    def form_valid(self, form):
        my_object = form.save()
        # now we need to do some magic with the file...

        # load the file
        url = self.request.META.get("HTTP_ORIGIN") + my_object.temp_file.url
        r = requests.get(url)
        # print(r.text.splitlines())
        csv_reader = csv.DictReader(r.iter_lines())

        for row in csv_reader:
            # OrderedDict([('record_name', 'St. John River'), ('site_name', '1'), ('site_lat', '46.302'), ('site_long', '-67.5327'), ('source', 'Environment Canada. 2013. Recovery Strategy for the Cobblestone Tiger Beetle (Cicindela marginipennis) in Canada. Species at Risk Act Recovery Strategy Series. Environment Canada, Ottawa. v + 18 pp.')])
            if row["type"] == "polygon":
                my_type = 3
            elif row["type"] == "line" or row["type"] == "polyline":
                my_type = 2
            else:
                my_type = 1

            my_record, created = models.Record.objects.get_or_create(
                species=my_object,
                name=row["record_name"],
                record_type=my_type,
                source=row["record_source"],
            )

            if row["site_lat"] and row["site_long"]:
                my_new_point = models.RecordPoints.objects.create(
                    record=my_record,
                    name=row["site_name"],
                    latitude_n=float(row["site_lat"]),
                    longitude_w=float(row["site_long"]),
                )

        # clear the file in my object
        my_object.temp_file = None
        my_object.save()
        return HttpResponseRedirect(reverse_lazy('shared_models:close_me'))


# SETTINGS #
############
@login_required(login_url='/accounts/login/')
@user_passes_test(in_sar_search_admin_group, login_url='/accounts/denied/')
def manage_taxa(request):
    qs = models.Taxon.objects.all()
    if request.method == 'POST':
        formset = forms.TaxonFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "Taxa have been successfully updated")
            return HttpResponseRedirect(reverse("sar_search:manage_taxa"))
    else:
        formset = forms.TaxonFormSet(queryset=qs)
    context = dict()
    context['title'] = "Manage Taxa"
    context['formset'] = formset
    context["my_object"] = qs.first()
    context["field_list"] = [
        'code',
        'name',
        'nom',
    ]
    return render(request, 'sar_search/manage_settings_small.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(in_sar_search_admin_group, login_url='/accounts/denied/')
def delete_taxon(request, pk):
    my_obj = models.Taxon.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("sar_search:manage_taxa"))


@login_required(login_url='/accounts/login/')
@user_passes_test(in_sar_search_admin_group, login_url='/accounts/denied/')
def manage_statuses(request):
    qs = models.SpeciesStatus.objects.all()
    if request.method == 'POST':
        formset = forms.SpeciesStatusFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "Species status has been successfully updated")
            return HttpResponseRedirect(reverse("sar_search:manage_statuses"))
    else:
        formset = forms.SpeciesStatusFormSet(queryset=qs)
    context = {}
    context['title'] = "Manage Species Statuses"
    context['formset'] = formset
    context["my_object"] = qs.first()
    context["field_list"] = [
        'used_for',
        'code',
        'name',
        'nom',
        'description_eng',
        'description_fre',
    ]
    return render(request, 'sar_search/manage_settings_small.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(in_sar_search_admin_group, login_url='/accounts/denied/')
def delete_status(request, pk):
    my_obj = models.SpeciesStatus.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("sar_search:manage_statuses"))


@login_required(login_url='/accounts/login/')
@user_passes_test(in_sar_search_admin_group, login_url='/accounts/denied/')
def manage_schedules(request):
    qs = models.SARASchedule.objects.all()
    if request.method == 'POST':
        formset = forms.SARAScheduleFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "schedules have been successfully updated")
            return HttpResponseRedirect(reverse("sar_search:manage_schedules"))
    else:
        formset = forms.SARAScheduleFormSet(queryset=qs)
    context = {}
    context['title'] = "Manage SARA Schedules"
    context['formset'] = formset
    context["my_object"] = qs.first()
    context["field_list"] = [
        'name',
        'nom',
        'description_eng',
        'description_fre',
    ]
    return render(request, 'sar_search/manage_settings_small.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(in_sar_search_admin_group, login_url='/accounts/denied/')
def delete_schedule(request, pk):
    my_obj = models.SARASchedule.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("sar_search:manage_schedules"))


# REGION
class RegionListView(SARSearchAccessRequiredMixin, FilterView):
    template_name = "sar_search/region_list.html"
    filterset_class = filters.RegionFilter
    queryset = models.Region.objects.annotate(
        search_term=Concat('name', 'nom', output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_object'] = models.Region.objects.first()
        context["field_list"] = [
            'name',
            'nom',
            'province',
        ]
        return context


class RegionDetailView(SARSearchAccessRequiredMixin, DetailView):
    model = models.Region

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY
        context["field_list"] = [
            'name',
            'nom',
            'province',
        ]
        my_object = context["object"]
        species_list = list(set([record.species for record in my_object.records.all()]))
        context["species_list"] = species_list
        return context


class RegionUpdateView(SARSearchAdminRequiredMixin, UpdateView):
    model = models.Region

    form_class = forms.RegionForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class RegionCreateView(SARSearchAdminRequiredMixin, CreateView):
    model = models.Region

    form_class = forms.RegionForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class RegionDeleteView(SARSearchAdminRequiredMixin, DeleteView):
    model = models.Region
    permission_required = "__all__"
    success_url = reverse_lazy('sar_search:region_list')
    success_message = 'The region was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


@login_required(login_url='/accounts/login/')
@user_passes_test(in_sar_search_admin_group, login_url='/accounts/denied/')
def manage_appendices(request):
    qs = models.CITESAppendix.objects.all()
    if request.method == 'POST':
        formset = forms.CITESAppendixFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "schedules have been successfully updated")
            return HttpResponseRedirect(reverse("sar_search:manage_appendices"))
    else:
        formset = forms.CITESAppendixFormSet(queryset=qs)
    context = {}
    context['title'] = "Manage CITES Appendices"
    context['formset'] = formset
    context["my_object"] = qs.first()
    context["field_list"] = [
        'name',
        'nom',
        'description_eng',
        'description_fre',
    ]
    return render(request, 'sar_search/manage_settings_small.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(in_sar_search_admin_group, login_url='/accounts/denied/')
def delete_appendix(request, pk):
    my_obj = models.CITESAppendix.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("sar_search:manage_appendices"))


@login_required(login_url='/accounts/login/')
@user_passes_test(in_sar_search_admin_group, login_url='/accounts/denied/')
def manage_authorities(request):
    qs = models.ResponsibleAuthority.objects.all()
    if request.method == 'POST':
        formset = forms.ResponsibleAuthorityFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "schedules have been successfully updated")
            return HttpResponseRedirect(reverse("sar_search:manage_authorities"))
    else:
        formset = forms.ResponsibleAuthorityFormSet(queryset=qs)
    context = {}
    context['title'] = "Manage Responsible Authorities"
    context['formset'] = formset
    context["my_object"] = qs.first()
    context["field_list"] = [
        'name',
        'nom',
    ]
    return render(request, 'sar_search/manage_settings_small.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(in_sar_search_admin_group, login_url='/accounts/denied/')
def delete_authority(request, pk):
    my_obj = models.ResponsibleAuthority.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("sar_search:manage_authorities"))
