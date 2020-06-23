from django.test import tag, TestCase
from django.urls import reverse_lazy
from django.utils.translation import activate

from travel.test import FactoryFloor
from travel.test.common_tests import CommonTravelTest as CommonTest


class TestTravelModels(CommonTest):



    @tag('models', 'trip')
    def test_trip_model(self):
        # the requests associated with a trip can be accessed by the reverse name called `trips`
        trip_request = FactoryFloor.IndividualTripRequestFactory()
        trip = trip_request.trip
        # create a group travel request
        child_trip_request = FactoryFloor.ChildTripRequestFactory()
        # now we have to set the parent tr to have the same trip
        parent_trip_request = child_trip_request.parent_request
        parent_trip_request.trip = trip
        parent_trip_request.save()

        self.assertIn(trip_request, trip.trip_requests.all())
        self.assertIn(parent_trip_request, trip.trip_requests.all())

        # get_connected_active_request prop should get a qs of all connected trip request, excluding any parent requests (for group travel only)
        self.assertNotIn(trip_request, trip.get_connected_active_requests())
        self.assertNotIn(child_trip_request, trip.get_connected_active_requests())
        self.assertNotIn(parent_trip_request, trip.get_connected_active_requests())

        trip_request.status_id = 11
        trip_request.save()

        parent_trip_request.status_id = 11
        parent_trip_request.save()

        self.assertIn(trip_request, trip.get_connected_active_requests())
        self.assertIn(child_trip_request, trip.get_connected_active_requests())
        self.assertNotIn(parent_trip_request, trip.get_connected_active_requests()) # parent should not turn up

        # any traveller on a group or individual request should be listed in the trip.traveller_list prop
        # ONLY IF THE STATUS IS NOT EQUAL TO draft, denied or cancelled
        self.assertIn(trip_request.user, trip.traveller_list)
        self.assertIn(child_trip_request.user, trip.traveller_list)
        # the owner of the group trip should NOT be on the list
        self.assertNotIn(parent_trip_request.user, trip.traveller_list)
        # there should be a total of 2 travellers at this point

        self.assertEqual(trip.trip_requests.count(), 2)
        self.assertEqual(len(trip.traveller_list), 2)

    @tag('models', 'trip_request')
    def test_trip_request_model(self):
        # a reviewer associated with a trip request can be accessed by the reverse name called `reviewers`
        reviewer = FactoryFloor.ReviewerFactory()
        tr = reviewer.trip_request
        self.assertIn(reviewer, tr.reviewers.all())

        # a file associated with a trip request can be accessed by the reverse name called `files`
        file = FactoryFloor.FileFactory()
        tr = file.trip_request
        self.assertIn(file, tr.files.all())

        # a file associated with a trip request can be accessed by the reverse name called `files`
        tr_cost = FactoryFloor.TripRequestCostTotalFactory()
        tr = tr_cost.trip_request
        self.assertIn(tr_cost, tr.trip_request_costs.all())

    @tag('models', 'trip_request_cost')
    def test_trip_request_cost_model(self):
        # if you save a tr cost with a rate and days, it should provide a total equal to the product of the two
        tr_cost_1 = FactoryFloor.TripRequestCostDayXRateFactory()
        rate = tr_cost_1.rate_cad
        days = tr_cost_1.number_of_days
        tr_cost_1.save()
        self.assertEqual(rate*days, tr_cost_1.amount_cad)

        # if a tr_cost has only an amount, the save method should not override if there is a zero value in either rate or days
        tr_cost_2 = FactoryFloor.TripRequestCostTotalFactory()
        amount = tr_cost_2.amount_cad
        tr_cost_2.save()
        self.assertEqual(amount, tr_cost_2.amount_cad)

        tr_cost_2.rate_cad = rate
        tr_cost_2.number_of_days = 0
        tr_cost_2.save()
        self.assertEqual(amount, tr_cost_2.amount_cad)

        tr_cost_2.rate_cad = 0
        tr_cost_2.number_of_days = days
        tr_cost_2.save()
        self.assertEqual(amount, tr_cost_2.amount_cad)

        tr_cost_2.rate_cad = rate
        tr_cost_2.number_of_days = days
        tr_cost_2.save()
        self.assertEqual(rate*days, tr_cost_2.amount_cad)

    @tag('models', 'reviewer')
    def test_reviewer_model(self):
        # if you save a reviewer while a request is in NON DRAFT (!=8) and the reviewer is in draft status (=4), there is a problem. the status should
        # be queued (=20)
        reviewer = FactoryFloor.ReviewerFactory()
        tr = reviewer.trip_request

        reviewer.status_id = 4 # draft
        reviewer.save()

        tr.status_id = 2 # pending review
        tr.save()

        reviewer.save()
        self.assertEqual(reviewer.status_id, 20)


        # reviewers with a status of pending should be accessible throught the trip_request prop `current_reviewer`
        reviewer.status_id = 1  # draft
        reviewer.save()
        self.assertEqual(tr.current_reviewer, reviewer)