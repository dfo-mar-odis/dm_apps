from django import forms
from django.forms import modelformset_factory
from django.utils import timezone
from django.utils.translation import gettext as _
from django.contrib.auth.models import User as AuthUser
from shared_models import models as shared_models

from . import models

chosen_js = {"class": "chosen-select-contains"}
attr_fp_date = {"class": "fp-date", "placeholder": "Click to select a date.."}
attr_fp_date_hide_me = {"class": "fp-date hide-me", "placeholder": "Click to select a date.."}
attr_hide_me = {"class": "hide-me"}
attr_hide_me_user_info = {"class": "hide-me user-info"}
attr_user_info = {"class": "user-info"}
attr_cost_hide_me = {"class": "hide-me cost"}
attr_cost = {"class": "cost"}
attr_row3_hide_me = {"class": "hide-me", "rows": 3}
attr_row3 = {"rows": 3}
attr_row4 = {"rows": 4}

YES_NO_CHOICES = (
    (True, _("Yes")),
    (False, _("No")),
)


class ReviewerApprovalForm(forms.ModelForm):
    approved = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    changes_requested = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    stay_on_page = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = models.Reviewer
        fields = [
            "comments",
        ]
        labels = {
            "comments": _("Please provide your comments here...")
        }
        widgets = {
            "comments": forms.Textarea(attrs=attr_row3)
        }


class ReviewerSkipForm(forms.ModelForm):
    class Meta:
        model = models.Reviewer
        fields = [
            "comments",
        ]
        labels = {
            "comments": _("If so, please provide the rationale here...")
        }
        widgets = {
            "comments": forms.Textarea(attrs=attr_row3)
        }


class TripRequestApprovalForm(forms.Form):
    approved = forms.BooleanField(widget=forms.HiddenInput(), required=False)


class TripRequestForm(forms.ModelForm):
    stay_on_page = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = models.TripRequest
        exclude = [
            "total_cost",
            "fiscal_year",
            "submitted",
            "status",
            "breakfasts",
            "lunches",
            "suppers",
            "incidentals",
            "meals",
        ]
        labels = {
            'bta_attendees': _("Other attendees covered under BTA (i.e., they will not need to have a travel plan)"),
            'adm': _("ADM (only if necessary, e.g., events, int'l travel, etc. )"),
        }
        widgets = {
            'bta_attendees': forms.SelectMultiple(attrs=chosen_js),
            'trip': forms.Select(attrs=chosen_js),
            'user': forms.Select(attrs=chosen_js),
            'section': forms.Select(attrs=chosen_js),
            'is_group_request': forms.Select(choices=YES_NO_CHOICES),
            'objective_of_event': forms.Textarea(attrs=attr_row3),
            'benefit_to_dfo': forms.Textarea(attrs=attr_row3),
            'multiple_attendee_rationale': forms.Textarea(attrs=attr_row3),
            'late_justification': forms.Textarea(attrs=attr_row3),
            'funding_source': forms.Textarea(attrs=attr_row3),
            'notes': forms.Textarea(attrs=attr_row3),

            # hidden fields
            'parent_request': forms.HiddenInput(),

            # non-group trip request fields
            'start_date': forms.DateInput(attrs=attr_fp_date_hide_me),
            'end_date': forms.DateInput(attrs=attr_fp_date_hide_me),
            'first_name': forms.TextInput(attrs=attr_hide_me_user_info),
            'last_name': forms.TextInput(attrs=attr_hide_me_user_info),
            'email': forms.EmailInput(attrs=attr_hide_me_user_info),
            'address': forms.TextInput(attrs=attr_hide_me),
            'phone': forms.TextInput(attrs=attr_hide_me),
            'is_public_servant': forms.Select(attrs=attr_hide_me, choices=YES_NO_CHOICES),
            'is_research_scientist': forms.Select(attrs=attr_hide_me, choices=YES_NO_CHOICES),
            'company_name': forms.TextInput(attrs=attr_hide_me),
            'departure_location': forms.TextInput(attrs=attr_hide_me),
            'role': forms.Select(attrs=attr_hide_me),
            'region': forms.Select(attrs=attr_hide_me),
            'role_of_participant': forms.Textarea(attrs=attr_row3_hide_me),
            'multiple_conferences_rationale': forms.Textarea(attrs=attr_row3_hide_me),
            'air': forms.NumberInput(attrs=attr_cost_hide_me),
            'rail': forms.NumberInput(attrs=attr_cost_hide_me),
            'rental_motor_vehicle': forms.NumberInput(attrs=attr_cost_hide_me),
            'personal_motor_vehicle': forms.NumberInput(attrs=attr_cost_hide_me),
            'taxi': forms.NumberInput(attrs=attr_cost_hide_me),
            'other_transport': forms.NumberInput(attrs=attr_cost_hide_me),
            'accommodations': forms.NumberInput(attrs=attr_cost_hide_me),
            'breakfasts': forms.NumberInput(attrs=attr_cost_hide_me),
            'breakfasts_rate': forms.NumberInput(attrs=attr_cost_hide_me),
            'no_breakfasts': forms.NumberInput(attrs=attr_cost_hide_me),
            'lunches': forms.NumberInput(attrs=attr_cost_hide_me),
            'lunches_rate': forms.NumberInput(attrs=attr_cost_hide_me),
            'no_lunches': forms.NumberInput(attrs=attr_cost_hide_me),
            'suppers': forms.NumberInput(attrs=attr_cost_hide_me),
            'suppers_rate': forms.NumberInput(attrs=attr_cost_hide_me),
            'no_suppers': forms.NumberInput(attrs=attr_cost_hide_me),
            'incidentals': forms.NumberInput(attrs=attr_cost_hide_me),
            'incidentals_rate': forms.NumberInput(attrs=attr_cost_hide_me),
            'no_incidentals': forms.NumberInput(attrs=attr_cost_hide_me),
            'registration': forms.NumberInput(attrs=attr_cost_hide_me),
            'other': forms.NumberInput(attrs=attr_cost_hide_me),
        }

    def __init__(self, *args, **kwargs):
        user_choices = [(u.id, "{}, {}".format(u.last_name, u.first_name)) for u in
                        AuthUser.objects.all().order_by("last_name", "first_name")]
        user_choices.insert(0, tuple((None, "---")))

        section_heads = [section.head for section in shared_models.Section.objects.filter(head__isnull=False)]
        division_heads = [division.head for division in shared_models.Division.objects.filter(head__isnull=False)]
        branch_heads = [branch.head for branch in shared_models.Branch.objects.filter(head__isnull=False)]
        region_heads = [region.head for region in shared_models.Region.objects.filter(head__isnull=False)]

        heads = []
        heads.extend(section_heads)
        heads.extend(division_heads)
        heads.extend(branch_heads)
        heads.extend(region_heads)
        # manually add Arran McPherson
        heads.append(AuthUser.objects.get(email__iexact="Arran.McPherson@dfo-mpo.gc.ca"))
        heads = set(heads)

        recommender_chocies = [(u.id, "{}, {}".format(u.last_name, u.first_name)) for u in
                               AuthUser.objects.all().order_by("last_name", "first_name") if u in heads]
        recommender_chocies.insert(0, tuple((None, "---")))

        section_choices = [(s.id, s.full_name) for s in
                           shared_models.Section.objects.filter(division__branch_id__in=[1, 3, ]).order_by("division__branch__region",
                                                                                                           "division__branch",
                                                                                                           "division", "name")]
        section_choices.insert(0, tuple((None, "---")))

        trip_choices = [(t.id, str(t)) for t in models.Conference.objects.filter(start_date__gte=timezone.now())]
        trip_choices.insert(0, tuple((None, "---")))

        super().__init__(*args, **kwargs)
        self.fields['trip'].choices = trip_choices
        self.fields['user'].choices = user_choices
        self.fields['bta_attendees'].choices = user_choices
        self.fields['section'].choices = section_choices


class AdminTripRequestForm(forms.ModelForm):
    class Meta:
        model = models.TripRequest
        fields = [
            # "adm_approval_status",
            # "rdg_approval_status",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        my_object = kwargs.get("instance")
        status_choices = [(s.id, s) for s in models.Status.objects.all() if s.id in [1, 2, 3]]
        status_choices.insert(0, tuple((None, "---")))
        self.fields.get("rdg_approval_status").choices = status_choices
        if not my_object.adm:
            del self.fields["adm_approval_status"]
        else:
            self.fields.get("adm_approval_status").choices = status_choices


class TripRequestAdminNotesForm(forms.ModelForm):
    class Meta:
        model = models.TripRequest
        fields = [
            "admin_notes",
        ]


class ChildTripRequestForm(forms.ModelForm):
    stay_on_page = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = models.TripRequest
        fields = [
            'user',
            'first_name',
            'last_name',
            'address',
            'phone',
            'email',
            'is_public_servant',
            'is_research_scientist',
            'company_name',
            'region',
            'start_date',
            'end_date',
            'departure_location',
            'role',
            'role_of_participant',

            'parent_request',
        ]
        widgets = {
            'user': forms.Select(attrs=chosen_js),
            'parent_request': forms.HiddenInput(),
            'start_date': forms.DateInput(attrs=attr_fp_date),
            'end_date': forms.DateInput(attrs=attr_fp_date),
            'role_of_participant': forms.Textarea(attrs=attr_row4),

            'first_name': forms.TextInput(attrs=attr_user_info),
            'last_name': forms.TextInput(attrs=attr_user_info),
            'email': forms.EmailInput(attrs=attr_user_info),
        }

    def __init__(self, *args, **kwargs):
        try:
            parent_request = kwargs.get("initial").get("parent_request")
        except AttributeError:
            parent_request = None

        if not parent_request:
            parent_request = kwargs.get("instance").parent_request

        user_choices = [(u.id, "{}, {}".format(u.last_name, u.first_name)) for u in
                        AuthUser.objects.all().order_by("last_name", "first_name")]
        user_choices.insert(0, tuple((None, "---")))
        super().__init__(*args, **kwargs)
        self.fields['user'].choices = user_choices

        # if parent_request.reason_id != 2:
        #     del self.fields['role']
        #     del self.fields['role_of_participant']


class TripForm(forms.ModelForm):
    class Meta:
        model = models.Conference
        exclude = ["fiscal_year", "is_verified", "verified_by", "cost_warning_sent" ]
        widgets = {
            'start_date': forms.DateInput(attrs=attr_fp_date),
            'end_date': forms.DateInput(attrs=attr_fp_date),
            'registration_deadline': forms.DateInput(attrs=attr_fp_date),
            'abstract_deadline': forms.DateInput(attrs=attr_fp_date),
        }


class ReportSearchForm(forms.Form):
    REPORT_CHOICES = (
        (None, "------"),
        (1, "CFTS export (xlsx)"),
        # (2, "Print Travel Plan PDF"),
    )
    report = forms.ChoiceField(required=True, choices=REPORT_CHOICES)
    # report #1
    fiscal_year = forms.ChoiceField(required=False, label=_('Fiscal year'))
    # report #2
    user = forms.ChoiceField(required=False, label=_('DFO traveller (leave blank for all)'))

    def __init__(self, *args, **kwargs):
        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all().order_by("id") if fy.trip_requests.count() > 0]
        # TRAVELLER_CHOICES = [(e['email'], "{}, {}".format(e['last_name'], e['first_name'])) for e in
        #                      models.Trip.objects.values("email", "first_name", "last_name").order_by("last_name", "first_name").distinct()]
        user_choices = [(u.id, "{}, {}".format(u.last_name, u.first_name)) for u in
                        AuthUser.objects.all().order_by("last_name", "first_name") if u.user_trip_requests.count() > 0]
        user_choices.insert(0, tuple((None, "---")))

        super().__init__(*args, **kwargs)
        self.fields['fiscal_year'].choices = fy_choices
        self.fields['user'].choices = user_choices


class StatusForm(forms.ModelForm):
    class Meta:
        model = models.Status
        fields = "__all__"


StatusFormSet = modelformset_factory(
    model=models.Status,
    form=StatusForm,
    extra=1,
)


class ReviewerForm(forms.ModelForm):
    class Meta:
        model = models.Reviewer
        fields = [
            'trip_request',
            'order',
            'user',
            'role',
        ]
        widgets = {
            'trip_request': forms.HiddenInput(),
            'user': forms.Select(attrs=chosen_js),
        }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     my_trip = cleaned_data.get("trip")
    #     my_order = cleaned_data.get("order")
    #     my_role = cleaned_data.get("role")
    #
    #     # make sure the role is properly positioned
    #     # last_reviewer = None
    #     # for reviewer in my_trip.reviewers.all():
    #     #     # basically, each subsequent reviewer should have a role that is further down in order than the previous
    #     #     if last_reviewer:
    #     #         if reviewer.role.order > last_reviewer.role.order:
    #     #             raise forms.ValidationError("The roles of the reviewers are out of order!")
    #     #     last_reviewer = reviewer
    #
    #
    #     # we have to do something smart with the order...
    #     # if there is nothing competing, our job is done. Otherwise...
    #     # if my_trip.reviewers.filter(order=my_order).count() > 0:
    #     #     print("found")
    #     #     found_equal = False
    #     #     for reviewer in my_trip.reviewers.all():
    #     #         if reviewer.order == my_order:
    #     #             found_equal = True
    #     #
    #     #         if found_equal:
    #     #             reviewer.order += 1
    #     #             reviewer.save()
    #     return cleaned_data

    # else:
    #     reviewer.order = count
    # count += 1

    # north = cleaned_data.get("north")
    # south = cleaned_data.get("south")
    # east = cleaned_data.get("east")
    # west = cleaned_data.get("west")
    #
    # if not north or not south or not east or not west:
    #
    # raise forms.ValidationError("You must enter valid values for all directions.")


ReviewerFormSet = modelformset_factory(
    model=models.Reviewer,
    form=ReviewerForm,
    extra=1,
)


class FileForm(forms.ModelForm):
    class Meta:
        model = models.File
        exclude = ["date_created", ]
        widgets = {
            'trip_request': forms.HiddenInput(),
        }


class HelpTextForm(forms.ModelForm):
    class Meta:
        model = models.HelpText
        fields = "__all__"
        widgets = {
            'eng_text': forms.Textarea(attrs={"rows": 4}),
            'fra_text': forms.Textarea(attrs={"rows": 4}),
        }


HelpTextFormSet = modelformset_factory(
    model=models.HelpText,
    form=HelpTextForm,
    extra=1,
)


class CostForm(forms.ModelForm):
    class Meta:
        model = models.Cost
        fields = "__all__"


CostFormSet = modelformset_factory(
    model=models.Cost,
    form=CostForm,
    extra=1,
)


class CostCategoryForm(forms.ModelForm):
    class Meta:
        model = models.CostCategory
        fields = "__all__"


CostCategoryFormSet = modelformset_factory(
    model=models.CostCategory,
    form=CostCategoryForm,
    extra=1,
)


class NJCRatesForm(forms.ModelForm):
    class Meta:
        model = models.NJCRates
        exclude = ['last_modified', ]


NJCRatesFormSet = modelformset_factory(
    model=models.NJCRates,
    form=NJCRatesForm,
    extra=0,
)


class TripRequestCostForm(forms.ModelForm):
    class Meta:
        model = models.TripRequestCost
        fields = "__all__"
        widgets = {
            'trip_request': forms.HiddenInput(),
            'rate_cad': forms.NumberInput(attrs={"class": "by-rate"}),
            'number_of_days': forms.NumberInput(attrs={"class": "by-rate"}),
            'amount_cad': forms.NumberInput(attrs={"class": "by-amount"}),
            # 'cost': forms.Select(attrs=chosen_js),
        }
