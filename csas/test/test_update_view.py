from django.test import TestCase, RequestFactory
from django.urls import reverse_lazy

from csas import views, models, forms
from csas.test import csas_common_test as cct
from csas.test import CsasFactory as Factory

from shared_models import views as shared_views


class CommonUpdateViewTest(cct.CommonTestCase):

    # view = None  # view is held by the common test case

    def setUp(self) -> None:

        self.view = views.CsasCommonUpdateView()

    def test_update_template(self):
        self.assertIn("csas/csas_entry_form.html", self.view.get_template_names())

    def test_update_extends(self):
        self.assertIsInstance(self.view, shared_views.CommonUpdateView)

    def test_update_nav_menu(self):
        nav = self.view.get_nav_menu()
        self.assertEquals(nav, cct.EXPECTED_NAV)

    def test_update_site_css(self):
        css = self.view.get_site_css()
        self.assertEquals(css, cct.EXPECTED_CSS)

    # test that if no user is logged in they will not be authorized to see add/update buttons in the template
    def test_anonymous_user_fail(self):
        self.assert_anonymous_user_auth_fail(url=None)

    # test that if the user is logged in, but not in the csas_admin group, they will not be authorized to see
    # add/update buttons in the template
    def test_regular_user_fail(self):
        self.assert_regular_user_auth_fail(url=None)

    # test that if a user is logged, and part of the csas_admin group, they will be authorized to see add/update
    # buttons in the template
    def test_csas_admin_func_pass(self):
        self.assert_csas_admin_user_auth_pass(url=None)

    def test_hide_nav_in_pop(self):
        req_faq = RequestFactory()
        request = req_faq.get(None)

        cct.setup_view(self.view, request, pop='pop')

        nav = self.view.get_nav_menu()
        self.assertIsNone(nav)


class ReqUpdateViewTest(TestCase):

    view = None

    def setUp(self) -> None:
        self.view = views.RequestUpdate()

    # Make sure the Req creation view is extending the CsasCommonCreateView class.
    def test_req_update_extends(self):
        self.assertIsInstance(self.view, views.CsasCommonUpdateView)

    # req should be using the ReqRequest model
    def test_req_update_model(self):
        self.assertEquals(self.view.model, models.ReqRequest)

    # upon success req redirects to the details view of the object being updated
    # in this case we have to create an object using a factory
    def test_req_success(self):
        # create an object to pretend it already existed in the database
        req = Factory.ReqRequestFactory()

        # set the update views object to the fake one
        self.view.object = req

        # get the success url
        addr = self.view.get_success_url()

        # we expect, for an update view, the url will point to the details page of the object we just
        # pretend updated
        self.assertEquals(addr, reverse_lazy('csas:details_req', args=(req.pk,)))

    # Use the RequestForm class for the req object
    def test_req_form(self):
        form_class = self.view.get_form_class()
        self.assertEquals(form_class, forms.RequestForm)
