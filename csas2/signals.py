import os

from django.db import models
from django.dispatch import receiver

from csas2.models import CSASRequestReview, CSASRequestFile, CSASRequest, Process
from lib.functions.custom_functions import fiscal_year


@receiver(models.signals.post_save, sender=CSASRequestReview)
def save_request_on_review_save(sender, instance, created, **kwargs):
    instance.csas_request.save()



# @receiver(models.signals.post_save, sender=Process)
# def update_fiscal_year_on_process_save(sender, instance, created, **kwargs):
#
#     instance.save()

@receiver(models.signals.m2m_changed, sender=Process.csas_requests.through)
def csas_request_change(sender, action, pk_set, instance=None, **kwargs):
    if action in ['post_add', 'post_remove']:
        instance.save()


@receiver(models.signals.post_delete, sender=CSASRequest)
def update_process_on_request_delete(sender, instance, **kwargs):
    for p in instance.processes.all():
        p.save()


@receiver(models.signals.post_save, sender=CSASRequest)
def update_process_on_request_change_or_create(sender, instance, **kwargs):
    for p in instance.processes.all():
        p.save()



@receiver(models.signals.post_delete, sender=CSASRequestFile)
def auto_delete_csas2_request_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=CSASRequestFile)
def auto_delete_csas2_request_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = CSASRequestFile.objects.get(pk=instance.pk).file
    except CSASRequestFile.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)



# TODO: add signal to create a person upon creating / updating a user