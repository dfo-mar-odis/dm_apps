from django.test import TestCase, RequestFactory
from django.urls import reverse_lazy
from django.contrib.auth.models import AnonymousUser

from shared_models import views as shared_views

from csas.test import csas_common_test as cct, test_urls as urt
from csas.views import CsasListCommon, CohList, SttList, MeqList, AptList, ScpList

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


# Used for testing listing values from models extending the Lookup model
class CohListTest(cct.CommonTestCase):

    def setUp(self) -> None:
        self.view = CohList()

    # Make sure the view is extending the expected classes
    def test_Coh_list_extends(self):
        self.assertIsInstance(self.view, CohList)

    # Test that given a key the lookup view will return the proper model
    def test_Coh_list_get_model(self):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(reverse_lazy("csas:list_coh"))

        view = cct.setup_view(self.view, request)

        self.assertIs(view.model, models.CohHonorific)

    # users should be authenticated in the csas_super group to user this view
    def test_Coh_list_not_auth(self):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(None)
        self.view.object_list = []

        # login the regular user
        request.user = cct.login_regular_user(self)
        view = cct.setup_view(self.view, request)
        context = view.get_context_data()

        # csas_user is authorized for most things, but not all
        self.assertIn("auth", context)
        self.assertFalse(context["auth"])

    # users should be authenticated in the csas_super group to user this view
    def test_Coh_list_super_auth(self):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(None)
        self.view.object_list = []

        # login the csas_admin user
        request.user = cct.login_csas_super(self)
        view = cct.setup_view(self.view, request)
        context = view.get_context_data()

        # csas_user is authorized for most things, but not all
        self.assertIn("auth", context)
        self.assertTrue(context["auth"])

        # csas_super is authorized for all things
        self.assertIn("csas_super", context)
        self.assertTrue(context["csas_super"])


# Used for testing listing values from models extending the Lookup model
class SttListTest(cct.CommonTestCase):

    def setUp(self) -> None:
        self.view = SttList()

    # Make sure the view is extending the expected classes
    def test_Stt_list_extends(self):
        self.assertIsInstance(self.view, SttList)

    # Test that given a key the lookup view will return the proper model
    def test_Stt_list_get_model(self):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(reverse_lazy("csas:list_stt"))

        view = cct.setup_view(self.view, request)

        self.assertIs(view.model, models.SttStatus)

    # users should be authenticated in the csas_super group to user this view
    def test_Stt_list_not_auth(self):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(None)
        self.view.object_list = []

        # login the regular user
        request.user = cct.login_regular_user(self)
        view = cct.setup_view(self.view, request)
        context = view.get_context_data()

        # csas_user is authorized for most things, but not all
        self.assertIn("auth", context)
        self.assertFalse(context["auth"])

    # users should be authenticated in the csas_super group to user this view
    def test_Stt_list_super_auth(self):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(None)
        self.view.object_list = []

        # login the csas_admin user
        request.user = cct.login_csas_super(self)
        view = cct.setup_view(self.view, request)
        context = view.get_context_data()

        # csas_user is authorized for most things, but not all
        self.assertIn("auth", context)
        self.assertTrue(context["auth"])

        # csas_super is authorized for all things
        self.assertIn("csas_super", context)
        self.assertTrue(context["csas_super"])


# Used for testing listing values from models extending the Lookup model
class MeqListTest(cct.CommonTestCase):

    def setUp(self) -> None:
        self.view = MeqList()

    # Make sure the view is extending the expected classes
    def test_Meq_list_extends(self):
        self.assertIsInstance(self.view, MeqList)

    # Test that given a key the lookup view will return the proper model
    def test_Meq_list_get_model(self):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(reverse_lazy("csas:list_meq"))

        view = cct.setup_view(self.view, request)

        self.assertIs(view.model, models.MeqQuarter)

    # users should be authenticated in the csas_super group to user this view
    def test_Meq_list_not_auth(self):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(None)
        self.view.object_list = []

        # login the regular user
        request.user = cct.login_regular_user(self)
        view = cct.setup_view(self.view, request)
        context = view.get_context_data()

        # csas_user is authorized for most things, but not all
        self.assertIn("auth", context)
        self.assertFalse(context["auth"])

    # users should be authenticated in the csas_super group to user this view
    def test_Meq_list_super_auth(self):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(None)
        self.view.object_list = []

        # login the csas_admin user
        request.user = cct.login_csas_super(self)
        view = cct.setup_view(self.view, request)
        context = view.get_context_data()

        # csas_user is authorized for most things, but not all
        self.assertIn("auth", context)
        self.assertTrue(context["auth"])

        # csas_super is authorized for all things
        self.assertIn("csas_super", context)
        self.assertTrue(context["csas_super"])


# Used for testing listing values from models extending the Lookup model
class AptListTest(cct.CommonTestCase):

    def setUp(self) -> None:
        self.view = AptList()

    # Make sure the view is extending the expected classes
    def test_Apt_list_extends(self):
        self.assertIsInstance(self.view, AptList)

    # Test that given a key the lookup view will return the proper model
    def test_Apt_list_get_model(self):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(reverse_lazy("csas:list_apt"))

        view = cct.setup_view(self.view, request)

        self.assertIs(view.model, models.AptAdvisoryProcessType)

    # users should be authenticated in the csas_super group to user this view
    def test_Apt_list_not_auth(self):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(None)
        self.view.object_list = []

        # login the regular user
        request.user = cct.login_regular_user(self)
        view = cct.setup_view(self.view, request)
        context = view.get_context_data()

        # csas_user is authorized for most things, but not all
        self.assertIn("auth", context)
        self.assertFalse(context["auth"])

    # users should be authenticated in the csas_super group to user this view
    def test_Apt_list_super_auth(self):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(None)
        self.view.object_list = []

        # login the csas_admin user
        request.user = cct.login_csas_super(self)
        view = cct.setup_view(self.view, request)
        context = view.get_context_data()

        # csas_user is authorized for most things, but not all
        self.assertIn("auth", context)
        self.assertTrue(context["auth"])

        # csas_super is authorized for all things
        self.assertIn("csas_super", context)
        self.assertTrue(context["csas_super"])


# Used for testing listing values from models extending the Lookup model
class ScpListTest(cct.CommonTestCase):

    def setUp(self) -> None:
        self.view = ScpList()

    # Make sure the view is extending the expected classes
    def test_Scp_list_extends(self):
        self.assertIsInstance(self.view, ScpList)

    # Test that given a key the lookup view will return the proper model
    def test_Scp_list_get_model(self):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(reverse_lazy("csas:list_apt"))

        view = cct.setup_view(self.view, request)

        self.assertIs(view.model, models.ScpScope)

    # users should be authenticated in the csas_super group to user this view
    def test_Scp_list_not_auth(self):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(None)
        self.view.object_list = []

        # login the regular user
        request.user = cct.login_regular_user(self)
        view = cct.setup_view(self.view, request)
        context = view.get_context_data()

        # csas_user is authorized for most things, but not all
        self.assertIn("auth", context)
        self.assertFalse(context["auth"])

    # users should be authenticated in the csas_super group to user this view
    def test_Scp_list_super_auth(self):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(None)
        self.view.object_list = []

        # login the csas_admin user
        request.user = cct.login_csas_super(self)
        view = cct.setup_view(self.view, request)
        context = view.get_context_data()

        # csas_user is authorized for most things, but not all
        self.assertIn("auth", context)
        self.assertTrue(context["auth"])

        # csas_super is authorized for all things
        self.assertIn("csas_super", context)
        self.assertTrue(context["csas_super"])
