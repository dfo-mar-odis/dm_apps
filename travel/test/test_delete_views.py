from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import DeleteView

from shared_models.test.SharedModelsFactoryFloor import RegionFactory
from shared_models.views import CommonDeleteView
from travel.test import FactoryFloor
from .. import models
from .. import views
from travel.test.common_tests import CommonTravelTest as CommonTest


class IndividualTripRequestDelete(CommonTest):
    def setUp(self):
        super().setUp()
        self.tr = FactoryFloor.IndividualTripRequestFactory()
        self.tr1 = FactoryFloor.ChildTripRequestFactory()
        self.test_url = reverse_lazy('travel:request_delete', args=(self.tr.pk, "my"))
        self.test_url1 = reverse_lazy('travel:request_delete', args=(self.tr1.pk, "pop"))
        self.expected_template = 'travel/confirm_delete.html'
        self.expected_template1 = 'shared_models/generic_popout_form.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("trip_request", 'delete', "view")
    def test_view_class(self):
        # make sure the view is inheriting from CanModify Mixin
        self.assert_inheritance(views.TripRequestDeleteView, views.CanModifyMixin)
        self.assert_inheritance(views.TripRequestDeleteView, CommonDeleteView)

    @tag("trip_request", 'delete', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        # create an admin user (who should always be able to delete) and check to see there is a 200 response
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)
        self.assert_non_public_view(test_url=self.test_url1, expected_template=self.expected_template1, user=self.admin_user)

    @tag("trip_request", 'delete', "submit")
    def test_submit(self):
        # use an admin user because they should always be able to delete
        self.assert_success_url(self.test_url, user=self.admin_user)
        # ensure the user is deleted
        self.assertEqual(models.TripRequest.objects.filter(pk=self.tr.pk).count(), 0)

    @tag("trip_request", 'delete', "submit")
    def test_submit_pop(self):
        # use an admin user because they should always be able to delete
        self.assert_success_url(self.test_url1, user=self.admin_user)
        # ensure the user is deleted
        self.assertEqual(models.TripRequest.objects.filter(pk=self.tr1.pk).count(), 0)

class TestTripDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance0 = FactoryFloor.TripFactory()
        self.instance1 = FactoryFloor.TripFactory()
        self.instance2 = FactoryFloor.TripFactory(lead=RegionFactory())
        self.instance3 = FactoryFloor.TripFactory(is_adm_approval_required=True)
        self.test_url0 = reverse_lazy('travel:trip_delete', kwargs={"pk": self.instance0.pk, "type": "adm-hit-list"})
        self.test_url1 = reverse_lazy('travel:trip_delete', kwargs={"pk": self.instance1.pk, "type": "region-1"})
        self.test_url2 = reverse_lazy('travel:trip_delete', kwargs={"pk": self.instance2.pk, "type": "back_to_verify"})
        self.test_url3 = reverse_lazy('travel:trip_delete', kwargs={"pk": self.instance3.pk, "type": "all"})
        self.expected_template = 'travel/confirm_delete.html'

    @tag("trip_delete", 'delete', "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripDeleteView, CommonDeleteView)

    @tag("trip_delete", 'delete', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url0)
        self.assert_not_broken(self.test_url1)
        self.assert_not_broken(self.test_url2)
        self.assert_not_broken(self.test_url3)
        # TODO: do some more elaborate testing here!!
        my_user = self.get_and_login_user(in_group="travel_admin")
        self.assert_non_public_view(test_url=self.test_url0, expected_template=self.expected_template, user=my_user)
        self.assert_non_public_view(test_url=self.test_url1, expected_template=self.expected_template, user=my_user)
        self.assert_non_public_view(test_url=self.test_url2, expected_template=self.expected_template, user=my_user)
        self.assert_non_public_view(test_url=self.test_url3, expected_template=self.expected_template, user=my_user)

    @tag("trip_delete", 'delete', "submit")
    def test_submit(self):
        my_user = self.get_and_login_user(in_group="travel_admin")
        self.assert_success_url(self.test_url0, user=my_user)
        self.assert_success_url(self.test_url1, user=my_user)
        self.assert_success_url(self.test_url2, user=my_user)
        self.assert_success_url(self.test_url3, user=my_user)

        # for delete views...
        self.assertEqual(models.Conference.objects.filter(pk=self.instance0.pk).count(), 0)
        self.assertEqual(models.Conference.objects.filter(pk=self.instance1.pk).count(), 0)
        self.assertEqual(models.Conference.objects.filter(pk=self.instance2.pk).count(), 0)
        self.assertEqual(models.Conference.objects.filter(pk=self.instance3.pk).count(), 0)


