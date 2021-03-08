import datetime

import factory
from django.utils import timezone
from faker import Faker

from shared_models.test.SharedModelsFactoryFloor import SectionFactory, UserFactory, BranchFactory, RegionFactory
from .. import models

faker = Faker()


class ReferenceMaterialFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ReferenceMaterial

    file_en = factory.lazy_attribute(lambda o: faker.url())
    name = factory.lazy_attribute(lambda o: faker.catch_phrase())

    @staticmethod
    def get_valid_data():
        return {
            'file_en': faker.url(),
            'name': faker.catch_phrase(),

        }


class DefaultReviewerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.DefaultReviewer

    user = factory.SubFactory(UserFactory)

    @staticmethod
    def get_valid_data():
        return {
            'user': UserFactory().id,
            'sections': SectionFactory().id,
            'branches': BranchFactory().id,
        }


class TripFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Trip

    trip_subcategory = factory.lazy_attribute(lambda o: models.TripSubcategory.objects.all()[faker.random_int(0, models.TripSubcategory.objects.count() - 1)])
    name = factory.lazy_attribute(lambda o: faker.catch_phrase())
    location = factory.lazy_attribute(lambda o: faker.catch_phrase())
    start_date = factory.lazy_attribute(lambda o: faker.date_time_this_year(tzinfo=timezone.get_current_timezone()))
    end_date = factory.lazy_attribute(lambda o: o.start_date + datetime.timedelta(days=faker.random_int(1, 10)))
    lead = factory.SubFactory(RegionFactory)

    @staticmethod
    def get_valid_data():
        start_date = faker.future_datetime(tzinfo=timezone.get_current_timezone())
        end_date = start_date + datetime.timedelta(days=faker.random_int(1, 10))
        return {
            'trip_subcategory': models.TripSubcategory.objects.all()[faker.random_int(0, models.TripSubcategory.objects.count() - 1)].id,
            'name': faker.catch_phrase(),
            'location': faker.catch_phrase(),
            "start_date": start_date.strftime("%Y-%m-%d %H:%M"),
            "end_date": end_date.strftime("%Y-%m-%d %H:%M"),
            'is_virtual': faker.pybool(),
            'is_adm_approval_required': faker.pybool(),
            'lead': RegionFactory().id,

        }


class TripRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TripRequest

    trip = factory.SubFactory(TripFactory)
    section = factory.SubFactory(SectionFactory)
    created_by = factory.SubFactory(UserFactory)
    status = 8

    @staticmethod
    def get_valid_data():
        valid_data = {
            'trip': TripFactory().id,
            "section": SectionFactory().id,
            "created_by": UserFactory().id,
        }
        return valid_data


class TravellerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Traveller

    request = factory.SubFactory(TripRequestFactory)
    user = factory.SubFactory(UserFactory)
    start_date = factory.lazy_attribute(lambda o: faker.date_time_this_year(tzinfo=timezone.get_current_timezone()))
    end_date = factory.lazy_attribute(lambda o: o.start_date + datetime.timedelta(days=faker.random_int(1, 10)))
    is_public_servant = factory.lazy_attribute(lambda o: faker.pybool())
    is_research_scientist = factory.lazy_attribute(lambda o: faker.pybool())

    @staticmethod
    def get_valid_data():
        start_date = faker.future_datetime(tzinfo=timezone.get_current_timezone())
        end_date = start_date + datetime.timedelta(days=faker.random_int(1, 10))
        trip = TripFactory(
            start_date=start_date,
            end_date=end_date,
        )
        return {
            'request': TripRequestFactory().id,
            "user": UserFactory().id,
            "start_date": trip.start_date.strftime("%Y-%m-%d %H:%M"),
            "end_date": trip.end_date.strftime("%Y-%m-%d %H:%M"),
            'is_public_servant': faker.pybool(),
            'is_research_scientist': faker.pybool(),
        }


class ReviewerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Reviewer
        django_get_or_create = ('request', 'user', 'role')

    request = factory.SubFactory(TripRequestFactory)
    user = factory.SubFactory(UserFactory)
    role = factory.lazy_attribute(lambda o: models.Reviewer.role_choices[faker.random_int(0, len(models.Reviewer.role_choices) - 1)][0])
    status = factory.lazy_attribute(lambda o: models.Reviewer.status_choices[faker.random_int(0, len(models.Reviewer.status_choices) - 1)][0])
    order = factory.lazy_attribute(lambda o: faker.pyint(1,10))

    @staticmethod
    def get_valid_data():
        return {
            'request': TripRequestFactory().id,
            'user': UserFactory().id,
            'role': models.Reviewer.role_choices[faker.random_int(0, len(models.Reviewer.role_choices) - 1)][0],
            'status': models.Reviewer.status_choices[faker.random_int(0, len(models.Reviewer.status_choices) - 1)][0],
        }


class TripReviewerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TripReviewer

    trip = factory.SubFactory(TripFactory)
    role = factory.lazy_attribute(lambda o: models.TripReviewer.role_choices[faker.random_int(0, len(models.TripReviewer.role_choices) - 1)][0])
    user = factory.SubFactory(UserFactory)

    @staticmethod
    def get_valid_data():
        return {
            'comments': faker.catch_phrase(),
        }


class FileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.File

    trip_request = factory.SubFactory(TripRequestFactory)
    name = factory.lazy_attribute(lambda o: faker.word())
