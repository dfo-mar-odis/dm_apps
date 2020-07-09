import factory
from faker import Factory

from csas import models
from shared_models.test import SharedModelsFactoryFloor

from shared_models import models as shared_models

faker = Factory.create()


class LookupFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Lookup

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())


class SecSectorFactory(LookupFactory):

    class Meta:
        model = models.SecSector


class RepPriorityFactory(LookupFactory):
    class Meta:
        model = models.RepPriority


class RetTimingFactory(LookupFactory):
    class Meta:
        model = models.RetTiming


class ReqRequestFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.ReqRequest

    title = factory.lazy_attribute(lambda o: faker.word())

    region = factory.SubFactory(SharedModelsFactoryFloor.RegionFactory)

    client_sector = factory.SubFactory(SecSectorFactory)

    client_title = factory.lazy_attribute(lambda o: faker.sentence())
    client_email = factory.lazy_attribute(lambda o: faker.email())
    issue = factory.lazy_attribute(lambda o: faker.text())

    priority = factory.SubFactory(RepPriorityFactory)

    rationale = factory.lazy_attribute(lambda o: faker.text())

    proposed_timing = factory.SubFactory(RetTimingFactory)

    rationale_for_timing = factory.lazy_attribute(lambda o: faker.text())
    funding_notes = factory.lazy_attribute(lambda o: faker.text())
    science_discussion_notes = factory.lazy_attribute(lambda o: faker.sentence())

    in_year_request = factory.lazy_attribute(lambda o: faker.boolean())
    funding = factory.lazy_attribute(lambda o: faker.boolean())
    science_discussion = factory.lazy_attribute(lambda o: faker.boolean())
