from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import ListView
from django_filters.views import FilterView
from .. import models
from .. import views
from .common_tests import CommonTest
from ..views import CommonListView


class TestSectionListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('shared_models:section_list')
        self.expected_template = 'shared_models/org_list.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("section_list", 'list', "view")
    def test_view_class(self):
        self.assert_inheritance(views.SectionListView, CommonListView)
        self.assert_inheritance(views.SectionListView, views.AdminRequiredMixin)

    @tag("section_list", 'list', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("section_list", 'list', "context")
    def test_context(self):
        context_vars = [
            "section",
            "division",
            "branch",
            "region",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.admin_user)


class TestDivisionListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('shared_models:division_list')
        self.expected_template = 'shared_models/org_list.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("division_list", 'list', "view")
    def test_view_class(self):
        self.assert_inheritance(views.DivisionListView, CommonListView)
        self.assert_inheritance(views.DivisionListView, views.AdminRequiredMixin)

    @tag("division_list", 'list', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("division_list", 'list', "context")
    def test_context(self):
        context_vars = [
            "section",
            "division",
            "branch",
            "region",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.admin_user)


class TestBranchListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('shared_models:branch_list')
        self.expected_template = 'shared_models/org_list.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("branch_list", 'list', "view")
    def test_view_class(self):
        self.assert_inheritance(views.BranchListView, CommonListView)
        self.assert_inheritance(views.BranchListView, views.AdminRequiredMixin)

    @tag("branch_list", 'list', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("branch_list", 'list', "context")
    def test_context(self):
        context_vars = [
            "section",
            "division",
            "branch",
            "region",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.admin_user)


class TestRegionListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('shared_models:region_list')
        self.expected_template = 'shared_models/org_list.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("region_list", 'list', "view")
    def test_view_class(self):
        self.assert_inheritance(views.RegionListView, CommonListView)
        self.assert_inheritance(views.RegionListView, views.AdminRequiredMixin)

    @tag("region_list", 'list', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("region_list", 'list', "context")
    def test_context(self):
        context_vars = [
            "section",
            "division",
            "branch",
            "region",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.admin_user)
