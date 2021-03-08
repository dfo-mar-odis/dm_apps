from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import modelformset_factory
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _, gettext, gettext_lazy

from lib.functions.custom_functions import fiscal_year
from shared_models import models as shared_models
from . import models, utils

chosen_js = {"class": "chosen-select-contains"}
multi_select_js = {"class": "multi-select"}
attr_fp_date = {"class": "fp-date", "placeholder": "Click to select a date.."}
# class_editable = {"class": "editable"}
class_editable = {"class": "widgEditor"}
row4 = {"rows": "4"}
comment_row3 = {"rows": "3", "placeholder": "comments"}
row2 = {"rows": "2"}

# Choices for YesNo
YESNO_CHOICES = (
    (True, _("Yes")),
    (False, _("No")),
)
NULLYESNO_CHOICES = (
    (None, _("----")),
    (True, _("Yes")),
    (False, _("No")),
)


class NewProjectForm(forms.ModelForm):
    region = forms.ChoiceField(label=_("Region"))
    division = forms.ChoiceField()
    field_order = [
        'title',
        'default_funding_source',
        'region',
        'division',
        'section'
    ]

    class Meta:
        model = models.Project
        fields = [
            'title',
            'default_funding_source',
            'section',
            'modified_by',
        ]
        widgets = {
            'modified_by': forms.HiddenInput(),
            'title': forms.Textarea(attrs={"rows": 3}),
            'default_funding_source': forms.Select(attrs=chosen_js),
        }

    def __init__(self, *args, **kwargs):
        region_choices = utils.get_region_choices(all=True)
        region_choices.insert(0, tuple((None, "---")))
        division_choices = utils.get_division_choices(all=True)
        division_choices.insert(0, tuple((None, "---")))
        section_choices = utils.get_section_choices(all=True)
        section_choices.insert(0, tuple((None, "---")))
        funding_source_choices = [(f.id, f.display3) for f in models.FundingSource.objects.all()]
        funding_source_choices.insert(0, tuple((None, "---")))

        super().__init__(*args, **kwargs)
        self.fields['region'].choices = region_choices

        # even though these are overwritten by js scripts you have to define these so that the validation kicks in properly
        self.fields['division'].choices = division_choices
        self.fields['section'].choices = section_choices
        self.fields['default_funding_source'].choices = funding_source_choices


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        exclude = [
            'updated_at',
            'meeting_notes',
            'programs',
            "allocated_budget",
        ]
        widgets = {
            "title": forms.Textarea(attrs={"rows": "3"}),
            "overview": forms.Textarea(attrs=class_editable),
            'modified_by': forms.HiddenInput(),
            "section": forms.Select(attrs=chosen_js),
            "tags": forms.SelectMultiple(attrs=chosen_js),
            "default_funding_source": forms.Select(attrs=chosen_js),
            "client_information": forms.Select(attrs=chosen_js),
            "second_priority": forms.Select(attrs=chosen_js),
            "is_hidden": forms.Select(choices=YESNO_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        SECTION_CHOICES = utils.get_section_choices(all=True)
        SECTION_CHOICES.insert(0, tuple((None, "---")))
        funding_source_choices = [(f.id, f.display3) for f in models.FundingSource.objects.all()]
        funding_source_choices.insert(0, tuple((None, "---")))

        super().__init__(*args, **kwargs)
        self.fields['default_funding_source'].choices = funding_source_choices
        self.fields['section'].choices = SECTION_CHOICES
        # self.fields['programs'].label = "{} ({})".format(_(get_verbose_label(models.Project.objects.first(), "programs")),
        #                                                  _("mandatory - select multiple, if necessary"))

        functional_group_choices = [(tg.id, str(tg)) for tg in kwargs.get("instance").section.functional_groups2.all()]
        functional_group_choices.insert(0, tuple((None, "---")))
        self.fields['functional_group'].choices = functional_group_choices

        if kwargs.get("initial") and kwargs.get("initial").get("cloning"):
            del self.fields["tags"]

        # if not acrdp project, we should remove certain fields
        if kwargs.get("instance"):
            if not kwargs.get("instance").is_acrdp and not kwargs.get("instance").is_csrf and not kwargs.get("instance").is_sara:
                specialized_fields = [
                    # ACRDP
                    'organization',
                    'species_involved',
                    'team_description',
                    'rationale',
                    'experimental_protocol',
                    # CSRF
                    'client_information',
                    'second_priority',
                    'objectives',
                    'innovation',
                    'other_funding',
                    # SARA
                    'reporting_mechanism',
                    'future_funding_needs',
                ]
                for field in specialized_fields:
                    del self.fields[field]

            elif kwargs.get("instance").is_acrdp:
                specialized_fields = [
                    # CSRF
                    'client_information',
                    'second_priority',
                    'objectives',
                    'innovation',
                    'other_funding',
                    # SARA
                    'reporting_mechanism',
                    'future_funding_needs',
                ]
                for field in specialized_fields:
                    del self.fields[field]

                self.fields["overview"].label += str(_(" /  ACRDP objectives"))
            elif kwargs.get("instance").is_csrf:
                specialized_fields = [
                    # ACRDP
                    'organization',
                    'species_involved',
                    'team_description',
                    'rationale',
                    'experimental_protocol',
                    # SARA
                    'reporting_mechanism',
                    'future_funding_needs',
                ]
                for field in specialized_fields:
                    del self.fields[field]
                self.fields["overview"].label = str(
                    _("Provide a brief overview of the project outlining how it specifically addresses the priority identified "))
                self.fields["objectives"].label = str(_("Describe the objective(s) of the project (CSRF)"))
                # self.fields["objectives_methods"].label = str(
                #     _("Outline the methods applied to achieve the objective(s) of the project, and the main steps of the work plan by year (CSRF)"))
                self.fields["innovation"].label = str(_("Describe how the project will generate or promote innovation (CSRF)"))
                self.fields["other_funding"].label = str(
                    _("Provide any additional information on the other sources of funding relevant to the project (e.g. type of in-kind contribution) (CSRF)"))
                self.fields["client_information"].label += " " + str(_("SEE PRIORITIES DOCUMENT"))
                self.fields["second_priority"].label += " " + str(_("SEE PRIORITIES DOCUMENT"))
            elif kwargs.get("instance").is_sara:
                specialized_fields = [
                    # CSRF
                    'client_information',
                    'second_priority',
                    'objectives',
                    'innovation',
                    'other_funding',
                    # ACRDP
                    'organization',
                    'species_involved',
                    'team_description',
                    'rationale',
                    'experimental_protocol',
                ]
                for field in specialized_fields:
                    del self.fields[field]

                self.fields["overview"].label = mark_safe(_(
                    "Overview:<br>"
                    "a) What SARA process step does this work support?<br>"
                    "b) What recovery or conservation measures does this work support? (if applicable) (SARA)"))
                self.fields["tags"].label = _("Tags / species (single or multi-species), threat or area of focus (SARA)")


class ProjectYearForm(forms.ModelForm):
    class Meta:
        model = models.ProjectYear
        exclude = [
            # 'project',
            "allocated_budget",
            "approval_notification_email_sent",
            "review_notification_email_sent",
            "modified_by",
            "administrative_notes",
        ]
        widgets = {
            'project': forms.HiddenInput(),
            'start_date': forms.DateInput(attrs=attr_fp_date),
            'end_date': forms.DateInput(attrs=attr_fp_date),
            'priorities': forms.Textarea(attrs=class_editable),
            'deliverables': forms.Textarea(attrs=class_editable),
            "responsibility_center": forms.Select(attrs=chosen_js),
            "allotment_code": forms.Select(attrs=chosen_js),
            "existing_project_codes": forms.SelectMultiple(attrs=chosen_js),

            # SPECIALIZED EQUIPMENT
            ########################

            'requires_specialized_equipment': forms.Select(choices=YESNO_CHOICES),
            'technical_service_needs': forms.Textarea(attrs=row4),
            'mobilization_needs': forms.Textarea(attrs=row4),

            # FIELD COMPONENT
            #################
            'has_field_component': forms.Select(choices=YESNO_CHOICES),
            'vehicle_needs': forms.Textarea(attrs=row4),
            'ship_needs': forms.Textarea(attrs=row4),
            # 'coip_reference_id': forms.Textarea(attrs=row4),
            'instrumentation': forms.Textarea(attrs=row4),
            'owner_of_instrumentation': forms.Textarea(attrs=row4),
            'requires_field_staff': forms.Select(choices=YESNO_CHOICES),
            'field_staff_needs': forms.Textarea(attrs=row4),

            # DATA COMPONENT
            ################
            'has_data_component': forms.Select(choices=YESNO_CHOICES),
            'data_collected': forms.Textarea(attrs=row4),
            'data_products': forms.Textarea(attrs=row4),
            'open_data_eligible': forms.Select(choices=YESNO_CHOICES),
            'data_storage_plan': forms.Textarea(attrs=row4),
            'data_management_needs': forms.Textarea(attrs=row4),

            # LAB COMPONENT
            ###############
            'has_lab_component': forms.Select(choices=YESNO_CHOICES),
            'requires_abl_services': forms.Select(choices=YESNO_CHOICES),
            'requires_lab_space': forms.Select(choices=YESNO_CHOICES),
            'requires_other_lab_support': forms.Select(choices=YESNO_CHOICES),
            'other_lab_support_needs': forms.Textarea(attrs=row4),

            'it_needs': forms.Textarea(attrs=row4),
            'additional_notes': forms.Textarea(attrs=row4),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # if not acrdp project, we should remove certain fields
        if kwargs.get("instance"):
            if kwargs.get("instance").project.is_csrf:
                self.fields["priorities"].label = str(
                    _(
                        "Outline the methods applied to achieve the objective(s) of the project, and the main steps of the work plan FOR THIS PROJECT YEAR ONLY (CSRF)"))
                self.fields["data_products"].label += " " + str(_("And what is the plan for the publication of these products (CSRF)?"))
            elif kwargs.get("instance").project.is_sara:
                self.fields["priorities"].label = mark_safe(str(
                    _("Priorities:<br>"
                      "a) Objectives – what will be achieved by completing this work?<br>"
                      "b) Methods – how will this work be completed (broadly)?")))


    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        fy = shared_models.FiscalYear.objects.get(pk=fiscal_year(start_date, sap_style=True))

        # is there already a fiscal year? There is a special case when there will be a fiscal year, but we are cloning
        if not self.initial.get("cloning") and self.instance.fiscal_year:
            # there if we remove this instance, there should not be another projectyear with the same fiscal year as fy
            project = self.instance.project
            other_years = project.years.filter(~Q(id=self.instance.id))
            if other_years.filter(fiscal_year=fy).exists():
                raise forms.ValidationError(gettext(
                    f"Sorry, there is already a {fy} year in this project."
                ))
            pass
        else:
            if self.initial.get("cloning"):
                project = self.instance.project
            else:
                project = self.initial["project"]
            if project.years.filter(fiscal_year=fy).exists():
                raise forms.ValidationError(gettext(
                    f"Sorry, there is already a {fy} year in this project."
                ))
        return start_date

    def clean(self):
        cleaned_data = super().clean()

        # we have to make sure
        # 1) the end date is after the start date and
        # 2)the start and end dates are within the same fiscal year
        end_date = cleaned_data.get("end_date")
        if end_date:
            start_date = cleaned_data.get("start_date")
            if end_date and start_date and end_date < start_date:
                self.add_error('end_date', gettext(
                    "The end date must be after the start date!"
                ))

            if end_date and start_date and fiscal_year(start_date) != fiscal_year(end_date):
                self.add_error('end_date', gettext(
                    "The start and end dates must be within the same fiscal year!"
                ))


class ProjectSubmitForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'modified_by',
        ]
        widgets = {
            'modified_by': forms.HiddenInput(),
        }


class ProjectNotesForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'modified_by',
        ]
        widgets = {
            'modified_by': forms.HiddenInput(),
        }


class StaffForm(forms.ModelForm):
    field_order = [
        "user",
        "name",
        "employee_type",
        "is_lead",
        "funding_source",
        "amount",
        "level",
        "student_program",
        "duration_weeks",
        "overtime_hours",
        "overtime_description",
    ]

    class Meta:
        model = models.Staff
        exclude = ["project_year"]
        labels = {
            "user": _("DFO User"),
            "amount": _("Approximate amount (CAD) (will only be visible to project leads and managers)"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["overtime_description"].widget.attrs = {"v-model": "staff.overtime_description", "rows": 7}
        self.fields["amount"].widget.attrs = {"v-model": "staff.amount", ":disabled": "disableAmountField"}
        self.fields["funding_source"].widget.attrs = {"v-model": "staff.funding_source"}
        self.fields["is_lead"].widget.attrs = {"v-model": "staff.is_lead", "@change": "adjustStaffFields", }

        self.fields["employee_type"].widget.attrs = {"v-model": "staff.employee_type", "@change": "adjustStaffFields"}
        self.fields["level"].widget.attrs = {"v-model": "staff.level", ":disabled": "disableLevelField"}
        self.fields["duration_weeks"].widget.attrs = {"v-model": "staff.duration_weeks", "step": "0.1"}
        self.fields["overtime_hours"].widget.attrs = {"v-model": "staff.overtime_hours", "step": "0.1"}
        self.fields["student_program"].widget.attrs = {"v-model": "staff.student_program", ":disabled": "disableStudentProgramField"}

        self.fields["name"].widget.attrs = {"v-model": "staff.name", ":disabled": "disableNameField"}
        self.fields["user"].widget.attrs = {"v-model": "staff.user", "@change": "adjustStaffFields",
                                            "@click": "adjustStaffFields"}  # , "class": "chosen-select-contains"
        user_choices = [(u.id, f"{u.last_name}, {u.first_name}") for u in User.objects.order_by("last_name", "first_name")]
        user_choices.insert(0, (None, "-----"))
        self.fields["user"].choices = user_choices
        funding_source_choices = [(f.id, f.display2) for f in models.FundingSource.objects.all()]
        funding_source_choices.insert(0, tuple((None, "---")))
        self.fields["funding_source"].choices = funding_source_choices
        self.fields["role"].widget.attrs = {"v-model": "staff.role", "rows": "4", ":disabled": "!isCSRF"}
        self.fields["expertise"].widget.attrs = {"v-model": "staff.expertise", "rows": "4", ":disabled": "!isCSRF"}


class OMCostForm(forms.ModelForm):
    field_order = ["om_category", "funding_source", "description", "amount"]

    class Meta:
        model = models.OMCost
        exclude = ["project_year"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["amount"].widget.attrs = {"v-model": "om_cost.amount"}
        self.fields["funding_source"].widget.attrs = {"v-model": "om_cost.funding_source"}
        self.fields["description"].widget.attrs = {"v-model": "om_cost.description"}
        self.fields["om_category"].widget.attrs = {"v-model": "om_cost.om_category"}
        funding_source_choices = [(f.id, f.display2) for f in models.FundingSource.objects.all()]
        funding_source_choices.insert(0, tuple((None, "---")))
        self.fields["funding_source"].choices = funding_source_choices


class CapitalCostForm(forms.ModelForm):
    field_order = ["category", "funding_source", "description", "amount"]

    class Meta:
        model = models.CapitalCost
        exclude = ["project_year"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["amount"].widget.attrs = {"v-model": "capital_cost.amount"}
        self.fields["funding_source"].widget.attrs = {"v-model": "capital_cost.funding_source"}
        self.fields["description"].widget.attrs = {"v-model": "capital_cost.description"}
        self.fields["category"].widget.attrs = {"v-model": "capital_cost.category"}
        funding_source_choices = [(f.id, f.display2) for f in models.FundingSource.objects.all()]
        funding_source_choices.insert(0, tuple((None, "---")))
        self.fields["funding_source"].choices = funding_source_choices


class ActivityForm(forms.ModelForm):
    class Meta:
        model = models.Activity
        exclude = ["project_year"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["type"].widget.attrs = {"v-model": "activity.type"}
        self.fields["name"].widget.attrs = {"v-model": "activity.name"}
        self.fields["description"].widget.attrs = {"v-model": "activity.description", "rows": "4"}
        self.fields["responsible_party"].widget.attrs = {"v-model": "activity.responsible_party"}
        self.fields["target_date"].widget = forms.DateInput(attrs={"v-model": "activity.target_date", "type": "date"})
        self.fields["likelihood"].widget.attrs = {"v-model": "activity.likelihood", ":disabled": "!isACRDP"}
        self.fields["impact"].widget.attrs = {"v-model": "activity.impact", ":disabled": "!isACRDP"}
        self.fields["risk_description"].widget.attrs = {"v-model": "activity.risk_description", "rows": "4", ":disabled": "!isACRDP && !isCSRF"}
        self.fields["mitigation_measures"].widget.attrs = {"v-model": "activity.mitigation_measures", "rows": "4", ":disabled": "!isACRDP && !isCSRF"}


class CollaborationForm(forms.ModelForm):
    class Meta:
        model = models.Collaboration
        exclude = ["project_year"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["type"].widget.attrs = {"v-model": "collaboration.type"}
        self.fields["new_or_existing"].widget.attrs = {"v-model": "collaboration.new_or_existing"}
        self.fields["organization"].widget.attrs = {"v-model": "collaboration.organization"}
        self.fields["people"].widget.attrs = {"v-model": "collaboration.people"}
        self.fields["critical"].widget.attrs = {"v-model": "collaboration.critical"}
        self.fields["agreement_title"].widget.attrs = {"v-model": "collaboration.agreement_title",
                                                       ":disabled": "collaboration.type != 2 && collaboration.type != 3"}
        self.fields["gc_program"].widget.attrs = {"v-model": "collaboration.gc_program", ":disabled": "collaboration.type != 2"}
        self.fields["amount"].widget.attrs = {"v-model": "collaboration.amount", ":disabled": "collaboration.type != 2"}
        self.fields["notes"].widget.attrs = {"v-model": "collaboration.notes"}


class StatusReportForm(forms.ModelForm):
    class Meta:
        model = models.StatusReport
        exclude = ["project_year", "section_head_comment", "section_head_reviewed"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].widget.attrs = {"v-model": "status_report.status"}
        self.fields["major_accomplishments"].widget.attrs = {"v-model": "status_report.major_accomplishments", "rows": "4"}
        self.fields["major_accomplishments"].label = _("Major accomplishments (this can be left blank if reported at the activity level")
        self.fields["major_issues"].widget.attrs = {"v-model": "status_report.major_issues", "rows": "4"}
        self.fields["target_completion_date"].widget = forms.DateInput(
            attrs={"v-model": "status_report.target_completion_date", "type": "date"})
        self.fields["rationale_for_modified_completion_date"].widget.attrs = {
            "v-model": "status_report.rationale_for_modified_completion_date", "rows": "4"}
        self.fields["general_comment"].widget.attrs = {"v-model": "status_report.general_comment", "rows": "4"}


class ActivityUpdateForm(forms.ModelForm):
    class Meta:
        model = models.ActivityUpdate
        exclude = ["status_report", "activity"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].widget.attrs = {"v-model": "update.status"}
        self.fields["notes"].widget.attrs = {"v-model": "update.notes", "rows": "4"}


class StatusReportReviewForm(forms.ModelForm):
    class Meta:
        model = models.StatusReport
        fields = ["section_head_comment", "section_head_reviewed"]
        labels = {"section_head_reviewed": gettext_lazy("Mark as reviewed")}


class FileForm(forms.ModelForm):
    class Meta:
        model = models.File
        exclude = ["project", "project_year", "status_report"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs = {"v-model": "file.name"}
        self.fields["file"].widget.attrs = {"v-on:change": "onFileChange", "ref": "file"}
        self.fields["external_url"].widget.attrs = {"v-model": "file.external_url"}


class ReviewForm(forms.ModelForm):
    review_email_update = forms.BooleanField(required=False, label=gettext_lazy("send an email update to project leads"))

    class Meta:
        model = models.Review
        exclude = ["project_year", "approval_status", "approval_level", "allocated_budget", "approver_comment"]
        widgets = {
            "general_comment": forms.Textarea(attrs=comment_row3),
            "comments_for_staff": forms.Textarea(attrs=comment_row3),
            "collaboration_comment": forms.Textarea(attrs=comment_row3),
            "strategic_comment": forms.Textarea(attrs=comment_row3),
            "operational_comment": forms.Textarea(attrs=comment_row3),
            "ecological_comment": forms.Textarea(attrs=comment_row3),
            "scale_comment": forms.Textarea(attrs=comment_row3),
            "collaboration_score": forms.RadioSelect(),
            "strategic_score": forms.RadioSelect(),
            "operational_score": forms.RadioSelect(),
            "ecological_score": forms.RadioSelect(),
            "scale_score": forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["general_comment"].widget.attrs["v-model"] = "project_year.review.general_comment"
        self.fields["comments_for_staff"].widget.attrs["v-model"] = "project_year.review.comments_for_staff"
        self.fields["review_email_update"].widget.attrs["v-model"] = "project_year.review.review_email_update"

        # update the choices for the scores
        score_dict = utils.get_review_score_rubric()
        criteria = [
            "collaboration",
            "strategic",
            "operational",
            "ecological",
            "scale",
        ]
        for c in criteria:
            self.fields[c + "_comment"].widget.attrs["v-model"] = f"project_year.review.{c}_comment"
            self.fields[c + "_score"].widget.attrs["v-model"] = f"project_year.review.{c}_score"


class ApprovalForm(forms.ModelForm):
    approval_email_update = forms.BooleanField(required=False, label=gettext_lazy("send an email update to project leads"))

    class Meta:
        model = models.Review
        fields = ["approval_status", "approval_level", "allocated_budget", "approver_comment", ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["approval_status"].widget.attrs = {"v-model": "project_year.review.approval_status"}
        self.fields["approval_level"].widget.attrs = {"v-model": "project_year.review.approval_level"}
        self.fields["allocated_budget"].widget.attrs = {"v-model": "project_year.review.allocated_budget"}
        self.fields["approver_comment"].widget.attrs = {"v-model": "project_year.review.approver_comment"}
        self.fields["approval_email_update"].widget.attrs = {"v-model": "project_year.review.approval_email_update"}


class FundingSourceForm(forms.ModelForm):
    class Meta:
        model = models.FundingSource
        fields = "__all__"


FundingSourceFormset = modelformset_factory(
    model=models.FundingSource,
    form=FundingSourceForm,
    extra=1,
)


class OMCategoryForm(forms.ModelForm):
    class Meta:
        model = models.OMCategory
        fields = "__all__"
        widgets = {
            'name': forms.Textarea(attrs={"rows": 3}),
            'nom': forms.Textarea(attrs={"rows": 3}),
        }


OMCategoryFormset = modelformset_factory(
    model=models.OMCategory,
    form=OMCategoryForm,
    extra=1,
)


#
#
class EmployeeTypeForm(forms.ModelForm):
    class Meta:
        model = models.EmployeeType
        fields = "__all__"
        widgets = {
            'exclude_from_rollup': forms.Select(choices=YESNO_CHOICES),
        }


EmployeeTypeFormset = modelformset_factory(
    model=models.EmployeeType,
    form=EmployeeTypeForm,
    extra=1,
)


class TagForm(forms.ModelForm):
    class Meta:
        model = models.Tag
        fields = "__all__"


TagFormset = modelformset_factory(
    model=models.Tag,
    form=TagForm,
    extra=1,
)


class HelpTextForm(forms.ModelForm):
    class Meta:
        model = models.HelpText
        fields = "__all__"
        widgets = {
            'eng_text': forms.Textarea(attrs={"rows": 4}),
            'fra_text': forms.Textarea(attrs={"rows": 4}),
        }


HelpTextFormset = modelformset_factory(
    model=models.HelpText,
    form=HelpTextForm,
    extra=1,
)


class FunctionalGroupForm(forms.ModelForm):
    class Meta:
        model = models.FunctionalGroup
        fields = "__all__"
        widgets = {
            'name': forms.Textarea(attrs={"rows": 3}),
            'nom': forms.Textarea(attrs={"rows": 3}),
            'sections': forms.SelectMultiple(attrs=chosen_js),
            'program': forms.Select(attrs=chosen_js),
        }

    def __init__(self, *args, **kwargs):
        section_choices = utils.get_section_choices(all=True)

        super().__init__(*args, **kwargs)
        self.fields['sections'].choices = section_choices


class ActivityTypeForm(forms.ModelForm):
    class Meta:
        model = models.ActivityType
        fields = "__all__"


ActivityTypeFormset = modelformset_factory(
    model=models.ActivityType,
    form=ActivityTypeForm,
    extra=1,
)


class ThemeForm(forms.ModelForm):
    class Meta:
        model = models.Theme
        fields = "__all__"


ThemeFormset = modelformset_factory(
    model=models.Theme,
    form=ThemeForm,
    extra=1,
)


class UpcomingDateForm(forms.ModelForm):
    class Meta:
        model = models.UpcomingDate
        fields = "__all__"
        # widgets = {
        #     "date": forms.DateTimeInput()
        # }


UpcomingDateFormset = modelformset_factory(
    model=models.UpcomingDate,
    form=UpcomingDateForm,
    extra=1,
)


class CSRFThemeForm(forms.ModelForm):
    class Meta:
        model = models.CSRFTheme
        fields = "__all__"
        widgets = {
        }


CSRFThemeFormset = modelformset_factory(
    model=models.CSRFTheme,
    form=CSRFThemeForm,
    extra=1,
)


class CSRFSubThemeForm(forms.ModelForm):
    class Meta:
        model = models.CSRFSubTheme
        fields = "__all__"
        widgets = {
        }


CSRFSubThemeFormset = modelformset_factory(
    model=models.CSRFSubTheme,
    form=CSRFSubThemeForm,
    extra=1,
)


class CSRFPriorityForm(forms.ModelForm):
    class Meta:
        model = models.CSRFPriority
        fields = "__all__"
        widgets = {
            'name': forms.Textarea(attrs={}),
            'nom': forms.Textarea(attrs={}),
        }


CSRFPriorityFormset = modelformset_factory(
    model=models.CSRFPriority,
    form=CSRFPriorityForm,
    extra=1,
)


class CSRFClientInformationForm(forms.ModelForm):
    class Meta:
        model = models.CSRFClientInformation
        fields = "__all__"
        widgets = {
            'name': forms.Textarea(attrs={}),
            'nom': forms.Textarea(attrs={}),
            'description_en': forms.Textarea(attrs={"style": "width:400px"}),
            'description_fr': forms.Textarea(attrs={"style": "width:400px"}),
        }


CSRFClientInformationFormset = modelformset_factory(
    model=models.CSRFClientInformation,
    form=CSRFClientInformationForm,
    extra=1,
)


class ReferenceMaterialForm(forms.ModelForm):
    class Meta:
        model = models.ReferenceMaterial
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"})
        }


ReferenceMaterialFormset = modelformset_factory(
    model=models.ReferenceMaterial,
    form=ReferenceMaterialForm,
    extra=1,
)


class LevelForm(forms.ModelForm):
    class Meta:
        model = models.Level
        fields = "__all__"


LevelFormset = modelformset_factory(
    model=models.Level,
    form=LevelForm,
    extra=1,
)


class AdminStaffForm(forms.ModelForm):
    class Meta:
        model = models.Staff
        fields = ["user", 'name']
        labels = {
            "user": _("DFO User"),
        }
        widgets = {
            'user': forms.Select(attrs=chosen_js),
        }


class ReportSearchForm(forms.Form):
    REPORT_CHOICES = (
        (None, "------"),
        (1, "Science Culture Committee Report (xlsx)"),
        (2, "CSRF Submission List (xlsx)"),
        (3, "Project Status Summary (csv)"),
        (4, "Project List (csv)"),
        (5, "SAR Workplan (xlsx)"),
        (6, "Regional Staff Allocation (csv)"),
        (7, "HR Project-Position Allocation (csv)"),
    )
    report = forms.ChoiceField(required=True, choices=REPORT_CHOICES)
    year = forms.ChoiceField(required=False, label=gettext_lazy('Fiscal Year'))
    region = forms.ChoiceField(required=False, label=gettext_lazy('DFO Region'))
    section = forms.ChoiceField(required=False, label=gettext_lazy('DFO Section'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.filter(projectyear__isnull=False).distinct()]
        fy_choices.insert(0, (None, "-------"))
        region_choices = [(obj.id, str(obj)) for obj in shared_models.Region.objects.all()]
        region_choices.insert(0, (None, "All"))
        section_choices = [(obj.id, obj.full_name) for obj in shared_models.Section.objects.filter(projects2__isnull=False).distinct()]
        section_choices.insert(0, (None, "All"))
        self.fields['year'].choices = fy_choices
        self.fields['region'].choices = region_choices
        self.fields['section'].choices = section_choices
        self.fields['section'].widget.attrs = chosen_js


class CitationForm(forms.ModelForm):
    new_publication = forms.CharField(required=False)

    class Meta:
        model = shared_models.Citation
        fields = "__all__"
        widgets = {
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        klass = "form-control form-control-sm w100percent"
        self.fields["name"].widget.attrs = {"v-model": "citationToEdit.name", "class": klass, "ref": "edit_home"}
        self.fields["nom"].widget.attrs = {"v-model": "citationToEdit.nom", "class": klass}
        self.fields["authors"].widget.attrs = {"v-model": "citationToEdit.authors", "class": klass}
        self.fields["year"].widget.attrs = {"v-model": "citationToEdit.year", "class": klass}
        self.fields["publication"].widget.attrs = {"v-model": "citationToEdit.publication", "class": klass, "v-if": "!newPublication"}
        self.fields["new_publication"].widget.attrs = {"v-model": "citationToEdit.new_publication", "class": klass, "v-if": "newPublication",
                                                       "placeholder": gettext("Enter new publication name here")}
        self.fields["pub_number"].widget.attrs = {"v-model": "citationToEdit.pub_number", "class": klass}
        self.fields["url_en"].widget.attrs = {"v-model": "citationToEdit.url_en", "class": klass}
        self.fields["url_fr"].widget.attrs = {"v-model": "citationToEdit.url_fr", "class": klass}
        self.fields["abstract_en"].widget.attrs = {"v-model": "citationToEdit.abstract_en", "class": klass}
        self.fields["abstract_fr"].widget.attrs = {"v-model": "citationToEdit.abstract_fr", "class": klass}
        self.fields["series"].widget.attrs = {"v-model": "citationToEdit.series", "class": klass}
        self.fields["region"].widget.attrs = {"v-model": "citationToEdit.region", "class": klass}
