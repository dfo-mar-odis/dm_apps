from django.test import TestCase, RequestFactory

from csas import views
from csas.test import csas_common_test as cct

from django.contrib.auth.models import AnonymousUser


class CloserTemplateViewTest(TestCase):

    def test_close_template(self):
        view = views.CloserTemplateView()

        self.assertIn("shared_models/close_me.html", view.get_template_names())


class IndexTemplateViewTest(cct.CommonTestCase):

    def setUp(self) -> None:
        self.view = views.IndexTemplateView()

    def test_index_template(self):
        self.assertIn("csas/index.html", self.view.get_template_names())

    def test_index_get_context_anon(self):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(None)

        # set the user to Anonymous
        request.user = AnonymousUser()

        view = cct.setup_view(self.view, request)

        context = view.get_context_data()

        self.assertNotIn("csas_user", context)
        self.assertIn("auth", context)
        self.assertFalse(context["auth"])

    def test_index_get_context_csas_user(self):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(None)

        # login the csas_user user
        request.user = cct.login_csas_user(self)

        view = cct.setup_view(self.view, request)

        context = view.get_context_data()

        # csas_user is authorized for most things, but not all
        self.assertIn("auth", context)
        self.assertTrue(context["auth"])

        # csas_admin is authorized for all things
        self.assertIn("csas_admin", context)
        self.assertFalse(context["csas_admin"])

    def test_index_get_context_csas_admin(self):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(None)

        # login the csas_admin user
        request.user = cct.login_csas_admin(self)

        view = cct.setup_view(self.view, request)

        context = view.get_context_data()

        # csas_user is authorized for most things, but not all
        self.assertIn("auth", context)
        self.assertTrue(context["auth"])

        # csas_admin is authorized for all things
        self.assertIn("csas_admin", context)
        self.assertTrue(context["csas_admin"])
