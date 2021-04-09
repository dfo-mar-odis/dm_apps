from django.utils import timezone
from django.utils.translation import activate
from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import DetailView, UpdateView

from shared_models.views import CommonDetailView, CommonUpdateView, CommonPopoutUpdateView
from vault.test import FactoryFloor
from vault.test.common_tests import CommonVaultTest as CommonTest
from .. import views
from .. import models


# Example how to run with keyword tags
# python manage.py test vault.test --tag species_edit


class TestSpeciesUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.SpeciesFactory()
        self.test_url = reverse_lazy('vault:species_edit', args=[self.instance.pk, ])
        self.expected_template = 'vault/form.html'
        self.user = self.get_and_login_user(in_group="vault_admin")

    @tag("Species", "species_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.SpeciesUpdateView, CommonUpdateView)
        self.assert_inheritance(views.SpeciesUpdateView, views.VaultAdminAccessRequired)

    @tag("Species", "species_edit", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Species", "species_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.SpeciesFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    @tag("Species", "species_edit", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("vault:species_edit", f"/en/vault/species/{self.instance.pk}/edit/", [self.instance.pk])


class TestOutingUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.OutingFactory()
        self.test_url = reverse_lazy('vault:outing_edit', args=[self.instance.pk, ])
        self.expected_template = 'vault/outing_form.html'
        self.user = self.get_and_login_user(in_group="vault_admin")

    @tag("Outing", "outing_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.OutingUpdateView, CommonUpdateView)
        self.assert_inheritance(views.OutingUpdateView, views.VaultAdminAccessRequired)

    @tag("Outing", "outing_edit", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Outing", "outing_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.OutingFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    @tag("Outing", "outing_edit", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("vault:outing_edit", f"/en/vault/outing/{self.instance.pk}/edit/", [self.instance.pk])