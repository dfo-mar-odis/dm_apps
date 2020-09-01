from datetime import datetime

import pytz
from django.db import models
from django.urls.base import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import make_aware
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

# Create your models here.


class Country(models.Model):
    country_code = models.CharField(_("ISO3166-2 country code"), max_length=3)
    country_name = models.CharField(_("Country name"), max_length=120)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = _("country")
        verbose_name_plural = _("countries")

    def __str__(self):
        return self.country_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.country_name)
        super(Country, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("country_detail", kwargs={"slug": self.slug})


class Subregion(models.Model):

    subregion = models.CharField(_("ISO3316 subregion name"), max_length=100)
    code = models.CharField(_("ISO3316 subregion code"), max_length=10)

    class Meta:
        verbose_name = _("subregion")
        verbose_name_plural = _("subregions")

    def __str__(self):
        return f'{self.code} - {self.subregion}'

    def get_absolute_url(self):
        return reverse("subdivision_detail", kwargs={"slug": self.slug})


class MarineRegion(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(
        "grainsize.Country",
        verbose_name=_("Country"),
        on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = _("marine region")
        verbose_name_plural = _("marine regions")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("marineregion_detail", kwargs={"slug": self.slug})


class Project(models.Model):

    name = models.CharField(max_length=100, unique=True)
    pi = models.CharField(_("Principal investigator"), max_length=100)
    marine_region = models.ForeignKey(
        "grainsize.MarineRegion",
        on_delete=models.DO_NOTHING,
        verbose_name="Marine Region Name")
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"pk": self.pk})


class Analysis(models.Model):

    code = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name = _("analysis")
        verbose_name_plural = _("analyses")

    def __str__(self):
        return f'{self.code} - {self.description}'

    def get_absolute_url(self):
        return reverse("analysis_detail", kwargs={"pk": self.pk})


class Collection(models.Model):

    code = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = _("collection")
        verbose_name_plural = _("collections")

    def __str__(self):
        return f'{self.code} - {self.description}'

    def get_absolute_url(self):
        return reverse("collection_detail", kwargs={"pk": self.pk})


class Preservation(models.Model):

    code = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = _("preservation")
        verbose_name_plural = _("preservations")

    def __str__(self):
        return f'{self.code} - {self.description}'

    def get_absolute_url(self):
        return reverse("preservation_detail", kwargs={"pk": self.pk})


class SampleType(models.Model):

    code = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = _("sample type")
        verbose_name_plural = _("sample types")

    def __str__(self):
        return f'{self.code} - {self.description}'

    def get_absolute_url(self):
        return reverse("sampletype_detail", kwargs={"pk": self.pk})


class StorageType(models.Model):

    code = models.CharField(max_length=100, unique=True)
    container = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("storage type")
        verbose_name_plural = _("storage types")

    def __str__(self):
        return f'{self.code} - {self.container}, {self.container}'

    def get_absolute_url(self):
        return reverse("storagetype_detail", kwargs={"pk": self.pk})


class Unit(models.Model):

    unit = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=120)

    class Meta:
        verbose_name = _("unit")
        verbose_name_plural = _("units")

    def __str__(self):
        return self.unit

    def get_absolute_url(self):
        return reverse("unit_detail", kwargs={"pk": self.pk})


class Sample(models.Model):

    project = models.ForeignKey(
        "grainsize.Project", on_delete=models.DO_NOTHING)
    event_number = models.CharField(null=True, blank=True, max_length=128)
    latitude = models.DecimalField(max_digits=8,
                                   decimal_places=5)
    longitude = models.DecimalField(max_digits=8,
                                    decimal_places=5)
    datetime = models.DateTimeField(_("Datetime (UTC)"), default=timezone.now)
    start_depth = models.DecimalField(
        _("Start Depth (m)"),
        max_digits=6,
        decimal_places=3,
        null=True,
        blank=True)
    end_depth = models.DecimalField(
        _("End Depth (m)"),
        max_digits=6,
        decimal_places=3,
        null=True,
        blank=True)
    sounding = models.DecimalField(
        _("Sounding (m)"),
        max_digits=7,
        decimal_places=3,
        null=True,
        blank=True)
    ancillary_data = models.BooleanField(_("Ancillary Data?"), default=False)
    unit = models.ForeignKey("grainsize.Unit", verbose_name=_(
        "Sample units"), on_delete=models.DO_NOTHING, default=1)
    sample_id = models.CharField(
        _("Sample ID"),
        null=True,
        blank=True,
        max_length=128)
    core = models.CharField(
        _("Core ID"),
        null=True,
        blank=True,
        max_length=128)
    filter = models.CharField(
        _("Filter ID"),
        null=True,
        blank=True,
        max_length=128)
    filter_spm = models.DecimalField(
        _("Filter Suspended Particulate Matter (SPM, g/m^3)"),
        max_digits=6,
        decimal_places=3,
        null=True,
        blank=True)
    analysis = models.ForeignKey(
        "grainsize.Analysis",
        verbose_name=_("Sample analysis method"),
        on_delete=models.DO_NOTHING)
    collection = models.ForeignKey(
        "grainsize.Collection",
        verbose_name=_("Sample collection method"),
        on_delete=models.DO_NOTHING)
    preservation = models.ForeignKey(
        "grainsize.Preservation",
        verbose_name=_("Sample preservation method"),
        on_delete=models.DO_NOTHING)
    storage = models.ForeignKey(
        "grainsize.StorageType",
        verbose_name=_("Sample storage method"),
        on_delete=models.DO_NOTHING)
    sample_type = models.ForeignKey(
        "grainsize.SampleType",
        verbose_name=_("Sample type"),
        on_delete=models.DO_NOTHING)
    comment = models.TextField(_("Sample Comments"), null=True, blank=True)

    class Meta:
        verbose_name = _("sample")
        verbose_name_plural = _("samples")

    def __str__(self):
        return f'{self.project} - {self.event_number}'

    def get_absolute_url(self):
        return reverse("sample_detail", kwargs={"pk": self.pk})


class Data(models.Model):

    sample = models.ForeignKey("grainsize.Sample", verbose_name=_(
        "Sample"), on_delete=models.DO_NOTHING)
    diameter = models.CharField(
        _("Diameter"), max_length=5)
    value = models.DecimalField(
        _("Sample fraction"), max_digits=15, decimal_places=12)

    class Meta:
        verbose_name = _("data")
        verbose_name_plural = _("data")

    def __str__(self):
        return f'{self.sample} - {self.diameter} - {self.value}'

    def get_absolute_url(self):
        return reverse("data_detail", kwargs={"pk": self.pk})

    def get_latest_sample(Sample):
        return
