import os
from django.dispatch import receiver
from django.db import models
from django.utils import timezone
from datetime import timedelta
from shared_models import models as shared_models
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext
from dm_apps import custom_widgets

# Create your models here.

def img_file_name(instance, filename):
    img_name = 'oceanography/{}'.format(filename)
    return img_name

class Doc(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    source = models.TextField(null=True, blank=True)
    # url = models.TextField(null=True, blank=True)
    file = models.FileField(null=True, blank=True, upload_to=img_file_name)
    date_modified = models.DateTimeField(default = timezone.now )

    def save(self,*args,**kwargs):
        self.date_modified  = timezone.now()
        return super().save(*args,**kwargs)


    def __str__(self):
        return self.item_name

class Bottle(models.Model):

    # Choices for sal_units
    PPT = "PPT"
    PSU = "PSU"
    SAL_UNITS_CHOICES = (
        (PPT, "parts per thousand (PPT)"),
        (PSU, "practical salinity unit (PSU)"),
    )

    # Choices for timezone
    TIMEZONE_CHOICES = (
        ("AST","Atlantic Standard Time"),
        ("ADT","Atlantic Daylight Time"),
        ("UTC","Coordinated Universal Time"),
    )

    mission = models.ForeignKey(shared_models.Cruise, related_name="bottles", on_delete=models.CASCADE)
    bottle_uid = models.CharField(max_length=10, unique=True)
    station = models.CharField(null=True, blank=True, max_length=25, verbose_name="Station")
    stratum = models.IntegerField(null=True, blank=True, verbose_name="Stratum")
    set = models.IntegerField(null=True, blank=True, verbose_name="Set #")
    event = models.CharField(max_length=510, null=True, blank=True)
    date_time = models.DateTimeField(null=True, blank=True)
    timezone = models.CharField(max_length=3, choices=TIMEZONE_CHOICES)
    date_time_UTC = models.DateTimeField(null=True, blank=True, verbose_name="Date / time (UTC)")
    sounding_m = models.FloatField(null=True, blank=True, verbose_name="Sounding (m)")
    bottle_depth_m = models.FloatField(null=True, blank=True, verbose_name="Bottle depth (m)")
    temp_c = models.FloatField(null=True, blank=True, verbose_name="Temperature (°C)")
    salinity = models.FloatField(null=True, blank=True, verbose_name="Salinity")
    sal_units = models.CharField(max_length=5, null=True, blank=True, choices=SAL_UNITS_CHOICES, verbose_name="Salinity units")
    ph = models.FloatField(null=True, blank=True, verbose_name="pH")
    lat_DDdd = models.FloatField(null=True, blank=True, verbose_name="Latitude")
    long_DDdd = models.FloatField(null=True, blank=True, verbose_name="Longitude")
    ctd_filename = models.CharField(max_length=255, null=True, blank=True)
    remarks = models.CharField(max_length=510, null=True, blank=True)
    samples_collected = models.CharField(max_length=510, null=True, blank=True)

    def save(self,*args,**kwargs):
        if self.date_time and self.timezone:
            if self.timezone == "UTC":
                self.date_time_UTC  = self.date_time
            elif self.timezone == "AST":
                self.date_time_UTC  = self.date_time + timedelta(hours=4)
            elif self.timezone == "ADT":
                self.date_time_UTC  = self.date_time + timedelta(hours=3)
        return super().save(*args,**kwargs)

    class Meta:
        ordering = ['mission','bottle_uid']

    def __str__(self):
        return "Bottle {}".format(self.bottle_uid)


def file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'oceanography/{0}/{1}'.format(instance.mission.mission_number, filename)

class File(models.Model):
    caption = models.CharField(max_length=255)
    mission = models.ForeignKey(shared_models.Cruise, related_name="files", on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_directory_path)
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

class HelpText(models.Model):
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