from django.test import tag
from django.urls import reverse_lazy
from django.utils.translation import activate
from django.views.generic import TemplateView

from ihub.test import FactoryFloor
from ihub.test.common_tests import CommonIHubTest as CommonTest
from .. import views

class TestIndexTemplateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('ihub:index')
        self.expected_template = 'ihub/index.html'
        self.user = self.get_and_login_user()

    @tag("Index", "index", "view")
    def test_view_class(self):
        self.assert_inheritance(views.IndexTemplateView, TemplateView)

    @tag("Index", "index", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

