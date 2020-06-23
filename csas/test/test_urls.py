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
