from django.test import tag, RequestFactory
from django.urls import reverse_lazy
from faker import Faker
from datetime import date

from bio_diversity.test import BioFactoryFloor
# from cruises.test.common_tests import CommonCruisesTest as CommonTest
from shared_models.test.common_tests import CommonTest

# from bio_diversity.models import Cruise
# from shared_models.test.SharedModelsFactoryFloor import CruiseFactory
from bio_diversity.views import CommonCreate, CommonDetails, CommonList, CommonUpdate
from .. import views

faker = Faker()


# This is used to simulate calling the as_veiw() function normally called in the urls.py
# this will return a view that can then have it's internal methods tested
def setup_view(view, request, *args, **kwargs):
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class MockCommonCreate(views.CommonCreate):
    pass


@tag('CreateCommon')
class TestCommonCreate(CommonTest):

    def setUp(self):
        self.view = MockCommonCreate()

    def test_get_init(self):
        # test created_by field auto population
        req_faq = RequestFactory()
        request = req_faq.get(None)

        # create and login a user to be expected by the inital function
        user = self.get_and_login_user(in_group="bio_diversity_admin")
        request.user = user

        setup_view(self.view, request)

        init = self.view.get_initial()
        self.assertIsNotNone(init)
        self.assertEqual(init['created_by'], user.username)
        self.assertEqual(init['created_by'], user.username)
        self.assertEqual(init['created_date'], date.today)
        self.assertEqual(init['start_date'], date.today)


@tag("Anidc")
class TestAnidcCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.AnidcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_anidc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.AnidcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.AnidcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_anidc", "/en/bio_diversity/create/anidc/")


@tag("Anidc")
class TestAnidcDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.AnidcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_anidc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.AnidcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "min_val",
            "max_val",
            "unit_id",
            "ani_subj_flag",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_anidc", f"/en/bio_diversity/details/anidc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Anidc")
class TestAnidcListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_anidc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.AnidcList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_anidc", f"/en/bio_diversity/list/anidc/")


@tag("Anidc")
class AnidcUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.AnidcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_anidc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.AnidcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.AnidcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_anidc", f"/en/bio_diversity/update/anidc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Adsc")
class TestAdscCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.AdscFactory()
        self.test_url = reverse_lazy('bio_diversity:create_adsc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.AdscCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.AdscFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_adsc", "/en/bio_diversity/create/adsc/")


@tag("Adsc")
class TestAdscDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.AdscFactory()
        self.test_url = reverse_lazy('bio_diversity:details_adsc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.AdscDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "anidc_id",
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_adsc", f"/en/bio_diversity/details/adsc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Adsc")
class TestAdscListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_adsc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.AdscList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_adsc", f"/en/bio_diversity/list/adsc/")


@tag("Adsc")
class AdscUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.AdscFactory()
        self.test_url = reverse_lazy('bio_diversity:update_adsc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.AdscUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.AdscFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_adsc", f"/en/bio_diversity/update/adsc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cnt")
class TestCntCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CntFactory()
        self.test_url = reverse_lazy('bio_diversity:create_cnt')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.CntCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CntFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_cnt", "/en/bio_diversity/create/cnt/")


@tag("Cnt")
class TestCntDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CntFactory()
        self.test_url = reverse_lazy('bio_diversity:details_cnt', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.CntDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "loc_id",
            "contx_id",
            "cntc_id",
            "spec_id",
            "cnt",
            "est",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_cnt", f"/en/bio_diversity/details/cnt/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cnt")
class TestCntListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_cnt')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.CntList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_cnt", f"/en/bio_diversity/list/cnt/")


@tag("Cnt")
class CntUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CntFactory()
        self.test_url = reverse_lazy('bio_diversity:update_cnt', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.CntUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CntFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_cnt", f"/en/bio_diversity/update/cnt/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cntc")
class TestCntcCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CntcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_cntc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.CntcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CntcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_cntc", "/en/bio_diversity/create/cntc/")


@tag("Cntc")
class TestCntcDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CntcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_cntc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.CntcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_cntc", f"/en/bio_diversity/details/cntc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cntc")
class TestCntcListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_cntc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.CntcList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_cntc", f"/en/bio_diversity/list/cntc/")


@tag("Cntc")
class CntcUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CntcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_cntc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.CntcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CntcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_cntc", f"/en/bio_diversity/update/cntc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cntd")
class TestCntdCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CntdFactory()
        self.test_url = reverse_lazy('bio_diversity:create_cntd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.CntdCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CntdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_cntd", "/en/bio_diversity/create/cntd/")


@tag("Cntd")
class TestCntdDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CntdFactory()
        self.test_url = reverse_lazy('bio_diversity:details_cntd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.CntdDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "cnt_id",
            "anidc_id",
            "det_val",
            "adsc_id",
            "qual_id",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_cntd", f"/en/bio_diversity/details/cntd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cntd")
class TestCntdListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_cntd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_cntd", f"/en/bio_diversity/list/cntd/")


@tag("Cntd")
class CntdUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CntdFactory()
        self.test_url = reverse_lazy('bio_diversity:update_cntd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CntdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_cntd", f"/en/bio_diversity/update/cntd/{self.instance.pk}/",
                                [self.instance.pk])



@tag("Coll")
class TestCollCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CollFactory()
        self.test_url = reverse_lazy('bio_diversity:create_coll')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.CollCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CollFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_coll", "/en/bio_diversity/create/coll/")


@tag("Coll")
class TestCollDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CollFactory()
        self.test_url = reverse_lazy('bio_diversity:details_coll', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.CollDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_coll", f"/en/bio_diversity/details/coll/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Coll")
class TestCollListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_coll')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.CollList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_coll", f"/en/bio_diversity/list/coll/")


@tag("Coll")
class CollUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CollFactory()
        self.test_url = reverse_lazy('bio_diversity:update_coll', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.CollUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CollFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_coll", f"/en/bio_diversity/update/coll/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Contdc")
class TestContdcCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ContdcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_contdc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.ContdcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ContdcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_contdc", "/en/bio_diversity/create/contdc/")


@tag("Contdc")
class TestContdcDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ContdcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_contdc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.ContdcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Contdc", "details_contdc", "context")
    # def test_context(self):
    #     context_vars = [
    #         "contdcc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_contdc", f"/en/bio_diversity/details/contdc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Contdc")
class TestContdcListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_contdc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.ContdcList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_contdc", f"/en/bio_diversity/list/contdc/")


@tag("Contdc")
class ContdcUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ContdcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_contdc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.ContdcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ContdcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_contdc", f"/en/bio_diversity/update/contdc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Contx")
class TestContxCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ContxFactory()
        self.test_url = reverse_lazy('bio_diversity:create_contx')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.ContxCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ContxFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_contx", "/en/bio_diversity/create/contx/")


@tag("Contx")
class TestContxDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ContxFactory()
        self.test_url = reverse_lazy('bio_diversity:details_contx', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.ContxDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Contx", "details_contx", "context")
    # def test_context(self):
    #     context_vars = [
    #         "contxc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_contx", f"/en/bio_diversity/details/contx/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Contx")
class TestContxListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_contx')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.ContxList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_contx", f"/en/bio_diversity/list/contx/")


@tag("Contx")
class ContxUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ContxFactory()
        self.test_url = reverse_lazy('bio_diversity:update_contx', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.ContxUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ContxFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_contx", f"/en/bio_diversity/update/contx/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cdsc")
class TestCdscCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CdscFactory()
        self.test_url = reverse_lazy('bio_diversity:create_cdsc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.CdscCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CdscFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_cdsc", "/en/bio_diversity/create/cdsc/")


@tag("Cdsc")
class TestCdscDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CdscFactory()
        self.test_url = reverse_lazy('bio_diversity:details_cdsc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.CdscDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Cdsc", "details_cdsc", "context")
    # def test_context(self):
    #     context_vars = [
    #         "cdscc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_cdsc", f"/en/bio_diversity/details/cdsc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cdsc")
class TestCdscListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_cdsc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.CdscList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_cdsc", f"/en/bio_diversity/list/cdsc/")


@tag("Cdsc")
class CdscUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CdscFactory()
        self.test_url = reverse_lazy('bio_diversity:update_cdsc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.CdscUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CdscFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_cdsc", f"/en/bio_diversity/update/cdsc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cup")
class TestCupCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CupFactory()
        self.test_url = reverse_lazy('bio_diversity:create_cup')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.CupCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CupFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_cup", "/en/bio_diversity/create/cup/")


@tag("Cup")
class TestCupDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CupFactory()
        self.test_url = reverse_lazy('bio_diversity:details_cup', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.CupDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_cup", f"/en/bio_diversity/details/cup/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cup")
class TestCupListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_cup')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.CupList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_cup", f"/en/bio_diversity/list/cup/")


@tag("Cup")
class CupUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CupFactory()
        self.test_url = reverse_lazy('bio_diversity:update_cup', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.CupUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CupFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_cup", f"/en/bio_diversity/update/cup/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cupd")
class TestCupdCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CupdFactory()
        self.test_url = reverse_lazy('bio_diversity:create_cupd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.CupdCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CupdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_cupd", "/en/bio_diversity/create/cupd/")


@tag("Cupd")
class TestCupdDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CupdFactory()
        self.test_url = reverse_lazy('bio_diversity:details_cupd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.CupdDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Cupd", "details_cupd", "context")
    # def test_context(self):
    #     context_vars = [
    #         "cupdc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_cupd", f"/en/bio_diversity/details/cupd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cupd")
class TestCupdListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_cupd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.CupdList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_cupd", f"/en/bio_diversity/list/cupd/")


@tag("Cupd")
class CupdUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CupdFactory()
        self.test_url = reverse_lazy('bio_diversity:update_cupd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.CupdUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CupdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_cupd", f"/en/bio_diversity/update/cupd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Draw")
class TestDrawCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.DrawFactory()
        self.test_url = reverse_lazy('bio_diversity:create_draw')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.DrawCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.DrawFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_draw", "/en/bio_diversity/create/draw/")


@tag("Draw")
class TestDrawDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.DrawFactory()
        self.test_url = reverse_lazy('bio_diversity:details_draw', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.DrawDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_draw", f"/en/bio_diversity/details/draw/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Draw")
class TestDrawListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_draw')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.DrawList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_draw", f"/en/bio_diversity/list/draw/")


@tag("Draw")
class DrawUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.DrawFactory()
        self.test_url = reverse_lazy('bio_diversity:update_draw', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.DrawUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.DrawFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_draw", f"/en/bio_diversity/update/draw/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Env")
class TestEnvCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvFactory()
        self.test_url = reverse_lazy('bio_diversity:create_env')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.EnvCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EnvFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_env", "/en/bio_diversity/create/env/")


@tag("Env")
class TestEnvDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvFactory()
        self.test_url = reverse_lazy('bio_diversity:details_env', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "contx_id",
            "loc_id",
            "inst_id",
            "envc_id",
            "env_val",
            "env_start",
            "env_starttime",
            "env_end",
            "env_endtime",
            "env_avg",
            "qual_id",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_env", f"/en/bio_diversity/details/env/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Env")
class TestEnvListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_env')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_env", f"/en/bio_diversity/list/env/")


@tag("Env")
class EnvUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvFactory()
        self.test_url = reverse_lazy('bio_diversity:update_env', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.EnvUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EnvFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_env", f"/en/bio_diversity/update/env/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Envc")
class TestEnvcCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_envc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.EnvcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EnvcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_envc", "/en/bio_diversity/create/envc/")


@tag("Envc")
class TestEnvcDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_envc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "min_val",
            "max_val",
            "unit_id",
            "env_subj_flag",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_envc", f"/en/bio_diversity/details/envc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Envc")
class TestEnvcListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_envc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvcList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_envc", f"/en/bio_diversity/list/envc/")


@tag("Envc")
class EnvcUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_envc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.EnvcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EnvcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_envc", f"/en/bio_diversity/update/envc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Envsc")
class TestEnvscCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvscFactory()
        self.test_url = reverse_lazy('bio_diversity:create_envsc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.EnvscCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EnvscFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_envsc", "/en/bio_diversity/create/envsc/")


@tag("Envsc")
class TestEnvscDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvscFactory()
        self.test_url = reverse_lazy('bio_diversity:details_envsc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvscDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            'envc_id',
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_envsc", f"/en/bio_diversity/details/envsc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Envsc")
class TestEnvscListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_envsc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvscList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_envsc", f"/en/bio_diversity/list/envsc/")


@tag("Envsc")
class EnvscUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvscFactory()
        self.test_url = reverse_lazy('bio_diversity:update_envsc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.EnvscUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EnvscFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_envsc", f"/en/bio_diversity/update/envsc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Evnt")
class TestEvntCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EvntFactory()
        self.test_url = reverse_lazy('bio_diversity:create_evnt')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.EvntCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EvntFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_evnt", "/en/bio_diversity/create/evnt/")


@tag("Evnt")
class TestEvntDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EvntFactory()
        self.test_url = reverse_lazy('bio_diversity:details_evnt', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Evnt", "details_evnt", "context")
    # def test_context(self):
    #     context_vars = [
    #         "evntc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_evnt", f"/en/bio_diversity/details/evnt/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Evnt")
class TestEvntListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_evnt')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_evnt", f"/en/bio_diversity/list/evnt/")


@tag("Evnt")
class EvntUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EvntFactory()
        self.test_url = reverse_lazy('bio_diversity:update_evnt', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.EvntUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EvntFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_evnt", f"/en/bio_diversity/update/evnt/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Evntc")
class TestEvntcCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EvntcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_evntc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.EvntcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EvntcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_evntc", "/en/bio_diversity/create/evntc/")


@tag("Evntc")
class TestEvntcDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EvntcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_evntc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Evntc", "details_evntc", "context")
    # def test_context(self):
    #     context_vars = [
    #         "evntcc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_evntc", f"/en/bio_diversity/details/evntc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Evntc")
class TestEvntcListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_evntc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntcList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_evntc", f"/en/bio_diversity/list/evntc/")


@tag("Evntc")
class EvntcUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EvntcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_evntc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.EvntcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EvntcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_evntc", f"/en/bio_diversity/update/evntc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Facic")
class TestFacicCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FacicFactory()
        self.test_url = reverse_lazy('bio_diversity:create_facic')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.FacicCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.FacicFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_facic", "/en/bio_diversity/create/facic/")


@tag("Facic")
class TestFacicDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FacicFactory()
        self.test_url = reverse_lazy('bio_diversity:details_facic', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.FacicDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Facic", "details_facic", "context")
    # def test_context(self):
    #     context_vars = [
    #         "facicc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_facic", f"/en/bio_diversity/details/facic/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Facic")
class TestFacicListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_facic')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.FacicList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_facic", f"/en/bio_diversity/list/facic/")


@tag("Facic")
class FacicUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FacicFactory()
        self.test_url = reverse_lazy('bio_diversity:update_facic', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.FacicUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.FacicFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_facic", f"/en/bio_diversity/update/facic/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Feed")
class TestFeedCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FeedFactory()
        self.test_url = reverse_lazy('bio_diversity:create_feed')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.FeedCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.FeedFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_feed", "/en/bio_diversity/create/feed/")


@tag("Feed")
class TestFeedDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FeedFactory()
        self.test_url = reverse_lazy('bio_diversity:details_feed', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.FeedDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "contx_id",
            "feedm_id",
            "feedc_id",
            "lot_num",
            "amt",
            "unit_id",
            "freq",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_feed", f"/en/bio_diversity/details/feed/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Feed")
class TestFeedListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_feed')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.FeedList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_feed", f"/en/bio_diversity/list/feed/")


@tag("Feed")
class FeedUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FeedFactory()
        self.test_url = reverse_lazy('bio_diversity:update_feed', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.FeedUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.FeedFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_feed", f"/en/bio_diversity/update/feed/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Feedc")
class TestFeedcCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FeedcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_feedc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.FeedcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.FeedcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_feedc", "/en/bio_diversity/create/feedc/")


@tag("Feedc")
class TestFeedcDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FeedcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_feedc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.FeedcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "manufacturer",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_feedc", f"/en/bio_diversity/details/feedc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Feedc")
class TestFeedcListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_feedc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.FeedcList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_feedc", f"/en/bio_diversity/list/feedc/")


@tag("Feedc")
class FeedcUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FeedcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_feedc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.FeedcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.FeedcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_feedc", f"/en/bio_diversity/update/feedc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Feedm")
class TestFeedmCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FeedmFactory()
        self.test_url = reverse_lazy('bio_diversity:create_feedm')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.FeedmCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.FeedmFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_feedm", "/en/bio_diversity/create/feedm/")


@tag("Feedm")
class TestFeedmDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FeedmFactory()
        self.test_url = reverse_lazy('bio_diversity:details_feedm', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.FeedmDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_feedm", f"/en/bio_diversity/details/feedm/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Feedm")
class TestFeedmListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_feedm')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.FeedmList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_feedm", f"/en/bio_diversity/list/feedm/")


@tag("Feedm")
class FeedmUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FeedmFactory()
        self.test_url = reverse_lazy('bio_diversity:update_feedm', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.FeedmUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.FeedmFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_feedm", f"/en/bio_diversity/update/feedm/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Heat")
class TestHeatCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.HeatFactory()
        self.test_url = reverse_lazy('bio_diversity:create_heat')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.HeatCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.HeatFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_heat", "/en/bio_diversity/create/heat/")


@tag("Heat")
class TestHeatDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.HeatFactory()
        self.test_url = reverse_lazy('bio_diversity:details_heat', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.HeatDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Heat", "details_heat", "context")
    # def test_context(self):
    #     context_vars = [
    #         "heatc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_heat", f"/en/bio_diversity/details/heat/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Heat")
class TestHeatListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_heat')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.HeatList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_heat", f"/en/bio_diversity/list/heat/")


@tag("Heat")
class HeatUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.HeatFactory()
        self.test_url = reverse_lazy('bio_diversity:update_heat', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.HeatUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.HeatFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_heat", f"/en/bio_diversity/update/heat/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Heatd")
class TestHeatdCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.HeatdFactory()
        self.test_url = reverse_lazy('bio_diversity:create_heatd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.HeatdCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.HeatdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_heatd", "/en/bio_diversity/create/heatd/")


@tag("Heatd")
class TestHeatdDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.HeatdFactory()
        self.test_url = reverse_lazy('bio_diversity:details_heatd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.HeatdDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Heatd", "details_heatd", "context")
    # def test_context(self):
    #     context_vars = [
    #         "heatdc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_heatd", f"/en/bio_diversity/details/heatd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Heatd")
class TestHeatdListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_heatd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.HeatdList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_heatd", f"/en/bio_diversity/list/heatd/")


@tag("Heatd")
class HeatdUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.HeatdFactory()
        self.test_url = reverse_lazy('bio_diversity:update_heatd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.HeatdUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.HeatdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_heatd", f"/en/bio_diversity/update/heatd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Inst")
class TestInstCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstFactory()
        self.test_url = reverse_lazy('bio_diversity:create_inst')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.InstFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_inst", "/en/bio_diversity/create/inst/")


@tag("Inst")
class TestInstDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstFactory()
        self.test_url = reverse_lazy('bio_diversity:details_inst', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Inst", "details_inst", "context")
    # def test_context(self):
    #     context_vars = [
    #         "instc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_inst", f"/en/bio_diversity/details/inst/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Inst")
class TestInstListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_inst')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_inst", f"/en/bio_diversity/list/inst/")


@tag("Inst")
class InstUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstFactory()
        self.test_url = reverse_lazy('bio_diversity:update_inst', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.InstFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_inst", f"/en/bio_diversity/update/inst/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Instc")
class TestInstcCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_instc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.InstcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_instc", "/en/bio_diversity/create/instc/")


@tag("Instc")
class TestInstcDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_instc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_instc", f"/en/bio_diversity/details/instc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Instc")
class TestInstcListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_instc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_instc", f"/en/bio_diversity/list/instc/")


@tag("Instc")
class InstcUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_instc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.InstcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_instc", f"/en/bio_diversity/update/instc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Instd")
class TestInstdCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstdFactory()
        self.test_url = reverse_lazy('bio_diversity:create_instd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstdCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.InstdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_instd", "/en/bio_diversity/create/instd/")


@tag("Instd")
class TestInstdDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstdFactory()
        self.test_url = reverse_lazy('bio_diversity:details_instd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstdDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Inst", "details_inst", "context")
    # def test_context(self):
    #     context_vars = [
    #         "instc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_instd", f"/en/bio_diversity/details/instd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Instd")
class TestInstdListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_instd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstdList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_instd", f"/en/bio_diversity/list/instd/")


@tag("Instd")
class InstdUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstdFactory()
        self.test_url = reverse_lazy('bio_diversity:update_instd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstdUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.InstdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_instd", f"/en/bio_diversity/update/instd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Instdc")
class TestInstdcCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstdcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_instdc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstdcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.InstdcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_instdc", "/en/bio_diversity/create/instdc/")


@tag("Instdc")
class TestInstdcDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstdcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_instdc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstdcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_instdc", f"/en/bio_diversity/details/instdc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Instdc")
class TestInstdcListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_instdc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_instdc", f"/en/bio_diversity/list/instdc/")


@tag("Instdc")
class InstdcUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstdcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_instdc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.InstdcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_instdc", f"/en/bio_diversity/update/instdc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Loc")
class TestLocCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LocFactory()
        self.test_url = reverse_lazy('bio_diversity:create_loc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.LocCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.LocFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_loc", "/en/bio_diversity/create/loc/")


@tag("Loc")
class TestLocDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LocFactory()
        self.test_url = reverse_lazy('bio_diversity:details_loc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.LocDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Inst", "details_inst", "context")
    # def test_context(self):
    #     context_vars = [
    #         "instc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_loc", f"/en/bio_diversity/details/loc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Loc")
class TestLocListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_loc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_loc", f"/en/bio_diversity/list/loc/")


@tag("Loc")
class LocUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LocFactory()
        self.test_url = reverse_lazy('bio_diversity:update_loc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.LocFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_loc", f"/en/bio_diversity/update/loc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Locc")
class TestLoccCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LoccFactory()
        self.test_url = reverse_lazy('bio_diversity:create_locc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.LoccCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.LoccFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_locc", "/en/bio_diversity/create/locc/")


@tag("Locc")
class TestLoccDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LoccFactory()
        self.test_url = reverse_lazy('bio_diversity:details_locc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.LoccDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_locc", f"/en/bio_diversity/details/locc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Locc")
class TestLoccListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_locc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_locc", f"/en/bio_diversity/list/locc/")


@tag("Locc")
class LoccUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LoccFactory()
        self.test_url = reverse_lazy('bio_diversity:update_locc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.LoccFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_locc", f"/en/bio_diversity/update/locc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Orga")
class TestOrgaCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.OrgaFactory()
        self.test_url = reverse_lazy('bio_diversity:create_orga')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.OrgaCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.OrgaFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_orga", "/en/bio_diversity/create/orga/")


@tag("Orga")
class TestOrgaDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.OrgaFactory()
        self.test_url = reverse_lazy('bio_diversity:details_orga', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.OrgaDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_orga", f"/en/bio_diversity/details/orga/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Orga")
class TestOrgaListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_orga')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_orga", f"/en/bio_diversity/list/orga/")


@tag("Orga")
class OrgaUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.OrgaFactory()
        self.test_url = reverse_lazy('bio_diversity:update_orga', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.OrgaFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_orga", f"/en/bio_diversity/update/orga/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Perc")
class TestPercCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.PercFactory()
        self.test_url = reverse_lazy('bio_diversity:create_perc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.PercCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.PercFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_perc", "/en/bio_diversity/create/perc/")


@tag("Perc")
class TestPercDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.PercFactory()
        self.test_url = reverse_lazy('bio_diversity:details_perc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.PercDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Inst", "details_inst", "context")
    # def test_context(self):
    #     context_vars = [
    #         "instc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_perc", f"/en/bio_diversity/details/perc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Perc")
class TestPercListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_perc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_perc", f"/en/bio_diversity/list/perc/")


@tag("Perc")
class PercUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.PercFactory()
        self.test_url = reverse_lazy('bio_diversity:update_perc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.PercFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_perc", f"/en/bio_diversity/update/perc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Prio")
class TestPrioCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.PrioFactory()
        self.test_url = reverse_lazy('bio_diversity:create_prio')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.PrioCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.PrioFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_prio", "/en/bio_diversity/create/prio/")


@tag("Prio")
class TestPrioDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.PrioFactory()
        self.test_url = reverse_lazy('bio_diversity:details_prio', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.PrioDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_prio", f"/en/bio_diversity/details/prio/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Prio")
class TestPrioListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_prio')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.PrioList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_prio", f"/en/bio_diversity/list/prio/")


@tag("Prio")
class PrioUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.PrioFactory()
        self.test_url = reverse_lazy('bio_diversity:update_prio', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.PrioUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.PrioFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_prio", f"/en/bio_diversity/update/prio/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Prog")
class TestProgCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProgFactory()
        self.test_url = reverse_lazy('bio_diversity:create_prog')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.ProgCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProgFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_prog", "/en/bio_diversity/create/prog/")


@tag("Prog")
class TestProgDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProgFactory()
        self.test_url = reverse_lazy('bio_diversity:details_prog', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.ProgDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Inst", "details_inst", "context")
    # def test_context(self):
    #     context_vars = [
    #         "instc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_prog", f"/en/bio_diversity/details/prog/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Prog")
class TestProgListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_prog')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_prog", f"/en/bio_diversity/list/prog/")


@tag("Prog")
class ProgUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProgFactory()
        self.test_url = reverse_lazy('bio_diversity:update_prog', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProgFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_prog", f"/en/bio_diversity/update/prog/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Proga")
class TestProgaCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProgaFactory()
        self.test_url = reverse_lazy('bio_diversity:create_proga')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.ProgaCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProgaFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_proga", "/en/bio_diversity/create/proga/")


@tag("Proga")
class TestProgaDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProgaFactory()
        self.test_url = reverse_lazy('bio_diversity:details_proga', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.ProgaDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Inst", "details_inst", "context")
    # def test_context(self):
    #     context_vars = [
    #         "instc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_proga", f"/en/bio_diversity/details/proga/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Proga")
class TestProgaListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_proga')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_proga", f"/en/bio_diversity/list/proga/")


@tag("Proga")
class ProgaUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProgaFactory()
        self.test_url = reverse_lazy('bio_diversity:update_proga', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProgaFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_proga", f"/en/bio_diversity/update/proga/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Prot")
class TestProtCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProtFactory()
        self.test_url = reverse_lazy('bio_diversity:create_prot')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.ProtCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProtFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_prot", "/en/bio_diversity/create/prot/")


@tag("Prot")
class TestProtDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProtFactory()
        self.test_url = reverse_lazy('bio_diversity:details_prot', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.ProtDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Inst", "details_inst", "context")
    # def test_context(self):
    #     context_vars = [
    #         "instc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_prot", f"/en/bio_diversity/details/prot/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Prot")
class TestProtListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_prot')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_prot", f"/en/bio_diversity/list/prot/")


@tag("Prot")
class ProtUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProtFactory()
        self.test_url = reverse_lazy('bio_diversity:update_prot', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProtFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_prot", f"/en/bio_diversity/update/prot/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Protc")
class TestProtcCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProtcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_protc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.ProtcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProtcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_protc", "/en/bio_diversity/create/protc/")


@tag("Protc")
class TestProtcDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProtcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_protc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.ProtcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_protc", f"/en/bio_diversity/details/protc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Protc")
class TestProtcListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_protc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_protc", f"/en/bio_diversity/list/protc/")


@tag("Protc")
class ProtcUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProtcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_protc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProtcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_protc", f"/en/bio_diversity/update/protc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Protf")
class TestProtfCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProtfFactory()
        self.test_url = reverse_lazy('bio_diversity:create_protf')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.ProtfCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProtfFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_protf", "/en/bio_diversity/create/protf/")


@tag("Protf")
class TestProtfDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProtfFactory()
        self.test_url = reverse_lazy('bio_diversity:details_protf', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.ProtfDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Inst", "details_inst", "context")
    # def test_context(self):
    #     context_vars = [
    #         "instc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_protf", f"/en/bio_diversity/details/protf/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Protf")
class TestProtfListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_protf')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_protf", f"/en/bio_diversity/list/protf/")


@tag("Protf")
class ProtfUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProtfFactory()
        self.test_url = reverse_lazy('bio_diversity:update_protf', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProtfFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_protf", f"/en/bio_diversity/update/protf/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Qual")
class TestQualCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.QualFactory()
        self.test_url = reverse_lazy('bio_diversity:create_qual')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.QualCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.QualFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_qual", "/en/bio_diversity/create/qual/")


@tag("Qual")
class TestQualDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.QualFactory()
        self.test_url = reverse_lazy('bio_diversity:details_qual', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.QualDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_qual", f"/en/bio_diversity/details/qual/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Qual")
class TestQualListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_qual')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.QualList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_qual", f"/en/bio_diversity/list/qual/")


@tag("Qual")
class QualUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.QualFactory()
        self.test_url = reverse_lazy('bio_diversity:update_qual', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.QualUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.QualFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_qual", f"/en/bio_diversity/update/qual/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Relc")
class TestRelcCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.RelcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_relc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.RelcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.RelcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_relc", "/en/bio_diversity/create/relc/")


@tag("Relc")
class TestRelcDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.RelcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_relc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.RelcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Inst", "details_inst", "context")
    # def test_context(self):
    #     context_vars = [
    #         "instc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_relc", f"/en/bio_diversity/details/relc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Relc")
class TestRelcListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_relc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_relc", f"/en/bio_diversity/list/relc/")


@tag("Relc")
class RelcUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.RelcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_relc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.RelcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_relc", f"/en/bio_diversity/update/relc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Rive")
class TestRiveCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.RiveFactory()
        self.test_url = reverse_lazy('bio_diversity:create_rive')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.RiveCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.RiveFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_rive", "/en/bio_diversity/create/rive/")


@tag("Rive")
class TestRiveDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.RiveFactory()
        self.test_url = reverse_lazy('bio_diversity:details_rive', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.RiveDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_rive", f"/en/bio_diversity/details/rive/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Rive")
class TestRiveListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_rive')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_rive", f"/en/bio_diversity/list/rive/")


@tag("Rive")
class RiveUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.RiveFactory()
        self.test_url = reverse_lazy('bio_diversity:update_rive', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.RiveFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_rive", f"/en/bio_diversity/update/rive/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Role")
class TestRoleCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.RoleFactory()
        self.test_url = reverse_lazy('bio_diversity:create_role')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.RoleCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.RoleFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_role", "/en/bio_diversity/create/role/")


@tag("Role")
class TestRoleDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.RoleFactory()
        self.test_url = reverse_lazy('bio_diversity:details_role', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.RoleDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_role", f"/en/bio_diversity/details/role/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Role")
class TestRoleListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_role')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_role", f"/en/bio_diversity/list/role/")


@tag("Role")
class RoleUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.RoleFactory()
        self.test_url = reverse_lazy('bio_diversity:update_role', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.RoleFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_role", f"/en/bio_diversity/update/role/{self.instance.pk}/",
                                [self.instance.pk])


@tag("amp")
class TestSampCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SampFactory()
        self.test_url = reverse_lazy('bio_diversity:create_samp')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.SampCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SampFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_samp", "/en/bio_diversity/create/samp/")


@tag("Samp")
class TestSampDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SampFactory()
        self.test_url = reverse_lazy('bio_diversity:details_samp', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.SampDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "loc_id",
            "samp_num",
            "spec_id",
            "sampc_id",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_samp", f"/en/bio_diversity/details/samp/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Samp")
class TestSampListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_samp')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_samp", f"/en/bio_diversity/list/samp/")


@tag("Samp")
class SampUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SampFactory()
        self.test_url = reverse_lazy('bio_diversity:update_samp', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SampFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_samp", f"/en/bio_diversity/update/samp/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Sampc")
class TestSampcCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SampcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_sampc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.SampcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SampcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_sampc", "/en/bio_diversity/create/sampc/")


@tag("Sampc")
class TestSampcDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SampcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_sampc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.SampcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_sampc", f"/en/bio_diversity/details/sampc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Sampc")
class TestSampcListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_sampc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_sampc", f"/en/bio_diversity/list/sampc/")


@tag("Sampc")
class SampcUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SampcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_sampc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SampcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_sampc", f"/en/bio_diversity/update/sampc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Sampd")
class TestSampdCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SampdFactory()
        self.test_url = reverse_lazy('bio_diversity:create_sampd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.SampdCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SampdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_sampd", "/en/bio_diversity/create/sampd/")


@tag("Sampd")
class TestSampdDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SampdFactory()
        self.test_url = reverse_lazy('bio_diversity:details_sampd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.SampdDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "samp_id",
            "anidc_id",
            "det_val",
            "adsc_id",
            "qual_id",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_sampd", f"/en/bio_diversity/details/sampd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Sampd")
class TestSampdListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_sampd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_sampd", f"/en/bio_diversity/list/sampd/")


@tag("Sampd")
class SampdUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SampdFactory()
        self.test_url = reverse_lazy('bio_diversity:update_sampd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SampdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_sampd", f"/en/bio_diversity/update/sampd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Spec")
class TestSpecCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SpecFactory()
        self.test_url = reverse_lazy('bio_diversity:create_spec')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.SpecCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SpecFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_spec", "/en/bio_diversity/create/spec/")


@tag("Spec")
class TestSpecDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SpecFactory()
        self.test_url = reverse_lazy('bio_diversity:details_spec', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.SpecDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "species",
            "com_name",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_spec", f"/en/bio_diversity/details/spec/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Spec")
class TestSpecListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_spec')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_spec", f"/en/bio_diversity/list/spec/")


@tag("Spec")
class SpecUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SpecFactory()
        self.test_url = reverse_lazy('bio_diversity:update_spec', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SpecFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_spec", f"/en/bio_diversity/update/spec/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Stok")
class TestStokCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.StokFactory()
        self.test_url = reverse_lazy('bio_diversity:create_stok')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.StokCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.StokFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_stok", "/en/bio_diversity/create/stok/")


@tag("Stok")
class TestStokDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.StokFactory()
        self.test_url = reverse_lazy('bio_diversity:details_stok', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.StokDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_stok", f"/en/bio_diversity/details/stok/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Stok")
class TestStokListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_stok')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.StokList, CommonList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_stok", f"/en/bio_diversity/list/stok/")


@tag("Stok")
class StokUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.StokFactory()
        self.test_url = reverse_lazy('bio_diversity:update_stok', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.StokUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.StokFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_stok", f"/en/bio_diversity/update/stok/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Subr")
class TestSubrCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SubrFactory()
        self.test_url = reverse_lazy('bio_diversity:create_subr')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.SubrCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SubrFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_subr", "/en/bio_diversity/create/subr/")


@tag("Subr")
class TestSubrDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SubrFactory()
        self.test_url = reverse_lazy('bio_diversity:details_subr', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.SubrDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "rive_id",
            "trib_id",
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_subr", f"/en/bio_diversity/details/subr/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Subr")
class TestSubrListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_subr')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_subr", f"/en/bio_diversity/list/subr/")


@tag("Subr")
class SubrUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SubrFactory()
        self.test_url = reverse_lazy('bio_diversity:update_subr', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SubrFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_subr", f"/en/bio_diversity/update/subr/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Tank")
class TestTankCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TankFactory()
        self.test_url = reverse_lazy('bio_diversity:create_tank')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.TankCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TankFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_tank", "/en/bio_diversity/create/tank/")


@tag("Tank")
class TestTankDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TankFactory()
        self.test_url = reverse_lazy('bio_diversity:details_tank', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.TankDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_tank",
                                f"/en/bio_diversity/details/tank/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Tank")
class TestTankListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_tank')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_tank", f"/en/bio_diversity/list/tank/")


@tag("Tank")
class TankUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TankFactory()
        self.test_url = reverse_lazy('bio_diversity:update_tank', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TankFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_tank",
                                f"/en/bio_diversity/update/tank/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Tankd")
class TestTankdCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TankdFactory()
        self.test_url = reverse_lazy('bio_diversity:create_tankd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.TankdCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TankdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_tankd", "/en/bio_diversity/create/tankd/")


@tag("Tankd")
class TestTankdDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TankdFactory()
        self.test_url = reverse_lazy('bio_diversity:details_tankd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.TankdDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Inst", "details_inst", "context")
    # def test_context(self):
    #     context_vars = [
    #         "instc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_tankd",
                                f"/en/bio_diversity/details/tankd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Tankd")
class TestTankdListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_tankd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_tankd", f"/en/bio_diversity/list/tankd/")


@tag("Tankd")
class TankdUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TankdFactory()
        self.test_url = reverse_lazy('bio_diversity:update_tankd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TankdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_tankd",
                                f"/en/bio_diversity/update/tankd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Team")
class TestTeamCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TeamFactory()
        self.test_url = reverse_lazy('bio_diversity:create_team')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.TeamCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TeamFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_team", "/en/bio_diversity/create/team/")


@tag("Team")
class TestTeamDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TeamFactory()
        self.test_url = reverse_lazy('bio_diversity:details_team', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.TeamDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Inst", "details_inst", "context")
    # def test_context(self):
    #     context_vars = [
    #         "instc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_team",
                                f"/en/bio_diversity/details/team/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Team")
class TestTeamListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_team')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_team", f"/en/bio_diversity/list/team/")


@tag("Team")
class TeamUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TeamFactory()
        self.test_url = reverse_lazy('bio_diversity:update_team', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TeamFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_team",
                                f"/en/bio_diversity/update/team/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Tray")
class TestTrayCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TrayFactory()
        self.test_url = reverse_lazy('bio_diversity:create_tray')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.TrayCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TrayFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_tray", "/en/bio_diversity/create/tray/")


@tag("Tray")
class TestTrayDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TrayFactory()
        self.test_url = reverse_lazy('bio_diversity:details_tray', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.TrayDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_tray", f"/en/bio_diversity/details/tray/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Tray")
class TestTrayListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_tray')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_tray", f"/en/bio_diversity/list/tray/")


@tag("Tray")
class TrayUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TrayFactory()
        self.test_url = reverse_lazy('bio_diversity:update_tray', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TrayFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_tray", f"/en/bio_diversity/update/tray/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Trayd")
class TestTraydCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TraydFactory()
        self.test_url = reverse_lazy('bio_diversity:create_trayd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.TraydCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TraydFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_trayd", "/en/bio_diversity/create/trayd/")


@tag("Trayd")
class TestTraydDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TraydFactory()
        self.test_url = reverse_lazy('bio_diversity:details_trayd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.TraydDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Inst", "details_inst", "context")
    # def test_context(self):
    #     context_vars = [
    #         "instc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_trayd", f"/en/bio_diversity/details/trayd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Trayd")
class TestTraydListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_trayd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_trayd", f"/en/bio_diversity/list/trayd/")


@tag("Trayd")
class TraydUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TraydFactory()
        self.test_url = reverse_lazy('bio_diversity:update_trayd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TraydFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_trayd", f"/en/bio_diversity/update/trayd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Trib")
class TestTribCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TribFactory()
        self.test_url = reverse_lazy('bio_diversity:create_trib')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.TribCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TribFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_trib", "/en/bio_diversity/create/trib/")


@tag("Trib")
class TestTribDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TribFactory()
        self.test_url = reverse_lazy('bio_diversity:details_trib', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.TribDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "rive_id",
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_trib", f"/en/bio_diversity/details/trib/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Trib")
class TestTribListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_trib')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_trib", f"/en/bio_diversity/list/trib/")


@tag("Trib")
class TribUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TribFactory()
        self.test_url = reverse_lazy('bio_diversity:update_trib', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TribFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_trib", f"/en/bio_diversity/update/trib/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Trof")
class TestTrofCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TrofFactory()
        self.test_url = reverse_lazy('bio_diversity:create_trof')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.TrofCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TrofFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_trof", "/en/bio_diversity/create/trof/")


@tag("Trof")
class TestTrofDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TrofFactory()
        self.test_url = reverse_lazy('bio_diversity:details_trof', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.TrofDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_trof", f"/en/bio_diversity/details/trof/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Trof")
class TestTrofListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_trof')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_trof", f"/en/bio_diversity/list/trof/")


@tag("Trof")
class TrofUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TrofFactory()
        self.test_url = reverse_lazy('bio_diversity:update_trof', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TrofFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_trof", f"/en/bio_diversity/update/trof/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Trofd")
class TestTrofdCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TrofdFactory()
        self.test_url = reverse_lazy('bio_diversity:create_trofd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.TrofdCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TrofdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_trofd", "/en/bio_diversity/create/trofd/")


@tag("Trofd")
class TestTrofdDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TrofdFactory()
        self.test_url = reverse_lazy('bio_diversity:details_trofd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.TrofdDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    # not sure how to do this bit
    # @tag("Inst", "details_inst", "context")
    # def test_context(self):
    #     context_vars = [
    #         "instc",
    #         "serial_number",
    #         "comments",
    #         "created_by",
    #         "created_date",
    #     ]
    #     self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_trofd", f"/en/bio_diversity/details/trofd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Trofd")
class TestTrofdListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_trofd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_trofd", f"/en/bio_diversity/list/trofd/")


@tag("Trofd")
class TrofdUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TrofdFactory()
        self.test_url = reverse_lazy('bio_diversity:update_trofd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TrofdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_trofd", f"/en/bio_diversity/update/trofd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Unit")
class TestUnitCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.UnitFactory()
        self.test_url = reverse_lazy('bio_diversity:create_unit')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.UnitCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.UnitFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_unit", "/en/bio_diversity/create/unit/")


@tag("Unit")
class TestUnitDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.UnitFactory()
        self.test_url = reverse_lazy('bio_diversity:details_unit', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        self.assert_inheritance(views.UnitDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_unit", f"/en/bio_diversity/details/unit/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Unit")
class TestUnitListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_unit')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.get_and_login_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, CommonList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_unit", f"/en/bio_diversity/list/unit/")


@tag("Unit")
class UnitUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.UnitFactory()
        self.test_url = reverse_lazy('bio_diversity:update_unit', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.get_and_login_user(in_group="bio_diversity_admin")

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.UnitFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_unit", f"/en/bio_diversity/update/unit/{self.instance.pk}/",
                                [self.instance.pk])