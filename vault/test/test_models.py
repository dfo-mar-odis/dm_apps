from django.urls import reverse_lazy
from django.test import tag

import shared_models
from vault import models
from vault.test import FactoryFloor
from vault.test.common_tests import CommonVaultTest as CommonTest
from faker import Faker

faker = Faker()

#TODO add static/integer field tests here to ensure they don't change by accident

# class TestItemModel(CommonTest):
#     def setUp(self):
#         super().setUp()
#         self.instance = FactoryFloor.ItemFactory()
#
#     @tag('Item', 'models', 'fields')
#     def test_fields(self):
#         fields_to_check = [
#             "item_name",
#             "description",
#             "note",
#             "owner",
#             "size",
#             "category",
#             "gear_type",
#         ]
#         self.assert_has_fields(models.Item, fields_to_check)
#
#     @tag('Item', 'models', 'props')
#     def test_props(self):
#         self.assert_has_props(models.Item, ["tname",
#                                             "lent_out_quantities",
#                                             "get_oh_quantity",
#                                             "total_oh_quantity",
#                                             "oh_quantity_by_location",
#                                             "active_orders"
#                                             ])
#
#     @tag('Item', 'models', 'm2m')
#     def test_m2m_supplier(self):
#         # a `my_model` that is attached to a given `supplier` should be accessible by the m2m field name `suppliers`
#         supplier = FactoryFloor.SupplierFactory()
#         self.instance.suppliers.add(supplier)
#         self.assertEqual(self.instance.suppliers.count(), 1)
#         self.assertIn(supplier, self.instance.suppliers.all())
#
#     @tag('Item', 'models', 'unique_together')
#     def test_unique_together(self):
#         expected_unique_together = (('item_name', 'size'),)
#         actual_unique_together = models.Item._meta.unique_together
#         self.assertEqual(expected_unique_together, actual_unique_together)
#
#     @tag('Item', 'models', 'mandatory_fields')
#     def test_mandatory_fields(self):
#         fields_to_check = ['owner',
#                            'category',
#                            'gear_type',
#                            ]
#         self.assert_mandatory_fields(models.Item, fields_to_check)
#
#
# class TestOrderModel(CommonTest):
#     def setUp(self):
#         super().setUp()
#         self.instance = FactoryFloor.OrderFactory()
#
#     @tag('Order', 'models', 'fields')
#     def test_fields(self):
#         fields_to_check = ["item",
#                            "quantity",
#                            "cost",
#                            "date_ordered",
#                            "date_received",
#                            "transaction",
#                            ]
#
#         self.assert_has_fields(models.Order, fields_to_check)
#
#     @tag('Order', 'models', 'props')
#     def test_props(self):
#         self.assert_has_props(models.Order, ["trans_id"])
#
#     @tag('Order', 'models', 'mandatory_fields')
#     def test_mandatory_fields(self):
#         fields_to_check = ['item',
#                            "date_ordered",
#                            ]
#
#         self.assert_mandatory_fields(models.Order, fields_to_check)
#
#
# class TestTransactionModel(CommonTest):
#     def setUp(self):
#         super().setUp()
#         self.instance = FactoryFloor.TransactionFactory()
#
#     @tag('Transaction', 'models', 'fields')
#     def test_fields(self):
#         fields_to_check = ["item",
#                            "quantity",
#                            "category",
#                            "comments",
#                            "location",
#                            "created_at",
#                            "created_by",
#                            "updated_at",
#                            ]
#
#         self.assert_has_fields(models.Transaction, fields_to_check)
#
#     @tag('Transaction', 'models', 'm2m')
#     def test_m2m_audit(self):
#         # a `my_model` that is attached to a given `audit` should be accessible by the m2m field name `audits`
#         audit = FactoryFloor.AuditFactory()
#         self.instance.audits.add(audit)
#         self.assertEqual(self.instance.audits.count(), 1)
#         self.assertIn(audit, self.instance.audits.all())
#
#     @tag('Transaction', 'models', 'm2m')
#     def test_m2m_tag(self):
#         # a `my_model` that is attached to a given `tag` should be accessible by the m2m field name `tags`
#         tag = FactoryFloor.TagFactory()
#         self.instance.tags.add(tag)
#         self.assertEqual(self.instance.tags.count(), 1)
#         self.assertIn(tag, self.instance.tags.all())
#
#     @tag('Transaction', 'models', 'mandatory_fields')
#     def test_mandatory_fields(self):
#         fields_to_check = ['item',
#                            "category",
#                            "location",
#                            "created_at",
#                            "created_by",
#                            "updated_at",
#                            ]
#         self.assert_mandatory_fields(models.Transaction, fields_to_check)