from django import forms
from . import models


class FundingForm(forms.ModelForm):

    class Meta:
        model = models.StaffingPlanFunding
        exclude = []
        widgets = {
            'staffing_plan': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'initial' not in kwargs or 'object' not in kwargs['initial']:
            return

        obj = kwargs['initial']['object']
        print(obj)
        print(self.fields)
        self.fields['staffing_plan'].initial = obj


class NewStaffingForm(forms.ModelForm):

    field_order = [
        "fiscal_year", "section", "name", "employee_class_level", "responsibility_center", "staffing_plan_status", "funding_type",
        "work_location", "position_staffing_option", "position_tenure", "position_security", "position_linguistic",
        "position_employment_equity", "position_number", "position_title", "is_key_position", "employee_last_name",
        "employee_first_name", "reports_to", "estimated_start_date", "start_date", "end_date",
        "duration_temporary_coverage", "potential_rollover_date", "allocation", "rd_approval_number",
        "description", "date_last_modified", "last_modified_by",
    ]

    class Meta:
        model = models.StaffingPlan
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'initial' not in kwargs or 'object' not in kwargs['initial']:
            return

        obj = kwargs['initial']['object']
        if obj:
            attrs = [[str(o).replace("_id", ""), vars(obj)[o]] for o in vars(obj)]
            for i in range(2, len(attrs)):
                key = attrs[i][0]
                if key != 'last_modified_by' and key != 'date_last_modified':
                    val = attrs[i][1]
                    self.fields[key].initial = val
