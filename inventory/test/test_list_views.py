from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import ListView
from django_filters.views import FilterView
from .. import models
from .. import views

from inventory.test.common_tests import CommonInventoryTest as CommonTest
from inventory.test import FactoryFloor


class TestResourceListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('inventory:resource_list')
        self.expected_template = 'inventory/resource_list.html'

    @tag("inventory", 'list', "view")
    def test_view_class(self):
        self.assert_inheritance(views.ResourceListView, FilterView)

    @tag("inventory", 'list', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        # create an admin user (who should always be able to delete) and check to see there is a 200 response
        self.assert_public_view(test_url=self.test_url, expected_template=self.expected_template)

    # Test that the context contains the proper vars
    @tag("inventory", 'list', "context")
    def test_context(self):
        context_vars = [
            "object_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars)


class TestMyResourceListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('inventory:my_resource_list')
        self.expected_template = 'inventory/my_resource_list.html'

    @tag("inventory", 'list', "view")
    def test_view_class(self):
        self.assert_inheritance(views.MyResourceListView, ListView)

    @tag("inventory", 'list', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template)

    # Test that the context contains the proper vars
    @tag("inventory", 'list', "context")
    def test_context(self):
        context_vars = [
            "field_list",
            "now",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars)