from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import CreateView, UpdateView

from ihub.test import FactoryFloor
from ihub.test.common_tests import CommonIHubTest as CommonTest
from .. import views
from .. import models
from masterlist import models as ml_models


class TestPersonUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.PersonFactory()
        self.test_url = reverse_lazy('ihub:person_edit', args=[self.instance.pk, ])
        self.test_url1 = reverse_lazy('ihub:person_edit_pop', args=[self.instance.pk, ])
        self.expected_template = 'ihub/person_form.html'
        self.expected_template1 = 'ihub/person_form_popout.html'
        self.user = self.get_and_login_user(in_group="ihub_edit")

    @tag("Person", "person_form", "view")
    def test_view_class(self):
        self.assert_inheritance(views.PersonUpdateView, UpdateView)
        self.assert_inheritance(views.PersonUpdateViewPopout, UpdateView)

    @tag("Person", "person_form", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)
        self.assert_not_broken(self.test_url1)
        self.assert_non_public_view(test_url=self.test_url1, expected_template=self.expected_template1, user=self.user)

    @tag("Person", "person_form", "submit")
    def test_submit(self):
        data = FactoryFloor.PersonFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)
        self.assert_success_url(self.test_url1, data=data, user=self.user)


class TestOrganizationUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.OrganizationFactory()
        self.test_url = reverse_lazy('ihub:org_edit', args=[self.instance.pk, ])
        self.expected_template = 'ihub/organization_form.html'
        self.user = self.get_and_login_user(in_group="ihub_edit")

    @tag("Organization", "org_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.OrganizationUpdateView, UpdateView)
        self.assert_inheritance(views.OrganizationUpdateView, views.iHubEditRequiredMixin)

    @tag("Organization", "org_edit", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Organization", "org_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.OrganizationFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestOrganizationMemberUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.OrganizationMemberFactory()
        self.test_url = reverse_lazy('ihub:member_edit', args=[self.instance.pk, ])
        self.expected_template = 'ihub/member_form_popout.html'
        self.user = self.get_and_login_user(in_group="ihub_edit")

    @tag("OrganizationMember", "member_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.MemberUpdateView, UpdateView)

    @tag("OrganizationMember", "member_edit", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("OrganizationMember", "member_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.OrganizationMemberFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestEntryUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.EntryFactory()
        self.test_url = reverse_lazy('ihub:entry_edit', args=[self.instance.pk, ])
        self.expected_template = 'ihub/entry_form.html'
        self.user = self.get_and_login_user(in_group="ihub_edit")

    @tag("Entry", "entry_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.EntryUpdateView, UpdateView)
        self.assert_inheritance(views.EntryUpdateView, views.iHubEditRequiredMixin)

    @tag("Entry", "entry_edit", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Entry", "entry_edit", "submit")
    def test_submit(self):
        # need to make sure the organization is
        org = FactoryFloor.OrganizationFactory()
        grouping = ml_models.Grouping.objects.filter(is_indigenous=True).first()
        org.grouping.add(grouping)

        data = FactoryFloor.EntryFactory.get_valid_data()
        data["organizations"] = [org.id]
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestEntryNoteUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.EntryNoteFactory()
        self.test_url = reverse_lazy('ihub:note_edit', args=[self.instance.pk, ])
        self.expected_template = 'ihub/note_form_popout.html'
        self.user = self.get_and_login_user(in_group="ihub_edit")

    @tag("EntryNote", "note_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.NoteUpdateView, UpdateView)

    @tag("EntryNote", "note_edit", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("EntryNote", "note_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.EntryNoteFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestEntryPersonUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.EntryPersonFactory()
        self.test_url = reverse_lazy('ihub:ep_edit', args=[self.instance.pk, ])
        self.expected_template = 'ihub/entry_person_form_popout.html'
        self.user = self.get_and_login_user(in_group="ihub_edit")

    @tag("EntryPerson", "ep_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.EntryPersonUpdateView, UpdateView)

    @tag("EntryPerson", "ep_edit", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("EntryPerson", "ep_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.EntryPersonFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)
