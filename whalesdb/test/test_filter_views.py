from django.test import tag
from django.urls import reverse_lazy

from whalesdb.test.common_views import CommonListTest


class TestDepList(CommonListTest):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_dep')

    # User should be able to view lists without login required
    @tag('dep', 'dep_list', 'response', 'access')
    def test_dep_list_en(self):
        super().assert_view()

    # User should be able to view lists without login required
    @tag('dep', 'dep_list', 'response', 'access')
    def test_dep_list_fr(self):
        super().assert_view(lang='fr')

    # make sure project list context returns expected context objects
    # The deployment view should use create_dep and details_dep for the create and details buttons
    @tag('dep', 'dep_list', 'response', 'context')
    def test_dep_list_context_fields(self):
        response = super().assert_list_view_context_fields()

        self.assertEqual("whalesdb:create_dep", response.context['create_url'])
        self.assertEqual("whalesdb:details_dep", response.context['details_url'])
        self.assertEqual("whalesdb:update_dep", response.context['update_url'])


class TestEmmList(CommonListTest):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_emm')

    # User should be able to view lists without login required
    @tag('emm', 'emm_list', 'response', 'access')
    def test_emm_list_en(self):
        super().assert_view()

    # User should be able to view lists without login required
    @tag('emm', 'emm_list', 'response', 'access')
    def test_emm_list_fr(self):
        super().assert_view(lang='fr')

    # make sure project list context returns expected context objects
    @tag('emm', 'emm_list', 'response', 'context')
    def test_emm_list_context_fields(self):
        response = super().assert_list_view_context_fields()


class TestEqpList(CommonListTest):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_eqp')

    # User should be able to view lists without login required
    @tag('eqp', 'eqp_list', 'response', 'access')
    def test_eqp_list_en(self):
        super().assert_view()

    # User should be able to view lists without login required
    @tag('eqp', 'eqp_list', 'response', 'access')
    def test_eqp_list_fr(self):
        super().assert_view(lang='fr')

    # make sure project list context returns expected context objects
    @tag('eqp', 'eqp_list', 'response', 'context')
    def test_eqp_list_context_fields(self):
        response = super().assert_list_view_context_fields()


class TestMorList(CommonListTest):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_mor')

    # User should be able to view lists without login required
    @tag('mor', 'mor_list', 'response', 'access')
    def test_mor_list_en(self):
        super().assert_view()

    # User should be able to view lists without login required
    @tag('mor', 'mor_list', 'response', 'access')
    def test_mor_list_fr(self):
        super().assert_view(lang='fr')

    # make sure project list context returns expected context objects
    # The mooring view should use create_mor and details_mor for the create and details buttons
    @tag('mor', 'mor_list', 'response', 'context')
    def test_mor_list_context_fields(self):
        response = super().assert_list_view_context_fields()

        self.assertEqual("whalesdb:create_mor", response.context['create_url'])
        self.assertEqual("whalesdb:details_mor", response.context['details_url'])
        self.assertEqual("whalesdb:update_mor", response.context['update_url'])


class TestPrjList(CommonListTest):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_prj')

    # User should be able to view lists without login required
    @tag('prj', 'prj_list', 'response', 'access')
    def test_prj_list_en(self):
        super().assert_view()

    # User should be able to view lists without login required
    @tag('prj', 'prj_list', 'response', 'access')
    def test_prj_list_fr(self):
        super().assert_view(lang='fr')

    # make sure project list context returns expected context objects
    # The project view should use create_mor and details_prj for the create and details buttons
    @tag('prj', 'prj_list', 'response', 'context')
    def test_prj_list_context_fields(self):
        response = super().assert_list_view_context_fields()

        self.assertEqual("whalesdb:create_prj", response.context['create_url'])
        self.assertEqual("whalesdb:details_prj", response.context['details_url'])
        self.assertEqual("whalesdb:update_prj", response.context['update_url'])


class TestRecList(CommonListTest):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_rec')

    # User should be able to view lists without login required
    @tag('rec', 'rec_list', 'response', 'access')
    def test_rec_list_en(self):
        super().assert_view()

    # User should be able to view lists without login required
    @tag('rec', 'rec_list', 'response', 'access')
    def test_rec_list_fr(self):
        super().assert_view(lang='fr')

    @tag('rec', 'rec_list', 'response', 'context')
    def test_rec_list_context_fields(self):
        response = super().assert_list_view_context_fields()

        self.assertEqual("whalesdb:create_rec", response.context['create_url'])
        # self.assertEqual("whalesdb:details_rec", response.context['details_url'])

        self.assertEquals(False, response.context["editable"])


class TestRscList(CommonListTest):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_rsc')

    # User should be able to view lists without login required
    @tag('rsc', 'rsc_list', 'response', 'access')
    def test_rsc_list_en(self):
        super().assert_view()

    # User should be able to view lists without login required
    @tag('rsc', 'rsc_list', 'response', 'access')
    def test_rsc_list_fr(self):
        super().assert_view(lang='fr')

    @tag('rsc', 'rsc_list', 'response', 'context')
    def test_rsc_list_context_fields(self):
        response = super().assert_list_view_context_fields()

        self.assertEqual("whalesdb:create_rsc", response.context['create_url'])
        self.assertEqual("whalesdb:details_rsc", response.context['details_url'])

        self.assertEquals(False, response.context["editable"])


class TestRttList(CommonListTest):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_rtt')

    # User should be able to view lists without login required
    @tag('rtt', 'rtt_list', 'response', 'access')
    def test_rsc_list_en(self):
        super().assert_view()

    # User should be able to view lists without login required
    @tag('rtt', 'rtt_list', 'response', 'access')
    def test_rsc_list_fr(self):
        super().assert_view(lang='fr')



class TestStnList(CommonListTest):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_stn')

    # User should be able to view lists without login required
    @tag('stn', 'stn_list', 'response', 'access')
    def test_stn_list_en(self):
        super().assert_view()

    # User should be able to view lists without login required
    @tag('stn', 'stn_list', 'response', 'access')
    def test_stn_list_fr(self):
        super().assert_view(lang='fr')

    # make sure project list context returns expected context objects
    # The station view should use create_stn and details_stn for the create and details buttons
    @tag('stn', 'stn_list', 'response', 'context')
    def test_stn_list_context_fields(self):
        response = super().assert_list_view_context_fields()

        self.assertEqual("whalesdb:create_stn", response.context['create_url'])
        self.assertEqual("whalesdb:details_stn", response.context['details_url'])
        self.assertEqual("whalesdb:update_stn", response.context['update_url'])


class TestTeaList(CommonListTest):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_tea')

    # User should be able to view lists without login required
    @tag('tea', 'tea_list', 'response', 'access')
    def test_tea_list_en(self):
        super().assert_view()

    # User should be able to view lists without login required
    @tag('tea', 'tea_list', 'response', 'access')
    def test_tea_list_fr(self):
        super().assert_view(lang='fr')

    # make sure project list context returns expected context objects
    # The station view should use create_tea and details_tea for the create and details buttons
    @tag('tea', 'tea_list', 'response', 'context')
    def test_tea_list_context_fields(self):
        response = super().assert_list_view_context_fields()

        self.assertEqual("whalesdb:create_tea", response.context['create_url'])
