from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from grais import filters
from grais import forms
from grais import models
from grais.mixins import GraisAccessRequiredMixin
from grais.utils import is_grais_admin
from shared_models.views import CommonFilterView, CommonUpdateView, CommonCreateView, \
    CommonDetailView, CommonDeleteView


# INCIDENTAL REPORT #
#####################

class ReportListView(GraisAccessRequiredMixin, CommonFilterView):
    model = models.IncidentalReport
    filterset_class = filters.ReportFilter
    template_name = "grais/list.html"
    home_url_name = "grais:index"


class ReportUpdateView(GraisAccessRequiredMixin, CommonUpdateView):
    model = models.IncidentalReport
    form_class = forms.ReportForm
    template_name = "grais/form.html"
    home_url_name = "grais:index"

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class ReportCreateView(GraisAccessRequiredMixin, CommonCreateView):
    model = models.IncidentalReport
    form_class = forms.ReportForm
    template_name = "grais/form.html"
    home_url_name = "grais:index"
    parent_crumb = {"title": _("Reports"), "url": reverse_lazy("grais:ir_list")}

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class ReportDetailView(GraisAccessRequiredMixin, CommonDetailView):
    model = models.IncidentalReport

    template_name = "grais/scratch/report_detail.html"

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

        # # get a list of species
        # species_list = []
        # for obj in models.Species.objects.all():
        #     url = reverse("grais:report_species_add", kwargs={"report": self.object.id, "species": obj.id}),
        #     html_insert = '<a class="add-btn btn btn-outline-dark" href="#" target-url="{}"> <img src="{}" alt=""></a><span style="margin-left: 10px;">{} / <em>{}</em> / {}</span>'.format(
        #         url[0],
        #         static("admin/img/icon-addlink.svg"),
        #         obj.common_name,
        #         obj.scientific_name,
        #         obj.abbrev
        #     )
        #     species_list.append(html_insert)
        # context['species_list'] = species_list
        return context


class ReportDeleteView(GraisAccessRequiredMixin, CommonDeleteView):
    model = models.IncidentalReport
    success_url = reverse_lazy('grais:report_list')
    success_message = 'The report was successfully deleted!'
    template_name = "grais/confirm_delete.html"

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
