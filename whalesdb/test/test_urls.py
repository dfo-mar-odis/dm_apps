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

    @tag('report', 'url', 'report')
    def test_url_report_view(self):
        self.basic_en_url_test('whalesdb:report', 'whalesdb/report/', views.ReportView)

    @tag('cru', 'url', 'create')
    def test_url_create_cru_view(self):
        self.basic_en_url_test('whalesdb:create_cru', 'whalesdb/create/cru/', views.CruCreate)

    @tag('cru', 'url', 'update')
    def test_url_update_cru_view(self):
        self.basic_en_url_test('whalesdb:update_cru', 'whalesdb/update/cru/1/', views.CruUpdate, [1])

    @tag('cru', 'url', 'details')
    def test_url_details_cru_view(self):
        self.basic_en_url_test('whalesdb:details_cru', 'whalesdb/details/cru/1/', views.CruDetails, [1])

    @tag('cru', 'url', 'list')
    def test_url_list_cru_view(self):
        self.basic_en_url_test('whalesdb:list_cru', 'whalesdb/list/cru/', views.CruList)

    @tag('cru', 'url', 'delete')
    def test_url_delete_cru_view(self):
        self.basic_en_url_test('whalesdb:delete_cru', 'whalesdb/delete/cru/1/', views.CruDelete, [1])

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

    @tag('dep', 'url', 'delete')
    def test_url_delete_dep_view(self):
        self.basic_en_url_test('whalesdb:delete_dep', 'whalesdb/delete/dep/1/', views.dep_delete, [1])

    @tag('dep', 'url', 'list')
    def test_url_list_dep_view(self):
        self.basic_en_url_test('whalesdb:list_dep', 'whalesdb/list/dep/', views.DepList)

    @tag('dep', 'url', 'details')
    def test_url_details_dep_view(self):
        self.basic_en_url_test('whalesdb:details_dep', 'whalesdb/details/dep/1/', views.DepDetails, [1])

    @tag('ecc', 'url', 'create')
    def test_url_create_ecc_view(self):
        self.basic_en_url_test('whalesdb:create_ecc', 'whalesdb/create/ecc/1/pop/', views.EccCreate, [1, 'pop'])

    @tag('ecc', 'url', 'delete')
    def test_url_delete_ecc_view(self):
        self.basic_en_url_test('whalesdb:delete_ecc', 'whalesdb/delete/ecc/1/', views.ecc_delete, [1])

    @tag('eca', 'url', 'list')
    def test_url_list_eca_view(self):
        self.basic_en_url_test('whalesdb:list_eca', 'whalesdb/list/eca/', views.EcaList)

    @tag('eca', 'url', 'create')
    def test_url_create_eca_view(self):
        self.basic_en_url_test('whalesdb:create_eca', 'whalesdb/create/eca/', views.EcaCreate)

    @tag('eca', 'url', 'details')
    def test_url_details_eca_view(self):
        self.basic_en_url_test('whalesdb:details_eca', 'whalesdb/details/eca/1/', views.EcaDetails, [1])

    @tag('eca', 'url', 'update', 'pop')
    def test_url_update_eca_view(self):
        self.basic_en_url_test('whalesdb:update_eca', 'whalesdb/update/eca/1/', views.EcaUpdate, [1])

    @tag('ecp', 'url', 'create')
    def test_url_create_ecp_view(self):
        self.basic_en_url_test('whalesdb:create_ecp', 'whalesdb/create/ecp/1/pop/', views.EcpCreate, [1, 'pop'])

    @tag('eda', 'url', 'create')
    def test_url_create_eda_view(self):
        self.basic_en_url_test('whalesdb:create_eda', 'whalesdb/create/eda/1/', views.EdaCreate, [1])

    @tag('eda', 'url', 'create', 'pop')
    def test_url_create_pop_eda_view(self):
        self.basic_en_url_test('whalesdb:create_eda', 'whalesdb/create/eda/1/pop/', views.EdaCreate, [1, 'pop'])

    @tag('eda', 'url', 'delete', 'pop')
    def test_url_delete_pop_eda_view(self):
        self.basic_en_url_test('whalesdb:delete_eda', 'whalesdb/delete/eda/1/', views.eda_delete, [1])

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

    @tag('ehe', 'url', 'create')
    def test_url_create_pop_ehe_view(self):
        self.basic_en_url_test('whalesdb:create_ehe', 'whalesdb/create/ehe/1/1/pop/', views.EheCreate, [1, 1, 'pop'])

    @tag('ehe', 'url', 'manage')
    def test_url_update_ehe_view(self):
        self.basic_en_url_test('whalesdb:managed_ehe', 'whalesdb/managed/ehe/1/1/', views.EheMangedView, [1, 1])

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

    @tag('eqt', 'url', 'managed')
    def test_url_managed_rtt_view(self):
        self.basic_en_url_test('whalesdb:managed_eqt', 'whalesdb/settings/managed-eqt/', views.EqtMangedView)

    @tag('ert', 'url', 'managed')
    def test_url_managed_rtt_view(self):
        self.basic_en_url_test('whalesdb:managed_ert', 'whalesdb/settings/managed-ert/', views.ErtMangedView)

    @tag('etr', 'url', 'list')
    def test_url_list_etr_view(self):
        self.basic_en_url_test('whalesdb:list_etr', 'whalesdb/list/etr/', views.EtrList)

    @tag('etr', 'url', 'create')
    def test_url_create_etr_view(self):
        self.basic_en_url_test('whalesdb:create_etr', 'whalesdb/create/etr/', views.EtrCreate)

    @tag('etr', 'url', 'details')
    def test_url_details_etr_view(self):
        self.basic_en_url_test('whalesdb:details_etr', 'whalesdb/details/etr/1/', views.EtrDetails, [1])

    @tag('etr', 'url', 'update')
    def test_url_update_etr_view(self):
        self.basic_en_url_test('whalesdb:update_etr', 'whalesdb/update/etr/1/', views.EtrUpdate, [1])

    @tag('etr', 'url', 'update', 'pop')
    def test_url_update_pop_etr_view(self):
        self.basic_en_url_test('whalesdb:update_etr', 'whalesdb/update/etr/1/pop/', views.EtrUpdate, [1, 'pop'])

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

    @tag('prm', 'url', 'managed')
    def test_url_managed_prm_view(self):
        self.basic_en_url_test('whalesdb:managed_prm', 'whalesdb/settings/managed-prm/', views.PrmMangedView)

    @tag('ree', 'url', 'pop', 'update')
    def test_url_update_ree_pop_view(self):
        self.basic_en_url_test('whalesdb:update_ree', 'whalesdb/update/ree/1/pop/', views.ReeUpdate, [1, 'pop'])

    @tag('rsc', 'url', 'create')
    def test_url_create_rsc_view(self):
        self.basic_en_url_test('whalesdb:create_rsc', 'whalesdb/create/rsc/', views.RscCreate)

    @tag('rsc', 'url', 'update')
    def test_url_update_rsc_view(self):
        self.basic_en_url_test('whalesdb:update_rsc', 'whalesdb/update/rsc/1/', views.RscUpdate, [1])

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

    @tag('set', 'url', 'managed')
    def test_url_managed_set_view(self):
        self.basic_en_url_test('whalesdb:managed_set', 'whalesdb/settings/managed-set/', views.SetMangedView)

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

    @tag('ste', 'url', 'delete', 'pop')
    def test_url_delete_set_pop_ste_view(self):
        # The Station Event object requires a Deployment and a station event type
        self.basic_en_url_test('whalesdb:delete_ste', 'whalesdb/delete/ste/1/pop/', views.SteDelete, [1,'pop'])

    @tag('ste', 'url', 'update', 'pop')
    def test_url_update_set_pop_ste_view(self):
        self.basic_en_url_test('whalesdb:update_ste', 'whalesdb/update/ste/1/pop/', views.SteUpdate, [1, 'pop'])

    @tag('tea', 'url', 'create')
    def test_url_create_tea_view(self):
        self.basic_en_url_test('whalesdb:create_tea', 'whalesdb/create/tea/', views.TeaCreate)

    @tag('tea', 'url', 'update')
    def test_url_update_tea_view(self):
        self.basic_en_url_test('whalesdb:update_tea', 'whalesdb/update/tea/1/', views.TeaUpdate, [1,])

    @tag('tea', 'url', 'list')
    def test_url_list_tea_view(self):
        self.basic_en_url_test('whalesdb:list_tea', 'whalesdb/list/tea/', views.TeaList)

    @tag('tea', 'url', 'list')
    def test_url_list_tea_view(self):
        self.basic_en_url_test('whalesdb:list_tea', 'whalesdb/list/tea/', views.TeaList)

    @tag('rtt', 'url', 'managed')
    def test_url_managed_rtt_view(self):
        self.basic_en_url_test('whalesdb:managed_rtt', 'whalesdb/settings/managed-rtt/', views.RttMangedView)

    @tag('rec', 'url', 'create')
    def test_url_create_rec_view(self):
        self.basic_en_url_test('whalesdb:create_rec', 'whalesdb/create/rec/', views.RecCreate)

    @tag('rec', 'url', 'create')
    def test_url_create_rec_view(self):
        self.basic_en_url_test('whalesdb:create_rec', 'whalesdb/create/rec/1/', views.RecCreate, [1])

    @tag('rec', 'url', 'list')
    def test_url_list_rec_view(self):
        self.basic_en_url_test('whalesdb:list_rec', 'whalesdb/list/rec/', views.RecList)

    @tag('rec', 'url', 'update')
    def test_url_update_rec_view(self):
        self.basic_en_url_test('whalesdb:update_rec', 'whalesdb/update/rec/1/', views.RecUpdate, [1])

    @tag('rec', 'url', 'delete')
    def test_url_delete_rec_view(self):
        self.basic_en_url_test('whalesdb:delete_rec', 'whalesdb/delete/rec/1/pop/', views.RecDelete, [1, 'pop'])

    @tag('ret', 'url', 'create')
    def test_url_create_ret_view(self):
        self.basic_en_url_test('whalesdb:create_ret', 'whalesdb/create/ret/', views.RetCreate)

    @tag('ret', 'url', 'list')
    def test_url_list_ret_view(self):
        self.basic_en_url_test('whalesdb:list_ret', 'whalesdb/list/ret/', views.RetList)

    @tag('rci', 'url', 'create', 'pop')
    def test_url_create_rci_pop_ste_view(self):
        self.basic_en_url_test('whalesdb:create_rci', 'whalesdb/create/rci/1/pop/', views.RciCreate, [1, 'pop'])

    @tag('rci', 'url', 'delete', 'pop')
    def test_url_delete_rci_pop_ste_view(self):
        self.basic_en_url_test('whalesdb:delete_rci', 'whalesdb/delete/rci/1/', views.rci_delete, [1])

    @tag('ree', 'url', 'create', 'pop')
    def test_url_create_set_pop_ree_view(self):
        self.basic_en_url_test('whalesdb:create_ree', 'whalesdb/create/ree/1/pop/', views.ReeCreate, [1, 'pop'])

