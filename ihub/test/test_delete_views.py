from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import DeleteView

from .. import models
from masterlist import models as ml_models
from .. import views
from ihub.test.common_tests import CommonIHubTest as CommonTest
from ihub.test import FactoryFloor


class TestPersonDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.PersonFactory()
        self.test_url = reverse_lazy('ihub:person_delete', args=[self.instance.pk, ])
        self.expected_template = 'ihub/person_confirm_delete.html'
        self.user = self.get_and_login_user(in_group="ihub_admin")

    @tag("Person", "person_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.PersonDeleteView, DeleteView)
        self.assert_inheritance(views.PersonDeleteView, views.iHubAdminRequiredMixin)

    @tag("Person", "person_delete", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Person", "person_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.PersonFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(ml_models.Person.objects.filter(pk=self.instance.pk).count(), 0)


class TestOrganizationDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.OrganizationFactory()
        self.test_url = reverse_lazy('ihub:org_delete', args=[self.instance.pk, ])
        self.expected_template = 'ihub/organization_confirm_delete.html'
        self.user = self.get_and_login_user(in_group="ihub_admin")

    @tag("Organization", "org_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.OrganizationDeleteView, DeleteView)

    @tag("Organization", "org_delete", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Organization", "org_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.OrganizationFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(ml_models.Organization.objects.filter(pk=self.instance.pk).count(), 0)


class TestOrganizationMemberDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.OrganizationMemberFactory()
        self.test_url = reverse_lazy('ihub:member_delete', args=[self.instance.pk, ])
        self.expected_template = 'ihub/member_confirm_delete_popout.html'
        self.user = self.get_and_login_user(in_group="ihub_admin")

    @tag("OrganizationMember", "member_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.MemberDeleteView, DeleteView)

    @tag("OrganizationMember", "member_delete", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("OrganizationMember", "member_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.OrganizationMemberFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(ml_models.OrganizationMember.objects.filter(pk=self.instance.pk).count(), 0)


class TestEntryDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.EntryFactory()
        self.test_url = reverse_lazy('ihub:entry_delete', args=[self.instance.pk, ])
        self.expected_template = 'ihub/entry_confirm_delete.html'
        self.user = self.get_and_login_user(in_group="ihub_admin")

    @tag("Entry", "entry_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.EntryDeleteView, DeleteView)
        self.assert_inheritance(views.EntryDeleteView, views.iHubAdminRequiredMixin)

    @tag("Entry", "entry_delete", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Entry", "entry_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.EntryFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Entry.objects.filter(pk=self.instance.pk).count(), 0)
