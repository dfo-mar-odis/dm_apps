from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from django.contrib import messages
from django.utils.translation import gettext as _
from django_filters.views import FilterView
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from django.db.models import Q
from shared_models import models as shared_models
from publications import filters

import json

from . import models
from . import forms


def get_mod(mod_str):

    lookup_mod = None

    if mod_str == "theme":
        lookup_mod = models.Theme
    elif mod_str == "pillar":
        lookup_mod = models.Pillar
    elif mod_str == "human":
        lookup_mod = models.HumanComponent
    elif mod_str == "ecosystem":
        lookup_mod = models.EcosystemComponent
    elif mod_str == "linkage":
        lookup_mod = models.ProgramLinkage
    elif mod_str == "site":
        lookup_mod = models.Site
    elif mod_str == "publication":
        lookup_mod = models.Publication
    elif mod_str == "computer_environment":
        lookup_mod = models.ComputerEnvironment
    elif mod_str == "spatial":
        lookup_mod = models.SpatialManagementDesignation
    elif mod_str == "spatialproduct":
        lookup_mod = models.SpatialDataProduct
    elif mod_str == "spatialproductyear":
        lookup_mod = models.SpatialDataProductYear
    elif mod_str == "sourceinternal":
        lookup_mod = models.SourceDataInternal
    elif mod_str == "sourceexternal":
        lookup_mod = models.SourceDataExternal
    elif mod_str == "computerlibraries":
        lookup_mod = models.ComputerLibraries
    elif mod_str == "fgp":
        lookup_mod = models.FgpLinkage
    elif mod_str == "code":
        lookup_mod = models.CodeSite
    elif mod_str == "contact_external":
        lookup_mod = models.ExternalContact
    elif mod_str == "contact_internal":
        lookup_mod = models.InternalContact
    elif mod_str == "geoscope":
        lookup_mod = models.GeographicScope
    elif mod_str == "spatialscale":
        lookup_mod = models.SpatialScale
    elif mod_str == "organization":
        lookup_mod = models.Organization

    return lookup_mod


def lookup_delete(request, lookup, project, theme):
    project = models.Project.objects.get(pk=project)
    mod = get_mod(lookup)
    val = mod.objects.get(pk=theme)
    if project:
        if mod is models.Theme:
            project.theme.remove(val)
        elif mod is models.HumanComponent:
            project.human_component.remove(val)
        elif mod is models.EcosystemComponent:
            project.ecosystem_component.remove(val)
        elif mod is models.Pillar:
            project.sustainability_pillar.remove(val)
        elif mod is models.ProgramLinkage:
            project.program_linkage.remove(val)
        elif mod is models.GeographicScope:
            project.geographic_scope.remove(val)
        elif mod is models.InternalContact:
            project.dfo_contact.remove(val)
        elif mod is models.Organization:
            project.organization.remove(val)
        elif mod is models.SpatialScale:
            project.spatial_scale.remove(val)
        elif issubclass(mod, models.TextLookup):
            val.delete()

    messages.success(request, _("The " + mod._meta.verbose_name.title() + " has been successfully deleted."))
    return HttpResponseRedirect(reverse_lazy("publications:prj_detail", kwargs={"pk": project.id}))


def lookup_add(project, mod, val):
    if project and not mod.objects.filter(pk=val.id, project__id=project.id):
        if mod is models.Theme:
            project.theme.add(val)
        elif mod is models.HumanComponent:
            project.human_component.add(val)
        elif mod is models.EcosystemComponent:
            project.ecosystem_component.add(val)
        elif mod is models.Pillar:
            project.sustainability_pillar.add(val)
        elif mod is models.ProgramLinkage:
            project.program_linkage.add(val)
        elif mod is models.GeographicScope:
            project.geographic_scope.add(val)
        elif mod is models.InternalContact:
            project.dfo_contact.add(val)
        elif mod is models.Organization:
            project.organization.add(val)
        elif mod is models.SpatialScale:
            project.spatial_scale.add(val)
        return True

    return False


class CloserTemplateView(TemplateView):
    template_name = 'publications/close_me.html'


class IndexTemplateView(TemplateView):
    template_name = 'publications/index.html'


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'publications/pub_form.html'
    model = models.Project

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

    form_class = forms.NewProjectForm
    template_name = "publications/pub_form.html"

    def get_initial(self):
        my_dict = {
            'key': self.kwargs['pk'],
            'last_modified_by': self.request.user,
        }

        return my_dict


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Publication
    permission_required = "__all__"
    success_url = reverse_lazy('publications:index')
    success_message = _('The project was successfully deleted!')
    template_name = 'publications/pub_confirm_delete.html'


    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class SiteDetailView(LoginRequiredMixin, DetailView):
    template_name = 'publications/pub_site.html'
    model = models.Site

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ProjectDetailView(DetailView):
    permission_required = 'publications.publications_admin'
    template_name = 'publications/pub_detail.html'
    model = models.Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        context['google_api_key'] = settings.GOOGLE_API_KEY
        context["has_admin"] = "publications_admin" in [v for k,v in self.request.user.groups.all().values_list()]
        context["coordinates"] = models.GeoCoordinate.objects.filter(project__id=project.id)
        context["divisions"] = shared_models.Division.objects.filter(project__id=project.id)

        if len(context["coordinates"]) == 1:
            context["center"] = {
                "lat": context["coordinates"][0].north_south,
                "lon": context["coordinates"][0].east_west
            }
        elif len(context["coordinates"]) > 2:
            lat = 0;
            lon = 0;
            for i in range(0, len(context["coordinates"])):
                cor = context["coordinates"][i]
                lat = lat + cor.north_south
                lon = lon + cor.east_west
            context["center"] = {
                "lat": (lat/len(context["coordinates"])),
                "lon": (lon/len(context["coordinates"]))
            }
        else:
            context["center"] = {"lat": 44.0, "lon": -60.0}

        context["abstract"] = [
            'abstract',
            'method'
        ]

        context["field_list"] = [
            # {
            #     "url": None,
            #     "label": "Division",
            #     "list": project.division
            # },
            {
                "url": "computer_environment",
                "label": models.ComputerEnvironment._meta.verbose_name_plural,
                "list": models.ComputerEnvironment.objects.filter(project__id=project.id)
            },
            {
                "url": "spatial",
                "label": models.SpatialManagementDesignation._meta.verbose_name_plural,
                "list": models.SpatialManagementDesignation.objects.filter(project__id=project.id)
            },
            {
                "url": "spatialproduct",
                "label": models.SpatialDataProduct._meta.verbose_name_plural,
                "list": models.SpatialDataProduct.objects.filter(project__id=project.id)
            },
            {
                "url": "spatialproductyear",
                "label": models.SpatialDataProductYear._meta.verbose_name_plural,
                "list": models.SpatialDataProductYear.objects.filter(project__id=project.id)
            },
            {
                "url": "computerlibraries",
                "label": models.ComputerLibraries._meta.verbose_name_plural,
                "list": models.ComputerLibraries.objects.filter(project__id=project.id)
            },
            {
                "url": "sourceinternal",
                "label": models.SourceDataInternal._meta.verbose_name_plural,
                "list": models.SourceDataInternal.objects.filter(project__id=project.id)
            },
            {
                "url": "sourceexternal",
                "label": models.SourceDataExternal._meta.verbose_name_plural,
                "list": models.SourceDataExternal.objects.filter(project__id=project.id)
            },
            {
                "url": "site",
                "label": models.Site._meta.verbose_name_plural,
                "list": models.Site.objects.filter(project__id=project.id)
            },
            {
                "url": "fgp",
                "label": models.FgpLinkage._meta.verbose_name_plural,
                "list": models.FgpLinkage.objects.filter(project__id=project.id)
            },
            {
                "url": "code",
                "label": models.CodeSite._meta.verbose_name_plural,
                "list": models.CodeSite.objects.filter(project__id=project.id)
            },
            {
                "url": "contact_external",
                "label": models.ExternalContact._meta.verbose_name_plural,
                "list": models.ExternalContact.objects.filter(project__id=project.id)
            },
            {
                "url": "publication",
                "label": models.Publication._meta.verbose_name_plural,
                "list": models.Publication.objects.filter(project__id=project.id)
            },
        ]

        context["lookups"] = [
            {
                "url": "theme",
                "label": models.Theme._meta.verbose_name_plural,
                "list": models.Theme.objects.filter(project__id=project.id).order_by("name")
            },
            {
                "url": "pillar",
                "label": models.Pillar._meta.verbose_name_plural,
                "list": models.Pillar.objects.filter(project__id=project.id).order_by("name")
            },
            {
                "url": "human",
                "label": models.HumanComponent._meta.verbose_name_plural,
                "list": models.HumanComponent.objects.filter(project__id=project.id).order_by("name")
            },
            {
                "url": "ecosystem",
                "label": models.EcosystemComponent._meta.verbose_name_plural,
                "list": models.EcosystemComponent.objects.filter(project__id=project.id).order_by("name")
            },
            {
                "url": "linkage",
                "label": models.ProgramLinkage._meta.verbose_name_plural,
                "list": models.ProgramLinkage.objects.filter(project__id=project.id).order_by("name")
            },
            {
                "url": "geoscope",
                "label": models.GeographicScope._meta.verbose_name_plural,
                "list": models.GeographicScope.objects.filter(project__id=project.id).order_by("name")
            },
            {
                "url": "spatialscale",
                "label": models.SpatialScale._meta.verbose_name_plural,
                "list": models.SpatialScale.objects.filter(project__id=project.id).order_by("name")
            },
            {
                "url": "contact_internal",
                "label": models.InternalContact._meta.verbose_name_plural,
                "list": models.InternalContact.objects.filter(project__id=project.id)
            },
            {
                "url": "organization",
                "label": models.Organization._meta.verbose_name_plural,
                "list": models.Organization.objects.filter(project__id=project.id).order_by("name")
            },
        ]
        context
        context["field_list_1"] = [
            'human_component',
            'ecosystem_component',
            'spatial_management',
            'sustainability_pillar',
            'program_linkage',
        ]

        if models.GeographicScope.objects.filter(project__id=project.id):
            geo = models.GeographicScope.objects.filter(project__id=project.id)
            context["polygon"] = []
            for g in geo:
                poly_points = models.Polygon.objects.filter(geoscope=g)
                if poly_points:
                    poly = {
                        'name': str(g),
                        'points': []
                    }
                    for point in poly_points:
                        poly['points'].append(point)
                    context["polygon"].append(poly)
        return context


class ProjectListView(FilterView):
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

        print("lookup mod: " + str(lookup_mod))
        return {
            'project': project,
            'lookup': lookup_mod
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = models.Project.objects.get(id=self.kwargs['project'])
        context['project'] = project
        context['title'] = get_mod(self.kwargs['lookup'])._meta.verbose_name
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
            dirty = lookup_add(project, mod, val)

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

    def form_valid(self, form):
        context = self.get_context_data()
        print(context['project'])
        text_obj = form.save(commit=False)
        text_obj.project = context['project']
        text_obj.save()

        return HttpResponseRedirect(reverse('publications:close_me'))
