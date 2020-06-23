import factory
from faker import Factory

from csas import models

from shared_models import models as shared_models

faker = Factory.create()


class LookupFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Lookup

    name_en = faker.word()
    name_fr = faker.word()
    description_en = faker.text()
    description_fr = faker.text()


class RegionFactory(factory.DjangoModelFactory):
    class Meta:
        model = shared_models.Region


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

    title = faker.word()

    region = factory.SubFactory(RegionFactory)

    client_sector = factory.SubFactory(SecSectorFactory)
    client_title = faker.sentence()
    client_email = faker.email()
    issue = faker.text()
    priority = factory.SubFactory(RepPriorityFactory)
    rationale = faker.text()
    proposed_timing = factory.SubFactory(RetTimingFactory)
    rationale_for_timing = faker.text()
    funding_notes = faker.text()
    science_discussion_notes = faker.sentence()

    in_year_request = faker.boolean()
    funding = faker.boolean()
    science_discussion = faker.boolean()
