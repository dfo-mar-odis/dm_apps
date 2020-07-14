import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

from dm_apps.utils import custom_send_mail
from django.db import IntegrityError
from django.utils import timezone
from django.utils.translation import gettext as _
from Levenshtein import distance

from lib.templatetags.custom_filters import nz
from . import models
from . import emails
from shared_models import models as shared_models


def get_trip_reviewers(trip):
    """add reviewers to a trip is adm approval is required. If it isn't, it will remove all reviewers from the trip (if present)"""
    # This section only matters for ADM trips

    if trip.is_adm_approval_required:

        # NCR travel coordinator
        try:
            # add each default NCR coordinator to the queue
            for default_reviewer in models.ReviewerRole.objects.get(pk=3).travel_default_reviewers.order_by("id"):
                models.TripReviewer.objects.get_or_create(trip=trip, user=default_reviewer.user, role_id=3)
        except (IntegrityError, KeyError):
            pass

        # ADM Approver
        try:
            # add each default ADM approver to the queue
            for default_reviewer in models.ReviewerRole.objects.get(pk=4).travel_default_reviewers.order_by("id"):
                models.TripReviewer.objects.get_or_create(trip=trip, user=default_reviewer.user, role_id=4)
        except (IntegrityError, KeyError):
            pass

        # ADM Approver
        try:
            # add ADM to the queue
            for default_reviewer in models.ReviewerRole.objects.get(pk=5).travel_default_reviewers.all():
                models.TripReviewer.objects.get_or_create(trip=trip, user=default_reviewer.user, role_id=5)
        except (IntegrityError, KeyError):
            pass
    else:
        trip.reviewers.all().delete()
    trip.save()


def get_tr_reviewers(trip_request):
    if trip_request.section:

        # section level reviewer
        try:
            # add each default reviewer to the queue
            for default_reviewer in trip_request.section.travel_default_reviewers.all():
                models.Reviewer.objects.get_or_create(trip_request=trip_request, user=default_reviewer.user, role_id=1)
        except (IntegrityError, KeyError):
            pass

        # section level recommender  - only applies if this is not the section head
        try:
            # if the division head is the one creating the request, the section head should be skipped as a recommender AND
            # if the section head is the one creating the request, they should be skipped as a recommender
            if trip_request.user != trip_request.section.head and trip_request.user != trip_request.section.division.head:
                models.Reviewer.objects.get_or_create(trip_request=trip_request, user=trip_request.section.head, role_id=2, )
        except (IntegrityError, AttributeError):
            pass
            # print("not adding section head")

        # division level recommender  - only applies if this is not the division manager
        try:
            # if the division head is the one creating the request, they should be skipped as a recommender
            if trip_request.user != trip_request.section.division.head:
                models.Reviewer.objects.get_or_create(trip_request=trip_request, user=trip_request.section.division.head, role_id=2, )
        except (IntegrityError, AttributeError):
            pass
            # print("not adding division manager")

        # Branch level reviewer - only applies if this is not the RDS
        try:
            if trip_request.user != trip_request.section.division.branch.head:
                # TODO: DOES THE BRANCH HAVE A DEFAULT REVIEWER?
                # add each default reviewer to the queue
                for default_reviewer in trip_request.section.division.branch.travel_default_reviewers.all():
                    models.Reviewer.objects.get_or_create(trip_request=trip_request, user=default_reviewer.user, role_id=1)

                if trip_request.section.division.branch.region_id == 2:
                    my_user = User.objects.get(pk=1102)
                    models.Reviewer.objects.get_or_create(trip_request=trip_request, user=my_user, role_id=1, )  # MAR RDSO ADMIN user
        except (IntegrityError, AttributeError, User.DoesNotExist):
            pass

        # Branch level recommender  - only applies if this is not the RDS
        try:
            if trip_request.user != trip_request.section.division.branch.head:
                models.Reviewer.objects.get_or_create(trip_request=trip_request, user=trip_request.section.division.branch.head,
                                                      role_id=2, )
        except (IntegrityError, AttributeError, User.DoesNotExist):
            pass
            # print("not adding RDS")

    # should the ADMs office be invovled?
    if trip_request.trip:
        if trip_request.trip.is_adm_approval_required:
            # add the ADMs office staff
            try:
                models.Reviewer.objects.get_or_create(trip_request=trip_request, user_id=626, role_id=5, )  # Arran McPherson
            except IntegrityError:
                pass
                # print("not adding NCR ADM")

    # finally, we always need to add the RDG
    try:
        models.Reviewer.objects.get_or_create(trip_request=trip_request, user=trip_request.section.division.branch.region.head, role_id=6, )
    except (IntegrityError, AttributeError):
        pass
        # print("not adding RDG")

    trip_request.save()


def start_review_process(trip_request):
    """this should be used when a trip is submitted. It will change over all reviewers' statuses to Pending"""
    # focus only on reviewers that are status = Not Submitted
    for reviewer in trip_request.reviewers.all():
        # set everyone to being queued
        reviewer.status_id = 20
        reviewer.status_date = None
        reviewer.save()


def end_review_process(trip_request):
    """this should be used when a project is unsubmitted. It will change over all reviewers' statuses to Pending"""
    # focus only on reviewers that are status = Not Submitted
    for reviewer in trip_request.reviewers.all():
        reviewer.status_id = 4
        reviewer.status_date = None
        reviewer.comments = None
        reviewer.save()


def start_trip_review_process(trip, reset=False):
    """this should be used when a project is submitted. It will change over all reviewers' statuses to Pending
        set the `reset` arg to True is this is being used in the context of restarting a review process
    """
    # focus only on reviewers that are status = Not Submitted
    if not reset:
        trip.review_start_date = timezone.now()
        trip.status_id = 31
        trip.save()

    for reviewer in trip.reviewers.all():
        # set everyone to being queued
        reviewer.status_id = 24
        if not reset:
            reviewer.status_date = None
        reviewer.save()


def end_trip_review_process(trip, reset=False):
    """this should be used when a project is unsubmitted. It will change over all reviewers' statuses to Pending
    set the `reset` arg to True is this is being used in the context of restarting a review process
    """
    # focus only on reviewers that are status = Not Submitted
    if not reset:
        # trip.review_start_date = None NEVER reset the review start date!
        trip.status_id = 41
        trip.save()

    for reviewer in trip.reviewers.all():
        reviewer.status_id = 23
        if not reset:
            reviewer.status_date = None
            reviewer.comments = None
        reviewer.save()


def reset_trip_review_process(trip):
    """To be used if a trip reviewer finds modifications that are required and wants to restart the review process. COMMENTS ARE SAVED"""
    # focus only on reviewers that are status = Not Submitted
    end_trip_review_process(trip, reset=True)
    start_trip_review_process(trip, reset=True)


def __set_request_status__(trip_request, request):
    """
    IF POSSIBLE, THIS SHOULD ONLY BE CALLED BY THE approval_seeker() function.
    This will look at the reviewers and decide on  what the project status should be. Will return False if trip_request is denied or if trip_request is not submitted
    """

    # first order of business, if the trip_request is status "changes requested' do not continue
    if trip_request.status_id == 16:
        return False

    # Next: if the trip_request is unsubmitted, it is in 'draft' status
    elif not trip_request.submitted:
        trip_request.status_id = 8
        # don't stick around any longer. save the trip_request and leave exit the function
        trip_request.save()
        return False

    else:
        # if someone denied it at any point, the trip_request is 'denied' and all subsequent reviewers are set to "cancelled"
        is_denied = False
        for reviewer in trip_request.reviewers.all():
            # if is_denied, all subsequent reviewer statuses should be set to "cancelled"
            if is_denied:
                reviewer.status_id = 5
                reviewer.save()

            # if reviewer status is denied, set the is_denied var to true
            if reviewer.status_id == 3:
                is_denied = True

        if is_denied:
            trip_request.status_id = 10
            trip_request.save()
            # send an email to the trip_request owner
            email = emails.StatusUpdateEmail(trip_request, request)
            # # send the email object
            custom_send_mail(
                subject=email.subject,
                html_message=email.message,
                from_email=email.from_email,
                recipient_list=email.to_list
            )

            # don't stick around any longer. save the trip_request and leave exit the function
            return False

        # The trip_request should be approved if everyone has approved it. HOWEVER, some reviewers might have been skipped
        # The total number of reviewers should equal the number of reviewer who approved [id=2] and / or were skipped [id=21].
        elif trip_request.reviewers.all().count() == trip_request.reviewers.filter(status_id__in=[2, 21]).count():
            trip_request.status_id = 11
            trip_request.save()
            # send an email to the trip_request owner
            email = emails.StatusUpdateEmail(trip_request)
            # # send the email object
            custom_send_mail(
                subject=email.subject,
                html_message=email.message,
                from_email=email.from_email,
                recipient_list=email.to_list
            )
            # don't stick around any longer. save the trip_request and leave exit the function
            return False
        else:
            for reviewer in trip_request.reviewers.all():
                # if a reviewer's status is 'pending', we are waiting on them and the project status should be set accordingly.
                if reviewer.status_id == 1:
                    # if role is 'reviewer'
                    if reviewer.role_id == 1:
                        trip_request.status_id = 17
                    # if role is 'recommender'
                    elif reviewer.role_id == 2:
                        trip_request.status_id = 12
                    # if role is 'ncr reviewer'
                    elif reviewer.role_id == 3:
                        trip_request.status_id = 18
                    # if role is 'ncr recommender'
                    elif reviewer.role_id == 4:
                        trip_request.status_id = 19
                    # if role is 'adm'
                    elif reviewer.role_id == 5:
                        trip_request.status_id = 14
                    # if role is 'rdg'
                    elif reviewer.role_id == 6:
                        trip_request.status_id = 15

    trip_request.save()
    return True


def approval_seeker(trip_request, suppress_email=False, request=None):
    """
    This method is meant to seek approvals via email + set reveiwer statuses.
    It will also set the trip_request status vis a vis __set_request_status__()

    """

    # start by setting the trip_request status... if the trip_request is "denied" OR "draft" or "approved", do not continue
    if __set_request_status__(trip_request, request):
        next_reviewer = None
        email = None
        for reviewer in trip_request.reviewers.all():
            # if the reviewer's status is set to 'queued', they will be our next selection
            # we should then exit the loop and set the next_reviewer var

            # if this is a resubmission, there might still be a reviewer whose status is 'pending'. This should be the reviewer
            if reviewer.status_id == 20 or reviewer.status_id == 1:
                next_reviewer = reviewer
                break

        # if there is a next reviewer, set their status to pending
        if next_reviewer:
            next_reviewer.status_id = 1
            next_reviewer.status_date = timezone.now()
            next_reviewer.save()

            # now, depending on the role of this reviewer, perhaps we want to send an email.
            # if they are a recommender, rev...
            if next_reviewer.role_id in [1, 2, 3, 4, ] and request:  # essentially, just not the RDG or ADM
                email = emails.ReviewAwaitingEmail(trip_request, next_reviewer, request)

            elif next_reviewer.role_id in [5, 6]  and request:  # if we are going for ADM or RDG signature...
                email = emails.AdminApprovalAwaitingEmail(trip_request, next_reviewer.role_id, request)

            if email and not suppress_email:
                # send the email object
                custom_send_mail(
                    subject=email.subject,
                    html_message=email.message,
                    from_email=email.from_email,
                    recipient_list=email.to_list
                )

            # Then, lets set the trip_request status again to account for the fact that something happened
            __set_request_status__(trip_request, request)


def populate_trip_request_costs(request, trip_request):
    # determine if we are dealing with a child trip request - used to prepopulate number of days
    if trip_request.parent_request:
        trip = trip_request.parent_request.trip
    else:
        trip = trip_request.trip

    for obj in models.Cost.objects.all():
        new_item, created = models.TripRequestCost.objects.get_or_create(
            trip_request=trip_request,
            cost=obj,
            # number_of_days=trip.number_of_days,
        )
        if created:
            # breakfast
            if new_item.cost_id == 9:
                try:
                    new_item.rate_cad = models.NJCRates.objects.get(pk=1).amount
                    new_item.save()
                except models.NJCRates.DoesNotExist:
                    messages.warning(request,
                                     _("NJC rates for breakfast missing from database. Please let your system administrator know."))
            # lunch
            elif new_item.cost_id == 10:
                try:
                    new_item.rate_cad = models.NJCRates.objects.get(pk=2).amount
                    new_item.save()
                except models.NJCRates.DoesNotExist:
                    messages.warning(request, _("NJC rates for lunch missing from database. Please let your system administrator know."))
            # supper
            elif new_item.cost_id == 11:
                try:
                    new_item.rate_cad = models.NJCRates.objects.get(pk=3).amount
                    new_item.save()
                except models.NJCRates.DoesNotExist:
                    messages.warning(request, _("NJC rates for supper missing from database. Please let your system administrator know."))
            # incidentals
            elif new_item.cost_id == 12:
                try:
                    new_item.rate_cad = models.NJCRates.objects.get(pk=4).amount
                    new_item.save()
                except models.NJCRates.DoesNotExist:
                    messages.warning(request,
                                     _("NJC rates for incidentals missing from database. Please let your system administrator know."))

    # messages.success(request, _("All costs have been added to this project."))


def clear_empty_trip_request_costs(trip_request):
    for obj in models.Cost.objects.all():
        for cost in models.TripRequestCost.objects.filter(trip_request=trip_request, cost=obj):
            if (cost.amount_cad is None or cost.amount_cad == 0):
                cost.delete()


def compare_strings(str1, str2):
    def __strip_string__(string):
        return str(string.lower().replace(" ", "").split(",")[0])

    try:
        return distance(__strip_string__(str1), __strip_string__(str2))
    except AttributeError:
        return 9999


def manage_trip_warning(trip, request):
    """
    This function will decide if sending an email to NCR is necessary based on
    1) the total costs accrued for a trip
    2) whether or not a warning has already been sent

    :param trip: an instance of Trip
    :return: NoneObject
    """

    # first make sure we are not receiving a NoneObject
    try:
        trip.non_res_total_cost
    except AttributeError:
        pass
    else:

        # If the trip cost is below 10k, make sure the warning field is null and an then do nothing more :)
        if trip.non_res_total_cost < 10000:
            if trip.cost_warning_sent:
                trip.cost_warning_sent = None
                trip.save()

        # if the trip is >= 10K, we simply need to send an email to NCR
        else:
            if not trip.cost_warning_sent:
                email = emails.TripCostWarningEmail(trip, request)
                # # send the email object
                custom_send_mail(
                    subject=email.subject,
                    html_message=email.message,
                    from_email=email.from_email,
                    recipient_list=email.to_list
                )
                trip.cost_warning_sent = timezone.now()
                trip.save()


def __set_trip_status__(trip):
    """
    IF POSSIBLE, THIS SHOULD ONLY BE CALLED BY THE approval_seeker() function.
    This will look at the reviewers and decide on  what the project status should be. Will return False if trip_request is denied or if trip_request is not submitted
    Will return False if there are no reviewers left to seek
    """
    pass


def trip_approval_seeker(trip, request):
    """
    This method is meant to seek approvals via email + set reviewer statuses.
    """

    # start by setting the trip status... if the trip_request is "denied" OR "draft" or "approved", do not continue
    # Next: if the trip_request is un submitted, it is in 'draft' status

    # only look for a next reviewer if we are still in a review [id=31]
    if trip.status_id == 31:

        next_reviewer = None
        email = None

        # look through all the reviewers... see if we can decide on who the next reviewer should be...
        for reviewer in trip.reviewers.all():
            # if the reviewer's status is set to 'queued', they will be our next selection
            # we should then exit the loop and set the next_reviewer var
            # CAVEAT: if this is a resubmission, there might still be a reviewer whose status is 'pending'. This should be the reviewer
            if reviewer.status_id == 24 or reviewer.status_id == 25:
                next_reviewer = reviewer
                break

        # if there is a next reviewer, set their status to pending and send them an email
        if next_reviewer:
            next_reviewer.status_id = 25
            next_reviewer.status_date = timezone.now()
            next_reviewer.save()

            email = emails.TripReviewAwaitingEmail(trip, next_reviewer, request)

            # send the email object
            custom_send_mail(
                subject=email.subject,
                html_message=email.message,
                from_email=email.from_email,
                recipient_list=email.to_list
            )


        # if no next reviewer was found, the trip's review is complete...
        else:
            # THIS IS PROBABLY NOT NECESSARY.

            # The trip review is complete if all the reviewers' status are set to complete [id=26]
            # HOWEVER, some reviewers might have been skipped
            # The total number of reviewers should equal the number of reviewer who completed [id=26] and / or were skipped [id=42].
            if trip.reviewers.all().count() == trip.reviewers.filter(status_id__in=[26, 42]).count():
                trip.status_id = 32
                trip.save()


def get_related_trips(user):
    """give me a user and I'll send back a queryset with all related trips, i.e.
     they are the request.user | they are the request.created_by | they are a traveller on a child trip"""

    # all individual or group requests where user =user (this should include parent requests)
    tr_ids = [tr.id for tr in models.TripRequest.objects.filter(parent_request__isnull=True, user=user)]
    # all trips that were created by user
    tr_ids.extend([tr.id for tr in models.TripRequest.objects.filter(parent_request__isnull=True, created_by=user)])
    # all trips where the user is a traveller on a group trip
    tr_ids.extend([tr.parent_request.id for tr in models.TripRequest.objects.filter(parent_request__isnull=False, user=user)])
    return models.TripRequest.objects.filter(id__in=tr_ids)


def get_adm_eligible_trips():
    """returns a qs of trips that are ready for adm review"""
    # start with trips that need adm approval that have not already been reviewed or those that have been cancelled
    trips = models.Conference.objects.filter(is_adm_approval_required=True).filter(~Q(status_id__in=[32, 43, 31]))

    t_ids = list()
    for t in trips:
        # only get trips that have attached requests
        if t.get_connected_active_requests().count():
            # only get trips that are within three months from the closest date
            if t.date_eligible_for_adm_review and t.date_eligible_for_adm_review <= timezone.now():
                t_ids.append(t.id)
    return models.Conference.objects.filter(id__in=t_ids)
