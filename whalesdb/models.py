# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.translation import gettext_lazy as _

from shared_models import models as shared_models


class DepDeployment(models.Model):
    dep_id = models.AutoField(primary_key=True)
    dep_year = models.BigIntegerField(verbose_name=_("Year"))
    dep_month = models.BigIntegerField(verbose_name=_("Month"))
    dep_name = models.CharField(max_length=255, verbose_name=_("Deployment"))
    stn = models.ForeignKey('StnStation', on_delete=models.DO_NOTHING, verbose_name=_("Station"))
    prj = models.ForeignKey('PrjProject', on_delete=models.DO_NOTHING, verbose_name=_("Project"))
    mor = models.ForeignKey('MorMooringSetup', on_delete=models.DO_NOTHING, verbose_name=_("Mooring Setup"))

    def __str__(self):
        return "{}".format(self.dep_name)


class EcaCalibrationEvent(models.Model):
    eca_id = models.AutoField(primary_key=True)
    eca_date = models.DateField(verbose_name=_("Calibration Date"))
    eca_attachment = models.ForeignKey('EqpEquipment', on_delete=models.DO_NOTHING, related_name='eca_attachment',
                                       verbose_name=_("Equipment"))
    eca_hydrophone = models.ForeignKey('EqpEquipment', on_delete=models.DO_NOTHING, related_name='eca_hydrophone',
                                       blank=True, null=True, verbose_name=_("Hydrophone"))
    eca_notes = models.CharField(blank=True, null=True, max_length=50, verbose_name=_("Notes"))


class EccCalibrationValue(models.Model):
    eca = models.ForeignKey(EcaCalibrationEvent, on_delete=models.DO_NOTHING, verbose_name=_("Calibration Event"))
    ecc_frequency = models.DecimalField(max_digits=10, decimal_places=6, verbose_name=_("Frequency"))
    ecc_sensitivity = models.DecimalField(max_digits=10, decimal_places=6, verbose_name=_("Sensitivity"))


class EdaEquipmentAttachment(models.Model):
    eda_id = models.AutoField(primary_key=True)
    eqp = models.ForeignKey('EqpEquipment', on_delete=models.DO_NOTHING, verbose_name=_("Equipment"))
    dep = models.ForeignKey('DepDeployment', on_delete=models.DO_NOTHING, verbose_name=_("Deployment"))

    def __str__(self):
        return "{}: {}".format(self.dep, self.eqp)


class EmmMakeModel(models.Model):
    emm_id = models.AutoField(primary_key=True)
    eqt = models.ForeignKey('EqtEquipmentTypeCode', on_delete=models.DO_NOTHING, verbose_name=_("Equipment Type"))
    emm_make = models.CharField(max_length=50, verbose_name=_("Make"))
    emm_model = models.CharField(max_length=50, verbose_name=_("Model"))
    emm_depth_rating = models.BigIntegerField(verbose_name=_("Depth Rating"))
    emm_description = models.CharField(max_length=500, verbose_name=_("Description"))

    def __str__(self):
        return "{} {}".format(self.emm_make, self.emm_model)


class EcpChannelProperty(models.Model):
    ecp_id = models.AutoField(primary_key=True)
    emm_id = models.ForeignKey('EqrRecorderProperties', on_delete=models.DO_NOTHING, verbose_name=_("Recorder"))
    ecp_channel_no = models.BigIntegerField(verbose_name=_("Channel Number"))
    eqa_adc_bits = models.ForeignKey('EqaAdcBitsCode', on_delete=models.DO_NOTHING, db_column='eqa_adc_bits',
                                     verbose_name=_("ADC Bits"))
    ecp_voltage_range_min = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True,
                                                verbose_name=_("Maximum voltage"))
    ecp_voltage_range_max = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True,
                                                verbose_name=_("Minimum voltage"))

    class Meta:
        unique_together = (('ecp_channel_no', 'emm_id'),)

    def __str__(self):
        return "{}: {}".format(_("Channel"), self.ecp_channel_no)


class EhaHydrophoneAttachment(models.Model):
    eha_id = models.AutoField(primary_key=True)
    eda = models.ForeignKey("EdaEquipmentAttachment", blank=True, null=True, on_delete=models.DO_NOTHING,
                            verbose_name=_("Attachment"))
    eqp = models.ForeignKey('EqpEquipment', blank=True, null=True, on_delete=models.DO_NOTHING,
                            verbose_name=_("Hydrophone"))

    class Meta:
        unique_together = (('eda', 'eqp'),)


class EprEquipmentParameter(models.Model):
    epr_id = models.AutoField(primary_key=True)
    emm = models.ForeignKey(EmmMakeModel, on_delete=models.DO_NOTHING, verbose_name=_("Equipment"))
    prm = models.ForeignKey('PrmParameterCode', on_delete=models.DO_NOTHING, verbose_name=_("Parameter"))

    class Meta:
        unique_together = (('emm', 'prm'),)


class ErtRecorderType(models.Model):
    ert_id = models.AutoField(primary_key=True)
    ert_name = models.CharField(unique=True, max_length=50, verbose_name=_("Recorder Type"))

    def __str__(self):
        return "{}".format(self.ert_name)


class EqaAdcBitsCode(models.Model):
    eqa_id = models.AutoField(primary_key=True)
    eqa_name = models.CharField(unique=True, max_length=50, verbose_name=_("ADC Bit Name"))

    def __str__(self):
        return "{}".format(self.eqa_name)


class EqhHydrophoneProperty(models.Model):
    emm = models.OneToOneField(EmmMakeModel, on_delete=models.DO_NOTHING, primary_key=True,
                               verbose_name=_("Hydrophone"))
    eqh_range_min = models.BigIntegerField(verbose_name=_("Min Range (dB)"))
    eqh_range_max = models.BigIntegerField(verbose_name=_("Max Range (db)"))

    def __str__(self):
        return "{}".format(self.emm)


class EqoOwner(models.Model):
    eqo_id = models.AutoField(primary_key=True)
    eqo_institute = models.CharField(max_length=100, verbose_name=_("Institute"))

    def __str__(self):
        return "{}".format(self.eqo_institute)


class EqpEquipment(models.Model):
    eqp_id = models.AutoField(primary_key=True)
    emm = models.ForeignKey("EmmMakeModel", on_delete=models.DO_NOTHING, verbose_name=_("Make and Model"))
    eqp_serial = models.CharField(max_length=50, verbose_name=_("Serial Number"))
    eqp_asset_id = models.CharField(blank=True, null=True, unique=True, max_length=50, verbose_name=_("Asset ID"))
    eqp_date_purchase = models.DateField(blank=True, null=True, verbose_name=_("Date Purchased"))
    eqp_notes = models.CharField(max_length=4000, blank=True, null=True, verbose_name=_("Notes"))
    eqp_retired = models.BooleanField(default=False, verbose_name=_("Retired?"))
    eqo_owned_by = models.ForeignKey("EqoOwner", on_delete=models.DO_NOTHING, verbose_name=_("Owner"))

    def __str__(self):
        return "{} - {} - {}".format(self.emm, self.eqp_serial, self.eqp_asset_id)


class EqrRecorderProperties(models.Model):
    emm = models.OneToOneField('EmmMakeModel', primary_key=True, on_delete=models.CASCADE,
                            verbose_name=_("Make and Model"))
    ert_id = models.ForeignKey('ErtRecorderType', on_delete=models.DO_NOTHING, verbose_name=_("Recorder Type"))
    eqr_internal_hydro = models.BooleanField(default=False, verbose_name=_("Has Internal Hydrophone"))

    def __str__(self):
        return "{}".format(self.emm)


class EqtEquipmentTypeCode(models.Model):
    eqt_id = models.AutoField(primary_key=True)
    eqt_name = models.CharField(unique=True, max_length=50, verbose_name=_("Equipment Type"))

    def __str__(self):
        return "{}".format(self.eqt_name)


class EtrTechnicalRepairEvent(models.Model):
    etr_id = models.AutoField(primary_key=True)
    eqp_id = models.ForeignKey("EqpEquipment", on_delete=models.DO_NOTHING, verbose_name=_("Equipment"))
    etr_date = models.DateField(blank=True, null=True, verbose_name=_("Date"))
    etr_issue_desc = models.TextField(blank=True, null=True, verbose_name=_("Issue"))
    etr_repair_desc = models.TextField(blank=True, null=True, verbose_name=_("Repair"))
    etr_repaired_by = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Repaired By"))


class PrmParameterCode(models.Model):
    prm_id = models.AutoField(primary_key=True)
    prm_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Parameter Code"))

    def __str__(self):
        return "{}".format(self.prm_name)


class MorMooringSetup(models.Model):
    mor_id = models.AutoField(primary_key=True)
    mor_name = models.CharField(unique=True, max_length=50, blank=True, null=True, verbose_name=_("Name"))
    mor_max_depth = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True,
                                        verbose_name=_("Max Depth"))
    mor_link_setup_image = models.CharField(max_length=4000, blank=True, null=True, verbose_name=_("Setup Image Link"))

    # Note: I added the setup image field to try out putting the mooring setup image directly in the database
    mor_setup_image = models.ImageField(blank=True, null=True, verbose_name=_("Setup Image"))

    mor_additional_equipment = models.CharField(max_length=4000, blank=True, null=True, verbose_name=_("Equipment"))
    mor_general_moor_description = models.CharField(max_length=4000, blank=True, null=True, verbose_name=_("Equipment"))
    more_notes = models.CharField(max_length=4000, blank=True, null=True, verbose_name=_("Equipment"))

    def __str__(self):
        return "{}".format(self.mor_name)


class PrjProject(models.Model):
    prj_id = models.AutoField(primary_key=True)
    prj_name = models.CharField(unique=True, max_length=255, verbose_name=_("Name"))
    prj_description = models.CharField(max_length=4000, blank=True, null=True, verbose_name=_("Description"))
    prj_url = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("URL"))

    def __str__(self):
        return "{}".format(self.prj_name)


class SetStationEventCode(models.Model):
    set_id = models.AutoField(primary_key=True)
    set_name = models.CharField(unique=True, max_length=50, verbose_name=_("Type"))
    set_description = models.CharField(max_length=400, verbose_name=_("Description"))

    def __str__(self):
        return "{} - {}".format(self.set_name, self.set_description)


class SteStationEvent(models.Model):
    ste_id = models.AutoField(primary_key=True)
    dep = models.ForeignKey(DepDeployment, on_delete=models.DO_NOTHING, verbose_name=_("Deployment"))
    set_type = models.ForeignKey('SetStationEventCode', on_delete=models.DO_NOTHING, db_column='set_type',
                                 verbose_name=_("Event Type"))
    ste_date = models.DateField(verbose_name=_("Date"))

    # Note: We're using the cruise information from the Shared Models tables rather than duplicating information.
    #   Not to mention the Shared Model tables will have more detail than Team Whale expects to get.
    crs = models.ForeignKey(shared_models.Cruise, on_delete=models.DO_NOTHING, verbose_name=_("Cruise"))

    ste_lat_ship = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True,
                                       verbose_name=_("Ship Latitude"))
    ste_lon_ship = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True,
                                       verbose_name=_("Ship Longitude"))
    ste_depth_ship = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True,
                                         verbose_name=_("Ship Depth"))
    ste_lat_mcal = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True,
                                       verbose_name=_("MCAL Latitude"))
    ste_lon_mcal = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True,
                                       verbose_name=_("MCAL Longitude"))
    ste_depth_mcal = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True,
                                         verbose_name=_("MCAL Depth"))
    ste_team = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Team"))
    ste_instrument_cond = models.CharField(max_length=4000, blank=True, null=True,
                                           verbose_name=_("Instrument Condition"))
    ste_weather_cond = models.CharField(max_length=4000, blank=True, null=True, verbose_name=_("Weather Conditions"))
    ste_logs = models.CharField(max_length=4000, blank=True, null=True, verbose_name=_("Log Location"))
    ste_notes = models.CharField(max_length=4000, blank=True, null=True, verbose_name=_("Notes"))


class StnStation(models.Model):
    stn_id = models.AutoField(primary_key=True)
    stn_name = models.CharField(max_length=100, verbose_name=_("Name"))
    stn_code = models.CharField(max_length=3, verbose_name=_("Code"))
    stn_revision = models.BigIntegerField(verbose_name=_("Revision"))
    stn_planned_lat = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_("Latitude"))
    stn_planned_lon = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_("Longitude"))
    stn_planned_depth = models.DecimalField(max_digits=10, decimal_places=6, verbose_name=_("Depth"))
    stn_notes = models.CharField(max_length=4000, blank=True, null=True, verbose_name=_("Notes"))

    class Meta:
        unique_together = (('stn_code', 'stn_revision'),)

    def __str__(self):
        current = "Past"

        stlist = StnStation.objects.filter(stn_name=self.stn_name).order_by("-stn_revision").values_list("stn_revision")

        if stlist[0][0] == self.stn_revision:
            current = "Current"

        return "{}: {} Revision {} ({})".format(self.stn_code, self.stn_name, self.stn_revision, current)


class RciChannelInfo(models.Model):
    rci_id = models.AutoField(primary_key=True)
    rec_id = models.ForeignKey("RecDataset", on_delete=models.DO_NOTHING, verbose_name=_("Dataset"))
    rci_name = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Name"))
    rci_size = models.IntegerField(blank=True, null=True, verbose_name=_("Size (GB)"))
    rci_gain = models.IntegerField(blank=True, null=True, verbose_name=_("Gain"))
    rci_volts = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, verbose_name=_("Voltage"))


class RecDataset(models.Model):
    rec_id = models.AutoField(primary_key=True)
    eda_id = models.ForeignKey("EdaEquipmentAttachment", on_delete=models.DO_NOTHING,
                               verbose_name=_("Equipment Deployment"))
    rsc_id = models.ForeignKey("RscRecordingSchedule", on_delete=models.DO_NOTHING,
                               verbose_name=_("Recording Schedule"))
    rtt_dataset = models.ForeignKey("RttTimezoneCode", on_delete=models.DO_NOTHING, related_name="rtt_dataset",
                                    verbose_name=_("Dataset Timezone"))
    rtt_in_water = models.ForeignKey("RttTimezoneCode", on_delete=models.DO_NOTHING, related_name="rtt_in_water",
                                     verbose_name=_("In Water Timezone"))
    rec_start_date = models.DateField(blank=True, null=True, verbose_name=_("In Water Start Date"))
    rec_start_time = models.TimeField(blank=True, null=True, verbose_name=_("In Water Start Time"))
    rec_end_date = models.DateField(blank=True, null=True, verbose_name=_("In Water End Date"))
    rec_end_time = models.TimeField(blank=True, null=True, verbose_name=_("In Water End Time"))
    rec_backup_hd_1 = models.IntegerField(blank=True, null=True, verbose_name=_("HD Backup 1"))
    rec_backup_hd_2 = models.IntegerField(blank=True, null=True, verbose_name=_("HD Backup 2"))
    rec_notes = models.TextField(blank=True, null=True, verbose_name=_("Notes"))

    def __str__(self):
        return self.eda_id.__str__()


class ReeRecordingEvent(models.Model):
    ree_id = models.AutoField(primary_key=True)
    rec_id = models.ForeignKey("RecDataset", on_delete=models.DO_NOTHING, verbose_name=_("Dataset"))
    ret_id = models.ForeignKey("RetRecordingEventType", on_delete=models.DO_NOTHING, verbose_name=_("Event Type"))
    rtt_id = models.ForeignKey("RttTimezoneCode", on_delete=models.DO_NOTHING, verbose_name=_("Timezone"))
    ree_date = models.DateField(verbose_name=_("Date"))
    ree_time = models.TimeField(blank=True, null=True, verbose_name=_("Time"))
    tea_id = models.ForeignKey("TeaTeamMember", blank=True, null=True, on_delete=models.DO_NOTHING,
                               verbose_name=_("Team Member"))
    ree_notes = models.TextField(blank=True, null=True, verbose_name=_("Notes"))


class RetRecordingEventType(models.Model):
    ret_id = models.AutoField(primary_key=True)
    ret_name = models.CharField(max_length=50, verbose_name=_("Name"))
    ret_desc = models.CharField(max_length=255, verbose_name=_("Description"))


class RscRecordingSchedule(models.Model):
    rsc_id = models.AutoField(primary_key=True)
    rsc_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Recording Schedule"))
    rsc_period = models.BigIntegerField(verbose_name=_("Period"))


class RstRecordingStage(models.Model):
    rst_id = models.AutoField(primary_key=True)
    rst_channel_no = models.BigIntegerField(blank=True, null=True, verbose_name=_("Channel Number"))
    rsc = models.ForeignKey(RscRecordingSchedule, models.DO_NOTHING, verbose_name=_("Schedule"))
    rst_active = models.CharField(max_length=1, verbose_name=_("(A)ctive or (S)leep"))
    rst_duration = models.BigIntegerField(verbose_name=_("Duration"))
    rst_rate = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name=_("Rate (Hz)"))


class RttTimezoneCode(models.Model):
    rtt_id = models.AutoField(primary_key=True)
    rtt_abb = models.CharField(max_length=5, verbose_name=_("Abbreviation"))
    rtt_name = models.CharField(max_length=50, verbose_name=_("Name"))
    rtt_offset = models.DecimalField(max_digits=4, decimal_places=2, verbose_name=_("Offset"))


class TeaTeamMember(models.Model):
    tea_id = models.AutoField(primary_key=True)
    tea_abb = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Abbreviation"))
    tea_last_name = models.CharField(max_length=50, verbose_name=_("Last Name"))
    tea_first_name = models.CharField(max_length=50, verbose_name=_("First Name"))

    class Meta:
        unique_together = (('tea_last_name', 'tea_first_name'),)

    def __str__(self):
        return "{}, {} ({})".format(self.tea_last_name, self.tea_first_name, self.tea_abb)
