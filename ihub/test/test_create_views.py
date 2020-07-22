from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import CreateView

from ihub.test import FactoryFloor
from ihub.test.common_tests import CommonIHubTest as CommonTest
from .. import views
from .. import models
from masterlist import models as ml_models


class TestPersonCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('ihub:person_new')
        self.test_url1 = reverse_lazy('ihub:person_new_pop')
        self.expected_template = 'ihub/person_form.html'
        self.expected_template1 = 'ihub/person_form_popout.html'
        self.user = self.get_and_login_user(in_group="ihub_edit")

    @tag("Person", "person_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.PersonCreateView, CreateView)
        self.assert_inheritance(views.PersonCreateView, views.iHubEditRequiredMixin)
        self.assert_inheritance(views.PersonCreateViewPopout, CreateView)
        self.assert_inheritance(views.PersonCreateViewPopout, views.iHubEditRequiredMixin)

    @tag("Person", "person_new", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)
        self.assert_not_broken(self.test_url1)
        self.assert_non_public_view(test_url=self.test_url1, expected_template=self.expected_template1, user=self.user)

    @tag("Person", "person_new", "submit")
    def test_submit(self):
        data = FactoryFloor.PersonFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)
        self.assert_success_url(self.test_url1, data=data, user=self.user)


class TestOrganizationCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('ihub:org_new')
        self.expected_template = 'ihub/organization_form.html'
        self.user = self.get_and_login_user(in_group="ihub_edit")

    @tag("Organization", "org_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.OrganizationCreateView, CreateView)

    @tag("Organization", "org_new", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Organization", "org_new", "submit")
    def test_submit(self):
        data = FactoryFloor.OrganizationFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestOrganizationMemberCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.OrganizationFactory()
        self.test_url = reverse_lazy('ihub:member_new', args=[self.instance.pk, ])
        self.expected_template = 'ihub/member_form_popout.html'
        self.user = self.get_and_login_user(in_group="ihub_edit")

    @tag("OrganizationMember", "member_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.MemberCreateView, CreateView)

    @tag("OrganizationMember", "member_new", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("OrganizationMember", "member_new", "submit")
    def test_submit(self):
        data = FactoryFloor.OrganizationMemberFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestEntryCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('ihub:entry_new')
        self.expected_template = 'ihub/entry_form.html'
        self.user = self.get_and_login_user(in_group="ihub_edit")

    @tag("Entry", "entry_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.EntryCreateView, CreateView)

    @tag("Entry", "entry_new", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Entry", "entry_new", "submit")
    def test_submit(self):
        org = FactoryFloor.OrganizationFactory()
        grouping = ml_models.Grouping.objects.filter(is_indigenous=True).first()
        org.grouping.add(grouping)

        data = FactoryFloor.EntryFactory.get_valid_data()
        data["organizations"] = [org.id]
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestEntryNoteCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.EntryFactory()
        self.test_url = reverse_lazy('ihub:note_new', args=[self.instance.pk, ])
        self.expected_template = 'ihub/note_form_popout.html'
        self.user = self.get_and_login_user(in_group="ihub_edit")

    @tag("EntryNote", "note_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.NoteCreateView, CreateView)

    @tag("EntryNote", "note_new", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("EntryNote", "note_new", "submit")
    def test_submit(self):
        data = FactoryFloor.EntryNoteFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestEntryPersonCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.EntryPersonFactory()
        self.test_url = reverse_lazy('ihub:ep_new', args=[self.instance.pk, ])
        self.expected_template = 'ihub/entry_person_form_popout.html'
        self.user = self.get_and_login_user(in_group="ihub_edit")

    @tag("EntryPerson", "ep_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.EntryPersonCreateView, CreateView)

    @tag("EntryPerson", "ep_new", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("EntryPerson", "ep_new", "submit")
    def test_submit(self):
        data = FactoryFloor.EntryPersonFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)