import datetime

import factory
from django.utils import timezone
from faker import Faker

from shared_models.test.SharedModelsFactoryFloor import SectionFactory, UserFactory, RegionFactory, BranchFactory
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


class TripFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Trip
        # django_get_or_create = ('name',)

    # name = faker.catch_phrase()
    name = factory.lazy_attribute(lambda o: faker.catch_phrase())
    start_date = factory.lazy_attribute(lambda o: faker.date_time_this_year(tzinfo=timezone.get_current_timezone()))
    end_date = factory.lazy_attribute(lambda o: o.start_date + datetime.timedelta(days=faker.random_int(1, 10)))
    trip_subcategory = factory.lazy_attribute(
        lambda o: models.TripSubcategory.objects.all()[faker.random_int(0, models.TripSubcategory.objects.count() - 1)])

    @staticmethod
    def get_valid_data():
        start_date = faker.future_datetime(tzinfo=timezone.get_current_timezone())
        end_date = start_date + datetime.timedelta(days=faker.random_int(1, 10))
        valid_data = {
            "is_adm_approval_required": False,
            "location": faker.city(),
            "lead": RegionFactory().id,
            "name": faker.catch_phrase(),
            "start_date": start_date.strftime("%Y-%m-%d %H:%M"),
            "end_date": end_date.strftime("%Y-%m-%d %H:%M"),
            "trip_subcategory": models.TripSubcategory.objects.all()[faker.random_int(0, models.TripSubcategory.objects.count() - 1)].id,
        }
        return valid_data


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

    request = TripRequestFactory()
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
        request = TripRequestFactory(trip=trip)
        request.save()
        valid_data = {
            'request': request.id,
            "user": UserFactory().id,
            "start_date": trip.start_date.strftime("%Y-%m-%d %H:%M"),
            "end_date": trip.end_date.strftime("%Y-%m-%d %H:%M"),
            'is_public_servant': faker.pybool(),
            'is_research_scientist': faker.pybool(),

        }
        return valid_data


class ReviewerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Reviewer
        django_get_or_create = ('trip_request', 'user', 'role')

    trip_request = factory.SubFactory(TripRequestFactory)
    user = factory.SubFactory(UserFactory)
    role = factory.lazy_attribute(lambda o: models.Reviewer.role_choices[faker.random_int(0, len(models.Reviewer.role_choices) - 1)][0])
    status = factory.lazy_attribute(lambda o: models.Reviewer.status_choices[faker.random_int(0, len(models.Reviewer.status_choices) - 1)][0])
    status_date = factory.lazy_attribute(lambda o: o.trip_request.start_date + datetime.timedelta(days=faker.random_int(1, 365)))


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


class TravellerCostDayXRateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TravellerCost

    trip_request = factory.SubFactory(TripRequestFactory)
    cost = factory.lazy_attribute(lambda o: models.Cost.objects.all()[faker.random_int(0, models.Cost.objects.count() - 1)])

    rate_cad = factory.lazy_attribute(lambda o: faker.pyfloat(positive=True) + 1)
    number_of_days = factory.lazy_attribute(lambda o: faker.random_int(1, 10))


class TravellerCostTotalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TravellerCost

    trip_request = factory.SubFactory(TripRequestFactory)
    cost = factory.lazy_attribute(lambda o: models.Cost.objects.all()[faker.random_int(0, models.Cost.objects.count() - 1)])
    amount_cad = factory.lazy_attribute(lambda o: faker.pyfloat(positive=True))


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
