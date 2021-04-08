import os

from shared_models.test.common_tests import CommonTest

fixtures_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fixtures')
standard_fixtures = [file for file in os.listdir(fixtures_dir)]


# here are common tests for Fisheriescape. Essentially they will just load the fisheriescape fixtures
class CommonFisheriescapeTest(CommonTest):
    fixtures = standard_fixtures
