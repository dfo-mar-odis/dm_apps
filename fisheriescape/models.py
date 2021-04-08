from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models

REGION_CHOICES = (
    ("Gulf", "Gulf"),
    ("Mar", "Maritimes"),
    ("NL", "Newfoundland"),
    ("QC", "Quebec"),
)


class FisheryArea(models.Model):
    layer_id = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("layer id"))
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("fisheries area name"))
    region = models.CharField(max_length=255, null=True, blank=True, choices=REGION_CHOICES,
                              verbose_name=_("DFO region"))
    polygon = models.MultiPolygonField(srid=4326)

    class Meta:
        unique_together = (('name', 'layer_id'),)
        ordering = ["layer_id", "name", ]

    def __str__(self):
        my_str = "{}".format(self.name)

        if self.layer_id:
            my_str += f' ({self.layer_id})'
        return my_str

    def get_absolute_url(self):
        return reverse("fisheriescape:fishery_area_detail", kwargs={"pk": self.id})


class Species(models.Model):
    english_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("english name"))
    french_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("french name"))
    latin_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("scientific name"))
    website = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("website"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("english_name"))):

            return "{}".format(getattr(self, str(_("english_name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.english_name)

    def get_absolute_url(self):
        return reverse("fisheriescape:species_detail", kwargs={"pk": self.id})


RISK_STATUS_CHOICES = (
    ("No Status", "No Status"),
    ("Not at Risk", "Not at Risk"),
    ("Special Concern", "Special Concern"),
    ("Threatened", "Threatened"),
    ("Endangered", "Endangered"),
    ("Extirpated", "Extirpated"),
    ("Extinct", "Extinct"),
)


class MarineMammal(models.Model):
    english_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("english name"))
    english_name_short = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("short english name"))
    french_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("french name"))
    french_name_short = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("short french name"))
    latin_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("scientific name"))
    sara_status = models.CharField(max_length=255, null=True, blank=True, choices=RISK_STATUS_CHOICES, verbose_name=_("sara status"))
    cosewic_status = models.CharField(max_length=255, null=True, blank=True, choices=RISK_STATUS_CHOICES, verbose_name=_("cosewic status"))
    website = models.URLField(max_length=250, blank=True, null=True, verbose_name=_("website"))

    def __str__(self):
        if self.english_name_short:

            my_str = "{}".format(self.english_name_short)
        else:
            my_str = "{}".format(self.english_name)

        return my_str

    #
    # def get_absolute_url(self):
    #     return reverse("fisheriescape:species_detail", kwargs={"pk": self.id})


STATUS_CHOICES = (
    ("Active", "Active"),
    ("Inactive", "Inactive"),
    ("Experimental", "Experimental"),
    ("Unknown", "Unknown"),
)

LICENSE_CHOICES = (
    ("Single", "Single Species"),
    ("Multi", "Multi Species"),
)


class Fishery(models.Model):
    species = models.ForeignKey(Species, on_delete=models.DO_NOTHING, related_name="fisherys",
                                verbose_name=_("species"))
    fishery_areas = models.ManyToManyField(FisheryArea, related_name="species", verbose_name=_("fishery areas"))
    start_date = models.DateTimeField(null=True, blank=True, verbose_name=_("start date of season"))
    end_date = models.DateTimeField(null=True, blank=True, verbose_name=_("end date of season"))
    fishery_status = models.CharField(max_length=255, null=True, blank=True, choices=STATUS_CHOICES,
                                      verbose_name=_("fishery status"))
    gear_type = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("gear type"))
    marine_mammals = models.ManyToManyField(MarineMammal, blank=True, related_name="fisherys", verbose_name=_("marine mammals"))
    # license_type = models.CharField(max_length=255, null=True, blank=True, choices=LICENSE_CHOICES,
    #                                 verbose_name=_("type of license"))

    class Meta:
        ordering = ["start_date", "species", ]

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("species"))):

            my_str = "{}".format(getattr(self, str(_("species"))))
            # if there is no translated term, just pull from the english field
        else:
            my_str = "{}".format(self.species)

        if self.start_date:
            my_str += f' (record: {self.id})'
        return my_str

    def get_absolute_url(self):
        return reverse("fisheriescape:fishery_detail", kwargs={"pk": self.id})
