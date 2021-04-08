import uuid

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import default_if_none
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from shared_models.utils import get_metadata_string


class UnilingualSimpleLookup(models.Model):
    class Meta:
        abstract = True
        ordering = ["name", ]

    name = models.CharField(unique=True, max_length=255, verbose_name=_("name"))

    def __str__(self):
        return self.name


class SimpleLookup(models.Model):
    class Meta:
        abstract = True
        ordering = [_("name"), ]

    name = models.CharField(unique=True, max_length=255, verbose_name=_("name (en)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("name (fr)"))

    @property
    def tname(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            my_str = "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            my_str = self.name
        return my_str

    def __str__(self):
        return self.tname


class SimpleLookupWithUUID(SimpleLookup):
    class Meta:
        abstract = True

    uuid = models.UUIDField(editable=False, unique=True, blank=True, null=True, default=uuid.uuid4)


class Lookup(SimpleLookup):
    class Meta:
        abstract = True

    description_en = models.TextField(blank=True, null=True, verbose_name=_("Description (en)"))
    description_fr = models.TextField(blank=True, null=True, verbose_name=_("Description (fr)"))

    @property
    def tdescription(self):
        # check to see if a french value is given
        if getattr(self, str(_("description_en"))):
            my_str = "{}".format(getattr(self, str(_("description_en"))))
        # if there is no translated term, just pull from the english field
        else:
            my_str = self.description_en
        return my_str


class UnilingualLookup(UnilingualSimpleLookup):
    class Meta:
        abstract = True

    description_en = models.TextField(blank=True, null=True, verbose_name=_("Description (en)"))
    description_fr = models.TextField(blank=True, null=True, verbose_name=_("Description (fr)"))

    @property
    def tdescription(self):
        # check to see if a french value is given
        if getattr(self, str(_("description_en"))):
            my_str = "{}".format(getattr(self, str(_("description_en"))))
        # if there is no translated term, just pull from the english field
        else:
            my_str = self.description_en
        return my_str


class HelpTextLookup(models.Model):
    field_name = models.CharField(max_length=255)
    eng_text = models.TextField(verbose_name=_("English text"))
    fra_text = models.TextField(blank=True, null=True, verbose_name=_("French text"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("eng_text"))):
            return "{}".format(getattr(self, str(_("eng_text"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.eng_text)

    class Meta:
        ordering = ['field_name', ]
        abstract = True


class MetadataFields(models.Model):
    # metadata
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, editable=False, related_name='%(class)s_created_by')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, editable=False, related_name='%(class)s_updated_by')
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True

    @property
    def metadata(self):
        return get_metadata_string(
            self.created_at,
            self.created_by,
            self.updated_at,
            self.updated_by,
        )


# CONNECTED APPS: tickets, travel, projects, sci_fi
class FiscalYear(models.Model):
    full = models.TextField(blank=True, null=True)
    short = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.full)

    class Meta:
        ordering = ['id', ]


class Province(SimpleLookupWithUUID):
    # Choices for surface_type
    CAN = 'Canada'
    US = 'United States'
    COUNTRY_CHOICES = (
        (CAN, _('Canada')),
        (US, _('United States')),
    )
    abbrev_eng = models.CharField(max_length=25, blank=True, null=True, verbose_name=_("abbreviation (English)"))
    abbrev_fre = models.CharField(max_length=25, blank=True, null=True, verbose_name=_("abbreviation (French)"))
    country = models.CharField(max_length=25, choices=COUNTRY_CHOICES, verbose_name=_("country"))
    # meta
    date_last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    @property
    def tabbrev(self):
        # check to see if a french value is given
        if getattr(self, str(_("abbrev_eng"))):
            return "{}".format(getattr(self, str(_("abbrev_eng"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.abbrev_eng)

    class Meta:
        ordering = ['name', ]


# CONNECTED APPS: masterlist
class Region(SimpleLookupWithUUID):
    abbrev = models.CharField(max_length=10, verbose_name=_("abbreviation"))
    head = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("RDG / ADM"),
                             related_name="shared_models_regions")
    admin = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("admin"),
                              related_name="shared_models_admin_regions")
    # meta
    date_last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    class Meta:
        ordering = ['name', ]
        verbose_name = _("Region - Sector (NCR)")
        verbose_name_plural = _("Regions - Sectors (NCR)")


class Branch(SimpleLookupWithUUID):
    name = models.CharField(max_length=255, verbose_name=_("name (en)"))
    abbrev = models.CharField(max_length=10, verbose_name=_("abbreviation"))
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, verbose_name=_("region"), related_name="branches")
    head = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True,
                             verbose_name=_("regional director / NCR director general"),
                             related_name="shared_models_branches")
    admin = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("admin"),
                              related_name="shared_models_admin_branches")
    # meta
    date_last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def __str__(self):
        # check to see if a french value is given
        return f"{self.tname} ({self.region})"

    class Meta:
        ordering = ['name', ]
        verbose_name = _("Branch - Directorate (NCR)")
        verbose_name_plural = _("Branches - Directorates (NCR)")


class Division(SimpleLookupWithUUID):
    name = models.CharField(max_length=255, verbose_name=_("name (en)"))
    abbrev = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("abbreviation"))
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING, verbose_name=_("branch"), related_name="divisions")
    head = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("division manager / NCR director"),
                             related_name="shared_models_divisions")
    admin = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("admin"),
                              related_name="shared_models_admin_divisions")
    # meta
    date_last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def __str__(self):
        # check to see if a french value is given
        return "{} ({})".format(self.tname, self.branch.region)

    class Meta:
        ordering = ["branch__region", "name"]
        verbose_name = _("Division - Branch (NCR)")
        verbose_name_plural = _("Divisions - Branches (NCR)")


# CONNECTED APPS: tickets, travel, projects, inventory
class Section(SimpleLookupWithUUID):
    name = models.CharField(max_length=255, verbose_name=_("name (en)"))
    division = models.ForeignKey(Division, on_delete=models.DO_NOTHING, blank=False, null=True, related_name="sections")
    head = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("section head  / NCR team lead"),
                             related_name="shared_models_sections")
    admin = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("admin"),
                              related_name="shared_models_admin_sections")
    abbrev = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("abbreviation"))
    # meta
    date_last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    # calculated fields (for quick acquisition)
    shortish_name = models.CharField(max_length=1000, blank=True, null=True, editable=False)
    full_name_en = models.CharField(max_length=1000, blank=True, null=True, editable=False)
    full_name_en_ver1 = models.CharField(max_length=1000, blank=True, null=True, editable=False)
    full_name_fr = models.CharField(max_length=1000, blank=True, null=True, editable=False)
    full_name_fr_ver1 = models.CharField(max_length=1000, blank=True, null=True, editable=False)

    class Meta:
        ordering = ['division__branch__region', 'division__branch', 'division', 'name', ]
        verbose_name = _("Section - Team (NCR)")
        verbose_name_plural = _("Sections - Teams (NCR)")

    def get_full_name_en(self):
        if self.division:
            my_str = f"{self.division.branch.region.name} - {self.division.branch.name} - {self.division.name} - {self.name}"
        else:
            my_str = self.name
        return my_str

    def get_full_name_en_ver1(self):
        if self.division:
            my_str = f"{self.name} ({self.division.branch.region.name}/{self.division.name})"
        else:
            my_str = self.name
        return my_str

    def get_full_name_fr(self):
        s = self.nom if self.nom else self.name
        if self.division:
            r = self.division.branch.region.nom if self.division.branch.region.nom else self.division.branch.region.name
            b = self.division.branch.nom if self.division.branch.nom else self.division.branch.name
            d = self.division.nom if self.division.nom else self.division.name
            return f"{r} - {b} - {d} - {s}"
        else:
            return f"{s}"

    def get_full_name_fr_ver1(self):
        s = self.nom if self.nom else self.name
        if self.division:
            r = self.division.branch.region.nom if self.division.branch.region.nom else self.division.branch.region.name
            d = self.division.nom if self.division.nom else self.division.name
            return f"{s} ({r}/{d})"
        else:
            return f"{s}"

    def get_shortish_name(self):
        if self.division:
            my_str = f"{self.division.branch.region.abbrev} - {self.division.branch.abbrev} - {self.division.abbrev} - {self.name}"
        else:
            my_str = self.tname
        return my_str

    def save(self, *args, **kwargs):
        self.shortish_name = self.get_shortish_name()
        self.full_name_en = self.get_full_name_en()
        self.full_name_en_ver1 = self.get_full_name_en_ver1()
        self.full_name_fr = self.get_full_name_fr()
        self.full_name_fr_ver1 = self.get_full_name_fr_ver1()
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        # check to see if a french value is given
        if getattr(self, str(_("full_name_en"))):
            return str(getattr(self, str(_("full_name_en"))))
        # if there is no translated term, just pull from the english field
        return self.full_name_en

    @property
    def full_name_ver1(self):
        # check to see if a french value is given
        if getattr(self, str(_("full_name_en_ver1"))):
            return str(getattr(self, str(_("full_name_en_ver1"))))
        # if there is no translated term, just pull from the english field
        return self.full_name_en_ver1


class AllotmentCategory(models.Model):
    name = models.CharField(max_length=25)
    color = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


# CONNECTED APPS: projects, scifi
class AllotmentCode(models.Model):
    # choices for category
    SAL = "salary"
    CAP = "capital"
    OM = "om"
    GC = "gc"
    CBASE = "cbase"
    CATEGORY_CHOICES = (
        (SAL, "Salary"),
        (CAP, "Capital"),
        (OM, "O&M"),
        (CBASE, "Cbase"),
        (GC, "G&C"),
    )
    code = models.CharField(max_length=50, unique=True)
    name = models.TextField(blank=True, null=True)
    # category = models.CharField(max_length=25, choices=CATEGORY_CHOICES, default="other")
    allotment_category = models.ForeignKey(AllotmentCategory, on_delete=models.DO_NOTHING, related_name="allotment_codes", blank=True,
                                           null=True)

    def __str__(self):
        return "{} ({})".format(self.code, self.name)

    class Meta:
        ordering = ['code', ]


# CONNECTED APPS: scifi
class BusinessLine(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.code, self.name)

    class Meta:
        ordering = ['code', ]


# CONNECTED APPS: scifi
class LineObject(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name_eng = models.CharField(max_length=1000)
    description_eng = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.code, self.name_eng)

    class Meta:
        ordering = ['code', ]


# CONNECTED APPS: projects, scifi
class ResponsibilityCenter(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.TextField(blank=True, null=True)
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, )

    def __str__(self):
        return "{} ({})".format(self.code, self.name)

    class Meta:
        ordering = ['code', ]


# CONNECTED APPS: scifi
class CosigneeCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name_eng = models.CharField(max_length=1000)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING)
    rc_list = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "{} - {} ({})".format(self.code, self.name_eng, self.rc_list)

    class Meta:
        ordering = ['code', ]


# CONNECTED APPS: projects, scifi
class Project(models.Model):
    name = models.CharField(max_length=1000)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    project_lead = models.CharField(max_length=500, blank=True, null=True)
    default_responsibility_center = models.ForeignKey(ResponsibilityCenter, on_delete=models.DO_NOTHING, blank=True,
                                                      null=True, related_name='projects')
    default_allotment_code = models.ForeignKey(AllotmentCode, on_delete=models.DO_NOTHING, blank=True, null=True)
    default_business_line = models.ForeignKey(BusinessLine, on_delete=models.DO_NOTHING, blank=True, null=True)
    default_line_object = models.ForeignKey(LineObject, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.code, self.name)

    class Meta:
        ordering = ['code', ]


########################


class Probe(models.Model):
    name = models.CharField(max_length=255)
    nom = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class Institute(SimpleLookup):
    abbrev = models.CharField(max_length=255, verbose_name=_("abbreviation"))
    address = models.CharField(max_length=255, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class Vessel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    call_sign = models.CharField(max_length=56, null=True, blank=True, unique=True)
    ices_shipc_ship_codes = models.CharField(max_length=56, null=True, blank=True)
    country_of_origin = models.CharField(max_length=56, null=True, blank=True)
    platform_type = models.CharField(max_length=56, null=True, blank=True)
    platform_owner = models.CharField(max_length=255, null=True, blank=True)
    imo_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.call_sign:
            return "{} {}".format(self.name,
                                  self.call_sign)  # self.Country_of_origin, self.Platform_type, self.Platform_owner, self.IMO_number
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


# oceanography
# diets
# snowcrab
class Cruise(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="cruises")
    mission_number = models.CharField(max_length=255, verbose_name=_("Mission Number"), unique=True)
    mission_name = models.CharField(max_length=255, verbose_name=_("Mission Name"))
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Description"))
    purpose = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Purpose"))
    chief_scientist = models.CharField(max_length=255, verbose_name=_("Chief Scientist"))
    samplers = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Samplers"))
    start_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Start Date"))
    end_date = models.DateTimeField(null=True, blank=True, verbose_name=_("End Date"))
    probe = models.ForeignKey(Probe, null=True, blank=True, on_delete=models.DO_NOTHING)
    area_of_operation = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Area of Operation"))
    number_of_profiles = models.IntegerField(blank=True, null=True, verbose_name=_("Number of Profiles"))
    meds_id = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("MEDS ID"))
    notes = models.CharField(max_length=255, null=True, blank=True)
    season = models.IntegerField(null=True, blank=True)
    vessel = models.ForeignKey(Vessel, on_delete=models.DO_NOTHING, related_name="cruises", blank=True, null=True)
    west_bound_longitude = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=_(
        "West Bound Longitude"))  # , verbose_name="Westernmost longitude of the sampling (decimal degrees, negative for Western Hemisphere longitude)")
    east_bound_longitude = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=_(
        "East Bound Longitude"))  # , verbose_name="Easternmost longitude of the sampling (decimal degrees, negative for Western Hemisphere longitude)")
    north_bound_latitude = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=_(
        "North Bound Latitude"))  # , verbose_name="Northernmost latitude of the sampling (decimal degrees, negative for Southern Hemisphere latitude)")
    south_bound_latitude = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=_(
        "South Bound Latitude"))  # , verbose_name="Southernmost latitude of the sampling (decimal degrees, negative for Southern Hemisphere latitude)")
    funding_agency_name = models.CharField(max_length=255, null=True, blank=True,
                                           verbose_name=_("funding agency name"))  # , verbose_name="Funding agency of the data collection")
    funding_project_title = models.CharField(max_length=255, null=True, blank=True,
                                             verbose_name=_("funding project title"))  # , verbose_name="The title of your funded project")
    funding_project_id = models.CharField(max_length=255, null=True, blank=True,
                                          verbose_name=_("funding project ID"))  # , verbose_name="The ID of your funded project")
    research_projects_programs = models.TextField(null=True, blank=True, verbose_name=_(
        "research projects programs"))  # , verbose_name="The collaborative research or programs which the cruise is part of, separate them with comma")
    references = models.TextField(null=True, blank=True, verbose_name=_(
        "references"))  # , verbose_name="Provide the bibliographic citations for publications describing the data set. Example: cruise report, scientific paper")

    class Meta:
        ordering = ['mission_number', ]

    def __str__(self):
        return "{}".format(self.mission_number)

    def save(self, *args, **kwargs):
        if self.start_date:
            self.season = self.start_date.year
        return super().save(*args, **kwargs)

    @property
    def time_period(self):
        return mark_safe(
            f"{default_if_none(self.start_date.strftime('%Y-%m-%d'), '--')}  &rarr; {default_if_none(self.end_date.strftime('%Y-%m-%d'), '--')}")


#########################################

# species model
# person


class Port(models.Model):
    # Choices for province
    NS = "1"
    NB = "2"
    PE = "3"
    QC = "4"
    NL = "5"
    PROVINCE_CHOICES = (
        (NS, _('NS')),
        (NB, _('NB')),
        (PE, _('PE')),
        (QC, _('QC')),
        (NL, _('NL')),
    )

    province_code = models.CharField(max_length=1, choices=PROVINCE_CHOICES)
    district_code = models.CharField(max_length=2)
    port_code = models.CharField(max_length=2)
    port_name = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    herring_fishing_area_code = models.CharField(max_length=100, blank=True, null=True)
    nafo_unit_area_code = models.CharField(max_length=100, blank=True, null=True)

    # These two fields are just temporary. they are being created to help bridge the data from the hlog format into oracle.
    # They should be deleted once the new herring database is being used.
    alias_wharf_id = models.IntegerField(blank=True, null=True)
    alias_wharf_name = models.CharField(max_length=100, blank=True, null=True)

    @property
    def full_district(self):
        return "{}{}".format(self.province_code, self.district_code, )

    @property
    def full_code(self):
        return "{}{}{}".format(self.province_code, self.district_code, self.port_code)

    def __str__(self):
        return "{}, {} ({}{}{})".format(self.port_name, self.get_province_code_display(), self.province_code, self.district_code,
                                        self.port_code)

    class Meta:
        ordering = ['port_name', 'province_code', 'district_code', 'port_code']
        unique_together = ['province_code', 'district_code', 'port_code']


class Language(models.Model):
    name = models.CharField(max_length=25)
    nom = models.CharField(max_length=25)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = [_('name'), ]


class River(models.Model):
    name = models.CharField(max_length=255)
    fishing_area_code = models.CharField(max_length=255, blank=True, null=True)
    maritime_river_code = models.IntegerField(blank=True, null=True)
    old_maritime_river_code = models.IntegerField(blank=True, null=True)
    cgndb = models.CharField(max_length=255, blank=True, null=True, unique=True, verbose_name=_("GCNDB key"))
    parent_cgndb_id = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Parent GCNDB key"))
    nbadw_water_body_id = models.IntegerField(blank=True, null=True, verbose_name=_("NDADW water body ID"))
    parent_river = models.ForeignKey('River', on_delete=models.DO_NOTHING, related_name="children_rivers", blank=True, null=True)

    @property
    def display_hierarchy(self):
        my_str = "{}".format(self.name)
        next_higher = self.parent_river

        if next_higher:
            my_str = "{} > {}".format(next_higher.name, my_str)
            next_higher = self.parent_river.parent_river

            if next_higher:
                my_str = "{} > {}".format(next_higher.name, my_str)
                next_higher = self.parent_river.parent_river.parent_river

                if next_higher:
                    my_str = "{} > {}".format(next_higher.name, my_str)
                    next_higher = self.parent_river.parent_river.parent_river.parent_river

                    if next_higher:
                        my_str = "{} > {}".format(next_higher.name, my_str)
                        next_higher = self.parent_river.parent_river.parent_river.parent_river.parent_river

                        if next_higher:
                            my_str = "{} > {}".format(next_higher.name, my_str)
                            next_higher = self.parent_river.parent_river.parent_river.parent_river.parent_river.parent_river

                            if next_higher:
                                my_str = "{} > {}".format(next_higher.name, my_str)
                                next_higher = self.parent_river.parent_river.parent_river.parent_river.parent_river.parent_river.parent_river

                                if next_higher:
                                    my_str = "{} > {}".format(next_higher.name, my_str)

        return my_str

    @property
    def display_anchored_hierarchy(self):
        my_str = "{}".format(self.name)
        next_higher = self.parent_river

        if next_higher:
            my_str = "<a href='{}'>{}</a> > {}".format(reverse("trapnet:river_detail", kwargs={"pk": next_higher.id}), next_higher.name,
                                                       my_str)
            next_higher = self.parent_river.parent_river

            if next_higher:
                my_str = "<a href='{}'>{}</a> > {}".format(reverse("trapnet:river_detail", kwargs={"pk": next_higher.id}), next_higher.name,
                                                           my_str)
                next_higher = self.parent_river.parent_river.parent_river

                if next_higher:
                    my_str = "<a href='{}'>{}</a> > {}".format(reverse("trapnet:river_detail", kwargs={"pk": next_higher.id}),
                                                               next_higher.name, my_str)
                    next_higher = self.parent_river.parent_river.parent_river.parent_river

                    if next_higher:
                        my_str = "<a href='{}'>{}</a> > {}".format(reverse("trapnet:river_detail", kwargs={"pk": next_higher.id}),
                                                                   next_higher.name, my_str)
                        next_higher = self.parent_river.parent_river.parent_river.parent_river.parent_river

                        if next_higher:
                            my_str = "<a href='{}'>{}</a> > {}".format(reverse("trapnet:river_detail", kwargs={"pk": next_higher.id}),
                                                                       next_higher.name, my_str)
                            next_higher = self.parent_river.parent_river.parent_river.parent_river.parent_river.parent_river

                            if next_higher:
                                my_str = "<a href='{}'>{}</a> > {}".format(reverse("trapnet:river_detail", kwargs={"pk": next_higher.id}),
                                                                           next_higher.name, my_str)
                                next_higher = self.parent_river.parent_river.parent_river.parent_river.parent_river.parent_river.parent_river

                                if next_higher:
                                    my_str = "<a href='{}'>{}</a> > {}".format(
                                        reverse("trapnet:river_detail", kwargs={"pk": next_higher.id}), next_higher.name, my_str)

        return mark_safe(my_str)

    def __str__(self):
        return "{} ({})".format(self.name, self.fishing_area_code)

    class Meta:
        ordering = ['name']


class PAAItem(models.Model):
    code = models.CharField(max_length=255, verbose_name=_("code"), unique=True)
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("name (en)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("name (fr)"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            my_str = "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            my_str = "{}".format(self.name)
        return f"{self.code} - {my_str}"

    class Meta:
        ordering = ['code', ]


class Script(Lookup):
    script = models.CharField(max_length=1000, verbose_name=_("script"))

    # metadata
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="last_mod_by_ocean_samples", blank=True, null=True)

    @property
    def metadata(self):
        return get_metadata_string(self.created_at, None, self.updated_at, self.modified_by)


class Location(models.Model):
    # Choices for surface_type
    CAN = 'Canada'
    US = 'United States'
    COUNTRY_CHOICES = (
        (CAN, 'Canada'),
        (US, 'United States'),
    )
    location_en = models.CharField(max_length=1000)
    location_fr = models.CharField(max_length=1000, blank=True, null=True)
    country = models.CharField(max_length=25, choices=COUNTRY_CHOICES)
    abbrev_en = models.CharField(max_length=25, blank=True, null=True)
    abbrev_fr = models.CharField(max_length=25, blank=True, null=True)
    uuid_gcmd = models.CharField(max_length=255, blank=True, null=True)

    @property
    def tname(self):
        # check to see if a french value is given
        if getattr(self, str(_("location_en"))):
            my_str = "{}".format(getattr(self, str(_("location_en"))))
        # if there is no translated term, just pull from the english field
        else:
            my_str = self.location_en
        return my_str

    def __str__(self):
        return f"{self.location_en}, {self.get_country_display()}"

    class Meta:
        ordering = ["country", "location_en"]


class Organization(SimpleLookup):
    name = models.CharField(max_length=255, verbose_name=_("name (en)"))
    abbrev = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("abbreviation"))
    address = models.TextField(blank=True, null=True, verbose_name=_("address"))
    city = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("city"))
    postal_code = models.CharField(max_length=7, blank=True, null=True, verbose_name=_("postal code"))
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, blank=True, null=True)
    is_dfo = models.BooleanField(default=True, verbose_name=_("Is this a DFO location?"))

    # calc
    full_address = models.CharField(max_length=1000, blank=True, null=True, editable=False)
    full_name_and_address = models.CharField(max_length=1000, blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        self.full_address = self.get_full_address()
        self.full_name_and_address = self.get_full_name_and_address()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name_and_address

    def get_full_address(self):
        # initial my_str with either address or None
        if self.address:
            my_str = self.address
        else:
            my_str = ""

        # add city
        if self.city:
            if my_str:
                my_str += ", "
            my_str += self.city

        # add province abbrev.
        if self.location:
            if my_str:
                my_str += ", "
            my_str += str(self.location)

        # add postal code
        if self.postal_code:
            if my_str:
                my_str += ", "
            my_str += self.postal_code
        return my_str

    def get_full_name_and_address(self):
        return self.tname + f", {self.full_address}"


class Publication(SimpleLookup):
    pass


class Citation(models.Model):
    name = models.TextField(blank=True, null=True, verbose_name="title (en)")
    nom = models.TextField(blank=True, null=True, verbose_name="title (fr)")
    authors = models.TextField(blank=True, null=True, verbose_name=_("authors"))
    year = models.IntegerField(blank=True, null=True, verbose_name=_("year"))
    publication = models.ForeignKey(Publication, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("publication name"))
    pub_number = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("publication number"))
    url_en = models.TextField(blank=True, null=True, verbose_name=_("URL (en)"))
    url_fr = models.TextField(blank=True, null=True, verbose_name=_("URL (fr)"))
    abstract_en = models.TextField(blank=True, null=True, verbose_name=_("abstract (en)"))
    abstract_fr = models.TextField(blank=True, null=True, verbose_name=_("abstract (fr)"))
    series = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("series"))
    region = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("region"))

    @property
    def tname(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            my_str = "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            my_str = self.name
        return my_str

    @property
    def turl(self):
        # check to see if a french value is given
        if getattr(self, str(_("url_en"))):
            my_str = "{}".format(getattr(self, str(_("url_en"))))
        # if there is no translated term, just pull from the english field
        else:
            my_str = self.url_en
        return my_str

    @property
    def tabstract(self):
        # check to see if a french value is given
        if getattr(self, str(_("abstract_en"))):
            my_str = "{}".format(getattr(self, str(_("abstract_en"))))
        # if there is no translated term, just pull from the english field
        else:
            my_str = self.abstract_en
        return my_str

    def __str__(self):
        return self.tname

    @property
    def short_citation(self):
        my_str = f"{self.authors}. {self.year}. {self.tname}. {self.publication} {self.pub_number}."
        return my_str

    @property
    def short_citation_html(self):
        if not self.turl:
            my_str = self.short_citation
        else:
            my_str = f'{self.authors}. {self.year}. <a href="{self.turl}"> {self.tname}</a>. {self.publication} {self.pub_number}.'
        return my_str

    @property
    def citation_br(self):
        my_str = f"<b>Title:</b> {self.tname}<br><b>Authors:</b> {self.authors}<br><b>Year:</b> {self.year}<br><b>Publication:</b> {self.publication}. {self.pub_number}"
        return my_str
