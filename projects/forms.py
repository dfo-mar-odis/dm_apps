from django import forms
from django.db.models import Q
from django.forms import modelformset_factory
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from lib.templatetags.verbose_names import get_verbose_label
from . import models
from . import views
from django.contrib.auth.models import User
from shared_models import models as shared_models

chosen_js = {"class": "chosen-select-contains"}
multi_select_js = {"class": "multi-select"}
attr_fp_date = {"class": "fp-date", "placeholder": "Click to select a date.."}
# class_editable = {"class": "editable"}
class_editable = {"class": "widgEditor"}

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
        'year',
        'project_title',
        'activity_type',
        'default_funding_source',
        'region',
        'division',
        'section'
    ]

    class Meta:
        model = models.Project
        fields = [
            'year',
            'project_title',
            'activity_type',
            'default_funding_source',
            'section',
            'last_modified_by',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'project_title': forms.Textarea(attrs={"rows": 3}),
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


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        exclude = [
            'date_last_modified',
            'submitted',
            'approved',
            'meeting_notes',
            'programs',
            "recommended_for_funding",
            "allocated_budget",
        ]
        widgets = {
            "project_title": forms.Textarea(attrs={"rows": "3"}),
            "description": forms.Textarea(attrs=class_editable),
            "priorities": forms.Textarea(attrs=class_editable),
            "deliverables": forms.Textarea(attrs=class_editable),
            "data_collection": forms.Textarea(attrs=class_editable),
            "data_sharing": forms.Textarea(attrs=class_editable),
            "data_storage": forms.Textarea(attrs=class_editable),
            "regional_dm_needs": forms.Textarea(attrs=class_editable),
            "sectional_dm_needs": forms.Textarea(attrs=class_editable),
            "vehicle_needs": forms.Textarea(attrs=class_editable),
            "it_needs": forms.Textarea(attrs=class_editable),
            "chemical_needs": forms.Textarea(attrs=class_editable),
            "ship_needs": forms.Textarea(attrs=class_editable),
            "feedback": forms.Textarea(attrs=class_editable),

            'start_date': forms.DateInput(attrs=attr_fp_date),
            'end_date': forms.DateInput(attrs=attr_fp_date),
            'last_modified_by': forms.HiddenInput(),
            "section": forms.Select(attrs=chosen_js),
            "responsibility_center": forms.Select(attrs=chosen_js),
            "allotment_code": forms.Select(attrs=chosen_js),
            "existing_project_codes": forms.SelectMultiple(attrs=chosen_js),

            "tags": forms.SelectMultiple(attrs=chosen_js),
            "default_funding_source": forms.Select(attrs=chosen_js),
            "programs": forms.SelectMultiple(attrs=chosen_js),

            "is_hidden": forms.Select(choices=YESNO_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        SECTION_CHOICES = views.get_section_choices(all=True)
        SECTION_CHOICES.insert(0, tuple((None, "---")))

        super().__init__(*args, **kwargs)
        self.fields['section'].choices = SECTION_CHOICES
        # self.fields['programs'].label = "{} ({})".format(_(get_verbose_label(models.Project.objects.first(), "programs")),
        #                                                  _("mandatory - select multiple, if necessary"))

        functional_group_choices = [(tg.id, str(tg)) for tg in kwargs.get("instance").section.functional_groups.all()]
        functional_group_choices.insert(0, tuple((None, "---")))
        self.fields['functional_group'].choices = functional_group_choices

        if kwargs.get("instance").section.division.branch.region.id == 1:
            # del self.fields["programs"]
            del self.fields["is_competitive"]
            del self.fields["is_approved"]
            del self.fields["metadata_url"]
            del self.fields["regional_dm_needs"]
            del self.fields["sectional_dm_needs"]
            del self.fields["feedback"]


class ProjectSubmitForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'last_modified_by',
            'meeting_notes',
            'submitted',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'submitted': forms.HiddenInput(),
        }


class ProjectNotesForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'last_modified_by',
            'meeting_notes',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
        }


class IPSProjectMeetingForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'meeting_notes',
        ]
        widgets = {
            # 'last_modified_by': forms.HiddenInput(),
            # 'submitted': forms.HiddenInput(),
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = models.Note
        fields = [
            "summary",
            "pressures",
        ]
        widgets = {
            # 'submitted': forms.HiddenInput(),
        }


class ProjectRecommendationForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'last_modified_by',
            'meeting_notes',
            # 'approved',
            "recommended_for_funding",
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            # 'approved': forms.HiddenInput(),
            'recommended_for_funding': forms.HiddenInput(),
        }


class StaffForm(forms.ModelForm):
    save_then_go_OT = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = models.Staff
        fields = "__all__"
        labels = {
            "user": _("DFO User"),
        }
        widgets = {
            'project': forms.HiddenInput(),
            'overtime_description': forms.Textarea(attrs={"rows": 5}),
            'user': forms.Select(attrs=chosen_js),
        }


class AdminStaffForm(forms.ModelForm):
    class Meta:
        model = models.Staff
        fields = ["user", 'name']
        labels = {
            "user": _("DFO User"),
        }
        widgets = {
            #     'project': forms.HiddenInput(),
            #     'overtime_description': forms.Textarea(attrs={"rows": 5}),
            'user': forms.Select(attrs=chosen_js),
        }


class AdminProjectProgramForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ["project_title", "programs", "recommended_for_funding", "approved", "meeting_notes"]

        widgets = {
            'programs': forms.SelectMultiple(attrs=chosen_js),
        }


class CollaboratorForm(forms.ModelForm):
    class Meta:
        model = models.Collaborator
        fields = "__all__"
        widgets = {
            'project': forms.HiddenInput(),
        }


class AgreementForm(forms.ModelForm):
    class Meta:
        model = models.CollaborativeAgreement
        fields = "__all__"
        widgets = {
            'project': forms.HiddenInput(),
        }


class OMCostForm(forms.ModelForm):
    class Meta:
        model = models.OMCost
        fields = "__all__"
        widgets = {
            'project': forms.HiddenInput(),
        }


class CapitalCostForm(forms.ModelForm):
    class Meta:
        model = models.CapitalCost
        fields = "__all__"
        widgets = {
            'project': forms.HiddenInput(),
        }


class MilestoneForm(forms.ModelForm):
    class Meta:
        model = models.Milestone
        fields = "__all__"
        widgets = {
            'project': forms.HiddenInput(),
        }


class MilestoneUpdateForm(forms.ModelForm):
    class Meta:
        model = models.MilestoneUpdate
        fields = "__all__"
        widgets = {
            'status_report': forms.HiddenInput(),
            'milestone': forms.HiddenInput(),
        }


class StatusReportForm(forms.ModelForm):
    class Meta:
        model = models.StatusReport
        exclude = ["date_created", ]
        widgets = {
            'target_completion_date': forms.DateInput(attrs=attr_fp_date),
            'major_accomplishments': forms.Textarea(attrs=class_editable),
            'major_issues': forms.Textarea(attrs=class_editable),
            'rationale_for_modified_completion_date': forms.Textarea(attrs=class_editable),
            'general_comment': forms.Textarea(attrs=class_editable),
            # Hidden fields
            'project': forms.HiddenInput(),
            'section_head_reviewed': forms.HiddenInput(),
            'section_head_comment': forms.HiddenInput(),
            'created_by': forms.HiddenInput(),

        }


class StatusReportSectionHeadForm(forms.ModelForm):
    class Meta:
        model = models.StatusReport
        exclude = ["date_created", ]
        widgets = {
            'target_completion_date': forms.DateInput(attrs=attr_fp_date),
            'major_accomplishments': forms.Textarea(attrs=class_editable),
            'major_issues': forms.Textarea(attrs=class_editable),
            'rationale_for_modified_completion_date': forms.Textarea(attrs=class_editable),
            'general_comment': forms.Textarea(attrs=class_editable),
            'section_head_comment': forms.Textarea(attrs=class_editable),
            'section_head_reviewed': forms.Select(choices=YESNO_CHOICES),

            # Hidden fields
            'project': forms.HiddenInput(),
            'created_by': forms.HiddenInput(),

        }
        labels = {
            'section_head_comment': _("Section head comments (visible to section head only)"),
            'section_head_reviewed': _("Section review complete (visible to section head only)?"),
        }


class GCCostForm(forms.ModelForm):
    class Meta:
        model = models.GCCost
        fields = "__all__"
        widgets = {
            'project': forms.HiddenInput(),
        }


class FYForm(forms.Form):
    fiscal_year = forms.ChoiceField(required=True)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fy_choices = [(
            reverse("projects:report_sh", kwargs={"fiscal_year": fy.id, "user": user}), str(fy)) for fy in
            shared_models.FiscalYear.objects.all() if fy.projects.count() > 0]
        fy_choices.insert(0, (None, "-----"))

        self.fields["fiscal_year"].choices = fy_choices


class ReportSearchForm(forms.Form):
    REPORT_CHOICES = (
        (None, ""),
        (None, "----- GENERAL ------"),
        (3, "Project Summary Report (PDF - section head approved projects)"),
        (2, "Batch Workplan Export (PDF - section head approved projects)"),
        (1, "Master spreadsheet (MS Excel)"),
        (16, _("Feedback summary")),
        (17, _("Data management summary")),
        (21, _("COVID Assessment")),

        (None, ""),
        (None, "----- Funding ------"),
        (18, _("Funding (PDF)")),
        (19, _("Funding (MS Excel)")),
        (20, _("Summary Report by O&M Category (MS Excel)")),

        (None, ""),
        (None, "----- GULF ------"),
        (10, _("Weeks Worked by Employees (PDF)")),
        (11, _("Total Overtime Hours Requested (PDF)")),
        (12, _("Cost Summary by Section (PDF)")),
        (13, _("List of Collaborators (PDF)")),
        (15, _("List of Collaborative Agreements (PDF)")),
        (14, _("Doug's Report (MS Excel)")),

        (None, ""),
        (None, "----- ADMIN ------"),
        (4, "Science program list (MS Excel)"),

    )
    report = forms.ChoiceField(required=True, choices=REPORT_CHOICES)
    fiscal_year = forms.ChoiceField(required=False)
    region = forms.MultipleChoiceField(required=False, label="Regions (Leave blank to select all)")
    funding_src = forms.ChoiceField(required=False, label=_("Funding Source"))
    division = forms.MultipleChoiceField(required=False, label="Divisions (Leave blank to select all)")
    section = forms.MultipleChoiceField(required=False, label="Sections (Leave blank to select all)")
    omcatagory = forms.MultipleChoiceField(required=False, label="O&M Catagories (Leave blank to select all)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all() if fy.projects.count() > 0]
        fy_choices.insert(0, (None, "-----"))
        self.fields['funding_src'].choices = views.get_funding_sources()
        self.fields['region'].choices = views.get_region_choices()
        self.fields['division'].choices = views.get_division_choices()
        self.fields["section"].choices = views.get_section_choices()
        self.fields["omcatagory"].choices = views.get_omcatagory_choices()
        self.fields["fiscal_year"].choices = fy_choices


class OTForm(forms.ModelForm):
    class Meta:
        model = models.Staff
        fields = ["overtime_hours", "overtime_description"]
        widgets = {
            'overtime_hours': forms.HiddenInput(),
            'overtime_description': forms.HiddenInput(),
        }


class UserCreateForm(forms.Form):
    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"))
    email1 = forms.EmailField(label=_("Email"))
    email2 = forms.EmailField(label=_("Confirm email address"))

    def clean_email1(self):
        new_email = self.cleaned_data['email1']
        # check to make sure is not a duplicate
        if User.objects.filter(email__iexact=new_email).count() > 0:
            raise forms.ValidationError("This email address already exists in the database.")
        # check to make sure is a DFO email
        if new_email.lower().endswith("@dfo-mpo.gc.ca") == False:
            raise forms.ValidationError(_("The email address provided must be a DFO email address."))

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return new_email

    def clean(self):
        cleaned_data = super().clean()
        first_email = cleaned_data.get("email1")
        second_email = cleaned_data.get("email2")

        if first_email and second_email:
            # Only do something if both fields are valid so far.

            # verify the two emails are the same
            if first_email.lower() != second_email.lower():
                raise forms.ValidationError(_("Please make sure the two email addresses provided match."))


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


class StatusForm(forms.ModelForm):
    class Meta:
        model = models.Status
        fields = "__all__"


StatusFormset = modelformset_factory(
    model=models.Status,
    form=StatusForm,
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


class ProgramForm(forms.ModelForm):
    class Meta:
        model = models.Program
        fields = "__all__"
        widgets = {
            'national_responsibility_eng': forms.Textarea(attrs={"rows": 3}),
            'national_responsibility_fra': forms.Textarea(attrs={"rows": 3}),
            'program_inventory': forms.Textarea(attrs={"rows": 3}),
            'funding_source_and_type': forms.Textarea(attrs={"rows": 3}),
            'regional_program_name_eng': forms.Textarea(attrs={"rows": 3}),
            'regional_program_name_fra': forms.Textarea(attrs={"rows": 3}),
            'examples': forms.Textarea(attrs={"rows": 3}),
            'short_name': forms.Textarea(attrs={"rows": 3}),
        }


ProgramFormset = modelformset_factory(
    model=models.Program,
    form=ProgramForm,
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
        section_choices = views.get_section_choices(all=False)

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
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"})
        }


UpcomingDateFormset = modelformset_factory(
    model=models.UpcomingDate,
    form=UpcomingDateForm,
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


class TempForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            # "project_title",
            # "section",
            # "funding_sources",
            "activity_type",
            "default_funding_source",
            "functional_group",
        ]
        widgets = {
            'default_funding_source': forms.Select(attrs=chosen_js),
            'functional_group': forms.Select(attrs=chosen_js),
            # 'activity_type': forms.SelectMultiple(attrs=chosen_js),
            # 'tags': forms.SelectMultiple(attrs=chosen_js),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        functional_group_choices = [(tg.id, str(tg)) for tg in kwargs.get("instance").section.functional_groups.all()]
        functional_group_choices.insert(0, tuple((None, "---")))
        self.fields['functional_group'].choices = functional_group_choices


TempFormset = modelformset_factory(
    model=models.Project,
    form=TempForm,
    extra=0,
)


class FileForm(forms.ModelForm):
    class Meta:
        model = models.File
        exclude = ["date_created", ]
        # fields = "__all__"
        # labels={
        #     'district':mark_safe("District (<a href='#' >search</a>)"),
        #     'vessel':mark_safe("Vessel CFVN (<a href='#' >add</a>)"),
        # }
        widgets = {
            'project': forms.HiddenInput(),
            'status_report': forms.HiddenInput(),
            # 'end_date':forms.DateInput(attrs={'type': 'date'}),
        }


class IWForm(forms.Form):
    fiscal_year = forms.ChoiceField(label=_("Fiscal year"), widget=forms.Select(attrs=chosen_js), required=True)
    region = forms.ChoiceField(label=_("Region"), widget=forms.Select(attrs=chosen_js), required=False)
    division = forms.ChoiceField(label=_("Division"), widget=forms.Select(attrs=chosen_js), required=False)
    section = forms.ChoiceField(label=_("Section"), widget=forms.Select(attrs=chosen_js), required=False)

    def __init__(self, *args, **kwargs):
        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all() if fy.projects.count() > 0]

        super().__init__(*args, **kwargs)

        region_choices = views.get_region_choices()
        region_choices.insert(0, tuple((None, "---")))

        division_choices = views.get_division_choices()
        section_choices = views.get_section_choices(full_name=False)

        # if there is a region, we should limit the divisions and sections
        if kwargs.get("initial"):
            if kwargs.get("initial").get("region"):
                # overwrite the current choice list if a region is present
                division_choices = views.get_division_choices(region_filter=kwargs.get("initial").get("region"))
                section_choices = views.get_section_choices(region_filter=kwargs.get("initial").get("region"), full_name=False)
        division_choices.insert(0, tuple((None, "---")))

        # if there is a division, we should limit the sections
        if kwargs.get("initial"):
            if kwargs.get("initial").get("division"):
                # overwrite the current choice list if a division is present
                section_choices = views.get_section_choices(division_filter=kwargs.get("initial").get("division"), full_name=False)
        section_choices.insert(0, tuple((None, "---")))

        self.fields['fiscal_year'].choices = fy_choices
        self.fields['region'].choices = region_choices
        self.fields['division'].choices = division_choices
        self.fields['section'].choices = section_choices


class ApprovalQueryBuildForm(forms.Form):
    region = forms.ChoiceField(required=False, label="Region", widget=forms.RadioSelect())
    fiscal_year = forms.ChoiceField(required=False)

    # division = forms.MultipleChoiceField(required=False, label="Divisions (Leave blank to select all)")
    # section = forms.MultipleChoiceField(required=False, label="Sections (Leave blank to select all)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all() if fy.projects.count() > 0]
        fy_choices.insert(0, (None, "-----"))
        self.fields['region'].choices = views.get_region_choices()
        # self.fields['division'].choices = views.get_division_choices()
        # self.fields["section"].choices = views.get_section_choices()
        self.fields["fiscal_year"].choices = fy_choices


class ProjectApprovalForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            "allocated_budget",
            "meeting_notes",
            "approved",
        ]
        widgets = {
            'approved': forms.Select(choices=NULLYESNO_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["approved"].choices = YESNO_CHOICES


ProjectApprovalFormset = modelformset_factory(
    model=models.Project,
    form=ProjectApprovalForm,
    extra=0,
)
