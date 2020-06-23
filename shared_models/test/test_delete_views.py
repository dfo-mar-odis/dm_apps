from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import DeleteView

from . import SharedModelsFactoryFloor as FactoryFloor
from .common_tests import CommonTest
from .. import views
from .. import models
from ..views import CommonDeleteView


class TestSectionDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.SectionFactory()
        self.test_url = reverse_lazy('shared_models:section_delete', kwargs={"pk": self.instance.pk})
        self.expected_template = 'shared_models/generic_confirm_delete.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("section_delete", 'delete', "view")
    def test_view_class(self):
        self.assert_inheritance(views.SectionDeleteView, CommonDeleteView)
        self.assert_inheritance(views.SectionDeleteView, views.AdminRequiredMixin)

    @tag("section_delete", 'delete', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("section_delete", 'delete', "submit")
    def test_submit(self):
        data = FactoryFloor.SectionFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.admin_user)

        # for delete views...
        self.assertEqual(models.Section.objects.filter(pk=self.instance.pk).count(), 0)


class TestDivisionDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.DivisionFactory()
        self.test_url = reverse_lazy('shared_models:division_delete', kwargs={"pk": self.instance.pk})
        self.expected_template = 'shared_models/generic_confirm_delete.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("division_delete", 'delete', "view")
    def test_view_class(self):
        self.assert_inheritance(views.DivisionDeleteView, CommonDeleteView)
        self.assert_inheritance(views.DivisionDeleteView, views.AdminRequiredMixin)

    @tag("division_delete", 'delete', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("division_delete", 'delete', "submit")
    def test_submit(self):
        data = FactoryFloor.DivisionFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.admin_user)

        # for delete views...
        self.assertEqual(models.Division.objects.filter(pk=self.instance.pk).count(), 0)


class TestBranchDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.BranchFactory()
        self.test_url = reverse_lazy('shared_models:branch_delete', kwargs={"pk": self.instance.pk})
        self.expected_template = 'shared_models/generic_confirm_delete.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("branch_delete", 'delete', "view")
    def test_view_class(self):
        self.assert_inheritance(views.BranchDeleteView, CommonDeleteView)
        self.assert_inheritance(views.BranchDeleteView, views.AdminRequiredMixin)

    @tag("branch_delete", 'delete', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("branch_delete", 'delete', "submit")
    def test_submit(self):
        data = FactoryFloor.BranchFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.admin_user)

        # for delete views...
        self.assertEqual(models.Branch.objects.filter(pk=self.instance.pk).count(), 0)


class TestRegionDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.RegionFactory()
        self.test_url = reverse_lazy('shared_models:region_delete', kwargs={"pk": self.instance.pk})
        self.expected_template = 'shared_models/generic_confirm_delete.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("region_delete", 'delete', "view")
    def test_view_class(self):
        self.assert_inheritance(views.RegionDeleteView, CommonDeleteView)
        self.assert_inheritance(views.RegionDeleteView, views.AdminRequiredMixin)

    @tag("region_delete", 'delete', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("region_delete", 'delete', "submit")
    def test_submit(self):
        data = FactoryFloor.RegionFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.admin_user)

        # for delete views...
        self.assertEqual(models.Region.objects.filter(pk=self.instance.pk).count(), 0)
