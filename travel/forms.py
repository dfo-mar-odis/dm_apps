from django import forms
from django.forms import modelformset_factory
from django.utils import timezone
from django.utils.translation import gettext as _
from django.contrib.auth.models import User as AuthUser, User
from shared_models import models as shared_models
from travel.filters import get_region_choices

from . import models

chosen_js = {"class": "chosen-select-contains"}
attr_fp_date = {"class": "fp-date", "placeholder": "Click to select a date.."}
attr_phone = {"class": "input-phone"}
attr_row3 = {"rows": 3}
attr_row4 = {"rows": 4}

YES_NO_CHOICES = (
    (True, _("Yes")),
    (False, _("No")),
)
INT_YES_NO_CHOICES = (
    (None, "-----"),
    (1, _("Yes")),
    (0, _("No")),
)


class ReviewerApprovalForm(forms.ModelForm):
    approved = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    changes_requested = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    stay_on_page = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    reset = forms.BooleanField(widget=forms.HiddenInput(), required=False)

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


class TripReviewerApprovalForm(forms.ModelForm):
    # approved = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    stay_on_page = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = models.TripReviewer
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


class TripRequestApprovalForm(forms.ModelForm):
    class Meta:
        model = models.TripRequest
        fields = [
            "created_by",
        ]
        widgets = {
            "created_by": forms.HiddenInput()
        }


class TripTimestampUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Conference
        fields = [
            "last_modified_by",
        ]
        widgets = {
            "last_modified_by": forms.HiddenInput()
        }


class TripRequestForm(forms.ModelForm):
    stay_on_page = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    reset_reviewers = forms.BooleanField(widget=forms.Select(choices=YES_NO_CHOICES),
                                         label=_("Do you want to reset the reviewer list?"), required=False)

    class Meta:
        model = models.TripRequest
        exclude = [
            "total_cost",
            "fiscal_year",
            "submitted",
            "status",
            "exclude_from_travel_plan",
            "admin_notes",
            "original_submission_date",
            "created_by",
        ]
        labels = {
            'bta_attendees': _("Other attendees covered under BTA (i.e., they will not need to have a travel plan)"),
        }

        widgets = {
            'bta_attendees': forms.SelectMultiple(attrs=chosen_js),
            'trip': forms.Select(attrs=chosen_js),
            'is_group_request': forms.Select(choices=YES_NO_CHOICES),
            'objective_of_event': forms.Textarea(attrs=attr_row3),
            'benefit_to_dfo': forms.Textarea(attrs=attr_row3),
            'late_justification': forms.Textarea(attrs=attr_row3),
            'funding_source': forms.Textarea(attrs=attr_row3),
            'notes': forms.Textarea(attrs=attr_row3),

            # hidden fields
            'parent_request': forms.HiddenInput(),

            # non-group trip request fields

            # user fields
            'is_public_servant': forms.Select(attrs={"class": "not-a-group-field disappear-if-user"}, choices=YES_NO_CHOICES),
            'user': forms.Select(attrs={"class": "chosen-select-contains"}),
            'first_name': forms.TextInput(attrs={"class": "not-a-group-field disappear-if-user"}),
            'last_name': forms.TextInput(attrs={"class": "not-a-group-field disappear-if-user"}),
            'section': forms.Select(attrs=chosen_js),
            'email': forms.EmailInput(attrs={"class": "not-a-group-field disappear-if-user"}),
            'address': forms.TextInput(attrs={"class": "not-a-group-field"}),
            'phone': forms.TextInput(attrs={"class": "not-a-group-field input-phone"}),
            'company_name': forms.TextInput(attrs={"class": "not-a-group-field disappear-if-user hide-if-public-servant"}),
            'is_research_scientist': forms.Select(attrs={"class": "not-a-group-field hide-if-not-public-servant"}, choices=YES_NO_CHOICES),

            'start_date': forms.DateInput(attrs={"class": "not-a-group-field fp-date", "placeholder": "Click to select a date.."}),
            'end_date': forms.DateInput(attrs={"class": "not-a-group-field fp-date", "placeholder": "Click to select a date.."}),
            'departure_location': forms.TextInput(attrs={"class": "not-a-group-field"}),
            # 'reason': forms.Select(attrs={"class": "not-a-group-field"}),
            'role': forms.Select(attrs={"class": "not-a-group-field"}),
            'region': forms.Select(attrs={"class": "not-a-group-field hide-if-not-public-servant"}),
            'role_of_participant': forms.Textarea(attrs={"class": "not-a-group-field", "rows": 3}),
            'multiple_conferences_rationale': forms.Textarea(attrs={"class": "not-a-group-field", "rows": 3}),
            'non_dfo_costs': forms.NumberInput(attrs={"class": "not-a-group-field"}),
            'non_dfo_org': forms.TextInput(attrs={"class": "not-a-group-field"}),
        }

    def __init__(self, *args, **kwargs):
        user_choices = [(u.id, "{}, {}".format(u.last_name, u.first_name)) for u in
                        AuthUser.objects.all().order_by("last_name", "first_name") if u.first_name and u.last_name and u.email]
        user_choices.insert(0, tuple((None, "---")))

        section_choices = [(s.id, s.full_name) for s in
                           shared_models.Section.objects.filter(division__branch_id__in=[1, 3, 9, ]).order_by("division__branch__region",
                                                                                                              "division__branch",
                                                                                                              "division", "name")]
        section_choices.insert(0, tuple((None, "---")))

        trip_choices = [(t.id, f'{t} ({t.status})') for t in models.Conference.objects.filter(start_date__gte=timezone.now())]
        trip_choices.insert(0, tuple((None, "---")))

        super().__init__(*args, **kwargs)
        self.fields['trip'].choices = trip_choices
        self.fields['user'].choices = user_choices
        self.fields['bta_attendees'].choices = user_choices
        self.fields['section'].choices = section_choices

        # general trip infomation
        field_list = [
            'is_group_request',
            'trip',
            'departure_location',
            'destination',
            'start_date',
            'end_date',
            'bta_attendees',
            'non_dfo_costs',
            'non_dfo_org',
        ]
        for field in field_list:
            self.fields[field].group = 1

        # traveller info
        field_list = [
            'user',
            'section',
            'first_name',
            'last_name',
            'address',
            'phone',
            'email',
            'is_public_servant',
            'is_research_scientist',
            'company_name',
            'region',
        ]
        for field in field_list:
            self.fields[field].group = 2

        # justification
        field_list = [
            # 'reason',
            'role',
            'role_of_participant',
            'objective_of_event',
            'benefit_to_dfo',
            'multiple_conferences_rationale',
            'late_justification',
            'funding_source',
            'notes',
        ]
        for field in field_list:
            self.fields[field].group = 3

        # Reviewers
        field_list = [
            'reset_reviewers',
        ]
        for field in field_list:
            self.fields[field].group = 4

        # are there any forgotten fields?
        for field in self.fields:
            try:
                self.fields[field].group
            except AttributeError:
                # print(f'Adding label: "Unspecified" to field "{field}".')
                self.fields[field].group = 0

        # if there is no instance of TR, remove the field for reset_reviewers.
        if not kwargs.get("instance"):
            del self.fields["reset_reviewers"]

    def clean(self):
        """
        form validation:
        1) make sure the trip is opened for business
        2) make sure that the request start date and the trip start date make sense with respect to each other and individually
        """

        cleaned_data = super().clean()
        request_start_date = cleaned_data.get("start_date")
        request_end_date = cleaned_data.get("end_date")
        trip = cleaned_data.get("trip")
        trip_start_date = trip.start_date
        trip_end_date = trip.end_date

        if trip.status_id not in [30, 41] and self.instance not in trip.trip_requests.all():
            if trip.status_id == 31:
                message = _("This trip is currently under review from NCR and is closed to additional requests.")
            elif trip.status_id == 32:
                message = _("This trip has already been reviewed by NCR and is closed to additional requests.")
            else:
                message = _("This trip is closed to additional requests.")
            self.add_error('trip', message)
            # raise forms.ValidationError(message)

        # first, let's look at the request date and make sure it makes sense, i.e. start date is before end date and
        # the length of the trip is not too long
        if request_start_date and request_end_date:
            if request_end_date < request_start_date:
                msg = _('The start date of the trip must occur after the end date.')
                self.add_error('start_date', msg)
                self.add_error('end_date', msg)
                raise forms.ValidationError(_('The start date of the trip must occur after the end date.'))
            if abs((request_start_date - request_end_date).days) > 100:
                msg = _('The length of this trip is unrealistic.')
                self.add_error('start_date', msg)
                self.add_error('end_date', msg)
                raise forms.ValidationError(msg)
            # is the start date of the travel request equal to or before the start date of the trip?
            if trip_start_date:
                delta = abs(request_start_date - trip_start_date)
                if delta.days > 10:
                    msg = _(
                        f'The start date of this request ({request_start_date.strftime("%Y-%m-%d")}) has to be within 10 days of the'
                        f' start date of the selected trip ({trip_start_date.strftime("%Y-%m-%d")})!')
                    self.add_error('start_date', msg)
                    # self.add_error('trip', msg)
                    raise forms.ValidationError(msg)

            # is the end_date of the travel request equal to or after the end date of the trip?
            if trip_end_date:
                delta = abs(request_end_date - trip_end_date)
                if delta.days > 10:
                    msg = _(
                        f'The end date of this request ({request_end_date.strftime("%Y-%m-%d")}) must be within 10 days'
                        f' of the end date of the selected trip ({trip_end_date.strftime("%Y-%m-%d")})!')
                    self.add_error('end_date', msg)
                    # self.add_error('trip', msg)
                    raise forms.ValidationError(msg)


class TripRequestAdminNotesForm(forms.ModelForm):
    class Meta:
        model = models.TripRequest
        fields = [
            "admin_notes",
        ]


class TripAdminNotesForm(forms.ModelForm):
    class Meta:
        model = models.Conference
        fields = [
            "admin_notes",
            "last_modified_by",
        ]
        widgets = {
            "last_modified_by": forms.HiddenInput()
        }


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
            'non_dfo_costs',
            'non_dfo_org',
            # 'reason',
            'role',
            'role_of_participant',
            'exclude_from_travel_plan',
            'parent_request',
            'multiple_conferences_rationale',
        ]
        widgets = {
            'user': forms.Select(attrs=chosen_js),
            'parent_request': forms.HiddenInput(),
            'start_date': forms.DateInput(attrs=attr_fp_date),
            'end_date': forms.DateInput(attrs=attr_fp_date),
            'role_of_participant': forms.Textarea(attrs=attr_row3),
            'multiple_conferences_rationale': forms.Textarea(attrs=attr_row3),
            'phone': forms.TextInput(attrs={"class": "disappear-if-user input-phone"}),
            'first_name': forms.TextInput(attrs={"class": "disappear-if-user"}),
            'last_name': forms.TextInput(attrs={"class": "disappear-if-user"}),
            'email': forms.EmailInput(attrs={"class": "disappear-if-user"}),
            'exclude_from_travel_plan': forms.Select(choices=YES_NO_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        try:
            parent_request = kwargs.get("initial").get("parent_request")
        except AttributeError:
            parent_request = None

        if not parent_request:
            parent_request = kwargs.get("instance").parent_request

        user_choices = [(u.id, "{}, {}".format(u.last_name, u.first_name)) for u in
                        AuthUser.objects.all().order_by("last_name", "first_name") if u.first_name and u.last_name and u.email]
        user_choices.insert(0, tuple((None, "---")))
        super().__init__(*args, **kwargs)
        self.fields['user'].choices = user_choices

        # general trip infomation
        field_list = [
            'start_date',
            'end_date',
            'departure_location',
            'exclude_from_travel_plan',
            'non_dfo_costs',
            'non_dfo_org',
        ]
        for field in field_list:
            self.fields[field].group = 1

        # traveller info
        field_list = [
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
        ]
        for field in field_list:
            self.fields[field].group = 2

        # justification
        field_list = [
            # 'reason',
            'role',
            'role_of_participant',
            'multiple_conferences_rationale',
        ]
        for field in field_list:
            self.fields[field].group = 3

        # are there any forgotten fields?
        for field in self.fields:
            try:
                self.fields[field].group
            except AttributeError:
                # print(f'Adding label: "Unspecified" to field "{field}".')
                self.fields[field].group = 0

    def clean(self):
        """
        form validation:
        1) make sure that the request start date and the trip start date make sense with respect to each other and individually
        """

        cleaned_data = super().clean()
        request_start_date = cleaned_data.get("start_date")
        request_end_date = cleaned_data.get("end_date")
        trip = cleaned_data.get("parent_request").trip
        trip_start_date = trip.start_date
        trip_end_date = trip.end_date
        user = cleaned_data.get("user")

        # we have to make sure there is not already a trip request in the system for this user and this trip
        if user and user.user_trip_requests.filter(trip=trip, is_group_request=False).count():
            msg = _('There is already a trip request in the system for this user and this trip.')
            self.add_error('user', msg)

        # first, let's look at the request date and make sure it makes sense, i.e. start date is before end date and
        # the length of the trip is not too long
        if request_start_date and request_end_date:
            if request_end_date < request_start_date:
                msg = _('The start date of the trip must occur after the end date.')
                self.add_error('start_date', msg)
                self.add_error('end_date', msg)
            if abs((request_start_date - request_end_date).days) > 100:
                msg = _('The length of this trip is unrealistic.')
                self.add_error('start_date', msg)
                self.add_error('end_date', msg)
            # is the start date of the travel request equal to or before the start date of the trip?
            if trip_start_date:
                delta = abs(request_start_date - trip_start_date)
                if delta.days > 10:
                    msg = _(
                        f'The start date of this request ({request_start_date.strftime("%Y-%m-%d")}) has to be within 10 days of the'
                        f' start date of the selected trip ({trip_start_date.strftime("%Y-%m-%d")})!')
                    self.add_error('start_date', msg)
                    # self.add_error('trip', msg)

            # is the end_date of the travel request equal to or after the end date of the trip?
            if trip_end_date:
                delta = abs(request_end_date - trip_end_date)
                if delta.days > 10:
                    msg = _(
                        f'The end date of this request ({request_end_date.strftime("%Y-%m-%d")}) must be within 10 days'
                        f' of the end date of the selected trip ({trip_end_date.strftime("%Y-%m-%d")})!')
                    self.add_error('end_date', msg)
                    # self.add_error('trip', msg)


class TripForm(forms.ModelForm):
    class Meta:
        model = models.Conference
        exclude = ["fiscal_year", "is_verified", "verified_by", "cost_warning_sent", "status", "admin_notes", "review_start_date",
                   "adm_review_deadline", "date_eligible_for_adm_review"]
        widgets = {
            'start_date': forms.DateInput(attrs=attr_fp_date),
            'end_date': forms.DateInput(attrs=attr_fp_date),
            'registration_deadline': forms.DateInput(attrs=attr_fp_date),
            'abstract_deadline': forms.DateInput(attrs=attr_fp_date),
            'last_modified_by': forms.HiddenInput(),
            # 'trip_subcategory': forms.RadioSelect(),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        abstract_deadline = cleaned_data.get("abstract_deadline")
        registration_deadline = cleaned_data.get("registration_deadline")

        if start_date and end_date:
            if end_date < start_date:
                msg = _('The start date of the trip must occur after the end date.')
                self.add_error('start_date', msg)
                self.add_error('end_date', msg)
                raise forms.ValidationError(_('The start date of the trip must occur after the end date.'))
            if abs((start_date - end_date).days) > 100:
                msg = _('The length of this trip is unrealistic.')
                self.add_error('start_date', msg)
                self.add_error('end_date', msg)
                raise forms.ValidationError(msg)

        if abstract_deadline and abstract_deadline >= start_date:
            msg = _('The abstract deadline of the trip (if present) must occur before the start date.')
            self.add_error('abstract_deadline', msg)
            raise forms.ValidationError(msg)

        if registration_deadline and registration_deadline > start_date:
            msg = _('The registration deadline of the trip (if present) must occur before or on the start date.')
            self.add_error('registration_deadline', msg)
            raise forms.ValidationError(msg)


class ReportSearchForm(forms.Form):
    REPORT_CHOICES = (
        (None, "------"),
        (1, "CFTS export (xlsx)"),
        # (2, "Print Travel Plan PDF"),
        (3, "Export trip list (xlsx)"),
    )
    report = forms.ChoiceField(required=True, choices=REPORT_CHOICES)
    # report #1
    fiscal_year = forms.ChoiceField(required=False, label=_('Fiscal year'))
    # report #2
    user = forms.ChoiceField(required=False, label=_('Traveller'), widget=forms.Select(attrs=chosen_js))
    trip = forms.ChoiceField(required=False, label=_('Trip'), widget=forms.Select(attrs=chosen_js))
    region = forms.ChoiceField(required=False, label=_('Region'))
    adm = forms.ChoiceField(required=False, label=_('ADM approval required'), choices=INT_YES_NO_CHOICES)
    from_date = forms.CharField(required=False, widget=forms.DateInput(attrs=attr_fp_date))
    to_date = forms.CharField(required=False, widget=forms.DateInput(attrs=attr_fp_date))

    def __init__(self, *args, **kwargs):
        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all().order_by("id") if fy.trip_requests.count() > 0]
        fy_choices.insert(0, tuple((None, "---")))
        # TRAVELLER_CHOICES = [(e['email'], "{}, {}".format(e['last_name'], e['first_name'])) for e in
        #                      models.Trip.objects.values("email", "first_name", "last_name").order_by("last_name", "first_name").distinct()]
        user_choices = [(u.id, "{}, {}".format(u.last_name, u.first_name)) for u in
                        AuthUser.objects.all().order_by("last_name", "first_name") if u.user_trip_requests.count() > 0]
        user_choices.insert(0, tuple((None, "---")))
        trip_choices = [(trip.id, f"{trip}") for trip in models.Conference.objects.all()]
        trip_choices.insert(0, tuple((None, "---")))

        region_choices = get_region_choices()
        region_choices.insert(0, tuple((None, "---")))

        super().__init__(*args, **kwargs)
        self.fields['fiscal_year'].choices = fy_choices
        self.fields['user'].choices = user_choices
        self.fields['region'].choices = region_choices
        self.fields['trip'].choices = trip_choices


class StatusForm(forms.ModelForm):
    class Meta:
        model = models.Status
        fields = [
            "name",
            "nom",
            "used_for",
            "order",
            "color",
        ]


StatusFormset = modelformset_factory(
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

    def clean(self):
        """
        The order, user, or role cannot be changed if the reviewer status is approved or queued
        :return:
        """
        my_object = self.instance
        cleaned_data = super().clean()
        order = cleaned_data.get("order")
        user = cleaned_data.get("user")
        role = cleaned_data.get("role")

        # Check the role
        if my_object.status and my_object.status.id not in [4, 20]:
            # need to determine if there have been any changes
            if my_object.role != role:
                raise forms.ValidationError(_(f'Sorry, the role of a reviewer whose status is set to {my_object.status} cannot be changed'))

            if my_object.user != user:
                raise forms.ValidationError(
                    _(f'Sorry, you cannot change the associated DM Apps user of a reviewer whose status is set to {my_object.status}'))

            if my_object.order != order:
                raise forms.ValidationError(
                    _(f'Sorry, the order of a reviewer whose status is set to {my_object.status} cannot be changed'))


ReviewerFormset = modelformset_factory(
    model=models.Reviewer,
    form=ReviewerForm,
    extra=1,
)


class TripReviewerForm(forms.ModelForm):
    class Meta:
        model = models.TripReviewer
        fields = [
            'trip',
            'order',
            'user',
            'role',
        ]
        widgets = {
            'trip': forms.HiddenInput(),
            'user': forms.Select(attrs=chosen_js),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_choices = [(u.id, str(u)) for u in User.objects.all()]
        # user_choices = [(u.id, str(u)) for u in User.objects.filter(groups__name__icontains="travel_adm_admin")]
        # # add any users with special roles
        # user_choices.extend([(df.user.id, str(df.user)) for df in models.DefaultReviewer.objects.filter(reviewer_roles__id__in=[3, 4, 5])])
        # user_choices = list(set(user_choices))
        user_choices.insert(0, (None, "-----"))
        self.fields["user"].choices = user_choices

    def clean(self):
        """
        The order, user, or role cannot be changed if the reviewer status is approved or queued
        :return:
        """
        my_object = self.instance
        cleaned_data = super().clean()
        order = cleaned_data.get("order")
        user = cleaned_data.get("user")
        role = cleaned_data.get("role")

        # Check the role
        if my_object.status and my_object.status.id not in [23, 24]:
            # need to determine if there have been any changes
            if my_object.role != role:
                raise forms.ValidationError(_(f'Sorry, the role of a reviewer whose status is set to {my_object.status} cannot be changed'))

            if my_object.user != user:
                raise forms.ValidationError(
                    _(f'Sorry, you cannot change the associated DM Apps user of a reviewer whose status is set to {my_object.status}'))

            if my_object.order != order:
                raise forms.ValidationError(
                    _(f'Sorry, the order of a reviewer whose status is set to {my_object.status} cannot be changed'))


TripReviewerFormset = modelformset_factory(
    model=models.TripReviewer,
    form=TripReviewerForm,
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


HelpTextFormset = modelformset_factory(
    model=models.HelpText,
    form=HelpTextForm,
    extra=1,
)


class CostForm(forms.ModelForm):
    class Meta:
        model = models.Cost
        fields = "__all__"


CostFormset = modelformset_factory(
    model=models.Cost,
    form=CostForm,
    extra=1,
)


class CostCategoryForm(forms.ModelForm):
    class Meta:
        model = models.CostCategory
        fields = "__all__"


CostCategoryFormset = modelformset_factory(
    model=models.CostCategory,
    form=CostCategoryForm,
    extra=1,
)


class NJCRatesForm(forms.ModelForm):
    class Meta:
        model = models.NJCRates
        exclude = ['last_modified', ]


NJCRatesFormset = modelformset_factory(
    model=models.NJCRates,
    form=NJCRatesForm,
    extra=0,
)


class ReasonForm(forms.ModelForm):
    class Meta:
        model = models.Reason
        fields = "__all__"


ReasonFormset = modelformset_factory(
    model=models.Reason,
    form=ReasonForm,
    extra=1,
)


class ProcessStepForm(forms.ModelForm):
    class Meta:
        model = models.ProcessStep
        fields = "__all__"

ProcessStepFormset = modelformset_factory(
    model=models.ProcessStep,
    form=ProcessStepForm,
    extra=1,
)


class TripSubcategoryForm(forms.ModelForm):
    class Meta:
        model = models.TripSubcategory
        fields = [
            "trip_category",
            "name",
            "nom",
            "description_en",
            "description_fr",
        ]
        widgets = {
            "description_en": forms.Textarea(attrs=attr_row3),
            "description_fr": forms.Textarea(attrs=attr_row3),
        }


TripSubcategoryFormset = modelformset_factory(
    model=models.TripSubcategory,
    form=TripSubcategoryForm,
    extra=1,
)


class TripCategoryForm(forms.ModelForm):
    class Meta:
        model = models.TripCategory
        fields = [
            "name",
            "nom",
            "days_when_eligible_for_review",
        ]


TripCategoryFormset = modelformset_factory(
    model=models.TripCategory,
    form=TripCategoryForm,
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


class DefaultReviewerForm(forms.ModelForm):
    class Meta:
        model = models.DefaultReviewer
        fields = "__all__"
        widgets = {
            "user": forms.Select(attrs=chosen_js),
            "sections": forms.SelectMultiple(attrs=chosen_js),
            "branches": forms.SelectMultiple(attrs=chosen_js),
            "reviewer_roles": forms.SelectMultiple(attrs=chosen_js),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        section_choices = [(s.id, s.full_name) for s in shared_models.Section.objects.all()]
        branch_choices = [(b.id, f"{b} ({b.region})") for b in shared_models.Branch.objects.all()]
        self.fields["sections"].choices = section_choices


class TripSelectForm(forms.Form):
    trip = forms.ChoiceField(widget=forms.Select(attrs=chosen_js), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        trip_choices = [(t.id, f'{t} ({t.status})') for t in models.Conference.objects.all()]
        trip_choices.insert(0, tuple((None, "---")))

        self.fields["trip"].choices = trip_choices
