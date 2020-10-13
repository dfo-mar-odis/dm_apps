from django.test import tag

from django.urls import reverse_lazy, resolve
from django.test import TestCase
from django.utils.translation import activate

from csas import views


class URLTest(TestCase):

    # test that a url signature can be reversed into an address,
    # an address gives an expected signature and the address
    # will link to the expected view or function
    def assert_basic_url(self, signature, url, view, args=None):
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

    def test_index_url(self):
        self.assert_basic_url('csas:index', 'csas/', views.IndexTemplateView)

    def test_req_list_url(self):
        self.assert_basic_url('csas:list_req', 'csas/request/', views.RequestList)

    def test_req_create_url(self):
        self.assert_basic_url('csas:create_req', 'csas/request/new/', views.RequestEntry)

    def test_req_update_url(self):
        self.assert_basic_url('csas:update_req', 'csas/request/update/1/', views.RequestUpdate, [1])

    def test_req_update_pop_url(self):
        self.assert_basic_url('csas:update_req', 'csas/request/update/1/pop/', views.RequestUpdate, [1, 'pop'])

    # Test that the URL for the view exists
    def test_coh_list_url(self):
        # test the CohHonorific url
        self.assert_basic_url('csas:list_coh', 'csas/lookup/coh/', views.CohList)

    # Test that the URL for the view exists
    def test_coh_create_url_pop(self):
        # test the CohHonorific url
        self.assert_basic_url('csas:create_coh', 'csas/create/coh/pop/', views.CreateCohView, ['pop'])

    # Test that the URL for the view exists
    def test_coh_create_url(self):
        # test the CohHonorific url
        self.assert_basic_url('csas:create_coh', 'csas/create/coh/', views.CreateCohView)

    # Test that the URL for the view exists
    def test_coh_update_url(self):
        # test the CohHonorific url
        self.assert_basic_url('csas:update_coh', 'csas/update/coh/1/pop/', views.UpdateCohView, [1, 'pop'])

    # Test that the URL for the view exists
    def test_stt_list_url(self):
        # test the CohHonorific url
        self.assert_basic_url('csas:list_stt', 'csas/lookup/stt/', views.SttList)

    # Test that the URL for the view exists
    def test_stt_create_url_pop(self):
        # test the sttHonorific url
        self.assert_basic_url('csas:create_stt', 'csas/create/stt/pop/', views.CreateSttView, ['pop'])

    # Test that the URL for the view exists
    def test_stt_create_url(self):
        # test the sttHonorific url
        self.assert_basic_url('csas:create_stt', 'csas/create/stt/', views.CreateSttView)

    # Test that the URL for the view exists
    def test_stt_update_url(self):
        # test the sttHonorific url
        self.assert_basic_url('csas:update_stt', 'csas/update/stt/1/pop/', views.UpdateSttView, [1, 'pop'])

    # Test that the URL for the view exists
    def test_meq_list_url(self):
        self.assert_basic_url('csas:list_meq', 'csas/lookup/meq/', views.MeqList)

    # Test that the URL for the view exists
    def test_meq_create_url_pop(self):
        self.assert_basic_url('csas:create_meq', 'csas/create/meq/pop/', views.CreateMeqView, ['pop'])

    # Test that the URL for the view exists
    def test_meq_create_url(self):
        self.assert_basic_url('csas:create_meq', 'csas/create/meq/', views.CreateMeqView)

    # Test that the URL for the view exists
    def test_meq_update_url(self):
        self.assert_basic_url('csas:update_meq', 'csas/update/meq/1/pop/', views.UpdateMeqView, [1, 'pop'])

    # Test that the URL for the view exists
    def test_loc_list_url(self):
        self.assert_basic_url('csas:list_loc', 'csas/lookup/loc/', views.LocList)

    # Test that the URL for the view exists
    def test_loc_create_url_pop(self):
        self.assert_basic_url('csas:create_loc', 'csas/create/loc/pop/', views.CreateLocView, ['pop'])

    # Test that the URL for the view exists
    def test_loc_create_url(self):
        self.assert_basic_url('csas:create_loc', 'csas/create/loc/', views.CreateLocView)

    # Test that the URL for the view exists
    def test_loc_update_url(self):
        self.assert_basic_url('csas:update_loc', 'csas/update/loc/1/pop/', views.UpdateLocView, [1, 'pop'])

    # Test that the URL for the view exists
    def test_apt_list_url(self):
        self.assert_basic_url('csas:list_apt', 'csas/lookup/apt/', views.AptList)

    # Test that the URL for the view exists
    def test_apt_create_url_pop(self):
        self.assert_basic_url('csas:create_apt', 'csas/create/apt/pop/', views.CreateAptView, ['pop'])

    # Test that the URL for the view exists
    def test_apt_create_url(self):
        self.assert_basic_url('csas:create_apt', 'csas/create/apt/', views.CreateAptView)

    # Test that the URL for the view exists
    def test_apt_update_url(self):
        self.assert_basic_url('csas:update_apt', 'csas/update/apt/1/pop/', views.UpdateAptView, [1, 'pop'])

    # Test that the URL for the view exists
    def test_scp_list_url(self):
        self.assert_basic_url('csas:list_scp', 'csas/lookup/scp/', views.ScpList)

    # Test that the URL for the view exists
    def test_scp_create_url_pop(self):
        self.assert_basic_url('csas:create_scp', 'csas/create/scp/pop/', views.CreateScpView, ['pop'])

    # Test that the URL for the view exists
    def test_scp_create_url(self):
        self.assert_basic_url('csas:create_scp', 'csas/create/scp/', views.CreateScpView)

    # Test that the URL for the view exists
    def test_scp_update_url(self):
        self.assert_basic_url('csas:update_scp', 'csas/update/scp/1/pop/', views.UpdateScpView, [1, 'pop'])
