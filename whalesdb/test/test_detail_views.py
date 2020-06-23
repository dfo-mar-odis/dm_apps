from django.utils.translation import activate
from django.urls import reverse_lazy
from django.test import tag, RequestFactory

from whalesdb.test.common_views import CommonDetailsTest, setup_view
from whalesdb.test import WhalesdbFactoryFloor as Factory
from whalesdb import views, models


class TestEmmDetails(CommonDetailsTest):

    def createDict(self):
        if self._details_dict:
            return self._details_dict

        self._details_dict = {}

        obj = Factory.EmmFactory()

        self._details_dict['emm_1'] = obj

        return self._details_dict

    def setUp(self):
        super().setUp()

        emm_dic = self.createDict()

        self.test_url = reverse_lazy('whalesdb:details_emm', args=(emm_dic['emm_1'].pk,))
        self.test_expected_template = 'whalesdb/details_emm.html'
        self.fields = []

    @tag('emm', 'details_emm', 'response', 'access')
    def test_details_emm_en(self):
        super().assert_view()

    # Station Details are visible to all
    @tag('emm', 'details_emm', 'response', 'access')
    def test_details_emm_fr(self):
        super().assert_view(lang='fr')

    # Test that the context contains the proper fields
    @tag('emm', 'details_emm', 'context')
    def test_context_fields_emm(self):
        activate('en')

        response = self.client.get(self.test_url)

        super().assert_context_fields(response)


class TestEqpDetails(CommonDetailsTest):

    def createDict(self):
        if self._details_dict:
            return self._details_dict

        self._details_dict = {}

        obj = Factory.EqpFactory()

        self._details_dict['eqp_1'] = obj

        return self._details_dict

    def setUp(self):
        super().setUp()

        eqp_dic = self.createDict()

        self.test_url = reverse_lazy('whalesdb:details_eqp', args=(eqp_dic['eqp_1'].pk,))
        self.test_expected_template = 'whalesdb/details_eqp.html'
        self.fields = []

    @tag('eqp', 'details_eqp', 'response', 'access')
    def test_details_eqp_en(self):
        super().assert_view()

    # Station Details are visible to all
    @tag('eqp', 'details_eqp', 'response', 'access')
    def test_details_eqp_fr(self):
        super().assert_view(lang='fr')

    # Test that the context contains the proper fields
    @tag('eqp', 'details_eqp', 'context')
    def test_context_fields_eqp(self):
        activate('en')

        response = self.client.get(self.test_url)

        super().assert_context_fields(response)


class TestDepDetails(CommonDetailsTest):

    def createDict(self):
        if self._details_dict:
            return self._details_dict

        self._details_dict = {}

        # There should be one dep object loaded from the fixtures
        dep_1 = Factory.DepFactory()

        self._details_dict['dep_1'] = dep_1

        return self._details_dict

    def setUp(self):
        super().setUp()

        dep_dic = self.createDict()

        self.test_url = reverse_lazy('whalesdb:details_dep', args=(dep_dic['dep_1'].pk,))
        self.test_expected_template = 'whalesdb/details_dep.html'
        self.fields = ['dep_year', 'dep_month', 'dep_name', 'stn', 'prj', 'mor']

    # Station Details are visible to all
    @tag('dep', 'details_dep', 'response', 'access')
    def test_details_dep_en(self):
        super().assert_view()

    # Station Details are visible to all
    @tag('dep', 'details_dep', 'response', 'access')
    def test_details_dep_fr(self):
        super().assert_view(lang='fr')

    # Test that the context contains the proper fields
    @tag('dep', 'details_dep', 'context')
    def test_context_fields_dep(self):
        activate('en')

        response = self.client.get(self.test_url)

        super().assert_context_fields(response)
        # Google API key is required so map of station location doesn't nag about being in dev mode
        self.assertIn("google_api_key", response.context)
        self.assertEqual(response.context['list_url'], 'whalesdb:list_dep')
        self.assertEqual(response.context['update_url'], 'whalesdb:update_dep')

        self.assertEqual(response.context["object"], self.createDict()['dep_1'])
        super().assert_field_in_fields(response)

    # If a deployment event has been issued, a deployment should no longer be editable and the
    # test_func method should return false. This is to prevent URL hijacking and letting a user
    # paste in data to a url to update a view
    @tag('dep', 'details_dep', 'access')
    def test_details_dep_test_func(self):
        dep = Factory.DepFactory()

        # have to create the request and setup the view
        req_factory = RequestFactory()
        test_url = reverse_lazy("whalesdb:details_dep", kwargs={'pk': dep.pk})
        request = req_factory.get(test_url)
        request.user = self.login_whale_user()
        view = setup_view(views.DepDetails(), request, pk=dep.pk)

        # check to see if a deployment that's not been deployed can be edited
        self.assertTrue(view.test_func())

        # create a deployment event
        set_type = models.SetStationEventCode.objects.get(pk=1)  # 1 == Deployment event
        dep_evt = Factory.SteFactory(dep=dep, set_type=set_type)

        # deployment should no longer be editable
        self.assertFalse(view.test_func())

    # Same as test_details_dep_test_func, but we're testing the context returns the expected values
    # page is editable if the user is authorized and test_func returns true
    @tag('dep', 'details_dep', 'context', 'access')
    def test_details_dep_context_auth_denied(self):
        activate('en')

        dep = Factory.DepFactory()
        test_url = reverse_lazy("whalesdb:details_dep", kwargs={'pk': dep.pk})

        self.login_whale_user()
        response = self.client.get(test_url)

        self.assertIn("editable", response.context)
        self.assertTrue(response.context['editable'])

        # create a deployment event
        set_type = models.SetStationEventCode.objects.get(pk=1)  # 1 == Deployment event
        dep_evt = Factory.SteFactory(dep=dep, set_type=set_type)

        response = self.client.get(test_url)

        self.assertIn("editable", response.context)
        self.assertTrue(response.context['auth'])
        self.assertFalse(response.context['editable'])


class TestMorDetails(CommonDetailsTest):

    def createDict(self):
        if self._details_dict:
            return self._details_dict

        self._details_dict = {}

        # There should be one mooring setup loaded from the fixtures
        mor_1 = Factory.MorFactory()

        self._details_dict['mor_1'] = mor_1

        return self._details_dict

    def setUp(self):
        super().setUp()

        mor_dic = self.createDict()

        self.test_url = reverse_lazy('whalesdb:details_mor', args=(mor_dic['mor_1'].pk,))
        self.test_expected_template = 'whalesdb/details_mor.html'
        self.fields = ['mor_name', 'mor_max_depth', 'mor_link_setup_image', 'mor_additional_equipment',
                       'mor_general_moor_description', 'mor_notes']

    # Station Details are visible to all
    @tag('mor', 'details_mor', 'response', 'access')
    def test_details_mor_en(self):
        super().assert_view()

    # Station Details are visible to all
    @tag('mor', 'details_mor', 'response', 'access')
    def test_details_mor_fr(self):
        super().assert_view(lang='fr')

    # Test that the context contains the proper fields
    @tag('mor', 'details_mor', 'context')
    def test_context_fields_mor(self):
        activate('en')

        response = self.client.get(self.test_url)

        super().assert_context_fields(response)
        self.assertEqual(response.context['list_url'], 'whalesdb:list_mor')
        self.assertEqual(response.context['update_url'], 'whalesdb:update_mor')

        self.assertEqual(response.context["object"], self.createDict()['mor_1'])
        super().assert_field_in_fields(response)


class TestPrjDetails(CommonDetailsTest):

    def createDict(self):
        if self._details_dict:
            return self._details_dict

        self._details_dict = {}

        prj_1 = Factory.PrjFactory()

        self._details_dict['prj_1'] = prj_1

        return self._details_dict

    def setUp(self):
        super().setUp()

        stn_dic = self.createDict()

        self.test_url = reverse_lazy('whalesdb:details_prj', args=(stn_dic['prj_1'].pk,))
        self.test_expected_template = 'whalesdb/whales_details.html'

    # Project Details are visible to all
    @tag('prj', 'details_prj', 'response', 'access')
    def test_details_prj_en(self):
        super().assert_view()

    # Project Details are visible to all
    @tag('prj', 'details_prj', 'response', 'access')
    def test_details_prj_fr(self):
        super().assert_view(lang='fr')

    # Test that the context contains the proper fields
    @tag('prj', 'details_prj', 'context')
    def test_context_fields_prj(self):
        activate('en')

        response = self.client.get(self.test_url)

        super().assert_context_fields(response)
        self.assertEqual(response.context['list_url'], 'whalesdb:list_prj')
        self.assertEqual(response.context['update_url'], 'whalesdb:update_prj')

        self.assertEqual(response.context['object'], self.createDict()['prj_1'])
        super().assert_field_in_fields(response)


class TestRecDetails(CommonDetailsTest):

    def createDict(self):
        if self._details_dict:
            return self._details_dict

        self._details_dict = {}

        rec_1 = Factory.RecFactory()

        self._details_dict['rec_1'] = rec_1

        return self._details_dict

    def setUp(self):
        super().setUp()

        stn_dic = self.createDict()

        self.test_url = reverse_lazy('whalesdb:details_rec', args=(stn_dic['rec_1'].pk,))
        self.test_expected_template = 'whalesdb/details_rec.html'

    # Project Details are visible to all
    @tag('rec', 'details_rec', 'response', 'access')
    def test_details_rec_en(self):
        super().assert_view()

    # Project Details are visible to all
    @tag('rec', 'details_rec', 'response', 'access')
    def test_details_rec_fr(self):
        super().assert_view(lang='fr')

    # Test that the context contains the proper fields
    @tag('rec', 'details_rec', 'context')
    def test_context_fields_rec(self):
        activate('en')

        response = self.client.get(self.test_url)

        super().assert_context_fields(response)
        self.assertEqual(response.context['list_url'], 'whalesdb:list_rec')
        self.assertEqual(response.context['update_url'], 'whalesdb:update_rec')

        self.assertEqual(response.context['object'], self.createDict()['rec_1'])
        self.assertFalse(response.context['editable'])
        super().assert_field_in_fields(response)

    # Test that an rec object isn't editable even if the user is logged in with rights
    @tag('rec', 'details_rec', 'auth', 'context')
    def test_context_fields_auth_rec(self):
        activate('en')

        self.login_whale_user()
        response = self.client.get(self.test_url)

        self.assertTrue(response.context['auth'])
        self.assertTrue(response.context['editable'])


class TestRscDetails(CommonDetailsTest):

    def createDict(self):
        if self._details_dict:
            return self._details_dict

        self._details_dict = {}

        rsc_1 = Factory.RscFactory()

        self._details_dict['rsc_1'] = rsc_1

        return self._details_dict

    def setUp(self):
        super().setUp()

        stn_dic = self.createDict()

        self.test_url = reverse_lazy('whalesdb:details_rsc', args=(stn_dic['rsc_1'].pk,))
        self.test_expected_template = 'whalesdb/details_rsc.html'

    # Project Details are visible to all
    @tag('rsc', 'details_rsc', 'response', 'access')
    def test_details_rsc_en(self):
        super().assert_view()

    # Project Details are visible to all
    @tag('rsc', 'details_rsc', 'response', 'access')
    def test_details_rsc_fr(self):
        super().assert_view(lang='fr')

    # Test that the context contains the proper fields
    @tag('rsc', 'details_rsc', 'context')
    def test_context_fields_rsc(self):
        activate('en')

        response = self.client.get(self.test_url)

        super().assert_context_fields(response)
        self.assertEqual(response.context['list_url'], 'whalesdb:list_rsc')
        self.assertEqual(response.context['update_url'], 'whalesdb:update_rsc')

        self.assertEqual(response.context['object'], self.createDict()['rsc_1'])
        self.assertFalse(response.context['editable'])
        super().assert_field_in_fields(response)

    # Test that an rsc object isn't editable even if the user is logged in with rights
    @tag('rsc', 'details_rsc', 'auth', 'context')
    def test_context_fields_auth_rsc(self):
        activate('en')

        self.login_whale_user()
        response = self.client.get(self.test_url)

        self.assertTrue(response.context['auth'])
        self.assertFalse(response.context['editable'])


class TestStnDetails(CommonDetailsTest):

    def createDict(self):
        if self._details_dict:
            return self._details_dict

        self._details_dict = {}

        # Should be one station loaded from the fixtures
        stn_1 = Factory.StnFactory()

        self._details_dict['stn_1'] = stn_1

        return self._details_dict

    def setUp(self):
        super().setUp()

        stn_dic = self.createDict()

        self.test_url = reverse_lazy('whalesdb:details_stn', args=(stn_dic['stn_1'].pk,))
        self.test_expected_template = 'whalesdb/details_stn.html'
        self.fields = ['stn_name', 'stn_code', 'stn_revision', 'stn_planned_lat', 'stn_planned_lon',
                       'stn_planned_depth', 'stn_notes']

    # Station Details are visible to all
    @tag('stn', 'details_stn', 'response', 'access')
    def test_details_stn_en(self):
        super().assert_view(expected_template='whalesdb/details_stn.html')

    # Station Details are visible to all
    @tag('stn', 'stn', 'details_stn', 'response', 'access')
    def test_details_stn_fr(self):
        super().assert_view(lang='fr', expected_template='whalesdb/details_stn.html')

    # Test that the context contains the proper fields
    @tag('stn', 'details_stn', 'context')
    def test_context_fields_stn(self):
        activate('fr')

        response = self.client.get(self.test_url)

        super().assert_context_fields(response)

        # Google API key is required so map of station location doesn't nag about being in dev mode
        self.assertIn("google_api_key", response.context)
        self.assertEqual(response.context['list_url'], 'whalesdb:list_stn')
        self.assertEqual(response.context['update_url'], 'whalesdb:update_stn')
        self.assertEqual(response.context['object'], self.createDict()['stn_1'])

        super().assert_field_in_fields(response)
