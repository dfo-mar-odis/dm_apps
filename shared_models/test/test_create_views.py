from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import CreateView, UpdateView

from . import SharedModelsFactoryFloor as FactoryFloor
from .common_tests import CommonTest
from .. import views
from .. import models
from ..views import CommonCreateView


class TestSectionCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('shared_models:section_new')
        self.expected_template = 'shared_models/generic_form.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("section_new", 'update', "view")
    def test_view_class(self):
        self.assert_inheritance(views.SectionCreateView, CommonCreateView)
        self.assert_inheritance(views.SectionCreateView, views.AdminRequiredMixin)

    @tag("section_new", 'update', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("section_new", 'update', "submit")
    def test_submit(self):
        data = FactoryFloor.SectionFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.admin_user)


class TestDivisionCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('shared_models:division_new')
        self.expected_template = 'shared_models/generic_form.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("division_new", 'update', "view")
    def test_view_class(self):
        self.assert_inheritance(views.DivisionCreateView, CommonCreateView)
        self.assert_inheritance(views.DivisionCreateView, views.AdminRequiredMixin)

    @tag("division_new", 'update', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("division_new", 'update', "submit")
    def test_submit(self):
        data = FactoryFloor.DivisionFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.admin_user)


class TestBranchCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('shared_models:branch_new')
        self.expected_template = 'shared_models/generic_form.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("branch_new", 'update', "view")
    def test_view_class(self):
        self.assert_inheritance(views.BranchCreateView, CommonCreateView)
        self.assert_inheritance(views.BranchCreateView, views.AdminRequiredMixin)

    @tag("branch_new", 'update', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("branch_new", 'update', "submit")
    def test_submit(self):
        data = FactoryFloor.BranchFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.admin_user)


class TestRegionCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('shared_models:region_new')
        self.expected_template = 'shared_models/generic_form.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("region_new", 'update', "view")
    def test_view_class(self):
        self.assert_inheritance(views.RegionCreateView, CommonCreateView)
        self.assert_inheritance(views.RegionCreateView, views.AdminRequiredMixin)

    @tag("region_new", 'update', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("region_new", 'update', "submit")
    def test_submit(self):
        data = FactoryFloor.RegionFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.admin_user)
