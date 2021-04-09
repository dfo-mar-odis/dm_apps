from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from shared_models import models as shared_models
from django.contrib.auth.models import User as AuthUser

from shared_models.models import UnilingualSimpleLookup


class Species(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("Internal code"), unique=True)
    english_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("English name"))
    french_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("French name"))
    latin_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Scientific name"))
    vor_code = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("VOR code"))
    quebec_code = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Quebec code"))
    maritimes_code = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Maritimes code"))
    aphia_id = models.IntegerField(null=True, blank=True, verbose_name=_("ID in World Registry of Marine Species"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("english_name"))):

            return "{}".format(getattr(self, str(_("english_name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.english_name)

    def get_absolute_url(self):
        return reverse("vault:species_detail", kwargs={"pk": self.id})


class Role(models.Model):
    ROLE_CHOICES = (
        (1, _("Data Manager")),
        (2, _("Data Entry")),
        (3, _("Marine Mammal Observer (MMO)")),
        (4, _("Verification")),
    )

    name = models.IntegerField(choices=ROLE_CHOICES, verbose_name=_("name"))

    def __str__(self):
        return self.get_name_display()

    class Meta:
        ordering = ['name', ]


class Organisation(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("English name"))
    abbrev_name = models.CharField(max_length=255, verbose_name=_("English abbreviated name"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("French name"))
    abbrev_nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("French abbreviated name"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):

            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)


class Person(models.Model):
    first_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("First name"))
    last_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Last name"))
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="people",
                                     verbose_name=_("Organisation"), null=True, blank=True)
    email = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Email address"))
    phone = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Phone number"))
    roles = models.ManyToManyField(Role, verbose_name=_("Roles"))

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse("vault:person_detail", kwargs={"pk": self.id})


class MetadataField(models.Model):
    DATA_TYPE_CHOICES = (
        (1, _("integer/categorical")),
        (2, _("float")),
        (3, _("string")),
    )
    name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Name"))
    nom = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Nom"))
    description_eng = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("English description"))
    description_fra = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("French description"))
    data_type = models.IntegerField(choices=DATA_TYPE_CHOICES, verbose_name=_("data type"))

    def __str__(self):
        return self.name


# used for defining metadata field categories, when applicable
class MetadataFieldCategory(models.Model):
    metadata_field = models.ForeignKey(MetadataField, on_delete=models.CASCADE, related_name="categories")
    code = models.CharField(max_length=3)
    description_eng = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("English description"))
    description_fra = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("French description"))

    @property
    def tname(self):
        # check to see if a french value is given
        if getattr(self, str(_("description_eng"))):
            return "{}".format(getattr(self, str(_("description_eng"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.description_eng)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("description_eng"))):
            return "{}-{}".format(self.code, getattr(self, str(_("description_eng"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}-{}".format(self.code, self.description_eng)

    class Meta:
        ordering = ['code', ]
        unique_together = ['metadata_field', 'code']


class InstrumentType(UnilingualSimpleLookup):
    MODE_CHOICES = (
        (1, _("Optical")),
        (2, _("Acoustic")),
    )

    TYPE_CHOICES = (
        (1, _("Digital")),
        (2, _("Analog")),
    )

    mode = models.IntegerField(choices=MODE_CHOICES, verbose_name=_("mode"))
    type = models.IntegerField(choices=TYPE_CHOICES, verbose_name=_("mode type"))


class Instrument(models.Model):
    instrument_type = models.ForeignKey(InstrumentType, on_delete=models.DO_NOTHING, related_name="instruments",
                                        verbose_name=_("Type of instrument"))
    name = models.CharField(max_length=255, verbose_name=_("English name"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("French name"))

    # metadata = models.ManyToManyField("MetadataField", through="InstrumentMetadatum",  verbose_name=_("Metadata"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):

            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse("vault:instrument_detail", kwargs={"pk": self.id})


class InstrumentMetadatum(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.DO_NOTHING, related_name="instrument_metadata",
                                   verbose_name=_("instrument"))
    metadata_field = models.ForeignKey("MetadataField", on_delete=models.CASCADE, related_name="instrument_metadata")
    value = models.CharField(max_length=1000)


# CHOICES = plane, boat, drone, mooring, glider, land, space
# class ObservationPlatformType(models.Model):
#     name = models.CharField(max_length=255)
#     nom = models.CharField(max_length=255, blank=True, null=True)
#
#     def __str__(self):
#         # check to see if a french value is given
#         if getattr(self, str(_("name"))):
#
#             return "{}".format(getattr(self, str(_("name"))))
#         # if there is no translated term, just pull from the english field
#         else:
#             return "{}".format(self.name)
#
#     class Meta:
#         ordering = ['id', ]


class ObservationPlatform(models.Model):
    PLATFORM_TYPE_CHOICES = (
        (1, _("Plane")),
        (2, _("Boat")),
        (3, _("Drone")),
        (4, _("Underwater Glider")),
        (5, _("Land")),
        (6, _("Mooring")),
        (7, _("Space")),
        (8, _("Remotely Piloted Aircraft Systems (RPAS)")),

    )

    observation_platform_type = models.IntegerField(choices=PLATFORM_TYPE_CHOICES, verbose_name=_("Type of observation platform"))
    authority = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="platform_authorities",
                                  verbose_name=_("authority"), null=True, blank=True)
    owner = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="platform_owners",
                              verbose_name=_("owner"), null=True, blank=True)
    make_model = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Make and model"))
    name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Call name"))
    longname = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("Long name"))

    @property
    def foldername(self):
        return "{}_{}_{}".format(self.authority.abbrev_name, self.owner.abbrev_name, self.name)

    def __str__(self):
        return "{}".format(self.longname)

    def get_absolute_url(self):
        return reverse("vault:observationplatform_detail", kwargs={"pk": self.id})


class Region(models.Model):
    REGION_CHOICES = (
        (1, _("St. Lawrence Estuary")),
        (2, _("Northern GSL")),
        (3, _("Southern GSL")),
        (4, _("Cabot Strait")),
        (5, _("Western NFLD")),
        (6, _("Northern NFLD")),
        (7, _("Eastern NFLD")),
        (8, _("Southern NFLD")),
        (9, _("Eastern Scotian Shelf")),
        (10, _("Scotian Shelf")),
        (11, _("Western Scotian Shelf")),
        (12, _("Bay of Fundy")),
    )
    name = models.IntegerField(blank=True, null=True, choices=REGION_CHOICES, verbose_name=_("name"))

    def __str__(self):
        return self.get_name_display()


class Purpose(models.Model):
    PURPOSE_CHOICES = (
        (1, _("Broadscale Marine Mammal Survey")),
        (2, _("Science Multi-Species Survey")),
        (3, _("Fisheries Surveillance")),
        (4, _("Fisheries Management Support")),
        (5, _("Shipping Lane Surveillance")),
        (6, _("Whale Survey")),
        (7, _("Routine Patrol")),
    )
    name = models.IntegerField(blank=True, null=True, choices=PURPOSE_CHOICES, verbose_name=_("name"))

    def __str__(self):
        return self.get_name_display()


#TODO add track file presence/absence / spatial display? to outing
class Outing(models.Model):
    observation_platform = models.ForeignKey(ObservationPlatform, on_delete=models.DO_NOTHING, related_name="outings",
                                             verbose_name=_("observation platform"))
    region = models.ManyToManyField(Region, blank=True, related_name="outings", verbose_name=_("region"))
    purpose = models.ManyToManyField(Purpose, blank=True, related_name="outings", verbose_name=_("purpose"))
    start_date = models.DateTimeField(blank=True, null=True, verbose_name=_("start date and time"))
    end_date = models.DateTimeField(blank=True, null=True, verbose_name=_("end date and time"))
    identifier_string = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("identifier string"))
    created_by = models.ForeignKey(AuthUser, related_name="outings", on_delete=models.DO_NOTHING, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    verified_by = models.ForeignKey(AuthUser, blank=True, null=True, on_delete=models.DO_NOTHING, editable=False)
    verified_at = models.DateTimeField(blank=True, null=True, editable=False)

    def __str__(self):
        return self.identifier_string

    def get_absolute_url(self):
        return reverse("vault:outing_detail", kwargs={"pk": self.id})

    @property
    def outing_duration(self):
        """Determine the length in hours of the outing from the start and end date fields"""
        return self.end_date - self.start_date


    # @property
    # def quantity_by_species(self):
    #     """find total number of each species on an outing"""
    #     species_list = self.observations.observation_sightings.all().values("species").distinct().order_by("species")
    #     my_dict = dict()
    #     for s in species_list:
    #         species = Species.objects.get(pk=s["species"])
    #         my_dict[species] = pass #todo have to add quantity sum def
    #     return my_dict


#TODO I want to take all observation lat/long and map them on the outing_detail.html as well
class Observation(models.Model):
    outing = models.ForeignKey(Outing, on_delete=models.DO_NOTHING, related_name="observations", verbose_name=_("outing"))
    instrument = models.ForeignKey(Instrument, on_delete=models.DO_NOTHING, related_name="observations",
                                   verbose_name=_("instrument"))
    datetime = models.DateTimeField(null=True, blank=True, verbose_name=_("date and time"))
    longitude = models.FloatField(null=True, blank=True, verbose_name=_("longitude"))
    latitude = models.FloatField(null=True, blank=True, verbose_name=_("latitude"))
    observer = models.ForeignKey(Person, on_delete=models.DO_NOTHING, related_name="observations",
                                 verbose_name=_("observer"), null=True, blank=True)
    metadata = models.ManyToManyField(MetadataField, blank=True, through="ObservationMetadatum") #TODO why is this through
    opportunistic = models.BooleanField(default=False, verbose_name="opportunistic?")

    def __str__(self):
        return self.outing.identifier_string

    def get_absolute_url(self):
        return reverse("vault:observation_detail", kwargs={"pk": self.id})


#TODO I don't really know what this model was for
class ObservationMetadatum(models.Model):
    observation = models.ForeignKey(Observation, on_delete=models.DO_NOTHING, related_name="observation_metadata",
                                    verbose_name=_("Observation"))
    metadata_field = models.ForeignKey(MetadataField, on_delete=models.CASCADE, related_name="observation_metadata",
                                       verbose_name=_("Metadata field"))
    value = models.CharField(max_length=1000)


class Certainty(models.Model):
    CERTAINTY_CHOICES = (
        (1, _("Unsure")),
        (2, _("Probable")),
        (3, _("Certain")),
    )
    code = models.IntegerField(blank=True, null=True, choices=CERTAINTY_CHOICES, verbose_name=_("code"))
    english_certainty_description = models.CharField(max_length=250, blank=True, null=True,
                                                     verbose_name=_("description"))
    french_certainty_description = models.CharField(max_length=250, blank=True, null=True,
                                                    verbose_name=_("description"))

    def __str__(self):
        return self.get_code_display()


class IndividualIdentification(models.Model):
    SEX_CHOICES = (
        (1, _("Unknown")),
        (2, _("Female")),
        (3, _("Male")),
    )
    id_number = models.CharField(max_length=255, verbose_name="neaq catalog #")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="name")
    sex = models.IntegerField(blank=True, null=True, choices=SEX_CHOICES, verbose_name="sex")

    def __str__(self):
        my_str = "{}".format(self.id_number)

        if self.name:
            my_str += f' ({self.name})'
        return my_str

    class Meta:
        ordering = ['id_number', ]


class ObservationSighting(models.Model):
    HEALTH_CHOICES = (
        (1, _("Unknown")),
        (2, _("Free Swimming")),
        (3, _("Entangled")),
        (4, _("Injured")),
        (5, _("Dead")),
    )

    observation = models.ForeignKey(Observation, on_delete=models.DO_NOTHING, related_name="observation_sightings",
                                    verbose_name=_("observation"))
    species = models.ForeignKey(Species, on_delete=models.DO_NOTHING, related_name="observation_sightings", null=True,
                                blank=True, verbose_name="species")
    quantity = models.IntegerField(blank=True, null=True, verbose_name="# of individuals")
    certainty = models.ForeignKey(Certainty, on_delete=models.DO_NOTHING, related_name="observation_sightings",
                                  null=True, blank=True, verbose_name="certainty")
    health_status = models.IntegerField(blank=True, null=True, choices=HEALTH_CHOICES, verbose_name="status")
    calf = models.BooleanField(default=False, verbose_name=_("mother/calf pair"))
    verified = models.BooleanField(default=False, verbose_name=_("verified"))
    known_individual = models.ManyToManyField(IndividualIdentification, related_name="observation_sightings",
                                              blank=True, verbose_name=_("known individual"))

    def __str__(self):
        return "{} - Sighting {}".format(self.observation, self.id)


class OriginalMediafile(models.Model):
    file_path = models.CharField(max_length=1000, blank=True, null=True)
    filename = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("filename"))
    observation = models.ForeignKey(Observation, on_delete=models.DO_NOTHING, related_name="original_mediafiles",
                                    verbose_name=_("observation"))
    metadata = models.ManyToManyField(MetadataField, through="OriginalMediafileMetadatum") #TODO What is this trying to do

    def __str__(self):
        return self.filename


class OriginalMediafileMetadatum(models.Model):
    original_mediafile = models.ForeignKey(OriginalMediafile, on_delete=models.DO_NOTHING,
                                           related_name="original_mediafile_metadata",
                                           verbose_name=_("original media file"))
    metadata_field = models.ForeignKey(MetadataField, on_delete=models.CASCADE,
                                       related_name="original_mediafile_metadata")
    value = models.CharField(max_length=1000)


class FieldName(models.Model):
    field_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("name"))
    used_for = models.ManyToManyField(Instrument, verbose_name=_("used for"), blank=True)


class MediafileSighting(models.Model):
    SEX_CHOICES = (
        (1, _("Unknown")),
        (2, _("Female")),
        (3, _("Male")),
    )

    LIFESTAGE_CHOICES = (
        (1, _("Unknown")),
        (2, _("Calf")),
        (3, _("Mother Calf Pair")),
        (4, _("Juvenile")),
        (5, _("Adult")),
    )

    HEALTH_CHOICES = (
        (1, _("Unknown")),
        (2, _("Healthy")),
        (3, _("All Points Bulletin (APB)")),
        (4, _("New Injury")),
        (5, _("Entangled")),
        (6, _("Distressed")),
        (7, _("Dead")),
    )
    original_mediafile = models.ForeignKey(OriginalMediafile, on_delete=models.DO_NOTHING,
                                           related_name="mediafile_sightings",
                                           verbose_name=_("original media file"))
    species = models.ForeignKey(Species, on_delete=models.DO_NOTHING, related_name="mediafile_sightings", null=True,
                                blank=True)
    certainty = models.ForeignKey(Certainty, on_delete=models.DO_NOTHING, related_name="mediafile_sightings", null=True,
                                  blank=True)
    sex = models.IntegerField(blank=True, null=True, choices=SEX_CHOICES, verbose_name="sex")
    life_stage = models.IntegerField(blank=True, null=True, choices=LIFESTAGE_CHOICES, verbose_name="life_stage")
    health_status = models.IntegerField(blank=True, null=True, choices=HEALTH_CHOICES, verbose_name="health status")
    verified = models.BooleanField(default=False, verbose_name=_("verified"))
    known_individual = models.ForeignKey(IndividualIdentification, on_delete=models.DO_NOTHING,
                                         related_name="mediafile_sightings", null=True, blank=True, verbose_name=_("known individual"))


class ProcessedMediafile(models.Model):
    file_path = models.CharField(max_length=1000, blank=True, null=True)
    filename = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("filename"))
    original_mediafile = models.ForeignKey(OriginalMediafile, on_delete=models.DO_NOTHING,
                                           related_name="processed_mediafiles",
                                           verbose_name=_("original mediafile"))
    species = models.ManyToManyField(Species, verbose_name=_("species"), blank=True)
    verified = models.BooleanField(default=False, verbose_name=_("verified"))
    analyst = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    date_analysed = models.DateTimeField()
    date_created = models.DateTimeField()
