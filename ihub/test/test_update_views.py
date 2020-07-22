from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import CreateView, UpdateView

from ihub.test import FactoryFloor
from ihub.test.common_tests import CommonIHubTest as CommonTest
from .. import views
from .. import models


class TestPersonUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.PersonFactory()
        self.test_url = reverse_lazy('ihub:person_edit', args=[self.instance.pk, ])
        self.test_url1 = reverse_lazy('ihub:person_edit_pop', args=[self.instance.pk, ])
        self.expected_template = 'ihub/person_form.html'
        self.expected_template1 = 'ihub/person_form_pop.html'
        self.user = self.get_and_login_user(in_group="ihub_edit")

    @tag("Person", "person_form", "view")
    def test_view_class(self):
        self.assert_inheritance(views.PersonUpdateView, UpdateView)
        self.assert_inheritance(views.PersonUpdateViewPopout, UpdateView)

    @tag("Person", "person_form", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)
        self.assert_not_broken(self.test_url1)
        self.assert_non_public_view(test_url=self.test_url1, expected_template=self.expected_template1, user=self.user)

    @tag("Person", "person_form", "submit")
    def test_submit(self):
        data = FactoryFloor.PersonFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)
        self.assert_success_url(self.test_url1, data=data, user=self.user)
