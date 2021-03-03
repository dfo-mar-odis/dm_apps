import os

from django.db import models
from django.dispatch import receiver

from travel.models import File, Traveller


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        try:
            if os.path.isfile(instance.file.path):
                os.remove(instance.file.path)
        except:
            instance.file.delete()
            instance.delete()


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

    try:
        new_file = instance.file
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    except:
        pass


@receiver(models.signals.post_delete, sender=Traveller)
def update_request_on_traveller_delete(sender, instance, **kwargs):
    instance.request.save()


@receiver(models.signals.post_save, sender=Traveller)
def update_request_on_traveller_change_or_create(sender, instance, **kwargs):
    instance.request.save()
