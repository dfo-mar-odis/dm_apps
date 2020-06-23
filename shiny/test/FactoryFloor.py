import datetime
import factory
from django.utils import timezone
from faker import Faker

from shared_models.test.SharedModelsFactoryFloor import SectionFactory, UserFactory
from .. import models

faker = Faker()


class AppFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.App

    title_en = factory.lazy_attribute(lambda o: faker.company())
    description_en = factory.lazy_attribute(lambda o: faker.company())
    url = factory.lazy_attribute(lambda o: faker.url())
    github_url = factory.lazy_attribute(lambda o: faker.url())
    owner = factory.SubFactory(UserFactory)

    @staticmethod
    def get_valid_data():
        return {
            "title_en": faker.company(),
            "description_en": faker.company(),
            "url": faker.url(),
            "github_url": faker.url(),
            "owner": UserFactory().id,
        }
