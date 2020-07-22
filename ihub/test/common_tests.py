import os
from django.test import TestCase
from django.urls import reverse_lazy, resolve
from django.utils.translation import activate
from shared_models.test.SharedModelsFactoryFloor import UserFactory, GroupFactory
from shared_models.test.common_tests import CommonTest

fixtures_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fixtures')
standard_fixtures = [file for file in os.listdir(fixtures_dir)]


# here are common tests for Travel. Essentially they will just load the travel fixutres
class CommonIHubTest(CommonTest):
    fixtures = standard_fixtures
