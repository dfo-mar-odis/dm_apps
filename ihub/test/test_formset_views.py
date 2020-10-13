from django.test import tag
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import activate

from ihub.test import FactoryFloor
from ihub.test.common_tests import CommonIHubTest as CommonTest
from shared_models.views import CommonFormsetView, CommonHardDeleteView
from .. import views
from .. import models
from faker import Factory
from masterlist import models as ml_models

faker = Factory.create()


class TestAllFormsets(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url_names = [
            "manage_sectors",
            "manage_statuses",
            "manage_entry_types",
            "manage_funding_purposes",
            "manage_reserves",
            "manage_nations",
            "manage_programs",
            "manage_ratings",
        ]

        self.test_urls = [reverse_lazy("ihub:" + name) for name in self.test_url_names]
        self.test_views = [
            views.SectorFormsetView,
            views.StatusFormsetView,
            views.EntryTypeFormsetView,
            views.FundingPurposeFormsetView,
            views.ReserveFormsetView,
            views.NationFormsetView,
            views.FundingProgramFormsetView,
            views.RelationshipRatingFormsetView,
        ]
        self.expected_template = 'ihub/formset.html'
        self.user = self.get_and_login_user(in_group="ihub_admin")

    @tag('formsets', "view")
    def test_view_class(self):
        for v in self.test_views:
            self.assert_inheritance(v, views.iHubAdminRequiredMixin)
            self.assert_inheritance(v, CommonFormsetView)

    @tag('formsets', "access")
    def test_view(self):
        for url in self.test_urls:
            self.assert_not_broken(url)
            self.assert_non_public_view(test_url=url, expected_template=self.expected_template, user=self.user)

    @tag('formsets', "submit")
    def test_submit(self):
        data = dict()  # should be fine to submit with empty data
        for url in self.test_urls:
            self.assert_success_url(url, data=data)


class TestOrgFormset(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url_names = [
            "manage_orgs",
        ]

        self.test_urls = [reverse_lazy("ihub:" + name) for name in self.test_url_names]
        self.test_views = [
            views.OrganizationFormsetView,
        ]
        self.expected_template = 'ihub/organization_formset.html'
        self.user = self.get_and_login_user(in_group="ihub_admin")

    @tag('formsets', "view")
    def test_view_class(self):
        for v in self.test_views:
            self.assert_inheritance(v, views.iHubAdminRequiredMixin)
            self.assert_inheritance(v, CommonFormsetView)

    @tag('formsets', "access")
    def test_view(self):
        for url in self.test_urls:
            self.assert_not_broken(url)
            self.assert_non_public_view(test_url=url, expected_template=self.expected_template, user=self.user)

    @tag('formsets', "submit")
    def test_submit(self):
        data = dict()  # should be fine to submit with empty data
        for url in self.test_urls:
            self.assert_success_url(url, data=data)


class TestAllHardDeleteViews(CommonTest):
    def setUp(self):
        super().setUp()
        self.starter_dicts = [
            {"model": ml_models.Sector, "url_name": "delete_sector", "view": views.SectorHardDeleteView},
            {"model": models.Status, "url_name": "delete_status", "view": views.StatusHardDeleteView},
            {"model": models.EntryType, "url_name": "delete_entry_type", "view": views.EntryTypeHardDeleteView},
            {"model": models.FundingPurpose, "url_name": "delete_funding_purpose", "view": views.FundingPurposeHardDeleteView},
            {"model": ml_models.Reserve, "url_name": "delete_reserve", "view": views.ReserveHardDeleteView},
            {"model": ml_models.Nation, "url_name": "delete_nation", "view": views.NationHardDeleteView},
            {"model": models.FundingProgram, "url_name": "delete_program", "view": views.FundingProgramHardDeleteView},
            {"model": ml_models.RelationshipRating, "url_name": "delete_rating", "view": views.RelationshipRatingHardDeleteView},
        ]
        self.test_dicts = list()

        self.user = self.get_and_login_user(in_group="ihub_admin")
        for d in self.starter_dicts:
            new_d = d
            m = d["model"]
            if m == ml_models.Sector:
                obj = FactoryFloor.SectorFactory()
            elif m == ml_models.RelationshipRating:
                obj = m.objects.create(name=faker.catch_phrase(), level=faker.pyint(1,100))
            else:
                obj = m.objects.create(name=faker.catch_phrase())
            new_d["obj"] = obj
            new_d["url"] = reverse_lazy("ihub:" + d["url_name"], kwargs={"pk": obj.id})
            self.test_dicts.append(new_d)

    @tag('hard_delete', "view")
    def test_view_class(self):
        for d in self.test_dicts:
            self.assert_inheritance(d["view"], views.iHubAdminRequiredMixin)
            self.assert_inheritance(d["view"], CommonHardDeleteView)

    @tag('hard_delete', "access")
    def test_view(self):
        for d in self.test_dicts:
            self.assert_not_broken(d["url"])
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
