import datetime
from django.test import tag
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView
from easy_pdf.views import PDFTemplateView
from faker import Faker

from lib.functions.custom_functions import fiscal_year
from shared_models.test.SharedModelsFactoryFloor import RegionFactory, UserFactory
from travel.test import FactoryFloor

from travel.test.common_tests import CommonTravelTest as CommonTest
from .FactoryFloor import ResourceFactory
from .. import views

faker = Faker()


class TestReportSearchFormView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('inventory:report_search')
        self.expected_template = 'inventory/report_search.html'

    @tag("inventory", 'report', "view")
    def test_view_class(self):
        self.assert_inheritance(views.ReportSearchFormView, FormView)

    @tag("inventory", 'report', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        my_user = self.get_and_login_user(in_group="inventory_dm")
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=my_user)


class TestODIReport(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_urls = [
            reverse_lazy('inventory:export_odi_report'),
        ]
        self.view = views.export_odi_report

    @tag("inventory", 'report')
    def test_view(self):
        self.assert_non_public_view(test_url=self.test_urls[0])
        for url in self.test_urls:
            self.assert_not_broken(url)



class TestPhysicalSamplesReport(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_urls = [
            reverse_lazy('inventory:export_phyiscal_samples'),
        ]
        self.view = views.export_odi_report

    @tag("inventory", 'report')
    def test_view(self):
        self.assert_non_public_view(test_url=self.test_urls[0])
        for url in self.test_urls:
            self.assert_not_broken(url)
