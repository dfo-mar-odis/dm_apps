from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.forms import modelformset_factory
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from . import models
from shared_models import models as shared_models

chosen_js = {"class": "chosen-select-contains"}
attr_fp_date_time = {"class": "fp-date-time", "placeholder": "Select Date and Time.."}
attr_fp_date = {"class": "fp-date", "placeholder": "Select a Date.."}


class ResourceCreateForm(forms.ModelForm):
    add_custodian = forms.BooleanField(required=False, label="Add yourself as custodian")
    # add_point_of_contact = forms.BooleanField(required=False, label="Add Regional Data Manager as a Point of Contact")

    class Meta:
        model = models.Resource
        exclude = [
            'file_identifier',
            'uuid',
            'date_verified',
            'date_last_modified',
            'fgp_publication_date',
            'citations',
            'keywords',
            'people',
            'flagged_4_publication',
            'flagged_4_deletion',
            'completedness_report',
            'completedness_rating',
            'translation_needed',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'title_eng': forms.Textarea(attrs={"rows": 5}),
            'title_fre': forms.Textarea(attrs={"rows": 5}),
            "purpose_eng": forms.Textarea(attrs={"rows": 5}),
            "purpose_fre": forms.Textarea(attrs={"rows": 5}),
            "descr_eng": forms.Textarea(attrs={"rows": 8}),
            "descr_fre": forms.Textarea(attrs={"rows": 8}),
            "physical_sample_descr_eng": forms.Textarea(attrs={"rows": 5}),
            "physical_sample_descr_fre": forms.Textarea(attrs={"rows": 5}),
            "sampling_method_eng": forms.Textarea(attrs={"rows": 5}),
            "sampling_method_fre": forms.Textarea(attrs={"rows": 5}),
            "resource_constraint_eng": forms.Textarea(attrs={"rows": 5}),
            "resource_constraint_fre": forms.Textarea(attrs={"rows": 5}),
            "qc_process_descr_eng": forms.Textarea(attrs={"rows": 5}),
            "qc_process_descr_fre": forms.Textarea(attrs={"rows": 5}),
            "storage_envr_notes": forms.Textarea(attrs={"rows": 5}),
            "parameters_collected_eng": forms.Textarea(attrs={"rows": 5}),
            "parameters_collected_fre": forms.Textarea(attrs={"rows": 5}),
            "additional_credit": forms.Textarea(attrs={"rows": 5}),
            "analytic_software": forms.Textarea(attrs={"rows": 5}),
            "notes": forms.Textarea(attrs={"rows": 5}),
            "parent": forms.NumberInput(),
            "section": forms.Select(attrs=chosen_js),
        }
        labels = {
            "section": "Section (Region / Branch / Division / Section)",
            "parent": _("Parent Resource Id (click on field to find a parent resource)"),
        }

    def __init__(self, *args, **kwargs):
        SECTION_CHOICES = [(s.id, s.full_name) for s in
                           shared_models.Section.objects.all().order_by("division__branch__region", "division__branch", "division", "name")]
        SECTION_CHOICES.insert(0, tuple((None, "---")))



        resource_type_choices = [(obj.id, "{}  ({})".format(obj.label, obj.notes) if obj.notes else "{}".format(obj.label)) for obj in
                           models.ResourceType.objects.all()]
        resource_type_choices .insert(0, tuple((None, "---")))

        status_choices = [(obj.id, "{}  ({})".format(obj.label, obj.notes) if obj.notes else "{}".format(obj.label)) for obj in
                                 models.Status.objects.all()]
        status_choices.insert(0, tuple((None, "---")))

        super().__init__(*args, **kwargs)
        self.fields['section'].choices = SECTION_CHOICES
        self.fields['resource_type'].choices = resource_type_choices
        self.fields['status'].choices = status_choices


class ResourceForm(forms.ModelForm):
    class Meta:
        model = models.Resource
        exclude = [
            'file_identifier',
            'uuid',
            'date_verified',
            # 'date_last_modified',
            # 'fgp_publication_date',
            'citations',
            'keywords',
            'people',
            'flagged_4_publication',
            'flagged_4_deletion',
            'completedness_rating',
            'completedness_report',
            'translation_needed',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'date_last_modified': forms.HiddenInput(),
            'title_eng': forms.Textarea(attrs={"rows": 5}),
            'title_fre': forms.Textarea(attrs={"rows": 5}),
            "purpose_eng": forms.Textarea(attrs={"rows": 5}),
            "purpose_fre": forms.Textarea(attrs={"rows": 5}),
            "descr_eng": forms.Textarea(attrs={"rows": 8}),
            "descr_fre": forms.Textarea(attrs={"rows": 8}),
            "physical_sample_descr_eng": forms.Textarea(attrs={"rows": 5}),
            "physical_sample_descr_fre": forms.Textarea(attrs={"rows": 5}),
            "sampling_method_eng": forms.Textarea(attrs={"rows": 5}),
            "sampling_method_fre": forms.Textarea(attrs={"rows": 5}),
            "resource_constraint_eng": forms.Textarea(attrs={"rows": 5}),
            "resource_constraint_fre": forms.Textarea(attrs={"rows": 5}),
            "qc_process_descr_eng": forms.Textarea(attrs={"rows": 5}),
            "qc_process_descr_fre": forms.Textarea(attrs={"rows": 5}),
            "storage_envr_notes": forms.Textarea(attrs={"rows": 5}),
            "parameters_collected_eng": forms.Textarea(attrs={"rows": 5}),
            "distribution_formats": forms.SelectMultiple(attrs=chosen_js),
            "parameters_collected_fre": forms.Textarea(attrs={"rows": 5}),
            "additional_credit": forms.Textarea(attrs={"rows": 5}),
            "analytic_software": forms.Textarea(attrs={"rows": 5}),
            "notes": forms.Textarea(attrs={"rows": 5}),
            "parent": forms.NumberInput(),
            "fgp_publication_date": forms.DateInput(attrs=attr_fp_date),
            "od_publication_date": forms.DateInput(attrs=attr_fp_date),
            "od_release_date": forms.DateInput(attrs=attr_fp_date),
            "last_revision_date": forms.DateInput(attrs=attr_fp_date),
            "paa_items": forms.SelectMultiple(attrs=chosen_js),
        }
        labels = {
            "section": "Section (Region / Branch / Division / Section)",
            "parent": _("Parent Resource Id (click on field to find a parent resource)"),
        }

    def __init__(self, *args, **kwargs):

        mandatory_fields = [
            'resource_type',
            'section',
            'title_eng',
            'title_fre',
            'status',
            'maintenance',
            'purpose_eng',
            'purpose_fre',
            'descr_eng',
            'descr_fre',
            'time_start_year',
            'resource_constraint_eng',
            'resource_constraint_fre',
            'security_use_limitation_eng',
            'security_use_limitation_fre',
            'security_classification',
            'distribution_formats',
            'data_char_set',
            'spat_representation',
            'spat_ref_system',
            'geo_descr_eng',
            'geo_descr_fre',
            'west_bounding',
            'south_bounding',
            'east_bounding',
            'north_bounding',
        ]

        mandatory_bilingual_fields = [
            'sampling_method_eng',
            'sampling_method_fre',
            'physical_sample_descr_eng',
            'physical_sample_descr_fre',
            'qc_process_descr_eng',
            'qc_process_descr_fre',
            'parameters_collected_eng',
            'parameters_collected_fre',
        ]

        optional_fields = [
            'time_start_day',
            'time_start_month',
            'time_end_day',
            'time_end_month',
            'time_end_year',
            'additional_credit',
            'parent',
            # 'fgp_publication_date',
        ]

        internal_fields = [
            'storage_envr_notes',
            'notes',
            'open_data_notes',
            'fgp_url',
            'public_url',
            'analytic_software',
        ]

        SECTION_CHOICES = [(s.id, s.full_name) for s in
                           shared_models.Section.objects.all().order_by("division__branch__region", "division__branch", "division",
                                                                        "name")]
        SECTION_CHOICES.insert(0, tuple((None, "---")))

        super().__init__(*args, **kwargs)
        self.fields['section'].choices = SECTION_CHOICES

        for field_key in self.fields:
            if field_key in mandatory_fields:
                self.fields[field_key].label = mark_safe('<span class="red-font" data-toggle="tooltip" title="{}">{}</span>'.format(
                    _("This is a mandatory field in the Federal Geospatial Platform (FGP)"),
                    self.fields[field_key].label,
                ))
            elif field_key in mandatory_bilingual_fields:
                self.fields[field_key].label = mark_safe('<span class="orange-font" data-toggle="tooltip" title="{}">{}</span>'.format(
                    _("This is an optional field in the Federal Geospatial Platform (FGP), however if present, it needs to be entered "
                      "in both English and French"),
                    self.fields[field_key].label,
                ))
            elif field_key in internal_fields:
                self.fields[field_key].label = mark_safe('<span class="purple-font" data-toggle="tooltip" title="{}">{}</span>'.format(
                    _("This is an optional internal field (DFO only) and does not get published to the Federal Geospatial Platform (FGP)"),
                    self.fields[field_key].label,
                ))
            else:
                self.fields[field_key].label = mark_safe('<span class="green-font" data-toggle="tooltip" title="{}">{}</span>'.format(
                    _("This is an optional field"),
                    self.fields[field_key].label,
                ))


class ResourceKeywordForm(forms.ModelForm):
    class Meta:
        model = models.Resource
        fields = [
            'keywords',
        ]
        widgets = {
            "keywords": forms.SelectMultiple(attrs=chosen_js),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        keyword_choices = []
        for obj in models.Keyword.objects.all().order_by("keyword_domain", "text_value_eng"):
            if obj.keyword_domain_id == 8:
                keyword_choices.append(
                    (obj.id, "[{}] {}".format("ISO Topic Category", obj.text_value_eng))
                )
            elif obj.keyword_domain_id == 6:
                keyword_choices.append(
                    (obj.id, "[{}] {}".format("Core Subject", obj.text_value_eng))
                )
            elif obj.keyword_domain_id == 7:
                keyword_choices.append(
                    (obj.id, "[{}] {}".format("DFO Area", obj.text_value_eng))
                )
            elif obj.is_taxonomic:
                keyword_choices.append(
                    (obj.id, mark_safe("[{}] <em>{}</em> | {}".format("Taxonomic", obj.text_value_eng, obj.details)))
                )
            else:
                keyword_choices.append(
                    (obj.id, "[{}] {}".format("General", obj.text_value_eng))
                )
            # context['kcount_tc'] = self.object.keywords.filter(keyword_domain_id__exact=8).count()
            # context['kcount_cst'] = self.object.keywords.filter(keyword_domain_id__exact=6).count()
            # context['kcount_tax'] = self.object.keywords.filter(is_taxonomic__exact=True).count()
            # context['kcount_loc'] = self.object.keywords.filter(keyword_domain_id__exact=7).count()

            # context['kcount_other'] = self.object.keywords.filter(
            #     ~Q(keyword_domain_id=8) & ~Q(keyword_domain_id=6) & ~Q(keyword_domain_id=7) & Q(is_taxonomic=False)).count()
            #
            # topic
            # cat
            # core
            # sub
            # taxonoimic
            # dfo
            # area
            # other
            #
        self.fields["keywords"].choices = keyword_choices


class ResourcePersonForm(forms.ModelForm):
    class Meta:
        model = models.ResourcePerson
        fields = "__all__"
        labels = {
            'notes': "Notes (optional)",
        }
        widgets = {
            'resource': forms.HiddenInput(),
            'person': forms.HiddenInput(),
            'notes': forms.Textarea(attrs={'rows': "5"}),
            # 'last_modified_by':forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        role_choices = [(r.id, "{} - {}".format(r.role, r.notes)) for r in models.PersonRole.objects.all()]
        role_choices.insert(0, (None, "-----"))
        self.fields['role'].choices = role_choices
        self.fields['role'].choices = role_choices


class PersonForm(forms.Form):
    LANGUAGE_CHOICES = ((None, "---"),) + models.LANGUAGE_CHOICES

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(required=True)
    position_eng = forms.CharField(label="Position title (English)", required=False)
    position_fre = forms.CharField(label="Position title (French)", required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "000-000-0000 ext.000"}), required=False)
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, required=False)
    organization = forms.ModelChoiceField(required=False, queryset=models.Organization.objects.all())

    field_order = ["first_name", "last_name", "email", "position_eng", "position_fre", "phone", "language",
                   "organization"]


class PersonCreateForm(PersonForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        # if email already exists in db
        if User.objects.filter(email__iexact=email).count() > 0:
            raise forms.ValidationError("email address already exists in system.")
        return email


class KeywordForm(forms.ModelForm):
    class Meta:
        model = models.Keyword
        exclude = [
            'concept_scheme',
            'xml_block',
            'is_taxonomic',
        ]


class CitationForm(forms.ModelForm):
    class Meta:
        model = models.Citation
        fields = ("__all__")
        # exclude = [
        #     'concept_scheme',
        #     'xml_block',
        #     'is_taxonomic',
        # ]


class ResourceCertificationForm(forms.ModelForm):
    class Meta:
        model = models.ResourceCertification
        fields = "__all__"
        labels = {
            'notes': "Certification Notes",
        }
        widgets = {
            'certifying_user': forms.HiddenInput(),
            'resource': forms.HiddenInput(),
            'certification_date': forms.HiddenInput(),
            'notes': forms.Textarea(attrs={"rows": 2}),
        }


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
            'resource': forms.HiddenInput(),
            # 'end_date':forms.DateInput(attrs={'type': 'date'}),
        }


class DataResourceForm(forms.ModelForm):
    class Meta:
        model = models.DataResource
        fields = "__all__"
        widgets = {
            'resource': forms.HiddenInput(),
        }


class WebServiceForm(forms.ModelForm):
    class Meta:
        model = models.WebService
        fields = "__all__"
        widgets = {
            'resource': forms.HiddenInput(),
        }


class ResourceFlagging(forms.ModelForm):
    class Meta:
        model = models.Resource
        fields = ["flagged_4_deletion", "flagged_4_publication"]

        widgets = {
            'flagged_4_deletion': forms.HiddenInput(),
            'flagged_4_publication': forms.HiddenInput(),
        }


class ReportSearchForm(forms.Form):
    REPORT_CHOICES = (
        (None, "------"),
        (1, "Batch XML export"),
        (2, "Open Data Inventory - Quarterly Report"),
        (3, "Physical Collections Report (xlsx)"),
        # (2, "Organizational Report / Cue Card (PDF)"),
    )

    report = forms.ChoiceField(required=True, choices=REPORT_CHOICES)
    sections = forms.MultipleChoiceField(required=False, label='Region / Division / Section (Leave blank for all)')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sections'].choices = [(s.id, "{}".format(s.full_name)) for s in
                                           shared_models.Section.objects.all().order_by("division__branch__region", "division__branch",
                                                                                        'division', "name")]




class TempForm(forms.ModelForm):
    class Meta:
        model = models.Resource
        fields = ["title_eng", "section", "status", "descr_eng", "purpose_eng"]
        widgets = {
            'section': forms.Select(attrs=chosen_js),
            # 'tags': forms.SelectMultiple(attrs=chosen_js),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        SECTION_CHOICES = [(s.id, s.full_name) for s in
                           shared_models.Section.objects.all().order_by("division__branch__region", "division__branch", "division", "name")]
        SECTION_CHOICES.insert(0, tuple((None, "---")))

        self.fields['section'].choices = SECTION_CHOICES


TempFormSet = modelformset_factory(
    model=models.Resource,
    form=TempForm,
    extra=0,
)
