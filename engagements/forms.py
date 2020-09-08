from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Organization, Individual, EngagementPlan, Interaction

bs_form_attrs = {'class': 'form-control'}


# Organization - New
class OrganizationCreateForm(forms.ModelForm):
    error_css_class = 'is-invalid'

    class Meta:
        model = Organization
        exclude = ['slug', 'created_by', 'last_modified_by']
        help_texts = {
            'legal_name': "Enter the organization's legal name (127 characters maximum).",
            'phone_number': "Enter in '+12345678900' format",
            'fax_number': "Enter in '+12345678900' format",
        }
        widgets = {
            'legal_name': forms.TextInput(attrs=bs_form_attrs),
            'phone_number': forms.TextInput(attrs=bs_form_attrs),
            'fax_number': forms.TextInput(attrs=bs_form_attrs),
            'email': forms.EmailInput(attrs=bs_form_attrs),
            'webpage': forms.URLInput(attrs=bs_form_attrs),
            'business_number': forms.TextInput(attrs=bs_form_attrs),
            'address_line_1': forms.TextInput(attrs=bs_form_attrs),
            'address_line_2': forms.TextInput(attrs=bs_form_attrs),
            'city': forms.TextInput(attrs=bs_form_attrs),
            'province': forms.Select(attrs=bs_form_attrs),
            'zip_postal': forms.TextInput(attrs=bs_form_attrs),
            'country': forms.TextInput(attrs=bs_form_attrs),
            'organization_type': forms.Select(attrs={'class': 'form-control', 'onchange': 'Hide()'}),
            'other_organization_type': forms.TextInput(attrs=bs_form_attrs),
            'profit_nonprofit': forms.Select(attrs=bs_form_attrs),
            'stakeholder_type': forms.Select(attrs=bs_form_attrs),
            'parent_organizations': forms.SelectMultiple(attrs=bs_form_attrs),
        }


# Organization - Update
class OrganizationForm(forms.ModelForm):
    error_css_class = 'is-invalid'

    class Meta:
        model = Organization
        exclude = ['slug', 'created_by', 'last_modified_by']
        help_texts = {
            'legal_name': "Enter the organization's legal name (127 characters maximum).",
            'phone_number': "Enter in '+12345678900' format",
            'fax_number': "Enter in '+12345678900' format",
        }
        widgets = {
            'legal_name': forms.TextInput(attrs=bs_form_attrs),
            'phone_number': forms.TextInput(attrs=bs_form_attrs),
            'fax_number': forms.TextInput(attrs=bs_form_attrs),
            'email': forms.EmailInput(attrs=bs_form_attrs),
            'webpage': forms.URLInput(attrs=bs_form_attrs),
            'business_number': forms.TextInput(attrs=bs_form_attrs),
            'address_line_1': forms.TextInput(attrs=bs_form_attrs),
            'address_line_2': forms.TextInput(attrs=bs_form_attrs),
            'city': forms.TextInput(attrs=bs_form_attrs),
            'province': forms.Select(attrs=bs_form_attrs),
            'zip_postal': forms.TextInput(attrs=bs_form_attrs),
            'country': forms.TextInput(attrs=bs_form_attrs),
            'organization_type': forms.Select(attrs={'class': 'form-control', 'onchange': 'Hide()'}),
            'other_organization_type': forms.TextInput(attrs=bs_form_attrs),
            'profit_nonprofit': forms.Select(attrs=bs_form_attrs),
            'stakeholder_type': forms.Select(attrs=bs_form_attrs),
            'parent_organizations': forms.SelectMultiple(attrs=bs_form_attrs),
        }


# Individual - Create
class IndividualCreateForm(forms.ModelForm):
    error_css_class = 'is-invalid'

    class Meta:
        model = Individual
        exclude = ['slug', 'created_by', 'last_modified_by']
        widgets = {
            'first_name': forms.TextInput(attrs=bs_form_attrs),
            'last_name': forms.TextInput(attrs=bs_form_attrs),
            'title': forms.TextInput(attrs=bs_form_attrs),
            'organization': forms.SelectMultiple(attrs=bs_form_attrs),
            'email_address': forms.EmailInput(attrs=bs_form_attrs),
            'phone_number': forms.TextInput(attrs=bs_form_attrs),
            'fax_number': forms.TextInput(attrs=bs_form_attrs),
            'address_line_1': forms.TextInput(attrs=bs_form_attrs),
            'address_line_2': forms.TextInput(attrs=bs_form_attrs),
            'city': forms.TextInput(attrs=bs_form_attrs),
            'province': forms.Select(attrs=bs_form_attrs),
            'zip_postal': forms.TextInput(attrs=bs_form_attrs),
            'country': forms.TextInput(attrs=bs_form_attrs),
            'linkedin_profile': forms.URLInput(attrs=bs_form_attrs)
        }


# Individual - Update
class IndividualForm(forms.ModelForm):
    error_css_class = 'is-invalid'

    class Meta:
        model = Individual
        exclude = ['slug', 'created_by', 'last_modified_by']
        widgets = {
            'first_name': forms.TextInput(attrs=bs_form_attrs),
            'last_name': forms.TextInput(attrs=bs_form_attrs),
            'title': forms.TextInput(attrs=bs_form_attrs),
            'organization': forms.SelectMultiple(attrs=bs_form_attrs),
            'email_address': forms.EmailInput(attrs=bs_form_attrs),
            'phone_number': forms.TextInput(attrs=bs_form_attrs),
            'fax_number': forms.TextInput(attrs=bs_form_attrs),
            'address_line_1': forms.TextInput(attrs=bs_form_attrs),
            'address_line_2': forms.TextInput(attrs=bs_form_attrs),
            'city': forms.TextInput(attrs=bs_form_attrs),
            'province': forms.Select(attrs=bs_form_attrs),
            'zip_postal': forms.TextInput(attrs=bs_form_attrs),
            'country': forms.TextInput(attrs=bs_form_attrs),
            'linkedin_profile': forms.URLInput(attrs=bs_form_attrs)
        }


class PlanForm(forms.ModelForm):
    error_css_class = 'is-invalid'

    class Meta:
        model = EngagementPlan
        exclude = ['slug', 'created_by', 'last_modified_by']
        widgets = {
            'title': forms.TextInput(attrs=bs_form_attrs),
            'lead': forms.Select(attrs=bs_form_attrs),
            'region': forms.Select(attrs=bs_form_attrs),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs=bs_form_attrs),
            'end_date': forms.DateInput(attrs=bs_form_attrs),
            'stakeholders': forms.SelectMultiple(attrs=bs_form_attrs),
            'staff_collaborators': forms.SelectMultiple(attrs=bs_form_attrs),
            'status': forms.Select(attrs=bs_form_attrs)
        }
        
        
class InteractionForm(forms.ModelForm):
    error_css_class = 'is-invalid'

    class Meta:
        model = Interaction
        exclude = ['slug', 'created_by', 'last_modified_by']
        widgets = {
            'activity_type': forms.Select(attrs=bs_form_attrs),
            'title': forms.TextInput(attrs=bs_form_attrs),
            'file_reference': forms.TextInput(attrs=bs_form_attrs),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateInput(attrs=bs_form_attrs),
            'engagement_plan': forms.Select(attrs=bs_form_attrs),
            'initiator': forms.Select(attrs=bs_form_attrs),
            'primary_contact': forms.Select(attrs=bs_form_attrs),
            'staff_lead': forms.Select(attrs=bs_form_attrs),
            'attendees': forms.SelectMultiple(attrs=bs_form_attrs),
            'organization_attendees': forms.SelectMultiple(attrs=bs_form_attrs),
            'staff_attendees': forms.SelectMultiple(attrs=bs_form_attrs),
            'location': forms.TextInput(attrs=bs_form_attrs),
            'status': forms.Select(attrs=bs_form_attrs),
            'priority': forms.Select(attrs=bs_form_attrs),
            'subjects': forms.CheckboxSelectMultiple(attrs={'class': 'list-unstyled'}),
            'objectives': forms.CheckboxSelectMultiple(attrs={'class': 'list-unstyled'}),
            'geographic_level': forms.Select(attrs=bs_form_attrs)
        }


### Mozilla Example
# import datetime
# from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _
#
# class RenewBookForm(forms.Form):
#     renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
#
#     # Define clean_XXXXXX
#     def clean_renewal_date(self):
#         # Get pre-cleaned data to perform our own validation (removed unsafe chars, etc.)
#         data = self.cleaned_data['renewal_date']
#
#         # Check if a date is not in the past.
#         if data < datetime.date.today():
#             raise ValidationError(_('Invalid date - renewal in past'))
#
#         # Check if a date is in the allowed range (+4 weeks from today).
#         if data > datetime.date.today() + datetime.timedelta(weeks=4):
#             raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
#
#         # Remember to always return the cleaned data.
#         return data
