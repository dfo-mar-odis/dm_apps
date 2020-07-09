from django.test import TestCase, RequestFactory
from django.urls import reverse_lazy
from django.contrib.auth.models import AnonymousUser

from shared_models import views as shared_views

from csas.test import csas_common_test as cct
from csas.views import CsasListCommon

from csas import models


# This is to test the CSAS extention of the Shared Model common framework.
class CommonListTest(cct.CommonTestCase):

    # view = None  # view is held by the CommonTestCase

    # Things common to each test should be set in this method. For example this test class is specifically to test
    # the csas.views.ListCommon view, so the self.view variable should be set here
    def setUp(self) -> None:
        self.view = CsasListCommon()

    # Make sure the view is extending the expected classes
    def test_list_extends(self):
        self.assertIsInstance(self.view, shared_views.CommonFilterView)

    # test the nav menu is as expected
    def test_list_nav(self):
        nav = self.view.get_nav_menu()
        self.assertEquals(nav, cct.EXPECTED_NAV)

    # test the css include is as expected
    def test_list_css(self):
        css = self.view.get_site_css()
        self.assertEquals(css, cct.EXPECTED_CSS)

    # test that if no user is logged in they will not be authorized to see add/update buttons in the template
    def test_anonymous_user_fail(self):
        self.assert_anonymous_user_auth_fail()

    # test that if the user is logged in, but not in the csas_admin group, they will not be authorized to see
    # add/update buttons in the template
    def test_regular_user_fail(self):
        self.assert_regular_user_auth_fail()

    # test that if a user is logged, and part of the csas_admin group, they will be authorized to see add/update
    # buttons in the template
    def test_csas_admin_func_pass(self):
        self.assert_csas_admin_user_auth_pass()

    # Test that the create_url, update_url, details_url are part of the context returned by get_context_data
    def test_list_get_context(self):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(reverse_lazy("csas:list_req"))
        request.user = AnonymousUser()

        # The shared model framework requires a title attribute
        self.view.title = "EXAMPLE TITLE"

        view = cct.setup_view(self.view, request)

        # filter views require their object_list attribute be set, django does this normally.
        view.object_list = models.ReqRequest.objects.all()
        view.model = models.ReqRequest

        context = view.get_context_data()

        # All we're doing here is checking to ensure these dictionary items exists since the template depends on them
        self.assertIn("create_url", context)
        self.assertIn("update_url", context)
        self.assertIn("details_url", context)

        self.assertIn("fields", context)

        # to show/hide the add/update buttons set context['auth']
        # should be false if no user is logged in
        self.assertFalse(context['auth'])

        request.user = cct.login_csas_user(self)

        view = cct.setup_view(self.view, request)
        context = view.get_context_data()

        # should be true with a csas user logged in
        self.assertTrue(context['auth'])
