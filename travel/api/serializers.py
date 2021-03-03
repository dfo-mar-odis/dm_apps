from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Q
from django.template.defaultfilters import slugify, date
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from lib.functions.custom_functions import listrify
from lib.templatetags.custom_filters import nz
from shared_models.api.serializers import SectionSerializer
from .. import models
# from ..utils import can_modify_project
from ..utils import get_cost_comparison


class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class TripSerializerLITE(serializers.ModelSerializer):
    class Meta:
        model = models.Trip
        fields = "__all__"

    abstract_deadline = serializers.SerializerMethodField()
    adm_review_deadline = serializers.SerializerMethodField()
    date_eligible_for_adm_review = serializers.SerializerMethodField()
    dates = serializers.SerializerMethodField()
    days_until_adm_review_deadline = serializers.SerializerMethodField()
    days_until_eligible_for_adm_review = serializers.SerializerMethodField()
    display = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    fiscal_year = serializers.StringRelatedField()
    lead = serializers.StringRelatedField()
    registration_deadline = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    status_class = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    time_until_adm_review_deadline = serializers.SerializerMethodField()
    time_until_eligible_for_adm_review = serializers.SerializerMethodField()
    tname = serializers.SerializerMethodField()
    traveller_count = serializers.SerializerMethodField()
    trip_subcategory = serializers.StringRelatedField()

    def get_abstract_deadline(self, instance):
        return instance.abstract_deadline.strftime("%Y-%m-%d") if instance.abstract_deadline else None

    def get_adm_review_deadline(self, instance):
        return instance.adm_review_deadline.strftime("%Y-%m-%d") if instance.adm_review_deadline else None

    def get_date_eligible_for_adm_review(self, instance):
        return instance.date_eligible_for_adm_review.strftime("%Y-%m-%d") if instance.date_eligible_for_adm_review else None

    def get_dates(self, instance):
        return instance.dates

    def get_days_until_adm_review_deadline(self, instance):
        return instance.days_until_adm_review_deadline

    def get_days_until_eligible_for_adm_review(self, instance):
        return instance.days_until_eligible_for_adm_review

    def get_display(self, instance):
        return str(instance)

    def get_end_date(self, instance):
        return instance.end_date.strftime("%Y-%m-%d")

    def get_registration_deadline(self, instance):
        return instance.registration_deadline.strftime("%Y-%m-%d") if instance.registration_deadline else None

    def get_start_date(self, instance):
        return instance.start_date.strftime("%Y-%m-%d")

    def get_status_class(self, instance):
        return slugify(instance.get_status_display())

    def get_status_display(self, instance):
        return instance.get_status_display()

    def get_time_until_adm_review_deadline(self, instance):
        return naturaltime(instance.adm_review_deadline)

    def get_time_until_eligible_for_adm_review(self, instance):
        return naturaltime(instance.date_eligible_for_adm_review)

    def get_tname(self, instance):
        return instance.tname

    def get_traveller_count(self, instance):
        return instance.travellers.count()


class RequestReviewerSerializerLITE(serializers.ModelSerializer):
    class Meta:
        model = models.Reviewer
        fields = "__all__"

    comments_html = serializers.SerializerMethodField()
    role_display = serializers.SerializerMethodField()
    status_class = serializers.SerializerMethodField()
    status_date = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    user_display = serializers.SerializerMethodField()

    def get_comments_html(self, instance):
        return instance.comments_html

    def get_role_display(self, instance):
        return instance.get_role_display()

    def get_status_class(self, instance):
        return slugify(instance.get_status_display())

    def get_status_date(self, instance):
        return date(instance.status_date)

    def get_status_display(self, instance):
        return instance.get_status_display()

    def get_user_display(self, instance):
        return instance.user.get_full_name() if instance.user else None


class TripRequestSerializerLITE(serializers.ModelSerializer):
    class Meta:
        model = models.TripRequest
        fields = "__all__"

    created_by = serializers.SerializerMethodField()
    display = serializers.SerializerMethodField()
    is_late_request = serializers.SerializerMethodField()
    processing_time = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    reviewer_history = serializers.SerializerMethodField()
    section = SectionSerializer()
    status_class = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    traveller_count = serializers.SerializerMethodField()
    trip = TripSerializerLITE(read_only=True)
    trip_display = serializers.SerializerMethodField()
    fiscal_year = serializers.StringRelatedField()

    def get_created_by(self, instance):
        if instance.created_by:
            return instance.created_by.get_full_name()

    def get_display(self, instance):
        return str(instance)

    def get_is_late_request(self, instance):
        return instance.is_late_request

    def get_processing_time(self, instance):
        return instance.processing_time

    def get_region(self, instance):
        return instance.section.division.branch.region.tname

    def get_reviewer_history(self, instance):
        return RequestReviewerSerializerLITE(instance.reviewers.filter(~Q(status__in=[4, 20, 1])), many=True, read_only=True).data

    def get_section(self, instance):
        return instance.section.shortish_name

    def get_status_class(self, instance):
        return slugify(instance.get_status_display())

    def get_status_display(self, instance):
        return instance.get_status_display()

    def get_traveller_count(self, instance):
        return instance.travellers.count()

    def get_trip_display(self, instance):
        return str(instance.trip)


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = "__all__"

    date_created = serializers.SerializerMethodField()

    def get_date_created(self, instance):
        return date(instance.date_created)


class RequestReviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reviewer
        fields = "__all__"

    comments_html = serializers.SerializerMethodField()
    request_obj = serializers.SerializerMethodField()
    role_display = serializers.SerializerMethodField()
    status_class = serializers.SerializerMethodField()
    status_date = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    user_display = serializers.SerializerMethodField()

    def get_comments_html(self, instance):
        return instance.comments_html

    def get_request_obj(self, instance):
        if instance.request:
            return TripRequestSerializerLITE(instance.request, read_only=True).data

    def get_role_display(self, instance):
        return instance.get_role_display()

    def get_status_class(self, instance):
        return slugify(instance.get_status_display())

    def get_status_date(self, instance):
        return date(instance.status_date)

    def get_status_display(self, instance):
        return instance.get_status_display()

    def get_user_display(self, instance):
        return instance.user.get_full_name() if instance.user else None


class CostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TravellerCost
        fields = "__all__"

    cost_display = serializers.SerializerMethodField()

    def get_cost_display(self, instance):
        return str(instance.cost)


class TravellerSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(format="%Y-%m-%d", input_formats=None, required=False, allow_null=True)
    end_date = serializers.DateTimeField(format="%Y-%m-%d", input_formats=None, required=False, allow_null=True)
    costs = CostSerializer(many=True, read_only=True)

    class Meta:
        model = models.Traveller
        fields = "__all__"

    adm_travel_history = serializers.SerializerMethodField()
    cost_breakdown_html = serializers.SerializerMethodField()
    dates = serializers.SerializerMethodField()
    long_role = serializers.SerializerMethodField()
    non_dfo_costs_html = serializers.SerializerMethodField()
    request_obj = serializers.SerializerMethodField()
    role_display = serializers.SerializerMethodField()
    smart_name = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()

    def get_adm_travel_history(self, instance):
        if instance.user:
            qs = models.TripRequest.objects.filter(
                travellers__user=instance.user, trip__is_adm_approval_required=True, status=11).order_by("trip__start_date").distinct()
            return TripRequestSerializerLITE(qs, many=True, read_only=True).data
        return list()

    def get_cost_breakdown_html(self, instance):
        return instance.cost_breakdown_html

    def get_dates(self, instance):
        return instance.dates

    def get_long_role(self, instance):
        return instance.long_role

    def get_non_dfo_costs_html(self, instance):
        return instance.non_dfo_costs_html

    def get_request_obj(self, instance):
        return TripRequestSerializerLITE(instance.request).data

    def get_role_display(self, instance):
        return str(instance.role)

    def get_smart_name(self, instance):
        return instance.smart_name

    def get_total_cost(self, instance):
        return instance.total_cost

    def validate(self, attrs):
        """
        form validation:
        - make sure that the user is not already attending this trip!
        - make sure that the request start date and the trip start date make sense with respect to each other and individually
        - if this user selects Other as a role they must provide a description of role
        """
        trip_request = attrs.get("request")
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        user = attrs.get("user")
        trip = trip_request.trip
        trip_start_date = trip.start_date
        trip_end_date = trip.end_date

        # make sure that the user is not already attending this trip from another request!
        if user and models.Traveller.objects.filter(~Q(request=trip_request)).filter(request__trip=trip, user=user).exists():
            msg = _('This user is cannot be added here because they are listed on another request!')
            raise ValidationError(msg)

        # first, let's look at the request date and make sure it makes sense, i.e. start date is before end date and
        # the length of the trip is not too long
        if start_date and end_date:
            if end_date < start_date:
                msg = _('The start date of the trip must occur before the end date.')
                raise ValidationError(msg)
            if abs((start_date - end_date).days) > 180:
                msg = _('The length of this trip is unrealistic.')
                raise ValidationError(msg)
            # is the start date of the travel request equal to or before the start date of the trip?
            if trip_start_date:
                delta = abs(start_date - trip_start_date)
                if delta.days > 10:
                    msg = _(
                        "The start date of this request ({start_date}) has to be within 10 days of the start date of the selected trip ({trip_start_date})!").format(
                        start_date=start_date.strftime("%Y-%m-%d"),
                        trip_start_date=trip_start_date.strftime("%Y-%m-%d"),
                    )
                    raise ValidationError(msg)

            # is the end_date of the travel request equal to or after the end date of the trip?
            if trip_end_date:
                delta = abs(end_date - trip_end_date)
                if delta.days > 10:
                    msg = _(
                        "The end date of this request ({end_date}) must be within 10 days of the end date of the selected trip ({trip_end_date})!").format(
                        end_date=end_date.strftime("%Y-%m-%d"),
                        trip_end_date=trip_end_date.strftime("%Y-%m-%d"),
                    )
                    raise ValidationError(msg)

            # if this user selects Other as a role they must provide a description of role
            role = attrs.get("role")
            role_of_participant = attrs.get("role_of_participant")
            if role and "other" in role.name.lower() and not role_of_participant:
                msg = _("If you select the role 'other', you must also provide a description of the role.")
                raise ValidationError(msg)

        return attrs


class TripRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TripRequest
        fields = "__all__"

    admin_notes_html = serializers.SerializerMethodField()
    bta_attendees = serializers.SerializerMethodField()
    cost_comparison = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    display = serializers.SerializerMethodField()
    files = FileSerializer(many=True, read_only=True)
    fiscal_year = serializers.StringRelatedField()
    is_late_request = serializers.SerializerMethodField()
    metadata = serializers.SerializerMethodField()
    original_submission_date = serializers.SerializerMethodField()
    processing_time = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    reviewer_order_message = serializers.SerializerMethodField()
    reviewers = RequestReviewerSerializer(many=True, read_only=True)
    section = SectionSerializer()
    status_class = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    total_dfo_funding = serializers.SerializerMethodField()
    total_non_dfo_funding = serializers.SerializerMethodField()
    total_non_dfo_funding_sources = serializers.SerializerMethodField()
    total_request_cost = serializers.SerializerMethodField()
    travellers = TravellerSerializer(many=True, read_only=True)
    travellers_from_other_regions = serializers.SerializerMethodField()
    travellers_from_other_requests = serializers.SerializerMethodField()
    trip = TripSerializerLITE(read_only=True)
    trip_display = serializers.SerializerMethodField()

    def get_admin_notes_html(self, instance):
        return instance.admin_notes_html

    def get_bta_attendees(self, instance):
        return listrify(instance.bta_attendees.all())

    def get_cost_comparison(self, instance):
        return get_cost_comparison(instance.travellers.all())

    def get_created_by(self, instance):
        if instance.created_by:
            return instance.created_by.get_full_name()

    def get_display(self, instance):
        return str(instance)

    def get_is_late_request(self, instance):
        return instance.is_late_request

    def get_metadata(self, instance):
        return instance.metadata

    def get_original_submission_date(self, instance):
        return date(instance.original_submission_date)

    def get_processing_time(self, instance):
        return instance.processing_time

    def get_region(self, instance):
        return instance.region.tname

    def get_reviewer_order_message(self, instance):
        return instance.reviewer_order_message

    def get_section(self, instance):
        return instance.section.shortish_name

    def get_status_class(self, instance):
        return slugify(instance.get_status_display())

    def get_status_display(self, instance):
        return instance.get_status_display()

    def get_total_dfo_funding(self, instance):
        return instance.total_dfo_funding

    def get_total_non_dfo_funding(self, instance):
        return instance.total_non_dfo_funding

    def get_total_non_dfo_funding_sources(self, instance):
        return nz(instance.total_non_dfo_funding_sources)

    def get_total_request_cost(self, instance):
        return instance.total_request_cost

    def get_travellers_from_other_regions(self, instance):
        return TravellerSerializer(instance.travellers_from_other_regions, many=True, read_only=True).data

    def get_travellers_from_other_requests(self, instance):
        return TravellerSerializer(instance.travellers_from_other_requests, many=True, read_only=True).data

    def get_trip_display(self, instance):
        return instance.trip.tname


class TripReviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TripReviewer
        fields = "__all__"

    comments_html = serializers.SerializerMethodField()
    role_display = serializers.SerializerMethodField()
    status_class = serializers.SerializerMethodField()
    status_date = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    trip_obj = serializers.SerializerMethodField()
    user_display = serializers.SerializerMethodField()

    def get_comments_html(self, instance):
        return instance.comments_html

    def get_role_display(self, instance):
        return instance.get_role_display()

    def get_status_class(self, instance):
        return slugify(instance.get_status_display())

    def get_status_date(self, instance):
        return date(instance.status_date)

    def get_status_display(self, instance):
        return instance.get_status_display()

    def get_trip_obj(self, instance):
        if instance.trip:
            return TripSerializerLITE(instance.trip, read_only=True).data

    def get_user_display(self, instance):
        return instance.user.get_full_name() if instance.user else None


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Trip
        fields = "__all__"

    abstract_deadline = serializers.SerializerMethodField()
    adm_review_deadline = serializers.SerializerMethodField()
    admin_notes_html = serializers.SerializerMethodField()
    cost_comparison = serializers.SerializerMethodField()
    date_eligible_for_adm_review = serializers.SerializerMethodField()
    dates = serializers.SerializerMethodField()
    days_until_adm_review_deadline = serializers.SerializerMethodField()
    display = serializers.SerializerMethodField()
    fiscal_year = serializers.StringRelatedField()
    lead = serializers.StringRelatedField()
    metadata = serializers.SerializerMethodField()
    non_res_total_cost = serializers.SerializerMethodField()
    registration_deadline = serializers.SerializerMethodField()
    requests = TripRequestSerializerLITE(many=True, read_only=True)
    reviewers = TripReviewerSerializer(many=True, read_only=True)
    status_class = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    time_until_adm_review_deadline = serializers.SerializerMethodField()
    tname = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()
    total_dfo_cost = serializers.SerializerMethodField()
    total_non_dfo_cost = serializers.SerializerMethodField()
    total_non_dfo_funding_sources = serializers.SerializerMethodField()
    travellers = serializers.SerializerMethodField()
    trip_review_ready = serializers.SerializerMethodField()
    trip_subcategory = serializers.StringRelatedField()

    def get_abstract_deadline(self, instance):
        return date(instance.abstract_deadline)

    def get_adm_review_deadline(self, instance):
        return date(instance.adm_review_deadline)

    def get_admin_notes_html(self, instance):
        return instance.admin_notes_html

    def get_cost_comparison(self, instance):
        return get_cost_comparison(instance.travellers)

    def get_date_eligible_for_adm_review(self, instance):
        return date(instance.date_eligible_for_adm_review)

    def get_dates(self, instance):
        return instance.dates

    def get_days_until_adm_review_deadline(self, instance):
        return instance.days_until_adm_review_deadline

    def get_display(self, instance):
        return str(instance)

    def get_metadata(self, instance):
        return instance.metadata

    def get_non_res_total_cost(self, instance):
        return instance.non_res_total_cost

    def get_registration_deadline(self, instance):
        return date(instance.registration_deadline)

    def get_status_class(self, instance):
        return slugify(instance.get_status_display())

    def get_status_display(self, instance):
        return instance.get_status_display()

    def get_time_until_adm_review_deadline(self, instance):
        return naturaltime(instance.adm_review_deadline)

    def get_tname(self, instance):
        return instance.tname

    def get_total_cost(self, instance):
        return instance.total_cost

    def get_total_dfo_cost(self, instance):
        return instance.total_dfo_cost

    def get_total_non_dfo_cost(self, instance):
        return instance.total_non_dfo_cost

    def get_total_non_dfo_funding_sources(self, instance):
        return instance.total_non_dfo_funding_sources

    def get_travellers(self, instance):
        return TravellerSerializer(instance.travellers, many=True, read_only=True).data

    def get_trip_review_ready(self, instance):
        return instance.trip_review_ready

