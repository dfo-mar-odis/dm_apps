from django import forms
from django.forms import modelformset_factory

from . import models

chosen_js = {"class": "chosen-select-contains"}
multi_select_js = {"class": "multi-select"}
attr_fp_date = {"class": "fp-date", "placeholder": "Click to select a date.."}


class ItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = "__all__"
        widgets = {
            'container': forms.CheckboxInput(),
            'suppliers': forms.SelectMultiple(attrs=chosen_js),
            # 'suppliers': forms.SelectMultiple(attrs=multi_select_js),
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = "__all__"
        widgets = {
            'tag': forms.SelectMultiple(attrs=chosen_js),
            'created_by': forms.HiddenInput(),

        }


class TransactionForm1(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = "__all__"
        widgets = {
            'item': forms.HiddenInput(),
            'tag': forms.SelectMultiple(attrs=chosen_js),
            'created_by': forms.HiddenInput(),
        }


class TransactionForm2(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = "__all__"
        widgets = {
            'item': forms.HiddenInput(),
            'category': forms.HiddenInput(),
            'tag': forms.SelectMultiple(attrs=chosen_js),
            'created_by': forms.HiddenInput(),

        }


class TransactionForm3(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = "__all__"
        widgets = {
            'item': forms.HiddenInput(),
            'category': forms.HiddenInput(),
            'location': forms.HiddenInput(),
            'tag': forms.SelectMultiple(attrs=chosen_js),
            'created_by': forms.HiddenInput(),

        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = "__all__"
        widgets = {
            'date_ordered': forms.DateInput(
                attrs={"class": "not-a-group-field fp-date", "placeholder": "Click to select a date.."}),
            'date_received': forms.DateInput(
                attrs={"class": "not-a-group-field fp-date", "placeholder": "Click to select a date.."}),
            'transaction': forms.HiddenInput(),

        }


class OrderForm1(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = "__all__"
        widgets = {
            'item': forms.HiddenInput(),
            'date_ordered': forms.DateInput(
                attrs={"class": "not-a-group-field fp-date", "placeholder": "Click to select a date.."}),
            'date_received': forms.HiddenInput(),
            'transaction': forms.HiddenInput(),
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = models.Location
        fields = "__all__"


LocationFormset = modelformset_factory(
    model=models.Location,
    form=LocationForm,
    extra=1,
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


class OwnerForm(forms.ModelForm):
    class Meta:
        model = models.Owner
        fields = "__all__"


OwnerFormset = modelformset_factory(
    model=models.Owner,
    form=OwnerForm,
    extra=1,
)


class SizeForm(forms.ModelForm):
    class Meta:
        model = models.Size
        fields = "__all__"


SizeFormset = modelformset_factory(
    model=models.Size,
    form=SizeForm,
    extra=1,
)


class OrganisationForm(forms.ModelForm):
    class Meta:
        model = models.Organisation
        fields = "__all__"


OrganisationFormset = modelformset_factory(
    model=models.Organisation,
    form=OrganisationForm,
    extra=1,
)


class TrainingForm(forms.ModelForm):
    class Meta:
        model = models.Training
        fields = "__all__"


TrainingFormset = modelformset_factory(
    model=models.Training,
    form=TrainingForm,
    extra=1,
)


class SpeciesForm(forms.ModelForm):
    class Meta:
        model = models.Species
        fields = "__all__"


SpeciesFormset = modelformset_factory(
    model=models.Species,
    form=SpeciesForm,
    extra=1,
)


class PersonnelForm(forms.ModelForm):
    class Meta:
        model = models.Personnel
        fields = "__all__"


class SupplierForm(forms.ModelForm):
    class Meta:
        model = models.Supplier
        fields = "__all__"


class SupplierForm1(forms.ModelForm):
    class Meta:
        model = models.Supplier
        fields = "__all__"
        widgets = {
            'item': forms.HiddenInput(),
        }


class FileForm(forms.ModelForm):
    class Meta:
        model = models.File
        fields = "__all__"
        widgets = {
            'item': forms.HiddenInput(),
        }


class IncidentForm(forms.ModelForm):
    class Meta:
        model = models.Incident
        fields = "__all__"
        widgets = {
            'submitted': forms.CheckboxInput,
            'first_report': forms.DateInput(
                attrs={"class": "not-a-group-field fp-date", "placeholder": "Click to select a date.."}),
            'gear_presence': forms.CheckboxInput,
            'exam': forms.CheckboxInput,
            'necropsy': forms.CheckboxInput,
            'photos': forms.CheckboxInput,
            'date_email_sent': forms.HiddenInput(),
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = models.Image
        fields = "__all__"
        widgets = {
            'incident': forms.HiddenInput(),
        }


class ReportGeneratorForm(forms.Form):
    report = forms.ChoiceField(required=True)
    location = forms.ChoiceField(required=False, label="Location/Container Name", widget=forms.Select(attrs=chosen_js))
    item_name = forms.ChoiceField(required=False, label="Item Name", widget=forms.Select(attrs=chosen_js))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        report_choices = [
            (1, "Container Summary"),
            (2, "Sized Item Summary"),

        ]
        report_choices.insert(0, (None, "------"))

        location_choices = [(obj.id, "{}".format(obj.location)) for obj in
                            models.Location.objects.filter(container=True)]
        location_choices.insert(0, (None, "------"))

        item_list = set([item.item_name.lower() for item in models.Item.objects.filter(size__isnull=False)])
        item_name_choices = [(n, n.title()) for n in item_list]
        item_name_choices.insert(0, (None, "------"))

        self.fields['report'].choices = report_choices
        self.fields['location'].choices = location_choices
        self.fields['item_name'].choices = item_name_choices
