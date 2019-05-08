from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
import os
from django.utils.translation import gettext_lazy as _

from lib.functions.custom_functions import fiscal_year
from lib.functions.custom_functions import nz
from masterlist import models as ml_models
from shared_models import models as shared_models

class EntryType(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Name (French)"))
    color = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class Status(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Name (French)"))
    color = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class FundingPurpose(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Name (French)"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class Entry(models.Model):
    # basic
    title = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("title"))
    organizations = models.ManyToManyField(ml_models.Organization, related_name="entries",
                                           limit_choices_to={'grouping__is_indigenous': True})
    initial_date = models.DateTimeField(verbose_name=_("initial date"))
    status = models.ForeignKey(Status, default=1, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("status"),
                               related_name="entries")
    sectors = models.ManyToManyField(ml_models.Sector, related_name="entries", verbose_name=_("DFO sectors"))
    entry_type = models.ForeignKey(EntryType, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="entries", verbose_name=_("Entry Type")) # title case needed
    regions = models.ManyToManyField(shared_models.Region, related_name="entries")

    # funding
    fiscal_year = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("fiscal year/multiyear"))
    funding_needed = models.NullBooleanField(verbose_name=_("is funding needed"))
    funding_purpose = models.ForeignKey(FundingPurpose, on_delete=models.DO_NOTHING, blank=True, null=True,
                                        verbose_name=_("funding purpose"), related_name="entries")
    amount_requested = models.FloatField(blank=True, null=True, verbose_name=_("Funding Requested")) # title case needed
    amount_approved = models.FloatField(blank=True, null=True, verbose_name=_("funding approved"))
    amount_transferred = models.FloatField(blank=True, null=True, verbose_name=_("amount transferred"))
    amount_lapsed = models.FloatField(blank=True, null=True, verbose_name=_("amount lapsed"))
    amount_owing = models.NullBooleanField(verbose_name=_("Does any funding need to be recovered"))

    # meta
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    date_created = models.DateTimeField(default=timezone.now, verbose_name=_("date created"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("created by"),
                                   related_name="user_entries")

    class Meta:
        ordering = ['-date_created', ]

    def __str__(self):
        return "{}".format(self.title)

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        self.fiscal_year = fiscal_year(date=self.initial_date)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ihub:entry_detail', kwargs={'pk': self.pk})

    @property
    def amount_outstanding(self):
        return nz(self.amount_approved, 0) - nz(self.amount_transferred, 0) - nz(self.amount_lapsed, 0)


class EntryPerson(models.Model):
    # Choices for role
    LEAD = 1
    CONTACT = 2
    ROLE_CHOICES = (
        (LEAD, 'Lead'),
        (CONTACT, 'Contact'),
    )
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="people", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("User"))
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("name"))
    organization = models.CharField(max_length=50)
    role = models.IntegerField(choices=ROLE_CHOICES, blank=True, null=True, verbose_name=_("role"))

    def __str__(self):
        if self.user:
            return "{} {}".format(self.user.first_name, self.user.last_name)
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['role', 'user__first_name', "user__last_name"]


class EntryNote(models.Model):
    # Choices for type
    ACTION = 1
    NEXTSTEP = 2
    COMMENT = 3
    TYPE_CHOICES = (
        (ACTION, 'Action'),
        (NEXTSTEP, 'Next step'),
        (COMMENT, 'Comment'),
    )

    entry = models.ForeignKey(Entry, related_name='notes', on_delete=models.CASCADE)
    type = models.IntegerField(choices=TYPE_CHOICES)
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("author"))
    note = models.TextField()
    status = models.ForeignKey(Status, default=1, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("status"))

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-date"]


def file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/entry_<id>/<filename>
    return 'ihub/entry_{0}/{1}'.format(instance.entry.id, filename)


class File(models.Model):
    caption = models.CharField(max_length=255, verbose_name=_("caption"))
    entry = models.ForeignKey(Entry, related_name="files", on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_directory_path, verbose_name=_("file"))
    date_uploaded = models.DateTimeField(default=timezone.now, verbose_name=_("date uploaded"))

    class Meta:
        ordering = ['-date_uploaded']

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
