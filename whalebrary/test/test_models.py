from django.urls import reverse_lazy
from django.test import tag

from shared_models import models as shared_models
from whalebrary import models
from whalebrary.test import FactoryFloor
from whalebrary.test.common_tests import CommonWhalebraryTest as CommonTest
from faker import Faker

faker = Faker()


class TestItemModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ItemFactory()

    @tag('Item', 'models', 'fields')
    def test_fields(self):
        fields_to_check = [
            "item_name",
            "description",
            "note",
            "owner",
            "size",
            "category",
            "gear_type",
        ]
        self.assert_has_fields(models.Item, fields_to_check)

    @tag('Item', 'models', 'props')
    def test_props(self):
        self.assert_has_props(models.Item, ["tname",
                                            "lent_out_quantities",
                                            "get_oh_quantity",
                                            "total_oh_quantity",
                                            "oh_quantity_by_location",
                                            "active_orders"
                                            ])

    @tag('Item', 'models', 'm2m')
    def test_m2m_supplier(self):
        # a `my_model` that is attached to a given `supplier` should be accessible by the m2m field name `suppliers`
        supplier = FactoryFloor.SupplierFactory()
        self.instance.suppliers.add(supplier)
        self.assertEqual(self.instance.suppliers.count(), 1)
        self.assertIn(supplier, self.instance.suppliers.all())

    @tag('Item', 'models', 'unique_together')
    def test_unique_together(self):
        expected_unique_together = (('item_name', 'size'),)
        actual_unique_together = models.Item._meta.unique_together
        self.assertEqual(expected_unique_together, actual_unique_together)

    @tag('Item', 'models', 'mandatory_fields')
    def test_mandatory_fields(self):
        fields_to_check = ['owner',
                           'category',
                           'gear_type',
                           ]
        self.assert_mandatory_fields(models.Item, fields_to_check)


class TestOrderModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.OrderFactory()

    @tag('Order', 'models', 'fields')
    def test_fields(self):
        fields_to_check = ["item",
                           "quantity",
                           "cost",
                           "date_ordered",
                           "date_received",
                           "transaction",
                           ]

        self.assert_has_fields(models.Order, fields_to_check)

    @tag('Order', 'models', 'props')
    def test_props(self):
        self.assert_has_props(models.Order, ["trans_id"])

    @tag('Order', 'models', 'mandatory_fields')
    def test_mandatory_fields(self):
        fields_to_check = ['item',
                           "date_ordered",
                           ]

        self.assert_mandatory_fields(models.Order, fields_to_check)


class TestTransactionModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TransactionFactory()

    @tag('Transaction', 'models', 'fields')
    def test_fields(self):
        fields_to_check = ["item",
                           "quantity",
                           "category",
                           "comments",
                           "location",
                           "created_at",
                           "created_by",
                           "updated_at",
                           ]

        self.assert_has_fields(models.Transaction, fields_to_check)

    @tag('Transaction', 'models', 'm2m')
    def test_m2m_audit(self):
        # a `my_model` that is attached to a given `audit` should be accessible by the m2m field name `audits`
        audit = FactoryFloor.AuditFactory()
        self.instance.audits.add(audit)
        self.assertEqual(self.instance.audits.count(), 1)
        self.assertIn(audit, self.instance.audits.all())

    @tag('Transaction', 'models', 'm2m')
    def test_m2m_tag(self):
        # a `my_model` that is attached to a given `tag` should be accessible by the m2m field name `tags`
        tag = FactoryFloor.TagFactory()
        self.instance.tags.add(tag)
        self.assertEqual(self.instance.tags.count(), 1)
        self.assertIn(tag, self.instance.tags.all())

    @tag('Transaction', 'models', 'mandatory_fields')
    def test_mandatory_fields(self):
        fields_to_check = ['item',
                           "category",
                           "location",
                           "created_by",
                           ]
        self.assert_mandatory_fields(models.Transaction, fields_to_check)


class TestIncidentModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.IncidentFactory()
        self.instance = models.Incident.objects.all()[faker.random_int(0, models.Incident.objects.count() - 1)]

    @tag('Incident', 'models', 'fields')
    def test_fields(self):
        fields_to_check = ["name", "species", ]
        self.assert_has_fields(models.Incident, fields_to_check)

    @tag('Incident', 'models', 'props')
    def test_props(self):
        self.assert_has_props(models.Incident, ["coordinates"])

    @tag('Incident', 'models', 'inheritance')
    def test_inheritance(self):
        self.assert_inheritance(type(self.instance), shared_models.LatLongFields)

    @tag('Incident', 'models', 'choices')
    def test_choices_submitted(self):
        actual_choices = (
            (True, 'Yes'),
            (False, 'No'),
        )
        expected_choices = [field.choices for field in models.Incident._meta.fields if field.name == "submitted"][0]
        self.assertEqual(actual_choices, expected_choices)

    @tag('Incident', 'models', 'choices')
    def test_choices_gear_presence(self):
        actual_choices = (
            (True, 'Yes'),
            (False, 'No'),
        )
        expected_choices = [field.choices for field in models.Incident._meta.fields if field.name == "gear_presence"][0]
        self.assertEqual(actual_choices, expected_choices)

    @tag('Incident', 'models', 'choices')
    def test_choices_exam(self):
        actual_choices = (
            (True, 'Yes'),
            (False, 'No'),
        )
        expected_choices = [field.choices for field in models.Incident._meta.fields if field.name == "exam"][0]
        self.assertEqual(actual_choices, expected_choices)

    @tag('Incident', 'models', 'choices')
    def test_choices_necropsy(self):
        actual_choices = (
            (True, 'Yes'),
            (False, 'No'),
        )
        expected_choices = [field.choices for field in models.Incident._meta.fields if field.name == "necropsy"][0]
        self.assertEqual(actual_choices, expected_choices)

    @tag('Incident', 'models', 'choices')
    def test_choices_photos(self):
        actual_choices = (
            (True, 'Yes'),
            (False, 'No'),
        )
        expected_choices = [field.choices for field in models.Incident._meta.fields if field.name == "photos"][0]
        self.assertEqual(actual_choices, expected_choices)

    @tag('Incident', 'models', 'choices')
    def test_choices_region(self):
        actual_choices = (
            ("Gulf", "Gulf"),
            ("Mar", "Maritimes"),
            ("NL", "Newfoundland"),
            ("QC", "Quebec"),
        )
        expected_choices = [field.choices for field in models.Incident._meta.fields if field.name == "region"][0]
        self.assertEqual(actual_choices, expected_choices)

    @tag('Incident', 'models', 'choices')
    def test_choices_sex(self):
        actual_choices = (
            ("M", "Male"),
            ("F", "Female"),
            ("UnK", "Unknown"),
        )
        expected_choices = [field.choices for field in models.Incident._meta.fields if field.name == "sex"][0]
        self.assertEqual(actual_choices, expected_choices)

    @tag('Incident', 'models', 'choices')
    def test_choices_age_group(self):
        actual_choices = (
            ("J", "Juvenile"),
            ("YA", "Young Adult"),
            ("A", "Adult"),
        )
        expected_choices = [field.choices for field in models.Incident._meta.fields if field.name == "age_group"][0]
        self.assertEqual(actual_choices, expected_choices)

    @tag('Incident', 'models', 'choices')
    def test_choices_incident_type(self):
        actual_choices = (
            ("E", "Entangled"),
            ("DF", "DEAD - Floating"),
            ("DB", "DEAD - Beached"),
            ("N", "Necropsy"),
            ("LS", "LIVE - Stranded"),
            ("DS", "DEAD - Stranded"),
        )
        expected_choices = [field.choices for field in models.Incident._meta.fields if field.name == "incident_type"][0]
        self.assertEqual(actual_choices, expected_choices)

    @tag('Incident', 'models', 'mandatory_fields')
    def test_mandatory_fields(self):
        fields_to_check = ['species', ]
        self.assert_mandatory_fields(models.Incident, fields_to_check)
