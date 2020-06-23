from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.conf import settings

from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.utils.translation import gettext_lazy as _

from whalesdb import forms, models, filters, utils
from shared_models.views import CommonAuthCreateView, CommonAuthUpdateView, CommonAuthFilterView

import json


def rst_delete(request, pk):
    rst = models.RstRecordingStage.objects.get(pk=pk)
    if utils.whales_authorized(request.user):
        rst.delete()
        messages.success(request, _("The recording stage has been successfully deleted."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(reverse_lazy('accounts:denied_access'))


class IndexView(TemplateView):
    template_name = 'whalesdb/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()

        # for the most part if the user is authorized then the content is editable
        # but extending classes can choose to make content not editable even if the user is authorized
        context['auth'] = context['editable'] = utils.whales_authorized(self.request.user)

        return context


# CommonCreate Extends the UserPassesTestMixin used to determine if a user has
# has the correct privileges to interact with Creation Views
class CommonCreate(CommonAuthCreateView):

    nav_menu = 'whalesdb/whale_nav_menu.html'
    site_css = 'whalesdb/whales_css.css'
    home_url_name = "whalesdb:index"

    def get_nav_menu(self):
        if self.kwargs.get("pop"):
            return None

        return self.nav_menu

    # Upon success most creation views will be redirected to their respective 'CommonList' view. To send
    # a successful creation view somewhere else, override this method
    def get_success_url(self):
        success_url = self.success_url if self.success_url else reverse_lazy("whalesdb:list_{}".format(self.key))

        if self.kwargs.get("pop"):
            # create views intended to be pop out windows should close the window upon success
            success_url = reverse_lazy("shared_models:close_me_no_refresh")

        return success_url

    # overrides the UserPassesTestMixin test to check that a user belongs to the whalesdb_admin group
    def test_func(self):
        return self.request.user.groups.filter(name='whalesdb_admin').exists()

    # Get context returns elements used on the page. Make sure when extending to call
    # context = super().get_context_data(**kwargs) so that elements created in the parent
    # class are inherited by the extending class.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editable'] = context['auth']
        return context


class DepCreate(CommonCreate):
    key = 'dep'
    model = models.DepDeployment
    form_class = forms.DepForm
    title = _("Create Deployment")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        station_dict = [{"pk": v[0], "stn_code": v[2]} for v in
                        models.StnStation.objects.all().order_by('pk').values_list()]

        context['station_json'] = json.dumps(station_dict)
        context['java_script'] = 'whalesdb/_entry_dep_js.html'

        return context


class EdaCreate(CommonCreate):
    key = 'eda'
    model = models.EdaEquipmentAttachment
    form_class = forms.EdaForm
    title = _("Select Equipment")

    def get_initial(self):
        initial = super().get_initial()
        initial['dep'] = self.kwargs['dep']

        return initial


class EmmCreate(CommonCreate):
    key = 'emm'
    model = models.EmmMakeModel
    form_class = forms.EmmForm
    title = _("Create Make/Model")

    def form_valid(self, form):
        emm = form.save()

        if emm.eqt.pk == 4:
            return HttpResponseRedirect(reverse_lazy('whalesdb:details_emm', args=(emm.pk,)))
        else:
            return HttpResponseRedirect(self.get_success_url())


class EqhCreate(CommonCreate):
    key = 'eqh'
    model = models.EqhHydrophoneProperty
    form_class = forms.EqhForm
    title = _("Hydrophone Properties")

    def get_initial(self):
        initial = super().get_initial()
        initial['emm'] = self.kwargs['pk']

        return initial


class EqoCreate(CommonCreate):
    key = 'eqo'
    model = models.EqoOwner
    form_class = forms.EqoForm
    title = _("Create Equipment Owner")


class EqpCreate(CommonCreate):
    # This key is used by CommonCreate to create the 'whalesdb:list_eqp' name in the get_success_url method
    key = 'eqp'

    # The model this class uses
    model = models.EqpEquipment

    # The form class this model uses
    form_class = forms.EqpForm

    # the title to use on this views creation template
    title = _("Create Equipment")


class EqrCreate(CommonCreate):
    key = 'eqr'
    model = models.EqrRecorderProperties
    form_class = forms.EqrForm
    title = _("Recorder Properties")

    def get_initial(self):
        initial = super().get_initial()
        initial['emm'] = self.kwargs['pk']

        return initial


class MorCreate(CommonCreate):
    key = 'mor'
    model = models.MorMooringSetup
    form_class = forms.MorForm
    title = _("Create Mooring Setup")


class PrjCreate(CommonCreate):
    key = 'prj'
    model = models.PrjProject
    form_class = forms.PrjForm
    title = _("Create Project")


class RciCreate(CommonCreate):
    key = 'rci'
    model = models.RciChannelInfo
    form_class = forms.RciForm
    title = _("Channel Information")

    def get_initial(self):
        init = super().get_initial()
        if 'rec_id' in self.kwargs and models.RecDataset.objects.filter(pk=self.kwargs['rec_id']):
            init['rec_id'] = models.RecDataset.objects.get(pk=self.kwargs['rec_id'])

        return init


class RecCreate(CommonCreate):
    key = 'rec'
    model = models.RecDataset
    form_class = forms.RecForm
    title = _("Dataset")


class ReeCreate(CommonCreate):
    key = 'ree'
    model = models.ReeRecordingEvent
    form_class = forms.ReeForm
    title = _("Recording Events")

    def get_initial(self):
        init = super().get_initial()
        if 'rec_id' in self.kwargs and models.RecDataset.objects.filter(pk=self.kwargs['rec_id']):
            init['rec_id'] = models.RecDataset.objects.get(pk=self.kwargs['rec_id'])

        return init


class RscCreate(CommonCreate):
    key = 'rsc'
    model = models.RscRecordingSchedule
    form_class = forms.RscForm
    title = _("Create Recording Schedule")

    def form_valid(self, form):
        obj = form.save()

        return HttpResponseRedirect(reverse_lazy("whalesdb:details_rsc", kwargs={"pk": obj.pk}))


class RstCreate(CommonCreate):
    key = 'rst'
    model = models.RstRecordingStage
    form_class = forms.RstForm
    title = _("Create Recording Stage")

    def get_initial(self):
        initial = super().get_initial()
        initial['rsc'] = self.kwargs['rsc']

        return initial


class RttCreate(CommonCreate):
    key = 'rtt'
    model = models.RttTimezoneCode
    form_class = forms.RttForm
    title = _("Time Zone")


class SteCreate(CommonCreate):
    key = 'ste'
    model = models.SteStationEvent
    form_class = forms.SteForm
    title = _("Create Station Event")

    def get_initial(self):
        init = super().get_initial()
        if 'dep_id' in self.kwargs and models.DepDeployment.objects.filter(pk=self.kwargs['dep_id']):
            init['dep'] = models.DepDeployment.objects.get(pk=self.kwargs['dep_id'])

        if 'set_id' in self.kwargs and models.SetStationEventCode.objects.filter(pk=self.kwargs['set_id']):
            init['set_type'] = models.SetStationEventCode.objects.get(pk=self.kwargs['set_id'])
        return init


class StnCreate(CommonCreate):
    key = 'stn'
    model = models.StnStation
    form_class = forms.StnForm
    title = _("Create Station")


class TeaCreate(CommonCreate):
    key = 'tea'
    model = models.TeaTeamMember
    form_class = forms.TeaForm
    title = _("Create Team Member")


class CommonUpdate(CommonAuthUpdateView):

    nav_menu = 'whalesdb/whale_nav_menu.html'
    site_css = 'whalesdb/whales_css.css'
    home_url_name = "whalesdb:index"

    # update views are all intended to be pop out windows so upon success close the window
    success_url = reverse_lazy("shared_models:close_me_no_refresh")

    def get_nav_menu(self):
        if self.kwargs.get("pop"):
            return None

        return self.nav_menu

    # this function overrides UserPassesTestMixin.test_func() to determine if
    # the user should have access to this content, if the user is logged in
    # This function could be overridden in extending classes to preform further testing to see if
    # an object is editable
    def test_func(self):
        return self.request.user.groups.filter(name='whalesdb_admin').exists()

    # Get context returns elements used on the page. Make sure when extending to call
    # context = super().get_context_data(**kwargs) so that elements created in the parent
    # class are inherited by the extending class.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editable'] = context['auth']
        return context


class DepUpdate(CommonUpdate):
    model = models.DepDeployment
    form_class = forms.DepForm
    title = _("Update Deployment")

    def test_func(self):
        auth = super().test_func()
        if auth:
            # editable if the object has no station events
            auth = self.model.objects.get(pk=self.kwargs['pk']).station_events.count() <= 0

        return auth

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        station_dict = [{"stn_id": v[0], "stn_code": v[2]} for v in
                        models.StnStation.objects.all().order_by('pk').values_list()]

        context['station_json'] = json.dumps(station_dict)
        context['java_script'] = 'whalesdb/_entry_dep_js.html'

        return context

    def get_success_url(self):
        return reverse_lazy("whalesdb:list_dep")


class EmmUpdate(CommonUpdate):
    model = models.EmmMakeModel
    form_class = forms.EmmForm
    title = _("Update Make/Model")

    def get_success_url(self):
        return reverse_lazy("whalesdb:list_emm")


class EqhUpdate(CommonUpdate):
    model = models.EqhHydrophoneProperty
    form_class = forms.EqhForm
    title = _("Hydrophone Properties")


class EqpUpdate(CommonUpdate):
    model = models.EqpEquipment
    form_class = forms.EqpForm
    title = _("Update Equipment")

    def get_success_url(self):
        return reverse_lazy("whalesdb:list_eqp")


class EqrUpdate(CommonUpdate):
    model = models.EqrRecorderProperties
    form_class = forms.EqrForm
    title = _("Recorder Properties")


class MorUpdate(CommonUpdate):
    model = models.MorMooringSetup
    form_class = forms.MorForm
    title = _("Update Mooring Setup")

    def get_success_url(self):
        return reverse_lazy("whalesdb:list_mor")


class PrjUpdate(CommonUpdate):
    model = models.PrjProject
    form_class = forms.PrjForm
    title = _("Update Project")

    def get_success_url(self):
        return reverse_lazy("whalesdb:list_prj")


class RecUpdate(CommonUpdate):
    model = models.RecDataset
    form_class = forms.RecForm
    title = _("Update Dataset")

    def get_success_url(self):
        return reverse_lazy("whalesdb:details_rec", args=(self.kwargs['pk'],))


class StnUpdate(CommonUpdate):
    model = models.StnStation
    form_class = forms.StnForm
    title = _("Update Station")

    def get_success_url(self):
        return reverse_lazy("whalesdb:list_stn")


class CommonDetails(DetailView):
    # default template to use to create a details view
    template_name = "whalesdb/whales_details.html"

    # title to display on the list page
    title = None

    # key used for creating default list and update URLs in the get_context_data method
    key = None

    # URL linking the details page back to the proper list
    list_url = None
    update_url = None

    # By default detail objects are editable, set to false to remove update buttons
    editable = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.title:
            context['title'] = self.title

        if self.fields:
            context['fields'] = self.fields

        context['list_url'] = self.list_url if self.list_url else "whalesdb:list_{}".format(self.key)
        context['update_url'] = self.update_url if self.update_url else "whalesdb:update_{}".format(self.key)
        # for the most part if the user is authorized then the content is editable
        # but extending classes can choose to make content not editable even if the user is authorized
        context['auth'] = utils.whales_authorized(self.request.user)
        context['editable'] = context['auth'] and self.editable

        return context


class DepDetails(CommonDetails):
    key = "dep"
    model = models.DepDeployment
    template_name = 'whalesdb/details_dep.html'
    title = _("Deployment Details")
    fields = ['dep_name', 'dep_year', 'dep_month', 'stn', 'prj', 'mor']

    def test_func(self):
        # editable if the object has no station events
        auth = self.model.objects.get(pk=self.kwargs['pk']).station_events.count() <= 0

        return auth

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['google_api_key'] = settings.GOOGLE_API_KEY
        # auth is set in the CommonDetails.get_context_data function.
        # So if the user has auth AND the object is editable set auth to true
        context['editable'] = self.test_func() and context['auth']

        return context


class EmmDetails(CommonDetails):
    key = "emm"
    model = models.EmmMakeModel
    template_name = 'whalesdb/details_emm.html'
    title = _("Make/Model Details")
    fields = ['eqt', 'emm_make', 'emm_model', 'emm_depth_rating', 'emm_description']


class EqpDetails(CommonDetails):
    key = "eqp"
    template_name = "whalesdb/details_eqp.html"
    model = models.EqpEquipment
    title = _("Equipment Details")
    fields = ['emm', 'eqp_serial', 'eqp_asset_id', 'eqp_date_purchase', 'eqp_notes', 'eqp_retired', 'eqo_owned_by']


class MorDetails(CommonDetails):
    key = "mor"
    model = models.MorMooringSetup
    template_name = 'whalesdb/details_mor.html'
    title = _("Mooring Setup Details")
    fields = ["mor_name", "mor_max_depth", "mor_link_setup_image", "mor_additional_equipment",
              "mor_general_moor_description", "mor_notes"]
    creation_form_height = 600


class PrjDetails(CommonDetails):
    key = 'prj'
    model = models.PrjProject
    title = _("Project Details")
    fields = ['name', 'description_en', 'prj_url']
    creation_form_height = 725


class RecDetails(CommonDetails):
    key = 'rec'
    model = models.RecDataset
    title = _("Dataset")
    template_name = "whalesdb/details_rec.html"
    fields = ['eda_id', 'rsc_id', 'rtt_dataset', 'rtt_in_water', 'rec_start_date', 'rec_start_time', 'rec_end_date',
              'rec_end_time', 'rec_backup_hd_1', 'rec_backup_hd_2', 'rec_notes', ]


class RscDetails(CommonDetails):
    key = 'rsc'
    model = models.RscRecordingSchedule
    title = _("Recording Schedule Details")
    template_name = "whalesdb/details_rsc.html"
    fields = ['rsc_name', 'rsc_period']
    editable = False


class RttDetails(CommonDetails):
    key = 'rtt'
    model = models.RttTimezoneCode
    title = _("Time Zone")
    template_name = "whalesdb/details_rtt.html"
    fields = ['rtt_name', 'rtt_abb', 'rtt_period']


class StnDetails(CommonDetails):
    key = 'stn'
    model = models.StnStation
    title = _("Station Details")
    template_name = 'whalesdb/details_stn.html'
    fields = ['stn_name', 'stn_code', 'stn_revision', 'stn_planned_lat', 'stn_planned_lon',
              'stn_planned_depth', 'stn_notes']
    creation_form_height = 400

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['google_api_key'] = settings.GOOGLE_API_KEY

        return context


class CommonList(CommonAuthFilterView):

    nav_menu = 'whalesdb/whale_nav_menu.html'
    site_css = 'whalesdb/whales_css.css'
    home_url_name = "whalesdb:index"

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

    # By default Listed objects will have an update button, set editable to false in extending classes to disable
    editable = True

    def get_fields(self):
        if self.fields:
            return self.fields

        return ['tname|Name', 'tdescription|Description']

    def get_create_url(self):
        return self.create_url if self.create_url is not None else "whalesdb:create_{}".format(self.key)

    def get_details_url(self):
        return self.details_url if self.details_url is not None else "whalesdb:details_{}".format(self.key)

    def get_update_url(self):
        return self.update_url if self.update_url is not None else "whalesdb:update_{}".format(self.key)

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs)

        context['fields'] = self.get_fields()

        # if the url is not None, use the value specified by the url variable.
        # if the url is None, create a url using the views key
        # this way if no URL, say details_url, is provided it's assumed the default RUL will be 'whalesdb:details_key'
        # if the details_url = False in the extending view then False will be passed to the context['detials_url']
        # variable and in the template where the variable is used for buttons and links the button and/or links can
        # be left out without causing URL Not Found issues.
        context['create_url'] = self.get_create_url()
        context['details_url'] = self.get_details_url()
        context['update_url'] = self.get_update_url()

        # for the most part if the user is authorized then the content is editable
        # but extending classes can choose to make content not editable even if the user is authorized
        context['auth'] = utils.whales_authorized(self.request.user)
        context['editable'] = context['auth'] and self.editable

        if self.creation_form_height:
            context['height'] = self.creation_form_height

        return context


class DepList(CommonList):
    key = 'dep'
    model = models.DepDeployment
    filterset_class = filters.DepFilter
    fields = ['dep_name', 'dep_year', 'dep_month', 'stn', 'prj', 'mor']
    title = _("Deployment List")
    creation_form_height = 600

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs)
        context['editable'] = False
        return context


class EmmList(CommonList):
    key = 'emm'
    model = models.EmmMakeModel
    filterset_class = filters.EmmFilter
    fields = ['eqt', 'emm_make', 'emm_model', 'emm_depth_rating']
    title = _("Make/Model List")


class EqpList(CommonList):
    key = 'eqp'
    model = models.EqpEquipment
    filterset_class = filters.EqpFilter
    fields = ['emm', 'eqp_serial', 'eqp_date_purchase', 'eqo_owned_by', 'eqp_retired', "eqp_deployed"]
    title = _("Equipment List")


class MorList(CommonList):
    key = 'mor'
    model = models.MorMooringSetup
    filterset_class = filters.MorFilter
    fields = ['mor_name', 'mor_max_depth', 'mor_notes']
    title = _("Mooring Setup List")
    creation_form_height = 725


class PrjList(CommonList):
    key = 'prj'
    model = models.PrjProject
    filterset_class = filters.PrjFilter
    title = _("Project List")
    creation_form_height = 400
    fields = ['tname|Name', 'tdescription|Description']


class RecList(CommonList):
    key = 'rec'
    model = models.RecDataset
    filterset_class = filters.RecFilter
    title = _("Dataset")
    fields = ['eda_id', 'rsc_id', 'rec_start_date', 'rec_end_date']


class RscList(CommonList):
    key = 'rsc'
    model = models.RscRecordingSchedule
    filterset_class = filters.RscFilter
    title = _("Recording Schedule List")
    fields = ['rsc_name', 'rsc_period']
    editable = False


class RttList(CommonList):
    key = 'rtt'
    model = models.RttTimezoneCode
    filterset_class = filters.RttFilter
    title = _("Time Zone")
    fields = ['rtt_name', 'rtt_abb', 'rtt_offset']
    editable = False

    def get_details_url(self):
        return None


class StnList(CommonList):
    key = 'stn'
    model = models.StnStation
    filterset_class = filters.StnFilter
    fields = ['stn_name', 'stn_code', 'stn_revision']
    title = _("Station List")


class TeaList(CommonList):
    key = 'tea'
    model = models.TeaTeamMember
    filterset_class = filters.TeaFilter
    fields = ["tea_abb", "tea_last_name", "tea_first_name"]
    title = _("Team Member List")

    details_url = False
    update_url = False
