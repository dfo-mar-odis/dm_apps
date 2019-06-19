from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models
from django.urls import reverse
from django.utils import timezone
from textile import textile
# from lib.functions.fiscal_year import fiscal_year
from django.utils.translation import gettext_lazy as _
from shared_models import models as shared_models
from datetime import date, timedelta, datetime
import os
from django.db.models.signals import post_save
# from tagging.registry import register


class Instrument(models.Model):
    TYPE_CHOICES = [('AMAR', 'AMAR'),
                    ('Baker Traps', 'Baker Traps'),
                    ('SBE uCat', 'SB uCat'),
                    ('SBE ODO', 'SB ODO'),
                    ('SBE IDO', 'SB IDO'),
                    ('SBE16+', 'SBE16+'),
                    ('SBE19+', 'SBE19+'),
                    ('SBE37 NoPump', 'SBE37 NoPump'),
                    ('SBE37 W/Pump', 'SBE37 W/Pump'),
                    ('SBE SeaFET', 'SBE SeaFET'),
                    ('SBE SeapHox', 'SBE SeapHox'),
                    ('TRDI LR75kHz', 'TRDI LR75kHz'),
                    ('ADCP 150kHz', 'ADCP 150kHz'),
                    ('ADCP 300kHz', 'ADCP 300kHz'),
                    ('ADCP 600kHz', 'ADCP 600kHz'),
                    ('Nortek Aquadopps', 'Nortek Aquadopps'),
                    ('SONTEK Argonaut', 'SONTEK Argonaut'),
                    ('RBR Virtuoso', 'RBR Virtuoso'),
                    ('Wildlife Acoustics SM2M+', 'Wildlife Acoustics SM2M+'),
                    ('Wildlife Acoustics SM3M', 'Wildlife Acoustics SM3M'),
                    ('Multi Electronique Aural M2', 'Multi Electronique Aural M2'),
                    ('AR861 Acoustic Release', 'AR861 Acoustic Release'),
                    ('CTD', 'CTD'),
                    ('OXY', 'OXY')]
    CONNECTOR_TYPES = [('CIRCULAR', 'CIRCULAR'),
                       ('RA', 'RA')]
    COMMS = [('232', '232'),
             ('422', '422')]
    # fiscal_year = models.CharField(max_length=50, default="2019-2020", verbose_name=_("fiscal year"))
    # year = models.TextField(verbose_name=("Instrument title"))
    instrument_type = models.CharField(max_length=20, default='SBE16+', verbose_name=_("Instrument Type"),
                                       choices=TYPE_CHOICES)
    serial_number = models.CharField(max_length=20, default='00000', verbose_name=_("Serial ID"))
    purchase_date = models.DateField(blank=True, null=True, verbose_name=_("Purchase Date"))
    project_title = models.TextField(blank=True, null=True, verbose_name=_("Project title"))
    scientist = models.TextField(blank=True, null=True, verbose_name=_("Scientist"))
    connector = models.CharField(max_length=20,  blank=True, null=True, verbose_name=_("Connector Type"),
                                 choices=CONNECTOR_TYPES)
    comm_port = models.CharField(max_length=20,  blank=True, null=True,verbose_name=_("COMM Port"),
                                 choices=COMMS)
    # location = models.CharField(max_length=20,  blank=True, null=True,verbose_name=_("Location"))
    location = models.CharField(max_length=20, default='HOME IOS', verbose_name=_("Location"))
    # date_of_last_service = models.DateField(blank=True, null=True,
    #                                         verbose_name=_("Last Service Date"))
    date_of_next_service = models.DateField(blank=True, null=True,
                                            verbose_name=_("Next Service Date"))
    # last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True,
    #                                      verbose_name=_("last modified by"))
    # in_service = models.BooleanField(default=False, verbose_name=_("In Service"))
    is_sensor = models.BooleanField(default=False, verbose_name=_("Is Sensor?"))
    asset_tag = models.CharField(max_length=20, blank=True,  null=True,
                                 verbose_name=_("Asset Tag"), unique=True)
    # submitted = models.BooleanField(default=False, verbose_name=_("Submit instrument for review"))

    class Meta:
        ordering = ['instrument_type', 'serial_number', 'purchase_date', 'project_title']
        unique_together = ['instrument_type', 'serial_number']


    def __str__(self):
        # return "{}".format(self.project_title)

        return "{}".format(self.instrument_type) + " {}".format(self.serial_number)


    def get_absolute_url(self):
        return reverse('ios2:instrument_detail', kwargs={'pk': self.pk})


    # @property
    # def get_last_service_date(self):
    #     print(self.service)
    #     print('aaaaaaaaaaaaaaaaaa')
    #     return 0


# register(Instrument)


class Mooring(models.Model):

    instruments = models.ManyToManyField(Instrument, blank=True, through='InstrumentMooring',
                                         related_name='moorings')

    mooring = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("mooring name"))
    mooring_number = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("mooring number"))
    deploy_time = models.DateTimeField(blank=True, null=True,
                                       verbose_name=_("deploy time (UTC)"))
    recover_time = models.DateTimeField(blank=True, null=True,
                                        verbose_name=_("recover time (UTC)"))

    lat = models.TextField(blank=True, null=True, verbose_name=_("lat"))
    lon = models.TextField(blank=True, null=True, verbose_name=_("lon"))
    depth = models.TextField(blank=True, null=True, verbose_name=_("depth"))
    # orientation = models.TextField(blank=True, null=True, verbose_name=_("Orientation"))
    # comments = models.TextField(blank=True, null=True, verbose_name=_("comments"))
    comments = models.TextField(blank=True, null=True, verbose_name=_("comments"))
    submitted = models.BooleanField(default=False, verbose_name=_("Submit moorings for review"))

    def __str__(self):
        return "{}".format(self.mooring) + " {}".format(self.mooring_number)

    # def clean_title(self):
    #     return self.cleaned_data['mooring'].capitalize()

    class Meta:
        ordering = ['mooring', 'mooring_number']
        unique_together = ['mooring', 'mooring_number']


class InstrumentMooring(models.Model):

    ORIENTATION_CHOICES = [('UP', 'UP'),
                           ('DOWN', 'DOWN')]

    instrument = models.ForeignKey(Instrument, blank=True, on_delete=models.DO_NOTHING,
                                   related_name="instrudeploy", verbose_name=_("instrument"))
    mooring = models.ForeignKey(Mooring, on_delete=models.DO_NOTHING,
                                related_name="instrudeploy", verbose_name=_("mooring"))
    depth = models.TextField(blank=True)
    orientation = models.TextField(blank=True, null=True, verbose_name=_("Orientation"),
                                   choices=ORIENTATION_CHOICES)


    def __str__(self):

        return "{}".format(self.instrument) + " {}".format(self.mooring)
    class Meta:
        # ordering = ['mooring', 'mooring_number']
        # auto_created = True
        unique_together = ['instrument', 'mooring']


class ServiceHistory(models.Model):
    # category choices:
    CALIB = 1#'Calibration'
    REPAIR = 2#'Repair'
    REPAIRCALIB = 3

    CATEGORY_CHOICES = (
        (CALIB, _("Calibration")),
        (REPAIR, _("Repair")),
        (REPAIRCALIB, _("Repair&Calib")),
    )
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name="service",
                                   verbose_name=_("instrument"))

    category = models.IntegerField(choices=CATEGORY_CHOICES, verbose_name=_("category"))

    service_date = models.DateField(blank=True, null=True,
                                    verbose_name=_("Service Date"))

    next_service_date = models.DateField(blank=True, null=True,
                                         verbose_name=_("Next Service Date"))

    comments = models.TextField(blank=True)

    def __str__(self):
        return "{}".format(self.get_category_display())

    class Meta:
        get_latest_by = ['service_date']


@receiver(post_save, sender=ServiceHistory, dispatch_uid="update_next_service_date")
def update_next_service_date(sender, instance, **kwargs):
    if instance.instrument.date_of_next_service is not None:
        if instance.instrument.date_of_next_service < instance.next_service_date:
            instance.instrument.date_of_next_service = instance.next_service_date
            instance.instrument.save()
    else:
        instance.instrument.date_of_next_service = instance.next_service_date
        instance.instrument.save()

#
@receiver(post_save, sender=InstrumentMooring, dispatch_uid="update_instrument_location")
def update_instrument_location(sender, instance, **kwargs):
    print(kwargs)
    if instance.mooring.deploy_time is not None:  # Deploy date is entered
        if instance.mooring.recover_time is None:  # not recovered yet
            # if today > instance.mooring.recover_time:
            instance.instrument.location = instance.mooring.mooring + ' ' + instance.mooring.mooring_number

        else: # recovered
            instance.instrument.location = 'HOME IOS'
        instance.instrument.save()


@receiver(post_save, sender=Mooring, dispatch_uid="update_instrument_location_from_mooring")
def update_instrument_location_from_mooring(sender, instance, **kwargs):
    if instance.deploy_time is not None:  # Deploy date is entered
        if instance.recover_time is None:  # not recovered yet
            for deployed in instance.instrudeploy.all():
                deployed.instrument.location = instance.mooring + ' ' + instance.mooring_number
                deployed.instrument.save()

        else: # recovered
            for deployed in instance.instrudeploy.all():
                deployed.instrument.location = 'HOME IOS'
                deployed.instrument.save()


# @receiver(post_save, sender=Instrument, dispatch_uid="update_instrument_location_from_service")
# def update_instrument_location_from_service(sender, instance, **kwargs):
#     if instance.location == 'HOME IOS':  # Deploy date is entered
#         if instance.in_service == True:
#             instance.location == 'IN SERVICE'
#             instance.instrument.save()
#         else:
#             print('first')
#             raise
#     else:
#         print('second')
#         raise
        # if instance.recover_time is None:  # not recovered yet
        #     for deployed in instance.instrudeploy.all():
        #         deployed.instrument.location = instance.mooring + ' ' + instance.mooring_number
        #         deployed.instrument.save()
        #
        # else: # recovered
        #     for deployed in instance.instrudeploy.all():
        #         deployed.instrument.location = 'HOME IOS'
        #         deployed.instrument.save()


#
# def file_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return 'inventory/resource_{0}/{1}'.format(instance.id, filename)
#
#
# class File(models.Model):
#     caption = models.CharField(max_length=255)
#     resource = models.ForeignKey(Resource, related_name="files", on_delete=models.CASCADE)
#     file = models.FileField(upload_to=file_directory_path)
#     date_created = models.DateTimeField(default=timezone.now)
#
#     class Meta:
#         ordering = ['-date_created']
#
#     def __str__(self):
#         return self.caption
#
#
# @receiver(models.signals.post_delete, sender=File)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#     """
#     Deletes file from filesystem
#     when corresponding `MediaFile` object is deleted.
#     """
#     if instance.file:
#         if os.path.isfile(instance.file.path):
#             os.remove(instance.file.path)
#
#
# @receiver(models.signals.pre_save, sender=File)
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
#         old_file = File.objects.get(pk=instance.pk).file
#     except File.DoesNotExist:
#         return False
#
#     new_file = instance.file
#     if not old_file == new_file:
#         if os.path.isfile(old_file.path):
#             os.remove(old_file.path)
#

