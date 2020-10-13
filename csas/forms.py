from django import forms
from django.contrib.auth.context_processors import auth

from . import models
from . import custom_widgets

from django.forms import Textarea
from django.contrib.auth.models import User


class RequestForm(forms.ModelForm):
    class Meta:
        model = models.ReqRequest

        # fields shown on screen
        exclude = ["assigned_req_id", "adviser_submission", "rd_submission", "decision_date"]    # except listed fields

        # use some widgets
        widgets = {
            "issue": Textarea(attrs={"rows": 1, "cols": 20}),
            "rationale": Textarea(attrs={"rows": 1, "cols": 20}),
            "rationale_for_timing": Textarea(attrs={"rows": 1, "cols": 20}),
            "funding_notes": Textarea(attrs={"rows": 1, "cols": 20}),
            # "region": forms.Select(attrs={"class": "chosen-select-contains"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['program_contact'].widgets = forms.Select(choices=models.ConContact.objects.all())
        # self.fields['adviser_submission'].widgets = forms.DateField(help_text="Select date")


class RequestFormCSAS(forms.ModelForm):
    class Meta:
        model = models.ReqRequestCSAS

        exclude = []
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['program_contact'].widgets = forms.Select(choices=models.ConContact.objects.all())
        # self.fields['adviser_submission'].widgets = forms.DateField(help_text="Select date")


class ContactForm(forms.ModelForm):
    class Meta:
        model = models.ConContact
        exclude = []
        widgets = {
            "notes": Textarea(attrs={"rows": 1, "cols": 20}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # a lot being done here.
        # 1. Get all contact objects with models.ConContact.objects.all()
        # 2. Get all of the existing affiliation values for those objects with .values_list('affiliation')
        # 3. Remove duplicate affiliations with .distinct()
        # 4. iterate through the 'queryset' with for a in __returned queryset__
        # 6. save all the created tuples as an array with affilitations = [tuple]
        affiliations = [a[0] for a in models.ConContact.objects.all().order_by('affiliation').values_list('affiliation').distinct()]

        # pass the list of values to the select widget
        self.fields['affiliation'].widget = custom_widgets.SelectAdd(data_list=affiliations, name="affiliation-list")


class MeetingForm(forms.ModelForm):
    class Meta:
        model = models.MetMeeting
        exclude = []
        widgets = {
            "status_notes":   Textarea(attrs={"rows": 1, "cols": 20}),
            "chair_comments": Textarea(attrs={"rows": 1, "cols": 20}),
            "description":    Textarea(attrs={"rows": 1, "cols": 20})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['program_contact'].wigets = forms.Select(choices=models.ConContact.objects.all())


class MeetingFormDocs(forms.ModelForm):
    class Meta:
        model = models.MedMeetingDocs
        exclude = []
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['program_contact'].wigets = forms.Select(choices=models.ConContact.objects.all())


class MeetingFormDFOPars(forms.ModelForm):
    class Meta:
        model = models.MetMeetingDFOPars
        exclude = []
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['program_contact'].wigets = forms.Select(choices=models.ConContact.objects.all())


class MeetingFormOtherPars(forms.ModelForm):
    class Meta:
        model = models.MetMeetingOtherPars
        exclude = []
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['program_contact'].wigets = forms.Select(choices=models.ConContact.objects.all())


class MeetingFormOMCosts(forms.ModelForm):
    class Meta:
        model = models.MocMeetingOMCosts
        exclude = []
        widgets = {
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['program_contact'].wigets = forms.Select(choices=models.ConContact.objects.all())


class MeetingFormMedia(forms.ModelForm):
    class Meta:
        model = models.MemMeetingMedia
        exclude = []
        widgets = {
            "media_attention_yes": Textarea(attrs={"rows": 3, "cols": 20}),
            "media_attention_no":  Textarea(attrs={"rows": 3, "cols": 20}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['program_contact'].wigets = forms.Select(choices=models.ConContact.objects.all())


class PublicationForm(forms.ModelForm):
    class Meta:
        model = models.PubPublication
        exclude = []
        widgets = {
            "other_authors": Textarea(attrs={"rows": 3, "cols": 20}),
            "citation": Textarea(attrs={"rows": 1, "cols": 20}),
            # don't know why, client can't be set as rows=3, otherwise the name list doesn't show
            # as if the text area is too small
            # "client": Textarea(attrs={"rows": 3, "cols": 20}),
            "description": Textarea(attrs={"rows": 3, "cols": 20})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['citation'].wigets = forms.Select(choices=models.PubPublication.objects.all())


class PublicationFormStatus(forms.ModelForm):
    class Meta:
        model = models.PubPublicationStatus
        exclude = []
        widgets = {
            "status_comments": Textarea(attrs={"rows": 2, "cols": 20}),
            # "submitted_by": Textarea(attrs={"rows": 1, "cols": 20}),
            # "appr_by_chair": Textarea(attrs={"rows": 2, "cols": 20}),
            # "appr_by_CSAS": Textarea(attrs={"rows": 2, "cols": 20}),
            # "appr_by_dir": Textarea(attrs={"rows": 2, "cols": 20}),
            # "appr_by": Textarea(attrs={"rows": 2, "cols": 20}),
            "notes": Textarea(attrs={"rows": 3, "cols": 20})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['citation'].wigets = forms.Select(choices=models.PubPublication.objects.all())


class PublicationFormTransInfo(forms.ModelForm):
    class Meta:
        model = models.PubPublicationTransInfo
        exclude = []
        widgets = {
            "trans_note": Textarea(attrs={"rows": 3, "cols": 20}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['citation'].wigets = forms.Select(choices=models.PubPublication.objects.all())


class PublicationFormDocLocation(forms.ModelForm):
    class Meta:
        model = models.PubPublicationDocLocation
        exclude = []
        widgets = {
            "p1": Textarea(attrs={"class": "hidden", "rows": 0, "cols": 0})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['citation'].wigets = forms.Select(choices=models.PubPublication.objects.all())


class PublicationFormOMCosts(forms.ModelForm):
    class Meta:
        model = models.PubPublicationOMCosts
        exclude = []
        widgets = {
            "p1": Textarea(attrs={"class": "hidden", "rows": 0, "cols": 0})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['citation'].wigets = forms.Select(choices=models.PubPublication.objects.all())


class PublicationFormComResults(forms.ModelForm):
    class Meta:
        model = models.PubPublicationComResults
        exclude = []
        widgets = {
            "p1": Textarea(attrs={"class": "hidden", "rows": 0, "cols": 0}),
            "p2": Textarea(attrs={"class": "hidden", "rows": 0, "cols": 0}),
            "pub_description": Textarea(attrs={"rows": 2, "cols": 20})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['citation'].wigets = forms.Select(choices=models.PubPublication.objects.all())

# End of forms.py
# ----------------------------------------------------------------------------------------------------
# 1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
