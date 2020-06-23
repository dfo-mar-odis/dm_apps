from django.test import TestCase, tag, RequestFactory
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, ListView
from django_filters.views import FilterView

from shared_models import views, models
from .SharedModelsFactoryFloor import RegionFactory
from .common_tests import CommonTest

EXPECTED_LOGIN_URL = '/accounts/login_required/'
EXPECTED_FORM_TEMPLATE_NAME = 'shared_models/shared_entry_form.html'
EXPECTED_FILTER_TEMPLATE_NAME = 'shared_models/shared_filter.html'

EXPECTED_MOCK_TITLE = "Mock Title"


# This is used to simulate calling the as_veiw() function normally called in the urls.py
# this will return a view that can then have it's internal methods tested
def setup_view(view, request, *args, **kwargs):
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


# #################################################################################
#
#                       CommonMixin Testing
#
# #################################################################################
class TestCommonMixin(TestCase):
    view = None

    def setUp(self) -> None:
        self.view = views.CommonMixin()

    # The shared templates have a common layout that will display a form's title, so the CommonCreate
    # get_context method will return the title set in an extending class.
    def test_title(self):
        # CommonCreateView Should have the title
        self.assertTrue(hasattr(self.view, "title"))

        # The title should be null and overriden in an extending class. But be null in the parent
        self.assertIs(self.view.title, None)

    def test_title_exception(self):
        # The CommonCreate class will raise an exception if the dev forgot to set the title attribute
        self.assertRaises(AttributeError, self.view.get_common_context)

        self.view.title = EXPECTED_MOCK_TITLE

        # else the title should be returned by the get_title method
        self.assertEquals(self.view.get_title(), EXPECTED_MOCK_TITLE)

    # This frame work expects app urls to take a form app_label:create_[key], app_label:update_[key],
    # app_label:details_[key], app_label:list_[key]. The default functionality is that these URL names will be
    # created where needed in the respective common view class. Specifiy a key in the extending class and
    # The create view will create context variables with the expected URL Name.
    def test_key(self):
        # CommonCreateView Should have the key
        self.assertTrue(hasattr(self.view, "key"))

        # The key should be null and overriden in an extending class. But be null in the parent
        self.assertIs(self.view.key, None)

    # This frame work allows for the inclusion of a nav_menu attribute, if present it will be
    # included in the base forms and a navigation menu displayed at the top of a page
    def test_nav_menu(self):
        # CommonCreateView Should have the attribute
        self.assertTrue(hasattr(self.view, "nav_menu"))

        # The attribute should be null and overriden in an extending class. But be null in the parent
        self.assertIs(self.view.nav_menu, None)

    # This frame work allows for the inclusion of a java_script attribute, if present it will be
    # included in the base forms
    def test_java_script(self):
        # CommonCreateView Should have the attribute
        self.assertTrue(hasattr(self.view, "java_script"))

        # The attribute should be null and overriden in an extending class. But be null in the parent
        self.assertIs(self.view.java_script, None)

    # This frame work allows for the inclusion of a site_css attribute, if present it will be
    # included in the base forms template
    def test_site_css(self):
        # CommonCreateView Should have the attribute
        self.assertTrue(hasattr(self.view, "site_css"))

        # The attribute should be null and overriden in an extending class. But be null in the parent
        self.assertIs(self.view.site_css, None)

    # tests that if a kwarg pop is passed to the request the extended method in the mock class
    # can preform some operation on the java_script variable.
    def test_get_java_script(self):
        self.view.java_script = "some/location.js"
        self.assertEquals(self.view.get_java_script(), "some/location.js")

    # tests that if a kwarg pop is passed to the request the extended method in the mock class
    # can preform some operation on the nav_menu variable.
    def test_get_nav_menu(self):
        self.view.nav_menu = "some/nav_menu.html"
        self.assertEquals(self.view.get_nav_menu(), "some/nav_menu.html")

    # tests that if a kwarg pop is passed to the request the extended method in the mock class
    # can preform some operation on the site_css variable.
    def test_get_site_css(self):
        self.view.site_css = "some/site_css.css"
        self.assertEquals(self.view.get_site_css(), "some/site_css.css")

    def test_common_get_context(self):
        self.view.title = EXPECTED_MOCK_TITLE

        self.assertNotIn("java_script", self.view.get_common_context())

        self.view.java_script = "some/location.js"
        self.assertIn("java_script", self.view.get_common_context())
        self.assertEquals(self.view.get_common_context()['java_script'], "some/location.js")

        self.assertNotIn("nav_menu", self.view.get_common_context())

        self.view.nav_menu = "some/nav.html"
        self.assertIn("nav_menu", self.view.get_common_context())
        self.assertEquals(self.view.get_common_context()['nav_menu'], "some/nav.html")

        self.assertNotIn("site_css", self.view.get_common_context())

        self.view.site_css = "some/site.css"
        self.assertIn("site_css", self.view.get_common_context())
        self.assertEquals(self.view.get_common_context()['site_css'], "some/site.css")


# #################################################################################
#
#                       CommonTemplateView Testing
#
# #################################################################################


# mock example of extending the create common view used in testing
class MockCommonTemplateView(views.CommonCreateView):
    # These are required at a minimum by extending classes as part of Django's base framework
    model = models.Region
    fields = []

    # These are for testing purposes only
    auth = True
    editable = True

    # this should be overriden in an extending class to determine if a user is authorized to do certain actions
    def test_func(self):
        return self.auth

    # example of overriding the get_java_script function to return something other than the java_script variable
    def get_java_script(self):
        if self.kwargs.get("pop"):
            return "pop/{}".format(self.java_script)

        return super().get_java_script()

    # example of overriding the get_nav_menu function to return something other than the nav_menu variable
    def get_nav_menu(self):
        if self.kwargs.get("pop"):
            return "pop/{}".format(self.nav_menu)

        return super().get_nav_menu()

    # example of overriding the get_site_css function to return something other than the site_css variable
    def get_site_css(self):
        if self.kwargs.get("pop"):
            return "pop/{}".format(self.site_css)

        return super().get_site_css()


class TestCommonTemplateView(TestCase):

    # In order to test users should be allowed to create database objects extending apps should make use of the test_
    # func method that comes from Django's django.contrib.auth.mixins.UserPassesTestMixin module. As such
    # the CommonCreateView class is an abstract class with CreateView and UserPassesTestMixin as super classes
    def test_extends(self):
        view = views.CommonTemplateView()

        self.assertIsInstance(view, TemplateView)
        self.assertIsInstance(view, views.CommonMixin)

    # if the test_func method returns true then the get_context method will return an auth element used by
    # templates to determine when to show/hide certain elements
    def test_get_context(self):
        # have to create the request and setup the view
        req_factory = RequestFactory()
        request = req_factory.get(EXPECTED_LOGIN_URL)
        view = setup_view(MockCommonTemplateView(), request)
        view.object = models.Region()
        view.title = EXPECTED_MOCK_TITLE

        # at this point there is nothing more to test in this view. I am keeping this test as a placeholder for future tests


# #################################################################################
#
#                       CommonCreateView Testing
#
# #################################################################################


# mock example of extending the create common view used in testing
class MockCommonCreateView(views.CommonCreateView):
    # These are required at a minimum by extending classes as part of Django's base framework
    model = models.Region
    fields = []

    # These are for testing purposes only
    editable = True

    # example of overriding the get_java_script function to return something other than the java_script variable
    def get_java_script(self):
        if self.kwargs.get("pop"):
            return "pop/{}".format(self.java_script)

        return super().get_java_script()

    # example of overriding the get_nav_menu function to return something other than the nav_menu variable
    def get_nav_menu(self):
        if self.kwargs.get("pop"):
            return "pop/{}".format(self.nav_menu)

        return super().get_nav_menu()

    # example of overriding the get_site_css function to return something other than the site_css variable
    def get_site_css(self):
        if self.kwargs.get("pop"):
            return "pop/{}".format(self.site_css)

        return super().get_site_css()


class TestCommonCreateView(TestCase):

    # In order to test users should be allowed to create database objects extending apps should make use of the test_
    # func method that comes from Django's django.contrib.auth.mixins.UserPassesTestMixin module. As such
    # the CommonCreateView class is an abstract class with CreateView and UserPassesTestMixin as super classes
    def test_extends(self):
        view = views.CommonCreateView()

        self.assertIsInstance(view, CreateView)
        self.assertIsInstance(view, views.CommonMixin)
        self.assertIsInstance(view, views.CommonFormMixin)

    # Create common by default uses the simple shared_models/shared_entry_form.html template
    # Extending classes can provide their own templates modeled on the shared_entry_form.html Template
    def test_template(self):
        view = views.CommonCreateView()
        self.assertEquals(view.template_name, EXPECTED_FORM_TEMPLATE_NAME)

    # if the test_func method returns true then the get_context method will return an auth element used by
    # templates to determine when to show/hide certain elements
    def test_get_context(self):
        # have to create the request and setup the view
        req_factory = RequestFactory()
        request = req_factory.get(EXPECTED_LOGIN_URL)
        view = setup_view(MockCommonCreateView(), request)
        view.object = models.Region()
        view.title = EXPECTED_MOCK_TITLE

        # without overriding the defaults, h1 and submit_text should have specific values
        self.assertEqual(view.get_context_data()['h1'], _("New {}".format(view.model._meta.verbose_name.title())))
        self.assertEqual(view.get_context_data()['submit_text'], _("Add"))


# #################################################################################
#
#                       CommonAuthCreateView Testing
#
# #################################################################################

# mock example of extending the create common view used in testing
class MockCommonAuthCreateView(views.CommonAuthCreateView, MockCommonCreateView):
    auth = True

    # this should be overriden in an extending class to determine if a user is authorized to do certain actions
    def test_func(self):
        return self.auth


# Testing for CommonCreate view, used in:
class TestCommonAuthCreateView(TestCommonCreateView):
    def test_extends(self):
        view = views.CommonAuthCreateView()
        self.assertIsInstance(view, UserPassesTestMixin)
        self.assertIsInstance(view, CreateView)
        self.assertIsInstance(view, views.CommonMixin)
        self.assertIsInstance(view, views.CommonFormMixin)
        self.assertIsInstance(view, views.CommonCreateView)

    # All DM apps share a common login system so it makes sense that common views should direct
    # users to the common login URL
    def test_login_url(self):
        view = views.CommonAuthCreateView()

        # CreateCommon Should have the login_url attribute
        self.assertTrue(hasattr(view, "login_url"))

        # Expected Login URL
        self.assertEquals(view.login_url, EXPECTED_LOGIN_URL)

    def test_get_context(self):
        super().test_get_context()
        # have to create the request and setup the view
        req_factory = RequestFactory()
        request = req_factory.get(EXPECTED_LOGIN_URL)
        view = setup_view(MockCommonAuthCreateView(), request)
        view.object = models.Region()
        view.title = EXPECTED_MOCK_TITLE

        # the context should contain a title element
        self.assertIn("auth", view.get_context_data())
        self.assertTrue(view.get_context_data()['auth'])
        view.auth = False
        self.assertFalse(view.get_context_data()['auth'])


# #################################################################################
#
#                       CommonUpdateView Testing
#
# #################################################################################


# mock example of extending the update common view used in testing, virtually the same as CommonCreateView
class MockCommonUpdateView(views.CommonUpdateView):
    # These are required at a minimum by extending classes as part of Django's base framework
    model = models.Region
    fields = []

    # These are for testing purposes only
    editable = True

    # example of overriding the get_java_script function to return something other than the java_script variable
    def get_java_script(self):
        if self.kwargs.get("pop"):
            return "pop/{}".format(self.java_script)

        return super().get_java_script()

    # example of overriding the get_nav_menu function to return something other than the nav_menu variable
    def get_nav_menu(self):
        if self.kwargs.get("pop"):
            return "pop/{}".format(self.nav_menu)

        return super().get_nav_menu()

    # example of overriding the get_site_css function to return something other than the site_css variable
    def get_site_css(self):
        if self.kwargs.get("pop"):
            return "pop/{}".format(self.site_css)

        return super().get_site_css()

    def get_object(self, queryset=None):
        return models.Region.objects.first()


# Testing for CommonUpdateView view, used in:
class TestCommonUpdateView(TestCase):

    def setUp(self) -> None:
        RegionFactory()

    # In order to test users should be allowed to create database objects extending apps should make use of the test_
    # func method that comes from Django's django.contrib.auth.mixins.UserPassesTestMixin module. As such
    # the CommonUpdateView class is an abstract class with UpdateView and UserPassesTestMixin as super classes
    def test_extends(self):
        view = views.CommonUpdateView()

        # self.assertIsInstance(view, UserPassesTestMixin)
        self.assertIsInstance(view, UpdateView)
        self.assertIsInstance(view, views.CommonMixin)
        self.assertIsInstance(view, views.CommonFormMixin)

    # Update common by default uses the simple shared_models/shared_entry_form.html template
    # Extending classes can provide their own templates modeled on the shared_entry_form.html Template
    def test_template(self):
        view = views.CommonUpdateView()
        self.assertEquals(view.template_name, EXPECTED_FORM_TEMPLATE_NAME)

    # if the test_func method returns true then the get_context method will return an auth element used by
    # templates to determine when to show/hide certain elements
    def test_get_context(self):
        # have to create the request and setup the view
        req_factory = RequestFactory()
        request = req_factory.get(EXPECTED_LOGIN_URL)
        view = setup_view(MockCommonUpdateView(), request)
        view.object = models.Region()
        view.title = EXPECTED_MOCK_TITLE

        # without overriding the defaults, h1 and submit_text should have specific values
        self.assertEqual(view.get_context_data()['h1'], _("Edit"))
        self.assertEqual(view.get_context_data()['submit_text'], _("Save"))

        # should have a context var called model_name
        self.assertIn("model_name", view.get_context_data())


# #################################################################################
#
#                       CommonAuthUpdateView Testing
#
# #################################################################################

# mock example of extending the create common view used in testing
class MockCommonAuthUpdateView(views.CommonAuthUpdateView, MockCommonUpdateView):
    auth = True

    # this should be overriden in an extending class to determine if a user is authorized to do certain actions
    def test_func(self):
        return self.auth


# Testing for CommonUpdate view, used in:
class TestCommonAuthUpdateView(TestCommonUpdateView):
    def test_extends(self):
        view = views.CommonAuthUpdateView()
        self.assertIsInstance(view, UserPassesTestMixin)
        self.assertIsInstance(view, UpdateView)
        self.assertIsInstance(view, views.CommonMixin)
        self.assertIsInstance(view, views.CommonFormMixin)
        self.assertIsInstance(view, views.CommonUpdateView)

    # All DM apps share a common login system so it makes sense that common views should direct
    # users to the common login URL
    def test_login_url(self):
        view = views.CommonAuthUpdateView()

        # UpdateCommon Should have the login_url attribute
        self.assertTrue(hasattr(view, "login_url"))

        # Expected Login URL
        self.assertEquals(view.login_url, EXPECTED_LOGIN_URL)

    def test_get_context(self):
        super().test_get_context()
        # have to create the request and setup the view
        req_factory = RequestFactory()
        request = req_factory.get(EXPECTED_LOGIN_URL)
        view = setup_view(MockCommonAuthUpdateView(), request)
        view.object = models.Region()
        view.title = EXPECTED_MOCK_TITLE

        # the context should contain a title element
        self.assertIn("auth", view.get_context_data())
        self.assertTrue(view.get_context_data()['auth'])
        view.auth = False
        self.assertFalse(view.get_context_data()['auth'])


# #################################################################################
#
#                       CommonDeleteView Testing
#
# #################################################################################


# mock example of extending the update common view used in testing, virtually the same as CommonCreateView
class MockCommonDeleteView(views.CommonDeleteView):
    # These are required at a minimum by extending classes as part of Django's base framework
    model = models.Region
    fields = []

    # These are for testing purposes only
    auth = True
    editable = True

    # this should be overriden in an extending class to determine if a user is authorized to do certain actions
    def test_func(self):
        return self.auth

    # example of overriding the get_java_script function to return something other than the java_script variable
    def get_java_script(self):
        if self.kwargs.get("pop"):
            return "pop/{}".format(self.java_script)

        return super().get_java_script()

    # example of overriding the get_nav_menu function to return something other than the nav_menu variable
    def get_nav_menu(self):
        if self.kwargs.get("pop"):
            return "pop/{}".format(self.nav_menu)

        return super().get_nav_menu()

    # example of overriding the get_site_css function to return something other than the site_css variable
    def get_site_css(self):
        if self.kwargs.get("pop"):
            return "pop/{}".format(self.site_css)

        return super().get_site_css()

    def get_object(self, queryset=None):
        return models.Region.objects.first()


# Testing for CommonUpdateView view, used in:
class TestCommonDeleteView(TestCase):

    def setUp(self) -> None:
        RegionFactory()

    # In order to test users should be allowed to create database objects extending apps should make use of the test_
    # func method that comes from Django's django.contrib.auth.mixins.UserPassesTestMixin module. As such
    # the CommonUpdateView class is an abstract class with UpdateView and UserPassesTestMixin as super classes
    def test_extends(self):
        view = views.CommonDeleteView()

        # self.assertIsInstance(view, UserPassesTestMixin)
        self.assertIsInstance(view, DeleteView)
        self.assertIsInstance(view, views.CommonMixin)
        self.assertIsInstance(view, views.CommonFormMixin)

    # Update common by default uses the simple shared_models/shared_entry_form.html template
    # Extending classes can provide their own templates modeled on the shared_entry_form.html Template
    def test_template(self):
        view = views.CommonDeleteView()
        self.assertEquals(view.template_name, 'shared_models/generic_confirm_delete.html')

    # if the test_func method returns true then the get_context method will return an auth element used by
    # templates to determine when to show/hide certain elements
    def test_get_context(self):
        # have to create the request and setup the view
        req_factory = RequestFactory()
        request = req_factory.get(EXPECTED_LOGIN_URL)
        view = setup_view(MockCommonDeleteView(), request)
        view.object = models.Region

        # without overriding the defaults, h1 and submit_text should have specific values
        self.assertEqual(view.get_context_data()['h1'],
                         _("Are you sure you want to delete the following {}? <br>  <span class='red-font'>{}</span>".format(
                             view.model._meta.verbose_name,
                             view.get_object(),
                         )))
        self.assertEqual(view.get_context_data()['submit_text'], _("Delete"))

        # should have a context var called model_name
        self.assertIn("model_name", view.get_context_data())
        self.assertIn("delete_protection", view.get_context_data())
        self.assertIn("related_names", view.get_context_data())


# #################################################################################
#
#                       CommonFilterView Testing
#
# #################################################################################

class MockCommonFilterView(views.CommonFilterView):
    # These are required at a minimum by extending classes as part of Django's base framework
    model = models.Region
    fields = []
    object_list = models.Region.objects.all()


class TestCommonFilterView(TestCase):
    view = None

    def setUp(self) -> None:
        self.view = views.CommonFilterView()
        RegionFactory()

    # CommonFilterView Extends django_filters.views.FilterView
    def test_filter_extends(self):
        self.assertIsInstance(self.view, FilterView)
        self.assertIsInstance(self.view, views.CommonMixin)
        self.assertIsInstance(self.view, views.CommonListMixin)

    # Update common by default uses the simple shared_models/shared_entry_form.html template
    # Extending classes can provide their own templates modeled on the shared_entry_form.html Template
    def test_filter_template(self):
        self.assertEquals(self.view.template_name, EXPECTED_FILTER_TEMPLATE_NAME)

    def test_get_context(self):
        # have to create the request and setup the view
        req_factory = RequestFactory()
        request = req_factory.get(EXPECTED_LOGIN_URL)
        view = setup_view(MockCommonFilterView(), request)
        view.object_list = models.Region.objects.all()
        view.title = EXPECTED_MOCK_TITLE


# #################################################################################
#
#                       CommonAuthFilterView Testing
#
# #################################################################################

# mock example of extending the create common view used in testing
class MockCommonAuthFilterView(views.CommonAuthFilterView, MockCommonFilterView):
    auth = True

    # this should be overriden in an extending class to determine if a user is authorized to do certain actions
    def test_func(self):
        return self.auth


# Testing for CommonFilter view, used in:
class TestCommonAuthFilterView(TestCommonFilterView):
    def test_extends(self):
        view = views.CommonAuthFilterView()
        self.assertIsInstance(view, UserPassesTestMixin)
        self.assertIsInstance(view, FilterView)
        self.assertIsInstance(view, views.CommonMixin)
        self.assertIsInstance(view, views.CommonFilterView)

    # All DM apps share a common login system so it makes sense that common views should direct
    # users to the common login URL
    def test_login_url(self):
        view = views.CommonAuthFilterView()

        # FilterCommon Should have the login_url attribute
        self.assertTrue(hasattr(view, "login_url"))

        # Expected Login URL
        self.assertEquals(view.login_url, EXPECTED_LOGIN_URL)

    def test_get_context(self):
        super().test_get_context()
        # have to create the request and setup the view
        req_factory = RequestFactory()
        request = req_factory.get(EXPECTED_LOGIN_URL)
        view = setup_view(MockCommonAuthFilterView(), request)
        view.object = models.Region()
        view.title = EXPECTED_MOCK_TITLE

        # the context should contain a title element
        self.assertIn("auth", view.get_context_data())
        self.assertTrue(view.get_context_data()['auth'])
        view.auth = False
        self.assertFalse(view.get_context_data()['auth'])


class TestIndexTemplateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('shared_models:index')
        self.expected_template = 'shared_models/org_index.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")
        self.admin_user1 = self.get_and_login_user(in_group="travel_adm_admin")

    @tag("index", "view")
    def test_view_class(self):
        self.assert_inheritance(views.IndexTemplateView, TemplateView)
        self.assert_inheritance(views.IndexTemplateView, views.AdminRequiredMixin)

    @tag("index", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user1)


# #################################################################################
#
#                       CommonListView Testing
#
# #################################################################################


# mock example of extending the update common view used in testing, virtually the same as CommonCreateView
class MockCommonListView(views.CommonListView):
    # These are required at a minimum by extending classes as part of Django's base framework
    model = models.Region
    fields = []
    object_list = models.Region.objects.all()

    # These are for testing purposes only
    auth = True
    editable = True

    # this should be overriden in an extending class to determine if a user is authorized to do certain actions
    def test_func(self):
        return self.auth

    # example of overriding the get_java_script function to return something other than the java_script variable
    def get_java_script(self):
        if self.kwargs.get("pop"):
            return "pop/{}".format(self.java_script)

        return super().get_java_script()

    # example of overriding the get_nav_menu function to return something other than the nav_menu variable
    def get_nav_menu(self):
        if self.kwargs.get("pop"):
            return "pop/{}".format(self.nav_menu)

        return super().get_nav_menu()

    # example of overriding the get_site_css function to return something other than the site_css variable
    def get_site_css(self):
        if self.kwargs.get("pop"):
            return "pop/{}".format(self.site_css)

        return super().get_site_css()


# Testing for CommonUpdateView view, used in:
class TestCommonListView(TestCase):

    def setUp(self) -> None:
        RegionFactory()

    # In order to test users should be allowed to create database objects extending apps should make use of the test_
    # func method that comes from Django's django.contrib.auth.mixins.UserPassesTestMixin module. As such
    # the CommonUpdateView class is an abstract class with UpdateView and UserPassesTestMixin as super classes
    def test_extends(self):
        view = views.CommonListView()

        # self.assertIsInstance(view, UserPassesTestMixin)
        self.assertIsInstance(view, ListView)
        self.assertIsInstance(view, views.CommonMixin)
        self.assertIsInstance(view, views.CommonListMixin)

    # Update common by default uses the simple shared_models/shared_entry_form.html template
    # Extending classes can provide their own templates modeled on the shared_entry_form.html Template
    def test_template(self):
        view = views.CommonListView()
        self.assertEquals(view.template_name, 'shared_models/generic_filter.html')

    # if the test_func method returns true then the get_context method will return an auth element used by
    # templates to determine when to show/hide certain elements
    def test_get_context(self):
        # have to create the request and setup the view
        req_factory = RequestFactory()
        request = req_factory.get(EXPECTED_LOGIN_URL)
        view = setup_view(MockCommonListView(), request)
        view.object = models.Region

        # without overriding the defaults, h1 and submit_text should have specific values
        self.assertEqual(view.get_context_data()['h1'], view.get_queryset().model._meta.verbose_name_plural.title())

        # should have a context var called model_name
        self.assertIn("model_name", view.get_context_data())
