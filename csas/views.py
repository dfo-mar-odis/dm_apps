from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, TemplateView

from django.urls import reverse_lazy
from csas import models, forms, filters, utils
from django.utils.translation import gettext_lazy as _

from shared_models import views as shared_view


class FilterCommon(shared_view.CommonFilterView):
    auth = True
    template_name = 'csas/csas_filter.html'

    # override this if there are authorization requirements
    def test_func(self):
        return self.auth

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # for the most part if the user is authorized then the content is editable
        # but extending classes can choose to make content not editable even if the user is authorized
        # Default behaviour for the FilterCommon class is that users are authorized by default to view
        # Data, but not to create or modify it.
        context['auth'] = self.test_func()
        context['editable'] = context['auth']
        context.update(super().get_common_context())
        if self.request.user:
            context['auth'] = utils.csas_authorized(self.request.user)
            context['csas_admin'] = utils.csas_admin(self.request.user)
            context['csas_super'] = utils.csas_super(self.request.user)

        return context


class FilterCommonPars(shared_view.CommonFilterView):
    auth = True
    template_name = 'csas/csas_filter_pars.html'

    def test_func(self):
        return self.auth

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['auth'] = self.test_func()
        context['editable'] = context['auth']
        context.update(super().get_common_context())
        if self.request.user:
            context['auth'] = utils.csas_authorized(self.request.user)
            context['csas_admin'] = utils.csas_admin(self.request.user)
            context['csas_super'] = utils.csas_super(self.request.user)

        return context


# Extend this class to add a new list view
class CsasListCommon(FilterCommon):
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
    index_url = None

    # The height of the popup dialog used to display the creation/update form
    # if not set by the extending class the default popup height will be used
    creation_form_height = None

    # overrides the UserPassesTestMixin test to check that a user belongs to the csas_admin group
    def test_func(self):
        return utils.csas_authorized(self.request.user)

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs)

        if self.key:
            context['key'] = self.key

        context['fields'] = self.fields
        context['create_url'] = self.create_url if self.create_url else 'csas:create_{}'.format(self.key)
        context['details_url'] = self.details_url if self.details_url else 'csas:details_{}'.format(self.key)
        context['update_url'] = self.update_url if self.update_url else 'csas:update_{}'.format(self.key)
        context['index_url'] = self.index_url if self.index_url else 'csas:index_{}'.format(self.key)

        return context


class CsasListCommonPars(FilterCommonPars):
    nav_menu = 'csas/csas_nav.html'
    site_css = 'csas/csas_css.css'

    fields = []
    create_url = None
    details_url = None
    list_url = None
    update_url = None
    index_url = None
    creation_form_height = None

    def test_func(self):
        return utils.csas_authorized(self.request.user)

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs)

        if self.key:
            context['key'] = self.key

        context['fields'] = self.fields
        context['create_url'] = self.create_url if self.create_url else 'csas:create_{}'.format(self.key)
        context['details_url'] = self.details_url if self.details_url else 'csas:details_{}'.format(self.key)
        # context['details_url'] = 'csas:details_met_DFO_pars'
        context['list_url'] = self.update_url if self.update_url else 'csas:list_{}'.format(self.key)
        context['update_url'] = self.update_url if self.update_url else 'csas:update_{}'.format(self.key)
        context['index_url'] = self.index_url if self.index_url else 'csas:index_{}'.format(self.key)

        return context


# The Create Common class is a quick way to create an entry form. define a new class that extends it
# provide a title, model and form_class and away you go.
#
# Create Common uses the shared_models/shared_entry_form.html template to display common forms in a standard way
#
# class CreateCommon(UserPassesTestMixin, CreateView):
class CsasCreateCommon(shared_view.CommonCreateView):
    nav_menu = 'csas/csas_nav.html'
    site_css = 'csas/csas_css.css'
    template_name = 'csas/csas_entry_form.html'

    # overrides the UserPassesTestMixin test to check that a user belongs to the csas_admin group
    def test_func(self):
        return utils.csas_authorized(self.request.user)


# class CsasCreateCommon3col(shared_view.CommonCreateView):
#     nav_menu = 'csas/csas_nav.html'
#     site_css = 'csas/csas_css.css'
#     template_name = 'csas/csas_entry_form_3col.html'
#
#     # overrides the UserPassesTestMixin test to check that a user belongs to the csas_admin group
#     def test_func(self):
#         return utils.csas_authorized(self.request.user)


# The Update Common class is a quick way to create an entry form to edit existing objects.
# Define a new class that extends it provide a title, model and form_class and away you go.
#
# Virtually the same as the Create Common class, the Update Common class uses the _entry_form.html
# template to display common forms in a popup dialog intended to be attached to some "update" button.
#
# class UpdateCommon(UserPassesTestMixin, UpdateView):
class CsasUpdateCommon(shared_view.CommonUpdateView):
    nav_menu = 'csas/csas_nav.html'
    site_css = 'csas/csas_css.css'
    template_name = 'csas/csas_entry_form.html'

    # overrides the UserPassesTestMixin test to check that a user belongs to the csas_admin group
    def test_func(self):
        return utils.csas_authorized(self.request.user)

    def get_nav_menu(self):
        if hasattr(self, 'kwargs') and self.kwargs.get('pop'):
            return None
        return super().get_nav_menu()


class DetailsCommon(DetailView):
    # default template to use to create a details view
    template_name = 'csas/csas_details.html'

    # title to display on the list page
    title = None

    # key used for creating default list and update URLs in the get_context_data method
    key = None

    # URL linking the details page back to the proper list
    index_url = None
    list_url = None
    update_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.title:
            context['title'] = self.title

        if self.fields:
            context['fields'] = self.fields

        if self.key:
            context['key'] = self.key

        if self.request.user:
            context['auth'] = utils.csas_authorized(self.request.user)
            context['csas_admin'] = utils.csas_admin(self.request.user)
            context['csas_super'] = utils.csas_super(self.request.user)

        # If you don't provide specific list and update urls by setting list_url and/or update_url
        # in the extending class, then Common Details will use the provided key to create the url for you
        context['index_url'] = self.index_url if self.index_url else 'csas:index_{}'.format(self.key)
        context['list_url'] = self.list_url if self.list_url else 'csas:list_{}'.format(self.key)
        context['update_url'] = self.update_url if self.update_url else 'csas:update_{}'.format(self.key)

        return context


class CloserTemplateView(TemplateView):
    template_name = 'shared_models/close_me.html'


# ----------------------------------------------------------------------------------------------------
# Create index view for CSAS
#
class IndexTemplateView(TemplateView):
    template_name = 'csas/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user:
            context['auth'] = utils.csas_authorized(self.request.user)
            context['csas_admin'] = utils.csas_admin(self.request.user)
            context['csas_super'] = utils.csas_super(self.request.user)

        # Add controlled list lookups here.
        context['lookups'] = [
            {
                'title': _("Honorific"),
                'list_url': 'csas:list_coh',
                'create_url': 'csas:create_coh',
            },
            {
                'title': _("Meeting Status"),
                'list_url': 'csas:list_stt',
                'create_url': 'csas:create_stt',
            },
            {
                'title': _("Meeting Quarter"),
                'list_url': 'csas:list_meq',
                'create_url': 'csas:create_meq',
            },
            {
                'title': _("Meeting Location"),
                'list_url': 'csas:list_loc',
                'create_url': 'csas:create_loc',
            },
            {
                'title': _("Advisory Process Type"),
                'list_url': 'csas:list_apt',
                'create_url': 'csas:create_apt',
            },
            {
                'title': _("Scope"),
                'list_url': 'csas:list_scp',
                'create_url': 'csas:create_scp',
            },
        ]
        return context


# Create index view for new meeting
#
class IndexMeetingView(TemplateView):
    template_name = 'csas/index_met.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user:
            context['auth'] = utils.csas_authorized(self.request.user)
            context['csas_admin'] = utils.csas_admin(self.request.user)
            context['csas_super'] = utils.csas_super(self.request.user)

        return context


# Create index view for new publication
#
class IndexPublicationView(TemplateView):
    template_name = 'csas/index_pub.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user:
            context['auth'] = utils.csas_authorized(self.request.user)
            context['csas_admin'] = utils.csas_admin(self.request.user)
            context['csas_super'] = utils.csas_super(self.request.user)

        return context


# ----------------------------------------------------------------------------------------------------
# Create "Request" views
#
class RequestEntry(CsasCreateCommon):
    # The title to use on the Request form
    title = _('New Request Entry')
    # The model Django uses to retrieve the object(s) used on the page
    model = models.ReqRequest
    # This is what controls what fields and what widgets for what fields should be used on the entry form
    form_class = forms.RequestForm

    # Go to Request List or Request Details page after Submit a new request
    def get_success_url(self):
        return reverse_lazy('csas:details_req', args=(self.object.pk,))


class RequestEntryCSAS(CsasCreateCommon):
    title = _('New Request CSAS Entry')
    model = models.ReqRequestCSAS
    form_class = forms.RequestFormCSAS

    def get_success_url(self):
        return reverse_lazy('csas:details_req_CSAS', args=(self.object.pk,))


class RequestUpdate(CsasUpdateCommon):
    title = _('Update Request')
    model = models.ReqRequest
    form_class = forms.RequestForm

    # Go to Request Details page after Update a request
    def get_success_url(self):
        if hasattr(self, 'kwargs') and 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_req', args=(self.object.pk,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user:
            context['auth'] = utils.csas_authorized(self.request.user)
            context['csas_admin'] = utils.csas_admin(self.request.user)
            context['csas_super'] = utils.csas_super(self.request.user)

        return context


class RequestUpdateCSAS(CsasUpdateCommon):
    title = _('Update Request CSAS')
    model = models.ReqRequestCSAS
    form_class = forms.RequestFormCSAS

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_req_CSAS', args=(self.object.pk,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user:
            context['auth'] = utils.csas_authorized(self.request.user)
            context['csas_admin'] = utils.csas_admin(self.request.user)
            context['csas_super'] = utils.csas_super(self.request.user)

        return context


class RequestList(CsasListCommon):
    key = 'req'
    title = _('Request List')
    model = models.ReqRequest
    filterset_class = filters.RequestFilter
    fields = ['id', 'assigned_req_id', 'title', 'region', 'client_sector', 'client_name', 'client_email', 'funding']


class RequestListReg(CsasListCommon):
    key = 'req'
    title = _('Maritimes Region Request List')
    model = models.ReqRequest
    filterset_class = filters.RequestFilterReg
    template_name = "csas/csas_filter_regs.html"

    fields = ['id', 'assigned_req_id', 'title', 'client_sector', 'client_name', 'client_email', 'funding']


class RequestDetails(DetailsCommon):
    key = 'req'
    title = _('Request Details')
    model = models.ReqRequest
    fields = ['assigned_req_id', 'title', 'in_year_request', 'region', 'client_sector', 'client_name',
              'client_title', 'client_email', 'issue', 'priority', 'rationale', 'proposed_timing',
              'rationale_for_timing', 'funding', 'funding_notes', 'science_discussion', 'science_discussion_notes',
              'adviser_submission', 'rd_submission', 'decision_date', ]


class RequestDetailsCSAS(DetailsCommon):
    key = 'req_CSAS'
    title = _('Request Status Details')
    model = models.ReqRequestCSAS
    fields = ['request', 'status', 'trans_title', 'decision', 'decision_exp', 'decision_date', ]


# ----------------------------------------------------------------------------------------------------
# Create "Contact" forms
#
class ContactEntry(CsasCreateCommon):
    title = _('New Contact Entry')
    model = models.ConContact
    form_class = forms.ContactForm

    def get_success_url(self):
        return reverse_lazy('csas:details_con', args=(self.object.pk,))


class ContactUpdate(CsasUpdateCommon):
    title = _('Update Contact')
    model = models.ConContact
    form_class = forms.ContactForm

    def get_success_url(self):
        if "pop" in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_con', args=(self.object.pk,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user:
            context['auth'] = utils.csas_authorized(self.request.user)
            context['csas_admin'] = utils.csas_admin(self.request.user)
            context['csas_super'] = utils.csas_super(self.request.user)

        return context


class ContactList(CsasListCommon):
    key = 'con'
    title = _('Contact List')
    model = models.ConContact
    filterset_class = filters.ContactFilter
    fields = ['id', 'last_name', 'first_name', 'affiliation', 'contact_type', 'region', 'role', 'email', 'phone']


class ContactListReg(CsasListCommon):
    key = 'con'
    title = _('Maritimes Region Contact List')
    model = models.ConContact
    filterset_class = filters.ContactFilterReg
    template_name = 'csas/csas_filter_regs.html'

    fields = ['id', 'last_name', 'first_name', 'affiliation', 'contact_type', 'region', 'role', 'email', 'phone']


class ContactDetails(DetailsCommon):
    key = 'con'
    title = _('Contact Details')
    model = models.ConContact
    template_name = "csas/csas_details_con.html"

    fields = ['id', 'honorific', 'first_name', 'last_name', 'affiliation', 'job_title', 'language', 'contact_type',
              'notification_preference', 'phone', 'email', 'region', 'sector', 'role', 'expertise', 'cc_grad',
              'notes']


# ----------------------------------------------------------------------------------------------------
# Create "Meeting" forms
#
class MeetingEntry(CsasCreateCommon):
    key = 'met'
    title = _('New Meeting Details Entry')
    model = models.MetMeeting
    form_class = forms.MeetingForm

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_met', args=(self.object.pk,))
        # return reverse_lazy('csas:index_met', args='')


class MeetingEntryDocs(CsasCreateCommon):
    key = 'met_doc'
    title = _('New Meeting Documentation Entry')
    model = models.MedMeetingDocs
    form_class = forms.MeetingFormDocs

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_met_docs', args=(self.object.pk,))


class MeetingEntryDFOPars(CsasCreateCommon):
    title = _('New Meeting DFO Participants Entry')
    model = models.MetMeetingDFOPars
    form_class = forms.MeetingFormDFOPars

    def get_initial(self):
        initial = super().get_initial()

        if hasattr(self, "kwargs") and 'met_id' in self.kwargs:
            initial['meeting'] = self.kwargs['met_id']

        return initial

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_met_DFO_pars', args=(self.object.pk,))


class MeetingEntryOtherPars(CsasCreateCommon):
    title = _('New Meeting Other Participants Entry')
    model = models.MetMeetingOtherPars
    form_class = forms.MeetingFormOtherPars

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_met_other_pars', args=(self.object.pk,))


class MeetingEntryOMCosts(CsasCreateCommon):
    key = 'met_OM_costs'
    title = _('New Meeting O&M Costs Entry')
    model = models.MocMeetingOMCosts
    form_class = forms.MeetingFormOMCosts

    def get_initial(self):
        initial = super().get_initial()

        if hasattr(self, "kwargs") and 'met_id' in self.kwargs:
            initial['meeting'] = self.kwargs['met_id']

        return initial

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_met_OM_costs', args=(self.object.pk,))


class MeetingEntryMedia(CsasCreateCommon):
    key = 'met_media'
    title = _('New Meeting Media Entry')
    model = models.MemMeetingMedia
    form_class = forms.MeetingFormMedia

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_met_media', args=(self.object.pk,))


class MeetingUpdate(CsasUpdateCommon):
    key = 'met'
    title = _('Update Meeting')
    model = models.MetMeeting
    form_class = forms.MeetingForm

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_met', args=(self.object.pk,))


class MeetingUpdateDocs(CsasUpdateCommon):
    key = 'met_doc'
    title = _('Update Meeting Documentation')
    model = models.MedMeetingDocs
    form_class = forms.MeetingFormDocs

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_met_doc', args=(self.object.pk,))


class MeetingUpdateDFOPars(CsasUpdateCommon):
    title = _('Update Meeting DFO Participants')
    model = models.MetMeetingDFOPars
    form_class = forms.MeetingFormDFOPars

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_met_DFO_pars', args=(self.object.pk,))


class MeetingUpdateOtherPars(CsasUpdateCommon):
    key = 'met_other_pars'
    title = _('Update Meeting Other Participants')
    model = models.MetMeetingOtherPars
    form_class = forms.MeetingFormOtherPars

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_met_other_pars', args=(self.object.pk,))


class MeetingUpdateOMCosts(CsasUpdateCommon):
    key = 'met_OM_costs'
    title = _('Update Meeting O&M Costs')
    model = models.MocMeetingOMCosts
    form_class = forms.MeetingFormOMCosts

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_met_OM_costs', args=(self.object.pk,))


class MeetingUpdateMedia(CsasUpdateCommon):
    key = 'met_media'
    title = _('Update Meeting Media')
    model = models.MemMeetingMedia
    form_class = forms.MeetingFormMedia

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_met_media', args=(self.object.pk,))


class MeetingList(CsasListCommon):
    key = 'met'
    title = _('Meeting List')
    model = models.MetMeeting
    filterset_class = filters.MeetingFilter
    fields = ['id', 'start_date', 'title_en', 'title_fr', 'location_city', 'process_type']


class MeetingListReg(CsasListCommon):
    key = 'met'
    title = _('Maritimes Region Meeting List')
    model = models.MetMeeting
    filterset_class = filters.MeetingFilterReg
    template_name = "csas/csas_filter_regs.html"

    fields = ['id', 'start_date', 'title_en', 'title_fr', 'location_city', 'process_type']


class MeetingListDFOPars(CsasListCommonPars):
    key = 'met_DFO_pars'
    title = _('Meeting: DFO Participants List')
    model = models.MetMeetingDFOPars
    filterset_class = filters.MeetingFilterDFOPars
    fields = ['id', 'meeting', 'name', 'role', 'time', 'cost_category', 'funding_source', 'total_salary']


class MeetingListOtherPars(CsasListCommonPars):
    key = 'met_other_pars'
    title = _('Meeting: Other Participants List')
    model = models.MetMeetingOtherPars
    filterset_class = filters.MeetingFilterOtherPars
    fields = ['id', 'meeting', 'name', 'role', 'affiliation', 'invited', 'attended']


class MeetingDetails(DetailsCommon):
    key = 'met'
    title = _('Meeting Details')
    model = models.MetMeeting
    template_name = "csas/csas_details_met.html"

    fields = ['id', 'title_en', 'title_fr', 'status', 'status_notes', 'quarter', 'month', 'start_date', 'end_date',
              'range_en', 'range_fr', 'location_prov', 'location_city',
              'scope', 'process_type', 'lead_region', 'other_region', 'exp_publication', 'chair', 'csas_contact',
              'program_contact',  'chair_comments', 'description']


class MeetingDetailsDocs(DetailsCommon):
    key = 'met_doc'
    title = _('Meeting Documentation')
    model = models.MetMeeting
    template_name = "csas/csas_details_met_docs.html"
    fields = []


class MeetingDetailsDFOPars(DetailsCommon):
    key = 'met_DFO_pars'
    title = _('Meeting DFO Participants')
    model = models.MetMeetingDFOPars
    fields = ['id', 'meeting', 'name', 'role', 'time', 'cost_category', 'funding_source', 'total_salary']


class MeetingDetailsOtherPars(DetailsCommon):
    key = 'met_other_pars'
    title = _('Meeting Other Participants')
    model = models.MetMeetingOtherPars
    fields = ['id', 'meeting', 'name', 'role', 'affiliation', 'invited', 'attended']


class MeetingDetailsOMCosts(DetailsCommon):
    key = 'met_OM_costs'
    title = _('Meeting O&M Costs')
    model = models.MetMeeting
    template_name = "csas/csas_details_met_costs.html"
    fields = []


class MeetingDetailsMedia(DetailsCommon):
    key = 'met_media'
    title = _('Meeting Media')
    model = models.MetMeeting
    template_name = "csas/csas_details_met_media.html"
    fields = []


# ----------------------------------------------------------------------------------------------------
# Create "Publication" forms
#
class PublicationEntry(CsasCreateCommon):
    title = _('New Publication Details Entry')
    model = models.PubPublication
    form_class = forms.PublicationForm

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_pub', args=(self.object.pk,))


class PublicationEntryStatus(CsasCreateCommon):
    title = _('New Publication Status Entry')
    model = models.PubPublicationStatus
    form_class = forms.PublicationFormStatus

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        # return reverse_lazy('csas:details_pub_status', args=(self.object.pk,))
        return reverse_lazy('csas:details_pub_status', args=(self.object.pk,))


class PublicationEntryTransInfo(CsasCreateCommon):
    title = _('New Publication Translation Information Entry')
    model = models.PubPublicationTransInfo
    form_class = forms.PublicationFormTransInfo

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_pub_trans_info', args=(self.object.pk,))


class PublicationEntryDocLocation(CsasCreateCommon):
    title = _('New Publication Documentation Location Entry')
    model = models.PubPublicationDocLocation
    form_class = forms.PublicationFormDocLocation

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_pub_doc_location', args=(self.object.pk,))


class PublicationEntryOMCosts(CsasCreateCommon):
    title = _('New Publication O&M Costs Entry')
    model = models.PubPublicationOMCosts
    form_class = forms.PublicationFormOMCosts

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_pub_OM_costs', args=(self.object.pk,))


class PublicationEntryComResults(CsasCreateCommon):
    title = _('New Publication Communication of Results Entry')
    model = models.PubPublicationComResults
    form_class = forms.PublicationFormComResults

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_pub_com_results', args=(self.object.pk,))


class PublicationUpdate(CsasUpdateCommon):
    title = _('Update Publication')
    model = models.PubPublication
    form_class = forms.PublicationForm

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_pub', args=(self.object.pk,))


class PublicationUpdateStatus(CsasUpdateCommon):
    title = _('Update Publication Status')
    model = models.PubPublicationStatus
    form_class = forms.PublicationFormStatus

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_pub_status', args=(self.object.pk,))


class PublicationUpdateTransInfo(CsasUpdateCommon):
    title = _('Update Publication Translation Information')
    model = models.PubPublicationTransInfo
    form_class = forms.PublicationFormTransInfo

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_pub_trans_info', args=(self.object.pk,))


class PublicationUpdateDocLocation(CsasUpdateCommon):
    title = _('Update Publication Documentation Location')
    model = models.PubPublicationDocLocation
    form_class = forms.PublicationFormDocLocation

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_pub_doc_location', args=(self.object.pk,))


class PublicationUpdateOMCosts(CsasUpdateCommon):
    title = _('Update Publication O&M Costs')
    model = models.PubPublicationOMCosts
    form_class = forms.PublicationFormOMCosts

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_pub_OM_costs', args=(self.object.pk,))


class PublicationUpdateComResults(CsasUpdateCommon):
    title = _('Update Publication Communication of Results')
    model = models.PubPublicationComResults
    form_class = forms.PublicationFormComResults

    def get_success_url(self):
        if 'pop' in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return reverse_lazy('csas:details_pub_com_results', args=(self.object.pk,))


class PublicationList(CsasListCommon):
    key = 'pub'
    title = _('Publication List')
    model = models.PubPublication
    filterset_class = filters.PublicationFilter

    fields = ['id', 'series', 'title_en', 'lead_region', 'lead_author', 'other_author', 'pub_year']


class PublicationListReg(CsasListCommon):
    key = 'pub'
    title = _('Maritimes Region Publication List')
    model = models.PubPublication
    filterset_class = filters.PublicationFilterReg
    template_name = "csas/csas_filter_regs.html"

    fields = ['id', 'series', 'title_en', 'lead_region', 'lead_author', 'other_author', 'pub_year']


class PublicationDetails(DetailsCommon):
    key = 'pub'
    title = _('Publication Details')
    model = models.PubPublication
    template_name = "csas/csas_details_pub.html"

    fields = ['id', 'series', 'lead_region', 'title_en', 'title_fr',  'title_in', 'pub_year',
              'lead_author', 'other_author', 'pub_num', 'pages', 'keywords', 'citation', 'client',
              'description']


class PublicationDetailsStatus(DetailsCommon):
    key = 'pub_status'
    title = _('Publication Status')
    model = models.PubPublicationStatus

    fields = ['publication', 'date_due', 'status', 'status_comments', 'data_submitted', 'submitted_by',
              'date_appr_by_chair', 'appr_by_chair', 'data_appr_by_CSAS', 'appr_by_CSAS', 'date_appr_by_dir',
              'appr_by_dir', 'date_num_req', 'date_doc_submitted', 'date_pdf_proof', 'appr_by', 'date_anti',
              'date_pasted', 'date_modify', 'notes']


class PublicationDetailsTransInfo(DetailsCommon):
    key = 'pub_trans_info'
    title = _('Publication Translation Info.')
    model = models.PubPublicationTransInfo

    fields = ['publication', 'trans_status', 'date_to_trans', 'client_ref_num', 'target_lang',  'trans_ref_num',
              'urgent_req', 'date_fr_trans', 'invoice_num', 'attach', 'trans_note']


class PublicationDetailsDocLocation(DetailsCommon):
    key = 'pub_doc_location'
    title = _('Publication Doc. Location')
    model = models.PubPublicationDocLocation

    fields = ['publication', 'attach_en_file', 'attach_en_size', 'attach_fr_file', 'attach_fr_size',
              'url_e', 'url_f', 'dev_link_e', 'dev_link_f', 'lib_cat_e', 'lib_cat_f', 'lib_link_e', 'lib_link_f']


class PublicationDetailsOMCosts(DetailsCommon):
    key = 'pub_OM_costs'
    title = _('Publication O&M Costs')
    model = models.PubPublicationOMCosts

    fields = ['Publication', 'category', 'trans_funding', 'trans_code', 'trans_estimate', 'trans_cost']


class PublicationDetailsComResults(DetailsCommon):
    key = 'pub_com_results'
    title = _('Publication Com. of Results')
    model = models.PubPublication
    template_name = "csas/csas_details_pub_com_results.html"
    fields = []


# ----------------------------------------------------------------------------------------------------
# Controlled Lookup model views
# ----------------------------------------------------------------------------------------------------

class CommonCsasAuthLookup(UserPassesTestMixin):
    login_url = '/accounts/login_required/'

    def test_func(self):
        return utils.csas_super(self.request.user)

    def get_success_url(self):
        if "pop" in self.kwargs:
            return reverse_lazy('shared_models:close_me')
        return super().get_success_url()


class CsasLookupList(CommonCsasAuthLookup, CsasListCommon):

    fields = ['id', 'name', 'nom']

    def get_context_data(self, *args, object_list=None, **kwargs):

        context = super().get_context_data(*args, object_list, **kwargs)
        context['pop'] = True

        context['details_url'] = None

        if self.key:
            if self.key == 'coh':
                context['update_url'] = 'csas:update_coh'
                context['create_url'] = 'csas:create_coh'

        return context


class CohMixin:
    key = 'coh'
    model = models.CohHonorific
    title = _("Honorific")
    fields = ['name', 'nom', 'description_en', 'description_fr']
    success_url = reverse_lazy("csas:list_coh")


class CohList(CohMixin, CsasLookupList):
    pass


class UpdateCohView(CommonCsasAuthLookup, CohMixin, CsasUpdateCommon):
    pass


class CreateCohView(CommonCsasAuthLookup, CohMixin, CsasCreateCommon):
    pass


class SttMixin:
    key = 'stt'
    model = models.SttStatus
    title = _("Meeting Status")
    fields = ['name', 'nom', 'description_en', 'description_fr']
    success_url = reverse_lazy("csas:list_stt")


class SttList(SttMixin, CsasLookupList):
    pass


class UpdateSttView(CommonCsasAuthLookup, SttMixin, CsasUpdateCommon):
    pass


class CreateSttView(CommonCsasAuthLookup, SttMixin, CsasCreateCommon):
    pass


class MeqMixin:
    key = 'meq'
    model = models.MeqQuarter
    title = _("Meeting Quarter")
    fields = ['name', 'nom', 'description_en', 'description_fr']
    success_url = reverse_lazy("csas:list_meq")


class MeqList(MeqMixin, CsasLookupList):
    pass


class UpdateMeqView(CommonCsasAuthLookup, MeqMixin, CsasUpdateCommon):
    pass


class CreateMeqView(CommonCsasAuthLookup, MeqMixin, CsasCreateCommon):
    pass


class LocMixin:
    key = 'loc'
    model = models.LocLocationProv
    title = _("Meeting Location Province")
    fields = ['name', 'nom', 'description_en', 'description_fr']
    success_url = reverse_lazy("csas:list_loc")


class LocList(LocMixin, CsasLookupList):
    pass


class UpdateLocView(CommonCsasAuthLookup, LocMixin, CsasUpdateCommon):
    pass


class CreateLocView(CommonCsasAuthLookup, LocMixin, CsasCreateCommon):
    pass


class AptMixin:
    key = 'apt'
    model = models.AptAdvisoryProcessType
    title = _("Advisory Process Type")
    fields = ['name', 'nom', 'description_en', 'description_fr']
    success_url = reverse_lazy("csas:list_apt")


class AptList(AptMixin, CsasLookupList):
    pass


class UpdateAptView(CommonCsasAuthLookup, AptMixin, CsasUpdateCommon):
    pass


class CreateAptView(CommonCsasAuthLookup, AptMixin, CsasCreateCommon):
    pass


class ScpMixin:
    key = 'scp'
    model = models.ScpScope
    title = _("Scope")
    fields = ['name', 'nom', 'description_en', 'description_fr']
    success_url = reverse_lazy("csas:list_scp")


class ScpList(ScpMixin, CsasLookupList):
    pass


class UpdateScpView(CommonCsasAuthLookup, ScpMixin, CsasUpdateCommon):
    pass


class CreateScpView(CommonCsasAuthLookup, ScpMixin, CsasCreateCommon):
    pass
# ----------------------------------------------------------------------------------------------------


class CommonLookup(CreateView):
    template_name = 'csas/_lookup_entry_form.html'
    fields = ['name']
    success_url = reverse_lazy('csas:close_me')


class HonorificView(CsasCreateCommon):
    model = models.CohHonorific


class LanguageView(CommonLookup):
    model = models.LanLanguage

# End of views.py
# ----------------------------------------------------------------------------------------------------
# 1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
