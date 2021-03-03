import django_filters

from . import models


class AnidcFilter(django_filters.FilterSet):

    class Meta:
        model = models.AnimalDetCode
        fields = ["name", "nom", ]


class AnixFilter(django_filters.FilterSet):

    class Meta:
        model = models.AniDetailXref
        fields = ["evnt_id", ]


class AdscFilter(django_filters.FilterSet):

    class Meta:
        model = models.AniDetSubjCode
        fields = ["name", "nom", ]


class CntFilter(django_filters.FilterSet):

    class Meta:
        model = models.Count
        fields = ["loc_id", "contx_id", "spec_id", ]


class CntcFilter(django_filters.FilterSet):

    class Meta:
        model = models.CountCode
        fields = ["name", "nom", ]


class CntdFilter(django_filters.FilterSet):

    class Meta:
        model = models.CountDet
        fields = ["cnt_id", "anidc_id", "qual_id", ]


class CollFilter(django_filters.FilterSet):

    class Meta:
        model = models.Collection
        fields = ["name", "nom", ]


class ContdcFilter(django_filters.FilterSet):

    class Meta:
        model = models.ContainerDetCode
        fields = ["name", "nom", "min_val", "max_val", ]


class ContxFilter(django_filters.FilterSet):

    class Meta:
        model = models.ContainerXRef
        fields = ["evnt_id", ]


class CdscFilter(django_filters.FilterSet):

    class Meta:
        model = models.ContDetSubjCode
        fields = ["name", "nom", ]


class CupFilter(django_filters.FilterSet):

    class Meta:
        model = models.Cup
        fields = ["name", "nom", "facic_id", ]


class CupdFilter(django_filters.FilterSet):

    class Meta:
        model = models.CupDet
        fields = ["cup_id", "contdc_id", "cdsc_id", "start_date", "end_date", ]


class DrawFilter(django_filters.FilterSet):

    class Meta:
        model = models.Drawer
        fields = ["name", "nom", "facic_id", ]


class EnvFilter(django_filters.FilterSet):

    class Meta:
        model = models.EnvCondition
        fields = ["contx_id", "loc_id", "inst_id", "envc_id", ]


class EnvcFilter(django_filters.FilterSet):

    class Meta:
        model = models.EnvCode
        fields = ["name", "nom", ]


class EnvcfFilter(django_filters.FilterSet):

    class Meta:
        model = models.EnvCondFile
        fields = ["env_id", ]


class EnvscFilter(django_filters.FilterSet):

    class Meta:
        model = models.EnvSubjCode
        fields = ["name", "nom", "envc_id", ]


class EnvtFilter(django_filters.FilterSet):

    class Meta:
        model = models.EnvTreatment
        fields = ["contx_id", "envtc_id", "lot_num", ]


class EnvtcFilter(django_filters.FilterSet):

    class Meta:
        model = models.EnvTreatCode
        fields = ["name", "nom", "rec_dose", "manufacturer", ]


class EvntFilter(django_filters.FilterSet):

    class Meta:
        model = models.Event
        fields = ["facic_id", "evntc_id", "perc_id", "prog_id", "team_id", ]


class EvntcFilter(django_filters.FilterSet):

    class Meta:
        model = models.EventCode
        fields = ["name", "nom", "description_en", "description_fr", ]


class FacicFilter(django_filters.FilterSet):

    class Meta:
        model = models.FacilityCode
        fields = ["name", "nom", "description_en", "description_fr", ]


class FecuFilter(django_filters.FilterSet):

    class Meta:
        model = models.Fecundity
        fields = ["stok_id", "coll_id", "alpha", "beta", ]


class FeedFilter(django_filters.FilterSet):

    class Meta:
        model = models.Feeding
        fields = ["contx_id", "feedm_id", "feedc_id", ]


class FeedcFilter(django_filters.FilterSet):

    class Meta:
        model = models.FeedCode
        fields = ["name", "nom", "manufacturer", "description_en", "description_fr", ]


class FeedmFilter(django_filters.FilterSet):

    class Meta:
        model = models.FeedMethod
        fields = ["name", "nom", "description_en", "description_fr", ]


class GrpFilter(django_filters.FilterSet):

    class Meta:
        model = models.Group
        fields = ["spec_id", "stok_id", "grp_year", ]


class GrpdFilter(django_filters.FilterSet):

    class Meta:
        model = models.GroupDet
        fields = ["anix_id", "anidc_id", ]


class HeatFilter(django_filters.FilterSet):

    class Meta:
        model = models.HeathUnit
        fields = ["name", "nom", "facic_id", "manufacturer", "serial_number", "inservice_date",
                  ]


class HeatdFilter(django_filters.FilterSet):

    class Meta:
        model = models.HeathUnitDet
        fields = ["heat_id", "contdc_id", "cdsc_id", "start_date", "end_date", ]


class ImgFilter(django_filters.FilterSet):

    class Meta:
        model = models.Image
        fields = ["imgc_id", ]


class ImgcFilter(django_filters.FilterSet):

    class Meta:
        model = models.ImageCode
        fields = ["name", "nom", ]


class IndvFilter(django_filters.FilterSet):

    ufid = django_filters.CharFilter(field_name='ufid', lookup_expr='icontains')

    class Meta:
        model = models.Individual
        fields = ["ufid", "spec_id", "stok_id", "indv_year", ]


class IndvdFilter(django_filters.FilterSet):

    class Meta:
        model = models.IndividualDet
        fields = ["anix_id", "anidc_id", ]


class IndvtFilter(django_filters.FilterSet):

    class Meta:
        model = models.IndTreatment
        fields = ["indvtc_id", "lot_num", ]


class IndvtcFilter(django_filters.FilterSet):

    class Meta:
        model = models.IndTreatCode
        fields = ["name", "nom", "rec_dose", "manufacturer", ]


class InstFilter(django_filters.FilterSet):

    class Meta:
        model = models.Instrument
        fields = ["instc_id", "serial_number", ]


class InstcFilter(django_filters.FilterSet):

    class Meta:
        model = models.InstrumentCode
        fields = ["name", "nom", ]


class InstdFilter(django_filters.FilterSet):

    class Meta:
        model = models.InstrumentDet
        fields = ["inst_id", "instdc_id", "valid", ]


class InstdcFilter(django_filters.FilterSet):

    class Meta:
        model = models.InstDetCode
        fields = ["name", "nom", ]


class LocFilter(django_filters.FilterSet):

    class Meta:
        model = models.Location
        fields = ["evnt_id", "rive_id", "trib_id", "relc_id", ]


class LoccFilter(django_filters.FilterSet):

    class Meta:
        model = models.LocCode
        fields = ["name", "nom", ]


class MatpFilter(django_filters.FilterSet):

    class Meta:
        model = models.MatingPlan
        fields = ["evnt_id", ]


class OrgaFilter(django_filters.FilterSet):

    class Meta:
        model = models.Organization
        fields = ["name", "nom", ]


class PairFilter(django_filters.FilterSet):

    class Meta:
        model = models.Pairing
        fields = ["indv_id", ]


class PercFilter(django_filters.FilterSet):

    class Meta:
        model = models.PersonnelCode
        fields = ["perc_first_name", "perc_last_name", "perc_valid", ]


class PrioFilter(django_filters.FilterSet):

    class Meta:
        model = models.PriorityCode
        fields = ["name", "nom", ]


class ProgFilter(django_filters.FilterSet):

    prog_name = django_filters.CharFilter(field_name='prog_name', lookup_expr='icontains')

    class Meta:
        model = models.Program
        fields = ["prog_name", "proga_id", "orga_id", ]


class ProgaFilter(django_filters.FilterSet):

    class Meta:
        model = models.ProgAuthority
        fields = ["proga_last_name", "proga_first_name", ]


class ProtFilter(django_filters.FilterSet):

    class Meta:
        model = models.Protocol
        fields = ["prog_id", "protc_id", "facic_id",]


class ProtcFilter(django_filters.FilterSet):

    class Meta:
        model = models.ProtoCode
        fields = ["name", "nom", ]


class ProtfFilter(django_filters.FilterSet):

    class Meta:
        model = models.Protofile
        fields = ["prot_id", ]


class QualFilter(django_filters.FilterSet):

    class Meta:
        model = models.QualCode
        fields = ["name", "nom", ]


class RelcFilter(django_filters.FilterSet):

    class Meta:
        model = models.ReleaseSiteCode
        fields = ["rive_id", "trib_id", "name", "nom", ]


class RiveFilter(django_filters.FilterSet):

    class Meta:
        model = models.RiverCode
        fields = ["name", "nom", ]


class RoleFilter(django_filters.FilterSet):

    class Meta:
        model = models.RoleCode
        fields = ["name", "nom", ]


class SampFilter(django_filters.FilterSet):

    class Meta:
        model = models.Sample
        fields = ["loc_id", "samp_num",  "spec_id", ]


class SampcFilter(django_filters.FilterSet):

    class Meta:
        model = models.SampleCode
        fields = ["name", "nom", ]


class SampdFilter(django_filters.FilterSet):

    class Meta:
        model = models.SampleDet
        fields = ["samp_id", "anidc_id", ]


class SireFilter(django_filters.FilterSet):

    class Meta:
        model = models.Sire
        fields = ["prio_id", "pair_id", ]


class SpwndFilter(django_filters.FilterSet):

    class Meta:
        model = models.SpawnDet
        fields = ["spwndc_id", "pair_id", ]


class SpwndcFilter(django_filters.FilterSet):

    class Meta:
        model = models.SpawnDetCode
        fields = ["name", "nom", ]


class SpwnscFilter(django_filters.FilterSet):

    class Meta:
        model = models.SpawnDetSubjCode
        fields = ["name", "nom", ]


class SpecFilter(django_filters.FilterSet):

    class Meta:
        model = models.SpeciesCode
        fields = ["name", "species", "com_name", ]


class StokFilter(django_filters.FilterSet):

    class Meta:
        model = models.StockCode
        fields = ["name", "nom", ]


class SubrFilter(django_filters.FilterSet):

    class Meta:
        model = models.SubRiverCode
        fields = ["name", "nom", "rive_id", "trib_id",  "created_by",
                  "created_date", ]


class TankFilter(django_filters.FilterSet):

    class Meta:
        model = models.Tank
        fields = ["name", "nom", "facic_id", ]


class TankdFilter(django_filters.FilterSet):

    class Meta:
        model = models.TankDet
        fields = ["tank_id", "contdc_id", "cdsc_id", "start_date", "end_date", ]


class TeamFilter(django_filters.FilterSet):

    class Meta:
        model = models.Team
        fields = ["perc_id", "role_id", ]


class TrayFilter(django_filters.FilterSet):

    class Meta:
        model = models.Tray
        fields = ["name", "nom", "facic_id",]


class TraydFilter(django_filters.FilterSet):

    class Meta:
        model = models.TrayDet
        fields = ["tray_id", "contdc_id", "cdsc_id", "start_date", "end_date", ]


class TribFilter(django_filters.FilterSet):

    class Meta:
        model = models.Tributary
        fields = ["name", "nom", "rive_id", ]


class TrofFilter(django_filters.FilterSet):

    class Meta:
        model = models.Trough
        fields = ["name", "nom", "facic_id",]


class TrofdFilter(django_filters.FilterSet):

    class Meta:
        model = models.TroughDet
        fields = ["trof_id", "contdc_id", "cdsc_id", "start_date", "end_date", ]


class UnitFilter(django_filters.FilterSet):

    class Meta:
        model = models.UnitCode
        fields = ["name", "nom", ]
