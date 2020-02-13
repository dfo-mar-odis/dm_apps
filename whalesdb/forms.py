from _ast import mod

from bokeh.core.property.dataspec import field
from django import forms
from whalesdb import models
from django.utils.translation import gettext_lazy as _
from django.forms.models import inlineformset_factory


class PrjForm(forms.ModelForm):

    class Meta:
        model = models.PrjProject
        exclude = []
        widgets = {
            'prj_description': forms.Textarea(attrs={"rows": 2}),
        }


class StnForm(forms.ModelForm):

    class Meta:
        model = models.StnStation
        exclude = []
        widgets = {
            'stn_notes': forms.Textarea(attrs={"rows": 2}),
        }


class MorForm(forms.ModelForm):
    class Meta:
        model = models.MorMooringSetup
        exclude = ['mor_setup_image']
        widgets = {
            'mor_notes': forms.Textarea(attrs={"rows": 2}),
        }