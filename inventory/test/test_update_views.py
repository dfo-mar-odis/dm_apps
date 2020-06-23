from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import CreateView, UpdateView

from inventory.test import FactoryFloor
from inventory.test.common_tests import CommonInventoryTest as CommonTest
from .. import views
from .. import models


class TestResourceUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ResourceFactory()
        self.test_url = reverse_lazy('inventory:resource_edit', kwargs={"pk": self.instance.pk})
        self.resource_person = FactoryFloor.CustodianResourcePersonFactory(resource=self.instance)
        self.expected_template = 'inventory/resource_form.html'

    @tag("inventory", 'update', "view")
    def test_view_class(self):
        self.assert_inheritance(views.ResourceUpdateView, UpdateView)

    @tag("inventory", 'update', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        # the user must be a custodian...
        user = FactoryFloor.CustodianResourcePersonFactory(resource=self.instance)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.resource_person.person.user)

    # Test that the context contains the proper vars
    @tag("inventory", 'update', "context")
    def test_context(self):
        context_vars = [
            "resource_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.resource_person.person.user)

    @tag("inventory", 'update', "submit")
    def test_submit(self):
        data = FactoryFloor.ResourceFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.resource_person.person.user)


class TestResourceXMLExport(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ResourceFactory()
        self.test_url1 = reverse_lazy('inventory:export_xml', kwargs={"resource": self.instance.pk, "publish": "no"})  # this will be a draft
        self.test_url2 = reverse_lazy('inventory:export_xml',
                                      kwargs={"resource": self.instance.pk, "publish": "yes"})  # this will be to publish

    @tag("xml_export", 'update', "access")
    def test_xml_export_function(self):
        # let's ensure the resource starts out without a fgp date or revision date
        self.assertIsNone(self.instance.fgp_publication_date)
        self.assertIsNone(self.instance.last_revision_date)

        self.assert_not_broken(self.test_url1)
        self.assert_public_view(test_url=self.test_url1)

        # update the instance to check to see if fields were updated. they should not be
        self.instance = models.Resource.objects.get(pk=self.instance.pk)
        # this resource should not have an fgp publication date
        self.assertIsNone(self.instance.fgp_publication_date)
        self.assertIsNone(self.instance.last_revision_date)

        # check the second url
        response = self.client.get(self.test_url2)
        self.instance = models.Resource.objects.get(pk=self.instance.pk)
        self.assertIsNotNone(self.instance.fgp_publication_date)
        self.assertIsNone(self.instance.last_revision_date)

        # run a second time, the url2 should populate the last_revision_date
        response = self.client.get(self.test_url2)
        self.instance = models.Resource.objects.get(pk=self.instance.pk)
        self.assertIsNotNone(self.instance.fgp_publication_date)
        self.assertIsNotNone(self.instance.last_revision_date)


