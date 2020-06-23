from django.utils import timezone
from django.utils.translation import activate
from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import ListView
from django_filters.views import FilterView

from shared_models.test.SharedModelsFactoryFloor import RegionFactory
from shared_models.views import CommonFilterView, CommonListView
from travel.test import FactoryFloor
from .. import models
from .. import views
from travel.test.common_tests import CommonTravelTest as CommonTest


class TripRequestListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.tr = FactoryFloor.IndividualTripRequestFactory()
        self.test_url = reverse_lazy('travel:request_list', args=("my",))
        self.expected_template = 'travel/trip_request_list.html'

    @tag("trip_request", 'list', "view")
    def test_view_class(self):
        # make sure the view is inheriting from CanModify Mixin
        self.assert_inheritance(views.TripRequestListView, CommonFilterView)
        self.assert_inheritance(views.TripRequestListView, views.TravelAccessRequiredMixin)

    @tag("trip_request", 'list', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        # create an admin user (who should always be able to delete) and check to see there is a 200 response
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template)

    # Test that the context contains the proper vars
    @tag("trip_request", 'list', "context")
    def test_context(self):
        context_vars = [
            "field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars)

    @tag("trip_request", 'list', "custom")
    def test_excludes_child_requests(self):
        # TODO: make sure that the list is not showing child requests
        pass


class TestTripListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url2 = reverse_lazy('travel:trip_list', kwargs={"type": "upcoming"})  # should be accessible by anyone
        self.test_url3 = reverse_lazy('travel:trip_list', kwargs={"type": "adm-hit-list"})
        self.test_url1 = reverse_lazy('travel:trip_list', kwargs={"type": "all"})
        self.expected_template = 'travel/trip_list.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")
        # in order for this to work, we have to make sure there is a trip obj in the db
        FactoryFloor.TripFactory()

    @tag("trip_list", 'list', "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripListView, CommonFilterView)
        self.assert_inheritance(views.TripListView, views.TravelAccessRequiredMixin)

    @tag("trip_list", 'list', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url2)
        self.assert_not_broken(self.test_url3)
        self.assert_not_broken(self.test_url1)
        self.assert_non_public_view(test_url=self.test_url2, expected_template=self.expected_template)
        self.assert_non_public_view(test_url=self.test_url3, expected_template=self.expected_template, user=self.admin_user)
        self.assert_non_public_view(test_url=self.test_url1, expected_template=self.expected_template, user=self.admin_user)

    @tag("trip_list", 'list', "context")
    def test_context(self):
        context_vars = [
            "field_list",
            "is_admin",
        ]
        self.assert_presence_of_context_vars(self.test_url2, context_vars, user=self.admin_user)
        self.assert_presence_of_context_vars(self.test_url3, context_vars, user=self.admin_user)
        self.assert_presence_of_context_vars(self.test_url1, context_vars, user=self.admin_user)


class TestTripVerificationListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TripFactory()
        self.test_url = reverse_lazy('travel:admin_trip_verification_list', kwargs={"region": 0, "adm": 0})
        self.expected_template = 'travel/trip_verification_list.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("travel", 'list', "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripVerificationListView, CommonListView)
        self.assert_inheritance(views.TripVerificationListView, views.TravelAdminRequiredMixin)

    @tag("travel", 'list', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        admin_user = self.get_and_login_user(in_group="travel_admin")
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("travel", 'list', "context")
    def test_context(self):
        context_vars = [
            "field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.admin_user)


class TestDefaultReviewerListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('travel:default_reviewer_list')
        self.expected_template = 'travel/default_reviewer_list.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("default_reviewer_list", 'list', "view")
    def test_view_class(self):
        self.assert_inheritance(views.DefaultReviewerListView, CommonListView)

    @tag("default_reviewer_list", 'list', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("default_reviewer_list", 'list', "context")
    def test_context(self):
        context_vars = [
            "field_list",
            "random_object",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, self.admin_user)
