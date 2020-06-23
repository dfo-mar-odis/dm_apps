import factory
from django.contrib.auth.models import User, Group
from faker import Faker
from shared_models import models as shared_models
from django.contrib.auth.hashers import make_password

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


class RegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = shared_models.Region

    name = factory.LazyAttribute(lambda o: faker.word())

    @staticmethod
    def get_valid_data():
        return {
            'head': UserFactory().id,
            'name': faker.word(),
            'abbrev': faker.word()[:6],
        }


class BranchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = shared_models.Branch

    region = factory.SubFactory(RegionFactory)
    name = factory.LazyAttribute(lambda o: faker.word())

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

    @staticmethod
    def get_valid_data():
        return {
            'division': DivisionFactory().id,
            'head': UserFactory().id,
            'name': faker.word(),
            'abbrev': faker.word()[:6],
        }
