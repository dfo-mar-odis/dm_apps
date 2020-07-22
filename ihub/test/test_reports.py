import datetime
from django.test import tag
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView
from easy_pdf.views import PDFTemplateView
from faker import Faker

from lib.functions.custom_functions import fiscal_year
from shared_models.test.SharedModelsFactoryFloor import RegionFactory, UserFactory
from ihub.test import FactoryFloor

from ihub.test.common_tests import CommonIHubTest as CommonTest
from .. import views
from .. import models

faker = Faker()


class TestReportSearchFormView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('ihub:report_search')
        self.expected_template = 'ihub/report_search.html'

    @tag("ihub", 'report', "view")
    def test_view_class(self):
        self.assert_inheritance(views.ReportSearchFormView, FormView)

    @tag("ihub", 'report', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        my_user = self.get_and_login_user()
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=my_user)


class TestConsultationLogReport(CommonTest):
    def setUp(self):
        super().setUp()
        org = FactoryFloor.OrganizationFactory()
        status = models.Status.objects.first()
        entry_type = models.EntryType.objects.first()
        self.test_urls = [
            reverse_lazy('ihub:consultation_log', args=[2020, org.id, status.id, entry_type.id, "testing report"]),
            reverse_lazy('ihub:consultation_log_xlsx', args=[2020, org.id, status.id, entry_type.id, "testing report"]),
            reverse_lazy('ihub:report_q', args=[org.id]),
        ]
        self.view = views.ConsultationLogPDFTemplateView

    @tag("ihub", 'reports')
    def test_view(self):
        for url in self.test_urls:
            self.assert_not_broken(url)