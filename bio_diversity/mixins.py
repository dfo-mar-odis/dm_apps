from . import models
# from shared_models import models as shared_models

from . import forms
from django.utils.translation import gettext_lazy as _


class AnidcMixin:
    key = "anidc"
    form_class = forms.AnidcForm
    model = models.AnimalDetCode
    title = _("Animal Detail Code")
    admin_only = True


class AnixMixin:
    key = "anix"
    form_class = forms.AnixForm
    model = models.AniDetailXref
    title = _("Animal Detail Cross Reference")
    admin_only = False


class AdscMixin:
    key = "adsc"
    form_class = forms.AdscForm
    model = models.AniDetSubjCode
    title = _("Animal Detail Subjective Code")
    admin_only = True


class CntMixin:
    key = "cnt"
    form_class = forms.CntForm
    model = models.Count
    title = _("Count")
    admin_only = False


class CntcMixin:
    key = "cntc"
    form_class = forms.CntcForm
    model = models.CountCode
    title = _("Count Code")
    admin_only = True


class CntdMixin:
    key = "cntd"
    form_class = forms.CntdForm
    model = models.CountDet
    title = _("Count Detail")
    admin_only = False
    img = True


class CollMixin:
    key = "coll"
    form_class = forms.CollForm
    model = models.Collection
    title = _("Collection")
    admin_only = False


class ContdcMixin:
    key = "contdc"
    form_class = forms.ContdcForm
    model = models.ContainerDetCode
    title = _("Container Detail Code")
    admin_only = True


class ContxMixin:
    key = "contx"
    form_class = forms.ContxForm
    model = models.ContainerXRef
    title = _("Container Cross Reference")
    admin_only = False


class CdscMixin:
    key = "cdsc"
    form_class = forms.CdscForm
    model = models.ContDetSubjCode
    title = _("Container Detail Subjective Code")
    admin_only = True


class CupMixin:
    key = "cup"
    form_class = forms.CupForm
    model = models.Cup
    title = _("Cup")
    admin_only = False


class CupdMixin:
    key = "cupd"
    form_class = forms.CupdForm
    model = models.CupDet
    title = _("Cup Detail")
    admin_only = False
    img = True


class DataMixin:
    key = "data"
    form_class = forms.DataForm
    model = models.DataLoader
    title = _("Data")
    admin_only = False


class DrawMixin:
    key = "draw"
    form_class = forms.DrawForm
    model = models.Drawer
    title = _("Drawer")
    admin_only = False


class EnvcMixin:
    key = "envc"
    form_class = forms.EnvcForm
    model = models.EnvCode
    title = _("Environment Code")
    admin_only = True


class EnvMixin:
    key = "env"
    form_class = forms.EnvForm
    model = models.EnvCondition
    title = _("Environment Condition")
    admin_only = False


class EnvcfMixin:
    key = "envcf"
    form_class = forms.EnvcfForm
    model = models.EnvCondFile
    title = _("Environment Condition File")
    admin_only = True


class EnvscMixin:
    key = "envsc"
    form_class = forms.EnvscForm
    model = models.EnvSubjCode
    title = _("Environment Subjective Code")
    admin_only = True


class EnvtMixin:
    key = "envt"
    form_class = forms.EnvtForm
    model = models.EnvTreatment
    title = _("Environment Treatment")
    admin_only = False


class EnvtcMixin:
    key = "envtc"
    form_class = forms.EnvtcForm
    model = models.EnvTreatCode
    title = _("Environment Treatment Code")
    admin_only = True


class EvntMixin:
    key = "evnt"
    form_class = forms.EvntForm
    model = models.Event
    title = _("Event")
    admin_only = False


class EvntcMixin:
    key = "evntc"
    form_class = forms.EvntcForm
    model = models.EventCode
    title = _("Event Code")
    admin_only = True


class EvntfMixin:
    key = "evntf"
    form_class = forms.EvntfForm
    model = models.EventFile
    title = _("Event Files")
    admin_only = False


class EvntfcMixin:
    key = "evntfc"
    form_class = forms.EvntfcForm
    model = models.EventFileCode
    title = _("Event File Code")
    admin_only = True


class FacicMixin:
    key = "facic"
    form_class = forms.FacicForm
    model = models.FacilityCode
    title = _("Facility Code")
    admin_only = True


class FecuMixin:
    key = "fecu"
    form_class = forms.FecuForm
    model = models.Fecundity
    title = _("Fecundity")
    admin_only = False


class FeedMixin:
    key = "feed"
    form_class = forms.FeedForm
    model = models.Feeding
    title = _("Feeding")
    admin_only = False


class FeedcMixin:
    key = "feedc"
    form_class = forms.FeedcForm
    model = models.FeedCode
    title = _("Feeding Code")
    admin_only = True


class FeedmMixin:
    key = "feedm"
    form_class = forms.FeedmForm
    model = models.FeedMethod
    title = _("Feeding Method")
    admin_only = False


class GrpMixin:
    key = "grp"
    form_class = forms.GrpForm
    model = models.Group
    title = _("Group")
    admin_only = False


class GrpdMixin:
    key = "grpd"
    form_class = forms.GrpdForm
    model = models.GroupDet
    title = _("Group Detail")
    admin_only = False
    img = True


class HeatMixin:
    key = "heat"
    form_class = forms.HeatForm
    model = models.HeathUnit
    title = _("Heath Unit")
    admin_only = False


class HeatdMixin:
    key = "heatd"
    form_class = forms.HeatdForm
    model = models.HeathUnitDet
    title = _("Heath Unit Detail")
    admin_only = False
    img = True


class ImgMixin:
    key = "img"
    form_class = forms.ImgForm
    model = models.Image
    title = _("Image")
    admin_only = False


class ImgcMixin:
    key = "imgc"
    form_class = forms.ImgcForm
    model = models.ImageCode
    title = _("Image Code")
    admin_only = True


class IndvMixin:
    key = "indv"
    form_class = forms.IndvForm
    model = models.Individual
    title = _("Individual")
    admin_only = False


class IndvdMixin:
    key = "indvd"
    form_class = forms.IndvdForm
    model = models.IndividualDet
    title = _("Individual Detail")
    admin_only = False
    img = True


class IndvtMixin:
    key = "indvt"
    form_class = forms.IndvtForm
    model = models.IndTreatment
    title = _("Individual Treatment")
    admin_only = False


class IndvtcMixin:
    key = "indvtc"
    form_class = forms.IndvtcForm
    model = models.IndTreatCode
    title = _("Individual Treatment Code")
    admin_only = True


class InstMixin:
    key = "inst"
    form_class = forms.InstForm
    model = models.Instrument
    title = _("Instrument")
    admin_only = False


class InstcMixin:
    key = "instc"
    form_class = forms.InstcForm
    model = models.InstrumentCode
    title = _("Instrument Code")
    admin_only = True


class InstdMixin:
    key = "instd"
    form_class = forms.InstdForm
    model = models.InstrumentDet
    title = _("Instrument Detail")
    admin_only = False


class InstdcMixin:
    key = 'instdc'
    model = models.InstDetCode
    form_class = forms.InstdcForm
    title = _("Instrument Detail Code")
    admin_only = True


class LocMixin:
    key = 'loc'
    model = models.Location
    form_class = forms.LocForm
    title = _("Location")
    admin_only = False
    img = True


class LoccMixin:
    key = 'locc'
    model = models.LocCode
    form_class = forms.LoccForm
    title = _("Location Code")
    admin_only = True


class MortMixin:
    key = "mort"
    form_class = forms.MortForm
    title = _("Mortality")
    admin_only = False


class OrgaMixin:
    key = 'orga'
    model = models.Organization
    form_class = forms.OrgaForm
    title = _("Organization")
    admin_only = True


class PairMixin:
    key = 'pair'
    model = models.Pairing
    form_class = forms.PairForm
    title = _("Pairing")
    admin_only = False

class PercMixin:
    key = 'perc'
    model = models.PersonnelCode
    form_class = forms.PercForm
    title = _("Personnel Code")
    admin_only = True


class PrioMixin:
    key = 'prio'
    model = models.PriorityCode
    form_class = forms.PrioForm
    title = _("Priority Code")
    admin_only = True


class ProgMixin:
    key = 'prog'
    model = models.Program
    form_class = forms.ProgForm
    title = _("Program")
    admin_only = False


class ProgaMixin:
    key = 'proga'
    model = models.ProgAuthority
    form_class = forms.ProgaForm
    title = _("Program Authority")
    admin_only = False


class ProtMixin:
    key = 'prot'
    model = models.Protocol
    form_class = forms.ProtForm
    title = _("Protocol")
    admin_only = False


class ProtcMixin:
    key = 'protc'
    model = models.ProtoCode
    form_class = forms.ProtcForm
    title = _("Protocol Code")
    admin_only = True


class ProtfMixin:
    key = 'protf'
    model = models.Protofile
    form_class = forms.ProtfForm
    title = _("Protocol File")
    admin_only = False


class QualMixin:
    key = 'qual'
    model = models.QualCode
    form_class = forms.QualForm
    title = _("Quality Code")
    admin_only = True


class RelcMixin:
    key = 'relc'
    model = models.ReleaseSiteCode
    form_class = forms.RelcForm
    title = _("Site Code")
    admin_only = True


class ReportMixin:
    key = 'repr'
    form_class = forms.ReportForm
    title = _("Reports")
    admin_only = False


class RiveMixin:
    key = 'rive'
    model = models.RiverCode
    form_class = forms.RiveForm
    title = _("River Code")
    admin_only = True


class RoleMixin:
    key = 'role'
    model = models.RoleCode
    form_class = forms.RoleForm
    title = _("Role Code")
    admin_only = True


class SampMixin:
    key = 'samp'
    model = models.Sample
    form_class = forms.SampForm
    title = _("Sample ")
    admin_only = False


class SampcMixin:
    key = 'sampc'
    model = models.SampleCode
    form_class = forms.SampcForm
    title = _("Sample Code")
    admin_only = True


class SampdMixin:
    key = 'sampd'
    model = models.SampleDet
    form_class = forms.SampdForm
    title = _("Sample Detail")
    admin_only = False
    img = True


class SireMixin:
    key = 'sire'
    model = models.Sire
    form_class = forms.SireForm
    title = _("Sire")
    admin_only = False


class SpwndMixin:
    key = 'spwnd'
    model = models.SpawnDet
    form_class = forms.SpwndForm
    title = _("Spawning Detail")
    admin_only = False
    img = True


class SpwndcMixin:
    key = 'spwndc'
    model = models.SpawnDetCode
    form_class = forms.SpwndcForm
    title = _("Spawn Detail Code")
    admin_only = True


class SpwnscMixin:
    key = 'spwnsc'
    model = models.SpawnDetSubjCode
    form_class = forms.SpwnscForm
    title = _("Spawn Detail Subjective Code")
    admin_only = True


class SpecMixin:
    key = 'spec'
    model = models.SpeciesCode
    form_class = forms.SpecForm
    title = _("Species Code")
    admin_only = True


class StokMixin:
    key = 'stok'
    model = models.StockCode
    form_class = forms.StokForm
    title = _("Stock Code")
    admin_only = True


class SubrMixin:
    key = 'subr'
    model = models.SubRiverCode
    form_class = forms.SubrForm
    title = _("Sub river Code")
    admin_only = True


class TankMixin:
    key = 'tank'
    model = models.Tank
    form_class = forms.TankForm
    title = _("Tank")
    admin_only = False


class TankdMixin:
    key = 'tankd'
    model = models.TankDet
    form_class = forms.TankdForm
    title = _("Tank Detail")
    admin_only = False
    img = True


class TeamMixin:
    key = 'team'
    model = models.Team
    form_class = forms.TeamForm
    title = _("Team")
    admin_only = False


class TrayMixin:
    key = 'tray'
    model = models.Tray
    form_class = forms.TrayForm
    title = _("Tray")
    admin_only = False


class TraydMixin:
    key = 'trayd'
    model = models.TrayDet
    form_class = forms.TraydForm
    title = _("Tray Detail")
    admin_only = False
    img = True


class TribMixin:
    key = 'trib'
    model = models.Tributary
    form_class = forms.TribForm
    title = _("Tributary")
    admin_only = True


class TrofMixin:
    key = 'trof'
    model = models.Trough
    form_class = forms.TrofForm
    title = _("Trough")
    admin_only = False


class TrofdMixin:
    key = 'trofd'
    model = models.TroughDet
    form_class = forms.TrofdForm
    title = _("Trough Detail")
    admin_only = False
    img = True


class UnitMixin:
    key = 'unit'
    model = models.UnitCode
    form_class = forms.UnitForm
    title = _("Unit")
    admin_only = True
