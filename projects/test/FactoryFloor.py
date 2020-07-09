import factory
import datetime
from faker import Factory
from django.utils import timezone

from projects import models
from shared_models.test.SharedModelsFactoryFloor import UserFactory, SectionFactory, RegionFactory
from shared_models import models as shared_models

faker = Factory.create()


class ActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ActivityType


class FundingSourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FundingSource

    name = factory.lazy_attribute(lambda o: faker.word())
    funding_source_type = factory.lazy_attribute(
        lambda o: models.FundingSourceType.objects.all()[faker.random_int(0, models.FundingSourceType.objects.count() - 1)])


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Project

    section = factory.SubFactory(SectionFactory)
    activity_type = factory.lazy_attribute(
        lambda o: models.ActivityType.objects.all()[faker.random_int(0, models.ActivityType.objects.count() - 1)])
    start_date = factory.lazy_attribute(lambda o: faker.date_time(tzinfo=timezone.get_current_timezone()))
    end_date = factory.lazy_attribute(lambda o: o.start_date + datetime.timedelta(days=faker.random_int(1, 365)))
    project_title = factory.lazy_attribute(lambda o: faker.word())
    year = factory.lazy_attribute(
        lambda o: shared_models.FiscalYear.objects.all()[faker.random_int(0, shared_models.FiscalYear.objects.count() - 1)])


class StaffFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Staff

    project = factory.SubFactory(ProjectFactory)
    employee_type = factory.lazy_attribute(
        lambda o: models.EmployeeType.objects.all()[faker.random_int(0, models.EmployeeType.objects.count() - 1)])
    funding_source = factory.SubFactory(FundingSourceFactory)


class IndeterminateStaffFactory(StaffFactory):
    employee_type = factory.lazy_attribute(lambda o: models.EmployeeType.objects.get(pk=1))


class StudentStaffFactory(StaffFactory):
    employee_type = factory.lazy_attribute(lambda o: models.EmployeeType.objects.get(pk=4))


class OMCostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.OMCost

    project = factory.SubFactory(ProjectFactory)
    budget_requested = factory.lazy_attribute(lambda o: faker.random_int(100, 1000))
    funding_source = factory.SubFactory(FundingSourceFactory)


class OMCostTravelFactory(OMCostFactory):
    om_category = factory.lazy_attribute(lambda o: models.OMCategory.objects.get(pk=1))


class OMCostEquipmentFactory(OMCostFactory):
    om_category = factory.lazy_attribute(lambda o: models.OMCategory.objects.get(pk=5))


class UpcomingDateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.UpcomingDate

    region = factory.SubFactory(RegionFactory)
    description_en = factory.lazy_attribute(lambda o: faker.text())
    date = factory.lazy_attribute(lambda o: faker.date_time_this_year(tzinfo=timezone.get_current_timezone()))

    @staticmethod
    def get_valid_data():
        return {
            'region': RegionFactory().id,
            'description_en': faker.text(),
            'date': faker.date_time_this_year(tzinfo=timezone.get_current_timezone()),
        }

