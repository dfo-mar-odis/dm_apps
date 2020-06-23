from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import DeleteView

from .. import models
from .. import views
from inventory.test.common_tests import CommonInventoryTest as CommonTest
from inventory.test import FactoryFloor


class TestResourceDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ResourceFactory()
        self.user = self.get_and_login_user(in_group="inventory_dm")
        self.test_url = reverse_lazy('inventory:resource_delete', kwargs={"pk": self.instance.pk})
        self.expected_template = 'inventory/resource_confirm_delete.html'

    @tag("inventory", 'delete', "view")
    def test_view_class(self):
        self.assert_inheritance(views.ResourceDeleteView, DeleteView)

    @tag("inventory", 'delete', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)
        test_user=self.get_and_login_user()
        self.assert_not_accessible_by_user(test_url=self.test_url, user=test_user, login_search_term="accounts/denied")

    @tag("inventory", 'delete', "submit")
    def test_submit(self):
        self.assert_success_url(self.test_url, user=self.user)
        # for delete views...
        self.assertEqual(models.Resource.objects.filter(pk=self.instance.pk).count(), 0)
