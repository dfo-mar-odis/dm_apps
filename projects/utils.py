from collections import OrderedDict

from django.utils.translation import gettext as _

from lib.templatetags.custom_filters import nz
from shared_models import models as shared_models
from . import models


def get_help_text_dict():
    my_dict = {}
    for obj in models.HelpText.objects.all():
        my_dict[obj.field_name] = str(obj)

    return my_dict
    #
    # help_text_dict = {
    #     "user": _("This field should be used if the staff member is a DFO employee (as opposed to the 'Person name' field)"),
    #     "start_date": _("This is the start date of the project, not the fiscal year"),
    #     "is_negotiable": _("Is this program a part of DFO's core mandate?"),
    #     "is_competitive": _("For example, is the funding for this project coming from a program like ACRDP, PARR, SPERA, etc.?"),
    #     "priorities": _("What will be the project emphasis in this particular fiscal year?"),
    #     "deliverables": _("Please provide this information in bulleted form, if possible."),
    # }


def in_projects_admin_group(user):
    """
    Will return True if user is in project_admin group
    """
    if user:
        return user.groups.filter(name='projects_admin').count() != 0


def is_management_or_admin(user):
    """
        Will return True if user is in project_admin group, or if user is listed as a head of a section, division or branch
    """
    if user.id:
        if in_projects_admin_group(user) or \
                shared_models.Section.objects.filter(head=user).count() > 0 or \
                shared_models.Division.objects.filter(head=user).count() > 0 or \
                shared_models.Branch.objects.filter(head=user).count() > 0:
            return True


def is_section_head(user, project):
    try:
        return True if project.section.head == user else False
    except AttributeError as e:
        print(e)


def is_division_manager(user, project):
    try:
        return True if project.section.division.head == user else False
    except AttributeError:
        pass


def is_rds(user, project):
    try:
        return True if project.section.division.branch.head == user else False
    except AttributeError:
        pass


def is_project_lead(user, project_id):
    """
    returns True if user is among the project's project leads
    """
    if user.id:
        project = models.Project.objects.get(pk=project_id)
        return user in project.project_leads_as_users


def can_modify_project(user, project_id):
    """
    returns True if user has permissions to delete or modify a project

    The answer of this question will depend on whether the project is submitted. Project leads cannot edit a submitted project
    """
    if user.id:
        project = models.Project.objects.get(pk=project_id)

        # check to see if a superuser or projects_admin -- both are allow to modify projects
        if "projects_admin" in [g.name for g in user.groups.all()]:
            return True

        # check to see if they are a section head, div. manager or RDS
        if is_section_head(user, project) or is_division_manager(user, project) or is_rds(user, project):
            return True

        # if the project is unsubmitted, the project lead is also able to edit the project... obviously
        # check to see if they are a project lead
        if not project.submitted and is_project_lead(user, project.id):
            return True


def is_admin_or_project_manager(user, project):
    """returns True if user is either in 'projects_admin' group OR if they are a manager of the project (section head, div. manager, RDS)"""
    if user.id:

        # check to see if a superuser or projects_admin -- both are allow to modify projects
        if "projects_admin" in [g.name for g in user.groups.all()]:
            return True

        # check to see if they are a section head, div. manager or RDS
        if is_section_head(user, project) or is_division_manager(user, project) or is_rds(user, project):
            return True


def get_section_choices(all=False, full_name=True, region_filter=None, division_filter=None):
    if full_name:
        my_attr = "full_name"
    else:
        my_attr = _("name")

    if region_filter:
        reg_kwargs = {
            "division__branch__region_id": region_filter
        }
    else:
        reg_kwargs = {
            "division__branch__region_id__isnull": False
        }

    if division_filter:
        div_kwargs = {
            "division_id": division_filter
        }
    else:
        div_kwargs = {
            "division_id__isnull": False
        }

    if not all:
        my_choice_list = [(s.id, getattr(s, my_attr)) for s in
                          shared_models.Section.objects.all().order_by(
                              "division__branch__region",
                              "division__branch",
                              "division",
                              "name"
                          ).filter(**div_kwargs).filter(**reg_kwargs) if s.projects.count() > 0]
    else:
        my_choice_list = [(s.id, getattr(s, my_attr)) for s in
                          shared_models.Section.objects.filter(
                              division__branch__name__icontains="science").order_by(
                              "division__branch__region",
                              "division__branch",
                              "division",
                              "name"
                          ).filter(**div_kwargs).filter(**reg_kwargs)]

    return my_choice_list


def get_division_choices(all=False, region_filter=None):
    division_list = set(
        [shared_models.Section.objects.get(pk=s[0]).division_id for s in get_section_choices(all=all, region_filter=region_filter)])
    return [(d.id, str(d)) for d in
            shared_models.Division.objects.filter(id__in=division_list).order_by("branch__region", "name")]


def get_region_choices(all=False):
    region_list = set(
        [shared_models.Division.objects.get(pk=d[0]).branch.region_id for d in get_division_choices(all=all)])
    return [(r.id, str(r)) for r in
            shared_models.Region.objects.filter(id__in=region_list).order_by("name", )]


def get_omcatagory_choices():
    return [(o.id, str(o)) for o in models.OMCategory.objects.all()]


def get_funding_sources(all=False):
    return [(fs.id, str(fs)) for fs in models.FundingSource.objects.all()]


def pdf_financial_summary_data(project):
    salary_abase = 0
    om_abase = 0
    capital_abase = 0

    salary_bbase = 0
    om_bbase = 0
    capital_bbase = 0

    salary_cbase = 0
    om_cbase = 0
    capital_cbase = 0

    gc_total = 0

    # first calc for staff
    for staff in project.staff_members.all():
        # exclude full time employees
        if not staff.employee_type.exclude_from_rollup:
            # if the staff member is being paid from bbase...
            if staff.funding_source.id == 1:
                # if salary
                if staff.employee_type.cost_type == 1:
                    salary_abase += nz(staff.cost, 0)
                # if o&M
                elif staff.employee_type.cost_type == 2:
                    om_abase += nz(staff.cost, 0)
            elif staff.funding_source.id == 2:
                # if salary
                if staff.employee_type.cost_type == 1:
                    salary_bbase += nz(staff.cost, 0)
                # if o&M
                elif staff.employee_type.cost_type == 2:
                    om_bbase += nz(staff.cost, 0)
            elif staff.funding_source.id == 3:
                # if salary
                if staff.employee_type.cost_type == 1:
                    salary_cbase += nz(staff.cost, 0)
                # if o&M
                elif staff.employee_type.cost_type == 2:
                    om_cbase += nz(staff.cost, 0)

    # O&M costs
    for cost in project.om_costs.all():
        if cost.funding_source.id == 1:
            om_abase += nz(cost.budget_requested, 0)
        elif cost.funding_source.id == 2:
            om_bbase += nz(cost.budget_requested, 0)
        elif cost.funding_source.id == 3:
            om_cbase += nz(cost.budget_requested, 0)

    # Capital costs
    for cost in project.capital_costs.all():
        if cost.funding_source.id == 1:
            capital_abase += nz(cost.budget_requested, 0)
        elif cost.funding_source.id == 2:
            capital_bbase += nz(cost.budget_requested, 0)
        elif cost.funding_source.id == 3:
            capital_cbase += nz(cost.budget_requested, 0)

    # g&c costs
    for cost in project.gc_costs.all():
        gc_total += nz(cost.budget_requested, 0)

    context = {}
    # abase
    context["salary_abase"] = salary_abase
    context["om_abase"] = om_abase
    context["capital_abase"] = capital_abase

    # bbase
    context["salary_bbase"] = salary_bbase
    context["om_bbase"] = om_bbase
    context["capital_bbase"] = capital_bbase

    # cbase
    context["salary_cbase"] = salary_cbase
    context["om_cbase"] = om_cbase
    context["capital_cbase"] = capital_cbase

    context["salary_total"] = salary_abase + salary_bbase + salary_cbase
    context["om_total"] = om_abase + om_bbase + om_cbase
    context["capital_total"] = capital_abase + capital_bbase + capital_cbase
    context["gc_total"] = gc_total

    # import color schemes from funding_source table
    context["abase"] = models.FundingSourceType.objects.get(pk=1).color
    context["bbase"] = models.FundingSourceType.objects.get(pk=2).color
    context["cbase"] = models.FundingSourceType.objects.get(pk=3).color

    return context


def financial_summary_data(project):
    # for every funding source, we will want to summarize: Salary, O&M, Capital and TOTAL
    my_dict = OrderedDict()

    for fs in project.get_funding_sources():
        my_dict[fs] = {}
        my_dict[fs]["salary"] = 0
        my_dict[fs]["om"] = 0
        my_dict[fs]["capital"] = 0
        my_dict[fs]["total"] = 0

        # first calc for staff
        for staff in project.staff_members.filter(funding_source=fs):
            # exclude any employees that should be excluded. This is a fail safe since the form should prevent data entry
            if not staff.employee_type.exclude_from_rollup:
                if staff.employee_type.cost_type == 1:
                    my_dict[fs]["salary"] += nz(staff.cost, 0)
                elif staff.employee_type.cost_type == 2:
                    my_dict[fs]["om"] += nz(staff.cost, 0)

        # O&M costs
        for cost in project.om_costs.filter(funding_source=fs):
            my_dict[fs]["om"] += nz(cost.budget_requested, 0)

        # Capital costs
        for cost in project.capital_costs.filter(funding_source=fs):
            my_dict[fs]["capital"] += nz(cost.budget_requested, 0)

    # do the totals. I am doing this loop as separate so that the total entry comes at the end of all the funding sources
    my_dict["total"] = {}
    my_dict["total"]["salary"] = 0
    my_dict["total"]["om"] = 0
    my_dict["total"]["capital"] = 0
    my_dict["total"]["total"] = 0
    for fs in project.get_funding_sources():
        my_dict[fs]["total"] = float(my_dict[fs]["capital"]) + float(my_dict[fs]["salary"]) + float(my_dict[fs]["om"])
        my_dict["total"]["salary"] += my_dict[fs]["salary"]
        my_dict["total"]["om"] += my_dict[fs]["om"]
        my_dict["total"]["capital"] += my_dict[fs]["capital"]
        my_dict["total"]["total"] += my_dict[fs]["total"]

    return my_dict


def multiple_projects_financial_summary(project_list):
    my_dict = {}

    # first, get the list of funding sources
    funding_sources = []
    for project in project_list:
        funding_sources.extend(project.get_funding_sources())
    funding_sources = list(set(funding_sources))
    funding_sources_order = ["{} {}".format(fs.funding_source_type, fs.tname) for fs in funding_sources]
    for fs in [x for _, x in sorted(zip(funding_sources_order, funding_sources))]:
        my_dict[fs] = {}
        my_dict[fs]["salary"] = 0
        my_dict[fs]["om"] = 0
        my_dict[fs]["capital"] = 0
        my_dict[fs]["total"] = 0
        for project in project_list.all():
            # first calc for staff
            for staff in project.staff_members.filter(funding_source=fs):
                # exclude any employees that should be excluded. This is a fail safe since the form should prevent data entry
                if not staff.employee_type.exclude_from_rollup:
                    if staff.employee_type.cost_type == 1:
                        my_dict[fs]["salary"] += nz(staff.cost, 0)
                    elif staff.employee_type.cost_type == 2:
                        my_dict[fs]["om"] += nz(staff.cost, 0)
            # O&M costs
            for cost in project.om_costs.filter(funding_source=fs):
                my_dict[fs]["om"] += nz(cost.budget_requested, 0)
            # Capital costs
            for cost in project.capital_costs.filter(funding_source=fs):
                my_dict[fs]["capital"] += nz(cost.budget_requested, 0)

    my_dict["total"] = {}
    my_dict["total"]["salary"] = 0
    my_dict["total"]["om"] = 0
    my_dict["total"]["capital"] = 0
    my_dict["total"]["total"] = 0
    for fs in funding_sources:
        my_dict[fs]["total"] = float(my_dict[fs]["capital"]) + float(my_dict[fs]["salary"]) + float(my_dict[fs]["om"])
        my_dict["total"]["salary"] += my_dict[fs]["salary"]
        my_dict["total"]["om"] += my_dict[fs]["om"]
        my_dict["total"]["capital"] += my_dict[fs]["capital"]
        my_dict["total"]["total"] += my_dict[fs]["total"]

    return my_dict


def get_project_field_list(project=None):
    my_list = [
        'id',
        'year',
        'section',
        'project_title',
        'activity_type',
        'functional_group',
        'default_funding_source',
        'funding_sources|{}'.format(_("Complete list of funding sources")),
        'tags',
        'is_national',
        'status',
        'is_competitive',
        'is_approved',
        'start_date',
        'end_date',
        'description',
        'priorities',
        'deliverables',

        # specialized equipment
        'requires_specialized_equipment',
        'technical_service_needs' if not project or project.requires_specialized_equipment else None,
        'mobilization_needs' if not project or project.requires_specialized_equipment else None,

        # travel
        'has_travel',
        'vehicle_needs' if not project or project.has_travel else None,
        'ship_needs' if not project or project.has_travel else None,
        'coip_reference_id' if not project or project.has_travel else None,
        'instrumentation' if not project or project.has_travel else None,
        'owner_of_instrumentation' if not project or project.has_travel else None,
        'requires_field_staff' if not project or project.has_travel else None,
        'field_staff_needs' if not project or project.has_travel and project.requires_field_staff else None,

        # data
        'has_new_data',
        'data_collection' if not project or project.has_new_data else None,
        'data_products' if not project or project.has_new_data else None,
        'data_storage' if not project or project.has_new_data else None,
        'open_data_eligible' if not project or project.has_new_data else None,
        'regional_dm_needs' if not project or project.has_new_data else None,

        # lab work
        'has_lab_work',
        'abl_services_required' if not project or project.has_lab_work else None,
        'lab_space_required' if not project or project.has_lab_work else None,
        'requires_other_lab_support' if not project or project.has_lab_work else None,
        'other_lab_support_needs' if not project or project.has_lab_work else None,

        'it_needs',
        'notes|{}'.format("additional notes"),
        'coding|Known financial coding',
        'last_modified_by',
        'date_last_modified',
    ]

    # remove any instances of None
    while None in my_list: my_list.remove(None)

    return my_list
