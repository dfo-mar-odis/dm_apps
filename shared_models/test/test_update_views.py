from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import CreateView, UpdateView

from . import SharedModelsFactoryFloor as FactoryFloor
from .common_tests import CommonTest
from .. import views
from .. import models
from ..views import CommonUpdateView


class TestSectionUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.SectionFactory()
        self.test_url = reverse_lazy('shared_models:section_edit', kwargs={"pk": self.instance.pk})
        self.expected_template = 'shared_models/org_form.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("section_edit", 'update', "view")
    def test_view_class(self):
        self.assert_inheritance(views.SectionUpdateView, CommonUpdateView)
        self.assert_inheritance(views.SectionUpdateView, views.AdminRequiredMixin)

    @tag("section_edit", 'update', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)


    @tag("section_edit", 'update', "submit")
    def test_submit(self):
        data = FactoryFloor.SectionFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.admin_user)



class TestDivisionUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.DivisionFactory()
        self.test_url = reverse_lazy('shared_models:division_edit', kwargs={"pk": self.instance.pk})
        self.expected_template = 'shared_models/org_form.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("division_edit", 'update', "view")
    def test_view_class(self):
        self.assert_inheritance(views.DivisionUpdateView, CommonUpdateView)
        self.assert_inheritance(views.DivisionUpdateView, views.AdminRequiredMixin)

    @tag("division_edit", 'update', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)


    @tag("division_edit", 'update', "submit")
    def test_submit(self):
        data = FactoryFloor.DivisionFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.admin_user)


class TestBranchUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.BranchFactory()
        self.test_url = reverse_lazy('shared_models:branch_edit', kwargs={"pk": self.instance.pk})
        self.expected_template = 'shared_models/org_form.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("branch_edit", 'update', "view")
    def test_view_class(self):
        self.assert_inheritance(views.BranchUpdateView, CommonUpdateView)
        self.assert_inheritance(views.BranchUpdateView, views.AdminRequiredMixin)

    @tag("branch_edit", 'update', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)


    @tag("branch_edit", 'update', "submit")
    def test_submit(self):
        data = FactoryFloor.BranchFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.admin_user)


class TestRegionUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.RegionFactory()
        self.test_url = reverse_lazy('shared_models:region_edit', kwargs={"pk": self.instance.pk})
        self.expected_template = 'shared_models/org_form.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("region_edit", 'update', "view")
    def test_view_class(self):
        self.assert_inheritance(views.RegionUpdateView, CommonUpdateView)
        self.assert_inheritance(views.RegionUpdateView, views.AdminRequiredMixin)

    @tag("region_edit", 'update', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)


    @tag("region_edit", 'update', "submit")
    def test_submit(self):
        data = FactoryFloor.RegionFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.admin_user)
