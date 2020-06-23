import os

from django.contrib.auth.models import User, Group
from django.utils import timezone

from lib.functions.custom_functions import listrify
from . import models
from . import utils
from django.core import serializers
from django.core.files import File
from shared_models import models as shared_models


# def remove_empty_trips():
#     for trip in models.Conference.objects.all():
#         if trip.trip_requests.count() == 0:
#             trip.delete()
#


def reset_trip_reviewers():
    for trip in models.Conference.objects.filter(is_adm_approval_required=True):
        if trip.reviewers.count() == 0:
            utils.get_trip_reviewers(trip)


def check_trip_purposes():
    print(f"trip id; trip name; purposes")
    for trip in models.Conference.objects.all():
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
        models.Reason,
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
    conf_list = models.Conference.objects.all()
    for obj in conf_list:
        if obj.is_verified:
            obj.status_id = 41
        else:
            obj.status_id = 30

        obj.save()



def set_old_trips_to_reviewed():
    conf_list = models.Conference.objects.filter(is_adm_approval_required=True)
    for obj in conf_list:
        if obj.start_date <= timezone.now():
            obj.status_id = 32
            obj.save()



#
# def resave_all():
#     conf_list = models.Conference.objects.all()
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
#             my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="air fare"),
#             )
#             my_tr_cost.amount_cad = tr.air
#             my_tr_cost.save()
#
#         if tr.rail and tr.rail != 0:
#             my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="rail"),
#             )
#             my_tr_cost.amount_cad = tr.rail
#             my_tr_cost.save()
#
#         if tr.rental_motor_vehicle and tr.rental_motor_vehicle != 0:
#             my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="rental motor vehicle"),
#             )
#             my_tr_cost.amount_cad = tr.rental_motor_vehicle
#             my_tr_cost.save()
#
#         if tr.personal_motor_vehicle and tr.personal_motor_vehicle != 0:
#             my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="personal motor vehicle"),
#             )
#             my_tr_cost.amount_cad = tr.personal_motor_vehicle
#             my_tr_cost.save()
#
#         if tr.taxi and tr.taxi != 0:
#             my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="taxi"),
#             )
#             my_tr_cost.amount_cad = tr.taxi
#             my_tr_cost.save()
#
#         if tr.other_transport and tr.other_transport != 0:
#             my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="other"),
#             )
#             my_tr_cost.amount_cad = tr.other_transport
#
#             my_tr_cost.save()
#
#
#         if tr.accommodations and tr.accommodations != 0:
#             my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="accommodation"),
#             )
#             my_tr_cost.amount_cad = tr.accommodations
#             my_tr_cost.save()
#
#         if tr.breakfasts and tr.breakfasts != 0:
#             my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
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
#             my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="lunches"),
#             )
#             my_tr_cost.amount_cad = tr.lunches
#             my_tr_cost.number_of_days = tr.no_lunches
#             my_tr_cost.rate_cad = tr.lunches_rate
#             my_tr_cost.save()
#
#         if tr.suppers and tr.suppers != 0:
#             my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="suppers"),
#             )
#             my_tr_cost.amount_cad = tr.suppers
#             my_tr_cost.number_of_days = tr.no_suppers
#             my_tr_cost.rate_cad = tr.suppers_rate
#             my_tr_cost.save()
#
#         if tr.incidentals and tr.incidentals != 0:
#             my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="incidentals"),
#             )
#             my_tr_cost.amount_cad = tr.incidentals
#             my_tr_cost.number_of_days = tr.no_incidentals
#             my_tr_cost.rate_cad = tr.incidentals_rate
#             my_tr_cost.save()
#
#         if tr.registration and tr.registration != 0:
#             my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
#                 trip_request=tr,
#                 cost = models.Cost.objects.get(name__iexact="other"),
#             )
#             my_tr_cost.amount_cad = tr.registration
#             my_tr_cost.save()
#
#         if tr.other and tr.other != 0:
#             my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
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
