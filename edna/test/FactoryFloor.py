import factory
from django.utils import timezone
from faker import Factory

from .. import models

faker = Factory.create()


class FiltrationTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FiltrationType

    name = factory.lazy_attribute(lambda o: faker.catch_phrase())

    @staticmethod
    def get_valid_data():
        return {
            'name': faker.catch_phrase(),
        }


class DNAExtractionProtocolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.DNAExtractionProtocol

    name = factory.lazy_attribute(lambda o: faker.catch_phrase())

    @staticmethod
    def get_valid_data():
        return {
            'name': faker.catch_phrase(),
        }


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tag

    name = factory.lazy_attribute(lambda o: faker.catch_phrase())

    @staticmethod
    def get_valid_data():
        return {
            'name': faker.catch_phrase(),
        }


class SpeciesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Species

    common_name_en = factory.lazy_attribute(lambda o: faker.word())

    @staticmethod
    def get_valid_data():
        return {
            'common_name_en': faker.word(),
        }


class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Collection

    name = factory.lazy_attribute(lambda o: faker.catch_phrase())

    @staticmethod
    def get_valid_data():
        return {
            'name': faker.catch_phrase(),
        }


class FileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.File

    collection = factory.SubFactory(CollectionFactory)
    caption = factory.lazy_attribute(lambda o: faker.text())
    file = factory.lazy_attribute(lambda o: faker.url())

    @staticmethod
    def get_valid_data():
        return {
            'collection': CollectionFactory().id,
            'caption': faker.text(),
        }


class SampleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Sample

    collection = factory.SubFactory(CollectionFactory)
    unique_sample_identifier = factory.lazy_attribute(lambda o: faker.pyint(1, 100000))
    datetime = factory.lazy_attribute(lambda o: faker.date_time_this_year(tzinfo=timezone.get_current_timezone()))
    latitude = factory.lazy_attribute(lambda o: faker.pyfloat(positive=True))
    longitude = factory.lazy_attribute(lambda o: faker.pyfloat())

    @staticmethod
    def get_valid_data():
        return {
            'collection': CollectionFactory().id,
            'unique_sample_identifier': faker.pyint(1, 100000),
            'datetime': faker.date_time_this_year(tzinfo=timezone.get_current_timezone()),
            'latitude': faker.pyfloat(positive=True),
            'longitude': faker.pyfloat(),
        }


class FiltrationBatchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FiltrationBatch

    datetime = factory.lazy_attribute(lambda o: faker.date_time_this_year(tzinfo=timezone.get_current_timezone()))

    @staticmethod
    def get_valid_data():
        return {
            'datetime': faker.date_time_this_year(tzinfo=timezone.get_current_timezone()),
        }


class ExtractionBatchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ExtractionBatch

    datetime = factory.lazy_attribute(lambda o: faker.date_time_this_year(tzinfo=timezone.get_current_timezone()))

    @staticmethod
    def get_valid_data():
        return {
            'datetime': faker.date_time_this_year(tzinfo=timezone.get_current_timezone()),
        }


class PCRBatchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PCRBatch

    datetime = factory.lazy_attribute(lambda o: faker.date_time_this_year(tzinfo=timezone.get_current_timezone()))

    @staticmethod
    def get_valid_data():
        return {
            'datetime': faker.date_time_this_year(tzinfo=timezone.get_current_timezone()),
        }


class FilterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Filter

    filtration_batch = factory.SubFactory(FiltrationBatchFactory)
    sample = factory.SubFactory(SampleFactory)
    filtration_type = factory.SubFactory(FiltrationTypeFactory)
    start_datetime = factory.lazy_attribute(lambda o: faker.date_time_this_year(tzinfo=timezone.get_current_timezone()))

    @staticmethod
    def get_valid_data():
        return {
            'filtration_batch': FiltrationBatchFactory().id,
            'sample': SampleFactory().id,
            'filtration_type': FiltrationTypeFactory().id,
            'start_datetime': faker.date_time_this_year(tzinfo=timezone.get_current_timezone()),
        }


class DNAExtractFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.DNAExtract

    extraction_batch = factory.SubFactory(ExtractionBatchFactory)
    filter = factory.SubFactory(FilterFactory)
    dna_extraction_protocol = factory.SubFactory(DNAExtractionProtocolFactory)
    start_datetime = factory.lazy_attribute(lambda o: faker.date_time_this_year(tzinfo=timezone.get_current_timezone()))

    @staticmethod
    def get_valid_data():
        return {
            'extraction_batch': ExtractionBatchFactory().id,
            'filter': FilterFactory().id,
            'dna_extraction_protocol': DNAExtractionProtocolFactory().id,
            'start_datetime': faker.date_time_this_year(tzinfo=timezone.get_current_timezone()),
        }


class PCRFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PCR

    pcr_batch = factory.SubFactory(PCRBatchFactory)
    extract = factory.SubFactory(DNAExtractFactory)
    start_datetime = factory.lazy_attribute(lambda o: faker.date_time_this_year(tzinfo=timezone.get_current_timezone()))

    @staticmethod
    def get_valid_data():
        return {
            'pcr_batch': PCRBatchFactory().id,
            'extract': DNAExtractFactory().id,
            'start_datetime': faker.date_time_this_year(tzinfo=timezone.get_current_timezone()),
        }


class SpeciesObservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SpeciesObservation

    pcr = factory.SubFactory(PCRFactory)
    species = factory.SubFactory(SpeciesFactory)
    ct = factory.lazy_attribute(lambda o: faker.pyfloat(positive=True))
    edna_conc = factory.lazy_attribute(lambda o: faker.pyfloat(positive=True))
    is_undetermined = factory.lazy_attribute(lambda o: faker.pybool())

    @staticmethod
    def get_valid_data():
        return {
            'pcr': PCRFactory().id,
            'species': SpeciesFactory().id,
            'ct': faker.pyfloat(positive=True),
            'edna_conc': faker.pyfloat(positive=True),
            'is_undetermined': faker.pybool(),
        }
