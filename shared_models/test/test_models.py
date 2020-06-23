from django.test import tag, TestCase
from django.urls import reverse_lazy
from django.utils.translation import activate

from shared_models.test import SharedModelsFactoryFloor as FactoryFloor
from shared_models.test.common_tests import CommonTest
from shared_models import models as shared_models


class TestSectionModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.SectionFactory()

    @tag('models', 'section')
    def test_related(self):
        # a division associated with a section should be accessible by the reverse name called `division`
        division = FactoryFloor.DivisionFactory()
        my_instance = self.instance
        my_instance.division = division
        my_instance.save()
        self.assertIn(my_instance, division.sections.all())

    @tag('models', 'section')
    def test_uuid(self):
        # a section instance should have a uuid field
        hasattr(self.instance, "uuid")
        # the field should not be null
        self.assertIsNotNone(self.instance.uuid)

    @tag('models', 'section')
    def test_is_instance(self):
        instance = FactoryFloor.SectionFactory()
        self.assert_inheritance(type(self.instance), shared_models.SimpleLookupWithUUID)


class TestDivisionModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.DivisionFactory()

    @tag('models', 'relations')
    def test_related(self):
        # a `division` that is attached to a given `branch` should be accessible by the reverse name `divisions`
        branch = FactoryFloor.BranchFactory()
        my_instance = self.instance
        my_instance.branch = branch
        my_instance.save()
        self.assertIn(my_instance, branch.divisions.all())

    @tag('models', 'division')
    def test_uuid(self):
        # a `division` instance should have a uuid field
        hasattr(self.instance, "uuid")
        # the field should not be null
        self.assertIsNotNone(self.instance.uuid)

    @tag('models', 'division')
    def test_is_instance(self):
        instance = FactoryFloor.DivisionFactory()
        self.assert_inheritance(type(self.instance), shared_models.SimpleLookupWithUUID)


class TestBranchModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.BranchFactory()

    @tag('models', 'relations')
    def test_related(self):
        # a `branch` that is attached to a given `region` should be accessible by the reverse name `branches`
        region = FactoryFloor.RegionFactory()
        my_instance = self.instance
        my_instance.region = region
        my_instance.save()
        self.assertIn(my_instance, region.branches.all())

    @tag('models', 'branch')
    def test_uuid(self):
        # a `branch` instance should have a uuid field
        hasattr(self.instance, "uuid")
        # the field should not be null
        self.assertIsNotNone(self.instance.uuid)

    @tag('models', 'branch')
    def test_is_instance(self):
        instance = FactoryFloor.BranchFactory()
        self.assert_inheritance(type(self.instance), shared_models.SimpleLookupWithUUID)


class TestRegionModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.RegionFactory()

    @tag('models', 'region')
    def test_uuid(self):
        # a `region` instance should have a uuid field
        hasattr(self.instance, "uuid")
        # the field should not be null
        self.assertIsNotNone(self.instance.uuid)

    @tag('models', 'region')
    def test_is_instance(self):
        instance = FactoryFloor.RegionFactory()
        self.assert_inheritance(type(self.instance), shared_models.SimpleLookupWithUUID)
