from django import forms
from django.forms import modelformset_factory
from django.utils.translation import gettext as _
from shared_models import models as shared_models
from masterlist import models as ml_models
from . import models

attr_chosen_contains = {"class": "chosen-select-contains"}
attr_chosen = {"class": "chosen-select"}
attr_fp_date = {"class": "fp-date", "placeholder": "Select Date.."}
attr_fp_date_time = {"class": "fp-date-time", "placeholder": "Select Date and Time.."}
attr_fp_date_time_email = {"class": "fp-date-time green-borders", "placeholder": "Select Date and Time.."}

multi_select_js = {"class": "multi-select"}
class_editable = {"class": "editable"}

YES_NO_CHOICES = (
    (True, _("Yes")),
    (False, _("No")),
)

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = ml_models.Organization
        fields = [
            'name_eng',
            'name_fre',
            'abbrev',
            'address',
            'city',
            'postal_code',
            'province',
            'phone',
            'fax',
            'dfo_contact_instructions',
            'notes',
            'grouping',
            'regions',
            'sectors',
            'last_modified_by',
        ]
        widgets = {
            'key_species': forms.Textarea(attrs={"rows": 2}),
            'dfo_contact_instructions': forms.Textarea(attrs={"rows": 2}),
            'notes': forms.Textarea(attrs={"rows": 2}),
            'last_modified_by': forms.HiddenInput(),
        }


class MemberForm(forms.ModelForm):
    class Meta:
        model = ml_models.OrganizationMember
        fields = [
            'person',
            'organization',
            'role',
            # 'role_notes',
            'notes',
            'last_modified_by',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={"rows": 2}),
            'organization': forms.HiddenInput(),
            'last_modified_by': forms.HiddenInput(),
        }


class PersonForm(forms.ModelForm):
    class Meta:
        model = ml_models.Person
        fields = [
            "designation",
            "first_name",
            "last_name",
            "email_1",
            "email_2",
            "phone_1",
            "phone_2",
            "cell",
            "fax",
            "language",
            "email_block",
        ]

        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'language': forms.Select(attrs=attr_chosen),
            # 'email_block': forms.Textarea(attrs=class_editable),
        }


class NewPersonForm(forms.ModelForm):
    organization = forms.ChoiceField(widget=forms.Select(attrs=attr_chosen_contains))
    role = forms.CharField(required=False)

    class Meta:
        model = ml_models.Person
        fields = [
            "designation",
            "first_name",
            "last_name",
            "email_1",
            "email_2",
            "phone_1",
            "phone_2",
            "cell",
            "fax",
            "language",
        ]

        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'language': forms.Select(attrs=attr_chosen),
            # 'notes': forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        org_choices = [(o.id, "{} ({})".format(str(o), o.abbrev)) for o in ml_models.Organization.objects.all()]
        org_choices.insert(0, (None, "------"))
        self.fields['organization'].choices = org_choices


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'path_number',
            'program_reference_number',
            'organization',
            'language',
            'title',
            'program',
            'priority_area_or_threats',
            'status',
            'regions',
            'start_year',
            'project_length',
            'date_completed',
            'last_modified_by',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'organization': forms.Select(attrs=attr_chosen_contains),
            'program': forms.Select(attrs=attr_chosen_contains),
            'priority_area_or_threats': forms.SelectMultiple(attrs=attr_chosen_contains),
            'language': forms.Select(attrs=attr_chosen_contains),
            'status': forms.Select(attrs=attr_chosen_contains),
            'start_year': forms.Select(attrs=attr_chosen_contains),
            'regions': forms.SelectMultiple(attrs=attr_chosen_contains),
            'title': forms.Textarea(attrs={"rows": 4}),
            'date_completed': forms.TextInput(attrs=attr_fp_date),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        org_choices = [(o.id, "{} ({})".format(str(o), o.abbrev)) for o in ml_models.Organization.objects.all()]
        org_choices.insert(0, (None, "------"))
        self.fields['organization'].choices = org_choices


class NewProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'regions',
            'path_number',
            'program_reference_number',
            'organization',
            'language',
            'title',
            'program',
            'priority_area_or_threats',
            'status',
            'start_year',
            'requested_funding_y1',
            'requested_funding_y2',
            'requested_funding_y3',
            'requested_funding_y4',
            'requested_funding_y5',
            'last_modified_by',
            'initiation_date',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'initiation_date': forms.HiddenInput(),
            'organization': forms.Select(attrs=attr_chosen_contains),
            'program': forms.Select(attrs=attr_chosen_contains),
            'priority_area_or_threats': forms.SelectMultiple(attrs=attr_chosen_contains),
            'language': forms.Select(attrs=attr_chosen_contains),
            'status': forms.Select(attrs=attr_chosen_contains),
            'start_year': forms.Select(attrs=attr_chosen_contains),
            'regions': forms.SelectMultiple(attrs=attr_chosen_contains),
            'title': forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        org_choices = [(o.id, "{} ({})".format(str(o), o.abbrev)) for o in ml_models.Organization.objects.all()]
        org_choices.insert(0, (None, "------"))
        self.fields['organization'].choices = org_choices


class ProjectPersonForm(forms.ModelForm):
    class Meta:
        model = models.ProjectPerson
        fields = [
            'person',
            'project',
            'role',
            'last_modified_by',
        ]
        widgets = {
            'project': forms.HiddenInput(),
            'role': forms.Select(attrs=attr_chosen_contains),
            'last_modified_by': forms.HiddenInput(),
        }


class ProjectYearForm(forms.ModelForm):
    class Meta:
        model = models.ProjectYear
        fields = [
            'fiscal_year',
            'project',
            'annual_funding',
            'last_modified_by',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'project': forms.HiddenInput(),
        }


class InitiationForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'title',
            'title_abbrev',
            'initiation_date',
            'initiation_type',
            'initiation_acknowledgement_sent',
            'requested_funding_y1',
            'requested_funding_y2',
            'requested_funding_y3',
            'requested_funding_y4',
            'requested_funding_y5',
            'overview',
            'notes',
            'last_modified_by',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'title': forms.Textarea(attrs={"rows": 3}),
            'notes': forms.Textarea(attrs={"rows": 3}),
            'initiation_date': forms.DateInput(attrs=attr_fp_date),
            'initiation_acknowledgement_sent': forms.DateInput(attrs=attr_fp_date),
        }


class EOIForm(forms.ModelForm):
    class Meta:
        model = models.ExpressionOfInterest
        fields = [
            'project',
            'date_received',
            'description',
            'coordinator_notified',
            'project_eligible',
            'feedback',
            'feedback_sent',
            'last_modified_by',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'project': forms.HiddenInput(),

            'feedback': forms.Textarea(attrs={"rows": 5}),
            'coordinator_notified': forms.DateInput(attrs=attr_fp_date_time),
            'date_received': forms.DateInput(attrs={"type": "date"}),
            'feedback_sent': forms.DateInput(attrs=attr_fp_date),
        }


class ProjectReviewForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'regional_score',
            'rank',
            'application_submission_date',
            'submission_accepted',
            'recommended_funding_y1',
            'recommended_funding_y2',
            'recommended_funding_y3',
            'recommended_funding_y4',
            'recommended_funding_y5',
            'recommended_overprogramming',
            'regrets_or_op_letter_sent_date',
            'last_modified_by',
            'notes',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'notes': forms.Textarea(attrs={"rows": 3}),
            'application_submission_date': forms.DateInput(attrs=attr_fp_date_time),
            'regrets_or_op_letter_sent_date': forms.DateInput(attrs=attr_fp_date),
        }


class NegotiationForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'risk_assessment_score',
            'negotiations_workplan_completion_date',
            'negotiations_financials_completion_date',
            'negotiation_letter_sent',
            'notes',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'notes': forms.Textarea(attrs={"rows": 5}),
            'negotiations_workplan_completion_date': forms.DateInput(attrs=attr_fp_date),
            'negotiations_financials_completion_date': forms.DateInput(attrs=attr_fp_date),
            'negotiation_letter_sent': forms.DateInput(attrs=attr_fp_date_time_email),
        }


class CAChecklistForm(forms.ModelForm):
    class Meta:
        model = models.ContributionAgreementChecklist
        exclude = [
            "date_last_modified",
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'project': forms.HiddenInput(),

            'feedback': forms.Textarea(attrs={"rows": 5}),
            'review_completion_date': forms.DateInput(attrs=attr_fp_date_time),
            'date_assessed': forms.DateInput(attrs=attr_fp_date_time),
        }


class CAAdministrationForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'risk_assessment_score',
            'schedule_5_complete',
            'advance_payment',
            'draft_ca_sent_to_proponent',
            'draft_ca_proponent_approved',
            'draft_ca_ready',
            'draft_ca_sent_to_manager',
            'draft_ca_manager_approved',
            'draft_ca_sent_to_nhq',
            'aip_received',
            'final_ca_received',
            'final_ca_sent_to_proponent',
            'final_ca_proponent_signed',
            'final_ca_sent_to_nhq',
            'advance_payment_sent_to_nhq',
            'final_ca_nhq_signed',
            'notes',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'notes': forms.Textarea(attrs={"rows": 4}),

            'schedule_5_complete': forms.DateInput(attrs=attr_fp_date),
            'draft_ca_sent_to_proponent': forms.DateInput(attrs=attr_fp_date),
            'draft_ca_proponent_approved': forms.DateInput(attrs=attr_fp_date),
            'draft_ca_ready': forms.DateInput(attrs=attr_fp_date),
            'draft_ca_sent_to_manager': forms.DateInput(attrs=attr_fp_date),
            'draft_ca_sent_to_nhq': forms.DateInput(attrs=attr_fp_date),
            'draft_ca_manager_approved': forms.DateInput(attrs=attr_fp_date),
            'aip_received': forms.DateInput(attrs=attr_fp_date),
            'final_ca_received': forms.DateInput(attrs=attr_fp_date),
            'final_ca_proponent_signed': forms.DateInput(attrs=attr_fp_date),
            'final_ca_sent_to_proponent': forms.DateInput(attrs=attr_fp_date),
            'final_ca_sent_to_nhq': forms.DateInput(attrs=attr_fp_date),
            'advance_payment_sent_to_nhq': forms.DateInput(attrs=attr_fp_date),
            'final_ca_nhq_signed': forms.DateInput(attrs=attr_fp_date),
        }


class ActivitiesForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'last_modified_by',
            'activities',
            'notes',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'notes': forms.Textarea(attrs={"rows": 4}),
            'activities': forms.SelectMultiple(attrs=multi_select_js),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        my_project = kwargs["instance"]
        if my_project.program:
            activity_choices = [(obj.id, str(obj)) for obj in models.Activity.objects.filter(program=my_project.program)]
            self.fields["activities"].choices = activity_choices


class PaymentForm(forms.ModelForm):
    class Meta:
        model = models.Payment
        fields = [
            'project_year',
            'claim_number',
            'advance_amount',
            'reimbursement_amount',
            'from_period',
            'to_period',
            'final_payment',
            'materials_submitted',
            'nhq_notified',
            'payment_confirmed',
            'notes',
            'last_modified_by',
        ]
        widgets = {
            'project_year': forms.HiddenInput(),
            'last_modified_by': forms.HiddenInput(),
            'to_period': forms.DateInput(attrs={"type": "date"}),
            'from_period': forms.DateInput(attrs={"type": "date"}),
            'nhq_notified': forms.DateInput(attrs={"type": "date"}),
            'notes': forms.Textarea(attrs={"rows": "4"}),
            'materials_submitted': forms.Select(choices=YES_NO_CHOICES),
            'payment_confirmed': forms.Select(choices=YES_NO_CHOICES),
        }


class FileForm(forms.ModelForm):
    class Meta:
        model = models.File
        fields = "__all__"
        widgets = {
            'project': forms.HiddenInput(),
            'uploaded_by': forms.HiddenInput(),
            'date_modified': forms.HiddenInput(),
        }




class ReportSearchForm(forms.Form):

    REPORT_CHOICES = (
        (None, "------"),
        (1, "Negotiations summary"),
    )

    report = forms.ChoiceField(required=True, choices=REPORT_CHOICES)
    fiscal_year = forms.ChoiceField(required=True)
    programs = forms.MultipleChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all() if fy.projects.count() > 0]
        fy_choices.insert(0, (None, "-----"))
        program_choices = [(obj.id, str(obj)) for obj in models.Program.objects.all() if obj.projects.count() > 0]

        self.fields["fiscal_year"].choices = fy_choices
        self.fields["programs"].choices = program_choices
