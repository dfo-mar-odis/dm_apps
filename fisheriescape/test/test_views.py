from django.test import tag
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from fisheriescape import views
from fisheriescape.test.common_tests import CommonFisheriescapeTest as CommonTest


class TestIndexView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('fisheriescape:index')
        self.expected_template = 'fisheriescape/index.html'

    @tag("fisheriescape", 'index', "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url)


class TestMapView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('fisheriescape:map_view')
        self.expected_template = 'fisheriescape/map.html'

    @tag("fisheriescape", "map", "view")
    def test_view_class(self):
        self.assert_inheritance(views.MapView, TemplateView)
        self.assert_inheritance(views.MapView, views.FisheriescapeAccessRequired)

    @tag("fisheriescape", 'index', "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url)

