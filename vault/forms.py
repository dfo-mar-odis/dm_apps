from django import forms
from . import models
from shared_models import models as shared_models

#
# class CruiseForm(forms.ModelForm):
#     class Meta:
#         model = shared_models.Cruise
#         fields = ["mission_number",
#                   "description",
#                   "chief_scientist",
#                   "samplers",
#                   "start_date",
#                   "end_date",
#                   "notes",
#                   "season",
#                   "vessel", ]
#
#
# class DigestionForm(forms.ModelForm):
#     class Meta:
#         model = models.DigestionLevel
#         fields = "__all__"
#
#
# class SamplerForm(forms.ModelForm):
#     class Meta:
#         model = models.Sampler
#         fields = "__all__"
#
#
class SpeciesForm(forms.ModelForm):
    class Meta:
        model = models.Species
        fields = "__all__"

#
# class PredatorForm(forms.ModelForm):
#     class Meta:
#         model = models.Predator
#         exclude = ["old_seq_num", "date_last_modified", "stratum", "somatic_wt_g"]
#
#         widgets = {
#             "processing_date": forms.DateInput(attrs={"type": "date"}),
#             'last_modified_by': forms.HiddenInput(),
#         }
#
#
# class PreyForm(forms.ModelForm):
#     class Meta:
#         model = models.Prey
#         exclude = ["stomach_wt_g", "censored_length", "old_id", "date_last_modified"]
#         widgets = {
#             'species': forms.HiddenInput(),
#             'predator': forms.HiddenInput(),
#             'last_modified_by': forms.HiddenInput(),
#             'comments': forms.Textarea(attrs={"rows": "3"}),
#         }
#
#
# class SearchForm(forms.Form):
#     field_order = ["cruise", "species"]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         cruise_choices = [(obj.id, str(obj)) for obj in shared_models.Cruise.objects.all()]
#         species_choices = [(obj.id, str(obj)) for obj in models.Species.objects.all()]
#
#         self.fields['cruise'] = forms.ChoiceField(required=False, choices=cruise_choices)
#         self.fields['species'] = forms.ChoiceField(required=False, choices=species_choices)
#
#
# class ReportSearchForm(forms.Form):
#     report_choices = [
#         (1, "Summary of Prey Species"),
#         (2, "Data export (csv)"),
#     ]
#     report_choices.insert(0, (None, "------"))
#
#     report = forms.ChoiceField(required=True, choices=report_choices)
#     year = forms.IntegerField(required=False, label="Year (optional)")
#     cruise = forms.ChoiceField(required=False, label="Cruise (optional)")
#     spp = forms.MultipleChoiceField(required=False, label="Species (optional)")
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         cruise_choices = [(obj.id, "{} ({})".format(obj.mission_name, obj.season)) for obj in shared_models.Cruise.objects.all() if obj.predators.count() > 0]
#         cruise_choices.insert(0, (None, "------"))
#
#         self.fields['cruise'].choices = cruise_choices
#
#         spp_choices = [(obj.id, str(obj)) for obj in models.Species.objects.all() if obj.predators.count() > 0]
#         self.fields['spp'].choices = spp_choices
