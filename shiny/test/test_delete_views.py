from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import DeleteView

from shared_models.views import CommonDeleteView
from .. import models
from .. import views
from shiny.test.common_tests import CommonShinyTest as CommonTest
from shiny.test import FactoryFloor



class TestAppDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.AppFactory()
        self.test_url = reverse_lazy('shiny:delete', kwargs={"pk":self.instance.pk})
        self.expected_template = 'shared_models/generic_confirm_delete.html'

    @tag("shiny", 'delete', "view")
    def test_view_class(self):
        self.assert_inheritance(views.AppDeleteView, CommonDeleteView)

    @tag("shiny", 'delete', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template)

    @tag("shiny", 'delete', "submit")
    def test_submit(self):
        data = FactoryFloor.AppFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data)

        # for delete views...
        self.assertEqual(models.App.objects.filter(pk=self.instance.pk).count(), 0)