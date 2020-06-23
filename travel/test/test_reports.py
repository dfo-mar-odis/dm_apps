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
from .FactoryFloor import TripFactory
from .. import views

faker = Faker()


class TestReportSearchFormView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('travel:report_search')
        self.expected_template = 'travel/report_search.html'

    @tag("travel", 'report', "view")
    def test_view_class(self):
        self.assert_inheritance(views.ReportSearchFormView, FormView)

    @tag("travel", 'report', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template)

    # @tag("travel", 'report', "submit")
    # def test_submit(self):
    #     data = FactoryFloor.ReportSearchFactory.get_valid_data()
    #     self.assert_success_url(self.test_url, data=data)


class TestCFTSReport(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_urls = [
            reverse_lazy('travel:export_cfts_list', kwargs={
                "fy": "None", "region": "None", "trip": "None", "user": "None", "from_date": "None", "to_date": "None",
            }),
            reverse_lazy('travel:export_cfts_list', kwargs={
                "fy": fiscal_year(sap_style=True), "region": "None", "trip": "None", "user": "None", "from_date": "None", "to_date": "None",
            }),
            reverse_lazy('travel:export_cfts_list', kwargs={
                "fy": "None", "region": RegionFactory().id, "trip": "None", "user": "None", "from_date": "None", "to_date": "None",
            }),
            reverse_lazy('travel:export_cfts_list', kwargs={
                "fy": "None", "region": "None", "trip": TripFactory().id, "user": "None", "from_date": "None", "to_date": "None",
            }),
            reverse_lazy('travel:export_cfts_list', kwargs={
                "fy": "None", "region": "None", "trip": "None", "user": UserFactory().id, "from_date": "None", "to_date": "None",
            }),

        ]
        self.view = views.export_cfts_list

    @tag("travel", 'report')
    def test_view(self):
        self.assert_non_public_view(test_url=self.test_urls[0])
        for url in self.test_urls:
            self.assert_not_broken(url)


class TestTripListReport(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_urls = [
            reverse_lazy('travel:export_trip_list', kwargs={
                "fy": fiscal_year(sap_style=True), "region": "None", "adm": "None", "from_date": "None", "to_date": "None",
            }),
            reverse_lazy('travel:export_trip_list', kwargs={
                "fy": "None", "region": RegionFactory().id, "adm": "None", "from_date": "None", "to_date": "None",
            }),
            reverse_lazy('travel:export_trip_list', kwargs={
                "fy": "None", "region": "None", "adm": faker.pybool(), "from_date": "None", "to_date": "None",
            }),
            reverse_lazy('travel:export_trip_list', kwargs={
                "fy": "None", "region": "None", "adm": "None", "from_date": faker.date_time_this_year().strftime("%Y-%m-%d"), "to_date": "None",
            }),
            reverse_lazy('travel:export_trip_list', kwargs={
                "fy": "None", "region": "None", "adm": "None", "from_date": "None", "to_date": faker.date_time_this_year().strftime("%Y-%m-%d"),
            }),
        ]
        self.view = views.export_trip_list

    @tag("travel", 'report')
    def test_view(self):
        self.assert_non_public_view(test_url=self.test_urls[0])
        for url in self.test_urls:
            self.assert_not_broken(url)


class TestTravelPlanPDFDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.IndividualTripRequestFactory()
        self.test_url = reverse_lazy('travel:request_print', kwargs={"pk":self.instance.pk})

    @tag("travel", 'report', "view")
    def test_view_class(self):
        self.assert_inheritance(views.TravelPlanPDF, PDFTemplateView)
        self.assert_inheritance(views.TravelPlanPDF, views.TravelAccessRequiredMixin)

    @tag("travel", 'report', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, user=self.instance.user)

    @tag("travel", 'report', "context")
    def test_context(self):
        context_vars = [
            "parent",
            "trip_category_list",
            "object_list",
            "my_dict",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars)

