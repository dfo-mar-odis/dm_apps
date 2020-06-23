from django.test import tag
from django.urls import reverse_lazy

from projects.test.common_tests import CommonProjectTest as CommonTest
from shared_models.test.SharedModelsFactoryFloor import RegionFactory
from shared_models.views import CommonFormView, CommonFormsetView
from .. import views
from shared_models import models as shared_models
from faker import Factory

faker = Factory.create()


class TestProjectApprovalSearchView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('projects:admin_project_approval_search')
        self.expected_template = 'projects/form.html'
        self.user = self.get_and_login_user(in_group="projects_admin")

    @tag("admin_project_approval_search", "view")
    def test_view_class(self):
        self.assert_inheritance(views.ProjectApprovalsSearchView, CommonFormView)

    @tag("admin_project_approval_search", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("admin_project_approval_search", "submit")
    def test_submit(self):
        fy = shared_models.FiscalYear.objects.all()[faker.random_int(0, shared_models.FiscalYear.objects.count() - 1)]
        region = RegionFactory().id
        data = {"region": region, "fy": fy}
        self.assert_success_url(self.test_url, data=data)


class TestProjectApprovalFormsetView(CommonTest):
    def setUp(self):
        super().setUp()
        fy = shared_models.FiscalYear.objects.all()[faker.random_int(0, shared_models.FiscalYear.objects.count() - 1)].id
        region = RegionFactory().id
        self.test_url = reverse_lazy('projects:admin_project_approval', kwargs={"region": region, "fy": fy})
        self.expected_template = 'projects/formset.html'
        self.user = self.get_and_login_user(in_group="projects_admin")

    @tag("admin_project_approval", "view")
    def test_view_class(self):
        self.assert_inheritance(views.ProjectApprovalFormsetView, CommonFormsetView)

    @tag("admin_project_approval", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("admin_project_approval", "submit")
    def test_submit(self):
        data = dict()  # should be fine to submit an empty dict
        self.assert_success_url(self.test_url, data=data)

