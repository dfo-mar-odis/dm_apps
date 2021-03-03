import csv
from abc import ABC

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy, gettext
from django.views import View
from django.views.generic import UpdateView, CreateView, TemplateView, DeleteView, ListView, FormView
from django.views.generic.detail import SingleObjectMixin, DetailView
from django_filters.views import FilterView

###
from dm_apps.utils import custom_send_mail
from . import emails, filters
from . import forms
from . import models
from .mixins import CommonMixin, CommonFormMixin, CommonListMixin, CommonPopoutFormMixin, CommonPopoutMixin


class CloserTemplateView(TemplateView):
    template_name = 'shared_models/close_me.html'


class CloserNoRefreshTemplateView(TemplateView):
    template_name = 'shared_models/close_me_no_refresh.html'


def in_admin_group(user):
    """give a list of groups that would be allowed to access this form"""
    if user.id:
        if user.groups.filter(name='travel_admin').count() != 0 or \
                user.groups.filter(name='projects_admin').count() or \
                user.groups.filter(name='scifi_admin').count() or \
                user.groups.filter(name='travel_adm_admin').count():
            return True


class CommonTemplateView(TemplateView, CommonMixin):
    def get_context_data(self, **kwargs):
        # we want to update the context with the context vars added by CommonMixin classes
        context = super().get_context_data(**kwargs)
        context.update(super().get_common_context())
        return context


# CommonCreate Extends the UserPassesTestMixin used to determine if a user has
# has the correct privileges to interact with Creation Views
class CommonCreateView(CommonFormMixin, CreateView):
    submit_text = None

    # default template to use to create an update
    #  shared_entry_form.html contains the common navigation elements at the top of the template
    template_name = 'shared_models/shared_entry_form.html'

    def get_h1(self):
        if self.h1:
            return self.h1
        else:
            return gettext("New {}".format(self.model._meta.verbose_name.title()))

    def get_submit_text(self):
        if self.submit_text:
            return self.submit_text
        else:
            return gettext("Add")

    def get_context_data(self, **kwargs):
        # we want to update the context with the context vars added by CommonMixin classes
        context = super().get_context_data(**kwargs)
        context.update(super().get_common_context())
        return context

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                if self.get_parent_crumb():
                    return self.get_parent_crumb().get("url")
                else:
                    raise ImproperlyConfigured(
                        "No URL to redirect to.  Either provide a url or define"
                        " a get_absolute_url method on the Model.")
        return url


class CommonAuthCreateView(UserPassesTestMixin, CommonCreateView):
    # These are for testing purposes only
    auth = True
    login_url = '/accounts/login_required/'

    # this should be overriden in an extending class to determine if a user is authorized to do certain actions
    def test_func(self):
        return self.auth

    def get_auth(self):
        return self.auth

    def get_context_data(self, **kwargs):
        # we want to update the context with the context vars added by CommonMixin classes
        context = super().get_context_data(**kwargs)
        context["auth"] = self.get_auth()
        return context


class CommonUpdateView(CommonFormMixin, UpdateView):
    submit_text = None
    delete_url = None

    def get_h1(self):
        if self.h1:
            return self.h1
        else:
            return gettext("Edit")

    def get_submit_text(self):
        if self.submit_text:
            return self.submit_text
        else:
            return gettext("Save")

    def get_delete_url(self):
        return self.delete_url

    # default template to use to update an update
    #  shared_entry_form.html contains the common navigation elements at the top of the template
    template_name = 'shared_models/shared_entry_form.html'

    def get_context_data(self, **kwargs):
        # we want to update the context with the context vars added by CommonMixin classes
        context = super().get_context_data(**kwargs)
        context.update(super().get_common_context())
        context["model_name"] = self.get_object()._meta.verbose_name
        context["delete_url"] = self.get_delete_url()

        return context


class CommonAuthUpdateView(UserPassesTestMixin, CommonUpdateView):
    # These are for testing purposes only
    auth = True
    login_url = '/accounts/login_required/'

    # this should be overriden in an extending class to determine if a user is authorized to do certain actions
    def test_func(self):
        return self.auth

    def get_auth(self):
        return self.auth

    def get_context_data(self, **kwargs):
        # we want to update the context with the context vars added by CommonMixin classes
        context = super().get_context_data(**kwargs)
        context["auth"] = self.get_auth()
        return context


class CommonDeleteView(CommonFormMixin, DeleteView):
    template_name = 'shared_models/generic_confirm_delete.html'
    # set this to false if you do not want the delete button to be greyed out if there are related objects
    delete_protection = True
    submit_text = None

    def get_h1(self):
        if self.h1:
            return self.h1
        else:
            return gettext(
                "Are you sure you want to delete the following {}? <br>  <span class='red-font'>{}</span>".format(
                    self.model._meta.verbose_name,
                    self.get_object(),
                ))

    def get_submit_text(self):
        if self.submit_text:
            return self.submit_text
        else:
            return gettext("Delete")

    def get_related_names(self):
        """if a related_names list was provided, this will turn the simple list into a more complex list that is ready for template digestion"""
        my_list = list()
        field_map_dict = type(self.get_object())._meta.fields_map
        for field in field_map_dict:
            # some of these might be M2M fields...
            temp_related_name = field_map_dict[field].related_name

            if not temp_related_name:
                related_name = f"{field}_set"
            elif "+" not in temp_related_name:
                related_name = field_map_dict[field].related_name
            else:
                related_name = None

            if related_name:
                try:
                    my_list.append(
                        {
                            "title": getattr(type(self.get_object()),
                                             related_name).rel.related_model._meta.verbose_name_plural,
                            "qs": getattr(self.get_object(), related_name).all()
                        }
                    )
                except AttributeError:
                    pass
        return my_list

    def get_delete_protection(self):
        if not self.delete_protection:
            return False
        else:
            # the user wants delete protection to be turned on

            # go through each related field. If there is a related object, we set set a flag and exit the loop
            field_map_dict = type(self.get_object())._meta.fields_map
            for field in field_map_dict:
                temp_related_name = field_map_dict[field].related_name

                if not temp_related_name:
                    related_name = f"{field}_set"
                elif "+" not in temp_related_name:
                    related_name = field_map_dict[field].related_name
                else:
                    related_name = None

                # the second we find a related object, we are done here.
                try:
                    getattr(self.get_object(), related_name)
                except:
                    pass
                else:
                    if related_name and getattr(self.get_object(), related_name).count():
                        return True
            # if we got to this point, delete protection should be set to false, since there are no related objects
            return False

    def get_active_page_name_crumb(self):
        if self.active_page_name_crumb:
            return self.active_page_name_crumb
        else:
            return gettext("Delete Confirmation")

    def get_context_data(self, **kwargs):
        # we want to update the context with the context vars added by CommonMixin classes
        context = super().get_context_data(**kwargs)
        context.update(super().get_common_context())
        context["model_name"] = self.get_object()._meta.verbose_name
        context["related_names"] = self.get_related_names()
        context["delete_protection"] = self.get_delete_protection()
        return context


class CommonPopoutDeleteView(CommonPopoutFormMixin, CommonDeleteView):
    template_name = 'shared_models/generic_popout_confirm_delete.html'

    def get_context_data(self, **kwargs):
        # we want to update the context with the context vars added by CommonMixin classes
        context = super().get_context_data(**kwargs)
        context.update(super().get_common_context())
        context['width'] = self.width
        context['height'] = self.height
        context['submit_btn_class'] = 'btn-danger'
        return context


class CommonPopoutCreateView(CommonPopoutFormMixin, CommonCreateView):
    template_name = 'shared_models/generic_popout_form.html'

    def get_context_data(self, **kwargs):
        # we want to update the context with the context vars added by CommonMixin classes
        context = super().get_context_data(**kwargs)
        context.update(super().get_common_context())
        context['width'] = self.width
        context['height'] = self.height
        return context


class CommonPopoutUpdateView(CommonPopoutFormMixin, UpdateView):
    template_name = 'shared_models/generic_popout_form.html'

    def get_h1(self):
        if self.h1:
            return self.h1
        else:
            return gettext("Edit")

    def get_context_data(self, **kwargs):
        # we want to update the context with the context vars added by CommonMixin classes
        context = super().get_context_data(**kwargs)
        context.update(super().get_common_context())
        context['width'] = self.width
        context['height'] = self.height
        return context


class CommonFilterView(FilterView, CommonListMixin):
    # default template to use to update an update
    #  shared_entry_form.html contains the common navigation elements at the top of the template
    template_name = 'shared_models/shared_filter.html'
    extra_button_dict1 = None
    extra_button_dict2 = None

    def get_extra_button_dict1(self):
        return self.extra_button_dict1

    def get_extra_button_dict2(self):
        return self.extra_button_dict2

    def get_context_data(self, **kwargs):
        # we want to update the context with the context vars added by CommonMixin classes
        context = super().get_context_data(**kwargs)
        context.update(super().get_common_context())
        context["extra_button_dict1"] = self.get_extra_button_dict1()
        context["extra_button_dict2"] = self.get_extra_button_dict2()
        context["model_name"] = self.get_queryset().model._meta.verbose_name
        return context


class CommonAuthFilterView(UserPassesTestMixin, CommonFilterView):
    # These are for testing purposes only
    auth = True
    login_url = '/accounts/login_required/'

    # this should be overriden in an extending class to determine if a user is authorized to do certain actions
    def test_func(self):
        return self.auth

    def get_auth(self):
        return self.auth

    def get_context_data(self, **kwargs):
        # we want to update the context with the context vars added by CommonMixin classes
        context = super().get_context_data(**kwargs)
        context["auth"] = self.get_auth()
        return context


class CommonListView(ListView, CommonListMixin):
    # default template to use to update an update
    #  shared_entry_form.html contains the common navigation elements at the top of the template
    template_name = 'shared_models/generic_filter.html'

    def get_context_data(self, **kwargs):
        # we want to update the context with the context vars added by CommonMixin classes
        context = super().get_context_data(**kwargs)
        context.update(super().get_common_context())
        context["model_name"] = self.get_queryset().model._meta.verbose_name
        return context


class CommonFormView(FormView, CommonFormMixin):

    def get_context_data(self, **kwargs):
        # we want to update the context with the context vars added by CommonMixin classes
        context = super().get_context_data(**kwargs)
        context.update(super().get_common_context())
        return context


class CommonPopoutFormView(CommonPopoutFormMixin, FormView):

    def get_context_data(self, **kwargs):
        # we want to update the context with the context vars added by CommonMixin classes
        context = super().get_context_data(**kwargs)
        context.update(super().get_common_context())
        context['width'] = self.width
        context['height'] = self.height
        return context


class CommonDetailView(CommonMixin, DetailView):
    # template_name = 'shared_models/generic_detail.html'

    def get_context_data(self, **kwargs):
        # we want to update the context with the context vars added by CommonMixin classes
        context = super().get_context_data(**kwargs)
        context.update(super().get_common_context())
        return context

    def get_h1(self):
        return str(self.get_object())


class CommonPopoutDetailView(CommonPopoutMixin, CommonDetailView):
    template_name = 'shared_models/generic_popout_detail.html'


class CommonFormsetView(TemplateView, CommonFormMixin):
    queryset = None
    formset_class = None
    success_url = None
    success_url_name = None
    home_url_name = None
    delete_url_name = None
    pre_display_fields = ["id", ]
    post_display_fields = None
    random_object = None

    # override this if there are authorization requirements
    def get_queryset(self):
        return self.queryset

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        elif self.success_url_name:
            return reverse(self.success_url_name)

    def get_pre_display_fields(self):
        return self.pre_display_fields

    def get_post_display_fields(self):
        return self.post_display_fields

    def get_random_object(self):
        if self.random_object:
            return self.random_object
        else:
            return self.get_queryset().first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['random_object'] = self.get_random_object()
        context['delete_url_name'] = self.delete_url_name
        context['container_class'] = self.container_class

        context.update(super().get_common_context())
        # overwrite the existing field list to take just the fields being passed in by the formset / form
        context["field_list"] = [f for f in self.formset_class.form.base_fields]
        context["pre_display_fields"] = self.get_pre_display_fields()
        context["post_display_fields"] = self.get_post_display_fields()

        return context

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        formset = self.formset_class(queryset=queryset.all())
        return self.render_to_response(self.get_context_data(formset=formset))

    def post(self, request, *args, **kwargs):
        formset = self.formset_class(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(self.request, "Items have been successfully updated")
            return HttpResponseRedirect(self.get_success_url())
            # return self.form_valid(formset)
        else:
            return self.render_to_response(self.get_context_data(formset=formset))


class CommonHardDeleteView(View, SingleObjectMixin, ABC):
    '''a dangerous view; to use when you want to delete an object without any confirmation page; WARNING, this deletes on a GET request!!'''
    success_url = None

    def get(self, request, *args, **kwargs):
        my_obj = self.get_object()
        my_obj.delete()
        messages.error(self.request, f"{my_obj} has been successfully deleted.")

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        elif self.request.META.get('HTTP_REFERER'):
            return self.request.META.get('HTTP_REFERER')
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")


#
##
###
####
######
####################  SOME COMMON FORMS

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return in_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class SuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class IndexTemplateView(AdminRequiredMixin, CommonTemplateView):
    template_name = 'shared_models/org_index.html'
    h1 = "<span class='red-font'><span class='font-weight-bold'>{}:</span> {}</span>".format(gettext_lazy("Warning"),
                                                                                             gettext_lazy(
                                                                                                 "These are shared tables for all of DM Apps."))
    h2 = gettext_lazy("Please be careful when editing.")
    active_page_name_crumb = gettext_lazy("DM Apps Shared Settings")


# SECTION #
###########

class SectionListView(AdminRequiredMixin, CommonFilterView):
    paginate_by = 25
    filterset_class = filters.SectionFilter
    queryset = models.Section.objects.order_by("division__branch__region", "division__branch", "division", "name")
    template_name = 'shared_models/org_list.html'
    field_list = [
        {"name": "region", },
        {"name": "branch", },
        {"name": "division", },
        {"name": "tname|{}".format(gettext_lazy("section")), },
        {"name": "abbrev", },
        {"name": "head", },
        {"name": "date_last_modified", },
        {"name": "last_modified_by", },
    ]
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    home_url_name = "shared_models:index"
    row_object_url_name = "shared_models:section_edit"
    new_object_url_name = "shared_models:section_new"
    container_class = "container-fluid"
    h1 = queryset.model._meta.verbose_name_plural

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["region"] = models.Region.objects.first()
        context["branch"] = models.Branch.objects.first()
        context["division"] = models.Division.objects.first()
        context["section"] = models.Section.objects.first()
        return context


class SectionUpdateView(AdminRequiredMixin, CommonUpdateView):
    model = models.Section
    template_name = 'shared_models/org_form.html'
    form_class = forms.SectionForm
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    parent_crumb = {"title": model._meta.verbose_name_plural, "url": reverse_lazy("shared_models:section_list")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["delete_url"] = reverse("shared_models:section_delete", kwargs={"pk": self.get_object().id})
        return context

    def get_initial(self):
        return {"last_modified_by": self.request.user, }


class SectionCreateView(AdminRequiredMixin, CommonCreateView):
    model = models.Section
    template_name = 'shared_models/org_form.html'
    form_class = forms.SectionForm
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    parent_crumb = {"title": model._meta.verbose_name_plural, "url": reverse_lazy("shared_models:section_list")}

    def get_initial(self):
        return {"last_modified_by": self.request.user, }


class SectionDeleteView(AdminRequiredMixin, CommonDeleteView):
    model = models.Section
    success_url = reverse_lazy('shared_models:section_list')
    template_name = 'shared_models/generic_confirm_delete.html'
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    grandparent_crumb = {"title": model._meta.verbose_name_plural, "url": reverse_lazy("shared_models:section_list")}

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("shared_models:section_edit", kwargs={
            "pk": self.get_object().id})}


# DIVISION #
############


class DivisionListView(AdminRequiredMixin, CommonFilterView):
    paginate_by = 25
    filterset_class = filters.DivisionFilter
    queryset = models.Division.objects.order_by("branch__region", "branch", "name")
    template_name = 'shared_models/org_list.html'
    field_list = [
        {"name": "region", },
        {"name": "branch", },
        {"name": "tname|{}".format(gettext_lazy("division")), },
        {"name": "abbrev", },
        {"name": "head", },
        {"name": "date_last_modified", },
        {"name": "last_modified_by", },
    ]
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    home_url_name = "shared_models:index"
    row_object_url_name = "shared_models:division_edit"
    new_object_url_name = "shared_models:division_new"
    container_class = "container-fluid"
    h1 = queryset.model._meta.verbose_name_plural

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["region"] = models.Region.objects.first()
        context["branch"] = models.Branch.objects.first()
        context["division"] = models.Division.objects.first()
        context["section"] = models.Section.objects.first()
        return context


class DivisionUpdateView(AdminRequiredMixin, CommonUpdateView):
    model = models.Division
    template_name = 'shared_models/org_form.html'
    form_class = forms.DivisionForm
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    parent_crumb = {"title": model._meta.verbose_name_plural, "url": reverse_lazy("shared_models:division_list")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["delete_url"] = reverse("shared_models:division_delete", kwargs={"pk": self.get_object().id})
        return context

    def get_initial(self):
        return {"last_modified_by": self.request.user, }


class DivisionCreateView(AdminRequiredMixin, CommonCreateView):
    model = models.Division
    template_name = 'shared_models/org_form.html'
    form_class = forms.DivisionForm
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    parent_crumb = {"title": model._meta.verbose_name_plural, "url": reverse_lazy("shared_models:division_list")}

    def get_initial(self):
        return {"last_modified_by": self.request.user, }


class DivisionDeleteView(AdminRequiredMixin, CommonDeleteView):
    model = models.Division
    success_url = reverse_lazy('shared_models:division_list')
    template_name = 'shared_models/generic_confirm_delete.html'
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    grandparent_crumb = {"title": model._meta.verbose_name_plural, "url": reverse_lazy("shared_models:division_list")}

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("shared_models:division_edit", kwargs={
            "pk": self.get_object().id})}


# BRANCH #
##########


class BranchListView(AdminRequiredMixin, CommonFilterView):
    paginate_by = 25
    filterset_class = filters.BranchFilter
    queryset = models.Branch.objects.order_by("region", "name")
    template_name = 'shared_models/org_list.html'
    field_list = [
        {"name": "region", },
        {"name": "tname|{}".format(gettext_lazy("branch")), },
        {"name": "abbrev", },
        {"name": "head", },
        {"name": "date_last_modified", },
        {"name": "last_modified_by", },
    ]
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    home_url_name = "shared_models:index"
    row_object_url_name = "shared_models:branch_edit"
    new_object_url_name = "shared_models:branch_new"
    container_class = "container-fluid"
    h1 = queryset.model._meta.verbose_name_plural

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["region"] = models.Region.objects.first()
        context["branch"] = models.Branch.objects.first()
        context["division"] = models.Division.objects.first()
        context["section"] = models.Section.objects.first()
        return context


class BranchUpdateView(AdminRequiredMixin, CommonUpdateView):
    model = models.Branch
    template_name = 'shared_models/org_form.html'
    form_class = forms.BranchForm
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    parent_crumb = {"title": model._meta.verbose_name_plural, "url": reverse_lazy("shared_models:branch_list")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["delete_url"] = reverse("shared_models:branch_delete", kwargs={"pk": self.get_object().id})
        return context

    def get_initial(self):
        return {"last_modified_by": self.request.user, }


class BranchCreateView(AdminRequiredMixin, CommonCreateView):
    model = models.Branch
    template_name = 'shared_models/org_form.html'
    form_class = forms.BranchForm
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    parent_crumb = {"title": model._meta.verbose_name_plural, "url": reverse_lazy("shared_models:branch_list")}

    def get_initial(self):
        return {"last_modified_by": self.request.user, }


class BranchDeleteView(AdminRequiredMixin, CommonDeleteView):
    model = models.Branch
    success_url = reverse_lazy('shared_models:branch_list')
    template_name = 'shared_models/generic_confirm_delete.html'
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    grandparent_crumb = {"title": model._meta.verbose_name_plural, "url": reverse_lazy("shared_models:branch_list")}

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("shared_models:branch_edit", kwargs={
            "pk": self.get_object().id})}


# REGION #
###########

class RegionListView(AdminRequiredMixin, CommonListView):
    queryset = models.Region.objects.order_by("name")
    template_name = 'shared_models/org_list.html'
    field_list = [
        {"name": "tname|{}".format(gettext_lazy("Regions - Sectors (NCR)")), },
        {"name": "abbrev", },
        {"name": "head", },
        {"name": "date_last_modified", },
        {"name": "last_modified_by", },
    ]
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    home_url_name = "shared_models:index"
    row_object_url_name = "shared_models:region_edit"
    new_object_url_name = "shared_models:region_new"
    container_class = "container-fluid"
    h1 = queryset.model._meta.verbose_name_plural

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RegionUpdateView(AdminRequiredMixin, CommonUpdateView):
    model = models.Region
    template_name = 'shared_models/org_form.html'
    form_class = forms.RegionForm
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    parent_crumb = {"title": model._meta.verbose_name_plural, "url": reverse_lazy("shared_models:region_list")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["delete_url"] = reverse("shared_models:region_delete", kwargs={"pk": self.get_object().id})
        return context

    def get_initial(self):
        return {"last_modified_by": self.request.user, }


class RegionCreateView(AdminRequiredMixin, CommonCreateView):
    model = models.Region
    template_name = 'shared_models/org_form.html'
    form_class = forms.RegionForm
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    parent_crumb = {"title": model._meta.verbose_name_plural, "url": reverse_lazy("shared_models:region_list")}

    def get_initial(self):
        return {"last_modified_by": self.request.user, }


class RegionDeleteView(AdminRequiredMixin, CommonDeleteView):
    model = models.Region
    success_url = reverse_lazy('shared_models:region_list')
    template_name = 'shared_models/generic_confirm_delete.html'
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    grandparent_crumb = {"title": model._meta.verbose_name_plural, "url": reverse_lazy("shared_models:region_list")}

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("shared_models:region_edit", kwargs={
            "pk": self.get_object().id})}


# ORGANIZATION #
################

class OrganizationListView(AdminRequiredMixin, CommonListView):
    queryset = models.Organization.objects.order_by("name")
    template_name = 'shared_models/org_list.html'
    field_list = [
        {"name": "tname|{}".format(gettext_lazy("Organizations - Sectors (NCR)")), },
        {"name": "abbrev", },
        {"name": "address", },
        {"name": "city", },
        {"name": "postal_code", },
        {"name": "location", },
    ]
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    home_url_name = "shared_models:index"
    row_object_url_name = "shared_models:org_edit"
    new_object_url_name = "shared_models:org_new"
    container_class = "container-fluid"
    h1 = queryset.model._meta.verbose_name_plural

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OrganizationUpdateView(AdminRequiredMixin, CommonUpdateView):
    model = models.Organization
    template_name = 'shared_models/org_form.html'
    form_class = forms.OrganizationForm
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    parent_crumb = {"title": model._meta.verbose_name_plural, "url": reverse_lazy("shared_models:org_list")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["delete_url"] = reverse("shared_models:org_delete", kwargs={"pk": self.get_object().id})
        return context

    def get_initial(self):
        return {"last_modified_by": self.request.user, }


class OrganizationCreateView(AdminRequiredMixin, CommonCreateView):
    model = models.Organization
    template_name = 'shared_models/org_form.html'
    form_class = forms.OrganizationForm
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    parent_crumb = {"title": model._meta.verbose_name_plural, "url": reverse_lazy("shared_models:org_list")}

    def get_initial(self):
        return {"last_modified_by": self.request.user, }


class OrganizationDeleteView(AdminRequiredMixin, CommonDeleteView):
    model = models.Organization
    success_url = reverse_lazy('shared_models:org_list')
    template_name = 'shared_models/generic_confirm_delete.html'
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    grandparent_crumb = {"title": model._meta.verbose_name_plural, "url": reverse_lazy("shared_models:org_list")}

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("shared_models:org_edit", kwargs={
            "pk": self.get_object().id})}


# RESPONSIBILITY CENTER
########################

class ResponsibilityCenterListView(AdminRequiredMixin, CommonFilterView):
    template_name = "shared_models/org_list.html"
    filterset_class = filters.RCFilter
    model = models.ResponsibilityCenter
    field_list = [
        {"name": "name|{}".format(gettext_lazy("name")), "class": "", "width": ""},
        {"name": "code", "class": "", "width": ""},
        {"name": "manager", "class": "", "width": ""},
    ]
    new_object_url_name = "shared_models:rc_new"
    row_object_url_name = "shared_models:rc_edit"
    home_url_name = "shared_models:index"
    h1 = gettext_lazy("Responsibility Center")
    container_class = "container bg-light curvy"


class ResponsibilityCenterUpdateView(AdminRequiredMixin, CommonUpdateView):
    model = models.ResponsibilityCenter
    form_class = forms.ResponsibilityCenterForm
    home_url_name = "shared_models:index"
    parent_crumb = {"title": gettext_lazy("Responsibility Center"), "url": reverse_lazy("shared_models:rc_list")}
    template_name = "shared_models/org_form.html"
    is_multipart_form_data = True
    container_class = "container bg-light curvy"

    def get_delete_url(self):
        return reverse("shared_models:rc_delete", args=[self.get_object().id])


class ResponsibilityCenterCreateView(AdminRequiredMixin, CommonCreateView):
    model = models.ResponsibilityCenter
    form_class = forms.ResponsibilityCenterForm
    home_url_name = "shared_models:index"
    parent_crumb = {"title": gettext_lazy("Responsibility Center"), "url": reverse_lazy("shared_models:rc_list")}
    template_name = "shared_models/org_form.html"
    container_class = "container bg-light curvy"


class ResponsibilityCenterDeleteView(AdminRequiredMixin, CommonDeleteView):
    model = models.ResponsibilityCenter
    success_url = reverse_lazy('shared_models:rc_list')
    home_url_name = "shared_models:index"
    parent_crumb = {"title": gettext_lazy("Responsibility Center"), "url": reverse_lazy("shared_models:rc_list")}
    template_name = "shared_models/generic_confirm_delete.html"
    delete_protection = False
    container_class = "container bg-light curvy"


# PROJECT CODE
##############

class ProjectCodeListView(AdminRequiredMixin, CommonFilterView):
    template_name = "shared_models/org_list.html"
    filterset_class = filters.ProjectCodeFilter
    model = models.Project
    field_list = [
        {"name": "name|{}".format(gettext_lazy("name")), "class": "", "width": ""},
        {"name": "code", "class": "", "width": ""},
        {"name": "description", "class": "", "width": ""},
        {"name": "project_lead", "class": "", "width": ""},
    ]
    new_object_url_name = "shared_models:project_new"
    row_object_url_name = "shared_models:project_edit"
    home_url_name = "shared_models:index"
    h1 = gettext_lazy("Project Codes")
    container_class = "container bg-light curvy"


class ProjectCodeUpdateView(AdminRequiredMixin, CommonUpdateView):
    model = models.Project
    form_class = forms.ProjectCodeForm
    home_url_name = "shared_models:index"
    parent_crumb = {"title": gettext_lazy("Project Codes"), "url": reverse_lazy("shared_models:project_list")}
    template_name = "shared_models/org_form.html"
    is_multipart_form_data = True
    container_class = "container bg-light curvy"

    def get_delete_url(self):
        return reverse("shared_models:project_delete", args=[self.get_object().id])


class ProjectCodeCreateView(AdminRequiredMixin, CommonCreateView):
    model = models.Project
    form_class = forms.ProjectCodeForm
    home_url_name = "shared_models:index"
    parent_crumb = {"title": gettext_lazy("Project Codes"), "url": reverse_lazy("shared_models:project_list")}
    template_name = "shared_models/org_form.html"
    container_class = "container bg-light curvy"


class ProjectCodeDeleteView(AdminRequiredMixin, CommonDeleteView):
    model = models.Project
    success_url = reverse_lazy('shared_models:project_list')
    home_url_name = "shared_models:index"
    parent_crumb = {"title": gettext_lazy("Project Codes"), "url": reverse_lazy("shared_models:project_list")}
    template_name = "shared_models/generic_confirm_delete.html"
    delete_protection = False
    container_class = "container bg-light curvy"


# USER #
########

# this is a complicated cookie. Therefore we will not use a model view or model form and handle the clean data manually.
class UserCreateView(AdminRequiredMixin, CommonPopoutFormView):
    form_class = forms.UserCreateForm
    h1 = gettext_lazy("Create a New DM Apps User")
    h3 = "<span class='red-font'>{}</span> <br><br> <span class='text-muted'>{}</span> <br><br>".format(
        gettext_lazy("Please use extreme vigilance with this form."),
        gettext_lazy("After this form is submitted, the new user will receive a confirmation e-mail.") if not settings.AZURE_AD else "",
    )
    height = 850

    def form_valid(self, form):
        # retrieve data from form
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email1']

        # create a new user
        my_user = User.objects.create(
            username=email,
            first_name=first_name,
            last_name=last_name,
            password="pbkdf2_sha256$120000$ctoBiOUIJMD1$DWVtEKBlDXXHKfy/0wKCpcIDYjRrKfV/wpYMHKVrasw=",
            is_active=1,
            email=email,
        )

        # only send an email if AAD is not on
        if not settings.AZURE_AD:
            email = emails.UserCreationEmail(my_user, self.request)

            # send the email object
            custom_send_mail(
                subject=email.subject,
                html_message=email.message,
                from_email=email.from_email,
                recipient_list=email.to_list
            )
            messages.success(self.request, gettext("The user '{}' was created and an email was sent".format(my_user.get_full_name())))

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# SCRIPTS #
###########

class ScriptListView(SuperuserRequiredMixin, CommonListView):
    queryset = models.Script.objects.order_by("name")
    template_name = 'shared_models/script_list.html'
    field_list = [
        {"name": "tname|{}".format(gettext_lazy("name")), },
        {"name": "tdescription|{}".format(gettext_lazy("description")), },
        {"name": "script", },
    ]
    home_url_name = "shared_models:index"
    row_object_url_name = "shared_models:script_edit"
    new_object_url_name = "shared_models:script_new"
    container_class = "container-fluid"
    h1 = queryset.model._meta.verbose_name_plural.title()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ScriptUpdateView(SuperuserRequiredMixin, CommonUpdateView):
    model = models.Script
    template_name = 'shared_models/generic_form.html'
    form_class = forms.ScriptForm
    home_url_name = "index"
    parent_crumb = {"title": model._meta.verbose_name_plural, "url": reverse_lazy("shared_models:script_list")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["delete_url"] = reverse("shared_models:script_delete", kwargs={"pk": self.get_object().id})
        return context

    def get_initial(self):
        return {"last_modified_by": self.request.user, }


class ScriptCreateView(SuperuserRequiredMixin, CommonCreateView):
    model = models.Script
    template_name = 'shared_models/generic_form.html'
    form_class = forms.ScriptForm
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    parent_crumb = {"title": model._meta.verbose_name_plural, "url": reverse_lazy("shared_models:script_list")}
    home_url_name = "index"

    def get_initial(self):
        return {"last_modified_by": self.request.user, }


class ScriptDeleteView(SuperuserRequiredMixin, CommonDeleteView):
    model = models.Script
    success_url = reverse_lazy('shared_models:script_list')
    template_name = 'shared_models/generic_confirm_delete.html'
    root_crumb = {"title": gettext_lazy("DFO Orgs"), "url": reverse_lazy("shared_models:index")}
    grandparent_crumb = {"title": model._meta.verbose_name_plural, "url": reverse_lazy("shared_models:script_list")}
    home_url_name = "index"

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("shared_models:script_edit", kwargs={
            "pk": self.get_object().id})}


@login_required()
def run_script(request, pk):
    if request.user.is_superuser:
        script = models.Script.objects.get(pk=pk)
        try:
            mod = script.script.split(".")
            scr = mod.pop()
            mod = ".".join(mod)
            i = __import__(mod, fromlist=[''])
            getattr(i, scr)()
            messages.success(request, f"The '{script}' script has been run successfully.")

        except Exception as e:
            messages.error(request, e)
        return HttpResponseRedirect(reverse("shared_models:script_list"))


@login_required()
def export_org_report(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer = csv.writer(response)

    fields = [
        'region uuid',
        'region name',
        'region nom',
        'region head email',
        'region admin email',
        'branch uuid',
        'branch name',
        'branch nom',
        'branch head email',
        'branch admin email',
        'division uuid',
        'division name',
        'division nom',
        'division head email',
        'division admin email',
        'section uuid',
        'section name',
        'section nom',
        'section head email',
        'section admin email',
    ]
    writer.writerow(fields)

    for obj in models.Section.objects.all():
        data_row = [
            obj.division.branch.region.uuid,
            obj.division.branch.region.name,
            obj.division.branch.region.nom,
            obj.division.branch.region.head.email if obj.division.branch.region.head else None,
            obj.division.branch.region.admin.email if obj.division.branch.region.admin else None,
            obj.division.branch.uuid,
            obj.division.branch.name,
            obj.division.branch.nom,
            obj.division.branch.head.email if obj.division.branch.head else None,
            obj.division.branch.admin.email if obj.division.branch.admin else None,
            obj.division.uuid,
            obj.division.name,
            obj.division.nom,
            obj.division.head.email if obj.division.head else None,
            obj.division.admin.email if obj.division.admin else None,
            obj.uuid,
            obj.name,
            obj.nom,
            obj.head.email if obj.head else None,
            obj.admin.email if obj.admin else None,
        ]
        writer.writerow(data_row)

    # Create the HttpResponse object with the appropriate CSV header.
    response['Content-Disposition'] = f'attachment; filename="org list ({timezone.now().strftime("%Y_%m_%d")}).csv"'
    return response
