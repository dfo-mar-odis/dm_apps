from django import forms
from django.contrib.auth.models import User
from django.core import validators
from . import models
chosen_js = {"class": "chosen-select-contains"}


class SectionForm(forms.ModelForm):
    class Meta:
        model = models.Section
        exclude = [
            'date_last_modified',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'head': forms.Select(attrs=chosen_js),

        }

    def __init__(self, *args, **kwargs):
        USER_CHOICES = [(u.id, "{}, {}".format(u.last_name, u.first_name)) for u in
                        User.objects.all().order_by("last_name", "first_name")]
        USER_CHOICES.insert(0, tuple((None, "---")))

        DIVISION_CHOICES = [(obj.id, "{} - {}".format(obj.branch, obj.name)) for obj in
                        models.Division.objects.all().order_by("branch__region", "branch", "name")]
        DIVISION_CHOICES .insert(0, tuple((None, "---")))

        super().__init__(*args, **kwargs)
        self.fields['head'].choices = USER_CHOICES
        self.fields['division'].choices = DIVISION_CHOICES


class DivisionForm(forms.ModelForm):
    class Meta:
        model = models.Division
        exclude = [
            'date_last_modified',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'head': forms.Select(attrs=chosen_js),
        }

    def __init__(self, *args, **kwargs):
        BRANCH_CHOICES = [(obj.id, "{} - {}".format(obj.region, obj.name)) for obj in
                            models.Branch.objects.all().order_by("region", "name")]
        BRANCH_CHOICES.insert(0, tuple((None, "---")))

        super().__init__(*args, **kwargs)
        self.fields['branch'].choices = BRANCH_CHOICES

class BranchForm(forms.ModelForm):
    class Meta:
        model = models.Branch
        exclude = [
            'date_last_modified',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'head': forms.Select(attrs=chosen_js),

        }


class RegionForm(forms.ModelForm):
    class Meta:
        model = models.Region
        exclude = [
            'date_last_modified',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'head': forms.Select(attrs=chosen_js),

        }