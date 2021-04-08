import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from faker import Faker

from shared_models import models as shared_models

faker = Faker()

test_password = "test1234"


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group
        django_get_or_create = ('name',)

    name = factory.LazyAttribute(lambda o: faker.word())


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    first_name = factory.LazyAttribute(lambda o: faker.first_name())
    last_name = factory.LazyAttribute(lambda o: faker.last_name())
    username = factory.LazyAttribute(lambda o: f"{o.first_name}.{o.last_name}@dfo-mpo.gc.ca")
    email = factory.LazyAttribute(lambda o: f"{o.first_name}.{o.last_name}@dfo-mpo.gc.ca")
    password = make_password(test_password)

    @staticmethod
    def get_test_password():
        return test_password

    @staticmethod
    def get_valid_data():
        first_name = faker.first_name()
        last_name = faker.last_name()
        return {
            'first_name': first_name,
            'last_name': last_name,
            'username': f"{first_name}.{last_name}@dfo-mpo.gc.ca",
            'email1': f"{first_name}.{last_name}@dfo-mpo.gc.ca",
            'email2': f"{first_name}.{last_name}@dfo-mpo.gc.ca",
            'password': make_password(test_password),
        }


class RegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = shared_models.Region

    name = factory.LazyAttribute(lambda o: faker.catch_phrase())
    head = factory.SubFactory(UserFactory)

    @staticmethod
    def get_valid_data():
        return {
            'head': UserFactory().id,
            'name': faker.catch_phrase(),
            'abbrev': faker.word()[:6],
        }


class BranchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = shared_models.Branch

    region = factory.SubFactory(RegionFactory)
    name = factory.LazyAttribute(lambda o: faker.word())
    head = factory.SubFactory(UserFactory)

    @staticmethod
    def get_valid_data():
        return {
            'region': RegionFactory().id,
            'head': UserFactory().id,
            'name': faker.word(),
            'abbrev': faker.word()[:6],
        }


class DivisionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = shared_models.Division

    branch = factory.SubFactory(BranchFactory)
    name = factory.LazyAttribute(lambda o: faker.word())
    head = factory.SubFactory(UserFactory)
    admin = factory.SubFactory(UserFactory)

    @staticmethod
    def get_valid_data():
        return {
            'branch': BranchFactory().id,
            'head': UserFactory().id,
            'name': faker.word(),
            'abbrev': faker.word()[:6],
        }


class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = shared_models.Section

    division = factory.SubFactory(DivisionFactory)
    head = factory.SubFactory(UserFactory)
    name = factory.LazyAttribute(lambda o: faker.word())
    admin = factory.SubFactory(UserFactory)

    @staticmethod
    def get_valid_data():
        return {
            'division': DivisionFactory().id,
            'head': UserFactory().id,
            'name': faker.word(),
            'abbrev': faker.word()[:6],
        }


class InstituteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = shared_models.Institute


class CruiseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = shared_models.Cruise

    institute = factory.lazy_attribute(
        lambda o: shared_models.Institute.objects.all()[faker.random_int(0, shared_models.Institute.objects.count() - 1)])
    mission_number = factory.LazyAttribute(lambda o: faker.word())
    mission_name = factory.LazyAttribute(lambda o: faker.word())
    chief_scientist = factory.LazyAttribute(lambda o: faker.word())

    @staticmethod
    def get_valid_data():
        return {
            'institue': shared_models.Institute.objects.all()[faker.random_int(0, shared_models.Institute.objects.count() - 1)],
            'mission_number': faker.word(),
            'mission_name': faker.word(),
            'chief_scientist': faker.word(),

        }


class ScriptFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = shared_models.Script

    name = factory.lazy_attribute(lambda o: faker.catch_phrase())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    script = factory.lazy_attribute(lambda o: faker.text())

    @staticmethod
    def get_valid_data():
        return {
            'name': faker.catch_phrase(),
            'description_en': faker.text(),
            'script': faker.text(),
        }


class PublicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = shared_models.Publication

    name = factory.lazy_attribute(lambda o: faker.company())


class CitationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = shared_models.Citation

    name = factory.lazy_attribute(lambda o: faker.catch_phrase())
    authors = factory.lazy_attribute(lambda o: faker.name())
    publication = factory.SubFactory(PublicationFactory)


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = shared_models.Project

    name = factory.lazy_attribute(lambda o: faker.catch_phrase())
    code = factory.lazy_attribute(lambda o: faker.pyint(1,1000))

    @staticmethod
    def get_valid_data():
        return {
            'name': faker.word(),
            'code': faker.word(),
        }
