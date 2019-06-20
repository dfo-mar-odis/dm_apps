import os

from django.db import models
from staff import models as staff_models


def loadModel(src_model, des_model):
    val_array = src_model.objects.using('tmp').all()
    for val in val_array:
        if not des_model.objects.filter(name=val.name):
            des_model(code=val.code, name=val.name).save()


class CLookup(models.Model):

    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="name")

    def __str__(self):
        return "{} ({})".format(self.code, self.name)

    class Meta:
        abstract = True
        ordering = ['name', ]


class CWorkLocation(CLookup):

    class Meta:
        db_table = 'staffing_worklocation'


class CPositionEmploymentEquityRequirement(CLookup):
    class Meta:
        db_table = 'staffing_positionemploymentequityrequirement'


class CStaffingPlanStatus(CLookup):
    class Meta:
        db_table = 'staffing_staffingplanstatus'


class CEmployeeClassesLevel(CLookup):
    class Meta:
        db_table = 'staffing_employeeclasseslevel'


class CPositionStaffingOption(CLookup):
    class Meta:
        db_table = 'staffing_positionstaffingoption'


class CPositionTenure(CLookup):
    class Meta:
        db_table = 'staffing_positiontenure'


class CPositionSecurity(CLookup):
    class Meta:
        db_table = 'staffing_positionsecurity'


class CPositionLinguisticRequirement(CLookup):
    class Meta:
        db_table = 'staffing_positionLinguisticrequirement'


loadModel(CWorkLocation, staff_models.WorkLocation)
loadModel(CPositionEmploymentEquityRequirement, staff_models.PositionEmploymentEquityRequirement)
loadModel(CStaffingPlanStatus, staff_models.StaffingPlanStatus)
loadModel(CEmployeeClassesLevel, staff_models.EmployeeClassesLevel)
loadModel(CPositionStaffingOption, staff_models.PositionStaffingOption)
loadModel(CPositionTenure, staff_models.PositionTenure)
loadModel(CPositionSecurity, staff_models.PositionSecurity)
loadModel(CPositionLinguisticRequirement, staff_models.PositionLinguisticRequirement)

script_dir = os.path.dirname(__file__)
data_funding = r'data\FundingCodes.csv'
f = open(os.path.join(script_dir, data_funding))

header = False
for l in f:
    if not header:
        header = True
        continue

    array = l.replace("\n", "").split(",")
    key = array[0]

    ep_level = staff_models.EmployeeClassesLevel.objects.get(code=key)
    for r in range(1, len(array)):
        if array[r]:
            try:
                ep_rate = staff_models.EmployeeClassesLevelsPayRate.objects.get(employee_class_level=ep_level,
                                                                                pay_increment=r)
                ep_rate.pay_amount = float(array[r])
            except staff_models.EmployeeClassesLevelsPayRate.DoesNotExist:
                ep_rate = staff_models.EmployeeClassesLevelsPayRate(employee_class_level=ep_level, pay_increment=r,
                                                                    pay_amount=float(array[r]))
            ep_rate.save()
