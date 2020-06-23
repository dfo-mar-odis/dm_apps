from datetime import datetime

import requests
from django.db.models.functions import Concat
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView, TemplateView, FormView, ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, TextField
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django_filters.views import FilterView
from django.utils import timezone

from lib.templatetags.custom_filters import nz
from . import models
from . import forms
from . import filters
from . import reports

from numpy import arange
import math
import collections
import csv
from shared_models import models as shared_models


# Create your views here.

def in_herring_group(user):
    if user:
        return user.groups.filter(name='herring_access').count() != 0


def in_herring_admin_group(user):
    if user:
        return user.groups.filter(name='herring_admin').count() != 0


class HerringAdminAccessRequired(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return in_herring_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class HerringAccessRequired(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return in_herring_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


@login_required(login_url='/accounts/login/')
@user_passes_test(in_herring_group, login_url='/accounts/denied/')
def index(request):
    return render(request, 'herring/index.html')


# class IndexView(AnonymousRequiredMixin,TemplateView):
#     template_name = 'herring/index.html'
# group_required = [u"herring_access",]


class CloserTemplateView(TemplateView):
    template_name = 'herring/close_me.html'


# SAMPLER #
###########

class SamplerPopoutCreateView(HerringAccessRequired, CreateView):
    template_name = 'herring/sampler_form_popout.html'
    model = models.Sampler
    form_class = forms.SamplerForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse_lazy("herring:close_sampler", kwargs={"sampler": object.id}))


class SamplerCloseTemplateView(HerringAccessRequired, TemplateView):
    template_name = 'herring/sampler_close.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = models.Sampler.objects.get(pk=self.kwargs["sampler"])
        context["object"] = object
        return context


# SAMPLE #
##########
class SampleFilterView(HerringAccessRequired, FilterView):
    filterset_class = filters.SampleFilter
    template_name = "herring/sample_filter.html"

    def get_queryset(self):
        return models.Sample.objects.all().order_by("sample_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['field_list'] = [
            'id',
            'type',
            'sample_date',
            'sampler_ref_number',
            'survey_id',
            'sampler',
            'port',
            'experimental_net_used',
            'total_fish_preserved',
        ]
        return context
    # def get_filterset_kwargs(self, filterset_class):
    #     kwargs = super().get_filterset_kwargs(filterset_class)
    #     if kwargs["data"] is None:
    #         kwargs["data"] = {"season": timezone.now().year }
    #     return kwargs


class SampleCreateView(HerringAccessRequired, CreateView):
    template_name = 'herring/sample_form.html'
    form_class = forms.SampleForm
    model = models.Sample

    def get_initial(self):
        return {
            'created_by': self.request.user,
            'last_modified_by': self.request.user,
            'do_another': 1,
        }

    def form_valid(self, form):
        object = form.save()
        # port_sample_tests(object)
        if form.cleaned_data["do_another"] == 1:
            return HttpResponseRedirect(reverse_lazy('herring:sample_new'))
        else:
            return HttpResponseRedirect(reverse_lazy('herring:sample_list'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get a list of ports
        port_list = ['<a href="#" class="port_insert" code={}>{}</a>'.format(p.id, p) for p in shared_models.Port.objects.all()]
        context['port_list'] = port_list

        # get a list of samplers
        sampler_list = []
        for s in models.Sampler.objects.all():
            if s.first_name:
                first = s.first_name.replace("'", "")
            else:
                first = None

            if s.last_name:
                last = s.last_name.replace("'", "")
            else:
                last = None

            html_insert = '<a href="#" class="sampler_insert" code={id}>{first} {last}</a>'.format(id=s.id, first=first,
                                                                                                   last=last)
            sampler_list.append(html_insert)
        context['sampler_list'] = sampler_list
        return context


class SampleDeleteView(HerringAccessRequired, DeleteView):
    template_name = 'herring/sample_confirm_delete.html'
    model = models.Sample
    success_url = reverse_lazy("herring:sample_list")


class SampleUpdateView(HerringAccessRequired, UpdateView):
    template_name = 'herring/sample_form.html'
    form_class = forms.SampleForm
    model = models.Sample

    def get_initial(self):
        return {
            'last_modified_by': self.request.user,
        }

    def form_valid(self, form):
        # port_sample_tests(self.object)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get a list of districts
        # get a list of ports
        port_list = ['<a href="#" class="port_insert" code={}>{}</a>'.format(p.id, p) for p in shared_models.Port.objects.all()]
        context['port_list'] = port_list

        # get a list of samplers
        sampler_list = []
        for s in models.Sampler.objects.all():
            if s.first_name:
                first = s.first_name.replace("'", "")
            else:
                first = None

            if s.last_name:
                last = s.last_name.replace("'", "")
            else:
                last = None

            html_insert = '<a href="#" class="sampler_insert" code={id}>{first} {last}</a>'.format(id=s.id, first=first,
                                                                                                   last=last)
            sampler_list.append(html_insert)
        context['sampler_list'] = sampler_list
        return context


class SamplePopoutUpdateView(HerringAccessRequired, UpdateView):
    template_name = 'herring/sample_form_popout.html'
    model = models.Sample

    def get_form_class(self):
        if self.kwargs["type"] == "measured":
            return forms.SampleFishMeasuredForm
        elif self.kwargs["type"] == "preserved":
            return forms.SampleFishPreservedForm

    def get_initial(self):
        return {
            'last_modified_by': self.request.user,
        }

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse("herring:close_me"))


class SampleDetailView(HerringAccessRequired, DetailView):
    template_name = 'herring/sample_detail.html'
    model = models.Sample

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # pass in the tests
        tests = models.Test.objects.filter(Q(id=205) | Q(id=230) | Q(id=231) | Q(id=232))
        context['tests'] = tests
        context['field_list'] = [
            'type',
            'sample_date',
            'sampler_ref_number',
            'sampler',
            'port',
            'survey_id',
            'latitude_n',
            'longitude_w',
            'fishing_area',
            'gear',
            'experimental_net_used',
            'vessel_cfvn',
            'mesh_size',
            'catch_weight_lbs',
            'sample_weight_lbs',
            'total_fish_measured',
            'total_fish_preserved',
            'old_id',
            'remarks',
            'created_by',
            'creation_date',
            'last_modified_by',
            'last_modified_date',
        ]

        # create a list of length freq counts FOR SAMPLE
        if self.object.length_frequency_objects.count() > 0:
            count_list = []
            for obj in self.object.length_frequency_objects.all():
                count_list.append(obj.count)

            # add the max count as context
            context['max_count'] = max(count_list)

            # add the sum as context
            context['sum_count'] = sum(count_list)

            # add the phrase to read
            playback_string = "Reading back frequency counts. "
            playback_string = playback_string + ", ".join(str(count) for count in count_list)
            context['playback_string'] = playback_string

        # create a list of length freq counts FISH DETAILs
        length_list = []
        for obj in self.object.fish_details.all().order_by("fish_length"):
            if obj.fish_length:
                original_length_cm = obj.fish_length / 10
                integer = math.floor(original_length_cm)
                decimal = (original_length_cm - integer)
                if decimal > 0 and decimal <= 0.5:
                    new_decimal = 0.5
                else:
                    new_decimal = 1
                binned_length = new_decimal + integer

                length_list.append(binned_length)
        if len(length_list) > 0:
            # return a dict of length_bins and corresponding counts
            bin_dict = collections.Counter(length_list)
            bin_list = arange(min(length_list), max(length_list) + 0.5, step=0.5)
            max_fish_detail_count = 0
            sum_fish_detail_count = 0
            for i in range(0, len(bin_list)):
                count = bin_dict[bin_list[i]]
                bin_dict[bin_list[i]] = count
                if count > max_fish_detail_count:
                    max_fish_detail_count = count
                sum_fish_detail_count = sum_fish_detail_count + count
            context['bin_list'] = bin_list
            context['bin_dict'] = bin_dict
            context['max_fish_detail_count'] = max_fish_detail_count
            context['sum_fish_detail_count'] = sum_fish_detail_count

        # provide a list of fish detail lab_processed_dates
        for fishy in self.object.fish_details.all():
            fishy.save()
        # resave the sample instance to run thought sample save method
        self.object.save()
        print(self.object.lab_processing_complete)
        # now conduct the test

        return context


def move_sample_next(request, sample):
    # shared vars
    message_end = "You are at the last sample."

    sample_list = models.Sample.objects.all().order_by("id")
    record_count = sample_list.count()

    # populate a list with all fish detail ids
    id_list = [s.id for s in sample_list]

    # figure out where the current record is within recordset
    current_index = id_list.index(sample)

    # if you are at the end of the recordset, there is nowhere to go!
    if sample == id_list[-1]:
        messages.success(request, message_end)
        return HttpResponseRedirect(reverse(viewname='herring:sample_detail', kwargs={"pk": sample, }))

    # othersise move forward 1
    else:
        target_id = id_list[current_index + 1]
        return HttpResponseRedirect(reverse(viewname='herring:sample_detail', kwargs={"pk": target_id, }))


# Length Frequeny wizard #
##########################

class LengthFrquencyWizardConfirmation(HerringAccessRequired, TemplateView):
    template_name = 'herring/length_freq_wizard_confirmation.html'


class LengthFrquencyWizardSetupFormView(HerringAccessRequired, FormView):
    template_name = 'herring/length_freq_wizard_setup.html'
    form_class = forms.LengthFrquencyWizardSetupForm

    def form_valid(self, form):
        sample = int(self.kwargs["sample"])
        from_length = str(form.cleaned_data['minimum_length'])
        to_length = str(form.cleaned_data['maximum_length'])

        # Delete any existing length frequency data associated with this sample
        models.LengthFrequency.objects.filter(sample_id=sample).delete()

        return HttpResponseRedirect(reverse('herring:lf_wizard', kwargs={
            "sample": sample,
            "from_length": from_length,
            "to_length": to_length,
            "current_length": from_length,
        }))


class LengthFrquencyWizardFormView(HerringAccessRequired, FormView):
    template_name = 'herring/length_freq_wizard.html'
    form_class = forms.LengthFrquencyWizardForm

    def form_valid(self, form):
        sample = int(self.kwargs["sample"])
        from_length = float(self.kwargs['from_length'])
        to_length = float(self.kwargs['to_length'])
        current_length = float(self.kwargs['current_length'])
        models.LengthFrequency.objects.create(sample_id=sample, length_bin_id=current_length,
                                              count=form.cleaned_data['count'])

        if current_length == to_length:
            # port_sample_tests(models.Sample.objects.get(pk=sample))
            return HttpResponseRedirect(reverse('herring:close_me'))
        else:
            return HttpResponseRedirect(reverse('herring:lf_wizard', kwargs={
                "sample": sample,
                "from_length": from_length,
                "to_length": to_length,
                "current_length": str(current_length + 0.5)
            }))


class LengthFrquencyUpdateView(HerringAccessRequired, UpdateView):
    model = models.LengthFrequency
    template_name = 'herring/length_freq_wizard.html'
    fields = ["count"]

    # form_class = forms.LengthFrquencyWizardForm

    def form_valid(self, form):
        object = form.save()
        # port_sample_tests(object.sample)
        return HttpResponseRedirect(reverse('herring:close_me'))


# FISH DETAIL #
##############

class FishDetailView(HerringAccessRequired, DetailView):
    template_name = 'herring/fish_detail.html'
    model = models.FishDetail

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FishCreateView(HerringAccessRequired, CreateView):
    template_name = 'herring/fish_form.html'
    form_class = forms.FishForm
    model = models.FishDetail

    def get_initial(self):
        return {
            'sample': self.kwargs['sample'],
            'created_by': self.request.user,
            'last_modified_by': self.request.user,
        }


class FishUpdateView(HerringAccessRequired, UpdateView):
    template_name = 'herring/fish_form.html'
    form_class = forms.FishForm
    model = models.FishDetail

    def get_initial(self):
        return {
            'last_modified_by': self.request.user,
        }


class FishDeleteView(HerringAccessRequired, DeleteView):
    template_name = 'herring/fish_confirm_delete.html'
    model = models.FishDetail

    def get_success_url(self):
        return reverse_lazy('herring:sample_detail', kwargs={'pk': self.kwargs['sample']})


# lab samples

class LabSampleConfirmation(HerringAccessRequired, TemplateView):
    template_name = 'herring/lab_sample_confirmation.html'


def lab_sample_primer(request, sample):
    # figure out what the fish number is
    my_sample = models.Sample.objects.get(pk=sample)
    if my_sample.fish_details.count() == 0:
        fish_number = 1
    else:
        fish_number = my_sample.fish_details.order_by("fish_number").last().fish_number + 1

    # create new instance of FishDetail with appropriate primed detail
    my_fishy = models.FishDetail.objects.create(created_by=request.user, sample_id=sample, fish_number=fish_number)
    return HttpResponseRedirect(reverse('herring:lab_sample_form', kwargs={
        "sample": sample,
        "pk": my_fishy.id,
    }))


class FishboardTestView(HerringAccessRequired, TemplateView):
    template_name = 'herring/fishboard_test_form.html'



class LabSampleUpdateView(HerringAccessRequired, UpdateView):
    template_name = 'herring/lab_sample_form.html'
    model = models.FishDetail
    form_class = forms.LabSampleForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # pass in the tests
        tests = models.Test.objects.filter(
            Q(id=201) | Q(id=202) | Q(id=203) | Q(id=204) | Q(id=207) | Q(id=208) | Q(id=300) | Q(id=301) | Q(id=303) | Q(id=304) | Q(
                id=306) | Q(id=307)).order_by("id")
        context['tests'] = tests

        # determine the progress of data entry
        ## there are 6 fields: len, wt, g_wt, sex, mat, parasite; HOWEVER parasites are only looked at from sea samples
        progress = 0
        if self.object.fish_length:
            progress = progress + 1
        if self.object.fish_weight:
            progress = progress + 1
        if self.object.sex:
            progress = progress + 1
        if self.object.maturity:
            progress = progress + 1
        if self.object.gonad_weight != None:
            progress = progress + 1
        if self.object.sample.type == 2:
            if self.object.parasite != None:
                progress = progress + 1
            total_tests = 6
        else:
            total_tests = 5

        context['progress'] = progress
        context['total_tests'] = total_tests

        # determine if this is the last sample in the series
        ## populate a list with all fish detail ids
        id_list = []
        for f in models.FishDetail.objects.filter(sample_id=self.kwargs["sample"]).order_by("id"):
            id_list.append(f.id)

        ##determine if this fish is on the leading edge
        if self.object.id == id_list[-1]:
            context['last_record'] = True
        return context

    def get_initial(self):
        return {
            'last_modified_by': self.request.user,
            'lab_sampler': self.request.user,
        }

    def form_valid(self, form):
        object = form.save()
        print(form.cleaned_data["where_to"])
        if form.cleaned_data["where_to"] == "home":
            return HttpResponseRedirect(reverse("herring:sample_detail", kwargs={'pk': object.sample.id, }))
        elif form.cleaned_data["where_to"] == "prev":
            return HttpResponseRedirect(reverse("herring:move_record",
                                                kwargs={'sample': object.sample.id, "type": "lab", "direction": "prev",
                                                        "current_id": object.id}))
        elif form.cleaned_data["where_to"] == "next":
            return HttpResponseRedirect(reverse("herring:move_record",
                                                kwargs={'sample': object.sample.id, "type": "lab", "direction": "next",
                                                        "current_id": object.id}))
        elif form.cleaned_data["where_to"] == "new":
            return HttpResponseRedirect(reverse("herring:lab_sample_primer", kwargs={'sample': object.sample.id, }))
        else:
            return HttpResponseRedirect(
                reverse("herring:lab_sample_form", kwargs={'sample': object.sample.id, 'pk': object.id}))


# this view should have a progress bar and a button to get started. also should display any issues and messages about the input.

def delete_fish_detail(request, sample, pk):
    fishy = models.FishDetail.objects.get(pk=pk)
    fishy.delete()
    return HttpResponseRedirect(reverse("herring:sample_detail", kwargs={"pk": sample}))


# Otolith

class OtolithUpdateView(HerringAccessRequired, UpdateView):
    template_name = 'herring/otolith_form.html'
    model = models.FishDetail
    form_class = forms.OtolithForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pass in the tests
        tests = models.Test.objects.filter(
            Q(id=200) | Q(id=206) | Q(id=209) | Q(id=210) | Q(id=211) | Q(id=309) | Q(id=310)).order_by(
            "id")
        context['tests'] = tests

        # determine the progress of data entry
        ## there are 2 fields: len, wt, g_wt, sex, mat, parasite; HOWEVER parasites are only looked at from sea samples
        progress = 0
        if self.object.annulus_count:
            progress = progress + 1
        if self.object.otolith_season:
            progress = progress + 1
        total_tests = 2

        context['progress'] = progress
        context['total_tests'] = total_tests

        # provide some context about the position of the current record
        try:
            next_fishy = \
                models.FishDetail.objects.filter(sample=self.object.sample, fish_number=self.object.fish_number + 1)[0]
        except Exception as e:
            print(e)
        else:
            context['next_fish_id'] = next_fishy.id

        context["prev_record"] = reverse("herring:move_record",
                                         kwargs={'sample': self.object.sample.id, "type": "otolith",
                                                 "direction": "prev", "current_id": self.object.id})
        context["next_record"] = reverse("herring:move_record",
                                         kwargs={'sample': self.object.sample.id, "type": "otolith",
                                                 "direction": "next", "current_id": self.object.id})
        context["home"] = reverse("herring:sample_detail", kwargs={'pk': self.object.sample.id, })

        return context

    def get_initial(self):
        return {
            'last_modified_by': self.request.user,
            'otolith_sampler': self.request.user,
        }

    def form_valid(self, form):
        object = form.save()

        if form.cleaned_data["where_to"] == "home":
            return HttpResponseRedirect(reverse("herring:sample_detail", kwargs={'pk': object.sample.id, }))
        elif form.cleaned_data["where_to"] == "prev":
            return HttpResponseRedirect(reverse("herring:move_record",
                                                kwargs={'sample': object.sample.id, "type": "otolith",
                                                        "direction": "prev", "current_id": object.id}))
        elif form.cleaned_data["where_to"] == "next":
            return HttpResponseRedirect(reverse("herring:move_record",
                                                kwargs={'sample': object.sample.id, "type": "otolith",
                                                        "direction": "next", "current_id": object.id}))
        else:
            return HttpResponseRedirect(
                reverse("herring:otolith_form", kwargs={'sample': object.sample.id, 'pk': object.id}))


# SHARED #
##########
def move_record(request, sample, type, direction, current_id):
    # shared vars
    message_start = "You are at the start of the recordset."
    message_end = "You are at the end of the recordset."

    if type == "lab":
        viewname = "herring:lab_sample_form"
    elif type == "otolith":
        viewname = "herring:otolith_form"

    # prime a listto store ids
    id_list = []

    record_count = models.FishDetail.objects.filter(sample_id=sample).count()

    # populate a list with all fish detail ids
    for f in models.FishDetail.objects.filter(sample_id=sample).order_by("id"):
        id_list.append(f.id)

    # figure out where the current record is within recordset
    current_index = id_list.index(current_id)

    # PgaeUp
    if direction == "prev":
        # if at beginning, cannot go further back!
        if current_index == 0:
            messages.success(request, message_start)
            return HttpResponseRedirect(reverse(viewname=viewname, kwargs={'sample': sample, "pk": current_id, }))
        # otherwise, just move backwards 1
        else:
            target_id = id_list[current_index - 1]
            return HttpResponseRedirect(reverse(viewname=viewname, kwargs={'sample': sample, "pk": target_id}))

    # PageDown
    elif direction == "next":
        # if you are at the end of the recordset, there is nowhere to go!
        if current_id == id_list[-1]:
            messages.success(request, message_end)
            return HttpResponseRedirect(reverse(viewname=viewname, kwargs={'sample': sample, "pk": current_id, }))

        # othersise move forward 1
        else:
            target_id = id_list[current_index + 1]
            return HttpResponseRedirect(reverse(viewname=viewname, kwargs={'sample': sample, "pk": target_id}))


# REPORTS #
###########


class ReportSearchFormView(HerringAccessRequired, FormView):
    template_name = 'herring/report_search.html'

    form_class = forms.ReportSearchForm

    def get_initial(self):
        # default the year to the year of the latest samples
        return {
            # "report": 1,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        report = int(form.cleaned_data["report"])
        year = int(form.cleaned_data["year"])

        if report == 1:
            return HttpResponseRedirect(reverse("herring:progress_report_detail", kwargs={'year': year}))
        elif report == 2:
            return HttpResponseRedirect(reverse("herring:export_fish_detail", kwargs={'year': year}))
        elif report == 3:
            return HttpResponseRedirect(reverse("herring:export_hlen", kwargs={'year': year}))
        elif report == 4:
            return HttpResponseRedirect(reverse("herring:export_hlog", kwargs={'year': year}))
        elif report == 5:
            return HttpResponseRedirect(reverse("herring:export_hdet", kwargs={'year': year}))
        elif report == 6:
            return HttpResponseRedirect(reverse("herring:export_sample_report", kwargs={'year': year}))
        else:
            messages.error(self.request, "Report is not available. Please select another report.")
            return HttpResponseRedirect(reverse("herring:report_search"))


class ProgressReportListView(HerringAccessRequired, ListView):
    template_name = 'herring/report_progress_list.html'

    def get_queryset(self):
        return models.Sample.objects.filter(season=self.kwargs["year"]).order_by("sample_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs = models.Sample.objects.filter(season=self.kwargs["year"])

        # sum of samples
        context["sample_sum"] = qs.count

        # sum of fish
        running_total = 0
        for sample in qs:
            running_total = running_total + nz(sample.total_fish_preserved, 0)
        context["fish_sum"] = running_total

        # LAB PROCESSING

        # sum of samples COMPLETE
        context["sample_sum_lab_complete"] = qs.filter(lab_processing_complete=True).count

        # sum of fish COMPLETE
        running_total = 0
        for sample in qs.filter(lab_processing_complete=True):
            running_total = running_total + sample.total_fish_preserved
        context["fish_sum_lab_complete"] = running_total

        # sum of samples REMAINING
        context["sample_sum_lab_remaining"] = qs.filter(lab_processing_complete=False).count

        # sum of fish REMAINING
        running_total = 0
        for sample in qs.filter(lab_processing_complete=False):
            running_total = running_total + nz(sample.total_fish_preserved, 0)
        context["fish_sum_lab_remaining"] = running_total

        # OTOLITH PROCESSING

        # sum of samples COMPLETE
        context["sample_sum_oto_complete"] = qs.filter(otolith_processing_complete=True).count

        # sum of fish COMPLETE
        running_total = 0
        for sample in qs.filter(otolith_processing_complete=True):
            running_total = running_total + nz(sample.total_fish_preserved, 0)
        context["fish_sum_oto_complete"] = running_total

        # sum of samples REMAINING
        context["sample_sum_oto_remaining"] = qs.filter(otolith_processing_complete=False).count

        # sum of fish REMAINING
        running_total = 0
        for sample in qs.filter(otolith_processing_complete=False):
            running_total = running_total + nz(sample.total_fish_preserved, 0)
        context["fish_sum_oto_remaining"] = running_total

        return context


def export_progress_report(request, year):
    response = reports.generate_progress_report(year)
    return response


def export_fish_detail(request, year):
    response = reports.generate_fish_detail_report(year)
    return response


def export_sample_report(request, year):
    response = reports.generate_sample_report(year)
    return response


def export_hlog(request, year):
    response = reports.generate_hlog(year)
    return response


def export_hlen(request, year):
    response = reports.generate_hlen(year)
    return response


def export_hdet(request, year):
    response = reports.generate_hdet(year)
    return response


# ADMIN #
#########

class CheckUsageListView(HerringAdminAccessRequired, ListView):
    template_name = "herring/check_usage.html"
    model = models.FishDetail

    # show only the top twenty results
    queryset = model.objects.all().order_by('-last_modified_date')[:50]


class ImportFileView(HerringAdminAccessRequired, CreateView):
    model = models.File
    fields = "__all__"

    def get_template_names(self):
        if self.kwargs.get("type") == "sample":
            return 'herring/sample_file_import_form.html'
        if self.kwargs.get("type") == "lf":
            return 'herring/lf_file_import_form.html'
        if self.kwargs.get("type") == 'detail':
            return 'herring/detail_file_import_form.html'

    def form_valid(self, form):
        my_object = form.save()
        # now we need to do some magic with the file...

        # load the file
        url = self.request.META.get("HTTP_ORIGIN") + my_object.file.url
        r = requests.get(url)
        csv_reader = csv.DictReader(r.text.splitlines())

        # loop through each row of the csv file
        for row in csv_reader:
            # what to do if we are importing a sample data export..
            if self.kwargs.get("type") == "sample":
                # each row will represent a sample
                # we only want herring.. so if there is a species field, it should be clupea ...
                species_name = row.get("species")
                if not species_name or species_name.lower().startswith("clupea"):

                    # let's get or create a sample based on the uuid
                    my_sample, created = models.Sample.objects.get_or_create(
                        old_id=row.get("uuid"),
                        sample_date=datetime.strptime(row.get("sample_date"), "%Y-%m-%d %H:%M:%S%z"),
                    )

                    # let's do this easy stuff in one shot:
                    my_sample.type = row.get("type")
                    my_sample.survey_id = nz(row.get("survey_id"), None)
                    my_sample.sampler_ref_number = nz(row.get("sampler_ref_number"), None)
                    my_sample.latitude_n = nz(row.get("latitude_n"), None)
                    my_sample.longitude_w = nz(row.get("longitude_w"), None)
                    my_sample.experimental_net_used = row.get("experimental_net_used")
                    my_sample.sample_weight_lbs = nz(row.get("sample_weight_lbs"), None)
                    my_sample.catch_weight_lbs = nz(row.get("catch_weight_lbs"), None)
                    my_sample.total_fish_measured = nz(row.get("total_fish_measured"), None)
                    my_sample.total_fish_preserved = nz(row.get("total_fish_preserved"), None)
                    my_sample.remarks = nz(row.get("remarks"), None)
                    my_sample.creation_date = datetime.strptime(row.get("creation_date"), "%Y-%m-%d %H:%M:%S%z")
                    my_sample.last_modified_date = datetime.strptime(row.get("last_modified_date"), "%Y-%m-%d %H:%M:%S%z") if row.get(
                        "last_modified_date") else None
                    my_sample.created_by = self.request.user
                    my_sample.last_modified_by = self.request.user
                    my_sample.vessel_cfvn = nz(row.get("vessel_cfvn"), None)

                    # now the trickier stuff:
                    # SAMPLER
                    if row.get("sampler"):
                        sedna_sampler = row.get("sampler").lower().split(", ")  # this will be in the format [last_name, first_name]
                        # look for something similar in the hermorrhage db
                        herm_sampler = models.Sampler.objects.filter(
                            first_name__istartswith=sedna_sampler[1],
                            last_name__iexact=sedna_sampler[0],
                        )
                        if herm_sampler.count() == 1:
                            # bingo, we found our man
                            print("bingo, we found our man")
                            my_sample.sampler = herm_sampler.first()
                        elif herm_sampler.count() == 0:
                            print("no hits for sampler")
                            # this user appears to be absent from hermorrhage db
                            new_sampler = models.Sampler.objects.create(first_name=sedna_sampler[1], last_name=sedna_sampler[0])
                            my_sample.sampler = new_sampler
                        else:
                            print("more than one hit for sampler")
                            # we are in a position where there are more than one hits.. try using the whole first name.
                            # if there are still more than one hits we can just choose the first sampler arbitrarily... means there is a duplicate
                            # If no hits probably safer just to create a new sampler
                            herm_sampler = models.Sampler.objects.filter(
                                first_name__iexact=sedna_sampler[1],
                                last_name__iexact=sedna_sampler[0],
                            )
                            if herm_sampler.count() > 0:
                                # bingo, we found our man (after a few adjustments)
                                print("bingo, we found our man (after a few adjustments)")
                                my_sample.sampler = herm_sampler.first()
                            else:
                                print("no hits for sampler, when using full first name")
                                # this user appears to be absent from hermorrhage db
                                new_sampler = models.Sampler.objects.create(first_name=sedna_sampler[1], last_name=sedna_sampler[0])
                                my_sample.sampler = new_sampler
                    else:
                        herm_sampler = models.Sampler.objects.get(pk=29)  # sampler = UNKNOWN

                    # FISHING AREA
                    # since this is more fundamental, let's crush the script is not found
                    # look for something exactly the same in the hermorrhage db
                    if row.get("fishing_area"):
                        my_sample.fishing_area = models.FishingArea.objects.get(nafo_area_code__iexact=row.get("fishing_area"))

                    # GEAR
                    # same for gear. not finding something here is unacceptable
                    if row.get("gear"):
                        my_sample.gear = models.Gear.objects.get(gear_code__iexact=row.get("gear"))

                    # MESH SIZE
                    if row.get("mesh_size"):
                        try:
                            my_mesh = models.MeshSize.objects.get(size_mm=row.get("mesh_size"))
                        except models.MeshSize.DoesNotExist:
                            my_mesh = models.MeshSize.objects.create(
                                size_mm=row.get("mesh_size")
                            )
                        my_sample.mesh_size = my_mesh

                    # PORT
                    if row.get("port_code"):
                        # not finding something here is unacceptable
                        for port in shared_models.Port.objects.all():
                            if row.get("port_code") == port.full_code:
                                my_sample.port = port
                                break

                    my_sample.save()
                else:
                    messages.warning(self.request,
                                     "Skipping sample with uuid {} because it is not a herring sample.".format(row.get("uuid")))
            elif self.kwargs.get("type") == "lf":
                # each row will represent a length frequency object
                # let's get the sample based on the uuid; if not found we should crash because something went wrong
                try:
                    my_sample = models.Sample.objects.get(old_id=row.get("sample_uuid"))
                except models.Sample.DoesNotExist:
                    messages.warning(self.request,
                                     "Sample with uuid {} was not found in the hermorrhage db. This length frequecy will be skipped".format(
                                         row.get("sample_uuid")))
                else:
                    my_lf, created = models.LengthFrequency.objects.get_or_create(
                        sample=my_sample,
                        length_bin_id=row.get("length_bin"),
                    )
                    my_lf.count = row.get("count")
                    my_lf.save()
                    my_sample.save()  # run the save method to do a few updates

            elif self.kwargs.get("type") == "detail":
                # each row will represent a fish detail
                # let's get the sample based on the uuid; if not found we should crash because something went wrong
                my_sample = models.Sample.objects.get(old_id=row.get("sample_uuid"))

                # DJF: I DON'T HAVE THE TIME TO COMPLETE THIS RIGHT NOW. THIS YEAR (2019) THERE WERE NO FISH DETAIL RECORDS
                # PROCCESSED IN SEDNA SO I WILL KICK THE CAN DOWN UNTIL A LATER DATE
                # Note: this import scirpt is a combination of the sample import and the lf import above.
                messages.info(self.request,
                              "Due to limited time resources, this import script was not developed. Once fish details are process on "
                              "boats, this function will be built")
        # clear the file in my object
        my_object.delete()
        return HttpResponseRedirect(reverse_lazy('herring:index'))


# SAMPLER #
###########

class SamplerListView(HerringAdminAccessRequired, FilterView):
    template_name = "herring/sampler_list.html"
    filterset_class = filters.SamplerFilter
    queryset = models.Sampler.objects.annotate(
        search_term=Concat('first_name', 'last_name', output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_object'] = models.Sampler.objects.first()
        context["field_list"] = [
            'full_name|Sampler name',
        ]
        return context


class SamplerDetailView(HerringAdminAccessRequired, DetailView):
    model = models.Sampler

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'first_name',
            'last_name',
            'notes',
        ]
        return context


class SamplerUpdateView(HerringAdminAccessRequired, UpdateView):
    model = models.Sampler
    form_class = forms.SamplerForm

    def get_success_url(self):
        return reverse_lazy("herring:sampler_detail", kwargs={"pk": self.get_object().id})


class SamplerCreateView(HerringAdminAccessRequired, CreateView):
    model = models.Sampler
    form_class = forms.SamplerForm

    def form_valid(self, form):
        my_object = form.save()
        return HttpResponseRedirect(reverse_lazy("herring:sampler_detail", kwargs={"pk": my_object.id}))


class SamplerDeleteView(HerringAdminAccessRequired, DeleteView):
    model = models.Sampler
    permission_required = "__all__"
    success_url = reverse_lazy('herring:sampler_list')
    success_message = 'The sampler was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
