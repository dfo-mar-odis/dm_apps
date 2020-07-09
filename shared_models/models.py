from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
import uuid


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
    # meta
    date_last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    class Meta:
        ordering = ['name', ]
        verbose_name = _("Region / NCR Sector")
        verbose_name_plural = _("Regions / NCR Sectors")


class Branch(SimpleLookupWithUUID):
    name = models.CharField(max_length=255, verbose_name=_("name (en)"))
    abbrev = models.CharField(max_length=10, verbose_name=_("abbreviation"))
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, verbose_name=_("region"), related_name="branches")
    head = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True,
                             verbose_name=_("regional director / NCR director general"),
                             related_name="shared_models_branches")
    # meta
    date_last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def __str__(self):
        # check to see if a french value is given
        return "{} ({})".format(self.tname, self.region)

    class Meta:
        ordering = ['name', ]
        verbose_name = _("Branch / NCR Directorate")
        verbose_name_plural = _("Branches / NCR Directorates")


class Division(SimpleLookupWithUUID):
    name = models.CharField(max_length=255, verbose_name=_("name (en)"))
    abbrev = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("abbreviation"))
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING, verbose_name=_("branch"), related_name="divisions")
    head = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("division manager / NCR director"),
                             related_name="shared_models_divisions")
    # meta
    date_last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def __str__(self):
        # check to see if a french value is given
        return "{} ({})".format(self.tname, self.branch.region)

    class Meta:
        ordering = ['name', ]
        verbose_name = _("Division / NCR Branch")
        verbose_name_plural = _("Divisions / NCR Branches")


# CONNECTED APPS: tickets, travel, projects, inventory
class Section(SimpleLookupWithUUID):
    name = models.CharField(max_length=255, verbose_name=_("name (en)"))
    division = models.ForeignKey(Division, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="sections")
    head = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("section head  / NCR team lead"),
                             related_name="shared_models_sections")
    abbrev = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("abbreviation"))
    # meta
    date_last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    class Meta:
        ordering = ['division__branch__region', 'division__branch', 'division', 'name', ]
        verbose_name = _("Section / NCR Team")
        verbose_name_plural = _("Sections / NCR Teams")

    @property
    def full_name(self):
        try:

            my_str = "{} - {} - {} - {}".format(self.division.branch.region.tname, self.division.branch.tname, self.division.tname,
                                                self.tname)
        except AttributeError:
            my_str = self.tname
        return my_str

    @property
    def full_name_ver1(self):
        try:

            my_str = f"{self.tname} ({self.division.branch.region.tname}/{self.division.tname})"
        except AttributeError:
            my_str = self.tname
        return my_str

    @property
    def shortish_name(self):
        try:
            my_str = "{} - {} - {} - {}".format(self.division.branch.region.abbrev, self.division.branch.abbrev, self.division.abbrev,
                                                self.name)
        except AttributeError:
            my_str = self.tname
        return my_str


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


class Institute(models.Model):
    name = models.CharField(max_length=255)
    nom = models.CharField(max_length=255, blank=True, null=True)
    abbrev = models.CharField(max_length=255, verbose_name=_("abbreviation"))
    address = models.CharField(max_length=255, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]

class Observations(models.Model):
    variable_name = models.CharField(max_length=255)
    variable_abbreviation_in_files = models.CharField(max_length=255, blank=True, null=True)
    variable_unit = models.CharField(max_length=255)
    observation_type = models.CharField(max_length=255, verbose_name=_("Observation Type"))
    measured_or_calculated = models.CharField(max_length=255, blank=True, null=True)
    calculation_method = models.CharField(max_length=255, blank=True, null=True)
    sampling_instrument = models.CharField(max_length=255)
    analysing_instrument = models.CharField(max_length=255, blank=True, null=True)
    detailed_sampling_analyzing_information = models.CharField(max_length=255, blank=True, null=True)
    calibration_information = models.CharField(max_length=255, blank=True, null=True)
    method_reference = models.CharField(max_length=255, blank=True, null=True)
    analst_sampler = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("Variable_name"))):
            return "{}".format(getattr(self, str(_("Variable_name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{} {} {}".format(self.Variable_name, self.Variable_unit, self.Sampling_instrument)

    class Meta:
        ordering = ['variable_name', ]

class Vessel(models.Model):
    name = models.CharField(max_length=255)
    call_sign = models.CharField(max_length=56, null=True, blank=True)
    ices_shipc_ship_codes = models.CharField(max_length=56, null=True, blank=True)
    country_of_origin = models.CharField(max_length=56, null=True, blank=True)
    platform_type = models.CharField(max_length=56, null=True, blank=True)
    platform_owner = models.CharField(max_length=255, null=True, blank=True)
    imo_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.call_sign:
            return "{} {}".format(self.name, self.call_sign)  #self.Country_of_origin, self.Platform_type, self.Platform_owner, self.IMO_number
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


# oceanography
# diets
# snowcrab
class Cruise(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.DO_NOTHING, blank=True, null=True)
    mission_number = models.CharField(max_length=255, verbose_name=_("Mission Number"))
    mission_name = models.CharField(max_length=255, verbose_name=_("Mission Name"))
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Description"))
    purpose = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Purpose"))
    chief_scientist = models.CharField(max_length=255, verbose_name=_("Chief Scientist"))
    samplers = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Samplers"))
    start_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Start Date"))
    end_date = models.DateTimeField(null=True, blank=True, verbose_name=_("End Date"))
    observations = models.ForeignKey(Observations, null=True, blank=True, on_delete=models.DO_NOTHING)
    probe = models.ForeignKey(Probe, null=True, blank=True, on_delete=models.DO_NOTHING)
    area_of_operation = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Area of Operation"))
    number_of_profiles = models.IntegerField(blank=True, null=True, verbose_name=_("Number of Profiles"))
    meds_id = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("MEDS ID"))
    notes = models.CharField(max_length=255, null=True, blank=True)
    season = models.IntegerField(null=True, blank=True)
    vessel = models.ForeignKey(Vessel, on_delete=models.DO_NOTHING, related_name="missions", blank=True, null=True)
    west_bound_longitude = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=_("West Bound Longitude")) #, verbose_name="Westernmost longitude of the sampling (decimal degrees, negative for Western Hemisphere longitude)")
    east_bound_longitude = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=_("East Bound Longitude")) #, verbose_name="Easternmost longitude of the sampling (decimal degrees, negative for Western Hemisphere longitude)")
    north_bound_latitude = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=_("North Bound Latitude")) #, verbose_name="Northernmost latitude of the sampling (decimal degrees, negative for Southern Hemisphere latitude)")
    south_bound_latitude = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=_("South Bound Latitude")) #, verbose_name="Southernmost latitude of the sampling (decimal degrees, negative for Southern Hemisphere latitude)")
    funding_agency_name = models.CharField(max_length=255, null=True, blank=True,verbose_name=_("Funding Agency Name")) #, verbose_name="Funding agency of the data collection")
    funding_project_title = models.CharField(max_length=255, null=True, blank=True,verbose_name=_("Funding Project Title")) #, verbose_name="The title of your funded project")
    funding_project_ID = models.CharField(max_length=255, null=True, blank=True,verbose_name=_("Funding Project ID")) #, verbose_name="The ID of your funded project")
    research_Projects_Programs = models.CharField(max_length=255, null=True, blank=True,verbose_name=_("Research Projects Programs")) #, verbose_name="The collaborative research or programs which the cruise is part of, separate them with comma")
    references = models.CharField(max_length=255, null=True, blank=True,verbose_name=_("References")) #, verbose_name="Provide the bibliographic citations for publications describing the data set. Example: cruise report, scientific paper")

    class Meta:
        ordering = ['mission_number', ]

    def __str__(self):
        return "{}".format(self.mission_number)

    def save(self, *args, **kwargs):
        if self.start_date:
            self.season = self.start_date.year
        return super().save(*args, **kwargs)


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
