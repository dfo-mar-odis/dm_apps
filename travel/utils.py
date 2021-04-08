from collections import OrderedDict
from copy import deepcopy

from azure.storage.blob import BlockBlobService
from decouple import config
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import Group
from django.db.models import Q
from django.template.defaultfilters import date
from django.utils import timezone
from django.utils.translation import gettext as _
from msrestazure.azure_active_directory import MSIAuthentication

from shared_models import models as shared_models
from . import emails
from . import models


def in_travel_admin_group(user):
    # make sure the following group exist:
    admin_group, created = Group.objects.get_or_create(name="travel_admin")
    if user:
        return admin_group in user.groups.all()


def in_adm_admin_group(user):
    # make sure the following group exist:
    admin_group, created = Group.objects.get_or_create(name="travel_adm_admin")
    if user:
        return admin_group in user.groups.all()


def is_admin(user):
    return in_adm_admin_group(user) or in_travel_admin_group(user)


def is_approver(user, trip_request):
    """ only for when reviewer status is pending and request status is active"""
    return get_related_request_reviewers(user).filter(request_id=trip_request.id).exists()


def is_adm(user):
    try:
        if hasattr(user, "travel_default_reviewers") and user.travel_default_reviewers.special_role == 5:
            return True
        national_region = shared_models.Region.objects.get(name__icontains="national")
        if user == national_region.head:
            return True
    except Exception as ex:
        print("Cannot find region named: 'national'", ex)


def is_trip_approver(user, trip):
    if trip.current_reviewer and user == trip.current_reviewer.user:
        return True


def can_modify_request(user, trip_request_id, request_to_unsubmit=False, as_dict=False):
    """
    returns True if user has permissions to delete or modify a request

    The answer of this question will depend on whether the trip is submitted.
    owners cannot edit a submitted trip

    :param user:
    :param trip_request_id:
    :param request_to_unsubmit: Is this a request to unsubmit? If so, the permissions are a little different.
    :param as_dict: return as dict (with result and reason) as opposed to boolean
    :return: dict or bool
    """
    if user.id:
        my_request = models.TripRequest.objects.get(pk=trip_request_id)

        reason = None
        result = False

        # if the request is unsubmitted, the owner can edit
        if not my_request.submitted and my_request in user.travel_requests_created_by.all():
            result = True
            reason = _("You can edit this record because you are the request owner.")

        elif not my_request.submitted and my_request in models.TripRequest.objects.filter(travellers__user=user):
            result = True
            reason = _("You can edit this record because you are a traveller on this request.")

        elif request_to_unsubmit and my_request in user.travel_requests_created_by.all():
            result = True
            reason = _("You can un-submit this request because you are the request owner.")

        # check to see if they are the active reviewer
        elif get_related_request_reviewers(user).filter(request_id=trip_request_id).exists():
            result = True
            reason = _("You can edit this record because you are the active reviewer for this request.")

        # check to see if they are the RDS
        elif user == my_request.section.division.branch.head:
            result = True
            reason = _("You can edit this record because you are the Regional director / NCR Director General.")

        # check to see if a travel_admin or ADM admin
        elif in_adm_admin_group(user):
            result = True
            reason = _("You can edit this record because you are in the NCR National Coordinator Group.")

        elif in_travel_admin_group(user):
            result = True
            reason = _("You can edit this record because you are in the Regional Administrator Group.")

        if as_dict:
            return dict(can_modify=result, reason=reason)
        else:
            return result


def get_section_choices(all=False, full_name=True):
    if full_name:
        my_attr = "full_name"
    else:
        my_attr = _("name")

    if not all:
        return [(s.id, getattr(s, my_attr)) for s in
                shared_models.Section.objects.filter(requests__isnull=False).order_by(
                    "division__branch__region",
                    "division__branch",
                    "division",
                    "name"
                )]
    else:
        return [(s.id, getattr(s, my_attr)) for s in
                shared_models.Section.objects.all()]


def get_division_choices(all=False):
    if all:
        return [(d.id, str(d)) for d in shared_models.Division.objects.all()]
    else:
        return [(d.id, str(d)) for d in
                shared_models.Division.objects.filter(sections__in=shared_models.Section.objects.filter(requests__isnull=False)).distinct()]


def get_region_choices(all=False):
    if all:
        return [(r.id, str(r)) for r in shared_models.Region.objects.all()]
    else:
        # return [(d.id, str(d)) for d in shared_models.Region.objects.all()]
        return [(r.id, str(r)) for r in
                shared_models.Region.objects.filter(branches__divisions__sections__in=shared_models.Section.objects.filter(
                    requests__isnull=False)).distinct()]


def get_trip_reviewers(trip):
    """add reviewers to a trip is adm approval is required. If it isn't, it will remove all reviewers from the trip (if present)"""
    # This section only matters for ADM trips

    if trip.is_adm_approval_required:
        # NCR travel coordinator(3), ADM Recommender(4), ADM (5)
        roles = [3, 4, 5]
        for role in roles:
            for default_reviewer in models.DefaultReviewer.objects.filter(special_role=role).order_by("order"):
                models.TripReviewer.objects.get_or_create(trip=trip, user=default_reviewer.user, role=role)

    else:
        trip.reviewers.all().delete()
    trip.save()


def get_request_reviewers(trip_request):
    """
    - NCR coordinator (if LATE --> handled by submit on_valid method)
    - SPECIAL OPTIONAL INSERTs --> pre-section
    - section admin
    - section head
    - SPECIAL OPTIONAL INSERTs --> pre-division
    - div head
    - SPECIAL OPTIONAL INSERTs --> pre-branch
    - branch admin
    - branch head
    - ADM  --> THIS IS ACHIEVED INDIRECTLY THROUGH TRIP REVIEW
    - Expenditure Initiation --> this step follows back tot the branch admin
    """

    if trip_request.section:
        travellers = trip_request.travellers.filter(user__isnull=False)

        # SPECIAL OPTIONAL INSERTS --> pre-section
        ############################################
        # add each default reviewer to the queue
        for default_reviewer in trip_request.section.travel_default_reviewers.order_by("order"):
            models.Reviewer.objects.get_or_create(request=trip_request, user=default_reviewer.user, role=1)

        # section admin
        ###############
        if trip_request.section.admin:
            models.Reviewer.objects.get_or_create(request=trip_request, user=trip_request.section.admin, role=1)

        # section head
        ##############
        # if the division head is the one creating the request, the section head should be skipped as a recommender AND
        # if the section head is the one creating the request, they should be skipped as a recommender
        if trip_request.section.head and trip_request.section.head not in [t.user for t in travellers] and \
                trip_request.section.division.head not in [t.user for t in travellers]:
            models.Reviewer.objects.get_or_create(request=trip_request, user=trip_request.section.head, role=2)

        # SPECIAL OPTIONAL INSERTS --> pre-division
        ############################################
        # add each default reviewer to the queue
        for default_reviewer in trip_request.section.division.travel_default_reviewers.order_by("order"):
            models.Reviewer.objects.get_or_create(request=trip_request, user=default_reviewer.user, role=1)

        # division manager
        ###################
        # if the division head is the one creating the request, they should be skipped as a recommender
        if trip_request.section.division.head and trip_request.section.division.head not in [t.user for t in travellers]:
            models.Reviewer.objects.get_or_create(request=trip_request, user=trip_request.section.division.head, role=2)

        # SPECIAL OPTIONAL INSERTS --> pre-branch
        ############################################
        # add each default reviewer to the queue
        for default_reviewer in trip_request.section.division.branch.travel_default_reviewers.order_by("order"):
            models.Reviewer.objects.get_or_create(request=trip_request, user=default_reviewer.user, role=1)

        # rds admin
        ###############
        if trip_request.section.division.branch.admin:
            models.Reviewer.objects.get_or_create(request=trip_request, user=trip_request.section.division.branch.admin, role=1)

        # RDS
        #####
        if trip_request.section.division.branch.head and trip_request.section.division.branch.head not in [t.user for t in travellers]:
            models.Reviewer.objects.get_or_create(request=trip_request, user=trip_request.section.division.branch.head, role=2, )

        # ADM
        #####
        if trip_request.trip.is_adm_approval_required:
            # the ADM is head of the National Branch.
            national_branch = shared_models.Region.objects.filter(name__icontains="national")
            if national_branch.exists():
                national_branch = national_branch.first()
                if national_branch.head:
                    models.Reviewer.objects.get_or_create(request=trip_request, user=national_branch.head, role=5)
            else:
                adm_special_reviewer = models.DefaultReviewer.objects.filter(special_role=5).first()
                if adm_special_reviewer:
                    models.Reviewer.objects.get_or_create(request=trip_request, user=adm_special_reviewer.user, role=5)

        # RDG / Expenditure Initiation #
        ################################

        # only do this if the trip is NOT virtual!
        if not trip_request.trip.is_virtual:
            # IF domestic travel ("domestic travel and continental USA travel") AND if there is an expenditure initial approver
            ## Note: we are using the ADM approval required field as a proxy for domestic travel
            region_expenditure_initiation_qs = trip_request.section.division.branch.region.travel_default_reviewers.all()
            if not trip_request.trip.is_adm_approval_required and region_expenditure_initiation_qs.exists():
                r, created = models.Reviewer.objects.get_or_create(request=trip_request, user=region_expenditure_initiation_qs.first().user, role=6)
                # if at this point, we should check if the trip is adm approval required. If it is not, there is a good change the final approver is showing
                # up as both recommender and final approver. If so, we should delete this person as a recommender
                if trip_request.reviewers.filter(user=r.user, role=2).exists():
                    trip_request.reviewers.filter(user=region_expenditure_initiation_qs.first().user, role=2).first().delete()
            elif trip_request.section.division.branch.region.head:
                models.Reviewer.objects.get_or_create(request=trip_request, user=trip_request.section.division.branch.region.head, role=7)

        # ensure the process order makes sense
        count = 1
        for r in trip_request.reviewers.order_by('id'):  # sort by id since this will correspond to order of creation
            r.order = count
            r.save()
            count += 1


def start_request_review_process(trip_request):
    """this should be used when a trip is submitted. It will change over all reviewers' statuses to Pending"""
    # focus only on reviewers that are status = Not Submitted
    for reviewer in trip_request.reviewers.all():
        # set everyone to being queued
        reviewer.status = 20
        reviewer.status_date = None
        reviewer.save()


def end_request_review_process(trip_request):
    """this should be used when a project is unsubmitted. It will change over all reviewers' statuses to Pending"""
    # focus only on reviewers that are status = Not Submitted
    for reviewer in trip_request.reviewers.all():
        reviewer.status = 4
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
        trip.status = 31
        trip.save()

    for reviewer in trip.reviewers.all():
        # set everyone to being queued
        reviewer.status = 24
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
        trip.status = 41
    else:
        trip.status = 31
    trip.save()

    for reviewer in trip.reviewers.all():
        if not reset:
            reviewer.status = 23
            reviewer.status_date = None
            reviewer.comments = None
        else:
            reviewer.status = 24
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
    if trip_request.status == 16:
        return False

    # Next: if the trip_request is unsubmitted, it is in 'draft' status
    elif not trip_request.submitted:
        trip_request.status = 8
        # don't stick around any longer. save the trip_request and leave exit the function
        trip_request.save()
        return False

    else:
        # if someone denied it at any point, the trip_request is 'denied' and all subsequent reviewers are set to "cancelled"
        is_denied = False
        for reviewer in trip_request.reviewers.all():
            # if is_denied, all subsequent reviewer statuses should be set to "cancelled"
            if is_denied:
                reviewer.status = 5
                reviewer.save()

            # if reviewer status is denied, set the is_denied var to true
            if reviewer.status == 3:
                is_denied = True

        if is_denied:
            trip_request.status = 10
            trip_request.save()
            # send an email to the trip_request owner
            email = emails.StatusUpdateEmail(request, trip_request)
            email.send()

            # don't stick around any longer. save the trip_request and leave exit the function
            return False

        # The trip_request should be approved if everyone has approved it. HOWEVER, some reviewers might have been skipped
        # The total number of reviewers should equal the number of reviewer who approved [id=2] and / or were skipped [id=21].
        elif trip_request.reviewers.all().count() == trip_request.reviewers.filter(status__in=[2, 21]).count():
            trip_request.status = 11
            trip_request.save()
            # send an email to the trip_request owner
            email = emails.StatusUpdateEmail(request, trip_request)
            email.send()
            # don't stick around any longer. save the trip_request and leave exit the function
            return False
        else:
            for reviewer in trip_request.reviewers.all():
                # if a reviewer's status is 'pending', we are waiting on them and the project status should be set accordingly.
                if reviewer.status == 1:
                    # if role is 'reviewer'
                    if reviewer.role == 1:
                        trip_request.status = 17
                    # if role is 'recommender'
                    elif reviewer.role == 2:
                        trip_request.status = 12
                    # if role is 'ncr reviewer'
                    elif reviewer.role == 3:
                        trip_request.status = 17
                    # if role is 'ncr recommender'
                    elif reviewer.role == 4:
                        trip_request.status = 12
                    # if role is 'adm'
                    elif reviewer.role == 5:
                        trip_request.status = 14
                    # if role is 'rdg' or 'expenditure initiation'
                    elif reviewer.role in [6, 7]:
                        trip_request.status = 15

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
            if reviewer.status == 20 or reviewer.status == 1:
                next_reviewer = reviewer
                break

        # if there is a next reviewer, set their status to pending
        if next_reviewer:
            next_reviewer.status = 1
            next_reviewer.status_date = timezone.now()
            next_reviewer.save()

            # now, depending on the role of this reviewer, perhaps we want to send an email.
            # if they are a recommender, rev...
            if next_reviewer.role in [1, 2, 3, 4, 6, ] and request:  # essentially, just not the RDG or ADM
                email = emails.ReviewAwaitingEmail(request, trip_request, next_reviewer)

            elif next_reviewer.role in [7, ] and request:  # if we are going for RDG signature...
                email = emails.RDGReviewAwaitingEmail(request, trip_request, next_reviewer)

            if email and not suppress_email:
                # send the email object
                email.send()

            # Then, lets set the trip_request status again to account for the fact that something happened
            __set_request_status__(trip_request, request)


def populate_traveller_costs(request, traveller):
    for obj in models.Cost.objects.all():
        new_item, created = models.TravellerCost.objects.get_or_create(traveller=traveller, cost=obj)
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


def clear_empty_traveller_costs(traveller):
    for obj in models.Cost.objects.all():
        for cost in models.TravellerCost.objects.filter(traveller=traveller, cost=obj):
            if (cost.amount_cad is None or cost.amount_cad == 0):
                cost.delete()


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
                email = emails.TripCostWarningEmail(request, trip)
                email.send()
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
    if trip.status == 31:

        next_reviewer = None
        email = None

        # look through all the reviewers... see if we can decide on who the next reviewer should be...
        for reviewer in trip.reviewers.all():
            # if the reviewer's status is set to 'queued', they will be our next selection
            # we should then exit the loop and set the next_reviewer var
            # CAVEAT: if this is a resubmission, there might still be a reviewer whose status is 'pending'. This should be the reviewer
            if reviewer.status == 24 or reviewer.status == 25:
                next_reviewer = reviewer
                break

        # if there is a next reviewer, set their status to pending and send them an email
        if next_reviewer:
            next_reviewer.status = 25
            next_reviewer.status_date = timezone.now()
            next_reviewer.save()

            email = emails.TripReviewAwaitingEmail(request, trip, next_reviewer)
            # send the email object
            email.send()


        # if no next reviewer was found, the trip's review is complete...
        else:
            # THIS IS PROBABLY NOT NECESSARY.

            # The trip review is complete if all the reviewers' status are set to complete [id=26]
            # HOWEVER, some reviewers might have been skipped
            # The total number of reviewers should equal the number of reviewer who completed [id=26] and / or were skipped [id=42].
            if trip.reviewers.all().count() == trip.reviewers.filter(status__in=[26, 42]).count():
                trip.status = 32
                trip.save()


def get_related_requests(user):
    """give me a user and I'll send back a queryset with all related trip requests, i.e.
     they are a traveller || they are the request.created_by"""
    qs = models.TripRequest.objects.filter(Q(created_by=user) | Q(travellers__user=user)).distinct()
    return qs


def get_related_request_reviewers(user):
    """give me a user and I'll send back a queryset with all related trips request reviews that are actionable (pending)
     (excluding drafts (8), ADM approval (14) and when changes have already been requested (16)"""
    qs = models.Reviewer.objects.filter(status=1).filter(~Q(request__status__in=[16, 14, 8]), user=user).distinct()
    return qs


def get_related_trip_reviewers(user):
    """give me a user and I'll send back a queryset with all related trips reviews that are actionable (pending = 25)
     """
    qs = models.TripReviewer.objects.filter(status=25, user=user)
    return qs


def get_adm_eligible_trips():
    """returns a qs of trips that are ready for adm review"""
    # start with trips that need adm approval that have not already been reviewed or those that have been cancelled
    trips = models.Trip.objects.filter(is_adm_approval_required=True).filter(~Q(status__in=[32, 43, 31]))

    keepers = list()
    for t in trips:
        # only get trips that have attached travellers and that are in an active status (i.e. not draft=8, cancelled=22, denied=10)
        # (the trip.travellers prop is handling this filtering!)
        if t.travellers.exists():
            # only get trips that are within three months from the closest date
            if t.date_eligible_for_adm_review and t.date_eligible_for_adm_review <= timezone.now():
                keepers.append(t.id)
    return models.Trip.objects.filter(id__in=keepers).order_by("adm_review_deadline")


user_attr_list = [
    "shared_models_regions",
    "shared_models_admin_regions",
    "shared_models_branches",
    "shared_models_admin_branches",
    "shared_models_divisions",
    "shared_models_admin_divisions",
    "shared_models_sections",
    "shared_models_admin_sections",
]


def is_manager_or_assistant_or_admin(user):
    # start high and go low
    if is_admin(user):
        return True

    for attr in user_attr_list:
        if getattr(user, attr).exists():
            return True


def get_requests_with_managerial_access(user):
    queryset = models.TripRequest.objects.all()
    if is_admin(user):
        return queryset
    else:
        qs = queryset.filter(Q(section__admin=user) | Q(section__head=user)
                             | Q(section__division__admin=user) | Q(section__division__head=user)
                             | Q(section__division__branch__admin=user) | Q(section__division__branch__head=user)
                             | Q(section__division__branch__region__admin=user) | Q(section__division__branch__region__head=user))
        return qs


def upload_to_azure_blob(target_file_path, target_file):
    AZURE_STORAGE_ACCOUNT_NAME = settings.AZURE_STORAGE_ACCOUNT_NAME
    AZURE_MSI_CLIENT_ID = config("AZURE_MSI_CLIENT_ID", cast=str, default="")
    account_key = config("AZURE_STORAGE_SECRET_KEY", default=None)
    try:
        token_credential = MSIAuthentication(resource=f'https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net', client_id=AZURE_MSI_CLIENT_ID)
    except Exception as E:
        print(E)
        token_credential = None
    blobService = BlockBlobService(account_name=AZURE_STORAGE_ACCOUNT_NAME, token_credential=token_credential, account_key=account_key)
    blobService.create_blob_from_path('media', target_file, target_file_path)


def get_cost_comparison(travellers):
    """
    This method is used to return a dictionary of trip requests and will compare cost across all of them.
    """
    costs = models.TravellerCost.objects.filter(traveller__in=travellers, amount_cad__gt=0).values("cost").order_by("cost").distinct()
    header = [models.Cost.objects.get(pk=c["cost"]).tname for c in costs]
    cost_totals = OrderedDict()
    for c in costs:
        cost_totals[c["cost"]] = 0
    header.insert(0, _("Name"))
    header.append(_("Total"))
    list1 = [header, ]
    # get all travellers from active requests
    total = 0
    for t in travellers.all():
        name = t.smart_name
        if t.is_research_scientist:
            name += " (RES)"
        list2 = [name, ]
        traveller_total = 0
        for cost in costs:
            try:
                c = models.TravellerCost.objects.get(traveller=t, cost_id=cost['cost'])
                val = c.amount_cad
                cost_totals[c.cost.id] += c.amount_cad
                traveller_total += c.amount_cad
                total += c.amount_cad
            except Exception as e:
                val = 0
            list2.append(val)
        list2.append(traveller_total)
        list1.append(list2)

    total_row = [cost_totals[c["cost"]] for c in costs]
    total_row.insert(0, "TOTAL")
    total_row.append(total)
    list1.append(total_row)
    return list1


def cherry_pick_traveller(traveller, request, comment="approved / approuvé"):
    """this is a special function that is to be used by the ADM only.
    It is for when the ADM wants to approve a single traveller while not approving the entire delegation.
    Validation will be handled by views"""
    trip_request = traveller.request
    # scenario 1: this is a single person request (yayy!!)
    if trip_request.travellers.count() == 1:
        reviewer = trip_request.current_reviewer
        reviewer.user = request.user
        reviewer.comments = comment
        reviewer.status = 2
        reviewer.status_date = timezone.now()
        reviewer.save()
        approval_seeker(trip_request, False, request)
    else:
        # scenario 2: they are being cherry picked out of a group request
        # make a copy of the original request (include a copy of the reviewers)
        old_obj = trip_request
        new_obj = deepcopy(old_obj)
        new_obj.pk = None
        new_obj.save()

        # copy over the reviewers
        for old_rel_obj in old_obj.reviewers.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.request = new_obj
            new_rel_obj.save()

        # move traveller over to the new request
        traveller.request = new_obj
        traveller.save()
        old_obj.add_admin_note = f"{date(timezone.now())} - {traveller.smart_name} was automatically transferred to a separate request during" \
                                 f" the course of the ADM-level review."

        # finally, we approved the new request at the level of the active reviewer
        reviewer = new_obj.current_reviewer
        reviewer.user = request.user
        reviewer.comments = comment
        reviewer.status = 2
        reviewer.status_date = timezone.now()
        reviewer.save()
        approval_seeker(new_obj, False, request)


def get_trip_field_list(trip=None):
    my_list = [
        'tname|{}'.format(_("Name")),
        'location',
        'trip_subcategory',
        'lead',
        'has_event_template',
        'number',
        'start_date',
        'end_date',
        'meeting_url',
        'abstract_deadline',
        'registration_deadline',
        'is_adm_approval_required',
        'notes',
    ]

    while None in my_list: my_list.remove(None)
    return my_list
