from django import forms
from django.forms import modelformset_factory

from . import models
from shared_models import models as shared_models

attr_fp_date_time = {"class": "fp-date-time-with-seconds", "placeholder": "Select Date and Time.."}


class SpeciesForm(forms.ModelForm):
    class Meta:
        model = models.Species
        fields = "__all__"


class ObservationPlatformForm(forms.ModelForm):
    class Meta:
        model = models.ObservationPlatform
        fields = "__all__"


class ObservationPlatformTypeForm(forms.ModelForm):
    class Meta:
        model = models.ObservationPlatformType
        fields = "__all__"


ObservationPlatformTypeFormset = modelformset_factory(
    model=models.ObservationPlatformType,
    form=ObservationPlatformTypeForm,
    extra=1,
)


class InstrumentForm(forms.ModelForm):
    class Meta:
        model = models.Instrument
        fields = "__all__"


InstrumentFormset = modelformset_factory(
    model=models.Instrument,
    form=InstrumentForm,
    extra=1,
)


class InstrumentTypeForm(forms.ModelForm):
    class Meta:
        model = models.InstrumentType
        fields = "__all__"


InstrumentTypeFormset = modelformset_factory(
    model=models.InstrumentType,
    form=InstrumentTypeForm,
    extra=1,
)


class OutingForm(forms.ModelForm):
    class Meta:
        model = models.Outing
        fields = "__all__"
        widgets = {
            "start_date": forms.TextInput(attrs=attr_fp_date_time)
        }


class PersonForm(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = "__all__"


class ObservationForm(forms.ModelForm):
    class Meta:
        model = models.Observation
        fields = "__all__"


class OrganisationForm(forms.ModelForm):
    class Meta:
        model = models.Organisation
        fields = "__all__"


OrganisationFormset = modelformset_factory(
    model=models.Organisation,
    form=OrganisationForm,
    extra=1,
)
