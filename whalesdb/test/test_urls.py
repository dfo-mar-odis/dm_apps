from django.test import tag

from django.urls import reverse_lazy, resolve
from django.test import TestCase
from django.utils.translation import activate

from whalesdb import views


class URLTest(TestCase):

    # test that a url signature can be reversed into an address,
    # an address gives an expected signature and the address
    # will link to the expected view or function
    def basic_en_url_test(self, signature, url, view, args=None):
        activate('en')
        en_url = "/en/{}".format(url)

        # Test a URL can be reversed
        if args:
            addr = reverse_lazy(signature, args=args)
        else:
            addr = reverse_lazy(signature)

        self.assertEqual(addr, en_url)

        # Test the URL can be resolved
        found = resolve(en_url)
        self.assertEqual(found.view_name, signature)

        # Test the resolved URL points to the proper view
        self.assertEqual(found.func.__name__, view.__name__)

    @tag('index', 'url')
    def test_root_url_index_view(self):
        self.basic_en_url_test('whalesdb:index', 'whalesdb/', views.IndexView)

    @tag('dep', 'url', 'create')
    def test_url_create_dep_view(self):
        self.basic_en_url_test('whalesdb:create_dep', 'whalesdb/create/dep/', views.DepCreate)

    @tag('dep', 'url', 'create', 'pop')
    def test_url_create_pop_dep_view(self):
        self.basic_en_url_test('whalesdb:create_dep', 'whalesdb/create/dep/pop/', views.DepCreate, ['pop'])

    @tag('dep', 'url', 'update')
    def test_url_update_dep_view(self):
        self.basic_en_url_test('whalesdb:update_dep', 'whalesdb/update/dep/1/', views.DepUpdate, [1])

    @tag('dep', 'url', 'update', 'pop')
    def test_url_update_pop_dep_view(self):
        self.basic_en_url_test('whalesdb:update_dep', 'whalesdb/update/dep/1/pop/', views.DepUpdate, [1, 'pop'])

    @tag('dep', 'url', 'list')
    def test_url_list_dep_view(self):
        self.basic_en_url_test('whalesdb:list_dep', 'whalesdb/list/dep/', views.DepList)

    @tag('dep', 'url', 'details')
    def test_url_details_dep_view(self):
        self.basic_en_url_test('whalesdb:details_dep', 'whalesdb/details/dep/1/', views.DepDetails, [1])

    @tag('eda', 'url', 'create', 'pop')
    def test_url_create_pop_eda_view(self):
        self.basic_en_url_test('whalesdb:create_eda', 'whalesdb/create/eda/1/pop/', views.EdaCreate, [1, 'pop'])

    @tag('emm', 'url', 'create')
    def test_url_create_emm_view(self):
        self.basic_en_url_test('whalesdb:create_emm', 'whalesdb/create/emm/', views.EmmCreate)

    @tag('emm', 'url', 'create', 'pop')
    def test_url_create_pop_emm_view(self):
        self.basic_en_url_test('whalesdb:create_emm', 'whalesdb/create/emm/pop/', views.EmmCreate, ['pop'])

    @tag('emm', 'url', 'update', 'pop')
    def test_url_update_emm_view(self):
        self.basic_en_url_test('whalesdb:update_emm', 'whalesdb/update/emm/1/', views.EmmUpdate, [1])

    @tag('emm', 'url', 'list')
    def test_url_list_emm_view(self):
        self.basic_en_url_test('whalesdb:list_emm', 'whalesdb/list/emm/', views.EmmList)

    @tag('emm', 'url', 'details')
    def test_url_details_emm_view(self):
        self.basic_en_url_test('whalesdb:details_emm', 'whalesdb/details/emm/1/', views.EmmDetails, [1])

    @tag('eqh', 'url', 'create')
    def test_url_create_pop_eqh_view(self):
        self.basic_en_url_test('whalesdb:create_eqh', 'whalesdb/create/eqh/1/pop/', views.EqhCreate, [1, 'pop'])

    @tag('eqh', 'url', 'update', 'pop')
    def test_url_update_pop_eqh_view(self):
        self.basic_en_url_test('whalesdb:update_eqh', 'whalesdb/update/eqh/1/pop/', views.EqhUpdate, [1, 'pop'])

    @tag('eqo', 'url', 'create')
    def test_url_create_eqo_view(self):
        self.basic_en_url_test('whalesdb:create_eqo', 'whalesdb/create/eqo/pop/', views.EqoCreate, ['pop'])

    @tag('eqp', 'url', 'create')
    def test_url_create_eqp_view(self):
        self.basic_en_url_test('whalesdb:create_eqp', 'whalesdb/create/eqp/', views.EqpCreate)

    @tag('eqp', 'url', 'update')
    def test_url_update_eqp_view(self):
        self.basic_en_url_test('whalesdb:update_eqp', 'whalesdb/update/eqp/1/', views.EqpUpdate, [1])

    @tag('eqp', 'url', 'update', 'pop')
    def test_url_update_eqp_view(self):
        self.basic_en_url_test('whalesdb:update_eqp', 'whalesdb/update/eqp/1/pop/', views.EqpUpdate, [1, 'pop'])

    @tag('eqp', 'url', 'list')
    def test_url_list_eqp_view(self):
        self.basic_en_url_test('whalesdb:list_eqp', 'whalesdb/list/eqp/', views.EqpList)

    @tag('eqp', 'url', 'details')
    def test_url_details_eqp_view(self):
        self.basic_en_url_test('whalesdb:details_eqp', 'whalesdb/details/eqp/1/', views.EqpDetails, [1])

    @tag('eqr', 'url', 'create')
    def test_url_create_pop_eqr_view(self):
        self.basic_en_url_test('whalesdb:create_eqr', 'whalesdb/create/eqr/1/pop/', views.EqrCreate, [1, 'pop'])

    @tag('eqr', 'url', 'update', 'pop')
    def test_url_update_pop_eqr_view(self):
        self.basic_en_url_test('whalesdb:update_eqr', 'whalesdb/update/eqr/1/pop/', views.EqrUpdate, [1, 'pop'])

    @tag('mor', 'url', 'create')
    def test_url_create_mor_view(self):
        self.basic_en_url_test('whalesdb:create_mor', 'whalesdb/create/mor/', views.MorCreate)

    @tag('mor', 'url', 'create', 'pop')
    def test_url_create_pop_mor_view(self):
        self.basic_en_url_test('whalesdb:create_mor', 'whalesdb/create/mor/pop/', views.MorCreate, ['pop'])

    @tag('mor', 'url', 'update')
    def test_url_update_mor_view(self):
        self.basic_en_url_test('whalesdb:update_mor', 'whalesdb/update/mor/1/', views.MorUpdate, [1])

    @tag('mor', 'url', 'update', 'pop')
    def test_url_update_pop_mor_view(self):
        self.basic_en_url_test('whalesdb:update_mor', 'whalesdb/update/mor/1/pop/', views.MorUpdate, [1, 'pop'])

    @tag('mor', 'url', 'list')
    def test_url_list_mor_view(self):
        self.basic_en_url_test('whalesdb:list_mor', 'whalesdb/list/mor/', views.MorList)

    @tag('mor', 'url', 'details')
    def test_url_details_mor_view(self):
        self.basic_en_url_test('whalesdb:details_mor', 'whalesdb/details/mor/1/', views.MorDetails, [1])

    @tag('prj', 'url', 'create')
    def test_url_create_prj_view(self):
        self.basic_en_url_test('whalesdb:create_prj', 'whalesdb/create/prj/', views.PrjCreate)

    @tag('prj', 'url', 'create', 'pop')
    def test_url_create_pop_prj_view(self):
        self.basic_en_url_test('whalesdb:create_prj', 'whalesdb/create/prj/pop/', views.PrjCreate, ['pop'])

    @tag('prj', 'url', 'update')
    def test_url_update_prj_view(self):
        self.basic_en_url_test('whalesdb:update_prj', 'whalesdb/update/prj/1/', views.PrjUpdate, [1])

    @tag('prj', 'url', 'update', 'pop')
    def test_url_update_pop_prj_view(self):
        self.basic_en_url_test('whalesdb:update_prj', 'whalesdb/update/prj/1/pop/', views.PrjUpdate, [1, 'pop'])

    @tag('prj', 'url', 'list')
    def test_url_list_prj_view(self):
        self.basic_en_url_test('whalesdb:list_prj', 'whalesdb/list/prj/', views.PrjList)

    @tag('prj', 'url', 'details')
    def test_url_details_prj_view(self):
        self.basic_en_url_test('whalesdb:details_prj', 'whalesdb/details/prj/1/', views.PrjDetails, [1])

    @tag('rsc', 'url', 'create')
    def test_url_create_rsc_view(self):
        self.basic_en_url_test('whalesdb:create_rsc', 'whalesdb/create/rsc/', views.RscCreate)

    @tag('rsc', 'url', 'list')
    def test_url_list_rsc_view(self):
        self.basic_en_url_test('whalesdb:list_rsc', 'whalesdb/list/rsc/', views.RscList)

    @tag('rsc', 'url', 'details')
    def test_url_details_rsc_view(self):
        self.basic_en_url_test('whalesdb:details_rsc', 'whalesdb/details/rsc/1/', views.RscDetails, [1])

    @tag('rst', 'url', 'create')
    def test_url_create_rst_view(self):
        self.basic_en_url_test('whalesdb:create_rst', 'whalesdb/create/rst/1/pop/', views.RstCreate, [1, 'pop'])

    @tag('rst', 'url', 'delete')
    def test_url_delete_rst_view(self):
        self.basic_en_url_test('whalesdb:delete_rst', 'whalesdb/delete/rst/1/', views.rst_delete, [1])

    @tag('stn', 'url', 'create')
    def test_url_create_stn_view(self):
        self.basic_en_url_test('whalesdb:create_stn', 'whalesdb/create/stn/', views.StnCreate)

    @tag('stn', 'url', 'create', 'pop')
    def test_url_create_pop_stn_view(self):
        self.basic_en_url_test('whalesdb:create_stn', 'whalesdb/create/stn/pop/', views.StnCreate, ['pop'])

    @tag('stn', 'url', 'update')
    def test_url_update_stn_view(self):
        self.basic_en_url_test('whalesdb:update_stn', 'whalesdb/update/stn/1/', views.StnUpdate, [1])

    @tag('stn', 'url', 'update', 'pop')
    def test_url_update_pop_stn_view(self):
        self.basic_en_url_test('whalesdb:update_stn', 'whalesdb/update/stn/1/pop/', views.StnUpdate, [1, 'pop'])

    @tag('stn', 'url', 'list')
    def test_url_list_stn_view(self):
        self.basic_en_url_test('whalesdb:list_stn', 'whalesdb/list/stn/', views.StnList)

    @tag('stn', 'url', 'details')
    def test_url_details_stn_view(self):
        self.basic_en_url_test('whalesdb:details_stn', 'whalesdb/details/stn/1/', views.StnDetails, [1])

    @tag('ste', 'url', 'create', 'pop')
    def test_url_create_set_pop_ste_view(self):
        # The Station Event object requires a Deployment and a station event type
        self.basic_en_url_test('whalesdb:create_ste', 'whalesdb/create/ste/1/2/pop/', views.SteCreate, [1, 2, 'pop'])

    @tag('tea', 'url', 'create')
    def test_url_create_tea_view(self):
        self.basic_en_url_test('whalesdb:create_tea', 'whalesdb/create/tea/', views.TeaCreate)

    @tag('tea', 'url', 'list')
    def test_url_list_tea_view(self):
        self.basic_en_url_test('whalesdb:list_tea', 'whalesdb/list/tea/', views.TeaList)

    @tag('tea', 'url', 'list')
    def test_url_list_tea_view(self):
        self.basic_en_url_test('whalesdb:list_tea', 'whalesdb/list/tea/', views.TeaList)

    @tag('rtt', 'url', 'list')
    def test_url_list_rtt_view(self):
        self.basic_en_url_test('whalesdb:list_rtt', 'whalesdb/list/rtt/', views.RttList)

    @tag('rtt', 'url', 'details')
    def test_url_details_rtt_view(self):
        self.basic_en_url_test('whalesdb:details_rtt', 'whalesdb/details/rtt/1/', views.RttDetails, [1])

    @tag('rtt', 'url', 'create')
    def test_url_create_rtt_view(self):
        self.basic_en_url_test('whalesdb:create_rtt', 'whalesdb/create/rtt/', views.RttCreate)

    @tag('rec', 'url', 'create')
    def test_url_create_rec_view(self):
        self.basic_en_url_test('whalesdb:create_rec', 'whalesdb/create/rec/', views.RecCreate)

    @tag('rec', 'url', 'list')
    def test_url_list_rec_view(self):
        self.basic_en_url_test('whalesdb:list_rec', 'whalesdb/list/rec/', views.RecList)

    @tag('rec', 'url', 'update')
    def test_url_update_rec_view(self):
        self.basic_en_url_test('whalesdb:update_rec', 'whalesdb/update/rec/1/', views.RecUpdate, [1])

    @tag('rci', 'url', 'create', 'pop')
    def test_url_create_rci_pop_ste_view(self):
        self.basic_en_url_test('whalesdb:create_rci', 'whalesdb/create/rci/1/pop/', views.RciCreate, [1, 'pop'])

    @tag('ree', 'url', 'create', 'pop')
    def test_url_create_set_pop_ree_view(self):
        self.basic_en_url_test('whalesdb:create_ree', 'whalesdb/create/ree/1/pop/', views.ReeCreate, [1, 'pop'])

