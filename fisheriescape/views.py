from copy import deepcopy

from django.conf import settings
from django.utils.translation import gettext as _, gettext_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import TextField, Value
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView, TemplateView, FormView
from django_filters.views import FilterView
from django.contrib.auth.models import User, Group

from shared_models.views import CommonFilterView, CommonCreateView, CommonDetailView, CommonUpdateView, \
    CommonDeleteView, CommonHardDeleteView, CommonFormsetView, CommonTemplateView
from . import models
from . import forms
from . import filters

import json
from django.core.serializers import serialize


class CloserTemplateView(TemplateView):
    template_name = 'fisheriescape/close_me.html'


### Permissions ###


class FisheriescapeAccessRequired(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return True

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


def in_fisheriescape_admin_group(user):
    if "fisheriescape_admin" in [g.name for g in user.groups.all()]:
        return True


class FisheriescapeAdminAccessRequired(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return in_fisheriescape_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


def in_fisheriescape_edit_group(user):
    """this group includes the admin group so there is no need to add an admin to this group"""
    if user:
        if in_fisheriescape_admin_group(user) or user.groups.filter(name='fisheriescape_edit').count() != 0:
            return True


class FisheriescapeEditRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return in_fisheriescape_edit_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'fisheriescape/index.html')


# #
# # # MAP #
# # ###########
# #
#

class MapView(FisheriescapeAccessRequired, TemplateView):
    template_name = "fisheriescape/map.html"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["lobster_areas"] = serialize("geojson", models.FisheryArea.objects.filter(layer_id="Lobster"))
        context["snow_crab_areas"] = serialize("geojson", models.FisheryArea.objects.filter(layer_id="Crab"))
        context["nafo_areas"] = serialize("geojson", models.FisheryArea.objects.filter(layer_id="NAFO"))
        context["mapbox_api_key"] = settings.MAPBOX_API_KEY
        return context


# #
# # # SPECIES #
# # ###########
# #
#


class SpeciesListView(FisheriescapeAccessRequired, CommonFilterView):
    template_name = "fisheriescape/list.html"
    filterset_class = filters.SpeciesFilter
    h1 = "Species List"
    home_url_name = "fisheriescape:index"
    row_object_url_name = "fisheriescape:species_detail"
    new_btn_text = "New Species"

    queryset = models.Species.objects.annotate(
        search_term=Concat('english_name', 'french_name', 'latin_name', 'id', output_field=TextField()))

    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'english_name', "class": "", "width": ""},
        {"name": 'french_name', "class": "", "width": ""},
        {"name": 'latin_name', "class": "", "width": ""},

    ]

    def get_new_object_url(self):
        return reverse("fisheriescape:species_new", kwargs=self.kwargs)


class SpeciesDetailView(FisheriescapeAdminAccessRequired, CommonDetailView):
    model = models.Species
    field_list = [
        'id',
        'english_name',
        'french_name',
        'latin_name',
        'website',

    ]
    home_url_name = "fisheriescape:index"
    parent_crumb = {"title": gettext_lazy("Species List"), "url": reverse_lazy("fisheriescape:species_list")}


class SpeciesUpdateView(FisheriescapeAdminAccessRequired, CommonUpdateView):
    model = models.Species
    form_class = forms.SpeciesForm
    template_name = 'fisheriescape/form.html'
    cancel_text = _("Cancel")
    home_url_name = "fisheriescape:index"

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Species record successfully updated for : {my_object}"))
        return HttpResponseRedirect(reverse("fisheriescape:species_detail", kwargs=self.kwargs))

    def get_active_page_name_crumb(self):
        my_object = self.get_object()
        return my_object

    def get_h1(self):
        my_object = self.get_object()
        return my_object

    def get_parent_crumb(self):
        return {"title": str(self.get_object()),
                "url": reverse_lazy("fisheriescape:species_detail", kwargs=self.kwargs)}

    def get_grandparent_crumb(self):
        kwargs = deepcopy(self.kwargs)
        del kwargs["pk"]
        return {"title": _("Species List"), "url": reverse("fisheriescape:species_list", kwargs=kwargs)}


class SpeciesCreateView(FisheriescapeAdminAccessRequired, CommonCreateView):
    model = models.Species
    form_class = forms.SpeciesForm
    template_name = 'fisheriescape/form.html'
    home_url_name = "fisheriescape:index"
    h1 = gettext_lazy("Add New Species")
    parent_crumb = {"title": gettext_lazy("Species List"), "url": reverse_lazy("fisheriescape:species_list")}

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Species record successfully created for : {my_object}"))
        return super().form_valid(form)


class SpeciesDeleteView(FisheriescapeAdminAccessRequired, CommonDeleteView):
    model = models.Species
    permission_required = "__all__"
    success_url = reverse_lazy('fisheriescape:species_list')
    template_name = 'fisheriescape/confirm_delete.html'
    home_url_name = "fisheriescape:index"
    grandparent_crumb = {"title": gettext_lazy("Species List"), "url": reverse_lazy("fisheriescape:species_list")}

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse_lazy("fisheriescape:species_detail", kwargs=self.kwargs)}


# #
# # # FISHERY AREA #
# # ###########
# #
#


class FisheryAreaListView(FisheriescapeAccessRequired, CommonFilterView):
    template_name = "fisheriescape/list.html"
    filterset_class = filters.FisheryAreaFilter
    h1 = "Fishery Area List"
    home_url_name = "fisheriescape:index"
    row_object_url_name = "fisheriescape:fishery_area_detail"
    # new_btn_text = "New Fishery Area"

    queryset = models.FisheryArea.objects.annotate(
        search_term=Concat('name', 'id', output_field=TextField()))

    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'layer_id', "class": "", "width": ""},
        {"name": 'name', "class": "", "width": ""},
        {"name": 'region', "class": "", "width": ""},
    ]

    # def get_new_object_url(self):
    #     return reverse("fisheriescape:fishery_area_new", kwargs=self.kwargs)


class FisheryAreaDetailView(FisheriescapeAdminAccessRequired, CommonDetailView):
    model = models.FisheryArea
    field_list = [
        'id',
        'layer_id',
        'name',
        'region',

    ]
    home_url_name = "fisheriescape:index"
    parent_crumb = {"title": gettext_lazy("Fishery Area List"), "url": reverse_lazy("fisheriescape:fishery_area_list")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # contexts for _fishery.html file
        context["random_fishery"] = models.Fishery.objects.first()
        context["fishery_field_list"] = [
            'species',
            'start_date',
            'end_date',
            'fishery_status',
            'gear_type',
        ]

        return context


# class FisheryAreaUpdateView(FisheriescapeAdminAccessRequired, CommonUpdateView):
#     model = models.FisheryArea
#     form_class = forms.FisheryAreaForm
#     template_name = 'fisheriescape/geo_form.html'
#     cancel_text = _("Cancel")
#     home_url_name = "fisheriescape:index"
#
#     def form_valid(self, form):
#         my_object = form.save()
#         messages.success(self.request, _(f"Fishery Area record successfully updated for : {my_object}"))
#         return HttpResponseRedirect(reverse("fisheriescape:fishery_area_detail", kwargs=self.kwargs))
#
#     def get_active_page_name_crumb(self):
#         my_object = self.get_object()
#         return my_object
#
#     def get_h1(self):
#         my_object = self.get_object()
#         return my_object
#
#     def get_parent_crumb(self):
#         return {"title": str(self.get_object()),
#                 "url": reverse_lazy("fisheriescape:fishery_area_detail", kwargs=self.kwargs)}
#
#     def get_grandparent_crumb(self):
#         kwargs = deepcopy(self.kwargs)
#         del kwargs["pk"]
#         return {"title": _("Fishery Area List"), "url": reverse("fisheriescape:fishery_area_list", kwargs=kwargs)}
#
#
# class FisheryAreaCreateView(FisheriescapeAdminAccessRequired, CommonCreateView):
#     model = models.FisheryArea
#     form_class = forms.FisheryAreaForm2
#     template_name = 'fisheriescape/form.html'
#     home_url_name = "fisheriescape:index"
#     h1 = gettext_lazy("Add New Fishery Area")
#     parent_crumb = {"title": gettext_lazy("Fishery Area List"), "url": reverse_lazy("fisheriescape:fishery_area_list")}
#
#     def form_valid(self, form):
#         my_object = form.save()
#         messages.success(self.request, _(f"Fishery Area record successfully created for : {my_object}"))
#         return super().form_valid(form)
#
#
# class FisheryAreaDeleteView(FisheriescapeAdminAccessRequired, CommonDeleteView):
#     model = models.FisheryArea
#     permission_required = "__all__"
#     success_url = reverse_lazy('fisheriescape:fishery_area_list')
#     template_name = 'fisheriescape/confirm_delete.html'
#     home_url_name = "fisheriescape:index"
#     grandparent_crumb = {"title": gettext_lazy("Fishery Area List"),
#                          "url": reverse_lazy("fisheriescape:fishery_area_list")}
#
#     def get_parent_crumb(self):
#         return {"title": self.get_object(), "url": reverse_lazy("fisheriescape:fishery_area_detail", kwargs=self.kwargs)}


# #
# # # FISHERY #
# # ###########
# #
#


class FisheryListView(FisheriescapeAccessRequired, CommonFilterView):
    template_name = "fisheriescape/list.html"
    filterset_class = filters.FisheryFilter
    h1 = "Fishery List"
    home_url_name = "fisheriescape:index"
    row_object_url_name = "fisheriescape:fishery_detail"
    new_btn_text = "New Fishery"

    queryset = models.Fishery.objects.annotate(
        search_term=Concat('species', 'id', output_field=TextField()))

    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'start_date', "class": "", "width": ""},
        {"name": 'end_date', "class": "", "width": ""},
        {"name": 'fishery_status', "class": "", "width": ""},
        {"name": 'species', "class": "", "width": ""},
        {"name": 'fishery_areas', "class": "", "width": ""},
        {"name": 'gear_type', "class": "", "width": ""},
        {"name": 'marine_mammals', "class": "", "width": ""},
    ]

    def get_new_object_url(self):
        return reverse("fisheriescape:fishery_new", kwargs=self.kwargs)


class FisheryDetailView(FisheriescapeAdminAccessRequired, CommonDetailView):
    model = models.Fishery
    field_list = [
        'id',
        'species',
        'fishery_areas',
        'start_date',
        'end_date',
        'fishery_status',
        'gear_type',
        'marine_mammals',
    ]
    home_url_name = "fisheriescape:index"
    parent_crumb = {"title": gettext_lazy("Fishery List"), "url": reverse_lazy("fisheriescape:fishery_list")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # contexts for _mammals.html file
        context["random_mammals"] = models.MarineMammal.objects.first()
        context["mammals_field_list"] = [
            'english_name',
            'french_name',
            'latin_name',
            'sara_status',
            'cosewic_status',
            'website',
        ]

        # contexts for fishery_detail maps
        polygon_subset = models.FisheryArea.objects.filter(species=self.object)

        context["fishery_polygons"] = serialize("geojson", polygon_subset)
        context["mapbox_api_key"] = settings.MAPBOX_API_KEY

        return context


class FisheryUpdateView(FisheriescapeAdminAccessRequired, CommonUpdateView):
    model = models.Fishery
    form_class = forms.FisheryForm
    template_name = 'fisheriescape/form.html'
    cancel_text = _("Cancel")
    home_url_name = "fisheriescape:index"

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Fishery record successfully updated for : {my_object}"))
        return HttpResponseRedirect(reverse("fisheriescape:fishery_detail", kwargs=self.kwargs))

    def get_active_page_name_crumb(self):
        my_object = self.get_object()
        return my_object

    def get_h1(self):
        my_object = self.get_object()
        return my_object

    def get_parent_crumb(self):
        return {"title": str(self.get_object()),
                "url": reverse_lazy("fisheriescape:fishery_detail", kwargs=self.kwargs)}

    def get_grandparent_crumb(self):
        kwargs = deepcopy(self.kwargs)
        del kwargs["pk"]
        return {"title": _("Fishery List"), "url": reverse("fisheriescape:fishery_list", kwargs=kwargs)}


class FisheryCreateView(FisheriescapeAdminAccessRequired, CommonCreateView):
    model = models.Fishery
    form_class = forms.FisheryForm
    template_name = 'fisheriescape/form.html'
    home_url_name = "fisheriescape:index"
    h1 = gettext_lazy("Add New Fishery")
    parent_crumb = {"title": gettext_lazy("Fishery List"), "url": reverse_lazy("fisheriescape:fishery_list")}

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Fishery record successfully created for : {my_object}"))
        return super().form_valid(form)


class FisheryDeleteView(FisheriescapeAdminAccessRequired, CommonDeleteView):
    model = models.Fishery
    permission_required = "__all__"
    success_url = reverse_lazy('fisheriescape:fishery_list')
    template_name = 'fisheriescape/confirm_delete.html'
    home_url_name = "fisheriescape:index"
    grandparent_crumb = {"title": gettext_lazy("Fishery List"), "url": reverse_lazy("fisheriescape:fishery_list")}

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse_lazy("fisheriescape:fishery_detail", kwargs=self.kwargs)}

