from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import CreateView, UpdateView

from shared_models.views import CommonUpdateView
from shiny.test import FactoryFloor
from shiny.test.common_tests import CommonShinyTest as CommonTest
from .. import views

class TestAppUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.AppFactory()
        self.test_url = reverse_lazy('shiny:update', kwargs={"pk":self.instance.pk})
        self.expected_template = 'shared_models/generic_form.html'

    @tag("shiny", 'update', "view")
    def test_view_class(self):
        self.assert_inheritance(views.AppUpdateView, CommonUpdateView)

    @tag("shiny", 'update', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template)

    @tag("shiny", 'update', "submit")
    def test_submit(self):
        data = FactoryFloor.AppFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data)
