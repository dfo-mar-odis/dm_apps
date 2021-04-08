import factory
from django.contrib.gis.geos import Polygon, MultiPolygon, fromstr
from faker import Faker

from .. import models

faker = Faker()


# TODO not sure how to test a multipolygon field for FisheryArea model - create a static polygon
def get_multipolygon():
    # p1 = Polygon(((0, 0), (0, 1), (1, 1), (0, 0)))
    # p2 = Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
    p1 = fromstr('POLYGON ((0 0, 0 50, 50 50, 50 0, 0 0))', srid=4326)
    # p1 = Polygon()
    mp = MultiPolygon(p1)
    # mp = MultiPolygon([p1, p2])
    return mp


class FisheryAreaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FisheryArea

    layer_id = factory.lazy_attribute(lambda o: faker.catch_phrase())
    name = factory.lazy_attribute(lambda o: faker.catch_phrase())
    polygon = get_multipolygon()

    @staticmethod
    def get_valid_data():
        return {
            'layer_id': faker.catch_phrase(),
            'name': faker.catch_phrase(),
            'polygon': get_multipolygon(),
        }


class SpeciesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Species

    english_name = factory.lazy_attribute(lambda o: faker.catch_phrase())

    @staticmethod
    def get_valid_data():
        return {
            'english_name': faker.catch_phrase(),
        }


class MarineMammalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MarineMammal

    english_name_short = factory.lazy_attribute(lambda o: faker.catch_phrase())

    @staticmethod
    def get_valid_data():
        return {
            'english_name_short': faker.catch_phrase(),
        }


class FisheryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Fishery

    species = factory.SubFactory(SpeciesFactory)

    @staticmethod
    def get_valid_data():
        return {
            'species': SpeciesFactory().id,
        }
