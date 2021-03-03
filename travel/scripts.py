import os

from django.contrib.auth.models import User
from django.core import serializers
from django.core.files import File
from django.utils import timezone

from lib.functions.custom_functions import listrify
from shared_models.models import Organization
from . import models
from . import utils


# def remove_empty_trips():
#     for trip in models.Trip.objects.all():
#         if trip.trip_requests.count() == 0:
#             trip.delete()
#


def resave_requests():
    for obj in models.TripRequest.objects.all():
        obj.save()


def find_and_save_virtual_trips():
    for obj in models.Trip.objects.filter(location__icontains="virtu"):
        obj.is_virtual = True
        obj.save()

def reset_trip_reviewers():
    for trip in models.Trip.objects.filter(is_adm_approval_required=True):
        if trip.reviewers.count() == 0:
            utils.get_trip_reviewers(trip)


def check_trip_purposes():
    print(f"trip id; trip name; purposes")
    for trip in models.Trip.objects.all():
        if trip.trip_requests.count():
            print(f"{trip.id}; {trip.name}; {listrify([tr.purpose.name for tr in trip.trip_requests.all() if tr.purpose])}")


def export_fixtures():
    """ a simple function to expor the important lookup tables. These fixutre will be used for testing and also for seeding new instances"""
    fixtures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
    models_to_export = [
        models.NJCRates,
        models.CostCategory,
        models.Cost,
        models.Role,
        models.Purpose,
        models.Status,
        models.TripCategory,
        models.TripSubcategory,
        # models.ReviewerRole,
        # models.HelpText,
        # shared_models.FiscalYear,
        # shared_models.Region,
        # shared_models.Branch,
        # shared_models.Division,
        # shared_models.Section,
        # models.DefaultReviewer,
        # User,
        # Group,
    ]
    for model in models_to_export:
        data = serializers.serialize("json", model.objects.all())
        my_label = model._meta.db_table
        f = open(os.path.join(fixtures_dir, f'{my_label}.json'), 'w')
        myfile = File(f)
        myfile.write(data)
        myfile.close()


def update_conf_status():
    conf_list = models.Trip.objects.all()
    for obj in conf_list:
        if obj.is_verified:
            obj.status = 41
        else:
            obj.status = 30

        obj.save()


def set_old_trips_to_reviewed():
    conf_list = models.Trip.objects.filter(is_adm_approval_required=True)
    for obj in conf_list:
        if obj.start_date <= timezone.now():
            obj.status = 32
            obj.save()


def update_participant_role():
    for r in models.TripRequest.objects.filter(role_id=2):
        r.role_id = 1
        r.save()

    for r in models.TripRequest.objects.filter(role_id=9):
        r.role_id = 8
        r.save()

    for r in models.TripRequest.objects.filter(role_id=5):
        r.role_id = 8
        r.save()

    for r in models.TripRequest.objects.filter(role_id=6):
        r.role_id = 7
        r.save()

    models.Role.objects.filter(name__icontains="DELETE ME").delete()


#
# def resave_all():
#     conf_list = models.Trip.objects.all()
#     for obj in conf_list:
#         obj.save()
#
# def add_original_submission_date():
#     for obj in models.TripRequest.objects.filter(submitted__isnull=False):
#         obj.original_submission_date = obj.submitted
#         obj.save()
#
#
#
# def copy_costs():
#     for tr in models.TripRequest.objects.filter():
#
#         if tr.air and tr.air != 0:
#             my_tr_cost, created = models.TravellerCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="air fare"),
#             )
#             my_tr_cost.amount_cad = tr.air
#             my_tr_cost.save()
#
#         if tr.rail and tr.rail != 0:
#             my_tr_cost, created = models.TravellerCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="rail"),
#             )
#             my_tr_cost.amount_cad = tr.rail
#             my_tr_cost.save()
#
#         if tr.rental_motor_vehicle and tr.rental_motor_vehicle != 0:
#             my_tr_cost, created = models.TravellerCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="rental motor vehicle"),
#             )
#             my_tr_cost.amount_cad = tr.rental_motor_vehicle
#             my_tr_cost.save()
#
#         if tr.personal_motor_vehicle and tr.personal_motor_vehicle != 0:
#             my_tr_cost, created = models.TravellerCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="personal motor vehicle"),
#             )
#             my_tr_cost.amount_cad = tr.personal_motor_vehicle
#             my_tr_cost.save()
#
#         if tr.taxi and tr.taxi != 0:
#             my_tr_cost, created = models.TravellerCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="taxi"),
#             )
#             my_tr_cost.amount_cad = tr.taxi
#             my_tr_cost.save()
#
#         if tr.other_transport and tr.other_transport != 0:
#             my_tr_cost, created = models.TravellerCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="other"),
#             )
#             my_tr_cost.amount_cad = tr.other_transport
#
#             my_tr_cost.save()
#
#
#         if tr.accommodations and tr.accommodations != 0:
#             my_tr_cost, created = models.TravellerCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="accommodation"),
#             )
#             my_tr_cost.amount_cad = tr.accommodations
#             my_tr_cost.save()
#
#         if tr.breakfasts and tr.breakfasts != 0:
#             my_tr_cost, created = models.TravellerCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="breakfasts"),
#             )
#             my_tr_cost.amount_cad = tr.breakfasts
#
#             my_tr_cost.number_of_days = tr.no_breakfasts
#             my_tr_cost.rate_cad = tr.breakfasts_rate
#             my_tr_cost.save()
#
#         if tr.lunches and tr.lunches != 0:
#             my_tr_cost, created = models.TravellerCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="lunches"),
#             )
#             my_tr_cost.amount_cad = tr.lunches
#             my_tr_cost.number_of_days = tr.no_lunches
#             my_tr_cost.rate_cad = tr.lunches_rate
#             my_tr_cost.save()
#
#         if tr.suppers and tr.suppers != 0:
#             my_tr_cost, created = models.TravellerCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="suppers"),
#             )
#             my_tr_cost.amount_cad = tr.suppers
#             my_tr_cost.number_of_days = tr.no_suppers
#             my_tr_cost.rate_cad = tr.suppers_rate
#             my_tr_cost.save()
#
#         if tr.incidentals and tr.incidentals != 0:
#             my_tr_cost, created = models.TravellerCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="incidentals"),
#             )
#             my_tr_cost.amount_cad = tr.incidentals
#             my_tr_cost.number_of_days = tr.no_incidentals
#             my_tr_cost.rate_cad = tr.incidentals_rate
#             my_tr_cost.save()
#
#         if tr.registration and tr.registration != 0:
#             my_tr_cost, created = models.TravellerCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="other"),
#             )
#             my_tr_cost.amount_cad = tr.registration
#             my_tr_cost.save()
#
#         if tr.other and tr.other != 0:
#             my_tr_cost, created = models.TravellerCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="other"),
#             )
#             my_tr_cost.amount_cad = tr.other
#             my_tr_cost.save()
#
#
#
#
#
#
#


def copy_old_tables_to_new():
    # piggy back: resave all orgs
    for o in Organization.objects.all():
        o.save()

    # loop through all requests, except for child requests

    bad_trip, created = models.Trip.objects.get_or_create(
        name="NOT A REAL TRIP",
        location="TestVille",
        start_date=timezone.datetime(year=2020, month=1, day=1),
        end_date=timezone.datetime(year=2021, month=1, day=1),
    )

    for old_request in models.TripRequest.objects.filter(parent_request__isnull=True):
        # print(old_request.id)
        if old_request.user:
            lead = old_request.user
        elif old_request.created_by:
            lead = old_request.created_by
        elif User.objects.filter(first_name=old_request.first_name, last_name=old_request.last_name).exists():
            lead = User.objects.get(first_name=old_request.first_name, last_name=old_request.last_name)
        else:
            print("assigning to Amelie")
            lead = User.objects.get(id=385)

        qs = models.TripRequest.objects.filter(id=old_request.id)
        if qs.exists():
            new_request = qs.first()
        else:
            new_request = models.TripRequest.objects.create(
                id=old_request.id,
                trip=old_request.trip if old_request.trip else bad_trip,
            )
        new_request.created_by = lead
        new_request.section = old_request.section
        new_request.status = old_request.status
        new_request.objective_of_event = old_request.objective_of_event
        new_request.benefit_to_dfo = old_request.benefit_to_dfo
        new_request.late_justification = old_request.late_justification
        new_request.funding_source = old_request.funding_source
        new_request.notes = old_request.notes
        new_request.admin_notes = old_request.admin_notes
        new_request.submitted = old_request.submitted
        new_request.original_submission_date = old_request.original_submission_date
        new_request.fiscal_year = old_request.fiscal_year
        new_request.save()

        for obj in old_request.bta_attendees.all():
            new_request.bta_attendees.add(obj)

        # reviewers
        for obj in old_request.reviewers.all():
            if not obj.request or obj.request != new_request:
                obj.request = new_request
                obj.save()

        # files
        for obj in old_request.files.all():
            if not obj.request or obj.request != new_request:
                obj.request = new_request
                obj.save()

        if not old_request.is_group_request:
            # might as well use the same id as the request

            qs = models.Traveller.objects.filter(id=old_request.id)
            if qs.exists():
                traveller = qs.first()
            else:
                traveller = models.Traveller.objects.create(
                    id=old_request.id,
                    request=new_request,
                    start_date=old_request.start_date,
                    end_date=old_request.end_date,
                )
            traveller.user = old_request.user
            traveller.is_public_servant = old_request.is_public_servant
            traveller.is_research_scientist = old_request.is_research_scientist
            traveller.first_name = old_request.first_name
            traveller.last_name = old_request.last_name
            traveller.address = old_request.address
            traveller.phone = old_request.phone
            traveller.email = old_request.email
            traveller.company_name = old_request.company_name
            traveller.departure_location = old_request.departure_location
            traveller.role = old_request.role
            traveller.role_of_participant = old_request.role_of_participant
            traveller.learning_plan = old_request.learning_plan
            traveller.notes = old_request.notes
            traveller.non_dfo_costs = old_request.non_dfo_costs
            traveller.non_dfo_org = old_request.non_dfo_org
            traveller.save()

            # costs
            for obj in old_request.trip_request_costs.all():
                if not obj.traveller or obj.traveller != traveller:
                    obj.traveller = traveller
                    obj.save()

        else:
            for old_child in old_request.children_requests.all():
                traveller, created = models.Traveller.objects.get_or_create(
                    id=old_child.id,
                    request=new_request,
                    start_date=old_child.start_date if old_child.start_date else old_request.start_date,
                    end_date=old_child.end_date if old_child.end_date else old_request.end_date,
                )
                traveller.user = old_child.user
                traveller.is_public_servant = old_child.is_public_servant
                traveller.is_research_scientist = old_child.is_research_scientist
                traveller.first_name = old_child.first_name
                traveller.last_name = old_child.last_name
                traveller.address = old_child.address
                traveller.phone = old_child.phone
                traveller.email = old_child.email
                traveller.company_name = old_child.company_name
                traveller.departure_location = old_child.departure_location
                traveller.role = old_child.role
                traveller.role_of_participant = old_child.role_of_participant
                traveller.learning_plan = old_child.learning_plan
                traveller.notes = old_child.notes
                traveller.non_dfo_costs = old_child.non_dfo_costs
                traveller.non_dfo_org = old_child.non_dfo_org
                traveller.save()

                # costs
                for obj in old_child.trip_request_costs.all():
                    if not obj.traveller or obj.traveller != traveller:
                        obj.traveller = traveller
                        obj.save()
