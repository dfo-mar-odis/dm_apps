from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from shared_models import models as shared_models
from projects import models as project_models

# Create your models here.


# Choices for language
ENG = 1
FRE = 2
LANGUAGE_CHOICES = (
    (ENG, 'English'),
    (FRE, 'French'),
)


class Lookup(models.Model):

    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="name")

    def __str__(self):
        return "{} ({})".format(self.code, self.name)

    class Meta:
        abstract = True
        ordering = ['name', ]


class StaffingPlanStatus(Lookup):
    pass


class EmployeeClassesLevel(Lookup):
    pass


class PositionStaffingOption(Lookup):
    pass


class PositionTenure(Lookup):
    pass


class PositionSecurity(Lookup):
    pass


class PositionLinguisticRequirement(Lookup):
    pass


class PositionEmploymentEquityRequirement(Lookup):
    pass


class FundingType(Lookup):
    pass


class WorkLocation(Lookup):
    pass


class EmployeeClassesLevelsPayRate(models.Model):
    employee_class_level = models.ForeignKey(EmployeeClassesLevel, on_delete=models.DO_NOTHING, blank=True, null=True,
                                             verbose_name="employee class and level")
    pay_increment = models.IntegerField(verbose_name="Pay Increment", blank=True, null=True)
    pay_amount = models.FloatField(verbose_name="Annual Pay", blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.employee_class_level, self.pay_increment, self.pay_amount)

    class Meta:
        ordering = ['employee_class_level', 'pay_increment']


class StaffingPlan(models.Model):
    fiscal_year = models.ForeignKey(shared_models.FiscalYear, on_delete=models.DO_NOTHING, blank=True, null=True,
                                    verbose_name="fiscal year")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='short name for planned staffing (<255 characters)')
    section = models.ForeignKey(shared_models.Section, on_delete=models.DO_NOTHING, blank=True, null=True,
                                verbose_name="section")
    employee_class_level = models.ForeignKey(EmployeeClassesLevel, on_delete=models.DO_NOTHING, blank=True, null=True,
                                             verbose_name="employee class and level")

    responsibility_center = models.ForeignKey(shared_models.ResponsibilityCenter, on_delete=models.DO_NOTHING,
                                              blank=True,
                                              null=True,
                                              verbose_name="responsibility center (if known)")
    staffing_plan_status = models.ForeignKey(StaffingPlanStatus, on_delete=models.DO_NOTHING,
                                             blank=True,
                                             null=True,
                                             verbose_name="staffing plan status")
    funding_type = models.ForeignKey(project_models.FundingSource, on_delete=models.DO_NOTHING,
                                     blank=True,
                                     null=True,
                                     verbose_name="funding type")
    work_location = models.ForeignKey(WorkLocation, on_delete=models.DO_NOTHING, blank=True, null=True,
                                      verbose_name='work location')
    position_staffing_option = models.ForeignKey(PositionStaffingOption, on_delete=models.DO_NOTHING,
                                                 blank=True,
                                                 null=True,
                                                 verbose_name="position staffing option")
    position_tenure = models.ForeignKey(PositionTenure, on_delete=models.DO_NOTHING,
                                        blank=True,
                                        null=True,
                                        verbose_name="position tenure"
                                        )
    position_security = models.ForeignKey(PositionSecurity, on_delete=models.DO_NOTHING,
                                          blank=True,
                                          null=True,
                                          verbose_name="position security requirement")
    position_linguistic = models.ForeignKey(PositionLinguisticRequirement, on_delete=models.DO_NOTHING, blank=True,
                                            null=True, verbose_name='linguistic requirement')
    position_employment_equity = models.ForeignKey(PositionEmploymentEquityRequirement, on_delete=models.DO_NOTHING,
                                                   blank=True, null=True, verbose_name='employment equity requirement')
    position_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="position number")
    position_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="position title")
    is_key_position = models.BooleanField(verbose_name='is key position', null=False, blank=False, default=False)
    employee_last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="employee last name")
    employee_first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="employee first name")
    reports_to = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING,
                                   related_name='reports_to_manager',
                                   verbose_name='manager')
    estimated_start_date = models.DateField(blank=True, null=True, verbose_name="start date (estimated)")
    # financial information goes here.
    start_date = models.DateField(blank=True, null=True, verbose_name="start date (actual)")
    end_date = models.DateField(blank=True, null=True, verbose_name="end date (actual)")
    duration_temporary_coverage = models.IntegerField(blank=True, null=True,
                                                      verbose_name='duration of temporary coverage based on end date (months)')
    potential_rollover_date = models.DateField(blank=True, null=True,
                                               verbose_name="potential rollover date based on start date")
    allocation = models.FloatField(verbose_name="allocation (0 - 1.00)", blank=True, null=True)
    rd_approval_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="RDS approval number")
    description = models.TextField(blank=True, null=True, verbose_name="Staffing Request Notes")
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now,
                                              verbose_name="date last modified")
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, verbose_name="last modified by",
                                         null=True)

    def __str__(self):
        return "{} ({})".format(self.fiscal_year, self.name )

    class Meta:
        ordering = ['fiscal_year__name', 'responsibility_center__name', 'position_number', 'position_title']


class StaffingPlanFunding(models.Model):
    staffing_plan = models.ForeignKey(StaffingPlan, related_name="staff_funding", on_delete=models.DO_NOTHING, blank=False, null=False,
                                      verbose_name='staffing_plan')
    responsibility_center = models.ForeignKey(shared_models.ResponsibilityCenter, on_delete=models.DO_NOTHING)
    business_line = models.ForeignKey(shared_models.BusinessLine, on_delete=models.DO_NOTHING)
    allotment_code = models.ForeignKey(shared_models.AllotmentCode, on_delete=models.DO_NOTHING)
    line_object = models.ForeignKey(shared_models.LineObject, on_delete=models.DO_NOTHING, blank=True, null=True)
    project = models.ForeignKey(shared_models.Project, on_delete=models.DO_NOTHING)

    # financial_coding = models.CharField(max_length=255, blank=True, null=True, verbose_name='financial coding')
    funding_amount = models.FloatField(blank=False, null=False, verbose_name='funding amount ($)')

    def __str__(self):
        return "{} ({}-{}-{}-{}-{}): {}".format(self.staffing_plan, self.responsibility_center, self.business_line,
                                self.allotment_code, self.line_object, self.project, self.funding_amount)

    class Meta:
        ordering = ['staffing_plan', 'responsibility_center', 'business_line', 'allotment_code', 'line_object',
                    'project', 'funding_amount']
