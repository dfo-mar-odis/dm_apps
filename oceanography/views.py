import csv
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import TextField
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
from django.utils.text import slugify
from django.urls import reverse_lazy, reverse
from django_filters.views import FilterView

from . import models
from . import filters
from . import forms
from shared_models import models as shared_models


# open basic access up to anybody who is logged in
def in_oceanography_group(user):
    if user.id:
        # return user.groups.filter(name='sar_search_access').count() != 0
        return True


class OceanographyAccessRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return in_oceanography_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


def in_oceanography_admin_group(user):
    if user:
        return user.groups.filter(name='oceanography_admin').count() != 0


class OceanographyAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return in_oceanography_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class IndexTemplateView(TemplateView):
    template_name = "oceanography/index.html"


def get_help_text_dict():
    my_dict = {}
    for obj in models.HelpText.objects.all():
        my_dict[obj.field_name] = str(obj)

    return my_dict


# MISSIONS #
############

class MissionListView(OceanographyAccessRequiredMixin, FilterView):
    template_name = "oceanography/mission_list.html"
    filterset_class = filters.MissionFilter
    queryset = shared_models.Cruise.objects.annotate(
        search_term=Concat('mission_name', 'mission_number', output_field=TextField())).order_by("-start_date", "mission_number")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_object'] = shared_models.Cruise.objects.first()
        context["field_list"] = [
            'institute',
            'mission_number',
            'mission_name',
            'vessel',
            'chief_scientist',
            'start_date',
            'end_date',
            'meds_id',
            'season',
        ]
        return context


class MissionDetailView(OceanographyAccessRequiredMixin, DetailView):
    template_name = "oceanography/mission_detail.html"
    model = shared_models.Cruise

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = False
        context['google_api_key'] = settings.GOOGLE_API_KEY
        context['field_list'] = [
            'institute',
            'mission_number',
            'mission_name',
            'description',
            'chief_scientist',
            'samplers',
            'start_date',
            'end_date',
            'probe',
            'area_of_operation',
            'number_of_profiles',
            'meds_id',
            'notes',
            'season',
            'vessel',
        ]
        return context


class MissionUpdateView(OceanographyAdminRequiredMixin, UpdateView):
    template_name = "oceanography/mission_form.html"
    model = shared_models.Cruise
    form_class = forms.MissionForm

    def get_success_url(self, **kwargs):
        return reverse_lazy("oceanography:mission_detail", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()
        context["editable"] = True
        return context


class MissionCreateView(OceanographyAdminRequiredMixin, CreateView):
    template_name = "oceanography/mission_form.html"
    model = shared_models.Cruise
    form_class = forms.MissionForm

    def get_success_url(self, **kwargs):
        return reverse_lazy("oceanography:mission_detail", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()
        context["editable"] = True
        return context


# BOTTLES #
###########

class BottleListView(OceanographyAccessRequiredMixin, ListView):
    template_name = "oceanography/bottle_list.html"

    def get_queryset(self):
        return models.Bottle.objects.filter(mission=self.kwargs["mission"])

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)

        context["mission"] = models.Mission.objects.get(id=self.kwargs["mission"])
        context["bottle"] = models.Bottle.objects.first()
        return context


class BottleDetailView(OceanographyAccessRequiredMixin, UpdateView):
    template_name = "oceanography/bottle_form.html"
    model = models.Bottle
    form_class = forms.BottleForm

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = False
        return context


class BottleUpdateView(OceanographyAdminRequiredMixin, UpdateView):
    template_name = "oceanography/bottle_form.html"
    model = models.Bottle
    form_class = forms.BottleForm

    def get_success_url(self, **kwargs):
        return reverse_lazy("oceanography:bottle_detail", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = True
        return context


# CSVs #
########
def export_mission_csv(request, pk):
    # create instance of mission:
    m = shared_models.Cruise.objects.get(pk=pk)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(slugify(m.mission_number))

    writer = csv.writer(response)

    # write the header information
    writer.writerow(['institute', m.institute])
    writer.writerow(['mission_name', m.mission_name])
    writer.writerow(['mission_number', m.mission_number])
    writer.writerow(['vessel', m.vessel])
    writer.writerow(['chief_scientist', m.chief_scientist])
    writer.writerow(['samplers', m.samplers])
    writer.writerow(['start_date (yyyy-mm-dd)', m.start_date.strftime('%Y-%m-%d')])
    writer.writerow(['end_date (yyyy-mm-dd)', m.end_date.strftime('%Y-%m-%d')])
    writer.writerow(['probe', m.probe])
    writer.writerow(['area_of_operation', m.area_of_operation])
    writer.writerow(['notes', m.notes])
    writer.writerow(['timezone', "UTC"])

    # write the header for the bottle table
    writer.writerow(["", ])
    writer.writerow([
        "bottle_uid",
        "station",
        "set",
        "event",
        "date_yyyy_mm_dd",
        "time_hh_mm",
        "sounding_m",
        "bottle_depth_m",
        "temp_c",
        "salinity",
        "salinity_units",
        "ph",
        "lat_DDdd",
        "long_DDdd",
        "ctd_filename",
        "samples_collected",
        "remarks", ])

    my_date = ""
    my_time = ""
    for b in m.bottles.all():
        try:
            my_date = b.date_time_UTC.strftime('%Y-%m-%d')
            my_time = b.date_time_UTC.strftime('%H:%M')
        except Exception as e:
            print(e)
            my_date = None
            my_time = None

        writer.writerow(
            [
                b.bottle_uid,
                b.station,
                b.set,
                b.event,
                my_date,
                my_time,
                b.sounding_m,
                b.bottle_depth_m,
                b.temp_c,
                b.salinity,
                b.get_sal_units_display(),
                b.ph,
                b.lat_DDdd,
                b.long_DDdd,
                b.ctd_filename,
                b.samples_collected,
                b.remarks, ])

    return response


# FILES #
#########

class FileCreateView(OceanographyAccessRequiredMixin, CreateView):
    template_name = "oceanography/file_form.html"
    model = models.File
    form_class = forms.FileForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse_lazy("oceanography:mission_detail", kwargs={"pk": object.mission.id}))

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = True
        context["mission"] = shared_models.Cruise.objects.get(pk=self.kwargs.get("mission"))
        return context

    def get_initial(self):
        mission = shared_models.Cruise.objects.get(pk=self.kwargs['mission'])
        return {'mission': mission}


class FileDetailView(OceanographyAccessRequiredMixin, UpdateView):
    template_name = "oceanography/file_form.html"
    model = models.File
    form_class = forms.FileForm

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = False
        return context


class FileUpdateView(OceanographyAdminRequiredMixin, UpdateView):
    template_name = "oceanography/file_form.html"
    model = models.File
    form_class = forms.FileForm

    def get_success_url(self, **kwargs):
        return reverse_lazy("oceanography:mission_detail", kwargs={"pk": self.object.mission.id})

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = True
        return context


class FileDeleteView(OceanographyAdminRequiredMixin, DeleteView):
    template_name = "oceanography/file_confirm_delete.html"
    model = models.File

    def get_success_url(self, **kwargs):
        return reverse_lazy("oceanography:mission_detail", kwargs={"pk": self.object.mission.id})


# Helptext #
############
def in_ocean_admin_group(user):
    """
    Will return True if user is in project_admin group
    """
    if user:
        return user.groups.filter(name='oceanography_admin').count() != 0


@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_ocean_admin_group, login_url='/accounts/denied/')
def delete_help_text(request, pk):
    my_obj = models.HelpText.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("oceanography:manage_help_text"))


class HelpTextCreate(OceanographyAdminRequiredMixin, CreateView):

    model = models.HelpText
    template_name = 'oceanography/manage_settings_small.html'
    form_class = forms.HelpTextForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Manage Help Text"

        if self.request.POST:
            formset = forms.HelpTextFormSet(self.request.POST)
            if formset.is_valid():
                formset.save()
                # do something with the formset.cleaned_data
                messages.success(self.request, "Items have been successfully updated")

        context['formset'] = forms.HelpTextFormSet(queryset=models.HelpText.objects.all())
        return context

    def get_success_url(self):
        return reverse('oceanography:manage_help_text')