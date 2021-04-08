from django.db.models import Sum, Q
from django.utils.translation import gettext as _, gettext_lazy

from lib.templatetags.custom_filters import nz
from shared_models import models as shared_models
from . import models


def get_help_text_dict():
    my_dict = {}
    for obj in models.HelpText.objects.all():
        my_dict[obj.field_name] = str(obj)

    return my_dict


def in_projects_admin_group(user):
    """
    Will return True if user is in project_admin group
    """
    if user:
        return user.groups.filter(name='projects_admin').exists()


def is_management(user):
    """
        Will return True if user is in project_admin group, or if user is listed as a head of a section, division or branch
    """
    if user and user.id:
        return shared_models.Section.objects.filter(head=user).exists() or \
               shared_models.Division.objects.filter(head=user).exists() or \
               shared_models.Branch.objects.filter(head=user).exists()


def is_management_or_admin(user):
    """
        Will return True if user is in project_admin group, or if user is listed as a head of a section, division or branch
    """
    if user.id:
        return in_projects_admin_group(user) or is_management(user)


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


def is_rds(user, project=None):
    if project:
        try:
            return True if project.section.division.branch.head == user else False
        except AttributeError:
            pass
    else:
        return shared_models.Branch.objects.filter(head=user).exists()


def is_project_lead(user, project_id=None, project_year_id=None):
    """
    returns True if user is among the project's project leads
    """
    if user.id:
        project = None
        if project_year_id:
            project = models.ProjectYear.objects.get(pk=project_year_id).project
        elif project_id:
            project = models.Project.objects.get(pk=project_id)

        if project:
            return user in [s.user for s in models.Staff.objects.filter(project_year__project=project, is_lead=True)]


def can_modify_project(user, project_id, return_as_dict=False):
    """
    returns True if user has permissions to delete or modify a project
    The answer of this question will depend on whether the project is submitted. Project leads cannot edit a submitted project
    """
    my_dict = dict(can_modify=False, reason=_("You are not logged in"))

    if user.id:

        my_dict["reason"] = "You are not a project lead or manager of this project"
        project = models.Project.objects.get(pk=project_id)

        # check to see if a superuser or projects_admin -- both are allow to modify projects
        if in_projects_admin_group(user):
            my_dict["reason"] = "You can modify this record because you are a system administrator"
            my_dict["can_modify"] = True

        # check to see if they are a section head
        elif is_section_head(user, project):
            my_dict["reason"] = "You can modify this record because it falls under your section"
            my_dict["can_modify"] = True

        # check to see if they are a div. manager
        elif is_division_manager(user, project):
            my_dict["reason"] = "You can modify this record because it falls under your division"
            my_dict["can_modify"] = True

        # check to see if they are an RDS
        elif is_rds(user, project):
            my_dict["reason"] = "You can modify this record because it falls under your branch"
            my_dict["can_modify"] = True

        # check to see if they are a project lead
        elif is_project_lead(user, project_id=project.id):
            my_dict["reason"] = "You can modify this record because you are a project lead"
            my_dict["can_modify"] = True

        # check to see if they are a project lead
        elif not models.Staff.objects.filter(project_year__project=project, is_lead=True).exists():
            my_dict["reason"] = "You can modify this record because there are currently no project leads"
            my_dict["can_modify"] = True

        return my_dict if return_as_dict else my_dict["can_modify"]


def is_admin_or_project_manager(user, project):
    """returns True if user is either in 'projects_admin' group OR if they are a manager of the project (section head, div. manager, RDS)"""
    if user.id:

        # check to see if a superuser or projects_admin -- both are allow to modify projects
        if "projects_admin" in [g.name for g in user.groups.all()]:
            return True

        # check to see if they are a section head, div. manager or RDS
        if is_section_head(user, project) or is_division_manager(user, project) or is_rds(user, project):
            return True


def get_manageable_sections(user):
    if in_projects_admin_group(user):
        return shared_models.Section.objects.filter(projects2__isnull=False).distinct()
    return shared_models.Section.objects.filter(Q(head=user) | Q(division__head=user) | Q(division__branch__head=user))


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
                          ).filter(**div_kwargs).filter(**reg_kwargs) if s.projects2.count() > 0]
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


def get_user_fte_breakdown(user, fiscal_year_id):
    staff_instances = models.Staff.objects.filter(user=user, project_year__fiscal_year_id=fiscal_year_id)
    my_dict = dict()
    my_dict['name'] = f"{user.last_name}, {user.first_name}"
    my_dict['fiscal_year'] = str(shared_models.FiscalYear.objects.get(pk=fiscal_year_id))
    my_dict['draft'] = nz(staff_instances.filter(
        project_year__status=1
    ).aggregate(dsum=Sum("duration_weeks"))["dsum"], 0)

    my_dict['submitted_unapproved'] = nz(staff_instances.filter(
        project_year__status__in=[2, 3]
    ).aggregate(dsum=Sum("duration_weeks"))["dsum"], 0)

    my_dict['approved'] = nz(staff_instances.filter(
        project_year__status=4
    ).aggregate(dsum=Sum("duration_weeks"))["dsum"], 0)

    return my_dict


def financial_project_year_summary_data(project_year):
    """ this function will return a list, where each row corresponds to a funding source"""
    # for every funding source, we will want to summarize: Salary, O&M, Capital and TOTAL
    my_list = []

    for fs in project_year.get_funding_sources():
        my_dict = dict()
        my_dict["type"] = fs.get_funding_source_type_display()
        my_dict["name"] = str(fs)
        my_dict["salary"] = 0
        my_dict["om"] = 0
        my_dict["capital"] = 0

        # first calc for staff
        for staff in project_year.staff_set.filter(funding_source=fs):
            # exclude any employees that should be excluded. This is a fail safe since the form should prevent data entry
            if not staff.employee_type.exclude_from_rollup:
                if staff.employee_type.cost_type == 1:
                    my_dict["salary"] += nz(staff.amount, 0)
                elif staff.employee_type.cost_type == 2:
                    my_dict["om"] += nz(staff.amount, 0)

        # O&M costs
        for cost in project_year.omcost_set.filter(funding_source=fs):
            my_dict["om"] += nz(cost.amount, 0)

        # Capital costs
        for cost in project_year.capitalcost_set.filter(funding_source=fs):
            my_dict["capital"] += nz(cost.amount, 0)

        my_dict["total"] = my_dict["salary"] + my_dict["om"] + my_dict["capital"]

        my_list.append(my_dict)

    return my_list


def financial_project_summary_data(project):
    my_list = []
    if project.get_funding_sources():
        for fs in project.get_funding_sources():
            my_dict = dict()
            my_dict["type"] = fs.get_funding_source_type_display()
            my_dict["name"] = str(fs)
            my_dict["salary"] = 0
            my_dict["om"] = 0
            my_dict["capital"] = 0

            # first calc for staff
            for staff in models.Staff.objects.filter(funding_source=fs, project_year__project=project):
                # exclude any employees that should be excluded. This is a fail safe since the form should prevent data entry
                if not staff.employee_type.exclude_from_rollup:
                    if staff.employee_type.cost_type == 1:
                        my_dict["salary"] += nz(staff.amount, 0)
                    elif staff.employee_type.cost_type == 2:
                        my_dict["om"] += nz(staff.amount, 0)

            # O&M costs
            for cost in models.OMCost.objects.filter(funding_source=fs, project_year__project=project):
                my_dict["om"] += nz(cost.amount, 0)

            # Capital costs
            for cost in models.CapitalCost.objects.filter(funding_source=fs, project_year__project=project):
                my_dict["capital"] += nz(cost.amount, 0)

            my_dict["total"] = my_dict["salary"] + my_dict["om"] + my_dict["capital"]

            my_list.append(my_dict)

    return my_list


def multiple_financial_project_year_summary_data(project_years):
    my_list = []

    fs_list = list()
    # first get funding source list
    for py in project_years:
        fs_list.extend([fs.id for fs in py.get_funding_sources()])
    funding_sources = models.FundingSource.objects.filter(id__in=fs_list)

    for fs in funding_sources:
        my_dict = dict()
        my_dict["type"] = fs.get_funding_source_type_display()
        my_dict["name"] = str(fs)
        my_dict["salary"] = 0
        my_dict["om"] = 0
        my_dict["capital"] = 0

        for py in project_years:
            # first calc for staff
            for staff in models.Staff.objects.filter(funding_source=fs, project_year=py):
                # exclude any employees that should be excluded. This is a fail safe since the form should prevent data entry
                if not staff.employee_type.exclude_from_rollup:
                    if staff.employee_type.cost_type == 1:
                        my_dict["salary"] += nz(staff.amount, 0)
                    elif staff.employee_type.cost_type == 2:
                        my_dict["om"] += nz(staff.amount, 0)

            # O&M costs
            for cost in models.OMCost.objects.filter(funding_source=fs, project_year=py):
                my_dict["om"] += nz(cost.amount, 0)

            # Capital costs
            for cost in models.CapitalCost.objects.filter(funding_source=fs, project_year=py):
                my_dict["capital"] += nz(cost.amount, 0)

            my_dict["total"] = my_dict["salary"] + my_dict["om"] + my_dict["capital"]

        my_list.append(my_dict)

    return my_list


def get_project_field_list(project):
    is_acrdp = project.is_acrdp
    is_csrf = project.is_csrf
    is_sara = project.is_sara
    general_project = not is_csrf and not is_acrdp and not is_sara

    my_list = [
        'id',
        'section',
        # 'title',
        'overview' if general_project else None,
        # do not call the html field directly or we loose the ability to get the model's verbose name
        'activity_type',
        'functional_group.theme|{}'.format(_("theme")),
        'functional_group',
        'default_funding_source',
        'start_date',
        'end_date',
        'fiscal_years|{}'.format(_("Project years")),
        'funding_sources',
        'lead_staff',

        # acrdp fields
        'overview|{}'.format(gettext_lazy("Project overview / ACRDP objectives")) if is_acrdp else None,
        'organization' if is_acrdp else None,
        'species_involved' if is_acrdp else None,
        'team_description_html|{}'.format(_("description of team and required qualifications (ACRDP)")) if is_acrdp else None,
        'rationale_html|{}'.format(_("project problem / rationale (ACRDP)")) if is_acrdp else None,
        'experimental_protocol_html|{}'.format(_("experimental protocol (ACRDP)")) if is_acrdp else None,

        # csrf fields
        'overview' if is_csrf else None,
        'csrf_theme|{}'.format(_("CSRF theme")) if is_csrf else None,
        'csrf_sub_theme|{}'.format(_("CSRF sub-theme")) if is_csrf else None,
        'csrf_priority|{}'.format(_("CSRF priority")) if is_csrf else None,
        'client_information_html|{}'.format(_("Additional info supplied by client")) if is_csrf else None,
        'second_priority' if is_csrf else None,
        'objectives_html|{}'.format(_("project objectives (CSRF)")) if is_csrf else None,
        'innovation_html|{}'.format(_("innovation (CSRF)")) if is_csrf else None,
        'other_funding_html|{}'.format(_("other sources of funding (CSRF)")) if is_csrf else None,

        # sara fields
        'overview|{}'.format(_("Objectives and methods")) if is_sara else None,
        'reporting_mechanism' if is_sara else None,
        'future_funding_needs' if is_sara else None,

        'tags',
        'references',
        'metadata|{}'.format(_("metadata")),
    ]
    while None in my_list: my_list.remove(None)
    return my_list


def get_project_year_field_list(project_year=None):
    my_list = [
        'dates|dates',
        'priorities',  # do not call the html field directly or we loose the ability to get the model's verbose name
        # 'deliverables',  # do not call the html field directly or we loose the ability to get the model's verbose name

        # SPECIALIZED EQUIPMENT COMPONENT
        #################################
        'requires_specialized_equipment|{}'.format(_("requires specialized equipment?")),
        'technical_service_needs' if not project_year or project_year.requires_specialized_equipment else None,
        'mobilization_needs' if not project_year or project_year.requires_specialized_equipment else None,

        # FIELD COMPONENT
        #################
        'has_field_component|{}'.format(_("has field component?")),
        'vehicle_needs' if not project_year or project_year.has_field_component else None,
        'ship_needs' if not project_year or project_year.has_field_component else None,
        'coip_reference_id' if not project_year or project_year.has_field_component else None,
        'instrumentation' if not project_year or project_year.has_field_component else None,
        'owner_of_instrumentation' if not project_year or project_year.has_field_component else None,
        'requires_field_staff' if not project_year or project_year.has_field_component else None,
        'field_staff_needs' if not project_year or project_year.has_field_component and project_year.requires_field_staff else None,

        # DATA COMPONENT
        ################
        'has_data_component',
        'data_collected' if not project_year or project_year.has_data_component else None,
        'data_products' if not project_year or project_year.has_data_component else None,
        'open_data_eligible' if not project_year or project_year.has_data_component else None,
        'data_storage_plan' if not project_year or project_year.has_data_component else None,
        'data_management_needs' if not project_year or project_year.has_data_component else None,

        # LAB COMPONENT
        ###############
        'has_lab_component',
        'requires_abl_services' if not project_year or project_year.has_lab_component else None,
        'requires_lab_space' if not project_year or project_year.has_lab_component else None,
        'requires_other_lab_support' if not project_year or project_year.has_lab_component else None,
        'other_lab_support_needs' if not project_year or project_year.has_lab_component else None,

        'it_needs|{}'.format(_("special IT requirements")),
        'additional_notes',
        'coding',
        'submitted',
        'formatted_status|{}'.format(_("status")),
        # 'allocated_budget|{}'.format(_("allocated budget")),
        # 'review_score|{}'.format(_("review score")),
        'metadata|{}'.format(_("metadata")),
    ]

    # remove any instances of None
    while None in my_list: my_list.remove(None)

    return my_list


def get_review_field_list():
    my_list = [
        'collaboration_score_html|{}'.format("external pressures score"),
        'strategic_score_html|{}'.format("strategic direction score"),
        'operational_score_html|{}'.format("operational considerations score"),
        'ecological_score_html|{}'.format("ecological impact score"),
        'scale_score_html|{}'.format("scale score"),
        'total_score',
        'comments_for_staff',
        'approval_level',
        'approver_comment',
        'allocated_budget',
        'metadata',
    ]
    return my_list


def get_staff_field_list():
    my_list = [
        'smart_name|{}'.format(_("name")),
        'funding_source',
        'is_lead',
        'employee_type',
        'level',
        'duration_weeks',
        # 'overtime_hours',
        # 'overtime_description',
        # 'student_program',
        'amount',
    ]
    return my_list


def get_citation_field_list():
    my_list = [
        'tname|{}'.format(_("title")),
        'authors',
        'year',
        'publication',
        'pub_number',
        # 'turl|{}'.format(_("url")),
        'tabstract|{}'.format(_("abstract")),
        'series',
        'region',
    ]
    return my_list


def get_om_field_list():
    my_list = [
        'category_type|{}'.format(_("category type")),
        'om_category',
        'description',
        'funding_source',
        'amount',
    ]
    return my_list


def get_capital_field_list():
    my_list = [
        'category',
        'description',
        'funding_source',
        'amount',
    ]
    return my_list


def get_activity_field_list():
    my_list = [
        'type',
        'name',
        'description',
        'target_date',
        'responsible_party',
        'latest_update|{}'.format(_("latest status")),
    ]
    return my_list


def get_collaboration_field_list():
    my_list = [
        'type',
        'new_or_existing',
        'organization',
        'people',
        'critical',
        'agreement_title',
        # 'gc_program',
        # 'amount',
        'notes',
    ]
    return my_list


def get_status_report_field_list():
    my_list = [
        'report_number|{}'.format("number"),
        'status',
        'major_accomplishments_html|{}'.format(_("major accomplishments")),
        'major_issues_html|{}'.format(_("major issues")),
        'target_completion_date',
        'general_comment',
        'supporting_resources|{}'.format(_("supporting resources")),
        'section_head_comment',
        'section_head_reviewed',
        'metadata',
    ]
    return my_list


def get_activity_update_field_list():
    my_list = [
        'activity',
        'status',
        'notes_html|{}'.format("notes"),
        'metadata|{}'.format("meta"),
    ]
    return my_list


def get_file_field_list():
    my_list = [
        'name',
        'ref|{}'.format("reference"),
        'external_url',
        'file',
        'date_created',

    ]
    return my_list


def get_review_score_rubric():
    return {
        "collaboration": {
            1: {
                "criteria": _(
                    "no formal commitments; limited interest from stakeholders; limited opportunity for partnership or collaboration."),
                "examples": _(
                    "No expressed interest or identified as a low priority (or potential conflict) by a stakeholder advisory committee."),
            },
            2: {
                "criteria": _("Informal departmental commitments; some interest from stakeholders; internal collaboration."),
                "examples": _(
                    "Verbal agreement with stakeholders or external partner. Collaboration between internal programs of science staff."),
            },
            3: {
                "criteria": _(
                    "regulatory or legal commitment; high interest from stakeholders; strong opportunity for external partnership and collaboration."),
                "examples": _("Signed G&C agreement with external partner."),
            },
        },
        "strategic": {
            1: {
                "criteria": _("limited long-term value; short-term benefit (fire-fighting)"),
                "examples": _(
                    "Local, archived dataset, with limited likelihood of replication going forward.   No clear link to decision-making."),
            },
            2: {
                "criteria": _("some strategic value to department; medium-term benefit"),
                "examples": _(
                    "Regional dataset of current high value, but potential to be replaced by emerging technology.  Indirect link to decision."),
            },
            3: {
                "criteria": _("high long-term strategic value to the department; high innovation value; broad applicability"),
                "examples": _(
                    "High value/priority, nationally consistent dataset using emerging, more cost effective (emerging) technology.  Clear link to high-priority decision-making."),
            },
        },
        "operational": {
            1: {
                "criteria": _("One-off project; feasible now but not sustainable in the long-term."),
                "examples": _("New data collection. Significant admin work required."),
            },
            2: {
                "criteria": _(
                    "Moderate level of feasibility or operational efficiency, e.g. equipment/tools readily available to be implemented within year"),
                "examples": _("Some processing/analysis required of an existing dataset."),
            },
            3: {
                "criteria": _(
                    "high feasibility, e.g. data availability, expertise, existing monitoring platforms, and regulatory tools available"),
                "examples": _(
                    "Open publication of an existing data layer.  Low administrative burden (e.g. existing agreements in place)."),
            },
        },
        "ecological": {
            1: {
                "criteria": _("limited ecological value, or lower priority species/habitats"),
                "examples": _("Project related to a species or area with limited or unknown ecological role, or of localized interest."),
            },
            2: {
                "criteria": _("Evidence of ecological value, e.g., prey linkages to key species."),
                "examples": _(
                    "Project related to a species or area with known linkages to a species of high ecological value (prey species), or importance identified through ecological modelling."),
            },
            3: {
                "criteria": _("high ecological value (important species) or high ecological risk (SARA-listed species)"),
                "examples": _(
                    "Project related to a nationally or regionally recognized ESS (Eelgrass) or EBSA (Minas Basin), or SAR (Blue Whale)."),
            },
        },
        "scale": {
            1: {
                "criteria": _("limited geographic or temporal scope; site-specific and lessons not readily applicable to other areas"),
                "examples": _("Data only available for a single location or bay."),
            },
            2: {
                "criteria": _("broad geographic/temporal scope; area of some significance"),
                "examples": _("Subregional data layer, e.g., for a single NAFO Unit or MPA."),
            },
            3: {
                "criteria": _("broad geographic or temporal scope; area of high significance"),
                "examples": _("Bioregional data layers, e.g. remote sensing, RV Survey."),
            },
        },

    }


def get_risk_rating(impact, likelihood):
    """This is taken from the ACRDP application form"""
    l = 1
    m = 2
    h = 3
    rating_dict = {
        # impact
        1: {
            # likelihood -- > risk rating
            1: l, 2: l, 3: l, 4: m, 5: m,
        },
        2: {
            1: l, 2: l, 3: m, 4: m, 5: m,
        },
        3: {
            1: l, 2: m, 3: m, 4: m, 5: h,
        },
        4: {
            1: m, 2: m, 3: m, 4: h, 5: h,
        },
        5: {
            1: m, 2: m, 3: h, 4: h, 5: h,
        },
    }
    return rating_dict[impact][likelihood]
