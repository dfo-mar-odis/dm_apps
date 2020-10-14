from django import forms
from . import models
from django.utils.safestring import mark_safe
from shared_models import models as shared_models
from django.forms import modelformset_factory


class DocForm(forms.ModelForm):
    class Meta:
        model = models.Doc
        fields = "__all__"
        labels={
            'district':mark_safe("District (<a href='#' >search</a>)"),
            'vessel':mark_safe("Vessel CFVN (<a href='#' >add</a>)"),
        }
        widgets = {
            'description':forms.Textarea(attrs={'rows': '5'}),
            'source':forms.Textarea(attrs={'rows': '5'}),

        }


class MissionForm(forms.ModelForm):
    class Meta:
        model = shared_models.Cruise
        exclude = ["season",]
        # labels={
        #     'district':mark_safe("District (<a href='#' >search</a>)"),
        #     'vessel':mark_safe("Vessel CFVN (<a href='#' >add</a>)"),
        # }
        widgets = {
            'start_date':forms.DateInput(attrs={'type': 'date'}),
            'end_date':forms.DateInput(attrs={'type': 'date'}),
        }

class BottleForm(forms.ModelForm):
    class Meta:
        model = models.Bottle
        exclude = ["mission",]
        # labels={
        #     'district':mark_safe("District (<a href='#' >search</a>)"),
        #     'vessel':mark_safe("Vessel CFVN (<a href='#' >add</a>)"),
        # }
        widgets = {
            'start_date':forms.DateInput(attrs={'type': 'date'}),
            'end_date':forms.DateInput(attrs={'type': 'date'}),
        }

class FileForm(forms.ModelForm):
    class Meta:
        model = models.File
        exclude = ["date_created",]
        # fields = "__all__"
        # labels={
        #     'district':mark_safe("District (<a href='#' >search</a>)"),
        #     'vessel':mark_safe("Vessel CFVN (<a href='#' >add</a>)"),
        # }
        widgets = {
            'mission':forms.HiddenInput(),
            # 'end_date':forms.DateInput(attrs={'type': 'date'}),
        }


class HelpTextForm(forms.ModelForm):
    class Meta:
        model = models.HelpText
        fields = "__all__"
        widgets = {
            'eng_text': forms.Textarea(attrs={"rows": 2}),
            'fra_text': forms.Textarea(attrs={"rows": 2}),
        }


HelpTextFormSet = modelformset_factory(
    model=models.HelpText,
    form=HelpTextForm,
    extra=1,
)