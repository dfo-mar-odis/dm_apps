from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import DeleteView

from .. import models
from masterlist import models as ml_models
from .. import views
from ihub.test.common_tests import CommonIHubTest as CommonTest
from ihub.test import FactoryFloor

class TestPersonDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.PersonFactory()
        self.test_url = reverse_lazy('ihub:person_delete', args=[self.instance.pk, ])
        self.expected_template = 'ihub/person_confirm_delete.html'
        self.user = self.get_and_login_user(in_group="ihub_edit")

    @tag("Person", "person_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.PersonDeleteView, DeleteView)

    @tag("Person", "person_delete", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)
        self.assert_public_view(test_url=self.test_url, expected_template=self.expected_template)

    @tag("Person", "person_delete", "context")
    def test_context(self):
        context_vars = [
            "field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    @tag("Person", "person_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.PersonFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(ml_models.Person.objects.filter(pk=self.instance.pk).count(), 0)