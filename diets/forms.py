from django import forms
from . import models
from shared_models import models as shared_models


class CruiseForm(forms.ModelForm):
    class Meta:
        model = shared_models.Cruise
        fields = ["mission_number",
                  "description",
                  "chief_scientist",
                  "samplers",
                  "start_date",
                  "end_date",
                  "notes",
                  "season",
                  "vessel", ]


class DigestionForm(forms.ModelForm):
    class Meta:
        model = models.DigestionLevel
        fields = "__all__"


class SamplerForm(forms.ModelForm):
    class Meta:
        model = models.Sampler
        fields = "__all__"


class SpeciesForm(forms.ModelForm):
    class Meta:
        model = models.Species
        fields = "__all__"


class PredatorForm(forms.ModelForm):
    class Meta:
        model = models.Predator
        exclude = ["old_seq_num", "date_last_modified", "stratum", "somatic_wt_g"]

        widgets = {
            "processing_date": forms.DateInput(attrs={"type": "date"}),
            'last_modified_by': forms.HiddenInput(),
        }


class PreyForm(forms.ModelForm):
    class Meta:
        model = models.Prey
        exclude = ["stomach_wt_g", "sensor_used", "date_last_modified"]
        widgets = {
            'species': forms.HiddenInput(),
            'predator': forms.HiddenInput(),
            'last_modified_by': forms.HiddenInput(),
            'comments': forms.Textarea(attrs={"rows": "3"}),
        }


class SearchForm(forms.Form):

    field_order = ["cruise", "species"]

<<<<<<< HEAD
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cruise_choices = [(obj.id, str(obj)) for obj in shared_models.Cruise.objects.all()]
        species_choices = [(obj.id, str(obj)) for obj in models.Species.objects.all()]

        self.fields['cruise'] = forms.ChoiceField(required=False, choices=cruise_choices)
        self.fields['species'] = forms.ChoiceField(required=False, choices=species_choices)
=======

class ReportSearchForm(forms.Form):
    YEAR_CHOICES = [(y["season"], y["season"]) for y in shared_models.Cruise.objects.order_by("-season").values('season').distinct()]
    REPORT_CHOICES = [
        (1, "Summary of Prey Species"),
    ]
    REPORT_CHOICES.insert(0, (None, "------"))

    report = forms.ChoiceField(required=True, choices=REPORT_CHOICES)
    year = forms.ChoiceField(required=True, choices=YEAR_CHOICES)
>>>>>>> 4d6a75843c97a9612bf2913ec8bf7c3a20183d38
