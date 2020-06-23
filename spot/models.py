import datetime
import os

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from lib.functions.custom_functions import truncate
from lib.functions.custom_functions import fiscal_year
from lib.templatetags.custom_filters import nz
from shared_models import models as shared_models
from masterlist import models as ml_models
from sar_search import models as sar_models


class Status(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("name (French)"))
    color = models.CharField(max_length=15, blank=True, null=True)
    old_id = models.IntegerField(blank=True, null=True)
    description_text = models.CharField(max_length=250, blank=True, null=True)



    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = [_('name'), ]


class Program(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("name (French)"))
    abbrev_eng = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("abbreviation (French)"))
    abbrev_fre = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("abbreviation (French)"))

    def __str__(self):
        # # check to see if a french value is given
        # if getattr(self, str(_("name"))):
        #     return "{}".format(getattr(self, str(_("name"))))
        # # if there is no translated term, just pull from the english field
        # else:
        #     return "{}".format(self.name)
        return "{} ({})".format(self.name, self.abbrev_eng)

    @property
    def full_eng(self):
        return "{} ({})".format(self.name, self.abbrev_eng)

    @property
    def full_fre(self):
        return "{} ({})".format(self.nom, self.abbrev_fre)

    class Meta:
        ordering = [_('name'), ]


class RiskAssessmentScore(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("name (French)"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = [_('name'), ]


class InitiationType(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("name (French)"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = [_('name'), ]


class PriorityAreaOrThreat(models.Model):
    # choices for type
    THREAT = 1
    PRIORITY = 2
    SPECIES = 3
    TYPE_CHOICES = (
        (THREAT, _("Threat")),
        (PRIORITY, _("Priority area")),
        (SPECIES, _("Priority species")),
    )
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("name (French)"))
    type = models.IntegerField(blank=True, null=True, choices=TYPE_CHOICES)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{} ({})".format(
                getattr(self, str(_("name"))),
                self.get_type_display(),
            )
        # if there is no translated term, just pull from the english field
        else:
            return "{} ({})".format(self.name, self.get_type_display())

    class Meta:
        ordering = ['type', _('name'), ]


def draft_ca_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/entry_<id>/<filename>
    suffix = filename.split(".")[1]
    return 'spot/{0}/{0}_draft_contribution_agreement.{1}'.format(instance.id, suffix)


class Activity(models.Model):
    #choices for habitat
    FW = 1
    MAR =2
    HABITAT_CHOICES = (
        (FW, _("Freshwater")),
        (MAR, _("Marine")),
    )

    program = models.ForeignKey(Program, on_delete=models.DO_NOTHING, related_name="activities", verbose_name=_("funding program"),
                                blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("name (French)"))
    habitat = models.IntegerField(blank=True, null=True, choices=HABITAT_CHOICES)
    category_eng = models.CharField(max_length=1000, verbose_name=_("category/type (English)"))
    category_fre = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("category/type (French)"))

    def __str__(self):
        # check to see if a french value is given
        my_str = "{}".format(getattr(self, str(_("category_eng"))))

        if self.habitat:
            my_str += " ({}) - ".format(self.get_habitat_display())
        else:
            my_str += " - "

        my_str +=  "{}".format(getattr(self, str(_("name"))))
        return my_str

    class Meta:
        ordering = ["program", _('category_eng'), _('name'), ]



class DrainageBasin(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("name (French)"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = [_('name'), ]


class Watershed(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("name (French)"))
    province = models.ForeignKey(shared_models.Province, on_delete=models.DO_NOTHING, related_name="watersheds")
    drainage_basin = models.ForeignKey(DrainageBasin, on_delete=models.DO_NOTHING, related_name="watersheds")
    notes = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("notes"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}, {} ({})".format(getattr(self, str(_("name"))), self.province.tabbrev, self.drainage_basin)
        # if there is no translated term, just pull from the english field
        else:
            return "{}, {} ({})".format(self.name, self.province.tabbrev, self.drainage_basin)

    class Meta:
        ordering = [_('name'), ]


class Project(models.Model):
    path_number = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("DFO PATH #"))
    program_reference_number = models.CharField(max_length=50, blank=True, null=True)
    organization = models.ForeignKey(ml_models.Organization, on_delete=models.DO_NOTHING, related_name="projects")
    program = models.ForeignKey(Program, on_delete=models.DO_NOTHING, related_name="projects", verbose_name=_("funding program"))
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name="projects", default=1, verbose_name=_("project status"))
    regions = models.ManyToManyField(shared_models.Region, default=1, verbose_name=_("DFO regions"))
    start_year = models.ForeignKey(shared_models.FiscalYear, on_delete=models.DO_NOTHING, related_name="gc_projects",
                                   default=fiscal_year(sap_style=True, next=True))
    project_length = models.IntegerField(blank=True, null=True)
    date_completed = models.DateTimeField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True, verbose_name=_("summary"))
    old_id = models.IntegerField(blank=True, null=True)
    eccc_id = models.CharField(max_length=50, blank=True, null=True)

    ## Initiation
    language = models.ForeignKey(shared_models.Language, on_delete=models.DO_NOTHING, related_name="projects",
                                 verbose_name=_("project language"))
    title = models.TextField()
    title_abbrev = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("title abbreviation"))
    initiation_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    initiation_type = models.ForeignKey(InitiationType, on_delete=models.DO_NOTHING, related_name="projects", blank=True, null=True,
                                        verbose_name=_("type of initiation"))
    priority_area_or_threats = models.ManyToManyField(PriorityAreaOrThreat, related_name="projects", blank=True,
                                                      verbose_name=_("priority areas or threats"))
    initiation_acknowledgement_sent = models.DateTimeField(blank=True, null=True, verbose_name=_("acknowledgement email sent"))
    requested_funding_y1 = models.FloatField(blank=True, null=True, verbose_name=_("requested funding (year 1)"))
    requested_funding_y2 = models.FloatField(blank=True, null=True, verbose_name=_("requested funding (year 2)"))
    requested_funding_y3 = models.FloatField(blank=True, null=True, verbose_name=_("requested funding (year 3)"))
    requested_funding_y4 = models.FloatField(blank=True, null=True, verbose_name=_("requested funding (year 4)"))
    requested_funding_y5 = models.FloatField(blank=True, null=True, verbose_name=_("requested funding (year 5)"))
    overview = models.TextField(blank=True, null=True, verbose_name=_("project overview"))

    ## Regional Review
    regional_score = models.FloatField(blank=True, null=True, verbose_name=_("regional score"))
    rank = models.IntegerField(blank=True, null=True, verbose_name=_("project rank"))
    application_submission_date = models.DateTimeField(blank=True, null=True, verbose_name=_("Date/time of application submission"))
    submission_accepted = models.NullBooleanField(verbose_name=_("was the submission accepted?"))
    notes = models.TextField(blank=True, null=True, verbose_name=_("project notes"))
    recommended_funding_y1 = models.FloatField(blank=True, null=True, verbose_name=_("recommended funding amount - Year 1"))
    recommended_funding_y2 = models.FloatField(blank=True, null=True, verbose_name=_("recommended funding amount - Year 2"))
    recommended_funding_y3 = models.FloatField(blank=True, null=True, verbose_name=_("recommended funding amount - Year 3"))
    recommended_funding_y4 = models.FloatField(blank=True, null=True, verbose_name=_("recommended funding amount - Year 4"))
    recommended_funding_y5 = models.FloatField(blank=True, null=True, verbose_name=_("recommended funding amount - Year 5"))
    recommended_overprogramming = models.FloatField(blank=True, null=True, verbose_name=_("recommended amount for over-programming"))
    regrets_or_op_letter_sent_date = models.DateTimeField(blank=True, null=True,
                                                          verbose_name=_("client notification sent (OP or Regrets only)"))

    ## Negotiations
    risk_assessment_score = models.ForeignKey(RiskAssessmentScore, on_delete=models.DO_NOTHING, related_name="projects", blank=True,
                                              null=True)
    negotiations_workplan_completion_date = models.DateTimeField(blank=True, null=True, verbose_name=_("negotiation workplan complete"))
    negotiations_financials_completion_date = models.DateTimeField(blank=True, null=True, verbose_name=_("negotiation financials complete"))
    negotiation_letter_sent = models.DateTimeField(blank=True, null=True, verbose_name=_("negotiation letter sent to client"))

    ## CA Assembly
    schedule_5_complete = models.DateTimeField(blank=True, null=True, verbose_name=_("schedule 5 is complete"))
    advance_payment = models.BooleanField(default=True, verbose_name=_("will this project receive an advance payment?"))
    draft_ca_sent_to_proponent = models.DateTimeField(blank=True, null=True, verbose_name=_("draft CA sent to client"))
    draft_ca_proponent_approved = models.DateTimeField(blank=True, null=True, verbose_name=_("draft CA approved by client"))
    draft_ca_ready = models.DateTimeField(blank=True, null=True, verbose_name=_("draft CA ready"))
    ## CA Checklist stuff
    draft_ca_sent_to_manager = models.DateTimeField(blank=True, null=True, verbose_name=_("draft CA sent to manager"))
    draft_ca_manager_approved = models.DateTimeField(blank=True, null=True, verbose_name=_("draft CA approved by manager"))
    draft_ca_sent_to_nhq = models.DateTimeField(blank=True, null=True, verbose_name=_("draft CA sent to NHQ"))
    aip_received = models.DateTimeField(blank=True, null=True, verbose_name=_("approve-in-principal (AIP) received"))
    final_ca_received = models.DateTimeField(blank=True, null=True, verbose_name=_("final CA received from NHQ"))
    final_ca_sent_to_proponent = models.DateTimeField(blank=True, null=True, verbose_name=_("final CA sent to client"))
    final_ca_proponent_signed = models.DateTimeField(blank=True, null=True, verbose_name=_("final CA signed by client"))
    final_ca_sent_to_nhq = models.DateTimeField(blank=True, null=True, verbose_name=_("final CA sent to HNQ"))
    advance_payment_sent_to_nhq = models.DateTimeField(blank=True, null=True, verbose_name=_("advance payment sent to NHQ"))
    final_ca_nhq_signed = models.DateTimeField(blank=True, null=True, verbose_name=_("final CA signed by NHQ"))

    # meta
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"),
                                         related_name="gc_projects")
    people = models.ManyToManyField(ml_models.Person, through="ProjectPerson", blank=True)
    activities = models.ManyToManyField(Activity, blank=True, verbose_name=_("activities"))
    spp = models.ManyToManyField(sar_models.Species, blank=True, verbose_name=_("species"))
    watersheds = models.ManyToManyField(Watershed, blank=True, verbose_name=_("watersheds"))

    def __str__(self):
        return "{} ({})".format(truncate(self.title, 50), self.organization.abbrev)

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()

        # determine status
        self.status_id = determine_project_status(self)

        # determine length
        self.project_length = determine_project_length(self, self.status_id)

        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-start_year", "program"]

    @property
    def total_requested_funding(self):
        return sum([
            nz(self.requested_funding_y1, 0),
            nz(self.requested_funding_y2, 0),
            nz(self.requested_funding_y3, 0),
            nz(self.requested_funding_y4, 0),
            nz(self.requested_funding_y5, 0),
        ])

    @property
    def total_recommended_funding(self):
        return sum([
            nz(self.recommended_funding_y1, 0),
            nz(self.recommended_funding_y2, 0),
            nz(self.recommended_funding_y3, 0),
            nz(self.recommended_funding_y4, 0),
            nz(self.recommended_funding_y5, 0),
        ])

    @property
    def total_project_funding(self):
        if self.years:
            return sum([nz(f.annual_funding, 0) for f in self.years.all()])
        else:
            return 0

    @property
    def negotiation_completion_date(self):
        """ this will be the max of negotiations_workplan_completion_date and negotiations_financials_completion_date"""
        return max(self.negotiations_workplan_completion_date, self.negotiations_financials_completion_date)

    @property
    def end_year(self):
        return self.years.order_by("fiscal_year").last().fiscal_year.full

    # PEOPLE
    @property
    def pp(self):
        return self.project_people.get(role=1).person

    @property
    def gc_officer(self):
        return self.project_people.get(role=7).person

    # FILES
    @property
    def application_file(self):
        return File.objects.get(project=self, file_type_id=6)

    @property
    def project_evaluation_file(self):
        return File.objects.get(project=self, file_type_id=8)

    @property
    def risk_assessment_file(self):
        return File.objects.get(project=self, file_type_id=4)

    @property
    def draft_ca_file(self):
        return File.objects.get(project=self, file_type_id=1)

    @property
    def fully_signed_ca_file(self):
        return File.objects.get(project=self, file_type_id=2)


class Role(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Name (French)"))
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = [_('order'), ]


class ProjectPerson(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_people")
    person = models.ForeignKey(ml_models.Person, on_delete=models.DO_NOTHING, related_name="project_people")
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, related_name="project_people")

    # meta
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = ['project', 'person', 'role']
        ordering = ['project', 'role', 'person']


class ContributionAgreementChecklist(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name="ca_checklist")
    date_assessed = models.DateTimeField(blank=True, null=True, default=timezone.now)
    risk_assessment_complete = models.NullBooleanField(verbose_name=_("The risk assessment has been completed/approved and posted to PATH"))
    correct_clause_selected = models.NullBooleanField(
        verbose_name=_("The clauses selected in the CA reflect the risk level and contribution amount"))
    formatting_correct = models.NullBooleanField(verbose_name=_("There are no hanging/orphan lines/titles"))
    amounts_correct = models.NullBooleanField(verbose_name=_(
        "The annual contribution amount(s) (3.1) match(es) the budget in Schedule 5 and do(es) not exceed the amount(s) approved by the Minister"))
    clear_language = models.NullBooleanField(
        verbose_name=_("Schedule 5: Language is clear, concise and can be generally understood by someone who is not a specialist"))
    acronyms_defined = models.NullBooleanField(verbose_name=_("Schedule 5: Acronyms are defined upon first use"))
    activities_elibigle = models.NullBooleanField(verbose_name=_("Schedule 5: All Activities/tasks are eligible"))
    detail_commensurate_with_budget = models.NullBooleanField(
        verbose_name=_("Schedule 5: The level of detail for each Activity (i.e., task description) is commensurate with its budget"))
    realistic_timeframe = models.NullBooleanField(
        verbose_name=_("Schedule 5: Each Activity can be reasonably expected to be completed within its accorded timeframe"))
    key_tasks_outlined = models.NullBooleanField(
        verbose_name=_("Schedule 5: All key tasks required to be undertaken for each Activity to be achieved are outlined"))
    deliverables = models.NullBooleanField(verbose_name=_(
        "Schedule 5: All Activities/tasks have associated deliverables that will demonstrate that the former were completed as planned and as budgeted"))
    project_budgets_adds_up = models.NullBooleanField(
        verbose_name=_("Schedule 5: The sum of all individual project Activity budgets adds up to the agreement total"))
    sufficient_budget_detail = models.NullBooleanField(
        verbose_name=_("Schedule 5: Sufficient budget details have been provided to confirm that the costs are eligible and reasonable"))
    expenses_eligible = models.NullBooleanField(verbose_name=_("Schedule 5: All expenses are eligible"))
    reasonable_costs = models.NullBooleanField(verbose_name=_("Schedule 5: All costs are reasonable"))
    budget_adds_up = models.NullBooleanField(verbose_name=_("Schedule 5: The budget adds up correctly."))
    maximum_amounts_set = models.NullBooleanField(verbose_name=_(
        "Schedule 5: If applicable, maximum amounts for expense categories have been set (i.e., identified with an asterisk (*))."))
    budget_reflects_activity = models.NullBooleanField(verbose_name=_("Schedule 5: The budget reflects the nature of the Activity(ies)."))
    stacking_limits_respected = models.NullBooleanField(
        verbose_name=_("Schedule 5: The federal and stacking limit have been respected, based on confirmed funding."))
    no_funding_redundancy = models.NullBooleanField(verbose_name=_(
        "Schedule 5: The activities and budget items have been cross-checked against DFO Aboriginal program CAs (e.g., SPI-FHRI, AAROM, AFSAR) to ensure no funding redundancy."))
    stacking_identified = models.NullBooleanField(verbose_name=_(
        "Schedule 5: Funding directly related to the RFCPP project coming from DFO Aboriginal programs has been included in the federal and stacking support."))
    confirmation_letters_2_path = models.NullBooleanField(verbose_name=_(
        "Schedule 5: Confirmation letters for all confirmed cash support have been posted to PATH.  Confirmation letters for large amount/potentially inflated in-kind support have also been posted to PATH."))
    financial_information_2_path = models.NullBooleanField(
        verbose_name=_("Schedule 5: Financial information has been updated/entered in PATH as per Data Entry Procedures"))
    conflict_of_interest_assessed = models.NullBooleanField(verbose_name=_(
        "Schedule 5: If a current or former federal public servant is involved in the project, a conflict of interest assessment has been completed (conflict of interest assessment tool found in CA checklist folder in national shared folder) and conflicts, if any, have been addressed, as appropriate."))
    # Schedule 6
    cashflow_adds_up = models.NullBooleanField(
        verbose_name=_("Schedule 6: The cash flow adds up correctly and reflects the timing of Activities."))
    # Schedule 7
    pre_filled_sched7 = models.NullBooleanField(verbose_name=_("Schedule 7: is pre-filled and mirrors Schedule 5"))
    performance_measures_in_path = models.NullBooleanField(verbose_name=_(
        "Schedule 7: Performance measures are updated in the ‘Planned’ column of the performance tab in PATH as per Data Entry Procedures"))
    # General
    team_leader_reviewed = models.NullBooleanField(verbose_name=_("The Team Leader has reviewed and approves the CA"))
    comment_for_nhq = models.TextField(verbose_name=_("Comments for NHQ"), blank=True, null=True)
    review_completion_date = models.DateTimeField(blank=True, null=True)
    # completed_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    # meta
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"),
                                         related_name="ca_checklist_last_mods")

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        return super().save(*args, **kwargs)


class ExpressionOfInterest(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name="eoi")
    date_received = models.DateTimeField(blank=True, null=True, verbose_name=_("date received"))
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))
    coordinator_notified = models.DateTimeField(blank=True, null=True, verbose_name=_("coordinator was notified"))
    project_eligible = models.NullBooleanField(verbose_name=_("is the project eligible?"))
    feedback = models.TextField(blank=True, null=True, verbose_name=_("Feedback to client"))
    feedback_sent = models.DateTimeField(blank=True, null=True, verbose_name=_("feedback sent to client"))

    # meta
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        return super().save(*args, **kwargs)

    @property
    def file(self):
        return File.objects.get(project=self.project, file_type_id=3)

    @property
    def eoi_evaluation_file(self):
        return File.objects.get(project=self.project, file_type_id=7)


class ProjectYear(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="years", verbose_name=_("project language"))
    fiscal_year = models.ForeignKey(shared_models.FiscalYear, on_delete=models.DO_NOTHING, related_name="gc_project_years")
    expenditure_initiation_date = models.DateTimeField(blank=True, null=True, default=datetime.datetime(timezone.now().year, 4, 1))
    paye_number = models.CharField(max_length=50, blank=True, null=True)
    annual_funding = models.FloatField(blank=True, null=True)
    forecasting_notes = models.TextField(blank=True, null=True)
    yearend_reminder_sent = models.DateTimeField(blank=True, null=True)
    lapsing_funds = models.NullBooleanField()
    lapsing_funds_nhq_notified = models.DateTimeField(blank=True, null=True)
    funding_recovery_needed = models.NullBooleanField()
    funding_recovery_email_sent = models.DateTimeField(blank=True, null=True)
    funds_recovered = models.NullBooleanField()
    year_complete = models.DateTimeField(blank=True, null=True)

    # meta
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def __str__(self):
        return "FY {}".format(self.fiscal_year)

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = ['project', 'fiscal_year']
        ordering = ["project", "fiscal_year"]

    @property
    def payments_issued(self):
        return sum([p.disbursement for p in self.payments.all()])


class ReportType(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("name (French)"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = [_('name'), ]


class Report(models.Model):
    project_year = models.OneToOneField(ProjectYear, on_delete=models.DO_NOTHING, related_name="reports")
    report_type = models.ForeignKey(ReportType, on_delete=models.DO_NOTHING, related_name="reports")
    date_received = models.DateTimeField(blank=True, null=True, default=timezone.now)
    coordinator_notified = models.DateTimeField(blank=True, null=True)
    coordinator_approved = models.DateTimeField(blank=True, null=True)
    gc_officer_approved = models.DateTimeField(blank=True, null=True)
    manager_approved = models.DateTimeField(blank=True, null=True)
    nhq_notified = models.DateTimeField(blank=True, null=True)

    # meta
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        return super().save(*args, **kwargs)


class ReportChecklist(models.Model):
    report = models.OneToOneField(Report, on_delete=models.DO_NOTHING, related_name="report_checklist")
    recommended_payment_amount = models.FloatField(verbose_name=_("Recommended Payment Amount"))
    # Schedule 7 - General
    sounds_sched7 = models.NullBooleanField(
        verbose_name=_("Schedule 7 matches the one in the signed CA and all sections have been duly filled in."))
    accurate_reporting_period = models.NullBooleanField(verbose_name=_(
        "Reporting period: Where this is the first report submitted by a recipient under the CA, the reporting period commences on the day that RFCPP-funded activities first started taking place."))
    no_missing_period = models.NullBooleanField(verbose_name=_(
        "Reporting period: Where a previous report has been submitted by the recipient under the CA, the reporting period for this report commences the day after the end of the previous reporting period."))

    # Schedule 7 – Section 1
    matching_funds = models.NullBooleanField(verbose_name=_("The “RFCPP funds received year to date” matches the amount in RFCPP records."))
    summed_correctly = models.NullBooleanField(verbose_name=_("Amounts in Table 1.1 are summed correctly."))
    budgeted_amounts_not_exceeded = models.NullBooleanField(
        verbose_name=_("Claimed expenses for expense categories tagged with an asterisk (*) do not exceed the budgeted amount."))
    tab11_no_issues = models.NullBooleanField(verbose_name=_(
        "The amounts reported in Table 1.1 raise no issues and align with the timing of Activities in Schedule 5 and the reporting period."))
    reimbursable_taxes_not_claimed = models.NullBooleanField(
        verbose_name=_("Reimbursable taxes have not been claimed (see application form for percentages reimbursable)."))
    tab12_filled = models.NullBooleanField(verbose_name=_(
        "Table 1.2 has been filled in where budgeted amounts exceed the allowed deviation: a) If the deviation was previously approved by DFO: no action required. b) If the deviation was not previously approved by DFO: review the reason for the deviation and recommend to NHQ (when submitting the report for payment) whether or not the over-expenditure(s) should be reimbursed.  Whether the over-expenditures are reimbursed or not, the recipient must be informed that as per the CA (Sch. 5 s. 6.3) requests for budget reallocations in excess of the set percentage must be submitted to DFO prior to deviating from planned expenditures."))
    confirmation_letters = models.NullBooleanField(verbose_name=_(
        "Confirmation letters for all previously unconfirmed cash support and large in-kind support have been received and posted to PATH (applies to multi-year agreements with supplemental conditions for unconfirmed support)."))
    support_matches = models.NullBooleanField(verbose_name=_(
        "Support received matches what was detailed in the CA. If different, then no effect on federal and stacking limits has been confirmed."))
    actuals_entered = models.NullBooleanField(
        verbose_name=_("All financial information has been entered in the ‘Actual’ section of the financial tab in PATH."))

    # Schedule 7 – Section 2
    deliverables_check_out = models.NullBooleanField(
        verbose_name=_("The status of deliverables matches the claimed expenses and timing of Activities in Schedule 5."))
    invoices_check_out = models.NullBooleanField(verbose_name=_(
        "Where invoices were provided as deliverables, the total(s) of the invoices match what is reported/claimed in Section 1, Table 1.1."))
    sufficient_detail = models.NullBooleanField(verbose_name=_(
        "The quality/level of detail of the deliverables provided is sufficient to recommend payment under s. 34 of the Financial Administration Act (i.e., sufficient information has been provided to justify payment)."))
    tab22_complete = models.NullBooleanField(verbose_name=_(
        "Where Table 2.2 has been filled in: a) Determine whether the explanation may impact the payment amount being requested by the recipient - address with NHQ when submitting the report for payment. b) Determine whether an amendment may be required – address with NHQ when submitting the report for payment (does not apply to final reports). c) Determine whether as a result of cancelled/delayed activities the stacking limit may be exceeded.  If so, the recipient must confirm the actual amounts received from other sources.  If the stacking limit was/will be exceeded, the RFCPP recommended payment must be reduced accordingly to ensure that the staking limit is met."))
    compliant_signage = models.NullBooleanField(verbose_name=_("RFCPP signage follows the RFCPP-FIP Guidelines"))

    # Schedule 7 – Section 3
    tab31_actuals = models.NullBooleanField(verbose_name=_("The “actuals” in Table 3.1 align with the activities and budget table."))
    tab32_complete = models.NullBooleanField(verbose_name=_(
        "All capital acquisitions purchased have been included in Table 3.2 (and align with the costs identified in the budget table)."))
    section3_path_recored = models.NullBooleanField(
        verbose_name=_("All information provided in Section 3 has been recorded in PATH (for final/annual reports only)."))

    # Schedule 7 – Section 4
    section4_signed = models.NullBooleanField(verbose_name=_(
        "Section 4 has been signed by an authorised representative of the Recipient (does not need to be the CA signatory)."))

    # Regional Approval
    sched7_to_path = models.NullBooleanField(
        verbose_name=_("Schedule 7 and all supporting documents (e.g., deliverables) have been posted to PATH."))
    sched6_to_path = models.NullBooleanField(
        verbose_name=_("If a multi-year agreement, Schedule 6 for next year has been received and posted to PATH."))
    site_visit_summary_provided = models.NullBooleanField(
        verbose_name=_("If a site visit was completed for the CA, a summary thereof is provided in the comments section below."))
    team_leader_reviewed = models.NullBooleanField(
        verbose_name=_("The Team Leader has reviewed and approved the recipient report and recommends payment."))

    comments = models.TextField(blank=True, null=True)
    calculations_recommended_payment = models.TextField(blank=True, null=True, verbose_name=_("calculations for recommended payment"))
    review_completion_date = models.DateTimeField(blank=True, null=True)
    completed_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    # meta
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"),
                                         related_name="report_checklist_mods")

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        return super().save(*args, **kwargs)


class RestorationTypeCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("name (French)"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = [_('name'), ]


class RestorationType(models.Model):
    restoration_type_category = models.ForeignKey(RestorationTypeCategory, on_delete=models.DO_NOTHING, related_name="types")
    name = models.TextField(verbose_name=_("name (English)"))
    nom = models.TextField(blank=True, null=True, verbose_name=_("name (French)"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = [_('name'), ]


class SiteType(models.Model):
    name = models.TextField(verbose_name=_("name (English)"))
    nom = models.TextField(blank=True, null=True, verbose_name=_("name (French)"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = [_('name'), ]


class Site(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, related_name="sites")
    name = models.CharField(max_length=255, verbose_name=_("site name"))
    site_type = models.ForeignKey(SiteType, on_delete=models.DO_NOTHING, related_name="sites", verbose_name=_("site type"))
    lat = models.FloatField(max_length=255, verbose_name=_("latitude (DD.dddddd)"), blank=True, null=True)
    long = models.FloatField(max_length=255, verbose_name=_("longitude (DD.dddddd)"), blank=True, null=True, validators=[MaxValueValidator(0),])
    restoration_type = models.ForeignKey(RestorationType, on_delete=models.DO_NOTHING, related_name="sites", verbose_name=_("restoration type (optional)"), blank=True, null=True)
    width = models.CharField(max_length=255, verbose_name=_("width (optional)"), blank=True, null=True)
    depth = models.CharField(max_length=255, verbose_name=_("depth (optional)"), blank=True, null=True)
    substrate = models.CharField(max_length=255, verbose_name=_("substrate (optional)"), blank=True, null=True)
    comments = models.TextField(verbose_name=_("comments"), blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = [_('name'), ]


class SiteVisit(models.Model):
    project_year = models.OneToOneField(ProjectYear, on_delete=models.DO_NOTHING, related_name="site_visits")
    date_of_visit = models.DateTimeField(blank=True, null=True, default=timezone.now)
    personnel_1 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="site_visits_per1")
    personnel_2 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="site_visits_per2")

    # QUARTERLY DOCUMENTED ROUTINE REVIEW (REQUIRED)
    c1 = models.NullBooleanField(verbose_name=_(
        "C.1 Was the work completed as proposed in the CA (activities/tasks, timing and budget)? If not, is an amendment or note-to-file required? Provide details."))
    c1_comment = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("C.1 comments"))

    c2 = models.NullBooleanField(verbose_name=_(
        "C.2 Are there any challenges affecting delivery of the project (e.g., contractors/personnel issues, required permits, site conditions)? If so, provide details."))
    c2_comment = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("C.2 comments"))

    c3 = models.NullBooleanField(verbose_name=_("C.3 Was the sign installed?  If not, provide details."))
    c3_comment = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("C.3 comments"))

    c4 = models.NullBooleanField(verbose_name=_("C.4 Were photos taken? If so, ensure that photos are posted to PATH."))
    c4_comment = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("C.4 comments"))

    c5 = models.NullBooleanField(verbose_name=_(
        "C.5 Is a follow up site visit (or other follow-up) required? If yes, describe reasons for requiring follow-up, the type of follow-up, and when it is to occur."))
    c5_comment = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("C.5 comments"))

    # PROGRAM IMPROVEMENT (REQUIRED)
    c6 = models.NullBooleanField(verbose_name=_(
        "C.6 Does the group have any feedback on the Program (positive feedback or suggested improvements)?  Provide details."))
    c6_comment = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("C.6 comments"))

    # PROJECT EVALUATION (OPTIONAL)
    c7 = models.NullBooleanField(verbose_name=_("C.7 Were the structure(s)/works designed/installed properly?  If not, provide details."))
    c7_comment = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("C.7 comments"))

    c8 = models.NullBooleanField(
        verbose_name=_("C.8 Did the work address the key issues at the site / is it functioning as intended? If not, provide details."))
    c8_comment = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("C.8 comments"))

    c9 = models.NullBooleanField(verbose_name=_("C.9 Are recreational fish using the site/have access to the site?"))
    c9_comment = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("C.9 comments"))

    c10 = models.NullBooleanField(verbose_name=_("C.10 Are there concerns with any aspect of the work? If yes, provide details."))
    c10_comment = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("C.10 comments"))

    c11 = models.NullBooleanField(verbose_name=_("C.11 Were any suggestions made for future projects? If yes, provide details."))
    c11_comment = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("C.11 comments"))

    # SUMMARY
    summary = models.TextField(blank=True, null=True, verbose_name=_("Summary of Findings and/or Follow-up Actions (if applicable)"))

    # meta
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        return super().save(*args, **kwargs)


def file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/entry_<id>/<filename>
    return 'spot/{0}/{1}'.format(instance.project.id, filename)


class Photo(models.Model):
    caption = models.CharField(max_length=255)
    site_visit = models.ForeignKey(SiteVisit, related_name="photos", on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_directory_path)
    # meta
    date_created = models.DateTimeField(default=timezone.now)
    uploaded_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("uploaded"))

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.caption


class FileType(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("name (French)"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = [_('name'), ]


class File(models.Model):
    project = models.ForeignKey(Project, related_name="files", on_delete=models.CASCADE)
    caption = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("file caption (optional)"))
    file_type = models.ForeignKey(FileType, related_name="files", on_delete=models.DO_NOTHING)
    file = models.FileField(upload_to=file_directory_path)
    # meta
    date_modified = models.DateTimeField(default=timezone.now)
    uploaded_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("uploaded by"))

    class Meta:
        ordering = ['file_type']

    def __str__(self):
        my_str = str(self.file_type)
        if self.caption:
            my_str = "{} - {}".format(my_str, self.caption)
        return my_str

    def save(self, *args, **kwargs):
        self.date_modified = timezone.now()
        return super().save(*args, **kwargs)


class Payment(models.Model):
    project_year = models.ForeignKey(ProjectYear, related_name="payments", on_delete=models.CASCADE)
    claim_number = models.IntegerField()
    advance_amount = models.FloatField(default=0)
    reimbursement_amount = models.FloatField(default=0)
    from_period = models.DateTimeField(blank=True, null=True)
    to_period = models.DateTimeField(blank=True, null=True)
    final_payment = models.BooleanField(default=False, verbose_name=_("Is this a final payment (project-year)?"))
    materials_submitted = models.NullBooleanField(verbose_name=_("were all necessary materials submitted?"))
    nhq_notified = models.DateTimeField(blank=True, null=True, verbose_name=_("NHQ notified"))
    payment_confirmed = models.NullBooleanField(verbose_name=_("has the payment been confirmed?"))
    notes = models.TextField(blank=True, null=True)

    # meta
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = ['project_year', 'claim_number']

    @property
    def disbursement(self):
        return self.advance_amount + self.reimbursement_amount


def determine_project_status(project):
    ignore_statuses = [2, 4, 5, 7, 11, 12, 13]
    # first check to see if this function should be escaped
    if project.status_id in ignore_statuses:
        return project.status_id

    # otherwise we assess status
    else:
        # start backwards
        if project.date_completed:
            # means project is over
            return 13
        elif project.final_ca_nhq_signed:
            # means there is a signed agreement inplace. Status should be changed to 'active'
            return 10
        elif nz(project.recommended_overprogramming, 0) > 0:
            # means project is on OP
            return 8
        elif project.total_recommended_funding > 0:
            # means funding has been recommended
            return 9
        elif project.submission_accepted == False:
            # means submission has not been accepted
            return 5
        elif project.submission_accepted == True:
            # means submission was successful
            return 6
        elif ExpressionOfInterest.objects.filter(project=project).count() > 0:
            # means an eoi was submitted
            if project.eoi.project_eligible == False:
                # means project was deemed eligible
                return 2
            elif project.eoi.project_eligible == True:
                # means project was deemed ineligible
                return 3
            else:
                return 1
        else:
            print("returning default status")
            return project.status_id


def determine_project_length(project, status_id):
    # depending on the status, we should set the project length
    my_length = 0

    if status_id == 8:
        # an OP project can only be for 1 year
        my_length = 1
    elif status_id == 9:
        # recommended project will be based on the number of years recommended
        if nz(project.recommended_funding_y1, 0) > 0:
            my_length += 1
        if nz(project.recommended_funding_y2, 0) > 0:
            my_length += 1
        if nz(project.recommended_funding_y3, 0) > 0:
            my_length += 1
        if nz(project.recommended_funding_y4, 0) > 0:
            my_length += 1
        if nz(project.recommended_funding_y5, 0) > 0:
            my_length += 1
    elif status_id == 10:
        # active project will be based on the number of project-years
        my_length = project.years.count()

    else:
        my_length = None

    return my_length


#
# @receiver(models.signals.post_delete, sender=Project)
# def auto_delete_draft_ca_on_delete(sender, instance, **kwargs):
#     """
#     Deletes file from filesystem
#     when corresponding `MediaFile` object is deleted.
#     """
#     # for draft ca
#     if instance.draft_ca:
#         if os.path.isfile(instance.draft_ca.path):
#             os.remove(instance.draft_ca.path)
#
#
# @receiver(models.signals.pre_save, sender=Project)
# def auto_delete_draft_ca_on_change(sender, instance, **kwargs):
#     """
#     Deletes old file from filesystem
#     when corresponding `MediaFile` object is updated
#     with new file.
#     """
#     if not instance.pk:
#         return False
#
#     # for draft ca
#     try:
#         old_file = Project.objects.get(pk=instance.pk).draft_ca
#     except Project.DoesNotExist:
#         return False
#
#     if old_file:
#         new_file = instance.draft_ca
#         if not old_file == new_file:
#             if os.path.isfile(old_file.path):
#                 os.remove(old_file.path)


@receiver(models.signals.post_delete, sender=Photo)
def auto_delete_photo_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=Photo)
def auto_delete_photo_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Photo.objects.get(pk=instance.pk).file
    except Photo.DoesNotExist:
        return False

    if old_file:
        new_file = instance.file
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=File)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = File.objects.get(pk=instance.pk).file
    except File.DoesNotExist:
        return False

    if old_file:
        new_file = instance.file
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
