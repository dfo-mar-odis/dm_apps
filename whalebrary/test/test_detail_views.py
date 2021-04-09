from django.utils import timezone
from django.utils.translation import activate
from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import DetailView

from shared_models.views import CommonDetailView
from whalebrary.test import FactoryFloor
from whalebrary.test.common_tests import CommonWhalebraryTest as CommonTest
from .. import views

# Example how to run with keyword tags
# python manage.py test whalebrary.test --tag transaction_new


class TestItemDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ItemFactory()
        self.test_url = reverse_lazy('whalebrary:item_detail', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/item_detail.html'
        self.user = self.get_and_login_user()

    @tag("Item", "item_detail", "view")
    def test_view_class(self):
        self.assert_inheritance(views.ItemDetailView, CommonDetailView)

    @tag("Item", "item_detail", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Item", "item_detail", "context")
    def test_context(self):
        context_vars = [
            "field_list",
            "random_qty",
            "oh_qty_field_list",
            "random_sup",
            "sup_field_list",
            "random_ord",
            "ord_field_list",
            "random_lend",
            "lend_field_list",
            "random_file",
            "file_field_list",

        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)


class TestLocationDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.LocationFactory()
        self.test_url = reverse_lazy('whalebrary:location_detail', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/location_detail.html'
        self.user = self.get_and_login_user(in_group="whalebrary_admin")

    @tag("Location", "location_detail", "view")
    def test_view_class(self):
        self.assert_inheritance(views.LocationDetailView, CommonDetailView)
        self.assert_inheritance(views.LocationDetailView, views.WhalebraryAdminAccessRequired)

    @tag("Location", "location_detail", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Location", "location_detail", "context")
    def test_context(self):
        context_vars = [
            "field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)


class TestTransactionDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TransactionFactory()
        self.test_url = reverse_lazy('whalebrary:transaction_detail', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/transaction_detail.html'
        self.user = self.get_and_login_user()

    @tag("Transaction", "transaction_detail", "view")
    def test_view_class(self):
        self.assert_inheritance(views.TransactionDetailView, CommonDetailView)

    @tag("Transaction", "transaction_detail", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Transaction", "transaction_detail", "context")
    def test_context(self):
        context_vars = [
            "field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)


class TestOrderDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.OrderFactory()
        self.test_url = reverse_lazy('whalebrary:order_detail', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/order_detail.html'
        self.user = self.get_and_login_user()

    @tag("Order", "order_detail", "view")
    def test_view_class(self):
        self.assert_inheritance(views.OrderDetailView, CommonDetailView)
        self.assert_inheritance(views.OrderDetailView, views.WhalebraryAccessRequired)

    @tag("Order", "order_detail", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Order", "order_detail", "context")
    def test_context(self):
        context_vars = [
            "field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)


class TestPersonnelDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.PersonnelFactory()
        self.test_url = reverse_lazy('whalebrary:personnel_detail', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/personnel_detail.html'
        self.user = self.get_and_login_user(in_group="whalebrary_admin")

    @tag("Personnel", "personnel_detail", "view")
    def test_view_class(self):
        self.assert_inheritance(views.PersonnelDetailView, CommonDetailView)
        self.assert_inheritance(views.PersonnelDetailView, views.WhalebraryAdminAccessRequired)

    @tag("Personnel", "personnel_detail", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Personnel", "personnel_detail", "context")
    def test_context(self):
        context_vars = [
            "field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)


class TestSupplierDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.SupplierFactory()
        self.test_url = reverse_lazy('whalebrary:supplier_detail', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/supplier_detail.html'
        self.user = self.get_and_login_user()

    @tag("Supplier", "supplier_detail", "view")
    def test_view_class(self):
        self.assert_inheritance(views.SupplierDetailView, CommonDetailView)
        self.assert_inheritance(views.SupplierDetailView, views.WhalebraryAccessRequired)

    @tag("Supplier", "supplier_detail", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Supplier", "supplier_detail", "context")
    def test_context(self):
        context_vars = [
            "field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)


class TestIncidentDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.IncidentFactory()
        self.test_url = reverse_lazy('whalebrary:incident_detail', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/incident_detail.html'
        self.user = self.get_and_login_user()

    @tag("Incident", "incident_detail", "view")
    def test_view_class(self):
        self.assert_inheritance(views.IncidentDetailView, CommonDetailView)
        self.assert_inheritance(views.IncidentDetailView, views.WhalebraryAccessRequired)

    @tag("Incident", "incident_detail", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Incident", "incident_detail", "context")
    def test_context(self):
        context_vars = [
            "field_list",
            "random_image",
            "image_field_list",
            "all_incidents",
            "mapbox_api_key",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)


