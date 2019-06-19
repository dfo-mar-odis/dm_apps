from django.contrib import admin
from .models import StaffingPlanStatus, EmployeeClassesLevel, EmployeeClassesLevelsPayRate, PositionStaffingOption, \
    PositionTenure, PositionSecurity, PositionLinguisticRequirement, PositionEmploymentEquityRequirement, \
    FundingType, WorkLocation, StaffingPlan, StaffingPlanFunding

from shared_models.models import ResponsibilityCenter, Division, Branch, Section, FiscalYear

# admin.site.register(EmployeeClassesLevel)
# admin.site.register(EmployeeClassesLevelsPayRate)
# admin.site.register(PositionType)
# admin.site.register(FiscalYear)
# admin.site.register(Division)
# admin.site.register(Section)
# admin.site.register(ResponsibilityCenter)
# admin.site.register(StaffingPlan)


@admin.register(StaffingPlanStatus)
class StaffingPlanStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('code', 'name',)


@admin.register(EmployeeClassesLevel)
class EmployeeClassesLevelAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(EmployeeClassesLevelsPayRate)
class EmployeeClassesLevelsPayRatesAdmin(admin.ModelAdmin):
    list_display = ('employee_class_level', 'pay_increment', 'pay_amount')
    list_filter = ('employee_class_level', 'pay_increment')
    search_fields = ('employee_class_level__code', 'employee_class_level__name')
    raw_id_fields = ('employee_class_level',)
    ordering = ('employee_class_level', 'pay_increment', 'pay_amount')


@admin.register(PositionStaffingOption)
class PositionStaffingOptionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(PositionTenure)
class PositionTenureAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(PositionSecurity)
class PositionSecurityAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(PositionLinguisticRequirement)
class PositionLinguisticRequirementAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(PositionEmploymentEquityRequirement)
class PositionEmploymentEquityRequirementAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(FundingType)
class FundingTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(WorkLocation)
class WorkLocationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_filter = ('name',)
    search_fields = ('code', 'name')
    ordering = ('name',)


@admin.register(StaffingPlan)
class StaffingPlanAdmin(admin.ModelAdmin):
    list_display = (
        'fiscal_year', 'name', 'section', 'responsibility_center', 'staffing_plan_status', 'funding_type', 'work_location', 'position_staffing_option',
        'position_tenure', 'position_security',
        'position_linguistic', 'position_employment_equity', 'position_number', 'position_title',
        'is_key_position', 'employee_last_name', 'employee_first_name', 'reports_to', 'estimated_start_date',
        'start_date', 'end_date',
        'allocation', 'rd_approval_number',
        'description')
    list_filter = (
        'fiscal_year', 'name', 'section', 'responsibility_center', 'staffing_plan_status', 'funding_type', 'work_location', 'position_staffing_option',
        'position_tenure', 'position_security',
        'position_linguistic', 'position_employment_equity', 'position_number', 'position_title',
        'is_key_position', 'employee_last_name', 'employee_first_name', 'reports_to', 'estimated_start_date',
        'start_date', 'end_date',
        'allocation', 'rd_approval_number',
        'description')
    search_fields = (
        'fiscal_year__code', 'name', 'fiscal_year__name', 'section__code', 'section__name', 'responsibility_center__code',
        'responsibility_centre__name', 'staffing_plan_status__code', 'staffing_plan_status__name', 'funding_type__code', 'funding_type__name',
        'work_location__code', 'work_location__name', 'position_staffing_option__code',
        'position_staffing_option__name', 'position_tenure__code','position_staffing_tenure__name', 'position_security__code',
        'position_security__name', 'position_linguistic__code', 'position_linguistic__name', 'position_employment_equity__code',
        'position_employment_equity__name', 'position_number', 'position_title',
        'is_key_position', 'employee_last_name', 'employee_first_name', 'reports_to__name', 'estimated_start_date',
        'start_date', 'end_date',
        'allocation', 'rd_approval_number',
        'description')
    raw_id_fields = (
        'fiscal_year', 'section', 'responsibility_center', 'staffing_plan_status', 'funding_type', 'work_location', 'position_staffing_option',
        'position_tenure', 'position_security',
        'position_linguistic', 'position_employment_equity', 'reports_to', 'work_location')
    ordering = ('-fiscal_year', 'responsibility_center', 'position_number')


@admin.register(StaffingPlanFunding)
class StaffingPlanFundingAdmin(admin.ModelAdmin):

    list_display = (
        'staffing_plan', 'responsibility_center', 'business_line', 'allotment_code', 'line_object', 'project',
        'funding_amount')
    list_filter = (
        'staffing_plan', 'responsibility_center', 'business_line', 'allotment_code', 'line_object', 'project')
    search_fields = (
        'staffing_plan', 'responsibility_center', 'business_line', 'allotment_code', 'line_object', 'project')
    raw_id_fields = ('staffing_plan',)
    ordering = ('staffing_plan', 'responsibility_center', 'business_line', 'allotment_code', 'line_object', 'project',
                'funding_amount')
