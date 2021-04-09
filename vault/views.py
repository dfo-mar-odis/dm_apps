from copy import deepcopy

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
    CommonDeleteView, CommonHardDeleteView, CommonFormsetView
from . import models
from . import forms
from . import filters


class CloserTemplateView(TemplateView):
    template_name = 'vault/close_me.html'


### Permissions ###


class VaultAccessRequired(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return True

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


def in_vault_admin_group(user):
    if "vault_admin" in [g.name for g in user.groups.all()]:
        return True


class VaultAdminAccessRequired(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return in_vault_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


def in_vault_edit_group(user):
    """this group includes the admin group so there is no need to add an admin to this group"""
    if user:
        if in_vault_admin_group(user) or user.groups.filter(name='vault_edit').count() != 0:
            return True


class VaultEditRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return in_vault_edit_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'vault/index.html')


@login_required(login_url='/accounts/login/')
@user_passes_test(in_vault_admin_group, login_url='/accounts/denied/')
def admin_tools(request):
    return render(request, 'vault/_admin.html')


## ADMIN USER ACCESS CONTROL ##


class UserListView(VaultAdminAccessRequired, CommonFilterView):
    template_name = "vault/user_list.html"
    filterset_class = filters.UserFilter
    home_url_name = "index"
    paginate_by = 25
    h1 = "Vault App User List"
    field_list = [
        {"name": 'first_name', "class": "", "width": ""},
        {"name": 'last_name', "class": "", "width": ""},
        {"name": 'email', "class": "", "width": ""},
        {"name": 'last_login|{}'.format(gettext_lazy("Last login to DM Apps")), "class": "", "width": ""},
    ]
    new_object_url = reverse_lazy("shared_models:user_new")

    def get_queryset(self):
        queryset = User.objects.order_by("first_name", "last_name").annotate(
            search_term=Concat('first_name', Value(""), 'last_name', Value(""), 'email', output_field=TextField())
        )
        if self.kwargs.get("vault"):
            queryset = queryset.filter(groups__name__icontains="vault").distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vault_admin"] = get_object_or_404(Group, name="vault_admin")
        context["vault_edit"] = get_object_or_404(Group, name="vault_edit")
        return context


@login_required(login_url='/accounts/login/')
@user_passes_test(in_vault_admin_group, login_url='/accounts/denied/')
def toggle_user(request, pk, type):
    my_user = User.objects.get(pk=pk)
    vault_admin = get_object_or_404(Group, name="vault_admin")
    vault_edit = get_object_or_404(Group, name="vault_edit")
    if type == "admin":
        # if the user is in the admin group, remove them
        if vault_admin in my_user.groups.all():
            my_user.groups.remove(vault_admin)
        # otherwise add them
        else:
            my_user.groups.add(vault_admin)
    elif type == "edit":
        # if the user is in the edit group, remove them
        if vault_edit in my_user.groups.all():
            my_user.groups.remove(vault_edit)
        # otherwise add them
        else:
            my_user.groups.add(vault_edit)
    return HttpResponseRedirect("{}#user_{}".format(request.META.get('HTTP_REFERER'), my_user.id))


## ADMIN FORMSETS ##

## INSTRUMENT TYPE ##


class InstrumentTypeHardDeleteView(VaultAdminAccessRequired, CommonHardDeleteView):
    model = models.InstrumentType
    success_url = reverse_lazy("vault:manage_instrument_type")


class InstrumentTypeFormsetView(VaultAdminAccessRequired, CommonFormsetView):
    template_name = 'vault/formset.html'
    h1 = "Manage Instrument Type"
    queryset = models.InstrumentType.objects.all()
    formset_class = forms.InstrumentTypeFormset
    success_url = reverse_lazy("vault:manage_instrument_type")
    home_url_name = "vault:index"
    delete_url_name = "vault:delete_instrument_type"


## INSTRUMENT ##


class InstrumentHardDeleteView(VaultAdminAccessRequired, CommonHardDeleteView):
    model = models.Instrument
    success_url = reverse_lazy("vault:manage_instrument")


class InstrumentFormsetView(VaultAdminAccessRequired, CommonFormsetView):
    template_name = 'vault/formset.html'
    h1 = "Manage Instrument"
    queryset = models.Instrument.objects.all()
    formset_class = forms.InstrumentFormset
    success_url = reverse_lazy("vault:manage_instrument")
    home_url_name = "vault:index"
    delete_url_name = "vault:delete_instrument"


## ORGANISATION ##


class OrganisationHardDeleteView(VaultAdminAccessRequired, CommonHardDeleteView):
    model = models.Organisation
    success_url = reverse_lazy("vault:manage_organisation")


class OrganisationFormsetView(VaultAdminAccessRequired, CommonFormsetView):
    template_name = 'vault/formset.html'
    h1 = "Manage Organisation"
    queryset = models.Organisation.objects.all()
    formset_class = forms.OrganisationFormset
    success_url = reverse_lazy("vault:manage_organisation")
    home_url_name = "vault:index"
    delete_url_name = "vault:delete_organisation"


## PLATFORM TYPE ##


# class ObservationPlatformTypeHardDeleteView(VaultAdminAccessRequired, CommonHardDeleteView):
#     model = models.ObservationPlatformType
#     success_url = reverse_lazy("vault:manage_platform_type")
#
#
# class ObservationPlatformTypeFormsetView(VaultAdminAccessRequired, CommonFormsetView):
#     template_name = 'vault/formset.html'
#     h1 = "Manage Platform Type"
#     queryset = models.ObservationPlatformType.objects.all()
#     formset_class = forms.ObservationPlatformTypeFormset
#     success_url = reverse_lazy("vault:manage_platform_type")
#     home_url_name = "vault:index"
#     delete_url_name = "vault:delete_platform_type"


## PLATFORM ##


class ObservationPlatformHardDeleteView(VaultAdminAccessRequired, CommonHardDeleteView):
    model = models.ObservationPlatform
    success_url = reverse_lazy("vault:manage_platform")


class ObservationPlatformFormsetView(VaultAdminAccessRequired, CommonFormsetView):
    template_name = 'vault/formset.html'
    h1 = "Manage Platforms"
    queryset = models.ObservationPlatform.objects.all()
    formset_class = forms.ObservationPlatformFormset
    success_url = reverse_lazy("vault:manage_platform")
    home_url_name = "vault:index"
    delete_url_name = "vault:delete_platform"


## ROLE ##


class RoleHardDeleteView(VaultAdminAccessRequired, CommonHardDeleteView):
    model = models.Role
    success_url = reverse_lazy("vault:manage_role")


class RoleFormsetView(VaultAdminAccessRequired, CommonFormsetView):
    template_name = 'vault/formset.html'
    h1 = "Manage Roles"
    queryset = models.Role.objects.all()
    formset_class = forms.RoleFormset
    success_url = reverse_lazy("vault:manage_role")
    home_url_name = "vault:index"
    delete_url_name = "vault:delete_role"


## PERSON ##


class PersonHardDeleteView(VaultAdminAccessRequired, CommonHardDeleteView):
    model = models.Person
    success_url = reverse_lazy("vault:manage_person")


class PersonFormsetView(VaultAdminAccessRequired, CommonFormsetView):
    template_name = 'vault/formset.html'
    h1 = "Manage Person"
    queryset = models.Person.objects.all()
    formset_class = forms.PersonFormset
    success_url = reverse_lazy("vault:manage_person")
    home_url_name = "vault:index"
    delete_url_name = "vault:delete_person"


# #
# # # SPECIES #
# # ###########
# #
#


class SpeciesListView(VaultAccessRequired, CommonFilterView):
    template_name = "vault/list.html"
    filterset_class = filters.SpeciesFilter
    h1 = "Species List"
    home_url_name = "vault:index"
    row_object_url_name = "vault:species_detail"
    new_btn_text = "New Species"

    queryset = models.Species.objects.annotate(
        search_term=Concat('code', 'english_name', 'french_name', 'latin_name', 'id', output_field=TextField()))

    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'code', "class": "", "width": ""},
        {"name": 'french_name', "class": "", "width": ""},
        {"name": 'english_name', "class": "", "width": ""},
        {"name": 'latin_name', "class": "", "width": ""},
        {"name": 'vor_code', "class": "red-font", "width": ""},
        {"name": 'quebec_code', "class": "", "width": ""},
        {"name": 'aphia_code', "class": "", "width": ""},

    ]

    def get_new_object_url(self):
        return reverse("vault:species_new", kwargs=self.kwargs)


class SpeciesDetailView(VaultAdminAccessRequired, CommonDetailView):
    model = models.Species
    field_list = [
        'id',
        'code',
        'english_name',
        'french_name',
        'latin_name',
        'vor_code',
        'quebec_code',
        'maritimes_code',
        'aphia_id',
    ]
    home_url_name = "vault:index"
    parent_crumb = {"title": gettext_lazy("Species List"), "url": reverse_lazy("vault:species_list")}


class SpeciesUpdateView(VaultAdminAccessRequired, CommonUpdateView):
    model = models.Species
    form_class = forms.SpeciesForm
    template_name = 'vault/form.html'
    cancel_text = _("Cancel")
    home_url_name = "vault:index"

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Species record successfully updated for : {my_object}"))
        return HttpResponseRedirect(reverse("vault:species_detail", kwargs=self.kwargs))

    def get_active_page_name_crumb(self):
        my_object = self.get_object()
        return my_object

    def get_h1(self):
        my_object = self.get_object()
        return my_object

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("vault:species_detail", kwargs=self.kwargs)}

    def get_grandparent_crumb(self):
        kwargs = deepcopy(self.kwargs)
        del kwargs["pk"]
        return {"title": _("Species List"), "url": reverse("vault:species_list", kwargs=kwargs)}


class SpeciesCreateView(VaultAdminAccessRequired, CommonCreateView):
    model = models.Species
    form_class = forms.SpeciesForm
    template_name = 'vault/form.html'
    home_url_name = "vault:index"
    h1 = gettext_lazy("Add New Species")
    parent_crumb = {"title": gettext_lazy("Species List"), "url": reverse_lazy("vault:species_list")}

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Species record successfully created for : {my_object}"))
        return super().form_valid(form)


class SpeciesDeleteView(VaultAdminAccessRequired, CommonDeleteView):
    model = models.Species
    permission_required = "__all__"
    success_url = reverse_lazy('vault:species_list')
    template_name = 'vault/confirm_delete.html'
    home_url_name = "vault:index"
    grandparent_crumb = {"title": gettext_lazy("Species List"), "url": reverse_lazy("vault:species_list")}

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse_lazy("vault:species_detail", kwargs=self.kwargs)}


# #
# # # OUTING #
# # ###########
# #
#


class OutingListView(VaultAccessRequired, CommonFilterView):
    template_name = "vault/list.html"
    filterset_class = filters.OutingFilter
    h1 = "Outing List"
    home_url_name = "vault:index"
    row_object_url_name = "vault:outing_detail"
    new_btn_text = "New Outing"

    queryset = models.Outing.objects.annotate(
        search_term=Concat('id', 'observation_platform__longname', 'identifier_string',
                           output_field=TextField()))

    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'observation_platform', "class": "", "width": ""},
        {"name": 'region', "class": "", "width": ""},
        {"name": 'purpose', "class": "", "width": ""},
        {"name": 'start_date', "class": "", "width": ""},
        {"name": 'end_date', "class": "", "width": ""},
        {"name": 'outing_duration|{}'.format(gettext_lazy("outing duration")), "class": "", "width": ""},
        {"name": 'identifier_string', "class": "", "width": ""},
        {"name": 'created_by', "class": "", "width": ""},

    ]

    def get_new_object_url(self):
        return reverse("vault:outing_new", kwargs=self.kwargs)


class OutingDetailView(VaultAdminAccessRequired, CommonDetailView):
    model = models.Outing
    field_list = [
        'id',
        'observation_platform',
        'region',
        'purpose',
        'start_date',
        'end_date',
        'outing_duration',
        'identifier_string',
        'created_by',
        'created_at',
        'verified_by',
        'verified_at',
    ]
    home_url_name = "vault:index"
    parent_crumb = {"title": gettext_lazy("Outing List"), "url": reverse_lazy("vault:outing_list")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # contexts for _observation.html file
        context["random_observation"] = models.Observation.objects.first()
        context["observation_field_list"] = [
            'instrument',
            'datetime',
            'longitude',
            'latitude',
            'observer',
            'opportunistic',
        ]

        return context


class OutingUpdateView(VaultAdminAccessRequired, CommonUpdateView):
    model = models.Outing
    form_class = forms.OutingForm
    template_name = 'vault/outing_form.html'
    cancel_text = _("Cancel")
    home_url_name = "vault:index"

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Outing record successfully updated for : {my_object}"))
        return HttpResponseRedirect(reverse("vault:outing_detail", kwargs=self.kwargs))

    def get_active_page_name_crumb(self):
        my_object = self.get_object()
        return my_object

    def get_h1(self):
        my_object = self.get_object()
        return my_object

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("vault:outing_detail", kwargs=self.kwargs)}

    def get_grandparent_crumb(self):
        kwargs = deepcopy(self.kwargs)
        del kwargs["pk"]
        return {"title": _("Outing List"), "url": reverse("vault:outing_list", kwargs=kwargs)}


class OutingCreateView(VaultAdminAccessRequired, CommonCreateView):
    model = models.Outing
    form_class = forms.OutingForm
    template_name = 'vault/outing_form.html'
    home_url_name = "vault:index"
    h1 = gettext_lazy("Add New Outing")
    parent_crumb = {"title": gettext_lazy("Outing List"), "url": reverse_lazy("vault:outing_list")}

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Outing record successfully created for : {my_object}"))
        return super().form_valid(form)

    def get_initial(self):
        return {'created_by': self.request.user}


class OutingDeleteView(VaultAdminAccessRequired, CommonDeleteView):
    model = models.Outing
    permission_required = "__all__"
    success_url = reverse_lazy('vault:outing_list')
    template_name = 'vault/confirm_delete.html'
    home_url_name = "vault:index"
    grandparent_crumb = {"title": gettext_lazy("Outing List"), "url": reverse_lazy("vault:outing_list")}

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse_lazy("vault:outing_detail", kwargs=self.kwargs)}


# #
# # # OBSERVATION #
# # ###########
# #
#


class ObservationListView(VaultAccessRequired, CommonFilterView):
    template_name = "vault/list.html"
    filterset_class = filters.ObservationFilter
    h1 = "Observation List"
    home_url_name = "vault:index"
    row_object_url_name = "vault:observation_detail"
    new_btn_text = "New Observation"

    queryset = models.Observation.objects.annotate(
        search_term=Concat('id', 'outing__observation_platform', 'instrument__name',
                           output_field=TextField()))

    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'outing', "class": "", "width": ""},
        {"name": 'instrument', "class": "", "width": ""},
        {"name": 'datetime', "class": "", "width": ""},
        {"name": 'longitude', "class": "", "width": ""},
        {"name": 'latitude', "class": "", "width": ""},
        {"name": 'observer', "class": "", "width": ""},
        {"name": 'opportunistic', "class": "", "width": ""},

    ]

    def get_new_object_url(self):
        return reverse("vault:observation_new", kwargs=self.kwargs)


class ObservationDetailView(VaultAdminAccessRequired, CommonDetailView):
    model = models.Observation
    field_list = [
        'id',
        'outing',
        'instrument',
        'datetime',
        'longitude',
        'latitude',
        'observer',
        'metadata',
        'opportunistic',

    ]
    home_url_name = "vault:index"
    parent_crumb = {"title": gettext_lazy("Observation List"), "url": reverse_lazy("vault:observation_list")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # contexts for _obsighting.html file
        context["random_obsighting"] = models.ObservationSighting.objects.first()
        context["obsighting_field_list"] = [
            'species',
            'quantity',
            'certainty',
            'health_status',
            'calf',
            'verified',
            'known_individual',
        ]

        # contexts for _media.html file
        context["random_media"] = models.OriginalMediafile.objects.first()
        context["media_field_list"] = [
            'filename',
            'file_path',
            'metadata',

        ]

        return context

class ObservationUpdateView(VaultAdminAccessRequired, CommonUpdateView):
    model = models.Observation
    form_class = forms.ObservationForm
    template_name = 'vault/form.html'
    cancel_text = _("Cancel")
    home_url_name = "vault:index"

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Observation record successfully updated for : {my_object}"))
        return HttpResponseRedirect(reverse("vault:observation_detail", kwargs=self.kwargs))

    def get_active_page_name_crumb(self):
        my_object = self.get_object()
        return my_object

    def get_h1(self):
        my_object = self.get_object()
        return my_object

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("vault:observation_detail", kwargs=self.kwargs)}

    def get_grandparent_crumb(self):
        kwargs = deepcopy(self.kwargs)
        del kwargs["pk"]
        return {"title": _("Observation List"), "url": reverse("vault:observation_list", kwargs=kwargs)}


class ObservationCreateView(VaultAdminAccessRequired, CommonCreateView):
    model = models.Observation
    form_class = forms.ObservationForm
    template_name = 'vault/form.html'
    home_url_name = "vault:index"
    h1 = gettext_lazy("Add New Observation")
    parent_crumb = {"title": gettext_lazy("Observation List"), "url": reverse_lazy("vault:observation_list")}

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Observation record successfully created for : {my_object}"))
        return super().form_valid(form)


class ObservationDeleteView(VaultAdminAccessRequired, CommonDeleteView):
    model = models.Observation
    permission_required = "__all__"
    success_url = reverse_lazy('vault:observation_list')
    template_name = 'vault/confirm_delete.html'
    home_url_name = "vault:index"
    grandparent_crumb = {"title": gettext_lazy("Observation List"), "url": reverse_lazy("vault:observation_list")}

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse_lazy("vault:observation_detail", kwargs=self.kwargs)}