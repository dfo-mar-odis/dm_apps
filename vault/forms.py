from django import forms
from . import models
from shared_models import models as shared_models

class SpeciesForm(forms.ModelForm):
    class Meta:
        model = models.Species
        fields = "__all__"

class ObservationPlatformForm(forms.ModelForm):
    class Meta:
        model = models.ObservationPlatform
        fields = "__all__"

class InstrumentForm(forms.ModelForm):
    class Meta:
        model = models.Instrument
        fields = "__all__"