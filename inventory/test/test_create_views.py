from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import CreateView

from inventory.test import FactoryFloor
from inventory.test.common_tests import CommonInventoryTest as CommonTest
from .. import views
from .. import models


class TestResourceCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('inventory:resource_new')
        self.expected_template = 'inventory/resource_form.html'

    @tag("inventory", 'create', "view")
    def test_view_class(self):
        self.assert_inheritance(views.ResourceCreateView, CreateView)

    @tag("inventory", 'create', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template)

    # Test that the context contains the proper vars
    @tag("inventory", 'create', "context")
    def test_context(self):
        context_vars = [
            "resource_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars)

    @tag("inventory", 'create', "submit")
    def test_submit(self):
        data = FactoryFloor.ResourceFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data)
        # get the instance just created and ensure there is a uuid
        my_instance = models.Resource.objects.get(**data)
        self.assertIsNotNone(my_instance.uuid)