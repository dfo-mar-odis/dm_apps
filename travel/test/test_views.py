from django.test import tag
from django.urls import reverse_lazy
from django.utils.translation import activate

from travel.test import FactoryFloor
from travel.test.common_tests import CommonTravelTest as CommonTest


###########################################################################################
# Index View is a bit different from most views as it is basically just a landing page
###########################################################################################


class TestIndexView(CommonTest):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('travel:index')
        self.expected_template = 'travel/index.html'

    # Users should be able to view the travel index page corresponding to the travel/index.html template, in French
    @tag("index")
    def test_access(self):
        # only logged in users can access the landing
        super().assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template)

    # The index view should return a context to be used on the index.html template
    # this should consist of a "Sections" dictionary containing sub-sections

    @tag("index", "context")
    def test_context(self):
        context_vars = [
            "user_trip_requests",

            "tr_reviews_waiting",
            "trip_reviews_waiting",
            "reviews_waiting",
            "is_reviewer",
            "is_tr_reviewer",
            "is_trip_reviewer",
            "is_admin",
            "is_adm_admin",
            "tab_dict",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars)

        activate('en')
        reg_user = self.get_and_login_user()
        response = self.client.get(self.test_url)
        # a regular user should not be an admin or a reviewer
        self.assertEqual(response.context["is_admin"], False)
        self.assertEqual(response.context["is_reviewer"], False)

        # if a regular user is also a reviewer, the 'is_reviewer' var should be true
        FactoryFloor.ReviewerFactory(user=reg_user)
        response = self.client.get(self.test_url)
        self.assertEqual(response.context["is_reviewer"], True)

        # an admin user should be identified as such by the `is_admin` var in the template
        self.client.logout()
        admin_user = self.get_and_login_user(in_group="travel_admin")
        response = self.client.get(self.test_url)
        self.assertEqual(response.context["is_admin"], True)

        # an adm admin user should be identified as such by the `is_adm_admin` var in the template
        self.client.logout()
        admin_user = self.get_and_login_user(in_group="travel_adm_admin")
        response = self.client.get(self.test_url)
        self.assertEqual(response.context["is_adm_admin"], True)