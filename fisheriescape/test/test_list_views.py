from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import ListView
from django_filters.views import FilterView

from shared_models.test.SharedModelsFactoryFloor import GroupFactory
from shared_models.views import CommonFilterView, CommonListView
from .. import models
from .. import views

from fisheriescape.test.common_tests import CommonFisheriescapeTest as CommonTest
from fisheriescape.test import FactoryFloor
from ..views import FisheriescapeAccessRequired


# Example how to run with keyword tags
# python manage.py test fisheriescape.test --tag species_list

class TestSpeciesListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.SpeciesFactory()
        self.test_url = reverse_lazy('fisheriescape:species_list')
        self.expected_template = 'fisheriescape/list.html'
        self.user = self.get_and_login_user()

    @tag("Species", "species_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.SpeciesListView, CommonFilterView)
        self.assert_inheritance(views.SpeciesListView, views.FisheriescapeAccessRequired)

    @tag("Species", "species_new", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Species", "species_new", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("fisheriescape:species_list", f"/en/fisheriescape/species-list/")


class TestFisheryAreaListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.FisheryAreaFactory()
        self.test_url = reverse_lazy('fisheriescape:fishery_area_list')
        self.expected_template = 'fisheriescape/list.html'
        self.user = self.get_and_login_user()

    @tag("FisheryArea", "fishery_area_list", "view")
    def test_view_class(self):
        self.assert_inheritance(views.FisheryAreaListView, CommonFilterView)
        self.assert_inheritance(views.FisheryAreaListView, views.FisheriescapeAccessRequired)

    @tag("FisheryArea", "fishery_area_list", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("FisheryArea", "fishery_area_list", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("fisheriescape:fishery_area_list", f"/en/fisheriescape/fisheryarea-list/")


class TestFisheryListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.FisheryFactory()
        self.test_url = reverse_lazy('fisheriescape:fishery_list')
        self.expected_template = 'fisheriescape/list.html'
        self.user = self.get_and_login_user()

    @tag("Fishery", "fishery_list", "view")
    def test_view_class(self):
        self.assert_inheritance(views.FisheryListView, CommonFilterView)
        self.assert_inheritance(views.FisheryListView, views.FisheriescapeAccessRequired)

    @tag("Fishery", "fishery_list", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Fishery", "fishery_list", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("fisheriescape:fishery_list", f"/en/fisheriescape/fishery-list/")
