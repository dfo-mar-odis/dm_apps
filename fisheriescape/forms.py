# from django import forms
from django.contrib.gis import forms

from . import models

chosen_js = {"class": "chosen-select-contains"}
multi_select_js = {"class": "multi-select"}
attr_fp_date = {"class": "fp-date", "placeholder": "Click to select a date.."}


class SpeciesForm(forms.ModelForm):
    class Meta:
        model = models.Species
        fields = "__all__"
        widgets = {

        }


class FisheryForm(forms.ModelForm):
    class Meta:
        model = models.Fishery
        fields = "__all__"
        widgets = {
            'fishery_area': forms.SelectMultiple(attrs=chosen_js),
            'start_date': forms.DateInput(attrs=attr_fp_date),
            'end_date': forms.DateInput(attrs=attr_fp_date),
            'marine_mammals': forms.SelectMultiple(attrs=chosen_js),
        }


class FisheryAreaForm(forms.ModelForm):
    # polygon = forms.MultiPolygonField(widget=forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))

    class Meta:
        model = models.FisheryArea
        fields = "__all__"
        # polygon = forms.MultiPolygonField(widget=forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))
        widgets = {
            'polygon': forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500})
        }


class FisheryAreaForm2(forms.ModelForm):
    class Meta:
        model = models.FisheryArea
        fields = "__all__"
        widgets = {
        }
