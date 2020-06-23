import os

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from shared_models import models as shared_models
from shapely.geometry import Polygon, Point, LineString


class Taxon(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255, verbose_name=_("english name"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("french name"))

    def __str__(self):
        return "{}".format(getattr(self, str(_("name"))))

    class Meta:
        ordering = ['name', ]


class SARASchedule(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("english name"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("french name"))
    description_eng = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("english description"))
    description_fre = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("french description"))

    def __str__(self):
        return "{}".format(getattr(self, str(_("name"))))

    class Meta:
        ordering = ['name', ]


class CITESAppendix(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("english name"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("french name"))
    description_eng = models.TextField(blank=True, null=True, verbose_name=_("english description"))
    description_fre = models.TextField(blank=True, null=True, verbose_name=_("french description"))

    def __str__(self):
        return "{}".format(getattr(self, str(_("name"))))

    class Meta:
        ordering = ['name', ]


class ResponsibleAuthority(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("english name"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("french name"))

    def __str__(self):
        return "{}".format(getattr(self, str(_("name"))))

    class Meta:
        ordering = ['name', ]


class SpeciesStatus(models.Model):
    # choices for used_for
    SARA = 1
    NS = 2
    NB = 3
    # PE = 4
    REDLIST = 5
    USED_FOR_CHOICES = (
        (SARA, "SARA / COSEWIC"),
        (NS, "Nova Scotia"),
        (NB, "New Brunswick"),
        # (PE, "Prince Edward Island"),
        (REDLIST, "IUCN Red List"),
    )

    used_for = models.IntegerField(choices=USED_FOR_CHOICES)
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=255, verbose_name=_("english name"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("french name"))
    description_eng = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("english description"))
    description_fre = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("french description"))

    def __str__(self):
        return "{} - {}".format(self.code, getattr(self, str(_("name"))))

    class Meta:
        ordering = ['used_for', 'name', ]


class Region(models.Model):
    # POINT = 1
    LINE = 2
    POLYGON = 3
    RANGE_TYPE_CHOICES = (
        # (POINT, "points"),
        (LINE, "line"),
        (POLYGON, "polygon"),
    )

    # code = models.CharField(max_length=5, blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name=_("english name"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("french name"))
    province = models.ForeignKey(shared_models.Province, on_delete=models.DO_NOTHING, related_name='regions', blank=True, null=True)
    temp_file = models.FileField(upload_to='temp_file', null=True)
    type = models.IntegerField(verbose_name=_("record type"), choices=RANGE_TYPE_CHOICES, default=3)

    def __str__(self):
        name = getattr(self, str(_("name"))) if getattr(self, str(_("name"))) else self.name
        return "{}, {}".format(name, self.province.tabbrev) if self.province else "{}".format(name)

    class Meta:
        ordering = ['name', ]

    def get_absolute_url(self):
        return reverse("sar_search:region_detail", kwargs={"pk": self.id})


@receiver(models.signals.post_delete, sender=Region)
def auto_delete_region_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.temp_file:
        if os.path.isfile(instance.temp_file.path):
            os.remove(instance.temp_file.path)


@receiver(models.signals.pre_save, sender=Region)
def auto_delete_region_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Region.objects.get(pk=instance.pk).temp_file
    except Region.DoesNotExist:
        return False

    new_file = instance.temp_file
    if not old_file == new_file and old_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class RegionPolygon(models.Model):

    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="polygons")
    old_id = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['region', ]

    def get_polygon(self):
        point_list = [(point.latitude, point.longitude) for point in self.points.all()]
        if len(point_list) > 0:
            try:
                return Polygon(point_list)
            except (ValueError, TypeError):
                pass
                # print("problem creating polygon id {}".format(self.pk))
                # print(point_list)

    def coords(self):
        my_polygon = self.get_polygon()
        if my_polygon:
            return {"x": my_polygon.centroid.coords[0][0],
                    "y": my_polygon.centroid.coords[0][1]}


class RegionPolygonPoint(models.Model):
    region_polygon = models.ForeignKey(RegionPolygon, on_delete=models.CASCADE, related_name="points")
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True, verbose_name="order")

    class Meta:
        ordering = ['region_polygon', "order"]

    @property
    def point(self):
        return Point(self.latitude, self.longitude)


class Species(models.Model):
    common_name_eng = models.CharField(max_length=255, verbose_name="name (English)")
    common_name_fre = models.CharField(max_length=255, blank=True, null=True, verbose_name="name (French)")
    population_eng = models.CharField(max_length=255, blank=True, null=True, verbose_name="population (English)")
    population_fre = models.CharField(max_length=255, blank=True, null=True, verbose_name="population (French)")
    scientific_name = models.CharField(max_length=255, blank=True, null=True)
    tsn = models.IntegerField(blank=True, null=True, verbose_name="ITIS TSN")
    taxon = models.ForeignKey(Taxon, on_delete=models.DO_NOTHING, related_name='spp', blank=True, null=True)
    cosewic_status = models.ForeignKey(SpeciesStatus, on_delete=models.DO_NOTHING, related_name='cosewic_spp', verbose_name=_("COSEWIC status"),
                                    blank=True, null=True, limit_choices_to={"used_for": 1})
    sara_status = models.ForeignKey(SpeciesStatus, on_delete=models.DO_NOTHING, related_name='sara_spp',
                                       verbose_name=_("SARA status"), blank=True, null=True, limit_choices_to={"used_for": 1})
    ns_status = models.ForeignKey(SpeciesStatus, on_delete=models.DO_NOTHING, related_name='ns_spp', verbose_name=_("NS status"),
                                  blank=True, null=True, limit_choices_to={"used_for": 2})
    nb_status = models.ForeignKey(SpeciesStatus, on_delete=models.DO_NOTHING, related_name='nb_spp', verbose_name=_("NB status"),
                                  blank=True, null=True, limit_choices_to={"used_for": 3})
    # pe_status = models.ForeignKey(SpeciesStatus, on_delete=models.DO_NOTHING, related_name='pe_spp', verbose_name=_("PEI status"),
    #                               blank=True, null=True, limit_choices_to={"used_for": 4})
    iucn_red_list_status = models.ForeignKey(SpeciesStatus, on_delete=models.CASCADE, related_name='iucn_spp',
                                             verbose_name=_("IUCN Red Flag status"), blank=True, null=True,
                                             limit_choices_to={"used_for": 5})

    sara_schedule = models.ForeignKey(SARASchedule, on_delete=models.DO_NOTHING, related_name='spp', verbose_name=_("SARA schedule"),
                                      blank=True, null=True)
    cites_appendix = models.ForeignKey(CITESAppendix, on_delete=models.DO_NOTHING, related_name='spp', verbose_name=_("CITES appendix"),
                                       blank=True, null=True)
    responsible_authority = models.ForeignKey(ResponsibleAuthority, on_delete=models.DO_NOTHING, related_name='spp',
                                              verbose_name=_("responsible authority"),
                                              blank=True, null=True)
    province_range = models.ManyToManyField(shared_models.Province, blank=True)
    notes_eng = models.TextField(max_length=255, null=True, blank=True, verbose_name=_("notes (English)"))
    notes_fra = models.TextField(max_length=255, null=True, blank=True, verbose_name=_("notes (French)"))
    temp_file = models.FileField(upload_to='temp_file', null=True)

    # metadata
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"),
                                         related_name="sar_spp")

    def get_absolute_url(self):
        return reverse("sar_search:species_detail", kwargs={"pk": self.id})

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        if getattr(self, str(_("population_eng"))):
            return "{} ({})".format(
                getattr(self, str(_("common_name_eng"))),
                getattr(self, str(_("population_eng"))).lower(),
            )
        else:
            return getattr(self, str(_("common_name_eng")))

    @property
    def full_name(self):
        if getattr(self, str(_("population_eng"))):
            return "{} ({})".format(
                getattr(self, str(_("common_name_eng"))),
                getattr(self, str(_("population_eng"))).lower(),
            )
        else:
            return getattr(self, str(_("common_name_eng")))

    @property
    def tname(self):
        my_str = getattr(self, str(_("common_name_eng"))) if getattr(self, str(_("common_name_eng"))) else self.common_name_eng
        return my_str

    @property
    def tpopulation(self):
        my_str = getattr(self, str(_("population_eng"))) if getattr(self, str(_("population_eng"))) else self.population_eng
        return my_str

    @property
    def tnotes(self):
        my_str = getattr(self, str(_("notes_eng"))) if getattr(self, str(_("notes_eng"))) else self.notes_eng
        return my_str

    class Meta:
        ordering = ['common_name_eng',]


@receiver(models.signals.post_delete, sender=Species)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.temp_file:
        if os.path.isfile(instance.temp_file.path):
            os.remove(instance.temp_file.path)


@receiver(models.signals.pre_save, sender=Species)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Species.objects.get(pk=instance.pk).temp_file
    except Species.DoesNotExist:
        return False

    new_file = instance.temp_file
    if not old_file == new_file and old_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class Record(models.Model):
    # choice for record type:
    POINT = 1
    LINE = 2
    POLYGON = 3
    RANGE_TYPE_CHOICES = (
        (POINT, "points"),
        (LINE, "line"),
        (POLYGON, "polygon"),
    )

    species = models.ForeignKey(Species, on_delete=models.DO_NOTHING, related_name='records', blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name=_("record name"))
    regions = models.ManyToManyField(Region, blank=True, related_name="records")
    record_type = models.IntegerField(verbose_name=_("record type"), choices=RANGE_TYPE_CHOICES)
    source = models.CharField(max_length=1000, verbose_name=_("source"))
    year = models.CharField(max_length=1000, verbose_name=_("source year"), blank=True, null=True)
    # temp_file = models.FileField(upload_to='temp_file', null=True)
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))

    # metadata
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['species', 'name']

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        return super().save(*args, **kwargs)

    def get_polygon(self):
        if self.record_type in [2, 3] and self.points.count() > 0:
            point_list = [(point.latitude_n, point.longitude_w) for point in self.points.all()]
            return Polygon(point_list)

    def coords(self):
        if self.record_type == 1 and self.points.count() > 0:
            return {"x": self.points.first().latitude_n,
                    "y": self.points.first().longitude_w}
        elif self.record_type in [2, 3] and self.points.count() > 0:
            my_polygon = self.get_polygon()
            return {"x": my_polygon.centroid.coords[0][0],
                    "y": my_polygon.centroid.coords[0][1]}


#
# @receiver(models.signals.post_delete, sender=Record)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#     """
#     Deletes file from filesystem
#     when corresponding `MediaFile` object is deleted.
#     """
#     if instance.temp_file:
#         if os.path.isfile(instance.temp_file.path):
#             os.remove(instance.temp_file.path)
#
#
# @receiver(models.signals.pre_save, sender=Record)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     """
#     Deletes old file from filesystem
#     when corresponding `MediaFile` object is updated
#     with new file.
#     """
#     if not instance.pk:
#         return False
#
#     try:
#         old_file = Record.objects.get(pk=instance.pk).temp_file
#     except Record.DoesNotExist:
#         return False
#
#     new_file = instance.temp_file
#     if not old_file == new_file and old_file:
#         if os.path.isfile(old_file.path):
#             os.remove(old_file.path)


class RecordPoints(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='points')
    # record = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name=_("site name"), blank=True, null=True)
    latitude_n = models.FloatField()
    longitude_w = models.FloatField()

    class Meta:
        ordering = ['record', ]

    def save(self, *args, **kwargs):
        if self.longitude_w and self.longitude_w > 0:
            self.longitude_w = -self.longitude_w
        return super().save(*args, **kwargs)

    @property
    def point(self):
        return Point(self.latitude_n, self.longitude_w)
