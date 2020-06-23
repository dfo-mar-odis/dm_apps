import os

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from lib.functions.custom_functions import fiscal_year
from shared_models import models as shared_models
from django.contrib.gis.db import models


class Birds(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="english name")
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name="french name")
    latin = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("scientific name"))
    code = models.CharField(max_length=255, blank=True, null=True, unique=True)

    def __str__(self):
        my_str = f'{self.tname} - <em>{self.latin}</em> ({self.code})'
        return mark_safe(my_str)

    # This is just for the sake of views.SpeciesListView
    @property
    def tname(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name']


class Route(models.Model):
    description_en = models.TextField(blank=True, null=True, verbose_name=_("route description (EN)"))
    description_fr = models.TextField(blank=True, null=True, verbose_name=_("route description (FR)"))
    recommended_people = models.IntegerField(blank=True, null=True, verbose_name=_("recommended number of people"))
    estimated_time_required = models.FloatField(blank=True, null=True, verbose_name=_("estimated time needed (hours)"))
    polygon = models.MultiPolygonField(srid=4326)

    @property
    def coords(self):
        return self.polygon.coords[0][0]

    @property
    def area_km2(self):
        return self.polygon.transform(3492, clone=True).area / 1000000

    @property
    def tdesc(self):
        # check to see if a french value is given
        if getattr(self, str(_("description_en"))):
            return "{}".format(getattr(self, str(_("description_en"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.description_en)

    def birds(self):
        return set([bird for outing in self.outings.all() for bird in outing.birds.all()])

    @property
    def current_outing(self):
        if Outing.objects.filter(route=self, fiscal_year_id=fiscal_year(sap_style=True)):
            return Outing.objects.get(route=self, fiscal_year_id=fiscal_year(sap_style=True))
        else:
            return None

    def __str__(self):
        return _("Route no. {}".format(self.id))


class Outing(models.Model):
    fiscal_year = models.ForeignKey(shared_models.FiscalYear, blank=True, null=True, on_delete=models.DO_NOTHING)
    route = models.ForeignKey(Route, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="outings")
    date = models.DateTimeField(blank=True, null=True, verbose_name=_("date of outing"))
    actual_time_required = models.FloatField(blank=True, null=True, verbose_name=_("actual time it took (hours)"))
    green_bags_collected = models.IntegerField(blank=True, null=True, verbose_name=_("no. green bags collected"))
    blue_bags_collected = models.IntegerField(blank=True, null=True, verbose_name=_("no. blue bags collected"))
    birds = models.ManyToManyField(Birds, blank=False, verbose_name=_("birds observed"))
    users = models.ManyToManyField(User, blank=False, verbose_name=_("who signed up"))
    comments = models.TextField(blank=True, null=True, verbose_name=_("comments"))

    class Meta:
        unique_together = (("route", "fiscal_year"),)

    def __str__(self):
        return str(self.fiscal_year)

    def get_absolute_url(self):
        return reverse("spring_cleanup:route_detail", kwargs={"pk": self.route.id})


def file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'spring_cleanup/{instance.id}/{filename}'


class File(models.Model):
    type_choices = (
        (1, "just to share"),
        (2, "grossest garbage found"),
        (3, "wildlife"),
        (4, "coolest piece of garbage found"),
    )
    caption = models.CharField(max_length=255)
    type = models.IntegerField(blank=True, null=True, default=1, choices=type_choices)
    outing = models.ForeignKey(Outing, related_name="pics", on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=file_directory_path)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.caption


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=File)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = File.objects.get(pk=instance.pk).file
    except File.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
