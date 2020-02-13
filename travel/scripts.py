from . import models
from . import utils

def resave_all(events = models.TripRequest.objects.all()):
    for obj in events:
        if obj.status_id == 8:
            obj.reviewers.all().delete()
            utils.get_reviewers(obj)



def copy_costs():
    for tr in models.TripRequest.objects.filter():

        if tr.air and tr.air != 0:
            my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
                trip_request=tr,
                cost = models.Cost.objects.get(name__iexact="air fare"),
            )
            my_tr_cost.amount_cad = tr.air
            my_tr_cost.save()

        if tr.rail and tr.rail != 0:
            my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
                trip_request=tr,
                cost = models.Cost.objects.get(name__iexact="rail"),
            )
            my_tr_cost.amount_cad = tr.rail
            my_tr_cost.save()

        if tr.rental_motor_vehicle and tr.rental_motor_vehicle != 0:
            my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
                trip_request=tr,
                cost = models.Cost.objects.get(name__iexact="rental motor vehicle"),
            )
            my_tr_cost.amount_cad = tr.rental_motor_vehicle
            my_tr_cost.save()

        if tr.personal_motor_vehicle and tr.personal_motor_vehicle != 0:
            my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
                trip_request=tr,
                cost = models.Cost.objects.get(name__iexact="personal motor vehicle"),
            )
            my_tr_cost.amount_cad = tr.personal_motor_vehicle
            my_tr_cost.save()

        if tr.taxi and tr.taxi != 0:
            my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
                trip_request=tr,
                cost = models.Cost.objects.get(name__iexact="taxi"),
            )
            my_tr_cost.amount_cad = tr.taxi
            my_tr_cost.save()

        if tr.other_transport and tr.other_transport != 0:
            my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
                trip_request=tr,
                cost = models.Cost.objects.get(name__iexact="other"),
            )
            my_tr_cost.amount_cad = tr.other_transport

            my_tr_cost.save()


        if tr.accommodations and tr.accommodations != 0:
            my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
                trip_request=tr,
                cost = models.Cost.objects.get(name__iexact="accommodation"),
            )
            my_tr_cost.amount_cad = tr.accommodations
            my_tr_cost.save()

        if tr.breakfasts and tr.breakfasts != 0:
            my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
                trip_request=tr,
                cost = models.Cost.objects.get(name__iexact="breakfasts"),
            )
            my_tr_cost.amount_cad = tr.breakfasts

            my_tr_cost.number_of_days = tr.no_breakfasts
            my_tr_cost.rate_cad = tr.breakfasts_rate
            my_tr_cost.save()

        if tr.lunches and tr.lunches != 0:
            my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
                trip_request=tr,
                cost = models.Cost.objects.get(name__iexact="lunches"),
            )
            my_tr_cost.amount_cad = tr.lunches
            my_tr_cost.number_of_days = tr.no_lunches
            my_tr_cost.rate_cad = tr.lunches_rate
            my_tr_cost.save()

        if tr.suppers and tr.suppers != 0:
            my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
                trip_request=tr,
                cost = models.Cost.objects.get(name__iexact="suppers"),
            )
            my_tr_cost.amount_cad = tr.suppers
            my_tr_cost.number_of_days = tr.no_suppers
            my_tr_cost.rate_cad = tr.suppers_rate
            my_tr_cost.save()

        if tr.incidentals and tr.incidentals != 0:
            my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
                trip_request=tr,
                cost = models.Cost.objects.get(name__iexact="incidentals"),
            )
            my_tr_cost.amount_cad = tr.incidentals
            my_tr_cost.number_of_days = tr.no_incidentals
            my_tr_cost.rate_cad = tr.incidentals_rate
            my_tr_cost.save()

        if tr.registration and tr.registration != 0:
            my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
                trip_request=tr,
                cost = models.Cost.objects.get(name__iexact="other"),
            )
            my_tr_cost.amount_cad = tr.registration
            my_tr_cost.save()

        if tr.other and tr.other != 0:
            my_tr_cost, created = models.TripRequestCost.objects.get_or_create(
                trip_request=tr,
                cost = models.Cost.objects.get(name__iexact="other"),
            )
            my_tr_cost.amount_cad = tr.other
            my_tr_cost.save()







