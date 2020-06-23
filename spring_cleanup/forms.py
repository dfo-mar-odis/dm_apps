from django import forms
from django.core import validators
from django.forms import modelformset_factory

from shared_models import models as shared_models

from . import models

attr_fp_date_time = {"class": "fp-date-time", "placeholder": "Select Date and Time.."}
attr_fp_date = {"class": "fp-date", "placeholder": "Click to select a date.."}
multi_select_js = {"class": "multi-select"}
chosen_js = {"class": "chosen-select-contains"}


class OutingForm(forms.ModelForm):
    class Meta:
        model = models.Outing
        exclude = [
            'route',
            'fiscal_year',
        ]
        widgets = {
            'date': forms.TextInput(attrs=attr_fp_date),
            'birds': forms.SelectMultiple(attrs=chosen_js),
            'users': forms.SelectMultiple(attrs=chosen_js),
        }
