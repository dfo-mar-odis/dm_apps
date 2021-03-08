import os

from django.contrib.auth.models import Group

from shared_models.test.common_tests import CommonTest

fixtures_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fixtures')
standard_fixtures = [file for file in os.listdir(fixtures_dir)]


# here are common tests for Travel. Essentially they will just load the travel fixutres
class CommonTravelTest(CommonTest):
    fixtures = standard_fixtures

    def setUp(self):
        super().setUp()
        Group.objects.get_or_create(name="travel_admin")
        Group.objects.get_or_create(name="travel_adm_admin")
