from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import gettext as _
from django_filters.views import FilterView
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse_lazy, reverse

from django.db.models import Q
from shared_models import models as shared_models
from publications import filters

import json

from . import models
from . import forms


def get_mod(mod_str):
    if mod_str == "theme":
        lookup_mod = models.Theme
    elif mod_str == "human":
        lookup_mod = models.HumanComponents
    elif mod_str == "linkage":
        lookup_mod = models.ProgramLinkage
    elif mod_str == "ecosystem":
        lookup_mod = models.EcosystemComponents
    elif mod_str == "site":
        lookup_mod = models.Site
    elif mod_str == "publication":
        lookup_mod = models.Publication

    return lookup_mod


def get_mod_title(mod_str):
    if mod_str == "theme":
        title = "Theme"
    elif mod_str == "human":
        title = "Human Component"
    elif mod_str == "linkage":
        title = "Linkage to Program"
    elif mod_str == "ecosystem":
        title = "Ecosystem Component"
    elif mod_str == "site":
        title = "Site"
    elif mod_str == "publication":
        title = "Publication"

    return title


def lookup_delete(request, lookup, project, theme):
    project = models.Project.objects.get(pk=project)
    mod = get_mod(lookup)
    val = mod.objects.get(pk=theme)
    if project:
        if mod is models.Theme:
            project.theme.remove(val)
        elif mod is models.HumanComponents:
            project.human_component.remove(val)
        elif mod is models.ProgramLinkage:
            project.program_linkage.remove(val)
        elif mod is models.EcosystemComponents:
            project.ecosystem_component.remove(val)
        elif issubclass(mod, models.TextLookup):
            val.delete()

    messages.success(request, _("The " + get_mod_title(lookup) + " has been successfully deleted."))
    return HttpResponseRedirect(reverse_lazy("publications:prj_detail", kwargs={"pk": project.id}))


class CloserTemplateView(TemplateView):
    template_name = 'publications/close_me.html'


class IndexTemplateView(TemplateView):
    template_name = 'publications/index.html'


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'publications/pub_form.html'
    model = models.Project
    login_url = '/accounts/login_required/'
    form_class = forms.NewProjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # here are the option objects we want to send in through context
        # only from the science branches of each region
        division_choices = [(d.id, str(d)) for d in
                            shared_models.Division.objects.filter(Q(branch_id=1) | Q(branch_id=3)).order_by("branch__region", "name")]

        division_dict = {}
        for s in division_choices:
            division_dict[s[1]] = s[0]

        context['division_json'] = json.dumps(division_dict)

        return context

    def form_valid(self, form):
        project = form.save()

        return HttpResponseRedirect(reverse_lazy("publications:pub_detail", kwargs={"pk": project.id}))

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class ProjectSubmitUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Project
    login_url = '/accounts/login_required/'
    form_class = forms.ProjectSubmitForm
    template_name = "publications/pub_submit_form.html"

    def get_initial(self):

        return {
            'last_modified_by': self.request.user,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Project
    login_url = '/accounts/login_required/'
    form_class = forms.NewProjectForm
    template_name = "publications/pub_form.html"

    def get_initial(self):
        my_dict = {
            'last_modified_by': self.request.user,
        }

        return my_dict


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Project
    permission_required = "__all__"
    success_url = reverse_lazy('publications:')
    success_message = _('The publication was successfully deleted!')
    login_url = '/accounts/login_required/'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class SiteDetailView(LoginRequiredMixin, DetailView):
    template_name = 'publications/pub_site.html'
    model = models.Site

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    template_name = 'publications/pub_detail.html'
    model = models.Project
    login_url = '/accounts/login_required/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        context["abstract"] =[
            'abstract'
        ]

        comp_env_array = [site for site in models.ComputerEnvironment.objects.filter(project__id=project.id)]
        sdi_array = [site for site in models.SourceDataInternal.objects.filter(project__id=project.id)]
        sde_array = [site for site in models.SourceDataExternal.objects.filter(project__id=project.id)]
        spatial_array = [site for site in models.SpatialManagementDesignation.objects.filter(project__id=project.id)]
        spatial_product_array = [site for site in models.SpatialDataProduct.objects.filter(project__id=project.id)]
        site_array = [site for site in models.Site.objects.filter(project__id=project.id)]
        pub_array = [pub for pub in models.Publication.objects.filter(project__id=project.id)]
        print(str(project.id) + ": " + str(site_array))
        context["field_list"] = [
            # {
            #     "url": None,
            #     "label": "Division",
            #     "list": project.division
            # },
            {
                "url": "computer_environment",
                "label": "Computer Environment(s)",
                "list": comp_env_array
            },
            {
                "url": "spatial",
                "label": "Spatial Management Designation(s)",
                "list": spatial_array
            },
            {
                "url": "spatialproduct",
                "label": "Spatial Data Product(s)",
                "list": spatial_product_array
            },
            {
                "url": "sourceinternal",
                "label": "Source Data Internal",
                "list": sdi_array
            },
            {
                "url": "sourceexternal",
                "label": "Source Data External",
                "list": sde_array
            },
            {
                "url": "site",
                "label": "Site(s)",
                "list": site_array
            },
            {
                "url": "publication",
                "label": "Publications(s)",
                "list": pub_array
            },
        ]

        context["lookups"] = [
            {
                "url": "theme",
                "label": "Theme",
                "list": models.Theme.objects.filter(project__id=project.id).order_by("name")
            },
            {
                "url": "pillar",
                "label": "Pillar of sustainability",
                "list": models.Pillar.objects.filter(project__id=project.id).order_by("name")
            },
            {
                "url": "human",
                "label": "Human Component",
                "list": models.HumanComponent.objects.filter(project__id=project.id).order_by("name")
            },
            {
                "url": "ecosystem",
                "label": "Ecosystem Component",
                "list": models.EcosystemComponent.objects.filter(project__id=project.id).order_by("name")
            },
            {
                "url": "linkage",
                "label": "Linkage to Program",
                "list": models.ProgramLinkage.objects.filter(project__id=project.id).order_by("name")
            },
        ]
        context["field_list_1"] = [
            'human_component',
            'ecosystem_component',
            'spatial_management',
            'sustainability_pillar',
            'program_linkage',
        ]

        return context


class ProjectListView(LoginRequiredMixin, FilterView):
    login_url = '/accounts/login_required/'
    template_name = 'publications/pub_list.html'
    model = models.Project
    filterset_class = filters.ProjectFilter


'''
LookupAddView is an abstract class with the basic code
common to popout views used to add or edit values

Subclasses of this view should override the __init__
method and set the self.form_class to the specific
form required for the data entry
'''


class LookupAddView(LoginRequiredMixin, CreateView):
    template_name = 'publications/lookup_new_popout.html'
    model = models.Theme
    form_class = forms.LookupForm

    def get_initial(self):
        project = models.Project.objects.get(pk=self.kwargs['project'])
        lookup_mod = get_mod(self.kwargs['lookup'])

        return {
            'project': project,
            'lookup': lookup_mod
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = models.Project.objects.get(id=self.kwargs['project'])
        context['project'] = project
        context['title'] = get_mod_title(self.kwargs['lookup'])
        context['url_var'] = self.kwargs['lookup']

        return context


'''
ChoiceAddView is an extension of the LookupAddView.
It uses the forms.LookupForm to display a multiple text select
UI Component and a text field to enter values that are missing
from the text select.

This class is intended to deal with models that extend the Lookup
abstract class and require the models to have a "name" field
'''


class ChoiceAddView(LookupAddView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_class = forms.LookupForm
        print(self.form_class)

    def form_valid(self, form):
        mod = get_mod(self.kwargs['lookup'])

        name_pk = form.cleaned_data['mult_name']
        vals = [t for t in mod.objects.filter(pk__in=name_pk)]

        # if values were selected in the multiple choice 'name' field add them to the publication
        # Otherwise check to see if a new lookup was created, add to its lookup table then use
        # its lookup value as the name_pk

        if form.cleaned_data['name']:
            val = form.save()
            print("New object: " + str(val))
            vals.append(val)

        # get the publication the lookup are being added to
        project = models.Project.objects.get(id=self.kwargs['project'])

        dirty = False
        # for each lookup make sure it doesn't already exist in the publication variable
        for val in vals:
            if project and not mod.objects.filter(pk=val.id, project__id=project.id):
                if mod is models.Theme:
                    project.theme.add(val)
                elif mod is models.HumanComponents:
                    project.human_component.add(val)
                elif mod is models.ProgramLinkage:
                    project.program_linkage.add(val)
                elif mod is models.EcosystemComponents:
                    project.ecosystem_component.add(val)
                dirty = True

        if dirty:
            project.save()

        return HttpResponseRedirect(reverse('publications:close_me'))


'''
TextAddView is an extension of the LookupAddView.
It uses the forms.TextForm to display a TextArea
UI Component for large text entry

This class is intended to deal with models that extend the TextLookup
abstract class and require the models to have a "value" field and a
"project" field
'''


class TextAddView(LookupAddView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_class = forms.TextForm
        print(self.form_class)

    def form_valid(self, form):
        context = self.get_context_data()
        print(context['project'])
        text_obj = form.save(commit=False)
        text_obj.project = context['project']
        text_obj.save()

        return HttpResponseRedirect(reverse('publications:close_me'))
