from django import forms
from . import models

class ItemsForm(forms.ModelForm):
    class Meta:
        model = models.Items
        fields = "__all__"

