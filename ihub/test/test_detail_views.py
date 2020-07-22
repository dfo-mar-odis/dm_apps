from django.utils import timezone
from django.utils.translation import activate
from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import DetailView, UpdateView
from easy_pdf.views import PDFTemplateView

from ihub.test import FactoryFloor
from ihub.test.common_tests import CommonIHubTest as CommonTest
from .. import views

class TestPersonDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.PersonFactory()
        self.test_url = reverse_lazy('ihub:person_detail', args=[self.instance.pk, ])
        self.expected_template = 'ihub/person_detail.html'
        self.user = self.get_and_login_user()

    @tag("Person", "person_detail", "view")
    def test_view_class(self):
        self.assert_inheritance(views.PersonDetailView, DetailView)

    @tag("Person", "person_detail", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Person", "person_detail", "context")
    def test_context(self):
        context_vars = [
            "field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)
