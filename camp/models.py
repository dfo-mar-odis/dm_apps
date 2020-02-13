from django.db import models
from django.urls import reverse
from django.utils import timezone

from lib.templatetags.custom_filters import nz
from shared_models import models as shared_models

class Province(models.Model):
    province_eng = models.CharField(max_length=255, blank=True, null=True)
    province_fre = models.CharField(max_length=255, blank=True, null=True)
    abbrev = models.CharField(max_length=10, blank=True, null=True)
    abbrev_fre = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.province_eng, self.abbrev)


class Site(models.Model):
    site = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    province = models.ForeignKey(shared_models.Province, on_delete=models.DO_NOTHING, related_name='campsites', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.province:
            return "{} ({})".format(self.site, self.province.tabbrev)
        else:
            return "{}".format(self.site)

    class Meta:
        ordering = ['province', 'site']

    def get_absolute_url(self):
        return reverse("camp:site_detail", kwargs={"pk": self.id})


class Station(models.Model):
    name = models.CharField(max_length=255)
    site = models.ForeignKey('Site', on_delete=models.DO_NOTHING, related_name='stations', null=True)
    latitude_n = models.FloatField(blank=True, null=True)
    longitude_w = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    station_number = models.IntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("camp:station_detail", kwargs={"pk": self.id})

    def __str__(self):
        if self.site:
            return "{} ({})".format(self.name, self.site.site)
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class Species(models.Model):
    common_name_eng = models.CharField(max_length=255, blank=True, null=True, verbose_name="english name")
    common_name_fre = models.CharField(max_length=255, blank=True, null=True, verbose_name="french name")
    scientific_name = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True, unique=True)
    tsn = models.IntegerField(blank=True, null=True, verbose_name="ITIS TSN")
    aphia_id = models.IntegerField(blank=True, null=True, verbose_name="AphiaID")
    sav = models.BooleanField(default=False, verbose_name="Submerged aquatic vegetation (SAV)")
    ais = models.BooleanField(default=False, verbose_name="Aquatic invasive species")
    notes = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.common_name_eng

    class Meta:
        ordering = ['common_name_eng']

    def get_absolute_url(self):
        return reverse("camp:species_detail", kwargs={"pk": self.id})


class Sample(models.Model):
    # Choices for turbidity
    TURBID = 1
    CLEAR = 2
    TURBIDITY_CHOICES = (
        (TURBID, "Turbid"),
        (CLEAR, "Clear"),
    )

    # choice for tide_state
    LOW = 'l'
    MID = 'm'
    HIGH = 'h'
    TIDE_STATE_CHOICES = (
        (HIGH, "High"),
        (MID, "Mid"),
        (LOW, "Low"),
    )

    # choice for tide_direction
    INCOMING = 'in'
    OUTGOING = 'out'
    TIDE_DIR_CHOICES = (
        (INCOMING, "Incoming"),
        (OUTGOING, "Outgoing"),
    )

    # Choices for timezone
    AST = 'AST'
    ADT = 'ADT'
    UTC = 'UTC'
    TIMEZONE_CHOICES = (
        (AST, 'AST'),
        (ADT, 'ADT'),
        (UTC, 'UTC'),
    )

    nutrient_sample_id = models.IntegerField(blank=True, null=True, verbose_name="nutrient sample ID", unique=True)
    station = models.ForeignKey(Station, related_name='samples', on_delete=models.DO_NOTHING)
    timezone = models.CharField(max_length=5, choices=TIMEZONE_CHOICES, blank=True, null=True)
    start_date = models.DateTimeField(verbose_name="Start date / time (yyyy-mm-dd hh:mm:ss)")
    end_date = models.DateTimeField(blank=True, null=True, verbose_name="End date / time (yyyy-mm-dd hh:mm:ss)")
    weather_notes = models.CharField(max_length=1000, blank=True, null=True)
    rain_past_24_hours = models.BooleanField(default=False, verbose_name="Has it rained in the past 24 h?")
    h2o_temperature_c = models.FloatField(null=True, blank=True, verbose_name="Water temperature (°C)")
    salinity = models.FloatField(null=True, blank=True, verbose_name="Salinity (ppt)")
    dissolved_o2 = models.FloatField(null=True, blank=True, verbose_name="dissolved oxygen (mg/L)")
    water_turbidity = models.IntegerField(choices=TURBIDITY_CHOICES, blank=True, null=True)
    tide_state = models.CharField(max_length=5, choices=TIDE_STATE_CHOICES, blank=True, null=True)
    tide_direction = models.CharField(max_length=5, choices=TIDE_DIR_CHOICES, blank=True, null=True)
    samplers = models.CharField(max_length=1000, blank=True, null=True)

    percent_sand = models.FloatField(null=True, blank=True, verbose_name="Sand (%)")
    percent_gravel = models.FloatField(null=True, blank=True, verbose_name="Gravel (%)")
    percent_rock = models.FloatField(null=True, blank=True, verbose_name="Rock (%)")
    percent_mud = models.FloatField(null=True, blank=True, verbose_name="Mud (%)")

    visual_sediment_obs = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Visual sediment observations")
    sav_survey_conducted = models.BooleanField(default=False, verbose_name="Was SAV survey conducted?")
    excessive_green_algae_water = models.BooleanField(default=False, verbose_name="Excessive green algae in water?")
    excessive_green_algae_shore = models.BooleanField(default=False, verbose_name="Excessive green algae on shore?")
    unsampled_vegetation_inside = models.CharField(max_length=1000, blank=True, null=True,
                                                   verbose_name="Vegetation present inside sample area (underwater) but outside of quadrat")
    unsampled_vegetation_outside = models.CharField(max_length=1000, blank=True, null=True,
                                                    verbose_name="Vegetation present outside of sample area (underwater)")

    per_sediment_water_cont = models.FloatField(null=True, blank=True, verbose_name="sediment water content (%)")
    per_sediment_organic_cont = models.FloatField(null=True, blank=True, verbose_name="sediment organic content (%)")
    mean_sediment_grain_size = models.FloatField(null=True, blank=True,
                                                 verbose_name="Mean sediment grain size (??)")  # where 9999 means >2000

    silicate = models.FloatField(null=True, blank=True, verbose_name="Silicate (µM)")
    phosphate = models.FloatField(null=True, blank=True, verbose_name="Phosphate (µM)")
    nitrates = models.FloatField(null=True, blank=True, verbose_name="NO3 + NO2(µM)")
    nitrite = models.FloatField(null=True, blank=True, verbose_name="Nitrite (µM)")
    ammonia = models.FloatField(null=True, blank=True, verbose_name="Ammonia (µM)")
    notes = models.TextField(blank=True, null=True)

    year = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    last_modified = models.DateTimeField(blank=True, null=True)
    species = models.ManyToManyField(Species, through="SpeciesObservation")

    def save(self, *args, **kwargs):
        self.year = self.start_date.year
        self.month = self.start_date.month
        self.last_modified = timezone.now()

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-start_date', 'station']
        unique_together = [["start_date", "station"], ]

    def get_absolute_url(self):
        return reverse("camp:sample_detail", kwargs={"pk": self.id})

    def __str__(self):
        return "Sample {}".format(self.id)


class SpeciesObservation(models.Model):
    species = models.ForeignKey(Species, on_delete=models.DO_NOTHING, related_name="sample_spp")
    sample = models.ForeignKey(Sample, on_delete=models.DO_NOTHING, related_name="sample_spp")
    adults = models.IntegerField(blank=True, null=True)
    yoy = models.IntegerField(blank=True, null=True, verbose_name="young of the year (YOY)")
    total_non_sav = models.IntegerField(null=True, blank=True)
    total_sav = models.FloatField(blank=True, null=True, verbose_name="SAV level")  # this is reserved only for SAV

    def save(self, *args, **kwargs):
        self.total_non_sav = nz(self.adults, 0) + nz(self.yoy, 0)
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = [["sample", "species"], ]
        # ordering = ["-sample__year"] THIS IS WAY TOO SLOW!
