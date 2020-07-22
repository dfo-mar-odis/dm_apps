import datetime
import factory
from django.utils import timezone
from faker import Faker

from shared_models.test.SharedModelsFactoryFloor import SectionFactory, UserFactory, RegionFactory
from .. import models
from masterlist import models as ml_models

faker = Faker()


class SectorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ml_models.Sector

    name = factory.lazy_attribute(lambda o: faker.word())


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ml_models.Organization

    name_eng = factory.lazy_attribute(lambda o: faker.word())

    @staticmethod
    def get_valid_data():
        return {
            'name_eng': faker.word(),
            'processing_plant': 0,
            'wharf': 0,
        }


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ml_models.Person

    first_name = factory.lazy_attribute(lambda o: faker.first_name())
    last_name = factory.lazy_attribute(lambda o: faker.last_name())
    ihub_vetted = factory.lazy_attribute(lambda o: faker.pybool())

    @staticmethod
    def get_valid_data():
        return {
            'first_name': faker.first_name(),
            'last_name': faker.first_name(),
            'ihub_vetted': True,
        }


class OrganizationMemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ml_models.OrganizationMember

    person = factory.SubFactory(PersonFactory)
    organization = factory.SubFactory(OrganizationFactory)
    role = factory.lazy_attribute(lambda o: faker.catch_phrase())

    @staticmethod
    def get_valid_data():
        return {
            'person': PersonFactory().id,
            'organization': OrganizationFactory().id,
            'role': faker.catch_phrase(),
        }


class EntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Entry

    status = factory.lazy_attribute(lambda o: models.Status.objects.all()[faker.random_int(0, models.Status.objects.count() - 1)])
    entry_type = factory.lazy_attribute(lambda o: models.EntryType.objects.all()[faker.random_int(0, models.EntryType.objects.count() - 1)])
    title = factory.lazy_attribute(lambda o: faker.catch_phrase())

    @staticmethod
    def get_valid_data():
        return {
            'status': models.Status.objects.all()[faker.random_int(0, models.Status.objects.count() - 1)].id,
            'entry_type': models.EntryType.objects.all()[faker.random_int(0, models.EntryType.objects.count() - 1)].id,
            'title': faker.catch_phrase(),
            'regions': RegionFactory().id,
            'sectors': SectorFactory().id,
        }


class EntryPersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EntryPerson

    entry = factory.SubFactory(EntryFactory)
    user = factory.SubFactory(UserFactory)
    name = factory.lazy_attribute(lambda o: faker.catch_phrase())
    organization = factory.lazy_attribute(lambda o: faker.company())

    @staticmethod
    def get_valid_data():
        return {
            'entry': EntryFactory().id,
            'user': UserFactory().id,
            'name': faker.catch_phrase(),
            'organization': faker.company(),
        }


class EntryNoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EntryNote

    entry = factory.SubFactory(EntryFactory)
    type = factory.lazy_attribute(lambda o: faker.pyint(1, 4))
    date = factory.lazy_attribute(lambda o: faker.date_time_this_year(tzinfo=timezone.get_current_timezone()))
    note = factory.lazy_attribute(lambda o: faker.text())

    @staticmethod
    def get_valid_data():
        return {
            'entry': EntryFactory().id,
            'type': faker.pyint(1, 4),
            'date': faker.date_time_this_year(tzinfo=timezone.get_current_timezone()).strftime("%Y-%m-%d 13:00"),
            'note': faker.text(),
        }
