from django.test import tag
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import activate

from projects.test import FactoryFloor
from projects.test.common_tests import CommonProjectTest as CommonTest
from shared_models.views import CommonFormsetView, CommonHardDeleteView
from .. import views
from .. import models
from faker import Factory

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


#
# class TestAllHardDeleteViews(CommonTest):
#     def setUp(self):
#         super().setUp()
#         self.starter_dicts = [
#             {"model": models.FundingSource, "url_name": "delete_funding_source", "view": views.FundingSourceHardDeleteView},
#             {"model": models.ActivityType, "url_name": "delete_activity_type", "view": views.ActivityTypeHardDeleteView},
#             {"model": models.OMCategory, "url_name": "delete_om_cat", "view": views.OMCategoryHardDeleteView},
#             {"model": models.EmployeeType, "url_name": "delete_employee_type", "view": views.EmployeeTypeHardDeleteView},
#             {"model": models.Status, "url_name": "delete_status", "view": views.StatusHardDeleteView},
#             {"model": models.Tag, "url_name": "delete_tag", "view": views.TagHardDeleteView},
#             {"model": models.HelpText, "url_name": "delete_help_text", "view": views.HelpTextHardDeleteView},
#             {"model": models.Level, "url_name": "delete_level", "view": views.LevelHardDeleteView},
#             {"model": models.Program, "url_name": "delete_program", "view": views.ProgramHardDeleteView},
#             {"model": models.Theme, "url_name": "delete_theme", "view": views.ThemeHardDeleteView},
#             {"model": models.UpcomingDate, "url_name": "delete-upcoming-date", "view": views.UpcomingDateHardDeleteView},
#         ]
#         self.test_dicts = list()
#
#         self.user = self.get_and_login_user(in_group="projects_admin")
#         for d in self.starter_dicts:
#             new_d = d
#             m = d["model"]
#             if m == models.FundingSource:
#                 obj = FactoryFloor.FundingSourceFactory()
#             elif m == models.OMCategory:
#                 obj = m.objects.create(name=faker.word(), group=1)
#             elif m == models.EmployeeType:
#                 obj = m.objects.create(name=faker.word(), cost_type=1)
#             elif m == models.Status:
#                 obj = m.objects.create(name=faker.word(), used_for=1)
#             elif m == models.HelpText:
#                 obj = m.objects.create(field_name=faker.word(), eng_text=faker.word())
#             elif m == models.Program:
#                 obj = m.objects.create(regional_program_name_eng=faker.word(), is_core=True)
#             elif m == models.UpcomingDate:
#                 obj = FactoryFloor.UpcomingDateFactory()
#             else:
#                 obj = m.objects.create(name=faker.word())
#             new_d["obj"] = obj
#             new_d["url"] = reverse_lazy("projects:" + d["url_name"], kwargs={"pk": obj.id})
#             self.test_dicts.append(new_d)
#
#     @tag('hard_delete', "view")
#     def test_view_class(self):
#         for d in self.test_dicts:
#             self.assert_inheritance(d["view"], views.AdminRequiredMixin)
#             self.assert_inheritance(d["view"], CommonHardDeleteView)
#
#     @tag('hard_delete', "access")
#     def test_view(self):
#         for d in self.test_dicts:
#             self.assert_not_broken(d["url"])
#             # only have one chance to test this url
#             self.assert_non_public_view(test_url=d["url"], user=self.user, expected_code=302, locales=["en"])
#
#     @tag('hard_delete', "delete")
#     def test_delete(self):
#         # need to be an admin user to do this
#         self.get_and_login_user(user=self.user)
#         for d in self.test_dicts:
#             # start off to confirm the object exists
#             self.assertIn(d["obj"], type(d["obj"]).objects.all())
#             # visit the url
#             activate("en")
#             self.client.get(d["url"])
#             # confirm the object has been deleted
#             self.assertNotIn(d["obj"], type(d["obj"]).objects.all())
