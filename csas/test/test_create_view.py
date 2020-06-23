from django.test import TestCase, RequestFactory
from django.urls import reverse_lazy
from django.contrib.auth.models import AnonymousUser

from csas.views import CsasCommonCreateView, RequestEntry
from csas.test import csas_common_test as cct

from csas import models, forms

from shared_models import views as shared_views


# Test the CSAS' extention of the shared_models CommonCreateView shared framework
class CommonCreateViewTest(cct.CommonTestCase):

    view = None

    def setUp(self) -> None:
        self.view = CsasCommonCreateView()
        self.view.title = 'EXAMPLE TITLE'

    def test_ceate_template(self):
        self.assertIn("csas/csas_entry_form.html", self.view.get_template_names())

    def test_create_extends(self):
        self.assertIsInstance(self.view, shared_views.CommonCreateView)

    def test_create_nav_menu(self):
        nav = self.view.get_nav_menu()
        self.assertEquals(nav, cct.EXPECTED_NAV)

    def test_create_css(self):
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


class ReqCreateViewTest(TestCase):

    # view = None  # view object is held in the cct.CommonTestCase class

    def setUp(self) -> None:
        self.view = RequestEntry()

    # Make sure the Req creation view is extending the CsasCommonCreateView class.
    def test_req_create_extends(self):
        self.assertIsInstance(self.view, CsasCommonCreateView)

    # req should be using the ReqRequest model
    def test_req_create_model(self):
        self.assertEquals(self.view.model, models.ReqRequest)

    # upon success req redirects to the req filter view
    def test_req_success(self):
        addr = self.view.get_success_url()
        self.assertEquals(addr, reverse_lazy('csas:list_req'))

    # Use the RequestForm class for the req object
    def test_req_form(self):
        form_class = self.view.get_form_class()
        self.assertEquals(form_class, forms.RequestForm)
