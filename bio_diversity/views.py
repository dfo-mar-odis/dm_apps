from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, DetailView, DeleteView
from shared_models.views import CommonAuthCreateView, CommonAuthFilterView, CommonAuthUpdateView, CommonTemplateView, \
    CommonFormsetView, CommonHardDeleteView
from django.urls import reverse_lazy
from django import forms
from bio_diversity.forms import HelpTextFormset, CommentKeywordsFormset
from django.forms.models import model_to_dict
from . import mixins, filters, utils, models
from datetime import date
from django.utils.translation import gettext_lazy as _

from .mixins import IndvMixin
from .utils import get_cont_evnt


class IndexTemplateView(TemplateView):
    nav_menu = 'bio_diversity/bio_diversity_nav_menu.html'
    site_css = 'bio_diversity/bio_diversity_css.css'
    home_url_name = "bio_diversity:index"

    template_name = 'bio_diversity/index.html'


class AdminIndexTemplateView(TemplateView):
    nav_menu = 'bio_diversity/bio_diversity_nav_menu.html'
    site_css = 'bio_diversity/bio_diversity_css.css'
    home_url_name = "bio_diversity:index"

    template_name = 'bio_diversity/admin_index.html'

    def get(self, request, *args, **kwargs):
        if not utils.bio_diverisity_admin(self.request.user):
            return HttpResponseRedirect(reverse_lazy('accounts:login_required'))
        else:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        # we want to update the context with the context vars added by CommonMixin classes
        context = super().get_context_data(**kwargs)
        context["auth"] = utils.bio_diverisity_admin(self.request.user)
        return context


class CodesIndexTemplateView(TemplateView):
    nav_menu = 'bio_diversity/bio_diversity_nav_menu.html'
    site_css = 'bio_diversity/bio_diversity_css.css'
    home_url_name = "bio_diversity:index"

    template_name = 'bio_diversity/codes_index.html'

    def get(self, request, *args, **kwargs):
        if not utils.bio_diverisity_admin(self.request.user):
            return HttpResponseRedirect(reverse_lazy('accounts:login_required'))
        else:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        # we want to update the context with the context vars added by CommonMixin classes
        context = super().get_context_data(**kwargs)
        context["auth"] = utils.bio_diverisity_admin(self.request.user)
        return context


class FacicIndexTemplateView(TemplateView):
    nav_menu = 'bio_diversity/bio_diversity_nav_menu.html'
    site_css = 'bio_diversity/bio_diversity_css.css'
    home_url_name = "bio_diversity:index"

    template_name = 'bio_diversity/facic_index.html'

    def get(self, request, *args, **kwargs):
        if not utils.bio_diverisity_admin(self.request.user):
            return HttpResponseRedirect(reverse_lazy('accounts:login_required'))
        else:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        # we want to update the context with the context vars added by CommonMixin classes
        context = super().get_context_data(**kwargs)
        context["auth"] = utils.bio_diverisity_admin(self.request.user)
        return context


class ProgIndexTemplateView(TemplateView):
    nav_menu = 'bio_diversity/bio_diversity_nav_menu.html'
    site_css = 'bio_diversity/bio_diversity_css.css'
    home_url_name = "bio_diversity:index"

    template_name = 'bio_diversity/prog_index.html'

    def get(self, request, *args, **kwargs):
        if not utils.bio_diverisity_admin(self.request.user):
            return HttpResponseRedirect(reverse_lazy('accounts:login_required'))
        else:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        # we want to update the context with the context vars added by CommonMixin classes
        context = super().get_context_data(**kwargs)
        context["auth"] = utils.bio_diverisity_admin(self.request.user)
        return context


# CommonCreate Extends the UserPassesTestMixin used to determine if a user has
# has the correct privileges to interact with Creation Views
# --------------------CREATE VIEWS----------------------------------------
class CommonCreate(CommonAuthCreateView):

    nav_menu = 'bio_diversity/bio_diversity_nav.html'
    site_css = 'bio_diversity/bio_diversity.css'
    home_url_name = "bio_diversity:index"

    def get_initial(self):
        init = super().get_initial()

        init["created_by"] = self.request.user.username
        init["created_date"] = date.today

        if hasattr(self.model, "start_date"):
            init["start_date"] = date.today

        return init

    # Upon success most creation views will be redirected to their respective 'CommonList' view. To send
    # a successful creation view somewhere else, override this method
    def get_success_url(self):
        success_url = self.success_url if self.success_url else reverse_lazy("bio_diversity:list_{}".format(self.key))

        if self.kwargs.get("pop"):
            # create views intended to be pop out windows should close the window upon success
            success_url = reverse_lazy("shared_models:close_me_no_refresh")

        return success_url

    # overrides the UserPassesTestMixin test to check that a user belongs to the bio_diversity_admin group
    def test_func(self):
        if self.admin_only:
            return utils.bio_diverisity_admin(self.request.user)
        else:
            return utils.bio_diverisity_authorized(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editable'] = context['auth']
        context['help_text_dict'] = utils.get_help_text_dict(self.model)

        return context


class AnidcCreate(mixins.AnidcMixin, CommonCreate):
    pass


class AnixCreate(mixins.AnixMixin, CommonCreate):
    def get_initial(self):
        initial = super().get_initial()
        if 'evnt' in self.kwargs:
            initial['evnt_id'] = self.kwargs['evnt']

        if 'visible' in self.kwargs:
            for field in self.get_form_class().base_fields:
                if field in self.kwargs['visible']:
                    self.get_form_class().base_fields[field].widget = forms.Select()
                else:
                    self.get_form_class().base_fields[field].widget = forms.HiddenInput()
        else:
            for field in self.get_form_class().base_fields:
                self.get_form_class().base_fields[field].widget = forms.Select()

        return initial


class AdscCreate(mixins.AdscMixin, CommonCreate):
    pass


class CntCreate(mixins.CntMixin, CommonCreate):
    def get_initial(self):
        initial = super().get_initial()
        if 'loc' in self.kwargs:
            initial['loc_id'] = self.kwargs['loc']


class CntcCreate(mixins.CntcMixin, CommonCreate):
    pass


class CntdCreate(mixins.CntdMixin, CommonCreate):
    pass


class CollCreate(mixins.CollMixin, CommonCreate):
    pass


class ContdcCreate(mixins.ContdcMixin, CommonCreate):
    pass


class ContxCreate(mixins.ContxMixin, CommonCreate):
    def get_initial(self):
        initial = super().get_initial()
        if 'evnt' in self.kwargs:
            initial['evnt_id'] = self.kwargs['evnt']

        if 'visible' in self.kwargs:
            for field in self.get_form_class().base_fields:
                if field in self.kwargs['visible']:
                    self.get_form_class().base_fields[field].widget = forms.Select()
                else:
                    self.get_form_class().base_fields[field].widget = forms.HiddenInput()
        else:
            for field in self.get_form_class().base_fields:
                self.get_form_class().base_fields[field].widget = forms.Select()

        return initial


class CdscCreate(mixins.CdscMixin, CommonCreate):
    pass


class CupCreate(mixins.CupMixin, CommonCreate):
    pass


class CupdCreate(mixins.CupdMixin, CommonCreate):
    pass


class DataCreate(mixins.DataMixin, CommonCreate):
    template_name = 'bio_diversity/data_entry_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        init = super().get_initial()
        if 'evnt' in self.kwargs:
            init['evnt_id'] = self.kwargs['evnt']
            evntc = models.Event.objects.filter(pk=self.kwargs["evnt"]).get().evntc_id
            init['evntc_id'] = evntc
            init['facic_id'] = models.Event.objects.filter(pk=self.kwargs["evnt"]).get().facic_id
            self.get_form_class().base_fields["evnt_id"].widget = forms.HiddenInput()
            self.get_form_class().base_fields["evntc_id"].widget = forms.HiddenInput()
            self.get_form_class().base_fields["facic_id"].widget = forms.HiddenInput()
            if evntc.__str__() == "Electrofishing":
                self.get_form_class().base_fields["tank_id"].widget = forms.Select()
                self.get_form_class().base_fields["tank_id"].required = True
            else:
                self.get_form_class().base_fields["tank_id"].required = False
                self.get_form_class().base_fields["tank_id"].widget = forms.HiddenInput()
        return init

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'evnt' in self.kwargs:
            evnt_code = models.Event.objects.filter(pk=self.kwargs["evnt"]).get().evntc_id.__str__().lower()
            facility_code = models.Event.objects.filter(pk=self.kwargs["evnt"]).get().facic_id.__str__().lower()
            context["title"] = "Add {} data".format(evnt_code)
            context["template_url"] = 'data_templates/{}-{}.xlsx'.format(facility_code, evnt_code)
            context["template_name"] = "{}-{}".format(facility_code, evnt_code)
        return context

    def get_success_url(self):
        success_url = reverse_lazy("bio_diversity:data_log")
        return success_url


class DrawCreate(mixins.DrawMixin, CommonCreate):
    pass


class EnvCreate(mixins.EnvMixin, CommonCreate):
    def get_initial(self):
        init = super().get_initial()
        init["start_date"] = date.today()
        if 'loc' in self.kwargs:
            init['loc_id'] = self.kwargs['loc']
        return init


class EnvcCreate(mixins.EnvcMixin, CommonCreate):
    pass


class EnvcfCreate(mixins.EnvcfMixin, CommonCreate):
    pass


class EnvscCreate(mixins.EnvscMixin, CommonCreate):
    pass


class EnvtCreate(mixins.EnvtMixin, CommonCreate):
    pass


class EnvtcCreate(mixins.EnvtcMixin, CommonCreate):
    pass


class EvntCreate(mixins.EvntMixin, CommonCreate):
    def get_success_url(self):
        success_url = self.success_url if self.success_url else reverse_lazy("bio_diversity:details_{}".format(self.key), kwargs = {'pk': self.object.pk})

        if self.kwargs.get("pop"):
            # create views intended to be pop out windows should close the window upon success
            success_url = reverse_lazy("shared_models:close_me_no_refresh")

        return success_url


class EvntcCreate(mixins.EvntcMixin, CommonCreate):
    pass


class FacicCreate(mixins.FacicMixin, CommonCreate):
    pass


class FecuCreate(mixins.FecuMixin, CommonCreate):
    pass


class FeedCreate(mixins.FeedMixin, CommonCreate):
    pass


class FeedcCreate(mixins.FeedcMixin, CommonCreate):
    pass


class FeedmCreate(mixins.FeedmMixin, CommonCreate):
    pass


class GrpCreate(mixins.GrpMixin, CommonCreate):

    def form_valid(self, form):
        """If the form is valid, save the associated model and add an X ref object."""
        self.object = form.save()
        if 'evnt' in self.kwargs:
            anix_link = models.AniDetailXref(evnt_id=models.Event.objects.filter(pk=self.kwargs['evnt']).get(),
                                             grp_id=self.object, created_by=self.object.created_by,
                                             created_date=self.object.created_date)
            anix_link.clean()
            anix_link.save()
        return super().form_valid(form)


class GrpdCreate(mixins.GrpdMixin, CommonCreate):
    pass


class HeatCreate(mixins.HeatMixin, CommonCreate):
    pass


class HeatdCreate(mixins.HeatdMixin, CommonCreate):
    pass


class ImgCreate(mixins.ImgMixin, CommonCreate):
    pass


class ImgcCreate(mixins.ImgcMixin, CommonCreate):
    pass


class IndvCreate(mixins.IndvMixin, CommonCreate):

    def get_initial(self):
        init = super().get_initial()
        if 'clone' in self.kwargs:
            parent_indv = models.Individual.objects.filter(pk=self.kwargs["clone_id"]).get()
            for name, value in model_to_dict(parent_indv).items():
                if name not in ["ufid", "pit_tag", "created_by", "created_date"]:
                    init[name] = value
        return init

    def form_valid(self, form):
        """If the form is valid, save the associated model and add an X ref object."""
        self.object = form.save()
        if 'evnt' in self.kwargs:
            anix_link = models.AniDetailXref(evnt_id=models.Event.objects.filter(pk=self.kwargs['evnt']).get(),
                                             indv_id=self.object, created_by=self.object.created_by, 
                                             created_date=self.object.created_date)
            anix_link.clean()
            anix_link.save()
        return super().form_valid(form)


class IndvdCreate(mixins.IndvdMixin, CommonCreate):
    pass


class IndvtCreate(mixins.IndvtMixin, CommonCreate):
    pass


class IndvtcCreate(mixins.IndvtcMixin, CommonCreate):
    pass


class InstCreate(mixins.InstMixin, CommonCreate):
    pass


class InstcCreate(mixins.InstcMixin, CommonCreate):
    pass


class InstdCreate(mixins.InstdMixin, CommonCreate):
    pass


class InstdcCreate(mixins.InstdcMixin, CommonCreate):
    pass


class LocCreate(mixins.LocMixin, CommonCreate):
    pass


class LoccCreate(mixins.LoccMixin, CommonCreate):
    pass


class MatpCreate(mixins.MatpMixin, CommonCreate):
    pass


class OrgaCreate(mixins.OrgaMixin, CommonCreate):
    pass


class PairCreate(mixins.PairMixin, CommonCreate):
    pass


class PercCreate(mixins.PercMixin, CommonCreate):
    pass


class PrioCreate(mixins.PrioMixin, CommonCreate):
    pass


class ProgCreate(mixins.ProgMixin, CommonCreate):
    pass


class ProgaCreate(mixins.ProgaMixin, CommonCreate):
    pass


class ProtCreate(mixins.ProtMixin, CommonCreate):
    def get_initial(self):
        initial = super().get_initial()
        if 'prog' in self.kwargs:
            initial['prog_id'] = self.kwargs['prog']
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['java_script'] = 'bio_diversity/_entry_prot_js.html'

        return context


class ProtcCreate(mixins.ProtcMixin, CommonCreate):
    pass


class ProtfCreate(mixins.ProtfMixin, CommonCreate):
    def get_initial(self):
        initial = super().get_initial()
        if 'prot' in self.kwargs:
            initial['prot_id'] = self.kwargs['prot']
        return initial


class QualCreate(mixins.QualMixin, CommonCreate):
    pass


class RelcCreate(mixins.RelcMixin, CommonCreate):
    pass


class RiveCreate(mixins.RiveMixin, CommonCreate):
    pass


class RoleCreate(mixins.RoleMixin, CommonCreate):
    pass


class SampCreate(mixins.SampMixin, CommonCreate):
    pass


class SampcCreate(mixins.SampcMixin, CommonCreate):
    pass


class SampdCreate(mixins.SampdMixin, CommonCreate):
    pass


class SireCreate(mixins.SireMixin, CommonCreate):
    def get_initial(self):
        initial = super().get_initial()
        if 'pair' in self.kwargs:
            initial['pair_id'] = self.kwargs['pair']
        return initial


class SpwndCreate(mixins.SpwndMixin, CommonCreate):
    pass


class SpwndcCreate(mixins.SpwndcMixin, CommonCreate):
    pass


class SpwnscCreate(mixins.SpwnscMixin, CommonCreate):
    pass


class SpecCreate(mixins.SpecMixin, CommonCreate):
    pass


class StokCreate(mixins.StokMixin, CommonCreate):
    pass


class SubrCreate(mixins.SubrMixin, CommonCreate):
    pass


class TankCreate(mixins.TankMixin, CommonCreate):
    def form_valid(self, form):
        """If the form is valid, save the associated model and add an X ref object."""
        self.object = form.save()
        if 'evnt' in self.kwargs:
            contx_link = models.ContainerXRef(evnt_id=models.Event.objects.filter(pk=self.kwargs['evnt']).get(),
                                              tank_id=self.object, created_by=self.object.created_by,
                                              created_date=self.object.created_date)
            contx_link.clean()
            contx_link.save()
        return super().form_valid(form)


class TankdCreate(mixins.TankdMixin, CommonCreate):
    pass


class TeamCreate(mixins.TeamMixin, CommonCreate):
    pass


class TrayCreate(mixins.TrayMixin, CommonCreate):
    def form_valid(self, form):
        """If the form is valid, save the associated model and add an X ref object."""
        self.object = form.save()
        if 'evnt' in self.kwargs:
            contx_link = models.ContainerXRef(evnt_id=models.Event.objects.filter(pk=self.kwargs['evnt']).get(),
                                              tank_id=self.object, created_by=self.object.created_by,
                                              created_date=self.object.created_date)
            contx_link.clean()
            contx_link.save()
        return super().form_valid(form)


class TraydCreate(mixins.TraydMixin, CommonCreate):
    pass


class TribCreate(mixins.TribMixin, CommonCreate):
    pass


class TrofCreate(mixins.TrofMixin, CommonCreate):
    def form_valid(self, form):
        """If the form is valid, save the associated model and add an X ref object."""
        self.object = form.save()
        if 'evnt' in self.kwargs:
            contx_link = models.ContainerXRef(evnt_id=models.Event.objects.filter(pk=self.kwargs['evnt']).get(),
                                              trof_id=self.object, created_by=self.object.created_by,
                                              created_date=self.object.created_date)
            contx_link.clean()
            contx_link.save()
        return super().form_valid(form)


class TrofdCreate(mixins.TrofdMixin, CommonCreate):
    pass


class UnitCreate(mixins.UnitMixin, CommonCreate):
    pass


# ---------------------------DETAIL VIEWS-----------------------------------------------
class CommonDetails(DetailView):
    # default template to use to create a details view
    template_name = "bio_diversity/bio_details.html"

    # title to display on the list page
    title = None

    # key used for creating default list and update URLs in the get_context_data method
    key = None

    # URL linking the details page back to the proper list
    list_url = None
    update_url = None

    # By default detail objects are editable, set to false to remove update buttons
    editable = True

    def get_auth(self):
        if self.admin_only:
            return utils.bio_diverisity_admin(self.request.user)
        else:
            return utils.bio_diverisity_authorized(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.title:
            context['title'] = self.title

        if self.fields:
            context['fields'] = self.fields

        if "back" in self.kwargs:
            context['list_url'] = "bio_diversity:details_{}".format(self.kwargs["back"])
            context['back'] = True
            context['back_id'] = self.kwargs["back_id"]
        else:
            context['list_url'] = self.list_url if self.list_url else "bio_diversity:list_{}".format(self.key)
        context['update_url'] = self.update_url if self.update_url else "bio_diversity:update_{}".format(self.key)
        # for the most part if the user is authorized then the content is editable
        # but extending classes can choose to make content not editable even if the user is authorized
        context['auth'] = self.get_auth()
        context['editable'] = context['auth'] and self.editable
        context["model_key"] = self.key

        return context


class AnidcDetails(mixins.AnidcMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "min_val", "max_val", "unit_id", "ani_subj_flag",
              "created_by", "created_date", ]


class AnixDetails(mixins.AnixMixin, CommonDetails):
    fields = ["evnt_id", "loc_id", "indvt_id", "indv_id", "pair_id", "grp_id", "created_by",
              "created_date", ]


class AdscDetails(mixins.AdscMixin, CommonDetails):
    fields = ["anidc_id", "name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class CntDetails(mixins.CntMixin, CommonDetails):
    fields = ["loc_id", "cntc_id", "spec_id", "cnt", "est", "comments", "created_by", "created_date", ]

    def get_context_data(self, **kwargs):
        # use this to pass sire fields/sample object to template
        context = super().get_context_data(**kwargs)

        context["table_list"] = ["cntd"]

        cntd_list = [cntd for cntd in self.object.count_details.all()]
        cntd_field_list = ["anidc_id", "det_val"]
        obj_mixin = mixins.CntdMixin
        context["cntd_context_dict"] = {"div_title": "Count Details",
                                        "sub_model_key": obj_mixin.key,
                                        "objects_list": cntd_list,
                                        "field_list": cntd_field_list,
                                        "single_object": obj_mixin.model.objects.first()}

        return context


class CntcDetails(mixins.CntcMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class CntdDetails(mixins.CntdMixin, CommonDetails):
    fields = ["cnt_id", "anidc_id", "adsc_id", "det_val", "qual_id", "comments", "created_by", "created_date", ]


class CollDetails(mixins.CollMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class ContdcDetails(mixins.ContdcMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "min_val", "max_val", "unit_id", "cont_subj_flag",
              "created_by", "created_date", ]


class ContxDetails(mixins.ContxMixin, CommonDetails):
    fields = ["evnt_id", "cup_id", "draw_id", "heat_id", "tank_id", "tray_id", "trof_id", "created_by", "created_date"]


class CdscDetails(mixins.CdscMixin, CommonDetails):
    fields = ["contdc_id", "name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class CupDetails(mixins.CupMixin, CommonDetails):
    fields = ["facic_id", "name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class CupdDetails(mixins.CupdMixin, CommonDetails):
    fields = ["cup_id", "contdc_id", "det_value", "cdsc_id", "start_date", "end_date", "det_valid", "comments",
              "created_by", "created_date", ]


class DrawDetails(mixins.DrawMixin, CommonDetails):
    fields = ["facic_id", "name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class EnvDetails(mixins.EnvMixin, CommonDetails):
    template_name = 'bio_diversity/details_env.html'
    fields = ["loc_id", "inst_id", "envc_id", "env_val", "envsc_id", "start_date", "start_time",
              "end_date", "end_time", "env_avg", "qual_id", "comments", "created_by", "created_date"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["envcf_object"] = models.EnvCondFile.objects.first()
        context["envcf_field_list"] = [
            "env_pdf",
            "created_date",
        ]

        return context


class EnvcDetails(mixins.EnvcMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "min_val", "max_val", "unit_id", "env_subj_flag",
              "created_by", "created_date", ]


class EnvcfDetails(mixins.EnvcfMixin, CommonDetails):
    template_name = 'bio_diversity/details_envcf.html'
    fields = ["env_id", "env_pdf", "comments", "created_by", "created_date", ]


class EnvscDetails(mixins.EnvscMixin, CommonDetails):
    fields = ["name", "nom", "envc_id", "description_en", "description_fr", "created_by", "created_date", ]


class EnvtDetails(mixins.EnvtMixin, CommonDetails):
    fields = ["envtc_id", "lot_num", "amt", "unit_id", "duration", "comments", "created_by",
              "created_date", ]


class EnvtcDetails(mixins.EnvtcMixin, CommonDetails):
    fields = ["name", "nom", "rec_dose", "manufacturer", "description_en", "description_fr", "created_by",
              "created_date", ]


class EvntDetails(mixins.EvntMixin, CommonDetails):
    fields = ["facic_id", "evntc_id", "perc_id", "prog_id", "team_id", "start_date", "start_time", "end_date",
              "end_time", "comments", "created_by", "created_date", ]

    def get_context_data(self, **kwargs):
        # use this to pass sire fields/sample object to template
        context = super().get_context_data(**kwargs)

        loc_list = [loc for loc in self.object.location.all()]
        loc_field_list = ["locc_id", "rive_id", "subr_id", "start_date"]
        obj_mixin = mixins.LocMixin
        context["loc_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                       "sub_model_key": obj_mixin.key,
                                       "objects_list": loc_list,
                                       "field_list": loc_field_list,
                                       "single_object": obj_mixin.model.objects.first()}

        contx_set = self.object.containers.filter(tank_id__isnull=False, cup_id__isnull=True, heat_id__isnull=True,
                                                  tray_id__isnull=True, trof_id__isnull=True, draw_id__isnull=True)
        tank_list = list(dict.fromkeys([contx.tank_id for contx in contx_set]))
        tank_field_list = ["name"]
        obj_mixin = mixins.TankMixin
        context["tank_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                       "sub_model_key": obj_mixin.key,
                                       "objects_list": tank_list,
                                       "field_list": tank_field_list,
                                       "single_object": obj_mixin.model.objects.first()}

        contx_set = self.object.containers.filter(tank_id__isnull=True, cup_id__isnull=True, heat_id__isnull=True,
                                                  trof_id__isnull=False, draw_id__isnull=True)
        trof_list = list(dict.fromkeys([contx.trof_id for contx in contx_set]))
        trof_field_list = ["name"]
        obj_mixin = mixins.TrofMixin
        context["trof_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                       "sub_model_key": obj_mixin.key,
                                       "objects_list": trof_list,
                                       "field_list": trof_field_list,
                                       "single_object": obj_mixin.model.objects.first()}

        anix_set = self.object.animal_details.filter(indv_id__isnull=False, grp_id__isnull=True, contx_id__isnull=True,
                                                     loc_id__isnull=True, indvt_id__isnull=True, pair_id__isnull=True)
        indv_list = list(dict.fromkeys([anix.indv_id for anix in anix_set]))
        indv_field_list = ["ufid", "pit_tag", "grp_id", ]
        obj_mixin = mixins.IndvMixin
        context["indv_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                        "sub_model_key": obj_mixin.key,
                                        "objects_list": indv_list,
                                        "field_list": indv_field_list,
                                        "single_object": obj_mixin.model.objects.first()}

        anix_set = self.object.animal_details.filter(grp_id__isnull=False, indv_id__isnull=True, contx_id__isnull=True,
                                                     loc_id__isnull=True, indvt_id__isnull=True, pair_id__isnull=True)
        grp_list = list(dict.fromkeys([anix.grp_id for anix in anix_set]))  # get unique values
        grp_field_list = ["stok_id", "coll_id", "spec_id", ]
        obj_mixin = mixins.GrpMixin
        context["grp_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                       "sub_model_key": obj_mixin.key,
                                       "objects_list": grp_list,
                                       "field_list": grp_field_list,
                                       "single_object": obj_mixin.model.objects.first()}

        prot_set = models.Protocol.objects.filter(prog_id=self.object.prog_id, evntc_id=self.object.evntc_id)
        prot_list = list(dict.fromkeys([prot for prot in prot_set]))
        prot_field_list = ["evntc_id", "start_date", "end_date", ]
        obj_mixin = mixins.ProtMixin
        context["prot_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                        "sub_model_key": obj_mixin.key,
                                        "objects_list": prot_list,
                                        "field_list": prot_field_list,
                                        "single_object": obj_mixin.model.objects.first()}

        anix_set = self.object.animal_details.filter(pair_id__isnull=False, grp_id__isnull=True, contx_id__isnull=True,
                                                     loc_id__isnull=True, indvt_id__isnull=True, indv_id__isnull=True)
        pair_list = list(dict.fromkeys([anix.pair_id for anix in anix_set]))
        pair_field_list = ["start_date", "indv_id", ]
        obj_mixin = mixins.PairMixin
        context["pair_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                        "sub_model_key": obj_mixin.key,
                                        "objects_list": pair_list,
                                        "field_list": pair_field_list,
                                        "single_object": obj_mixin.model.objects.first()}

        matp_list = [matp for matp in self.object.mating_plan.all()]
        matp_field_list = ["matp_xls", "stok_id", ]
        obj_mixin = mixins.MatpMixin
        context["matp_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                        "sub_model_key": obj_mixin.key,
                                        "objects_list": matp_list,
                                        "field_list": matp_field_list,
                                        "single_object": obj_mixin.model.objects.first()}

        context["table_list"] = ["loc", "indv", "grp", "tank", "trof", "pair", "matp", "prot"]
        evnt_code = self.object.evntc_id.__str__()
        if evnt_code == "Electrofishing":
            context["table_list"] = ["data", "loc", "grp", "tank", "prot"]
        elif evnt_code == "PIT Tagging":
            context["table_list"] = ["data", "indv", "grp", "tank", "prot"]
        elif evnt_code == "Egg Development":
            context["table_list"] = ["data", "grp", "trof", "prot"]
        elif evnt_code == "Maturity Sorting":
            context["table_list"] = ["data", "indv", "tank", "prot"]
        elif evnt_code == "Water Quality Record":
            context["table_list"] = ["data", "tank", "prot"]
        elif evnt_code == "Spawning":
            context["table_list"] = ["data", "indv", "pair", "grp", "matp", "prot"]
        elif evnt_code == "Treatment":
            context["table_list"] = ["data", "tank", "trof", "prot"]

        return context


class EvntcDetails(mixins.EvntcMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class FacicDetails(mixins.FacicMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class FecuDetails(mixins.FecuMixin, CommonDetails):
    fields = ["stok_id", "coll_id", "description_en", "start_date", "end_date", "alpha", "beta", "valid",
              "comments", "created_by", "created_date", ]


class FeedDetails(mixins.FeedMixin, CommonDetails):
    fields = ["feedm_id", "feedc_id", "lot_num", "amt", "unit_id", "freq", "comments", "created_by",
              "created_date", ]


class FeedcDetails(mixins.FeedcMixin, CommonDetails):
    fields = ["name", "nom", "manufacturer", "description_en", "description_fr", "created_by", "created_date", ]


class FeedmDetails(mixins.FeedmMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class GrpDetails(mixins.GrpMixin, CommonDetails):
    fields = ["spec_id", "stok_id", "coll_id", "grp_year", "grp_valid", "comments", "created_by", "created_date", ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table_list"] = ["evnt", "grpd", "pair", "cont"]
        anix_set = self.object.animal_details.filter(evnt_id__isnull=False, contx_id__isnull=True, loc_id__isnull=True,
                                                     indvt_id__isnull=True, indv_id__isnull=True, pair_id__isnull=True)
        evnt_list = list(dict.fromkeys([anix.evnt_id for anix in anix_set]))
        evnt_field_list = ["evntc_id", "facic_id", "prog_id", "start_datetime" ]
        obj_mixin = mixins.EvntMixin
        context["evnt_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                        "sub_model_key": obj_mixin.key,
                                        "objects_list": evnt_list,
                                        "field_list": evnt_field_list,
                                        "single_object": obj_mixin.model.objects.first()}

        grpd_list = list(dict.fromkeys([models.GroupDet.objects.filter(anix_id=anix.pk).get() for anix in anix_set
                                        if models.GroupDet.objects.filter(anix_id=anix.pk)]))

        grpd_field_list = ["anidc_id", "det_val", "grpd_valid", "detail_date" ]
        obj_mixin = mixins.GrpdMixin
        context["grpd_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                        "sub_model_key": obj_mixin.key,
                                        "objects_list": grpd_list,
                                        "field_list": grpd_field_list,
                                        "single_object": obj_mixin.model.objects.first()}

        anix_evnt_set = self.object.animal_details.filter(contx_id__isnull=False, loc_id__isnull=True,
                                                          indvt_id__isnull=True, pair_id__isnull=True)

        contx_tuple_set = list(dict.fromkeys([(anix.contx_id, anix.final_contx_flag) for anix in anix_evnt_set]))
        context["cont_evnt_list"] = [get_cont_evnt(contx) for contx in contx_tuple_set]
        context["cont_evnt_field_list"] = [
            "Evnt",
            "Date",
            "Container",
        ]

        anix_set = self.object.animal_details.filter(contx_id__isnull=True, loc_id__isnull=True,
                                                      indvt_id__isnull=True, pair_id__isnull=False)
        pair_list = [anix.pair_id for anix in anix_set]
        pair_field_list = ["start_date", "indv_id", "prio_id" ]
        obj_mixin = mixins.PairMixin
        context["pair_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                        "sub_model_key": obj_mixin.key,
                                        "objects_list": pair_list,
                                        "field_list": pair_field_list,
                                        "single_object": obj_mixin.model.objects.first()}

        return context


class GrpdDetails(mixins.GrpdMixin, CommonDetails):
    fields = ["anidc_id",  "det_val", "adsc_id", "qual_id", "grpd_valid",  "detail_date", "comments", "created_by", "created_date", ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["title"] = "Group: {}".format(self.object.__str__())
        return context


class HeatDetails(mixins.HeatMixin, CommonDetails):
    fields = ["facic_id", "name", "nom", "description_en", "description_fr", "manufacturer", "serial_number", "inservice_date",
              "created_by", "created_date", ]


class HeatdDetails(mixins.HeatdMixin, CommonDetails):
    fields = ["heat_id", "contdc_id", "det_value", "cdsc_id", "start_date", "end_date", "det_valid", "comments",
              "created_by", "created_date", ]


class ImgDetails(mixins.ImgMixin, CommonDetails):
    template_name = 'bio_diversity/details_img.html'
    fields = ["imgc_id", "loc_id", "cntd_id", "grpd_id", "sampd_id", "indvd_id", "spwnd_id", "tankd_id", "heatd_id",
              "draw_id", "trofd_id", "trayd_id", "cupd_id", "img_png", "comments", "created_by", "created_date", ]


class ImgcDetails(mixins.ImgcMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class IndvDetails(mixins.IndvMixin, CommonDetails):
    fields = ["grp_id", "spec_id", "stok_id", "coll_id", "indv_year", "ufid", "pit_tag", "indv_valid", "comments", "created_by",
              "created_date", ]

    def get_context_data(self, **kwargs):
        # use this to pass fields/sample object to template
        context = super().get_context_data(**kwargs)
        context["title"] = "Individual: {}".format(self.object.__str__())
        context["table_list"] = ["evnt", "indvd", "pair", "cont", "sire"]

        anix_set = self.object.animal_details.filter(pair_id__isnull=False)
        pair_list = list(dict.fromkeys([anix.pair_id for anix in anix_set]))
        pair_field_list = ["start_date", "indv_id", "prio_id"]
        obj_mixin = mixins.PairMixin
        context["pair_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                        "sub_model_key": obj_mixin.key,
                                        "objects_list": pair_list,
                                        "field_list": pair_field_list,
                                        "single_object": obj_mixin.model.objects.first()}

        anix_evnt_set = self.object.animal_details.filter(contx_id__isnull=True, loc_id__isnull=True,
                                                          indvt_id__isnull=True, pair_id__isnull=True)
        evnt_list = list(dict.fromkeys([anix.evnt_id for anix in anix_evnt_set]))
        evnt_field_list = ["evntc_id", "facic_id", "prog_id", "start_datetime"]
        obj_mixin = mixins.EvntMixin
        context["evnt_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                        "sub_model_key": obj_mixin.key,
                                        "objects_list": evnt_list,
                                        "field_list": evnt_field_list,
                                        "single_object": obj_mixin.model.objects.first()}

        indvd_set = list(dict.fromkeys([anix.individual_details.all() for anix in anix_evnt_set]))
        indvd_list = list(dict.fromkeys([indvd for qs in indvd_set for indvd in qs]))
        indvd_field_list = ["anidc_id", "adsc_id", "det_val", "indvd_valid", "detail_date"]
        obj_mixin = mixins.IndvdMixin
        context["indvd_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                        "sub_model_key": obj_mixin.key,
                                        "objects_list": indvd_list,
                                        "field_list": indvd_field_list,
                                        "single_object": obj_mixin.model.objects.first()}

        sire_list = [sire for sire in self.object.sires.all()]
        sire_field_list = ["prio_id", "pair_id", "choice"]
        obj_mixin = mixins.SireMixin
        context["sire_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                        "sub_model_key": obj_mixin.key,
                                        "objects_list": sire_list,
                                        "field_list": sire_field_list,
                                        "single_object": obj_mixin.model.objects.first()}

        anix_evnt_set = self.object.animal_details.filter(contx_id__isnull=False, loc_id__isnull=True,
                                                          indvt_id__isnull=True, pair_id__isnull=True)
        contx_tuple_set = list(dict.fromkeys([(anix.contx_id, anix.final_contx_flag) for anix in anix_evnt_set]))
        context["cont_evnt_list"] = [get_cont_evnt(contx) for contx in contx_tuple_set]
        context["cont_evnt_field_list"] = [
            "Evnt",
            "Date",
            "Direction"
            "Container",
        ]

        return context


class IndvdDetails(mixins.IndvdMixin, CommonDetails):
    fields = ["anidc_id",  "det_val", "adsc_id", "qual_id", "indvd_valid", "detail_date", "comments", "created_by", "created_date", ]


class IndvtDetails(mixins.IndvtMixin, CommonDetails):
    fields = ["indvtc_id", "lot_num", "dose", "unit_id", "start_date", "start_time", "end_date", "end_time",
              "comments", "created_by", "created_date", ]


class IndvtcDetails(mixins.IndvtcMixin, CommonDetails):
    fields = ["name", "nom", "rec_dose", "manufacturer", "description_en", "description_fr", "created_by",
              "created_date", ]


class InstDetails(mixins.InstMixin, CommonDetails):
    fields = ["instc_id", "serial_number", "comments", "created_by", "created_date", ]


class InstcDetails(mixins.InstcMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class InstdDetails(mixins.InstdMixin, CommonDetails):
    fields = ["inst_id", "instdc_id", "det_value", "start_date", "end_date", "valid", "comments", "created_by",
              "created_date", ]


class InstdcDetails(mixins.InstdcMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class LocDetails(mixins.LocMixin, CommonDetails):
    fields = ["evnt_id", "locc_id", "rive_id", "trib_id", "subr_id", "relc_id", "loc_lat", "loc_lon", "start_date",
              "start_time", "comments", "created_by", "created_date", ]

    def get_context_data(self, **kwargs):
        # use this to pass sire fields/sample object to template
        context = super().get_context_data(**kwargs)
        context["table_list"] = ["env", "cnt"]

        env_list = [env for env in self.object.env_condition.all()]
        env_field_list = ["envc_id", "env_val", "env_start", ]
        obj_mixin = mixins.EnvMixin
        context["env_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                        "sub_model_key": obj_mixin.key,
                                        "objects_list": env_list,
                                        "field_list": env_field_list,
                                        "single_object": obj_mixin.model.objects.first()}

        cnt_list = [cnt for cnt in self.object.counts.all()]
        cnt_field_list = ["cntc_id", "spec_id", "cnt", "est"]
        obj_mixin = mixins.CntMixin
        context["cnt_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                       "sub_model_key": obj_mixin.key,
                                       "objects_list": cnt_list,
                                       "field_list": cnt_field_list,
                                       "single_object": obj_mixin.model.objects.first()}

        return context


class LoccDetails(mixins.LoccMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class MatpDetails(mixins.MatpMixin, CommonDetails):
    template_name = 'bio_diversity/details_matp.html'
    fields = ["evnt_id", "matp_xls", "stok_id", "comments", "created_by", "created_date", ]


class OrgaDetails(mixins.OrgaMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class PairDetails(mixins.PairMixin, CommonDetails):
    fields = ["indv_id", "start_date", "end_date", "valid", "comments", "created_by", "created_date", ]

    def get_context_data(self, **kwargs):
        # use this to pass sire fields/sample object to template
        context = super().get_context_data(**kwargs)
        context["table_list"] = ["sire", "spwnd"]

        sire_list = [sire for sire in self.object.sires.all()]
        sire_field_list = ["indv_id", "prio_id", "choice"]
        obj_mixin = mixins.SireMixin
        context["sire_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                        "sub_model_key": obj_mixin.key,
                                        "objects_list": sire_list,
                                        "field_list": sire_field_list,
                                        "single_object": obj_mixin.model.objects.first()}

        context["spwnd_object"] = models.SpawnDet.objects.first()
        context["spwnd_field_list"] = [
            "spwndc_id",
            "det_val",
            "qual_id",
        ]

        spwnd_list = [spwnd for spwnd in self.object.spawning_details.all()]
        spwnd_field_list = ["spwndc_id", "det_val", "qual_id"]
        obj_mixin = mixins.SpwndMixin
        context["spwnd_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                         "sub_model_key": obj_mixin.key,
                                         "objects_list": spwnd_list,
                                         "field_list": spwnd_field_list,
                                         "single_object": obj_mixin.model.objects.first()}
        return context


class PercDetails(mixins.PercMixin, CommonDetails):
    fields = ["perc_first_name", "perc_last_name", "initials", "perc_valid", "created_by", "created_date", ]


class PrioDetails(mixins.PrioMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class ProgDetails(mixins.ProgMixin, CommonDetails):
    fields = ["prog_name", "prog_desc", "proga_id", "orga_id", "start_date", "end_date", "valid", "comments",
              "created_by", "created_date", ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table_list"] = ["prot"]
        prot_list = [prot for prot in self.object.protocols.all()]
        prot_field_list = ["protc_id", "start_date"]
        obj_mixin = mixins.ProtMixin
        context["prot_context_dict"] = {"div_title": "{} Details".format(obj_mixin.title),
                                        "sub_model_key": obj_mixin.key,
                                        "objects_list": prot_list,
                                        "field_list": prot_field_list,
                                        "single_object": obj_mixin.model.objects.first()}

        return context


class ProgaDetails(mixins.ProgaMixin, CommonDetails):
    fields = ["proga_last_name", "proga_first_name", "created_by", "created_date", ]


class ProtDetails(mixins.ProtMixin, CommonDetails):
    template_name = "bio_diversity/details_prot.html"
    fields = ["prog_id", "protc_id", "prot_desc", "facic_id", "evntc_id", "start_date", "end_date", "valid", "created_by",
              "created_date", ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["protf_object"] = models.Protofile.objects.first()
        context["protf_field_list"] = [
            "protf_pdf",
            "created_date",
        ]

        return context


class ProtcDetails(mixins.ProtcMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class ProtfDetails(mixins.ProtfMixin, CommonDetails):
    template_name = 'bio_diversity/details_protf.html'
    fields = ["prot_id", "protf_pdf", "comments", "created_by", "created_date", ]


class QualDetails(mixins.QualMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class RelcDetails(mixins.RelcMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class RiveDetails(mixins.RiveMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "rive_id", "trib_id", "subr_id", "min_lat", "max_lat",
              "min_lon", "max_lon", "created_by", "created_date", ]


class RoleDetails(mixins.RoleMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class SampDetails(mixins.SampMixin, CommonDetails):
    fields = ["loc_id", "samp_num", "spec_id", "sampc_id", "comments", "created_by", "created_date", ]


class SampcDetails(mixins.SampcMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class SampdDetails(mixins.SampdMixin, CommonDetails):
    fields = ["samp_id", "anidc_id",  "det_val", "adsc_id", "qual_id", "comments", "created_by", "created_date", ]


class SireDetails(mixins.SireMixin, CommonDetails):
    fields = ["prio_id", "pair_id",  "indv_id", "choice", "comments", "created_by", "created_date", ]


class SpwndDetails(mixins.SpwndMixin, CommonDetails):
    fields = ["pair_id", "spwndc_id", "det_val", "spwnsc_id", "qual_id", "comments", "created_by", "created_date", ]


class SpwndcDetails(mixins.SpwndcMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "min_val", "max_val", "unit_id", "spwn_subj_flag",
              "created_by", "created_date", ]


class SpwnscDetails(mixins.SpwnscMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "spwndc_id", "created_by", "created_date", ]


class SpecDetails(mixins.SpecMixin, CommonDetails):
    fields = ["name", "species", "com_name", "created_by", "created_date", ]


class StokDetails(mixins.StokMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class SubrDetails(mixins.SubrMixin, CommonDetails):
    fields = ["name", "nom", "rive_id", "trib_id", "description_en", "description_fr", "created_by", "created_date", ]


class TankDetails(mixins.TankMixin, CommonDetails):
    fields = ["facic_id", "name", "nom", "description_en", "description_fr", "created_by", "created_date", ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        env_list = [env for contx in self.object.contxs.all() for env in contx.env_condition.all()]
        env_field_list = ["envc_id", "envsc_id", "start_datetime", "env_val", ]
        obj_mixin = mixins.EnvMixin
        context["env_context_dict"] = {"div_title": "Environment Conditions",
                                       "sub_model_key": obj_mixin.key,
                                       "objects_list": env_list,
                                       "field_list": env_field_list,
                                       "single_object": obj_mixin.model.objects.first()}

        envt_list = [envt for contx in self.object.contxs.all() for envt in contx.env_treatment.all()]
        envt_field_list = ["envtc_id", "amt", "unit_id", "duration", ]
        obj_mixin = mixins.EnvtMixin
        context["envt_context_dict"] = {"div_title": "Container Treatments",
                                        "sub_model_key": obj_mixin.key,
                                        "objects_list": envt_list,
                                        "field_list": envt_field_list,
                                        "single_object": obj_mixin.model.objects.first()}

        indv_list, grp_list = self.object.fish_in_cont()
        indv_field_list = ["ufid", "pit_tag", "grp_id", ]
        obj_mixin = mixins.IndvMixin
        context["indv_context_dict"] = {"div_title": "Individuals in Container",
                                        "sub_model_key": obj_mixin.key,
                                        "objects_list": indv_list,
                                        "field_list": indv_field_list,
                                        "single_object": obj_mixin.model.objects.first()}

        grp_field_list = ["stok_id", "coll_id", "spec_id", ]
        obj_mixin = mixins.GrpMixin
        context["grp_context_dict"] = {"div_title": "Groups in Container",
                                       "sub_model_key": obj_mixin.key,
                                       "objects_list": grp_list,
                                       "field_list": grp_field_list,
                                       "single_object": obj_mixin.model.objects.first()}

        context["table_list"] = ["grp_cont", "indv_cont", "env", "envt"]

        return context


class TankdDetails(mixins.TankdMixin, CommonDetails):
    fields = ["tank_id", "contdc_id", "det_value", "cdsc_id", "start_date", "end_date", "det_valid", "comments",
              "created_by", "created_date", ]


class TeamDetails(mixins.TeamMixin, CommonDetails):
    fields = ["perc_id", "role_id", "created_by", "created_date", ]


class TrayDetails(mixins.TrayMixin, CommonDetails):
    fields = ["facic_id", "name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


class TraydDetails(mixins.TraydMixin, CommonDetails):
    fields = ["tray_id", "contdc_id", "det_value", "cdsc_id", "start_date", "end_date", "det_valid", "comments",
              "created_by", "created_date", ]


class TribDetails(mixins.TribMixin, CommonDetails):
    fields = ["name", "nom", "rive_id", "description_en", "description_fr", "created_by", "created_date", ]


class TrofDetails(mixins.TrofMixin, CommonDetails):

    fields = ["facic_id", "name", "nom", "description_en", "description_fr", "created_by", "created_date", ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table_list"] = ["grp_cont", "indv_cont", "env", "envt"]

        context = super().get_context_data(**kwargs)
        env_list = [env for contx in self.object.contxs.all() for env in contx.env_condition.all()]
        env_field_list = ["envc_id", "envsc_id", "start_datetime", "env_val", ]
        obj_mixin = mixins.EnvMixin
        context["env_context_dict"] = {"div_title": "Environment Conditions",
                                       "sub_model_key": obj_mixin.key,
                                       "objects_list": env_list,
                                       "field_list": env_field_list,
                                       "single_object": obj_mixin.model.objects.first()}

        envt_list = [envt for contx in self.object.contxs.all() for envt in contx.env_treatment.all()]
        envt_field_list = ["envtc_id", "amt", "unit_id", "duration", ]
        obj_mixin = mixins.EnvtMixin
        context["envt_context_dict"] = {"div_title": "Container Treatments",
                                        "sub_model_key": obj_mixin.key,
                                        "objects_list": envt_list,
                                        "field_list": envt_field_list,
                                        "single_object": obj_mixin.model.objects.first()}

        indv_list, grp_list = self.object.fish_in_cont()
        indv_field_list = ["ufid", "pit_tag", "grp_id", ]
        obj_mixin = mixins.IndvMixin
        context["indv_context_dict"] = {"div_title": "Individuals in Container",
                                        "sub_model_key": obj_mixin.key,
                                        "objects_list": indv_list,
                                        "field_list": indv_field_list,
                                        "single_object": obj_mixin.model.objects.first()}

        grp_field_list = ["stok_id", "coll_id", "spec_id", ]
        obj_mixin = mixins.GrpMixin
        context["grp_context_dict"] = {"div_title": "Groups in Container",
                                       "sub_model_key": obj_mixin.key,
                                       "objects_list": grp_list,
                                       "field_list": grp_field_list,
                                       "single_object": obj_mixin.model.objects.first()}


        return context


class TrofdDetails(mixins.TrofdMixin, CommonDetails):
    fields = ["trof_id", "contdc_id", "det_value", "cdsc_id", "start_date", "end_date", "det_valid", "comments",
              "created_by", "created_date", ]


class UnitDetails(mixins.UnitMixin, CommonDetails):
    fields = ["name", "nom", "description_en", "description_fr", "created_by", "created_date", ]


# ----------------------------LIST VIEWS-----------------------------
class CommonList(CommonAuthFilterView):

    nav_menu = 'bio_diversity/bio_diversity_nav.html'
    site_css = 'bio_diversity/bio_diversity.css'
    home_url_name = "bio_diversity:index"

    # fields to be used as columns to display an object in the filter view table
    fields = []

    # URL to use to create a new object to be added to the filter view
    create_url = None

    # URL to use for the details button element in the filter view's list
    details_url = None

    # URL to use for the update button element in the filter view's list
    update_url = None

    # URL to use for the delete button element in the filter view's list
    delete_url = False

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
        return self.create_url if self.create_url is not None else "bio_diversity:create_{}".format(self.key)

    def get_details_url(self):
        return self.details_url if self.details_url is not None else "bio_diversity:details_{}".format(self.key)

    def get_update_url(self):
        return self.update_url if self.update_url is not None else "bio_diversity:update_{}".format(self.key)

    def get_delete_url(self):
        return self.delete_url if self.delete_url is not None else "bio_diversity:delete_{}".format(self.key)

    def get_auth(self):
        if self.admin_only:
            return utils.bio_diverisity_admin(self.request.user)
        else:
            return utils.bio_diverisity_authorized(self.request.user)

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
        context['delete_url'] = self.get_delete_url()

        # for the most part if the user is authorized then the content is editable
        # but extending classes can choose to make content not editable even if the user is authorized
        context['auth'] = self.get_auth()
        context['editable'] = context['auth'] and self.editable

        if self.creation_form_height:
            context['height'] = self.creation_form_height

        return context


class AnidcList(mixins.AnidcMixin, CommonList):
    filterset_class = filters.AnidcFilter
    fields = ["name", "nom", ]


class AnixList(mixins.AnixMixin, CommonList):
    filterset_class = filters.AnixFilter
    fields = ["evnt_id", ]


class AdscList(mixins.AdscMixin, CommonList):
    filterset_class = filters.AdscFilter
    fields = ["name", "nom", ]


class CntList(mixins.CntMixin, CommonList):
    filterset_class = filters.CntFilter
    fields = ["loc_id", "spec_id", ]


class CntcList(mixins.CntcMixin, CommonList):
    filterset_class = filters.CntcFilter
    fields = ["name", "nom", ]


class CntdList(mixins.CntdMixin, CommonList):
    filterset_class = filters.CntdFilter
    fields = ["cnt_id", "anidc_id", "qual_id", ]


class CollList(mixins.CollMixin, CommonList):
    filterset_class = filters.CollFilter
    fields = ["name", "nom", ]


class ContdcList(mixins.ContdcMixin, CommonList):
    filterset_class = filters.ContdcFilter
    fields = ["name", "nom", "min_val", "max_val", ]


class ContxList(mixins.ContxMixin, CommonList):
    filterset_class = filters.ContxFilter
    fields = ["evnt_id", ]


class CdscList(mixins.CdscMixin, CommonList):
    filterset_class = filters.CdscFilter
    fields = ["contdc_id", "name", "nom", ]


class CupList(mixins.CupMixin, CommonList):
    filterset_class = filters.CupFilter
    fields = ["name", "nom", "facic_id", ]


class CupdList(mixins.CupdMixin, CommonList):
    filterset_class = filters.CupdFilter
    fields = ["cup_id", "contdc_id", "cdsc_id", "start_date", "end_date", ]


class DrawList(mixins.DrawMixin, CommonList):
    filterset_class = filters.DrawFilter
    fields = ["name", "nom", "facic_id",]


class EnvList(mixins.EnvMixin, CommonList):
    filterset_class = filters.EnvFilter
    fields = ["loc_id", "inst_id", "envc_id", ]


class EnvcList(mixins.EnvcMixin, CommonList):
    filterset_class = filters.EnvcFilter
    fields = ["name", "nom", ]


class EnvcfList(mixins.EnvcfMixin, CommonList):
    filterset_class = filters.EnvcfFilter
    fields = ["env_id", ]


class EnvscList(mixins.EnvscMixin, CommonList):
    filterset_class = filters.EnvscFilter
    fields = ["name", "nom", ]


class EnvtList(mixins.EnvtMixin, CommonList):
    filterset_class = filters.EnvtFilter
    fields = ["envtc_id", "lot_num", ]


class EnvtcList(mixins.EnvtcMixin, CommonList):
    filterset_class = filters.EnvtcFilter
    fields = ["name", "nom", "rec_dose", "manufacturer", ]


class EvntList(mixins.EvntMixin, CommonList):
    filterset_class = filters.EvntFilter
    fields = ["facic_id", "evntc_id", "perc_id", "prog_id", "team_id", ]


class EvntcList(mixins.EvntcMixin, CommonList):
    filterset_class = filters.EvntcFilter
    fields = ["name", "nom", ]


class FacicList(mixins.FacicMixin, CommonList):
    filterset_class = filters.FacicFilter
    fields = ["name", "nom", ]


class FecuList(mixins.FecuMixin, CommonList):
    filterset_class = filters.FecuFilter
    fields = ["stok_id", "coll_id", "alpha", "beta", ]


class FeedList(mixins.FeedMixin, CommonList):
    filterset_class = filters.FeedFilter
    fields = ["feedm_id", "feedc_id", ]


class FeedcList(mixins.FeedcMixin, CommonList):
    filterset_class = filters.FeedcFilter
    fields = ["name", "nom", ]


class FeedmList(mixins.FeedmMixin, CommonList):
    filterset_class = filters.FeedmFilter
    fields = ["name", "nom", ]


class GrpList(mixins.GrpMixin, CommonList):
    filterset_class = filters.GrpFilter
    fields = ["spec_id", "stok_id", "grp_year" ]


class GrpdList(mixins.GrpdMixin, CommonList):
    filterset_class = filters.GrpdFilter
    fields = ["anix_id", "anidc_id", ]


class HeatList(mixins.HeatMixin, CommonList):
    filterset_class = filters.HeatFilter
    fields = ["name", "nom",  "manufacturer", "serial_number", "inservice_date", ]


class HeatdList(mixins.HeatdMixin, CommonList):
    filterset_class = filters.HeatdFilter
    fields = ["heat_id", "contdc_id", "cdsc_id", "start_date", "end_date", ]


class ImgList(mixins.ImgMixin, CommonList):
    filterset_class = filters.ImgFilter
    fields = ["imgc_id", ]


class ImgcList(mixins.ImgcMixin, CommonList):
    filterset_class = filters.ImgcFilter
    fields = ["name", "nom", ]


class IndvList(mixins.IndvMixin, CommonList):
    filterset_class = filters.IndvFilter
    fields = ["pit_tag", "spec_id", "stok_id", "indv_year" ]
    delete_url = "bio_diversity:delete_indv"


class IndvdList(mixins.IndvdMixin, CommonList):
    filterset_class = filters.IndvdFilter
    fields = ["anix_id", "anidc_id", ]


class IndvtList(mixins.IndvtMixin, CommonList):
    filterset_class = filters.IndvtFilter
    fields = ["indvtc_id", "lot_num", ]


class IndvtcList(mixins.IndvtcMixin, CommonList):
    filterset_class = filters.IndvtcFilter
    fields = ["name", "nom", "rec_dose", "manufacturer", ]


class InstList(mixins.InstMixin, CommonList):
    filterset_class = filters.InstFilter
    fields = ["instc_id", "serial_number", "comments", ]


class InstcList(mixins.InstcMixin, CommonList):
    filterset_class = filters.InstcFilter
    fields = ["name", "nom", ]


class InstdList(mixins.InstdMixin, CommonList):
    filterset_class = filters.InstdFilter
    fields = ["inst_id", "instdc_id", ]


class InstdcList(mixins.InstdcMixin, CommonList):
    filterset_class = filters.InstdcFilter
    fields = ["name", "nom", ]


class LocList(mixins.LocMixin, CommonList):
    filterset_class = filters.LocFilter
    fields = ["evnt_id", "rive_id", "trib_id", "relc_id", "start_date", ]


class LoccList(mixins.LoccMixin, CommonList):
    filterset_class = filters.LoccFilter
    fields = ["name", "nom", ]


class MatpList(mixins.MatpMixin, CommonList):
    filterset_class = filters.MatpFilter
    fields = ["evnt_id", ]


class OrgaList(mixins.OrgaMixin, CommonList):
    filterset_class = filters.OrgaFilter
    fields = ["name", "nom", ]


class PairList(mixins.PairMixin, CommonList):
    filterset_class = filters.PairFilter
    fields = ["indv_id", ]


class PercList(mixins.PercMixin, CommonList):
    filterset_class = filters.PercFilter
    fields = ["perc_first_name", "perc_last_name", "perc_valid", ]


class PrioList(mixins.PrioMixin, CommonList):
    filterset_class = filters.PrioFilter
    fields = ["name", "nom", ]


class ProgList(mixins.ProgMixin, CommonList):
    filterset_class = filters.ProgFilter
    fields = ["prog_name", "proga_id", "orga_id", ]


class ProgaList(mixins.ProgaMixin, CommonList):
    filterset_class = filters.ProgaFilter
    fields = ["proga_last_name", "proga_first_name", ]


class ProtList(mixins.ProtMixin, CommonList):
    filterset_class = filters.ProtFilter
    fields = ["prog_id", "protc_id", "facic_id", ]


class ProtcList(mixins.ProtcMixin, CommonList):
    filterset_class = filters.ProtcFilter
    fields = ["name", "nom", ]


class ProtfList(mixins.ProtfMixin, CommonList):
    filterset_class = filters.ProtfFilter
    fields = ["prot_id", "comments", ]


class QualList(mixins.QualMixin, CommonList):
    filterset_class = filters.QualFilter
    fields = ["name", "nom", ]


class RelcList(mixins.RelcMixin, CommonList):
    filterset_class = filters.RelcFilter
    fields = ["name", "nom", ]


class RiveList(mixins.RiveMixin, CommonList):
    filterset_class = filters.RiveFilter
    fields = ["name", "nom", ]


class RoleList(mixins.RoleMixin, CommonList):
    filterset_class = filters.RoleFilter
    fields = ["name", "nom", ]


class SampList(mixins.SampMixin, CommonList):
    filterset_class = filters.SampFilter
    fields = ["loc_id", "samp_num", "spec_id", ]


class SampcList(mixins.SampcMixin, CommonList):
    filterset_class = filters.SampcFilter
    fields = ["name", "nom", ]


class SampdList(mixins.SampdMixin, CommonList):
    filterset_class = filters.SampdFilter
    fields = ["samp_id", "anidc_id", ]


class SireList(mixins.SireMixin, CommonList):
    filterset_class = filters.SireFilter
    fields = ["prio_id", "pair_id", ]


class SpwndList(mixins.SpwndMixin, CommonList):
    filterset_class = filters.SpwndFilter
    fields = ["pair_id", "spwndc_id", ]


class SpwndcList(mixins.SpwndcMixin, CommonList):
    filterset_class = filters.SpwndcFilter
    fields = ["name", "nom", ]


class SpwnscList(mixins.SpwnscMixin, CommonList):
    filterset_class = filters.SpwnscFilter
    fields = ["name", "nom", ]


class SpecList(mixins.SpecMixin, CommonList):
    filterset_class = filters.SpecFilter
    fields = ["name", "species", "com_name", ]


class StokList(mixins.StokMixin, CommonList):
    filterset_class = filters.StokFilter
    fields = ["name", "nom", ]


class SubrList(mixins.SubrMixin, CommonList):
    filterset_class = filters.SubrFilter
    fields = ["name", "nom", "rive_id", "trib_id", ]


class TankList(mixins.TankMixin, CommonList):
    filterset_class = filters.TankFilter
    fields = ["name", "nom", "facic_id", ]


class TankdList(mixins.TankdMixin, CommonList):
    filterset_class = filters.TankdFilter
    fields = ["tank_id", "contdc_id", "cdsc_id", "start_date", "end_date", ]


class TeamList(mixins.TeamMixin, CommonList):
    filterset_class = filters.TeamFilter
    fields = ["perc_id", "role_id", ]


class TrayList(mixins.TrayMixin, CommonList):
    filterset_class = filters.TrayFilter
    fields = ["name", "nom", "facic_id",]


class TraydList(mixins.TraydMixin, CommonList):
    filterset_class = filters.TraydFilter
    fields = ["tray_id", "contdc_id", "cdsc_id", "start_date", "end_date", ]


class TribList(mixins.TribMixin, CommonList):
    filterset_class = filters.TribFilter
    fields = ["name", "nom", "rive_id", ]


class TrofList(mixins.TrofMixin, CommonList):
    filterset_class = filters.TrofFilter
    fields = ["name", "nom", "facic_id",]


class TrofdList(mixins.TrofdMixin, CommonList):
    filterset_class = filters.TrofdFilter
    fields = ["trof_id", "contdc_id", "cdsc_id", "start_date", "end_date", ]


class UnitList(mixins.UnitMixin, CommonList):
    filterset_class = filters.UnitFilter
    fields = ["name", "nom", ]


# ---------------------------UPDATE VIEWS-----------------------------------
class CommonUpdate(CommonAuthUpdateView):

    nav_menu = 'bio_diversity/bio_diversity_nav.html'
    site_css = 'bio_diversity/bio_diversity.css'
    home_url_name = "bio_diversity:index"

    def get_success_url(self):
        success_url = self.success_url if self.success_url else reverse_lazy("bio_diversity:list_{}".format(self.key))

        if self.kwargs.get("pop"):
            # create views intended to be pop out windows should close the window upon success
            success_url = reverse_lazy("shared_models:close_me_no_refresh")

        return success_url

    def get_nav_menu(self):
        if self.kwargs.get("pop"):
            return None

        return self.nav_menu

    def get_initial(self):
        init = super().get_initial()
        # can uncomment this to auto update user on any update
        # init["created_by"] = self.request.user.username
        if hasattr(self.model, "start_datetime"):
            init["start_date"] = self.object.start_date
            init["start_time"] = self.object.start_time
        if hasattr(self.model, "end_datetime"):
            if self.object.end_datetime:
                init["end_date"] = self.object.end_date
                init["end_time"] = self.object.end_time
        return init

    # this function overrides UserPassesTestMixin.test_func() to determine if
    # the user should have access to this content, if the user is logged in
    # This function could be overridden in extending classes to preform further testing to see if
    # an object is editable
    def test_func(self):
        if self.admin_only:
            return utils.bio_diverisity_admin(self.request.user)
        else:
            return utils.bio_diverisity_authorized(self.request.user)

    # Get context returns elements used on the page. Make sure when extending to call
    # context = super().get_context_data(**kwargs) so that elements created in the parent
    # class are inherited by the extending class.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editable'] = context['auth']
        return context


class AnidcUpdate(mixins.AnidcMixin, CommonUpdate):
    pass


class AnixUpdate(mixins.AnixMixin, CommonUpdate):
    pass


class AdscUpdate(mixins.AdscMixin, CommonUpdate):
    pass


class CntUpdate(mixins.CntMixin, CommonUpdate):
    pass


class CntcUpdate(mixins.CntcMixin, CommonUpdate):
    pass


class CntdUpdate(mixins.CntdMixin, CommonUpdate):
    pass


class CollUpdate(mixins.CollMixin, CommonUpdate):
    pass


class ContdcUpdate(mixins.ContdcMixin, CommonUpdate):
    pass


class ContxUpdate(mixins.ContxMixin, CommonUpdate):
    pass


class CdscUpdate(mixins.CdscMixin, CommonUpdate):
    pass


class CupUpdate(mixins.CupMixin, CommonUpdate):
    pass


class CupdUpdate(mixins.CupdMixin, CommonUpdate):
    pass


class DrawUpdate(mixins.DrawMixin, CommonUpdate):
    pass


class EnvUpdate(mixins.EnvMixin, CommonUpdate):
    pass


class EnvcUpdate(mixins.EnvcMixin, CommonUpdate):
    pass


class EnvcfUpdate(mixins.EnvcfMixin, CommonUpdate):
    pass


class EnvscUpdate(mixins.EnvscMixin, CommonUpdate):
    pass


class EnvtUpdate(mixins.EnvtMixin, CommonUpdate):
    pass


class EnvtcUpdate(mixins.EnvtcMixin, CommonUpdate):
    pass


class EvntUpdate(mixins.EvntMixin, CommonUpdate):
    def get_success_url(self):
        success_url = self.success_url if self.success_url else reverse_lazy("bio_diversity:details_{}".format(self.key), kwargs = {'pk': self.object.pk})

        if self.kwargs.get("pop"):
            # create views intended to be pop out windows should close the window upon success
            success_url = reverse_lazy("shared_models:close_me_no_refresh")

        return success_url

    def get_initial(self):
        init = super().get_initial()
        # can uncomment this to auto update user on any update
        # init["created_by"] = self.request.user.username
        init["start_date"] = self.object.start_date
        init["start_time"] = self.object.start_time
        init["end_date"] = self.object.end_date
        init["end_time"] = self.object.end_time
        return init


class EvntcUpdate(mixins.EvntcMixin, CommonUpdate):
    pass


class FacicUpdate(mixins.FacicMixin, CommonUpdate):
    pass


class FecuUpdate(mixins.FecuMixin, CommonUpdate):
    pass


class FeedUpdate(mixins.FeedMixin, CommonUpdate):
    pass


class FeedcUpdate(mixins.FeedcMixin, CommonUpdate):
    pass


class FeedmUpdate(mixins.FeedmMixin, CommonUpdate):
    pass


class GrpUpdate(mixins.GrpMixin, CommonUpdate):
    pass


class GrpdUpdate(mixins.GrpdMixin, CommonUpdate):
    pass


class HeatUpdate(mixins.HeatMixin, CommonUpdate):
    pass


class HeatdUpdate(mixins.HeatdMixin, CommonUpdate):
    pass


class ImgUpdate(mixins.ImgMixin, CommonUpdate):
    pass


class ImgcUpdate(mixins.ImgcMixin, CommonUpdate):
    pass


class IndvUpdate(mixins.IndvMixin, CommonUpdate):
    pass


class IndvdUpdate(mixins.IndvdMixin, CommonUpdate):
    pass


class IndvtUpdate(mixins.IndvtMixin, CommonUpdate):
    pass


class IndvtcUpdate(mixins.IndvtcMixin, CommonUpdate):
    pass


class InstUpdate(mixins.InstMixin, CommonUpdate):
    pass


class InstcUpdate(mixins.InstcMixin, CommonUpdate):
    pass


class InstdUpdate(mixins.InstdMixin, CommonUpdate):
    pass


class InstdcUpdate(mixins.InstdcMixin, CommonUpdate):
    pass


class LocUpdate(mixins.LocMixin, CommonUpdate):
    def get_initial(self):
        init = super().get_initial()
        # can uncomment this to auto update user on any update
        # init["created_by"] = self.request.user.username
        init["start_date"] = self.object.start_date
        init["start_time"] = self.object.start_time
        return init


class LoccUpdate(mixins.LoccMixin, CommonUpdate):
    pass


class MatpUpdate(mixins.MatpMixin, CommonUpdate):
    pass


class OrgaUpdate(mixins.OrgaMixin, CommonUpdate):
    pass


class PairUpdate(mixins.PairMixin, CommonUpdate):
    pass


class PercUpdate(mixins.PercMixin, CommonUpdate):
    pass


class PrioUpdate(mixins.PrioMixin, CommonUpdate):
    pass


class ProgUpdate(mixins.ProgMixin, CommonUpdate):
    pass


class ProgaUpdate(mixins.ProgaMixin, CommonUpdate):
    pass


class ProtUpdate(mixins.ProtMixin, CommonUpdate):
    pass


class ProtcUpdate(mixins.ProtcMixin, CommonUpdate):
    pass


class ProtfUpdate(mixins.ProtfMixin, CommonUpdate):
    pass


class QualUpdate(mixins.QualMixin, CommonUpdate):
    pass


class RelcUpdate(mixins.RelcMixin, CommonUpdate):
    pass


class RiveUpdate(mixins.RiveMixin, CommonUpdate):
    pass


class RoleUpdate(mixins.RoleMixin, CommonUpdate):
    pass


class SampUpdate(mixins.SampMixin, CommonUpdate):
    pass


class SampcUpdate(mixins.SampcMixin, CommonUpdate):
    pass


class SampdUpdate(mixins.SampdMixin, CommonUpdate):
    pass


class SireUpdate(mixins.SireMixin, CommonUpdate):
    pass


class SpwndUpdate(mixins.SpwndMixin, CommonUpdate):
    pass


class SpwndcUpdate(mixins.SpwndcMixin, CommonUpdate):
    pass


class SpwnscUpdate(mixins.SpwnscMixin, CommonUpdate):
    pass


class SpecUpdate(mixins.SpecMixin, CommonUpdate):
    pass


class StokUpdate(mixins.StokMixin, CommonUpdate):
    pass


class SubrUpdate(mixins.SubrMixin, CommonUpdate):
    pass


class TankUpdate(mixins.TankMixin, CommonUpdate):
    pass


class TankdUpdate(mixins.TankdMixin, CommonUpdate):
    pass


class TeamUpdate(mixins.TeamMixin, CommonUpdate):
    pass


class TrayUpdate(mixins.TrayMixin, CommonUpdate):
    pass


class TraydUpdate(mixins.TraydMixin, CommonUpdate):
    pass


class TribUpdate(mixins.TribMixin, CommonUpdate):
    pass


class TrofUpdate(mixins.TrofMixin, CommonUpdate):
    pass


class TrofdUpdate(mixins.TrofdMixin, CommonUpdate):
    pass


class UnitUpdate(mixins.UnitMixin, CommonUpdate):
    pass


class CommonLog(CommonTemplateView):
    success_url = reverse_lazy("shared_models:close_me")
    template_name = 'bio_diversity/bio_log.html'
    title = "Data Log"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        log_data = self.request.session.get("log_data")
        context['log_data'] = log_data
        context["load_success"] = self.request.session.get("load_success")

        return context

    def test_func(self):
        return utils.bio_diverisity_authorized(self.request.user)


class DataLog(CommonLog):
    pass


def indv_delete(request, pk):
    indv = models.Individual.objects.get(pk=pk)
    if utils.bio_diverisity_admin(request.user):
        indv.delete()
        messages.success(request, _("The Individual has been successfully deleted."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(reverse_lazy('accounts:denied_access'))


class CommonDelete(UserPassesTestMixin, DeleteView):
    success_url = reverse_lazy("shared_models:close_me")
    template_name = 'bio_diversity/delete_confirm.html'
    success_message = 'The dataset was successfully deleted!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title_msg'] = _("Are you sure you want to delete the following from the database?")
        context['confirm_msg'] = _("You will not be able to recover this object.")

        return context

    def test_func(self):
        return utils.bio_diverisity_admin(self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class IndvDelete(mixins.IndvMixin, CommonDelete):
    success_url = reverse_lazy("bio_diversity:list_indv")


class CommentKeywordsFormsetView(UserPassesTestMixin, CommonFormsetView):
    template_name = 'bio_diversity/formset.html'
    title = _("Bio Diversity Comment Keywords")
    h1 = _("Manage Comment Keywords")
    queryset = models.CommentKeywords.objects.all()
    formset_class = CommentKeywordsFormset
    success_url_name = "bio_diversity:manage_comment_keywords"
    home_url_name = "bio_diversity:index"
    delete_url_name = "bio_diversity:delete_comment_keywords"

    def test_func(self):
        return utils.bio_diverisity_admin(self.request.user)


class CommentKeywordsHardDeleteView(UserPassesTestMixin, CommonHardDeleteView):
    model = models.CommentKeywords
    success_url = reverse_lazy("bio_diversity:manage_comment_keywords")

    def test_func(self):
        return utils.bio_diverisity_admin(self.request.user)


class HelpTextFormsetView(UserPassesTestMixin, CommonFormsetView):
    template_name = 'bio_diversity/formset.html'
    title = _("Bio Diversity Help Text")
    h1 = _("Manage Help Texts")
    queryset = models.HelpText.objects.all()
    formset_class = HelpTextFormset
    success_url_name = "bio_diversity:manage_help_texts"
    home_url_name = "bio_diversity:index"
    delete_url_name = "bio_diversity:delete_help_text"

    def test_func(self):
        return utils.bio_diverisity_admin(self.request.user)


class HelpTextHardDeleteView(UserPassesTestMixin, CommonHardDeleteView):
    model = models.HelpText
    success_url = reverse_lazy("bio_diversity:manage_help_texts")

    def test_func(self):
        return utils.bio_diverisity_admin(self.request.user)
