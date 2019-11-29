from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from shared_models import models as shared_models


class Lookup(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Theme(Lookup):
    """
        Theme - Lookup table of Themes of which a publication can have multiple
    """
    class Meta:
        verbose_name = "Theme"
        verbose_name_plural = "Theme(s)"


class Pillar(Lookup):
    """
        Pillar - Lookup table of Pillars of Sustainability of which a publication can have multiple
    """
    class Meta:
        verbose_name = "Pillar of Sustainability"
        verbose_name_plural = "Pillar(s) of Sustainability"


class HumanComponent(Lookup):
    """
        HumanComponent - Lookup table of Human Components of which a publication can have multiple
    """
    class Meta:
        verbose_name = "Human Component"
        verbose_name_plural = "Human Component(s)"


class EcosystemComponent(Lookup):
    """
        EcosystemComponent - Lookup table of Ecosystem Components of which a publication can have multiple
    """
    class Meta:
        verbose_name = "Ecosystem Component"
        verbose_name_plural = "Ecosystem Component(s)"


class ProgramLinkage(Lookup):
    """
        ProgramLinkage - Lookup table of Program Linkage of which a
        publication can have multiple
    """
    class Meta:
        verbose_name = "Linkage to Program"
        verbose_name_plural = "Linkage(s) to Program"


class GeographicScope(Lookup):
    """
        GeographicScope - Lookup table of Geographic Scope of which a publication can have multiple
    """
    class Meta:
        verbose_name = "Geographic Scope"
        verbose_name_plural = "Geographic Scope(s)"


class InternalContact(Lookup):
    class Meta:
        verbose_name = "Contact (Internal)"
        verbose_name_plural = "Contact(s) (Internal)"


class Organization(Lookup):
    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organization(s)"


class SpatialScale(Lookup):
    class Meta:
        verbose_name = "Spatial Scale"
        verbose_name_plural = "Spatial Scale(s)"


'''
TextLookup is intended to be used for many-to-one relationships where a DB table
has large non-searchable text blobs associated with a single project
'''


class TextLookup(models.Model):
    project = models.ForeignKey("Project", verbose_name=_("Project"), on_delete=models.CASCADE)
    value = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.value


class SpatialManagementDesignation(TextLookup):
    class Meta:
        verbose_name = "Spatial Management Designation"
        verbose_name_plural = "Spatial Management Designation(s)"


class SpatialDataProduct(TextLookup):
    class Meta:
        verbose_name = "Spatial Data Product"
        verbose_name_plural = "Spatial Data Product(s)"


class SpatialDataProductYear(TextLookup):
    class Meta:
        verbose_name = "Spatial Data Product Year"
        verbose_name_plural = "Spatial Data Product Year(s)"


class ComputerEnvironment(TextLookup):
    class Meta:
        verbose_name = "Computer Environment"
        verbose_name_plural = "Computer Environment(s)"


class ComputerLibraries(TextLookup):
    class Meta:
        verbose_name = "Computer Library"
        verbose_name_plural = "Computer Libraries"


class SourceDataInternal(TextLookup):
    class Meta:
        verbose_name = "Data Source (Internal)"
        verbose_name_plural = "Data Source(s) (Internal)"


class SourceDataExternal(TextLookup):
    class Meta:
        verbose_name = "Data Source (External)"
        verbose_name_plural = "Data Source(s) (External)"


class Publication(TextLookup):
    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publication(s)"


class Site(TextLookup):
    class Meta:
        verbose_name = "Site"
        verbose_name_plural = "Site(s)"


class FgpLinkage(TextLookup):
    class Meta:
        verbose_name = "FGP Linkage"
        verbose_name_plural = "FGP Linkage(s)"


class CodeSite(TextLookup):
    class Meta:
        verbose_name = "Code Site"
        verbose_name_plural = "Code Site(s)"


class ExternalContact(TextLookup):
    class Meta:
        verbose_name = "Contact (External)"
        verbose_name_plural = "Contact(s) (External)"


class GeoCoordinate(models.Model):

    north_south = models.FloatField()
    east_west = models.FloatField()

    class Meta:
        verbose_name = "Geographic Coordinate"
        verbose_name_plural = "Geographic Coordinates"

    def __str__(self):
        return "[{}°N, {}°E]".format(self.north_south, self.east_west)


class Polygon(models.Model):
    geoscope = models.ForeignKey(GeographicScope, verbose_name=_("Polygon Name"), blank=False, null=False,
                             on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name=_("Point order"))
    latitude = models.FloatField(verbose_name=_("Latitude"))
    longitude = models.FloatField(verbose_name=_("Longitude"))

    def __str__(self):
        return "{}: [{}, {}]".format(self.order, self.longitude, self.latitude)


class Project(models.Model):
    # year
    # title
    # division <- region is a part of division
    # Linkage to national or regional program
    # Human component
    # Ecosystem component

    title = models.CharField(max_length=255, verbose_name=_("Project Title"))
    year = models.IntegerField(default=0000)
    division = models.ForeignKey(shared_models.Division, on_delete=models.DO_NOTHING, blank=True, null=True,
                                 verbose_name=_("Division"))
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now,
                                              verbose_name=_("Date last modified"))

    abstract = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    method = models.TextField(verbose_name=_("Method"), blank=True, null=True)

    # Todo: Last modified by isn't currently set in the new or update forms
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True,
                                         related_name="pub_projects")

    theme = models.ManyToManyField(Theme, verbose_name=_("Theme(s)"))
    human_component = models.ManyToManyField(HumanComponent, verbose_name=_("Human Component(s)"))
    ecosystem_component = models.ManyToManyField(EcosystemComponent, verbose_name=_("Ecosystem Component(s)"))
    sustainability_pillar = models.ManyToManyField(Pillar, verbose_name=_("Pillar(s) of Sustainability"))
    program_linkage = models.ManyToManyField(ProgramLinkage, verbose_name=_("Program Linkage(s)"))
    geographic_scope = models.ManyToManyField(GeographicScope, verbose_name=_("Geographic Scope(s)"))
    dfo_contact = models.ManyToManyField(InternalContact, verbose_name=_("Contact(s) (Internal)"))
    organization = models.ManyToManyField(Organization, verbose_name=_("Organization(s)"))
    spatial_scale = models.ManyToManyField(SpatialScale, verbose_name=_("Spatial Scale(s)"))
    coordinates = models.ForeignKey(GeoCoordinate, on_delete=models.DO_NOTHING, blank=True, null=True,
                                    verbose_name=_("Coordinate(s)"))

    division = models.ManyToManyField(shared_models.Division, verbose_name=_("Division(s)"))

    class Meta:
        ordering = ['title']

    def __str__(self):
        return "{}".format(self.title)

    def get_absolute_url(self):
        return reverse('publications:prj_detail', kwargs={'pk': self.pk})
