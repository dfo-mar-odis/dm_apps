import datetime
from django.test import tag
from travel.test import FactoryFloor

from travel.test.common_tests import CommonTravelTest as CommonTest
from .. import forms


class TestTripRequestForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixutres
        self.Form = forms.TripRequestForm

    @tag("trip_request", 'form')
    def test_valid_data(self):
        data = FactoryFloor.IndividualTripRequestFactory.get_valid_data()
        self.assert_form_valid(self.Form, data=data)

        # test the form clean method
        my_trip = self.Form(data).save().trip
        data["end_date"] = (my_trip.start_date - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        self.assert_form_invalid(self.Form, data=data)
        # TODO: test the other invalid scenarios... e.g., when the start/end dates of request are greater or
        #  less than 10 days from the start/end dates of trip

    @tag("trip_request", 'form')
    def test_fields(self):
        # if looking at the trip request form with no instance, the reset reviewer field should not be there
        self.assert_field_not_in_form(self.Form, "reset_reviewers")
        tr = FactoryFloor.IndividualTripRequestFactory()
        self.assert_field_in_form(self.Form, "reset_reviewers", tr)
