from django.utils import timezone
from django.utils.translation import activate
from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import DetailView

from shared_models.views import CommonDetailView
from travel.test import FactoryFloor
from travel.test.common_tests import CommonTravelTest as CommonTest
from .. import views


class TripRequestDetails(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixutres
        self.trip_request = FactoryFloor.IndividualTripRequestFactory()
        self.test_url = reverse_lazy('travel:request_detail', args=(self.trip_request.pk, "my"))
        self.expected_template = 'travel/trip_request_detail.html'

    @tag("trip_request", 'detail', "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripRequestDetailView, views.TravelAccessRequiredMixin)
        self.assert_inheritance(views.TripRequestDetailView, CommonDetailView)

    @tag("trip_request", 'detail')
    def test_access(self):
        # only logged in users can access the landing
        super().assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template)

    @tag("trip_request", 'detail', "field_list")
    def test_fields(self):
        fields_to_test = [
            "fiscal_year"
        ]
        self.assert_field_in_field_list(self.test_url, "field_list", fields_to_test)

    # Test that the context contains the proper vars
    @tag("trip_request", 'detail', "context")
    def test_context(self):
        context_vars = [
            "field_list",
            "child_field_list",
            "reviewer_field_list",
            "conf_field_list",
            "cost_field_list",
            "help_text_dict",
            "help_text_dict",
            "fy",
            "is_admin",
            "is_owner",
            "is_current_reviewer",
            "can_modify",
            "trip",
            "triprequest",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars)

        activate('en')
        reg_user = self.get_and_login_user()
        response = self.client.get(self.test_url)
        # expected to determine if the user is authorized to add content

        # a random user should not be an admin, owner, current_reviewer, able-to-modify
        self.assertEqual(response.context["is_admin"], False)
        self.assertEqual(response.context["is_owner"], False)
        # self.assertEqual(response.context["report_mode"], True)
        # self.assertIsNone(response.context["can_modify"], False)
        self.assertIsNone(response.context["is_current_reviewer"], True)

        # if owner, the is_owner var should be true
        self.trip_request.user = reg_user
        self.trip_request.save()
        response = self.client.get(self.test_url)
        self.assertEqual(response.context["is_admin"], False)
        self.assertEqual(response.context["is_owner"], True)
        self.assertIsNone(response.context["is_current_reviewer"], True)

        # if a user is an admin, they should be able to modify and are also always the current_reviewer
        self.get_and_login_user(in_group='travel_admin')
        response = self.client.get(self.test_url)
        self.assertEqual(response.context["is_admin"], True)
        self.assertEqual(response.context["is_owner"], False)
        self.assertEqual(response.context["is_current_reviewer"], True)

        # if a regular user is the current reviewer
        my_reviewer = FactoryFloor.ReviewerFactory(trip_request=self.trip_request, status_id=1)
        self.get_and_login_user(user=my_reviewer.user)
        response = self.client.get(self.test_url)
        self.assertEqual(response.context["is_admin"], False)
        self.assertEqual(response.context["is_owner"], False)
        self.assertEqual(response.context["is_current_reviewer"], True)

        # a submitted project being viewed by someone who is not admin or not current reviewer should have report_mode set to True
        self.trip_request.submitted = timezone.now()
        self.trip_request.save()
        reg_user = self.get_and_login_user()
        response = self.client.get(self.test_url)
        self.assertEqual(response.context["report_mode"], True)


class TestTripDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TripFactory()
        self.test_url0 = reverse_lazy('travel:trip_detail', kwargs={"pk": self.instance.pk, "type": "upcoming"})
        self.test_url1 = reverse_lazy('travel:trip_detail', kwargs={"pk": self.instance.pk, "type": "region-1"})
        self.expected_template = 'travel/trip_detail.html'

    @tag("travel", 'detail', "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripDetailView, CommonDetailView)

    @tag("travel", 'detail', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url0)
        self.assert_not_broken(self.test_url1)
        self.assert_non_public_view(test_url=self.test_url0, expected_template=self.expected_template)
        self.assert_non_public_view(test_url=self.test_url1, expected_template=self.expected_template)

    @tag("travel", 'detail', "context")
    def test_context(self):
        context_vars = [
            "conf_field_list",
            "reviewer_field_list",
            "is_adm_admin",
            "trip",
        ]
        self.assert_presence_of_context_vars(self.test_url0, context_vars)
        self.assert_presence_of_context_vars(self.test_url1, context_vars)
