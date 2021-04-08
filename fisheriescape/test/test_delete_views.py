from django.urls import reverse_lazy
from django.test import tag

from shared_models.views import CommonDeleteView, CommonPopoutDeleteView
from .. import models
from .. import views
from fisheriescape import views
from fisheriescape.test import FactoryFloor
from fisheriescape.test.common_tests import CommonFisheriescapeTest as CommonTest


# Example how to run with keyword tags
# python manage.py test fisheriescape.test --tag species_delete


class TestSpeciesDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.SpeciesFactory()
        self.test_url = reverse_lazy('fisheriescape:species_delete', args=[self.instance.pk, ])
        self.expected_template = 'fisheriescape/confirm_delete.html'
        self.user = self.get_and_login_user(in_group="fisheriescape_admin")

    @tag("Species", "species_list", "view")
    def test_view_class(self):
        self.assert_inheritance(views.SpeciesDeleteView, CommonDeleteView)
        self.assert_inheritance(views.SpeciesDeleteView, views.FisheriescapeAdminAccessRequired)

    @tag("Species", "species_list", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Species", "species_list", "submit")
    def test_submit(self):
        data = FactoryFloor.SpeciesFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Species.objects.filter(pk=self.instance.pk).count(), 0)

    @tag("Species", "species_list", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("fisheriescape:species_delete", f"/en/fisheriescape/species/{self.instance.pk}/delete/", [self.instance.pk])

#
# class TestFisheryAreaDeleteView(CommonTest):
#     def setUp(self):
#         super().setUp()
#         self.instance = FactoryFloor.FisheryAreaFactory()
#         self.test_url = reverse_lazy('fisheriescape:fishery_area_delete', args=[self.instance.pk, ])
#         self.expected_template = 'fisheriescape/confirm_delete.html'
#         self.user = self.get_and_login_user(in_group="fisheriescape_admin")
#
#     @tag("FisheryArea", "fishery_area_delete", "view")
#     def test_view_class(self):
#         self.assert_inheritance(views.FisheryAreaDeleteView, CommonDeleteView)
#         self.assert_inheritance(views.FisheryAreaDeleteView, views.FisheriescapeAdminAccessRequired)
#
#     @tag("FisheryArea", "fishery_area_delete", "access")
#     def test_view(self):
#         self.assert_good_response(self.test_url)
#         self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)
#
#     @tag("FisheryArea", "fishery_area_delete", "submit")
#     def test_submit(self):
#         data = FactoryFloor.FisheryAreaFactory.get_valid_data()
#         self.assert_success_url(self.test_url, data=data, user=self.user)
#
#         # for delete views...
#         self.assertEqual(models.FisheryArea.objects.filter(pk=self.instance.pk).count(), 0)
#
#     @tag("FisheryArea", "fishery_area_delete", "correct_url")
#     def test_correct_url(self):
#         # use the 'en' locale prefix to url
#         self.assert_correct_url("fisheriescape:fishery_area_delete", f"/en/fisheriescape/fisheryarea/{self.instance.pk}/delete/", [self.instance.pk])


class TestFisheryDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.FisheryFactory()
        self.test_url = reverse_lazy('fisheriescape:fishery_delete', args=[self.instance.pk, ])
        self.expected_template = 'fisheriescape/confirm_delete.html'
        self.user = self.get_and_login_user(in_group="fisheriescape_admin")

    @tag("Fishery", "fishery_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.FisheryDeleteView, CommonDeleteView)

    @tag("Fishery", "fishery_delete", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Fishery", "fishery_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.FisheryFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Fishery.objects.filter(pk=self.instance.pk).count(), 0)

    @tag("Fishery", "fishery_delete", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("fisheriescape:fishery_delete", f"/en/fisheriescape/fishery/{self.instance.pk}/delete/", [self.instance.pk])
