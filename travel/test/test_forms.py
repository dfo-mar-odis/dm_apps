import datetime

from django.test import tag
from django.utils import timezone

from travel.test import FactoryFloor
from travel.test.common_tests import CommonTravelTest as CommonTest
from .. import forms, models

#
# class TestTripRequestForm(CommonTest):
#
#     def setUp(self):
#         super().setUp()  # used to import fixutres
#         self.Form = forms.TripRequestForm
#
#     @tag("trip_request", 'form')
#     def test_valid_data(self):
#         data = FactoryFloor.IndividualTripRequestFactory.get_valid_data()
#         self.assert_form_valid(self.Form, data=data)
#
#         # test the form clean method
#         my_trip = self.Form(data).save().trip
#         data["end_date"] = (my_trip.start_date - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
#         self.assert_form_invalid(self.Form, data=data)
#
#         # test that if the trip request is late, a justification is required.
#         data = FactoryFloor.IndividualTripRequestFactory.get_valid_data()
#         my_trip_request = self.Form(data).save()
#         my_trip = my_trip_request.trip
#         my_trip.is_adm_approval_required = True
#         my_trip.date_eligible_for_adm_review = timezone.now() - datetime.timedelta(days=2)
#         my_trip.save()
#         my_trip_request = models.TripRequest.objects.get(pk=my_trip_request.id)
#         # make sure the TR is considered as late
#         self.assertTrue(my_trip_request.is_late_request)
#         self.assert_form_invalid(self.Form, data=data, instance=my_trip_request)
#         # let's add a justification
#         data["late_justification"] = "just because..."
#         self.assert_form_valid(self.Form, data=data, instance=my_trip_request)
#
#         # TODO: test the other invalid scenarios... e.g., when the start/end dates of request are greater or
#         #  less than 10 days from the start/end dates of trip
#
#     @tag("trip_request", 'form')
#     def test_fields(self):
#         # if looking at the trip request form with no instance, the reset reviewer field should not be there
#         self.assert_field_not_in_form(self.Form, "reset_reviewers")
#         tr = FactoryFloor.IndividualTripRequestFactory()
#         self.assert_field_in_form(self.Form, "reset_reviewers", tr)
