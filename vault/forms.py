from django import forms
from django.forms import modelformset_factory

from . import models

attr_fp_date_time = {"class": "fp-date-time-with-seconds", "placeholder": "Select Date and Time.."}
chosen_js = {"class": "chosen-select-contains"}
multi_select_js = {"class": "multi-select"}


class SpeciesForm(forms.ModelForm):
    class Meta:
        model = models.Species
        fields = "__all__"


class ObservationPlatformForm(forms.ModelForm):
    class Meta:
        model = models.ObservationPlatform
        fields = "__all__"


ObservationPlatformFormset = modelformset_factory(
    model=models.ObservationPlatform,
    form=ObservationPlatformForm,
    extra=1,
)


# class ObservationPlatformTypeForm(forms.ModelForm):
#     class Meta:
#         model = models.ObservationPlatformType
#         fields = "__all__"
#
#
# ObservationPlatformTypeFormset = modelformset_factory(
#     model=models.ObservationPlatformType,
#     form=ObservationPlatformTypeForm,
#     extra=1,
# )


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
            "region": forms.SelectMultiple(attrs=chosen_js),
            "purpose": forms.SelectMultiple(attrs=chosen_js),
            "start_date": forms.TextInput(attrs=attr_fp_date_time),
            "end_date": forms.TextInput(attrs=attr_fp_date_time),
            # "created_by": forms.HiddenInput(),
            # "verified_by": forms.HiddenInput(),
        }


class PersonForm(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = "__all__"


PersonFormset = modelformset_factory(
    model=models.Person,
    form=PersonForm,
    extra=1,
)


class ObservationForm(forms.ModelForm):
    class Meta:
        model = models.Observation
        fields = "__all__"
        widgets = {
            "datetime": forms.TextInput(attrs=attr_fp_date_time),
            "metadata": forms.SelectMultiple(attrs=chosen_js),
        }


class OrganisationForm(forms.ModelForm):
    class Meta:
        model = models.Organisation
        fields = "__all__"


OrganisationFormset = modelformset_factory(
    model=models.Organisation,
    form=OrganisationForm,
    extra=1,
)


class RoleForm(forms.ModelForm):
    class Meta:
        model = models.Role
        fields = "__all__"


RoleFormset = modelformset_factory(
    model=models.Role,
    form=RoleForm,
    extra=1,
)
