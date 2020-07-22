import os
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import TextField
from django.db.models.functions import Concat
from django.utils import timezone
from django.utils.translation import gettext as _
from django_filters.views import FilterView
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView, FormView, TemplateView
###

from lib.functions.custom_functions import nz
from . import models
from . import forms
from . import filters
from . import reports


# Create your views here.
class CloserTemplateView(TemplateView):
    template_name = 'masterlist/close_me.html'


def in_masterlist_group(user):
    if user:
        return user.groups.filter(name='masterlist_access').count() != 0


class MasterListAccessRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):


    def test_func(self):
        return in_masterlist_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


def in_masterlist_admin_group(user):
    if user:
        return user.groups.filter(name='masterlist_admin').count() != 0


class MasterListAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):


    def test_func(self):
        return in_masterlist_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class IndexTemplateView(MasterListAccessRequiredMixin, TemplateView):
    template_name = 'masterlist/index.html'


# PERSON #
##########

class PersonListView(MasterListAccessRequiredMixin, FilterView):
    template_name = 'masterlist/person_list.html'
    filterset_class = filters.PersonFilter
    model = models.Person
    queryset = models.Person.objects.annotate(
        search_term=Concat('first_name', 'last_name', 'notes', output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.Person.objects.first()
        context["field_list"] = [
            'last_name',
            'first_name',
            'phone_1',
            'phone_2',
            'email_1',
        ]
        return context


class PersonDetailView(MasterListAccessRequiredMixin, DetailView):
    model = models.Person

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'first_name',
            'last_name',
            'phone_1',
            'phone_2',
            'fax',
            'email_1',
            'email_2',
            'notes',
            'last_modified_by',
        ]
        return context



class PersonUpdateView(MasterListAccessRequiredMixin, UpdateView):
    model = models.Person
    form_class = forms.PersonForm

    def get_initial(self):
        return {
            'last_modified_by': self.request.user,
        }


class PersonUpdateViewPopout(MasterListAccessRequiredMixin, UpdateView):
    template_name = 'masterlist/person_form_popout.html'
    model = models.Person
    form_class = forms.PersonForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('masterlist:close_me'))

    def get_initial(self):
        return {
            'last_modified_by': self.request.user,
        }

class PersonCreateView(MasterListAccessRequiredMixin, CreateView):
    model = models.Person
    form_class = forms.PersonForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class PersonCreateViewPopout(MasterListAccessRequiredMixin, CreateView):
    template_name = 'masterlist/person_form_popout.html'
    model = models.Person
    form_class = forms.PersonForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('masterlist:close_me'))

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class PersonDeleteView(MasterListAdminRequiredMixin, DeleteView):
    model = models.Person
    success_url = reverse_lazy('masterlist:person_list')
    success_message = 'The person was deleted successfully!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# ORGANIZATION #
################

class OrganizationListView(MasterListAccessRequiredMixin, FilterView):
    template_name = 'masterlist/organization_list.html'
    filterset_class = filters.OrganizationFilter
    model = models.Organization
    queryset = models.Organization.objects.annotate(
        search_term=Concat('name_eng', 'abbrev', output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.Organization.objects.first()
        context["field_list"] = [
            'name_eng',
            'name_ind',
            'abbrev',
            'province',
        ]
        return context


class OrganizationDetailView(MasterListAccessRequiredMixin, DetailView):
    model = models.Organization

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'name_eng',
            'name_ind',
            'abbrev',
            'address',
            'city',
            'postal_code',
            'province',
            'phone',
            'fax',
            'key_species',
            'dfo_contact_instructions',
            'notes',
            'grouping',
            'regions',
            'sectors',
            'date_last_modified',
            'last_modified_by',
        ]
        return context


class OrganizationUpdateView(MasterListAccessRequiredMixin, UpdateView):
    model = models.Organization
    form_class = forms.OrganizationForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class OrganizationCreateView(MasterListAccessRequiredMixin, CreateView):
    model = models.Organization
    form_class = forms.OrganizationForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class OrganizationDeleteView(MasterListAdminRequiredMixin, DeleteView):
    model = models.Organization
    success_url = reverse_lazy('masterlist:org_list')
    success_message = 'The organization was deleted successfully!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# MEMBER  (ORGANIZATION MEMBER) #
#################################

class MemberCreateView(MasterListAccessRequiredMixin, CreateView):
    model = models.OrganizationMember
    template_name = 'masterlist/member_form_popout.html'

    form_class = forms.NewMemberForm

    def get_initial(self):
        org = models.Organization.objects.get(pk=self.kwargs['org'])
        return {
            'organization': org,
            'last_modified_by': self.request.user
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        org = models.Organization.objects.get(id=self.kwargs['org'])
        context['organization'] = org

        # get a list of people
        person_list = [
            '<a href="#" class="person_insert" code={id}>{first} {last}</a>'.format(
                id=p.id, first=p.first_name, last=p.last_name
            ) for p in models.Person.objects.all()
        ]

        context['person_list'] = person_list

        return context

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('masterlist:close_me'))


class MemberUpdateView(MasterListAccessRequiredMixin, UpdateView):
    model = models.OrganizationMember
    template_name = 'masterlist/member_form_popout.html'
    form_class = forms.MemberForm


    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('masterlist:close_me'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get a list of people
        person_list = [
            '<a href="#" class="person_insert" code={id}>{first} {last}</a>'.format(
                id=p.id, first=p.first_name, last=p.last_name
            ) for p in models.Person.objects.all()
        ]

        context['person_list'] = person_list

        return context

    def get_initial(self):
        return {
            'last_modified_by': self.request.user
        }


def member_delete(request, pk):
    object = models.OrganizationMember.objects.get(pk=pk)
    object.delete()
    messages.success(request, _("The member has been successfully deleted from the organization."))
    return HttpResponseRedirect(reverse_lazy("masterlist:org_detail", kwargs={"pk": object.organization.id}))


# CONSULTATION INSTRUCTION #
############################

class InstructionCreateView(MasterListAccessRequiredMixin, CreateView):
    model = models.ConsultationInstruction
    template_name = 'masterlist/instruction_form.html'
    form_class = forms.InstructionForm

    def get_initial(self):
        org = models.Organization.objects.get(pk=self.kwargs['org'])
        return {
            'organization': org,
            'last_modified_by': self.request.user
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        org = models.Organization.objects.get(id=self.kwargs['org'])
        context['org'] = org

        return context

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse_lazy('masterlist:instruction_edit', kwargs={"pk":object.id}))


class InstructionUpdateView(MasterListAccessRequiredMixin, UpdateView):
    model = models.ConsultationInstruction
    template_name = 'masterlist/instruction_form.html'
    form_class = forms.InstructionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # # get a list of members from only the indigenous organizations
        member_list = ['<a href="#" class="add-btn" target-url="{target_url}">{text}</a>'.format(
            target_url=reverse_lazy("masterlist:recipient_new", kwargs={"instruction": self.object.id, "member": member.id}),
            text=member) for member in models.OrganizationMember.objects.filter(organization__grouping__is_indigenous=True)]
        context['member_list'] = member_list

        return context

    def get_initial(self):
        return {
            'last_modified_by': self.request.user
        }


class InstructionDeleteView(MasterListAdminRequiredMixin, DeleteView):
    model = models.ConsultationInstruction
    success_message = _("The organization's consultation instructions were deleted successfully!")
    template_name = 'masterlist/instruction_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("masterlist:org_detail", kwargs={"pk": self.object.organization.id})


# REPORTS #
###########

class ReportSearchFormView(MasterListAccessRequiredMixin, FormView):
    template_name = 'masterlist/report_search.html'
    form_class = forms.ReportSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        report = int(form.cleaned_data["report"])
        provinces = str(form.cleaned_data["provinces"]).replace("[", "").replace("]", "").replace(" ", "").replace("'", "")
        groupings = str(form.cleaned_data["groupings"]).replace("[", "").replace("]", "").replace(" ", "").replace("'", "")
        sectors = str(form.cleaned_data["sectors"]).replace("[", "").replace("]", "").replace(" ", "").replace("'", "")
        regions = str(form.cleaned_data["regions"]).replace("[", "").replace("]", "").replace(" ", "").replace("'", "")
        is_indigenous = int(form.cleaned_data["is_indigenous"])
        species = str(form.cleaned_data["species"])

        if provinces == "":
            provinces = "None"
        if groupings == "":
            groupings = "None"
        if sectors == "":
            sectors = "None"
        if regions == "":
            regions = "None"
        if species == "":
            species = "None"

        if report == 1:
            return HttpResponseRedirect(reverse("masterlist:export_custom_list", kwargs={
                'provinces': provinces,
                'groupings': groupings,
                'sectors': sectors,
                'regions': regions,
                'is_indigenous': is_indigenous,
                'species': species,
            }))

        else:
            messages.error(self.request, "Report is not available. Please select another report.")
            return HttpResponseRedirect(reverse("masterlist:report_search"))


def export_custom_list(request, provinces, groupings, sectors, regions, is_indigenous, species):
    file_url = reports.generate_custom_list(provinces, groupings, sectors, regions, is_indigenous, species)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename="custom master list export {}.xlsx"'.format(
                timezone.now().strftime("%Y-%m-%d"))
            return response
    raise Http404
