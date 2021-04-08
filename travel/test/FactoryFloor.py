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
    is_adm_approval_required = factory.lazy_attribute(lambda o: faker.pybool())
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
            "late_justification": faker.text()
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
    order = factory.lazy_attribute(lambda o: faker.pyint(1, 10))

    @staticmethod
    def get_valid_data():
        return {
            'request': TripRequestFactory().id,
            'user': UserFactory().id,
            'role': models.Reviewer.role_choices[faker.random_int(0, len(models.Reviewer.role_choices) - 1)][0],
            'status': models.Reviewer.status_choices[faker.random_int(0, len(models.Reviewer.status_choices) - 1)][0],
            'order': faker.pyint(1, 10),
        }


class TripReviewerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TripReviewer

    trip = factory.SubFactory(TripFactory)
    role = factory.lazy_attribute(lambda o: models.TripReviewer.role_choices[faker.random_int(0, len(models.TripReviewer.role_choices) - 1)][0])
    status = factory.lazy_attribute(lambda o: models.TripReviewer.status_choices[faker.random_int(0, len(models.TripReviewer.status_choices) - 1)][0])
    user = factory.SubFactory(UserFactory)
    order = factory.lazy_attribute(lambda o: faker.pyint(1, 10))

    @staticmethod
    def get_valid_data():
        return {
            'trip': TripFactory().id,
            'user': UserFactory().id,
            'role': models.TripReviewer.role_choices[faker.random_int(0, len(models.TripReviewer.role_choices) - 1)][0],
            'status': models.TripReviewer.status_choices[faker.random_int(0, len(models.TripReviewer.status_choices) - 1)][0],
            'order': faker.pyint(1, 10),
        }


class FileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.File

    request = factory.SubFactory(TripRequestFactory)
    name = factory.lazy_attribute(lambda o: faker.catch_phrase())

    @staticmethod
    def get_valid_data():
        return {
            'request': TripRequestFactory().id,
            'name': faker.catch_phrase(),
        }


class ProcessStepFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProcessStep

    name = factory.lazy_attribute(lambda o: faker.catch_phrase())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    stage = factory.lazy_attribute(lambda o: faker.pyint(0, 2))
    is_visible = factory.lazy_attribute(lambda o: faker.pybool())

    @staticmethod
    def get_valid_data():
        return {
            'name': faker.catch_phrase(),
            'description_en': faker.text(),
            'stage': faker.pyint(1, 100),
            'is_visible': faker.pybool(),
        }


class FAQFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FAQ

    question_en = factory.lazy_attribute(lambda o: faker.text())
    answer_en = factory.lazy_attribute(lambda o: faker.text())

    @staticmethod
    def get_valid_data():
        return {
            'question_en': faker.text(),
            'answer_en': faker.text(),
        }


class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Role

    name = factory.lazy_attribute(lambda o: faker.catch_phrase())

    @staticmethod
    def get_valid_data():
        return {
            'name': faker.catch_phrase(),
        }


class TravellerCostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TravellerCost

    traveller = factory.SubFactory(TravellerFactory)
    cost = factory.lazy_attribute(lambda o: models.Cost.objects.all()[faker.random_int(0, models.Cost.objects.count() - 1)])
    amount_cad = factory.lazy_attribute(lambda o: faker.pyint(1000, 5000))

    @staticmethod
    def get_valid_data():
        return {
            'traveller': TravellerFactory().id,
            'cost': models.Cost.objects.all()[faker.random_int(0, models.Cost.objects.count() - 1)].id,
            'amount_cad': faker.pyint(1000, 5000),
        }


class HelpTextFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.HelpText

    field_name = factory.lazy_attribute(lambda o: faker.word())
    eng_text = factory.lazy_attribute(lambda o: faker.text())

    @staticmethod
    def get_valid_data():
        return {
            'field_name': faker.word(),
            'eng_text': faker.text(),
        }
