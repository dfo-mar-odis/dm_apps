from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import DeleteView

from shared_models.views import CommonDeleteView, CommonPopoutDeleteView
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
        self.expected_template = 'ihub/confirm_delete.html'
        self.user = self.get_and_login_user(in_group="ihub_admin")

    @tag("Person", "person_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.PersonDeleteView, CommonDeleteView)
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
        self.expected_template = 'ihub/confirm_delete.html'
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
        self.expected_template = 'shared_models/generic_popout_confirm_delete.html'
        self.user = self.get_and_login_user(in_group="ihub_admin")

    @tag("OrganizationMember", "member_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.MemberDeleteView, CommonPopoutDeleteView)

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
        self.expected_template = 'ihub/confirm_delete.html'
        self.user = self.get_and_login_user(in_group="ihub_admin")

    @tag("Entry", "entry_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.EntryDeleteView, CommonDeleteView)
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


class TestEntryPersonDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.EntryPersonFactory()
        self.test_url = reverse_lazy('ihub:ep_delete', args=[self.instance.pk, ])
        self.user = self.get_and_login_user(in_group="ihub_edit")

    @tag("EntryPerson", "ep_delete", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)

    @tag("EntryPerson", "ep_delete", "access")
    def test_view2(self):
        self.assert_non_public_view(test_url=self.test_url, user=self.user, expected_code=302, locales=["en"])


class TestConsultationInstructionDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ConsultationInstructionFactory()
        self.test_url = reverse_lazy('ihub:instruction_delete', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/generic_popout_confirm_delete.html'
        self.user = self.get_and_login_user(in_group="ihub_admin")

    @tag("ConsultationInstruction", "instruction_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.InstructionDeleteView, CommonPopoutDeleteView)

    @tag("ConsultationInstruction", "instruction_delete", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("ConsultationInstruction", "instruction_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.ConsultationInstructionFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(ml_models.ConsultationInstruction.objects.filter(pk=self.instance.pk).count(), 0)



class TestConsultationRoleDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ConsultationRoleFactory()
        self.test_url = reverse_lazy('ihub:consultee_delete', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/generic_popout_confirm_delete.html'
        self.user = self.get_and_login_user(in_group="ihub_admin")

    @tag("ConsultationRole", "consultee_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.ConsultationRoleDeleteView, CommonPopoutDeleteView)

    @tag("ConsultationRole", "consultee_delete", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("ConsultationRole", "consultee_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.ConsultationRoleFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(ml_models.ConsultationRole.objects.filter(pk=self.instance.pk).count(), 0)