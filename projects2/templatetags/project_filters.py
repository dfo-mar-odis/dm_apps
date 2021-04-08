from django import template

register = template.Library()


@register.filter
def is_markdown_field(value):
    target_field_list = [
        # project
        'overview',
        ## CSRF
        'objectives',
        'innovation',
        'other_funding',
        ## ACRDP
        'team_description',
        'rationale',
        'experimental_protocol',

        # project-year
        'deliverables',
        'priorities',
        'technical_service_needs',
        'mobilization_needs',
        'vehicle_needs',
        'ship_needs',
        'field_staff_needs',
        'instrumentation',
        'data_collected',
        'data_products',
        'data_storage_plan',
        'data_management_needs',
        'other_lab_support_needs',
        'it_needs',

        # status report
        'major_accomplishments',
        'major_issues',

        # activity update
        'notes',

    ]
    return value in target_field_list


@register.filter
def in_field_group(value, arg):
    if arg == "specialized_equipment":
        if value in [
            "technical_service_needs",
            "mobilization_needs"
        ]:
            return True
    elif arg == "field":
        if value in [
            "vehicle_needs",
            "ship_needs",
            "coip_reference_id",
            "instrumentation",
            "owner_of_instrumentation",
            "requires_field_staff",
            "field_staff_needs",
        ]:
            return True
    elif arg == "data":
        if value in [
            "data_collected",
            "data_products",
            "open_data_eligible",
            "data_storage_plan",
            "data_management_needs",
        ]:
            return True
    elif arg == "lab":
        if value in [
            "requires_abl_services",
            "requires_lab_space",
            "requires_other_lab_support",
            "other_lab_support_needs",
        ]:
            return True


@register.filter
def strip_label(val):
    try:
        return val.split("|")[0]
    except:
        return val