from django.test import tag
from django.urls import reverse_lazy
from django.utils.translation import activate

from shared_models.test.common_tests import CommonTest
from ..test import FactoryFloor
from shared_models.views import CommonFormsetView, CommonHardDeleteView
from ..views import biofouling_views
from .. import models
from faker import Factory

faker = Factory.create()


class TestAllFormsets(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url_names = [
            "manage_filtration_types",
            "manage_dna_extraction_protocols",
            "manage_tags",
        ]

        self.test_urls = [reverse_lazy("edna:" + name) for name in self.test_url_names]
        self.test_views = [
            biofouling_views.FiltrationTypeFormsetView,
            biofouling_views.DNAExtractionProtocolFormsetView,
            biofouling_views.TagFormsetView,
        ]
        self.expected_template = 'edna/formset.html'
        self.user = self.get_and_login_user(in_group="edna_admin")

    @tag('formsets', "view")
    def test_view_class(self):
        for v in self.test_views:
            self.assert_inheritance(v, biofouling_views.eDNAAdminRequiredMixin)
            self.assert_inheritance(v, CommonFormsetView)

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
            {"model": models.FiltrationType, "url_name": "delete_filtration_type", "view": biofouling_views.FiltrationTypeHardDeleteView},
            {"model": models.DNAExtractionProtocol, "url_name": "delete_dna_extraction_protocol", "view": biofouling_views.DNAExtractionProtocolHardDeleteView},
            {"model": models.Tag, "url_name": "delete_tag", "view": biofouling_views.TagHardDeleteView},
        ]
        self.test_dicts = list()

        self.user = self.get_and_login_user(in_group="edna_admin")
        for d in self.starter_dicts:
            new_d = d
            m = d["model"]
            if m == models.FiltrationType:
                obj = FactoryFloor.FiltrationTypeFactory()
            elif m == models.DNAExtractionProtocol:
                obj = FactoryFloor.DNAExtractionProtocolFactory()
            elif m == models.Tag:
                obj = FactoryFloor.TagFactory()
            else:
                obj = m.objects.create(name=faker.word())
            new_d["obj"] = obj
            new_d["url"] = reverse_lazy("edna:" + d["url_name"], kwargs={"pk": obj.id})
            self.test_dicts.append(new_d)

    @tag('hard_delete', "view")
    def test_view_class(self):
        for d in self.test_dicts:
            self.assert_inheritance(d["view"], biofouling_views.eDNAAdminRequiredMixin)
            self.assert_inheritance(d["view"], CommonHardDeleteView)

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
