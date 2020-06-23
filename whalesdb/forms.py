from django import forms
from whalesdb import models
from dm_apps import custom_widgets
import datetime


class DepForm(forms.ModelForm):
    min_height = 900
    min_width = 600

    class Meta:
        model = models.DepDeployment
        fields = ["stn", "dep_year", "dep_month", "dep_name", "prj", "mor"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['stn'].create_url = 'whalesdb:create_stn'
        self.fields['prj'].create_url = 'whalesdb:create_prj'
        self.fields['mor'].create_url = 'whalesdb:create_mor'


class EdaForm(forms.ModelForm):

    class Meta:
        model = models.EdaEquipmentAttachment
        exclude = []
        widgets = {
            'dep': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # exclude hydrophones from the equipment selection list
        self.fields['eqp'].queryset = self.fields['eqp'].queryset.exclude(emm__pk=4)


class EmmForm(forms.ModelForm):
    min_height = 700
    min_width = 600

    class Meta:
        model = models.EmmMakeModel
        exclude = []
        widgets = {
        }


class EqhForm(forms.ModelForm):
    class Meta:
        model = models.EqhHydrophoneProperty
        exclude = []
        widgets = {
            'emm': forms.HiddenInput()
        }


class EqoForm(forms.ModelForm):
    class Meta:
        model = models.EqoOwner
        exclude = []
        widgets = {
        }


class EqpForm(forms.ModelForm):
    min_height = 850
    min_width = 600

    class Meta:
        model = models.EqpEquipment
        exclude = []
        widgets = {
            'eqp_date_purchase': forms.DateInput(attrs={"placeholder": "Click to select a date..", "class": "fp-date"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['emm'].create_url = 'whalesdb:create_emm'
        self.fields['eqo_owned_by'].create_url = 'whalesdb:create_eqo'


class EqrForm(forms.ModelForm):
    class Meta:
        model = models.EqrRecorderProperties
        exclude = []
        widgets = {
            'emm': forms.HiddenInput()
        }


class MorForm(forms.ModelForm):

    min_height = 935
    min_width = 600

    class Meta:
        model = models.MorMooringSetup
        exclude = []
        widgets = {
            'mor_additional_equipment': forms.Textarea(attrs={"rows": 2}),
            'mor_general_moor_description': forms.Textarea(attrs={"rows": 2}),
            'mor_notes': forms.Textarea(attrs={"rows": 2}),
        }


class PrjForm(forms.ModelForm):

    class Meta:
        model = models.PrjProject
        fields = ["name", "nom", "description_en", "description_fr", "prj_url"]
        widgets = {
            'description_en': forms.Textarea(attrs={"rows": 2}),
            'description_fr': forms.Textarea(attrs={"rows": 2}),
        }


class RciForm(forms.ModelForm):
    min_height = 1000
    min_width = 600

    class Meta:
        model = models.RciChannelInfo
        exclude = []
        widgets = {
            'rec_id': forms.HiddenInput(),
        }


class RecForm(forms.ModelForm):
    class Meta:
        model = models.RecDataset
        exclude = []
        widgets = {
        }


class ReeForm(forms.ModelForm):
    min_height = 1000
    min_width = 600

    class Meta:
        model = models.ReeRecordingEvent
        exclude = []
        widgets = {
            'rec_id': forms.HiddenInput(),
        }


class RscForm(forms.ModelForm):
    class Meta:
        model = models.RscRecordingSchedule
        exclude = []
        widgets = {
        }


class RstForm(forms.ModelForm):
    class Meta:
        model = models.RstRecordingStage
        exclude = []
        widgets = {
            'rsc': forms.HiddenInput()
        }


class RttForm(forms.ModelForm):
    class Meta:
        model = models.RttTimezoneCode
        exclude = []


class StnForm(forms.ModelForm):
    min_height = 935
    min_width = 600

    class Meta:
        model = models.StnStation
        exclude = []
        widgets = {
            'stn_notes': forms.Textarea(attrs={"rows": 2}),
        }


class SteForm(forms.ModelForm):
    min_height = 935
    min_width = 600

    class Meta:
        model = models.SteStationEvent
        exclude = []
        widgets = {
            'ste_date': forms.DateInput(attrs={"placeholder": "Click to select a date..", "class": "fp-date"}),
            'dep': forms.HiddenInput(),
            'set_type': forms.HiddenInput(),
        }


class TeaForm(forms.ModelForm):
    class Meta:
        model = models.TeaTeamMember
        exclude = []
        widgets = {
        }
