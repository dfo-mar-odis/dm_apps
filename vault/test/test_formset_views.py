from django.test import tag
from django.urls import reverse_lazy
from django.utils.translation import activate
from django.views.generic import TemplateView

from vault.test import FactoryFloor
from vault.test.common_tests import CommonVaultTest as CommonTest
from shared_models.views import CommonFormsetView, CommonHardDeleteView
from .FactoryFloor import InstrumentTypeFactory, InstrumentFactory, OrganisationFactory, ObservationPlatformFactory, \
    ObservationPlatformTypeFactory, RoleFactory, PersonFactory
from .. import views
from .. import models
from faker import Factory

faker = Factory.create()


class TestAllFormsets(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url_names = [
            "manage_instrument_type",
            "manage_instrument",
            "manage_organisation",
            # "manage_platform_type",
            "manage_platform",
            "manage_role",
            "manage_person",
        ]

        self.test_urls = [reverse_lazy("vault:" + name) for name in self.test_url_names]
        self.test_views = [
            views.InstrumentTypeFormsetView,
            views.InstrumentFormsetView,
            views.OrganisationFormsetView,
            # views.ObservationPlatformTypeFormsetView,
            views.ObservationPlatformFormsetView,
            views.RoleFormsetView,
            views.PersonFormsetView,
        ]
        self.expected_template = 'vault/formset.html'
        self.user = self.get_and_login_user(in_group="vault_admin")

    @tag('formsets', "view")
    def test_view_class(self):
        for v in self.test_views:
            self.assert_inheritance(v, CommonFormsetView)
            self.assert_inheritance(v, views.VaultAdminAccessRequired)

    @tag('formsets', "access")
    def test_view(self):
        for url in self.test_urls:
            self.assert_good_response(url)
            self.assert_non_public_view(test_url=url, expected_template=self.expected_template, user=self.user)

    @tag('formsets', "submit")
    def test_submit(self):
        data = dict()  # should be fine to submit with empty data
        for url in self.test_urls:
            self.assert_success_url(url, data=data)


#TODO find out why this fails.. to do with Person model (role needs to be changed to non mandatory?)
class TestAllHardDeleteViews(CommonTest):
    def setUp(self):
        super().setUp()
        self.starter_dicts = [
            {"model": models.InstrumentType, "url_name": "delete_instrument_type",
             "view": views.InstrumentTypeHardDeleteView},
            {"model": models.Instrument, "url_name": "delete_instrument", "view": views.InstrumentHardDeleteView},
            {"model": models.Organisation, "url_name": "delete_organisation", "view": views.OrganisationHardDeleteView},
            # {"model": models.ObservationPlatformType, "url_name": "delete_platform_type",
            #  "view": views.ObservationPlatformTypeHardDeleteView},
            {"model": models.ObservationPlatform, "url_name": "delete_platform", "view": views.ObservationPlatformHardDeleteView},
            {"model": models.Role, "url_name": "delete_role", "view": views.RoleHardDeleteView},
            {"model": models.Person, "url_name": "delete_instrument", "view": views.InstrumentHardDeleteView},
        ]
        self.test_dicts = list()

        self.user = self.get_and_login_user(in_group="vault_admin")
        for d in self.starter_dicts:
            new_d = d
            m = d["model"]
            if m == models.InstrumentType:
                obj = InstrumentTypeFactory()
            elif m == models.Instrument:
                obj = InstrumentFactory()
            elif m == models.Organisation:
                obj = OrganisationFactory()
            # elif m == models.ObservationPlatformType:
            #     obj = ObservationPlatformTypeFactory()
            elif m == models.ObservationPlatform:
                obj = ObservationPlatformFactory()
            elif m == models.Role:
                obj = RoleFactory()
            elif m == models.Person:
                obj = PersonFactory()
            else:
                obj = m.objects.create(name=faker.catch_phrase())
            new_d["obj"] = obj
            new_d["url"] = reverse_lazy("vault:" + d["url_name"], kwargs={"pk": obj.id})
            self.test_dicts.append(new_d)

    @tag('hard_delete', "view")
    def test_view_class(self):
        for d in self.test_dicts:
            self.assert_inheritance(d["view"], CommonHardDeleteView)
            self.assert_inheritance(d["view"], views.VaultAdminAccessRequired)

    @tag('hard_delete', "access")
    def test_view(self):
        for d in self.test_dicts:
            self.assert_good_response(d["url"])
            # only have one chance to test this url
            self.assert_non_public_view(test_url=d["url"], user=self.user, expected_code=302, locales=["en"])

    @tag('hard_delete', "delete")
    def test_delete(self):
        # need to be an admin user to do this
        self.get_and_login_user(user=self.user)
        for d in self.test_dicts:
            # start off to confirm the object exists
            self.assertIn(d["obj"], type(d["obj"]).objects.all())
            # visit the url
            activate("en")
            self.client.get(d["url"])
            # confirm the object has been deleted
            self.assertNotIn(d["obj"], type(d["obj"]).objects.all())
