from django.urls import reverse_lazy
from django.test import tag

from shared_models.views import CommonCreateView
from vault import views
from vault.test import FactoryFloor
from vault.test.common_tests import CommonVaultTest as CommonTest

# Example how to run with keyword tags
# python manage.py test vault.test --tag species_new


class TestSpeciesCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.SpeciesFactory()
        self.test_url = reverse_lazy('vault:species_new')
        self.expected_template = 'vault/form.html'
        self.user = self.get_and_login_user(in_group="vault_admin")

    @tag("Species", "species_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.SpeciesCreateView, CommonCreateView)
        self.assert_inheritance(views.SpeciesCreateView, views.VaultAdminAccessRequired)

    @tag("Species", "species_new", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Species", "species_new", "submit")
    def test_submit(self):
        data = FactoryFloor.SpeciesFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestOutingCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.OutingFactory()
        self.test_url = reverse_lazy('vault:outing_new')
        self.expected_template = 'vault/outing_form.html'
        self.user = self.get_and_login_user(in_group="vault_admin")

    @tag("Outing", "outing_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.OutingCreateView, CommonCreateView)
        self.assert_inheritance(views.OutingCreateView, views.VaultAdminAccessRequired)

    @tag("Outing", "outing_new", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Outing", "outing_new", "submit")
    def test_submit(self):
        data = FactoryFloor.OutingFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)
