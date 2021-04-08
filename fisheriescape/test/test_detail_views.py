from django.utils import timezone
from django.utils.translation import activate
from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import DetailView

from shared_models.views import CommonDetailView
from fisheriescape.test import FactoryFloor
from fisheriescape.test.common_tests import CommonFisheriescapeTest as CommonTest
from .. import views

# Example how to run with keyword tags
# python manage.py test fisheriescape.test --tag species_new


class TestSpeciesDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.SpeciesFactory()
        self.test_url = reverse_lazy('fisheriescape:species_detail', args=[self.instance.pk, ])
        self.expected_template = 'fisheriescape/species_detail.html'
        self.user = self.get_and_login_user(in_group="fisheriescape_admin")

    @tag("Species", "species_detail", "view")
    def test_view_class(self):
        self.assert_inheritance(views.SpeciesDetailView, CommonDetailView)
        self.assert_inheritance(views.SpeciesDetailView, views.FisheriescapeAdminAccessRequired)

    @tag("Species", "species_detail", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Species", "species_detail", "context")
    def test_context(self):
        context_vars = [
            "field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    @tag("Species", "species_detail", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("fisheriescape:species_detail", f"/en/fisheriescape/species/{self.instance.pk}/view/", [self.instance.pk])


class TestFisheryAreaDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.FisheryAreaFactory()
        self.test_url = reverse_lazy('fisheriescape:fishery_area_detail', args=[self.instance.pk, ])
        self.expected_template = 'fisheriescape/fisheryarea_detail.html'
        self.user = self.get_and_login_user(in_group="fisheriescape_admin")

    @tag("FisheryArea", "fishery_area_detail", "view")
    def test_view_class(self):
        self.assert_inheritance(views.FisheryAreaDetailView, CommonDetailView)
        self.assert_inheritance(views.FisheryAreaDetailView, views.FisheriescapeAdminAccessRequired)

    @tag("FisheryArea", "fishery_area_detail", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("FisheryArea", "fishery_area_detail", "context")
    def test_context(self):
        context_vars = [
            "field_list",
            "random_fishery",
            "fishery_field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    @tag("FisheryArea", "fishery_area_detail", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("fisheriescape:fishery_area_detail", f"/en/fisheriescape/fisheryarea/{self.instance.pk}/view/", [self.instance.pk])


class TestFisheryDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.FisheryFactory()
        self.test_url = reverse_lazy('fisheriescape:fishery_detail', args=[self.instance.pk, ])
        self.expected_template = 'fisheriescape/fishery_detail.html'
        self.user = self.get_and_login_user(in_group="fisheriescape_admin")

    @tag("Fishery", "fishery_detail", "view")
    def test_view_class(self):
        self.assert_inheritance(views.FisheryDetailView, CommonDetailView)
        self.assert_inheritance(views.FisheryDetailView, views.FisheriescapeAdminAccessRequired)

    @tag("Fishery", "fishery_detail", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Fishery", "fishery_detail", "context")
    def test_context(self):
        context_vars = [
            "field_list",
            "random_mammals",
            "mammals_field_list",
            "fishery_polygons",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    @tag("Fishery", "fishery_detail", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("fisheriescape:fishery_detail", f"/en/fisheriescape/fishery/{self.instance.pk}/view/", [self.instance.pk])