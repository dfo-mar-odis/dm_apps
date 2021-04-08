from django import forms
from django.forms import modelformset_factory
from django.utils.translation import gettext_lazy

from . import models

attr_fp_date_time = {"class": "fp-date-time-with-seconds", "placeholder": "Select Date and Time.."}
chosen_js = {"class": "chosen-select-contains"}
YES_NO_CHOICES = (
    (True, "Yes"),
    (False, "No"),
)


class TagForm(forms.ModelForm):
    class Meta:
        model = models.Tag
        fields = "__all__"


TagFormset = modelformset_factory(
    model=models.Tag,
    form=TagForm,
    extra=1,
)


class FiltrationTypeForm(forms.ModelForm):
    class Meta:
        model = models.FiltrationType
        fields = "__all__"


FiltrationTypeFormset = modelformset_factory(
    model=models.FiltrationType,
    form=FiltrationTypeForm,
    extra=1,
)


class DNAExtractionProtocolForm(forms.ModelForm):
    class Meta:
        model = models.DNAExtractionProtocol
        fields = "__all__"


DNAExtractionProtocolFormset = modelformset_factory(
    model=models.DNAExtractionProtocol,
    form=DNAExtractionProtocolForm,
    extra=1,
)


class SpeciesForm(forms.ModelForm):
    class Meta:
        model = models.Species
        fields = "__all__"


class CollectionForm(forms.ModelForm):
    class Meta:
        model = models.Collection
        fields = "__all__"
        widgets = {
            "contact_users": forms.SelectMultiple(attrs=chosen_js),
            "tags": forms.SelectMultiple(attrs=chosen_js),
        }


class FileForm(forms.ModelForm):
    class Meta:
        model = models.File
        fields = "__all__"


class FiltrationBatchForm(forms.ModelForm):
    class Meta:
        model = models.FiltrationBatch
        fields = "__all__"
        widgets = {
            "datetime": forms.DateInput(attrs=dict(type="date")),
            "operators": forms.SelectMultiple(attrs=chosen_js),
        }

class ExtractionBatchForm(forms.ModelForm):
    class Meta:
        model = models.ExtractionBatch
        fields = "__all__"
        widgets = {
            "datetime": forms.DateInput(attrs=dict(type="date")),
            "operators": forms.SelectMultiple(attrs=chosen_js),
        }


class PCRBatchForm(forms.ModelForm):
    class Meta:
        model = models.PCRBatch
        fields = "__all__"
        widgets = {
            "datetime": forms.DateInput(attrs=dict(type="date")),
            "operators": forms.SelectMultiple(attrs=chosen_js),
        }

class SampleForm(forms.ModelForm):
    add_another = forms.BooleanField(required=False)

    class Meta:
        model = models.Sample
        fields = "__all__"
        widgets = {
            "datetime": forms.DateTimeInput(attrs=dict(type="datetime"))
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get("instance"):
            del self.fields["add_another"]
        # elif kwargs.get("initial"):
        #     self.fields["transect"].queryset = models.Collection.objects.get(pk=kwargs.get("initial").get("sample")).site.transects.all()
        #
        # self.fields["start_descent"].label += " (yyyy-mm-dd HH:MM:SS)"


#
#
# class SectionForm(forms.ModelForm):
#     class Meta:
#         model = models.Section
#         fields = "__all__"
#         exclude = ["dive"]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         klass = "form-control form-control-sm"
#
#         self.fields["interval"].widget.attrs = {"v-model": "sectionToEdit.interval", "ref": "top_of_form", "@change": "unsavedSectionWork=true",
#                                                 ":disabled": "sectionToEdit.id", "class": klass}
#         self.fields["depth_ft"].widget.attrs = {"v-model": "sectionToEdit.depth_ft", "min": 0, "@change": "unsavedSectionWork=true", "step": "0.01",
#                                                 "class": klass}
#         self.fields["percent_sand"].widget.attrs = {"v-model": "sectionToEdit.percent_sand", "max": 1, "min": 0, "@change": "unsavedSectionWork=true",
#                                                     "step": "0.01", "class": klass}
#         self.fields["percent_mud"].widget.attrs = {"v-model": "sectionToEdit.percent_mud", "max": 1, "min": 0, "@change": "unsavedSectionWork=true",
#                                                    "step": "0.01", "class": klass}
#         self.fields["percent_hard"].widget.attrs = {"v-model": "sectionToEdit.percent_hard", "max": 1, "min": 0, "@change": "unsavedSectionWork=true",
#                                                     "step": "0.01", "class": klass}
#         self.fields["percent_algae"].widget.attrs = {"v-model": "sectionToEdit.percent_algae", "max": 1, "min": 0, "@change": "unsavedSectionWork=true",
#                                                      "step": "0.01", "class": klass}
#         self.fields["percent_gravel"].widget.attrs = {"v-model": "sectionToEdit.percent_gravel", "max": 1, "min": 0, "@change": "unsavedSectionWork=true",
#                                                       "step": "0.01", "class": klass}
#         self.fields["percent_cobble"].widget.attrs = {"v-model": "sectionToEdit.percent_cobble", "max": 1, "min": 0, "@change": "unsavedSectionWork=true",
#                                                       "step": "0.01", "class": klass}
#         self.fields["percent_pebble"].widget.attrs = {"v-model": "sectionToEdit.percent_pebble", "max": 1, "min": 0, "@change": "unsavedSectionWork=true",
#                                                       "step": "0.01", "class": klass}
#         self.fields["comment"].widget.attrs = {"v-model": "sectionToEdit.comment", "@change": "unsavedSectionWork=true", "row": 3, "class": klass}
#
#
# class ObservationForm(forms.ModelForm):
#     class Meta:
#         model = models.Observation
#         fields = "__all__"
#         exclude = ["section"]
#         widgets = {
#             "comment": forms.TextInput(),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         klass = "form-control form-control-sm"
#         self.fields["sex"].widget.attrs = {"v-model": "obs.sex", "@change": "updateObservation(obs)", "class": klass}
#         self.fields["egg_status"].widget.attrs = {"v-model": "obs.egg_status", "@change": "updateObservation(obs)", "class": klass, ":disabled":"obs.sex!='f'"}
#         self.fields["carapace_length_mm"].widget.attrs = {"v-model": "obs.carapace_length_mm", "@change": "updateObservation(obs)", "class": klass}
#         self.fields["certainty_rating"].widget.attrs = {"v-model": "obs.certainty_rating", "@change": "updateObservation(obs)", "class": klass}
#         self.fields["comment"].widget.attrs = {"v-model": "obs.comment", "@change": "updateObservation(obs)", "class": klass}
#
#
# class NewObservationForm(forms.ModelForm):
#     class Meta:
#         model = models.Observation
#         fields = "__all__"
#         exclude = ["section"]
#         widgets = {
#             # "comment": forms.TextInput(),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         klass = "form-control form-control-sm"
#         self.fields["sex"].widget.attrs = {"v-model": "new_observation.sex", "ref": "top_of_form1", "class": klass, "@change":"updateEggStatus(new_observation)"}
#         self.fields["egg_status"].widget.attrs = {"v-model": "new_observation.egg_status", "class": klass}
#         self.fields["carapace_length_mm"].widget.attrs = {"v-model": "new_observation.carapace_length_mm", "class": klass, "@change":"updateLengthCertainty(new_observation)"}
#         self.fields["certainty_rating"].widget.attrs = {"v-model": "new_observation.certainty_rating", "class": klass}
#         self.fields["comment"].widget.attrs = {"v-model": "new_observation.comment", "row": 3, "class": klass}
#
#
class ReportSearchForm(forms.Form):
    REPORT_CHOICES = (
        (None, "------"),
        (1, "------"),
    )
    report = forms.ChoiceField(required=True, choices=REPORT_CHOICES)
    year = forms.IntegerField(required=False, label=gettext_lazy('Year'), widget=forms.NumberInput(attrs={"placeholder": "Leave blank for all years"}))



class FileImportForm(forms.Form):
    temp_file = forms.FileField(label="File to import")