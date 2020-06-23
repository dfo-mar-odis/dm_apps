from django.shortcuts import render

from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView, TemplateView, FormView
from django_filters.views import FilterView

from django.urls import reverse_lazy
from csas import models, forms, filters, utils
from django.utils.translation import gettext_lazy as _

from shared_models import views as shared_view


# Extend this class to add a new list view
# class CsasListCommon(shared_view.CommonAuthFilterView):
class CsasListCommon(shared_view.CommonAuthFilterView):

    template_name = 'csas/csas_filter.html'

    nav_menu = 'csas/csas_nav.html'
    site_css = 'csas/csas_css.css'

    # fields to be used as columns to display an object in the filter view table
    fields = []

    # URL to use to create a new object to be added to the filter view
    create_url = None

    # URL to use for the details button element in the filter view's list
    details_url = None

    # URL to use for the update button element in the filter view's list
    update_url = None

    # The height of the popup dialog used to display the creation/update form
    # if not set by the extending class the default popup height will be used
    creation_form_height = None

    # overrides the UserPassesTestMixin test to check that a user belongs to the csas_admin group
    def test_func(self):
        return utils.csas_authorized(self.request.user)

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs)

        context['fields'] = self.fields

        context['create_url'] = self.create_url if self.create_url else "csas:create_{}".format(self.key)
        context['details_url'] = self.details_url if self.details_url else "csas:details_{}".format(self.key)
        context['update_url'] = self.update_url if self.update_url else "csas:update_{}".format(self.key)

        return context


# The Create Common class is a quick way to create an entry form. define a new class that extends it
# provide a title, model and form_class and away you go.
#
# Create Common uses the shared_models/shared_entry_form.html template to display common forms in a standard way
#
# class CommonCreateView(UserPassesTestMixin, CreateView):
class CsasCommonCreateView(shared_view.CommonAuthCreateView):

    nav_menu = 'csas/csas_nav.html'
    site_css = 'csas/csas_css.css'

    template_name = 'csas/csas_entry_form.html'

    # overrides the UserPassesTestMixin test to check that a user belongs to the csas_admin group
    def test_func(self):
        return utils.csas_authorized(self.request.user)


# The Update Common class is a quick way to create an entry form to edit existing objects.
# Define a new class that extends it provide a title, model and form_class and away you go.
#
# Virtually the same as the Create Common class, the Update Common class uses the _entry_form.html
# template to display common forms in a popup dialog intended to be attached to some "update" button.
#
# class CommonUpdateView(UserPassesTestMixin, UpdateView):
class CsasCommonUpdateView(shared_view.CommonAuthUpdateView):

    nav_menu = 'csas/csas_nav.html'
    site_css = 'csas/csas_css.css'

    template_name = 'csas/csas_entry_form.html'

    # overrides the UserPassesTestMixin test to check that a user belongs to the csas_admin group
    def test_func(self):
        return utils.csas_authorized(self.request.user)

    def get_nav_menu(self):
        if hasattr(self, 'kwargs') and self.kwargs.get("pop"):
            return None

        return super().get_nav_menu()


class DetailsCommon(DetailView):
    # default template to use to create a details view
    template_name = "csas/csas_details.html"

    # title to display on the list page
    title = None

    # key used for creating default list and update URLs in the get_context_data method
    key = None

    # URL linking the details page back to the proper list
    list_url = None
    update_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.title:
            context['title'] = self.title

        if self.fields:
            context['fields'] = self.fields

        # If you don't provide specific list and update urls by setting list_url and/or update_url
        # in the extending class, then Common Details will use the provided key to create the url for you
        context['list_url'] = self.list_url if self.list_url else "csas:list_{}".format(self.key)
        context['update_url'] = self.update_url if self.update_url else "csas:update_{}".format(self.key)

        return context


class CloserTemplateView(TemplateView):
    template_name = "shared_models/close_me.html"


# Create your views here.
class IndexTemplateView(TemplateView):
    template_name = 'csas/index.html'

    # overrides the UserPassesTestMixin test to check that a user belongs to the csas_admin group

    # Hu (April 21): the following part is the only difference from Patrick's and it doesn't work, why?
    #
    # def test_func(self):
    #     return utils.csas_authorized(self.request.user)
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user:
            context["auth"] = utils.csas_authorized(self.request.user)
            context["csas_admin"] = utils.csas_admin(self.request.user)

        return context


# ----------------------------------------------------------------------------------------------------
# Create "Request" forms
#
class RequestEntry(CsasCommonCreateView):

    # The title to use on the Creation form
    title = _("New Request Entry")
    # The model Django uses to retrieve the object(s) used on the page
    model = models.ReqRequest
    # This is what controls what fields and what widgets for what fields should be used on the entry form
    form_class = forms.RequestForm

    # Go to Request List or Request Details page after Submit a new request
    def get_success_url(self):
        # return reverse_lazy("csas:list_req")
        return reverse_lazy("csas:details_req", args=(self.object.pk,))


class RequestUpdate(CsasCommonUpdateView):

    # The title to use on the Update form
    title = _("Update Request")
    # The model Django uses to retrieve the object(s) used on the page
    model = models.ReqRequest
    # This is what controls what fields and what widgets for what fields should be used on the entry form
    form_class = forms.RequestForm

    # Go to Request Details page after Update a request
    def get_success_url(self):
        if hasattr(self, 'kwargs') and "pop" in self.kwargs:
            return reverse_lazy("shared_models:close_me")
        return reverse_lazy("csas:details_req", args=(self.object.pk,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user:
            context["auth"] = utils.csas_authorized(self.request.user)
            context["csas_admin"] = utils.csas_admin(self.request.user)

        return context


class RequestList(CsasListCommon):

    # key used to create default urls. Without it you'll need to specify a create_url, details_url and update_url
    key = 'req'
    # title to display on the Filter page
    title = _("Request List")
    # The model Django uses to retrieve the object(s) used on the page
    model = models.ReqRequest
    # filter class used to filter the table. This is where you make changes to specify what fields to filter
    # on and how those fields should be laid out or work, like inclusive vs. partial text searching
    filterset_class = filters.RequestFilter
    # fields used in the table on the filter (list) page.
    fields = ['req_id', 'title', 'region', 'client_sector', 'client_name', 'funding']


class RequestDetails(DetailsCommon):

    # key used to create default urls. Without it you'll need to specify a list_url and update_url
    key = "req"
    # title to be displayed on the details page
    title = _("Request Details")
    # model Django uses to get the object being displayed on the details page
    model = models.ReqRequest
    # fields to be displayed on the details page
    fields = ['assigned_req_id', 'title', 'in_year_request', 'region', 'client_sector', 'client_name',
              'client_title', 'client_email', 'issue', 'priority', 'rationale', 'proposed_timing',
              'rationale_for_timing', 'funding', 'funding_notes', 'science_discussion', 'science_discussion_notes',
              'adviser_submission', 'rd_submission', 'decision_date', ]


# ----------------------------------------------------------------------------------------------------
# Create "Contact" forms
#
class ContactEntry(CsasCommonCreateView):

    # The title to use on the Creation form
    title = _("New Contact Entry")
    # The model Django uses to retrieve the object(s) used on the page
    model = models.ConContact
    # This is what controls what fields and what widgets for what fields should be used on the entry form
    form_class = forms.ContactForm

    # Go to Contact List or Contact Details page after Submit a new contact
    def get_success_url(self):
        # return reverse_lazy("csas:list_con")
        return reverse_lazy("csas:details_con", args=(self.object.pk,))


class ContactUpdate(CsasCommonUpdateView):

    # The title to use on the Update form
    title = _("Update Contact")
    # The model Django uses to retrieve the object(s) used on the page
    model = models.ConContact
    # This is what controls what fields and what widgets for what fields should be used on the entry form
    form_class = forms.ContactForm

    # Go to Contact Details page after Update a contact
    def get_success_url(self):
        if "pop" in self.kwargs:
            return reverse_lazy("shared_models:close_me")
        return reverse_lazy("csas:details_con", args=(self.object.pk,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user:
            context["auth"] = utils.csas_authorized(self.request.user)
            context["csas_admin"] = utils.csas_admin(self.request.user)

        return context


class ContactList(CsasListCommon):

    # key used to create default urls. Without it you'll need to specify a create_url, details_url and update_url
    key = 'con'
    # title to display on the Filter page
    title = _("Contact List")
    # The model Django uses to retrieve the object(s) used on the page
    model = models.ConContact
    # filter class used to filter the table. This is where you make changes to specify what fields to filter
    # on and how those fields should be laid out or work, like inclusive vs. partial text searching
    filterset_class = filters.ContactFilter
    # fields used in the table on the filter (list) page.
    fields = ['con_id', 'last_name', 'first_name', 'affiliation', 'contact_type', 'region', 'email', 'phone']


class ContactDetails(DetailsCommon):

    # key used to create default urls. Without it you'll need to specify a list_url and update_url
    key = "con"
    # title to be displayed on the details page
    title = _("Contact Details")
    # model Django uses to get the object being displayed on the details page
    model = models.ConContact
    # fields to be displayed on the details page
    fields = ['honorific', 'first_name', 'last_name', 'affiliation', 'job_title', 'language', 'contact_type',
              'notification_preference', 'phone', 'email', 'region', 'sector', 'role', 'expertise', 'cc_grad',
              'notes']


# ----------------------------------------------------------------------------------------------------
# Create "Meeting" forms
#
class MeetingEntry(CsasCommonCreateView):

    # The title to use on the Creation form
    title = _("New Meeting Entry")
    # The model Django uses to retrieve the object(s) used on the page
    model = models.MetMeeting
    # This is what controls what fields and what widgets for what fields should be used on the entry form
    form_class = forms.MeetingForm

    # Go to Meeting List or Meeting Details page after Submit a new meeting
    def get_success_url(self):
        # return reverse_lazy("csas:list_met")
        return reverse_lazy("csas:details_met", args=(self.object.pk,))


class MeetingUpdate(CsasCommonUpdateView):

    # The title to use on the Update form
    title = _("Update Meeting")
    # The model Django uses to retrieve the object(s) used on the page
    model = models.MetMeeting
    # This is what controls what fields and what widgets for what fields should be used on the entry form
    form_class = forms.MeetingForm

    # Go to Meeting Details page after Update a meeting
    def get_success_url(self):
        if "pop" in self.kwargs:
            return reverse_lazy("shared_models:close_me")
        return reverse_lazy("csas:details_met", args=(self.object.pk,))


class MeetingList(CsasListCommon):

    # key used to create default urls. Without it you'll need to specify a create_url, details_url and update_url
    key = 'met'
    # title to display on the Filter page
    title = _("Meeting List")
    # The model Django uses to retrieve the object(s) used on the page
    model = models.MetMeeting
    # filter class used to filter the table. This is where you make changes to specify what fields to filter
    # on and how those fields should be laid out or work, like inclusive vs. partial text searching
    filterset_class = filters.MeetingFilter
    # fields used in the table on the filter (list) page.
    fields = ['met_id', 'start_date', 'title_en', 'title_fr', 'location', 'process_type']


class MeetingDetails(DetailsCommon):

    # key used to create default urls. Without it you'll need to specify a list_url and update_url
    key = "met"
    # title to be displayed on the details page
    title = _("Meeting Details")
    # model Django uses to get the object being displayed on the details page
    model = models.MetMeeting
    # fields to be displayed on the details page
    fields = ['start_date', 'end_date', 'title_en', 'title_fr', 'scope', 'status', 'chair_comments',
              'status_notes', 'location', 'lead_region', 'other_region', 'process_type', 'program_contact',
              'csas_contact', ]


# ----------------------------------------------------------------------------------------------------
# Create "Meeting" forms
#
class PublicationEntry(CsasCommonCreateView):

    # The title to use on the Creation form
    title = _("New Publication Entry")
    # The model Django uses to retrieve the object(s) used on the page
    model = models.PubPublication
    # This is what controls what fields and what widgets for what fields should be used on the entry form
    form_class = forms.PublicationForm

    # Go to Publication List or Publication Details page after Submit a new publication
    def get_success_url(self):
        # return reverse_lazy("csas:list_pub")
        return reverse_lazy("csas:details_pub", args=(self.object.pk,))


class PublicationUpdate(CsasCommonUpdateView):

    # The title to use on the Update form
    title = _("Update Publication")
    # The model Django uses to retrieve the object(s) used on the page
    model = models.PubPublication
    # This is what controls what fields and what widgets for what fields should be used on the entry form
    form_class = forms.PublicationForm

    # Go to Publication Details page after Update a publication
    def get_success_url(self):
        if "pop" in self.kwargs:
            return reverse_lazy("shared_models:close_me")
        return reverse_lazy("csas:details_pub", args=(self.object.pk,))


class PublicationList(CsasListCommon):

    # key used to create default urls. Without it you'll need to specify a create_url, details_url and update_url
    key = 'pub'
    # title to display on the Filter page
    title = _("Publication List")
    # The model Django uses to retrieve the object(s) used on the page
    model = models.PubPublication
    # filter class used to filter the table. This is where you make changes to specify what fields to filter
    # on and how those fields should be laid out or work, like inclusive vs. partial text searching
    filterset_class = filters.PublicationFilter
    # fields used in the table on the filter (list) page.
    fields = ['pub_id', 'series', 'scope', 'lead_region', 'lead_author', 'pub_year']


class PublicationDetails(DetailsCommon):

    # key used to create default urls. Without it you'll need to specify a list_url and update_url
    key = "pub"
    # title to be displayed on the details page
    title = _("Publication Details")
    # model Django uses to get the object being displayed on the details page
    model = models.PubPublication
    # fields to be displayed on the details page
    fields = ['pub_id', 'series', 'scope', 'lead_region', 'lead_author', 'pub_year', 'pub_num', 'pages',
              'citation', 'location']


# ----------------------------------------------------------------------------------------------------


class CommonLookup(CreateView):

    template_name = 'csas/_lookup_entry_form.html'
    fields = ['name']
    success_url = reverse_lazy("csas:close_me")


class HonorificView(CommonLookup):

    model = models.CohHonorific


class LanguageView(CommonLookup):

    model = models.LanLanguage

# End of views.py
# ----------------------------------------------------------------------------------------------------
# 1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
