from django import forms
from django.utils.translation import gettext as _
from . import models
from django.contrib.auth.models import User
from shared_models import models as shared_models
from django.utils import timezone
from datetime import date, timedelta, datetime
from django.forms import modelformset_factory


chosen_js = {"class":"chosen-select-contains"}#, 'Select multiple': True}


class NewInstrumentForm(forms.ModelForm):

    class Meta:
        # TYPE_CHOICES = [('CTD', 'CTD'), ('ADCP', 'ADCP')]
        model = models.Instrument
        # instrument_type1 = forms.CharField(widget=forms.TextInput(attrs={"class": "chosen-select"}))

        fields = [
            'instrument_type',
            'serial_number',
            'purchase_date',
            'asset_tag',
            'connector',
            'comm_port',
            # 'date_of_last_service',
            # 'date_of_next_service',
            # 'in_service',
            'is_sensor',
            'project_title',
            'scientist',
            # 'last_modified_by',
        ]
        widgets = {
            # 'last_modified_by': forms.HiddenInput(),
            'purchase_date': forms.DateInput(attrs={"type": "date"}),
            # 'purchase_date' : forms.DateInput(attrs={"type": "datepicker",
            #                                        "value": timezone.now().strftime("%Y-%b-%d")},
            #                                 ),
            # 'instrument_type': forms.Textarea(attrs={"rows": 1},  choices=TYPE_CHOICES),
            # 'instrument_type': forms.Select(choices=TYPE_CHOICES),
            "instrument_type": forms.Select(attrs=chosen_js),
            # 'serial_number': forms.Textarea(attrs={"rows": 1}),
            # 'date_of_last_service': forms.DateInput(attrs={"type": "date",
            #                                                "value": timezone.now().strftime("%Y-%b-%d")}),
            # 'date_of_next_service': forms.DateInput(attrs={"type": "date",
            #                                                "value": (timezone.now() + timedelta(days=365)).strftime("%Y-%b-%d")}),
            # 'end_date': forms.DateInput(attrs={"type": "date"}),
            # 'last_modified_by': forms.HiddenInput(),
            'project_title': forms.Textarea(attrs={"rows": 1}),
            'scientist': forms.Textarea(attrs={"rows": 1}),
            # "description": forms.Textarea(attrs={"rows": 8}),
            # "notes": forms.Textarea(attrs={"rows": 5}),
        }


class InstrumentSubmitForm(forms.ModelForm):
    class Meta:
        model = models.Instrument
        fields = [
            # 'last_modified_by',
            # 'submitted',
        ]
        widgets = {
            # 'last_modified_by': forms.HiddenInput(),
            # 'submitted': forms.HiddenInput(),
        }


class InstrumentForm(forms.ModelForm):
    # purchase_date = forms.DateField(input_formats=["%Y-%b-%d"])
    class Meta:
        model = models.Instrument
        exclude = [
            # 'submitted',
            # 'date_last_modified',
            # 'section_head_approved',
            # 'description_html',
            # 'priorities_html',
            # 'deliverables_html',
            # 'date_of_last_service',
            # 'location',
            'date_of_next_service'

        ]

        widgets = {
            'id': forms.HiddenInput(),
            'purchase_date': forms.DateInput( attrs={"type": "date"}), #,'placeholder':'2015-01-01'}),
        #     # 'instrument_type': forms.Textarea(attrs={"rows": 1},  choices=TYPE_CHOICES),
        #     # 'instrument_type': forms.Select(choices=TYPE_CHOICES),
        #     'serial_number': forms.Textarea(attrs={"rows": 1}),
        #     'date_of_last_service': forms.DateInput( attrs={"type": "date",
        #                                                     'value': timezone.now().strftime("%Y-%b-%d")}),
        #     'date_of_next_service': forms.DateInput(attrs={"type": "date",
        #                                                    'value': (timezone.now()+ timedelta(days=365)).strftime("%Y-%b-%d")}),
        #     # 'end_date': forms.DateInput(attrs={"type": "date"}),
        #     # 'last_modified_by': forms.HiddenInput(),
            'scientist': forms.Textarea(attrs={"rows": 1}),
            'project_title': forms.Textarea(attrs={"rows": 1}),
        #     # "description": forms.Textarea(attrs={"rows": 8}),
        #     # "notes": forms.Textarea(attrs={"rows": 5}),
        }



class MooringForm(forms.ModelForm):
    class Meta:
        model = models.Mooring
        exclude = [
            # 'submitted',
            'date_last_modified',
            'instruments'

        ]

        widgets = {
            # 'instrument': forms.HiddenInput(),
            # 'instruments': forms.HiddenInput(),
            'deploy_time': forms.DateTimeInput(attrs={'placeholder': 'yyyy-mm-dd hh:mm:ss'}),

            # 'deploy_time': forms.DateTimeInput(attrs={"type": "datetime-local"}),#"type": "date"}),
            'recover_time': forms.DateTimeInput(attrs={'placeholder': 'yyyy-mm-dd hh:mm:ss'}),
            'depth': forms.Textarea(attrs={"rows": 1,}),
            # 'orientation': forms.Textarea(attrs={"rows": 1}),
            'lat': forms.Textarea(attrs={"rows": 1}),
            'lon': forms.Textarea(attrs={"rows": 1}),
            'comments': forms.Textarea(attrs={"rows": 1}),

        }


# class AddDeploymentForm(forms.ModelForm):
#     class Meta:
#         model = models.Mooring
#         exclude = [
#             'submitted',
#             'date_last_modified',
#
#         ]
#
#         widgets = {
#             # 'instrument': forms.HiddenInput(),
#             # 'instruments': forms.HiddenInput(),
#             'mooring': forms.HiddenInput(),
#             'mooring_number': forms.HiddenInput(),
#             'deploy_time': forms.DateTimeInput(attrs={"type": "date",
#                                                 'input_formats': ['%Y-%m-%d %H:%M:%S'],
#                                                            'placeholder': (timezone.now()+ timedelta(days=365)).strftime("%Y-%b-%d")}),
#             'recover_time': forms.DateTimeInput(attrs={"type": "date",
#                                                            'value': (timezone.now() + timedelta(days=365)).strftime(
#                                                                "%Y-%b-%d %T")}),
#             'depth': forms.Textarea(attrs={"rows": 1}),
#             'lat': forms.Textarea(attrs={"rows": 1}),
#             'lon': forms.Textarea(attrs={"rows": 1}),
#             'comments': forms.Textarea(attrs={"rows": 2}),
#         #     # "description": forms.Textarea(attrs={"rows": 8}),
#         #     # "notes": forms.Textarea(attrs={"rows": 5}),
#         }

class CustomModelFilter(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.column1, obj.column2)

from django.forms import inlineformset_factory


class AddInstrumentToMooringForm(forms.ModelForm):



    # INSTRUMENTTYPE_CHOICES = ((None, "---"),)
    # for ins_types in models.Instrument.objects.all():
    #     INSTRUMENTTYPE_CHOICES = INSTRUMENTTYPE_CHOICES.__add__(((ins_types.id, ins_types.instrument_type),))


    # organization = forms.ChoiceField(choices=ORGANIZATION_CHOICES, required=False)
    # instrument_type = forms.ChoiceField(choices=INSTRUMENTTYPE_CHOICES, required=False)
    # instrument_type = CustomModelFilter(queryset=models.Instrument.objects.values('instrument_type').distinct())
    class Meta:
        model = models.InstrumentMooring
        exclude = [
            # 'submitted',
            'date_last_modified',

        ]
        # fields = ['instrument_type', 'mooring', 'depth']


        widgets = {
            'mooring': forms.HiddenInput(),
            'depth': forms.Textarea(attrs={"rows": 1}),
            'lat': forms.Textarea(attrs={"rows": 1}),
            'lon': forms.Textarea(attrs={"rows": 1}),
            # 'orientation': forms.Textarea(attrs={"rows": 1}),
            'comments': forms.Textarea(attrs={"rows": 2}),
        #     # "description": forms.Textarea(attrs={"rows": 8}),
        #     # "notes": forms.Textarea(attrs={"rows": 5}),
        }
    # instruments = models.Instrument.objects.all()

    def __init__(self, *args, **kwargs):
        #
        # USER_CHOICES = [(u.id, "{}, {}".format(u.last_name, u.first_name)) for u in
        #                 User.objects.all().order_by("last_name", "first_name")]
        # USER_CHOICES.insert(0, tuple((None, "---")))
        #
        # super().__init__(*args, **kwargs)
        # self.fields['user'].queryset = User.objects.all().order_by("last_name", "first_name")
        # self.fields['user'].choices = USER_CHOICES
        #
        # self.fields['instrument_type'].queryset = models.Instrument.objects.values("instrument_type").distinct()
        super().__init__(*args, **kwargs)
        # print(self.instance)
        # self.fields['instrument'].choices = models.Instrument.objects.distinct().filter('instrument_type')
        # self.fields['instrument_type'].queryset = models.Instrument.objects.distinct().filter('instrument_type')
    #     super().__init__(*args, **kwargs)
    #     for instrument in self.instruments:
    #         self.fields[instrument.instrument_type] = forms.CharField


# from django.contrib.auth.models import User
# from masterlist import models as ml_models
# AddInstrumentToMooringFormSet = modelformset_factory(
#     model=models.InstrumentMooring,
#     form=AddInstrumentToMooringForm,
#     extra=1,
# )


class AddMooringToInstrumentForm(forms.ModelForm):
    class Meta:
        model = models.InstrumentMooring
        exclude = [
            # 'submitted',
            'date_last_modified',

        ]

        widgets = {
            'instrument': forms.HiddenInput(),
            'depth': forms.Textarea(attrs={"rows": 1}),
            'lat': forms.Textarea(attrs={"rows": 1}),
            'lon': forms.Textarea(attrs={"rows": 1}),
            # 'orientation': forms.Textarea(attrs={"rows": 1}),
            'comments': forms.Textarea(attrs={"rows": 2}),
        #     # "description": forms.Textarea(attrs={"rows": 8}),
        #     # "notes": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super(AddMooringToInstrumentForm, self).__init__(*args, **kwargs)
        # selected_choices = whatever
        # self.fields['mooring'].choices = [(k, v) for k, v in models.Mooring.objects.all()
        #                                          if k is not 'HOME']
        self.fields['mooring'].queryset = models.Mooring.objects.all()
        self.fields['mooring'].choices = [(u.id, u) for u in
                        models.Mooring.objects.all() if 'HOME' not in u.mooring ]

class EditInstrumentMooringForm(forms.ModelForm):
    class Meta:
        model = models.InstrumentMooring
        exclude = [
            # 'submitted',
            'date_last_modified',

        ]

        widgets = {
            # 'instrument': forms.HiddenInput(),
            # 'instruments': forms.HiddenInput(),
            # 'deployment': forms.HiddenInput(),
            # 'mooring': forms.HiddenInput(),
            # 'mooring_number': forms.HiddenInput(),
            # 'deploy_time': forms.DateTimeInput(attrs={"type": "date",
            #                                     'input_formats': ['%Y-%m-%d %H:%M:%S'],
            #                                                'placeholder': (timezone.now()+ timedelta(days=365)).strftime("%Y-%b-%d")}),
            # 'recover_time': forms.DateTimeInput(attrs={"type": "date",
            #                                                'value': (timezone.now() + timedelta(days=365)).strftime(
            #                                                    "%Y-%b-%d %T")}),
            'depth': forms.Textarea(attrs={"rows": 1}),
            'lat': forms.Textarea(attrs={"rows": 1}),
            'lon': forms.Textarea(attrs={"rows": 1}),
            'comments': forms.Textarea(attrs={"rows": 2}),
        #     # "description": forms.Textarea(attrs={"rows": 8}),
        #     # "notes": forms.Textarea(attrs={"rows": 5}),
        }


class MooringSubmitForm(forms.ModelForm):
    class Meta:
        model = models.Mooring
        fields = [
            # 'last_modified_by',
            # 'submitted',
        ]
        widgets = {
            # 'last_modified_by': forms.HiddenInput(),
            # 'submitted': forms.HiddenInput(),
        }


class ServiceForm(forms.ModelForm):
    # purchase_date = forms.DateField(input_formats=["%Y-%b-%d"])
    class Meta:
        model = models.ServiceHistory
        exclude = [
            # 'submitted',
            # 'date_last_modified',
            # 'section_head_approved',
            # 'description_html',
            # 'priorities_html',
            # 'deliverables_html',
        ]

        widgets = {
            'instrument': forms.HiddenInput(),
            'service_date': forms.DateInput( attrs={"type": "date"}),#,'placeholder':'2015-01-01'}),
            'next_service_date': forms.DateInput(attrs={"type": "date"}),
        #     # 'instrument_type': forms.Textarea(attrs={"rows": 1},  choices=TYPE_CHOICES),
        #     # 'instrument_type': forms.Select(choices=TYPE_CHOICES),
        #     'serial_number': forms.Textarea(attrs={"rows": 1}),
        #     'date_of_last_service': forms.DateInput( attrs={"type": "date",
        #                                                     'value': timezone.now().strftime("%Y-%b-%d")}),
        #     'date_of_next_service': forms.DateInput(attrs={"type": "date",
        #                                                    'value': (timezone.now()+ timedelta(days=365)).strftime("%Y-%b-%d")}),
        #     # 'end_date': forms.DateInput(attrs={"type": "date"}),
        #     # 'last_modified_by': forms.HiddenInput(),
            'comments': forms.Textarea(attrs={"rows": 1}),
            'project_title': forms.Textarea(attrs={"rows": 1}),
        #     # "description": forms.Textarea(attrs={"rows": 8}),
        #     # "notes": forms.Textarea(attrs={"rows": 5}),
        }