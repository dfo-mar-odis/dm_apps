from django.test import tag
from django.urls import reverse_lazy
from django.utils.translation import activate
from django.views.generic import TemplateView

from whalebrary.test import FactoryFloor
from whalebrary.test.common_tests import CommonWhalebraryTest as CommonTest
from shared_models.views import CommonFormsetView, CommonHardDeleteView
from .. import views
from .. import models
from faker import Factory

faker = Factory.create()


class TestAllFormsets(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url_names = [
            "manage_locations",
            "manage_tags",
            "manage_species",
        ]

        self.test_urls = [reverse_lazy("whalebrary:" + name) for name in self.test_url_names]
        self.test_views = [
            views.LocationFormsetView,
            views.TagFormsetView,
            views.SpeciesFormsetView,
        ]
        self.expected_template = 'whalebrary/formset.html'
        self.user = self.get_and_login_user(in_group="whalebrary_admin")

    @tag('formsets', "view")
    def test_view_class(self):
        for v in self.test_views:
            self.assert_inheritance(v, CommonFormsetView)
            self.assert_inheritance(v, views.WhalebraryAdminAccessRequired)

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


class TestAllHardDeleteViews(CommonTest):
    def setUp(self):
        super().setUp()
        self.starter_dicts = [
            {"model": models.Location, "url_name": "delete_location", "view": views.LocationHardDeleteView},
            {"model": models.Tag, "url_name": "delete_tag", "view": views.TagHardDeleteView},
            {"model": models.Species, "url_name": "delete_species", "view": views.SpeciesHardDeleteView},
        ]
        self.test_dicts = list()

        self.user = self.get_and_login_user(in_group="whalebrary_admin")
        for d in self.starter_dicts:
            new_d = d
            m = d["model"]
            if m == models.Location:
                obj = m.objects.create(location=faker.catch_phrase(), bin_id=faker.catch_phrase())
            elif m == models.Tag:
                obj = m.objects.create(tag=faker.catch_phrase())
            elif m == models.Species:
                obj = m.objects.create(name=faker.catch_phrase())
            else:
                obj = m.objects.create(name=faker.catch_phrase())
            new_d["obj"] = obj
            new_d["url"] = reverse_lazy("whalebrary:" + d["url_name"], kwargs={"pk": obj.id})
            self.test_dicts.append(new_d)

    @tag('hard_delete', "view")
    def test_view_class(self):
        for d in self.test_dicts:
            self.assert_inheritance(d["view"], CommonHardDeleteView)
            self.assert_inheritance(d["view"], views.WhalebraryAdminAccessRequired)

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



# class TestAllFormsets(CommonTest):
#     def setUp(self):
#         super().setUp()
#         self.test_url_names = [
#             "manage_statuses",
#             "manage_help_text",
#             "manage_cost_categories",
#             "manage_costs",
#             "manage_njc_rates",
#             "manage_trip_subcategories",
#             "manage_trip_categories",
#             # "manage_reasons",
#         ]
#
#         self.test_urls = [reverse_lazy("travel:" + name) for name in self.test_url_names]
#         self.test_views = [
#             views.StatusFormsetView,
#             views.HelpTextFormsetView,
#             views.CostCategoryFormsetView,
#             views.CostFormsetView,
#             views.NJCRatesFormsetView,
#             views.TripSubcategoryFormsetView,
#             views.TripCategoryFormsetView,
#             # views.ReasonFormsetView,
#         ]
#         self.expected_template = 'travel/formset.html'
#         self.user = self.get_and_login_user(in_group="travel_admin")
#
#     @tag('formsets', "view")
#     def test_view_class(self):
#         for v in self.test_views:
#             self.assert_inheritance(v, views.TravelAdminRequiredMixin)
#             self.assert_inheritance(v, CommonFormsetView)
#
#     @tag('formsets', "access")
#     def test_view(self):
#         for url in self.test_urls:
#             self.assert_good_response(url)
#             self.assert_non_public_view(test_url=url, expected_template=self.expected_template, user=self.user)
#
#     @tag('formsets', "submit")
#     def test_submit(self):
#         data = dict()  # should be fine to submit with empty data
#         for url in self.test_urls:
#             self.assert_success_url(url, data=data)
#
#
# class TestAllHardDeleteViews(CommonTest):
#     def setUp(self):
#         super().setUp()
#         self.starter_dicts = [
#             {"model": models.HelpText, "url_name": "delete_help_text", "view": views.HelpTextHardDeleteView},
#             {"model": models.Cost, "url_name": "delete_cost", "view": views.CostHardDeleteView},
#             {"model": models.CostCategory, "url_name": "delete_cost_category", "view": views.CostCategoryHardDeleteView},
#             {"model": models.TripSubcategory, "url_name": "delete_trip_subcategory", "view": views.TripSubcategoryHardDeleteView},
#             # {"model": models.Reason, "url_name": "delete_reason", "view": views.ReasonHardDeleteView},
#         ]
#         self.test_dicts = list()
#
#         self.user = self.get_and_login_user(in_group="travel_admin")
#         for d in self.starter_dicts:
#             new_d = d
#             m = d["model"]
#             if m == models.HelpText:
#                 obj = m.objects.create(field_name=faker.word(), eng_text=faker.word())
#             elif m == models.Cost:
#                 cc = models.CostCategory.objects.all()[faker.random_int(0, models.CostCategory.objects.count() - 1)]
#                 obj = m.objects.create(name=faker.word(), cost_category=cc)
#             elif m == models.TripSubcategory:
#                 tc = models.TripCategory.objects.all()[faker.random_int(0, models.TripCategory.objects.count() - 1)]
#                 obj = m.objects.create(name=faker.word(), trip_category=tc)
#             else:
#                 obj = m.objects.create(name=faker.word())
#             new_d["obj"] = obj
#             new_d["url"] = reverse_lazy("travel:" + d["url_name"], kwargs={"pk": obj.id})
#             self.test_dicts.append(new_d)
#
#     @tag('hard_delete', "view")
#     def test_view_class(self):
#         for d in self.test_dicts:
#             self.assert_inheritance(d["view"], views.TravelAdminRequiredMixin)
#             self.assert_inheritance(d["view"], CommonHardDeleteView)
#
#     @tag('hard_delete', "access")
#     def test_view(self):
#         for d in self.test_dicts:
#             self.assert_good_response(d["url"])
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
