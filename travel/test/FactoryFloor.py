import datetime
import factory
from django.utils import timezone
from faker import Faker

from shared_models.test.SharedModelsFactoryFloor import SectionFactory, UserFactory, RegionFactory, BranchFactory
from .. import models

faker = Faker()


class TripFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Conference
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


class IndividualTripRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TripRequest
        # django_get_or_create = ('trip','user','is_group_request')

    trip = factory.SubFactory(TripFactory)
    section = factory.SubFactory(SectionFactory)
    user = factory.SubFactory(UserFactory)
    is_group_request = False

    @staticmethod
    def get_valid_data():
        start_date = faker.future_datetime(tzinfo=timezone.get_current_timezone())
        end_date = start_date + datetime.timedelta(days=faker.random_int(1, 10))
        trip = TripFactory(
            start_date=start_date,
            end_date=end_date,
        )
        valid_data = {
            'trip': trip.id,
            "section": SectionFactory().id,
            "user": UserFactory().id,
            "is_group_request": False,
            "is_public_servant": True,
            "is_research_scientist": True,
            "start_date": trip.start_date.strftime("%Y-%m-%d %H:%M"),
            "end_date": trip.end_date.strftime("%Y-%m-%d %H:%M"),
        }
        return valid_data


class ParentTripRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TripRequest
        django_get_or_create = ('trip', 'user', 'is_group_request')

    trip = factory.SubFactory(TripFactory)
    section = factory.SubFactory(SectionFactory)
    user = factory.SubFactory(UserFactory)
    is_group_request = True


class ChildTripRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TripRequest

    trip = None
    parent_request = factory.SubFactory(ParentTripRequestFactory)
    user = factory.SubFactory(UserFactory)
    is_group_request = False

    @staticmethod
    def get_valid_data():
        start_date = faker.future_datetime(tzinfo=timezone.get_current_timezone())
        end_date = start_date + datetime.timedelta(days=faker.random_int(1, 10))
        trip = TripFactory(
            start_date=start_date,
            end_date=end_date,
        )
        parent_trip = ParentTripRequestFactory(trip=trip)
        parent_trip.save()
        valid_data = {
            'parent_request': parent_trip.id,
            "user": UserFactory().id,
            "is_public_servant": True,
            "is_research_scientist": True,
            "start_date": trip.start_date.strftime("%Y-%m-%d %H:%M"),
            "end_date": trip.end_date.strftime("%Y-%m-%d %H:%M"),
        }
        return valid_data


class ReviewerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Reviewer
        django_get_or_create = ('trip_request', 'user', 'role')

    trip_request = factory.SubFactory(IndividualTripRequestFactory)
    user = factory.SubFactory(UserFactory)
    role = factory.lazy_attribute(lambda o: models.ReviewerRole.objects.all()[faker.random_int(0, models.ReviewerRole.objects.count() - 1)])
    status = factory.lazy_attribute(
        lambda o: models.Status.objects.filter(used_for=1)[faker.random_int(0, models.Status.objects.filter(used_for=1).count() - 1)])
    status_date = factory.lazy_attribute(lambda o: o.trip_request.start_date + datetime.timedelta(days=faker.random_int(1, 365)))


class TripReviewerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TripReviewer

    trip = factory.SubFactory(TripFactory)
    role = factory.lazy_attribute(lambda o: models.ReviewerRole.objects.all()[faker.random_int(0, models.ReviewerRole.objects.count() - 1)])
    user = factory.SubFactory(UserFactory)

    @staticmethod
    def get_valid_data():
        return {
            # 'trip': TripFactory().id,
            # 'role': models.ReviewerRole.objects.all()[faker.random_int(0, models.ReviewerRole.objects.count() - 1)],
            # 'user': UserFactory().id,
            'comments': faker.catch_phrase(),
        }


class FileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.File

    trip_request = factory.SubFactory(IndividualTripRequestFactory)
    name = factory.lazy_attribute(lambda o: faker.word())


class TripRequestCostDayXRateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TripRequestCost

    trip_request = factory.SubFactory(IndividualTripRequestFactory)
    cost = factory.lazy_attribute(lambda o: models.Cost.objects.all()[faker.random_int(0, models.Cost.objects.count() - 1)])

    rate_cad = factory.lazy_attribute(lambda o: faker.pyfloat(positive=True))
    number_of_days = factory.lazy_attribute(lambda o: faker.random_int(1, 10))


class TripRequestCostTotalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TripRequestCost

    trip_request = factory.SubFactory(IndividualTripRequestFactory)
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
