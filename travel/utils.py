from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User

from dm_apps.utils import custom_send_mail
from django.db import IntegrityError
from django.utils import timezone
from django.utils.translation import gettext as _
from Levenshtein import distance

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
    """this should be used when a project is submitted. It will change over all reviewers' statuses to Pending"""
    # focus only on reviewers that are status = Not Submitted
    for reviewer in trip_request.reviewers.all():
        # set everyone to being queued
        reviewer.status_id = 20
        reviewer.status_date = None
        reviewer.save()


def start_trip_review_process(trip):
    """this should be used when a project is submitted. It will change over all reviewers' statuses to Pending"""
    # focus only on reviewers that are status = Not Submitted
    for reviewer in trip.reviewers.all():
        # set everyone to being queued
        reviewer.status_id = 24
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


def end_trip_review_process(trip):
    """this should be used when a project is unsubmitted. It will change over all reviewers' statuses to Pending"""
    # focus only on reviewers that are status = Not Submitted
    for reviewer in trip.reviewers.all():
        reviewer.status_id = 23
        reviewer.status_date = None
        reviewer.comments = None
        reviewer.save()


def set_request_status(trip_request):
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
            # if reviewer status is denied, set the is_denied var to true
            if reviewer.status_id == 3:
                is_denied = True
            # if is_denied, all subsequent reviewer statuses should be set to "cancelled"
            if is_denied:
                reviewer.status_id = 5
                reviewer.save()
        if is_denied:
            trip_request.status_id = 10
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


def approval_seeker(trip_request):
    """
    This method is meant to seek approvals via email + set reveiwer statuses.
    It will also set the trip_request status vis a vis set_request_status()

    """

    # start by setting the trip_request status... if the trip_request is "denied" OR "draft" or "approved", do not continue
    if set_request_status(trip_request):
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
            if next_reviewer.role_id in [1, 2, 3, 4, ]:  # essentially, just not the RDG or ADM
                email = emails.ReviewAwaitingEmail(trip_request, next_reviewer)

            elif next_reviewer.role_id in [5, 6]:  # if we are going for ADM or RDG signature...
                email = emails.AdminApprovalAwaitingEmail(trip_request, next_reviewer.role_id)

            if email:
                # send the email object
                custom_send_mail(
                    subject=email.subject,
                    html_message=email.message,
                    from_email=email.from_email,
                    recipient_list=email.to_list
                )

            # Then, lets set the trip_request status again to account for the fact that something happened
            set_request_status(trip_request)


def populate_trip_request_costs(request, trip_request):
    for obj in models.Cost.objects.all():
        new_item, created = models.TripRequestCost.objects.get_or_create(trip_request=trip_request, cost=obj)
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

    messages.success(request, _("All costs have been added to this project."))


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


def manage_trip_warning(trip):
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
                email = emails.TripCostWarningEmail(trip)
                # # send the email object
                custom_send_mail(
                    subject=email.subject,
                    html_message=email.message,
                    from_email=email.from_email,
                    recipient_list=email.to_list
                )
                trip.cost_warning_sent = timezone.now()
                trip.save()


def set_trip_status(trip):
    """
    IF POSSIBLE, THIS SHOULD ONLY BE CALLED BY THE approval_seeker() function.
    This will look at the reviewers and decide on  what the project status should be. Will return False if trip_request is denied or if trip_request is not submitted
    """

    # Next: if the trip_request is unsubmitted, it is in 'draft' status
    if not trip_request.submitted:
        trip_request.status_id = 8
        # don't stick around any longer. save the trip_request and leave exit the function
        trip_request.save()
        return False

    else:
        # if someone denied it at any point, the trip_request is 'denied' and all subsequent reviewers are set to "cancelled"
        is_denied = False
        for reviewer in trip.reviewers.all():
            # if reviewer status is denied, set the is_denied var to true
            if reviewer.status_id == 27:
                is_denied = True
            # if is_denied, all subsequent reviewer statuses should be set to "cancelled"
            if is_denied:
                reviewer.status_id = 5
                reviewer.save()
        if is_denied:
            trip.status_id = 10
            trip.save()
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


def trip_approval_seeker(trip):
    """
    This method is meant to seek approvals via email + set reveiwer statuses.
    It will also set the trip_request status vis a vis set_request_status()
    """

    # start by setting the trip_request status... if the trip_request is "denied" OR "draft" or "approved", do not continue
    if set_trip_status(trip):
        next_reviewer = None
        email = None
        for reviewer in trip.reviewers.all():
            # if the reviewer's status is set to 'queued', they will be our next selection
            # we should then exit the loop and set the next_reviewer var

            # if this is a resubmission, there might still be a reviewer whose status is 'pending'. This should be the reviewer
            if reviewer.status_id == 24 or reviewer.status_id == 25:
                next_reviewer = reviewer
                break

        # if there is a next reviewer, set their status to pending
        if next_reviewer:
            next_reviewer.status_id = 25
            next_reviewer.status_date = timezone.now()
            next_reviewer.save()

            # now, depending on the role of this reviewer, perhaps we want to send an email.
            # if they are a recommender, rev...
            email = emails.TripReviewAwaitingEmail(trip, next_reviewer)

            if email:
                # send the email object
                custom_send_mail(
                    subject=email.subject,
                    html_message=email.message,
                    from_email=email.from_email,
                    recipient_list=email.to_list
                )

            # Then, lets set the trip_request status again to account for the fact that something happened
            set_trip_status(trip)
