from django import forms

from . import views
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
        if isinstance(obj, models.StaffingPlan):
            self.fields['staffing_plan'].initial = obj
        elif obj:
            self.fields['staffing_plan'].initial = obj.staffing_plan
            self.fields['responsibility_center'].initial = obj.responsibility_center
            self.fields['business_line'].initial = obj.business_line
            self.fields['allotment_code'].initial = obj.allotment_code
            self.fields['line_object'].initial = obj.line_object
            self.fields['project'].initial = obj.project
            self.fields['funding_amount'].initial = obj.funding_amount


class NewStaffingForm(forms.ModelForm):

    region = forms.ChoiceField()
    division = forms.ChoiceField()

    field_order = [
        "fiscal_year", "region", "division", "section", "name", "employee_class_level", "responsibility_center", "staffing_plan_status",
        "funding_type", "work_location", "position_staffing_option", "position_tenure", "position_security",
        "position_linguistic", "position_employment_equity", "position_number", "position_title", "is_key_position",
        "employee_last_name", "employee_first_name", "reports_to", "estimated_start_date", "start_date", "end_date",
        "duration_temporary_coverage", "potential_rollover_date", "allocation", "rd_approval_number",
        "description", "date_last_modified", "last_modified_by",
    ]

    class Meta:
        model = models.StaffingPlan
        exclude = []
        widgets = {
            'estimated_start_date': forms.DateInput(attrs={"type": "date"}),
            'start_date': forms.DateInput(attrs={"type": "date"}),
            'end_date': forms.DateInput(attrs={"type": "date"}),
            'potential_rollover_date': forms.DateInput(attrs={"type": "date"}),
            'date_last_modified': forms.HiddenInput(),
            'last_modified_by': forms.HiddenInput(),

        }

    def __init__(self, *args, **kwargs):
        region_choices = views.get_region_choices(all=True)
        region_choices.insert(0, tuple((None, "---")))
        division_choices = views.get_division_choices(all=True)
        division_choices.insert(0, tuple((None, "---")))
        section_choices = views.get_section_choices(all=True)
        section_choices.insert(0, tuple((None, "---")))

        super().__init__(*args, **kwargs)
        self.fields['region'].choices = region_choices

        # even though these are overwritten by js scripts you have to define these so that the validation kicks in properly
        self.fields['division'].choices = division_choices
        self.fields['section'].choices = section_choices

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
