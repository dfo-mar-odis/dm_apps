from django_filters import FilterSet
from . import models


class StaffingPlanFilter(FilterSet):

    class Meta:
        model = models.StaffingPlan
        fields = [
            "fiscal_year", "section",  "employee_class_level", "name", "responsibility_center", "staffing_plan_status", "funding_type",
            "work_location", "position_staffing_option", "position_tenure", "position_security", "position_linguistic",
            "position_employment_equity", "position_number", "position_title", "is_key_position", "employee_last_name",
            "employee_first_name", "reports_to", "estimated_start_date", "start_date", "end_date",
            "duration_temporary_coverage", "potential_rollover_date", "allocation", "rd_approval_number",
            "description", "date_last_modified", "last_modified_by",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
