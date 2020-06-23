from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

# from .models import Question

import datetime
import os
import pandas as pd
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django_filters.views import FilterView
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView, FormView, TemplateView
from easy_pdf.views import PDFTemplateView
# from lib.functions.fiscal_year import fiscal_year
# from lib.functions.nz import nz
from . import models
from . import forms
from . import filters
# from . import reports
from shared_models import models as shared_models

# TYPE_CHOICES = [('CTD', 'CTD'), ('ADCP', 'ADCP')]

instrument_field_list = [
    'id',
    'instrument_type',
    'serial_number',
    'purchase_date',
    'project_title',
    # 'date_of_last_service',
    'date_of_next_service',
    'is_sensor',
    # 'section',
    # 'program',
    # 'responsibility_center',
    # 'allotment_code',
    # 'existing_project_code',
    # 'status',
    # 'approved',
    # 'start_date',
    # 'end_date',
    # 'description_html',
    # 'priorities_html',
    # 'deliverables_html',
    # 'data_collection',
    # 'data_sharing',
    # 'data_storage',
    # 'metadata_url',
    # 'regional_dm',
    # 'regional_dm_needs',
    # 'sectional_dm',
    # 'sectional_dm_needs',
    # 'vehicle_needs',
    # 'it_needs',
    # 'chemical_needs',
    # 'ship_needs',
    # 'date_last_modified',
    # 'last_modified_by',
]


# Create your views here.


class CloserTemplateView(TemplateView):
    template_name = 'ios2/close_me.html'


class IndexTemplateView(TemplateView):
    template_name = 'ios2/index.html'


class InstrumentListView(LoginRequiredMixin, FilterView):
    template_name = 'ios2/instrument_list.html'
    model = models.Instrument
    filterset_class = filters.InstrumentFilter
    #
    # def get_queryset(self, **kwargs):
    #     queryset = (models.ServiceHistory.objects
    #                        .all()
    #                        .prefetch_related('instrument')
    #                        .latest('service_date'))
    #     print(self.kwargs)
    #     # print(model.all)
    #     # try:
    #     #     queryset = models.ServiceHistory.objects. \
    #     #         select_related().filter(instrument=models.Instrument.id).latest('service_date')
    #     # except:
    #     #     queryset = None
    #     return queryset

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # instrument = self.object
    #     context["field_list"] = [
    #         # 'id',
    #         'instrument_type',
    #         'serial_number',
    #         'purchase_date',
    #         'project_title',
    #         # 'date_of_last_service',
    #         'date_of_next_service',
    #         # 'last_modified_by',
    #     ]
    #
    #     context["report_mode"] = False
    #     print(self.kwargs, 'yay?')
    #     # context['service_history'] = models.ServiceHistory.objects.get(pk=self.kwargs["pk"])#latest('service_date')\
    #     try:
    #         context['service_history'] = models.ServiceHistory.objects.\
    #             select_related().filter(instrument=self.kwargs["pk"]).latest('service_date')
    #     except:
    #         print('no service recorded...')
    #
    #     # context["field_list_1"] = [
    #     #     'service_history',
    #         # 'priorities_html',
    #         # 'deliverables_html',
    #     # ]
    #     return context


class MooringListView(LoginRequiredMixin, FilterView):
    template_name = 'ios2/mooring_list.html'
    model = models.Mooring
    filterset_class = filters.MooringFilter


class InstrumentCreateView(LoginRequiredMixin, CreateView):
    model = models.Instrument
    form_class = forms.NewInstrumentForm

    def form_valid(self, form):
        object = form.save()

        return HttpResponseRedirect(reverse_lazy("ios2:instrument_detail", kwargs={"pk": object.id}))

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class InstrumentDetailView(LoginRequiredMixin, DetailView):
    model = models.Instrument

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instrument = self.object
        context["field_list"] = [
            # 'id',
            'instrument_type',
            'serial_number',
            'location',
            # 'in_service',
            'is_sensor',
            'purchase_date',
            # 'date_of_last_service',
            'date_of_next_service',
            'connector',
            'comm_port',
            'project_title',
            'scientist'
            # 'last_modified_by',
        ]

        context["report_mode"] = False
        print(self.kwargs, 'yay?')
        # context['service_history'] = models.ServiceHistory.objects.get(pk=self.kwargs["pk"])#latest('service_date')\
        try:
            context['service_history'] = models.ServiceHistory.objects. \
                select_related().filter(instrument=self.kwargs["pk"]).latest('service_date')
        except:
            print('no service recorded...')

        # context["field_list_1"] = [
        #     'service_history',
        # 'priorities_html',
        # 'deliverables_html',
        # ]
        return context


class InstrumentSubmitUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Instrument
    form_class = forms.InstrumentSubmitForm
    template_name = "ios2/instrument_submit_form.html"

    def get_initial(self):
        if self.object.submitted:
            submit = False
        else:
            submit = True

        return {
            'last_modified_by': self.request.user,
            'submitted': submit,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        context["field_list"] = instrument_field_list
        context["report_mode"] = True

        # bring in financial summary data
        # my_context = financial_summary_data(project)
        # context = {**my_context, **context}

        return context


# Not working

class InstrumentPrintDetailView(LoginRequiredMixin, PDFTemplateView):
    model = models.Instrument
    template_name = "ios2/instrument_report.html"

    def get_pdf_filename(self):
        instrument = models.Instrument.objects.get(pk=self.kwargs["pk"])
        pdf_filename = "{}-{}-{}-{}-{}.pdf".format(
            # instrument.year.id,
            # instrument.section.division.abbrev,
            # instrument.section.abbrev,
            # instrument.id,
            str(instrument.project_title).title().replace(" ", "")[:10],
        )

        return pdf_filename

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instrument = models.Instrument.objects.get(pk=self.kwargs["pk"])
        context["report_mode"] = True
        context["object"] = instrument
        context["field_list"] = instrument_field_list

        # bring in financial summary data
        # my_context = financial_summary_data(project)
        # context = {**my_context, **context}

        return context


class InstrumentDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Instrument
    permission_required = "__all__"
    success_url = reverse_lazy('ios2:instrument_list')
    success_message = _('The instrument was successfully deleted!')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class InstrumentUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Instrument
    form_class = forms.InstrumentForm
    template_name = 'ios2/instrument_form_popout.html'

    def get_initial(self):
        my_dict = {
            'last_modified_by': self.request.user,
        }

        try:
            my_dict["start_date"] = "{}-{:02d}-{:02d}".format(self.object.start_date.year, self.object.start_date.month,
                                                              self.object.start_date.day)
        except:
            print("no start date...")

        try:
            my_dict["end_date"] = "{}-{:02d}-{:02d}".format(self.object.end_date.year, self.object.end_date.month,
                                                            self.object.end_date.day)
        except:
            print("no end date...")

        return my_dict

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('ios2:close_me'))


# Moorings #
############

class MooringCreateView(LoginRequiredMixin, CreateView):
    model = models.Mooring
    template_name = 'ios2/mooring_form.html'
    form_class = forms.MooringForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse_lazy("ios2:mooring_detail", kwargs={"pk": object.id}))


class MooringDetailView(LoginRequiredMixin, DetailView):
    model = models.Mooring

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # instrument = self.object
        context["field_list"] = [
            # 'id',
            'instruments',
            'mooring',
            'mooring_number',
            'deploy_time',
            'recover_time',
            # 'orientation',
            'depth',
            'lat',
            'lon',
            'comments'

        ]

        context["report_mode"] = False

        return context


class MooringUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Mooring
    template_name = 'ios2/mooring_form_popout.html'
    form_class = forms.MooringForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('ios2:close_me'))


# Does not work
class MooringPrintDetailView(LoginRequiredMixin, PDFTemplateView):
    model = models.Mooring
    template_name = "ios2/mooring_report.html"

    def get_pdf_filename(self):
        instrument = models.Mooring.objects.get(pk=self.kwargs["pk"])
        # pdf_filename = "{}-{}-{}-{}-{}.pdf".format(
        #     # instrument.year.id,
        #     # instrument.section.division.abbrev,
        #     # instrument.section.abbrev,
        #     instrument.id,
        #     str(instrument).title().replace(" ", "")[:10],
        # )
        pdf_filename = instrument

        return pdf_filename

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instrument = models.Instrument.objects.get(pk=self.kwargs["pk"])
        context["report_mode"] = True
        context["object"] = instrument
        context["field_list"] = instrument_field_list

        return context


class MooringSubmitUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Mooring
    form_class = forms.MooringSubmitForm
    template_name = "ios2/mooring_submit_form.html"

    def get_initial(self):
        if self.object.submitted:
            submit = False
        else:
            submit = True

        return {
            'last_modified_by': self.request.user,
            'submitted': submit,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        context["field_list"] = instrument_field_list
        # context["report_mode"] = True

        # bring in financial summary data
        # my_context = financial_summary_data(project)
        # context = {**my_context, **context}

        return context


class MooringDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Mooring
    permission_required = "__all__"
    success_url = reverse_lazy('ios2:mooring_list')
    success_message = _('The mooring was successfully deleted!')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# Instrument on Mooring
from django.forms import modelformset_factory


class InstrumentMooringCreateView(LoginRequiredMixin, CreateView):
    model = models.InstrumentMooring
    template_name = 'ios2/instrumentmooring_form_popout.html'
    form_class = forms.AddInstrumentToMooringForm

    # InstrumentFormSet = modelformset_factory(models.Instrument, form=forms.InstrumentForm)
    # instrumentformset = InstrumentFormSet(queryset=models.Instrument.objects.values('instrument_type').distinct())

    def get_initial(self):
        # InstrumentFormSet = modelformset_factory(models.InstrumentMooring, form=forms.InstrumentForm)
        # instrumentformset = InstrumentFormSet(queryset=models.InstrumentMooring.objects.values('instrument').distinct())

        mooring = models.Mooring.objects.get(pk=self.kwargs['pk'])
        return {
            'mooring': mooring,
            # 'instrumentformset': instrumentformset
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mooring = models.Mooring.objects.get(pk=self.kwargs['pk'])
        # self.instrument = models.Mooring.objects.get(pk=self.kwargs['pk'])
        context['name'] = mooring

        context['adding'] = "instrument"

        context['adding_to'] = "mooring"
        # context['instrument'] = models.Instrument.objects
        context["field_list"] = [
            'instrument_type',
            'purchase_date',
        ]
        # InstrumentFormSet = modelformset_factory(models.InstrumentMooring, form=forms.InstrumentForm)
        # instrumentformset = InstrumentFormSet(queryset=models.InstrumentMooring.objects.values('instrument').distinct())
        #
        # context['instrumentformset'] = instrumentformset
        return context

    def form_valid(self, form):
        # if request.POST:

        object = form.save()

        return HttpResponseRedirect(reverse('ios2:close_me'))


class InstrumentMooringUpdateView(LoginRequiredMixin, UpdateView):
    model = models.InstrumentMooring
    template_name = 'ios2/instrumentmooring_form_popout.html'
    form_class = forms.EditInstrumentMooringForm

    def get_initial(self):
        print(self.kwargs)

        instrumentmooring = models.InstrumentMooring.objects.get(pk=self.kwargs['pk'])
        return {
            'mooring': instrumentmooring.mooring,
            'instrument': instrumentmooring.instrument,
        }

    #
    # def get_context_data(self, **kwargs):
    #
    #     context = super().get_context_data(**kwargs)
    #     # Mooring = models.Deployment.objects.get(pk=self.kwargs['pk'])
    #     # context['Mooring'] = Mooring
    #     tmp = models.InstrumentDeployment.objects.get(pk=self.kwargs['instrument'])
    #     # object = self.object
    #     print(self.kwargs, tmp.depth)
    #     context['object'] = tmp
    #     context['adding'] = "instrument"
    #
    #     context['adding_to'] = "mooring"
    #     return context

    def form_valid(self, form):
        object = form.save()

        return HttpResponseRedirect(reverse('ios2:close_me'))


# Mooringinstrument
class MooringInstrumentCreateView(LoginRequiredMixin, CreateView):
    model = models.InstrumentMooring
    template_name = 'ios2/instrumentmooring_form_popout.html'
    form_class = forms.AddMooringToInstrumentForm

    def get_initial(self):
        instrument = models.Instrument.objects.get(pk=self.kwargs['pk'])
        return {
            'instrument': instrument,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instrument = models.Instrument.objects.get(pk=self.kwargs['pk'])
        context['name'] = instrument

        context['adding'] = "mooring"

        context['adding_to'] = "instrument"
        return context

    def form_valid(self, form):
        object = form.save()

        return HttpResponseRedirect(reverse('ios2:close_me'))


class MooringInstrumentUpdateView(LoginRequiredMixin, UpdateView):
    model = models.InstrumentMooring
    template_name = 'ios2/instrumentmooring_form_popout.html'
    form_class = forms.EditInstrumentMooringForm

    def get_initial(self):
        instrumentmooring = models.InstrumentMooring.objects.get(pk=self.kwargs['pk'])
        return {
            'mooring': instrumentmooring.mooring,
            'instrument': instrumentmooring.instrument,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tmp = models.InstrumentMooring.objects.get(pk=self.kwargs['pk'])
        # object = self.object
        print(self.kwargs, tmp.depth)
        context['object'] = tmp
        context['adding'] = "instrument"

        context['adding_to'] = "mooring"
        return context

    def form_valid(self, form):
        object = form.save()

        return HttpResponseRedirect(reverse('ios2:close_me'))


class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = models.ServiceHistory
    form_class = forms.ServiceForm
    template_name = 'ios2/service_form_popout.html'

    def form_valid(self, form):
        my_object = form.save()
        was_calibrated = form.cleaned_data["was_also_calibrated"]
        was_xxx = form.cleaned_data
        print(was_xxx)
        print(form)
        print('------------')
        if was_calibrated:
            my_object.pk = None
            # print(my_object)
            # print('------------.......')
            # print(form.category)

            my_object.save()
            my_object.category = 1
            my_object.save()

            return HttpResponseRedirect(reverse('ios2:close_me'))
        else:
            my_object.save()

            print('myobject', my_object, 'myobject')
            print(my_object.pk)
            # my_object.
            return HttpResponseRedirect(reverse('ios2:close_me'))

        # def get_initial(self):
        #     return {'last_modified_by': self.request.user}

    def get_initial(self):
        instrument = models.Instrument.objects.get(pk=self.kwargs['instrument'])
        return {
            'instrument': instrument,
        }


class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = models.ServiceHistory
    form_class = forms.ServiceForm
    template_name = 'ios2/service_form_popout.html'

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('ios2:close_me'))


def service_delete(request, pk):
    object = models.ServiceHistory.objects.get(pk=pk)
    # instrument_id = object.instrument.id
    object.delete()
    messages.success(request, _("The service record has been successfully deleted!!!"))
    return HttpResponseRedirect(reverse_lazy("ios2:instrument_detail", kwargs={"pk": object.instrument.id}))

# class AddDeploymentCreateView(LoginRequiredMixin, CreateView):
#     model = models.Mooring
#     template_name = 'ios2/mooring_form_popout.html'
#
#     form_class = forms.MooringForm
#
#     def get_initial(self):
#         instrument = models.Instrument.objects.get(pk=self.kwargs['instrument'])
#         return {
#             'instruments': instrument,
#         }
#
#     def get_context_data(self, **kwargs):
#         # print(self.kwargs)
#         # input('aaa?')
#         context = super().get_context_data(**kwargs)
#         # instrument = models.Instrument.objects.get(id=self.kwargs['instrument_type'])
#         # instrument = models.Instrument.objects.get(id=self.kwargs['instrument'])
#         # instrument = models.Instrument.objects.all
#         # context['instrument'] = instrument.serial_number
#         # context['object'] = self.object
#         # context["field_list"] = ['mooring', 'mooring_number']
#         context['cost_type'] = "mooring"
#         return context
#
#     def form_valid(self, form):
#         # if form.is_valid():
#         object = form.save()
#         # else:
#         #     raise
#         return HttpResponseRedirect(reverse('ios2:close_me'))
#
#
# class DeploymentUpdateView(LoginRequiredMixin, UpdateView):
#     model = models.Mooring
#     template_name = 'ios2/mooring_form_popout.html'
#     form_class = forms.MooringForm
#
#
#     def get_initial(self):
#         mooring = models.Mooring.objects.get(pk=self.kwargs['pk'])
#         return {
#             'mooring': mooring,
#         }
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # instrument = models.Instrument.objects.get(id=self.kwargs['instrument'])
#         # context['instrument'] = self.object.instruments
#         context['mooring_number'] = self.object.mooring_number
#         context["field_list"] = ['mooring', 'mooring_number']
#         context['cost_type'] = "mooring"
#         # instrument = models.Instrument.objects.get(kwargs={"pk": pk})
#         # context['instrument'] = instrument
#         # context['object'] = self.object
#         # context['cost_type'] = _("O&M")
#         return context
#
#     def form_valid(self, form):
#         object = form.save()
#         return HttpResponseRedirect(reverse('ios2:close_me'))

# def mooring_delete(request, pk):
#     object = models.Deployment.objects.get(pk=pk)
#     object.delete()
#     messages.success(request, _("The mooring has been successfully deleted."))
#     return HttpResponseRedirect(reverse_lazy("ios2:instrument_detail", kwargs={"pk": object.instrument.id}))

#
# class InstrumentDeploymentDeleteView(LoginRequiredMixin, DeleteView):
#     model = models.InstrumentMooring
#     permission_required = "__all__"
#     success_url = reverse_lazy('ios2:instrument_detail')
#     success_message = _('The instrument was successfully deleted!')
#
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)

def mooringtoinstrument_delete(request, pk):
    object = models.InstrumentMooring.objects.get(pk=pk)
    # instrument_id = object.instrument.id
    object.delete()
    messages.success(request, _("The mooring has been successfully deleted!!!"))
    return HttpResponseRedirect(reverse_lazy("ios2:instrument_detail", kwargs={"pk": object.instrument.id}))

def instrumentonmooring_delete(request, pk):
    object = models.InstrumentMooring.objects.get(pk=pk)
    # instrument_id = object.instrument.id
    object.delete()
    messages.success(request, _("The instrument has been successfully deleted!!!"))
    return HttpResponseRedirect(reverse_lazy("ios2:mooring_detail", kwargs={"pk": object.mooring.id}))
    # return HttpResponseRedirect(reverse_lazy("ios2:mooring_detail", kwargs={"pk": instrument_id}))
