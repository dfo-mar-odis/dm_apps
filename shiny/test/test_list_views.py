from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import ListView
from django_filters.views import FilterView

from shared_models.views import CommonFilterView
from .. import models
from .. import views

from shiny.test.common_tests import CommonShinyTest as CommonTest
from shiny.test import FactoryFloor

class TestAppListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.AppFactory()
        self.test_url = reverse_lazy('shiny:index')
        self.expected_template = 'shiny/index.html'

    @tag("shiny", 'list', "view")
    def test_view_class(self):
        self.assert_inheritance(views.IndexTemplateView, CommonFilterView)

    @tag("shiny", 'list', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_public_view(test_url=self.test_url, expected_template=self.expected_template)

    @tag("shiny", 'list', "context")
    def test_context(self):
        context_vars = [
            "field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars)
