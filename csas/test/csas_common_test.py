from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User, Group

EXPECTED_NAV = 'csas/csas_nav.html'
EXPECTED_CSS = 'csas/csas_css.css'

TEST_PASSWORD = 'test1234'


# use when a user needs to be logged in, and needs to be in the csas_super group
def login_csas_super(test_case):
    user_name = "Csas"
    if User.objects.filter(username=user_name):
        user = User.objects.get(username=user_name)
    else:
        csas_group = Group(name="csas_super")
        csas_group.save()

        user = User.objects.create_user(username=user_name, first_name="Hump", last_name="Back",
                                        email="Hump.Back@dfo-mpo.gc.ca", password=TEST_PASSWORD)
        user.groups.add(csas_group)
        user.save()

    test_case.client.login(username=user.username, password=TEST_PASSWORD)

    return user


# use when a user needs to be logged in, and needs to be in the csas_admin group
def login_csas_admin(test_case):
    user_name = "Csas"
    if User.objects.filter(username=user_name):
        user = User.objects.get(username=user_name)
    else:
        csas_group = Group(name="csas_admin")
        csas_group.save()

        user = User.objects.create_user(username=user_name, first_name="Hump", last_name="Back",
                                        email="Hump.Back@dfo-mpo.gc.ca", password=TEST_PASSWORD)
        user.groups.add(csas_group)
        user.save()

    test_case.client.login(username=user.username, password=TEST_PASSWORD)

    return user


# use when a user needs to be logged in, and needs to be in the csas_admin group
def login_csas_user(test_case):
    user_name = "Csas"
    if User.objects.filter(username=user_name):
        user = User.objects.get(username=user_name)
    else:
        csas_group = Group(name="csas_users")
        csas_group.save()

        user = User.objects.create_user(username=user_name, first_name="Hump", last_name="Back",
                                        email="Hump.Back@dfo-mpo.gc.ca", password=TEST_PASSWORD)
        user.groups.add(csas_group)
        user.save()

    test_case.client.login(username=user.username, password=TEST_PASSWORD)

    return user


# use when a user needs to be logged in.
def login_regular_user(test_case):
    user_name = "Csas"
    if User.objects.filter(username=user_name):
        user = User.objects.get(username=user_name)
    else:
        user = User.objects.create_user(username=user_name, first_name="Hump", last_name="Back",
                                        email="Hump.Back@dfo-mpo.gc.ca", password=TEST_PASSWORD)
        user.save()

    test_case.client.login(username=user.username, password=TEST_PASSWORD)

    return user


# This is used to simulate calling the as_veiw() function normally called in the urls.py
# this will return a view that can then have it's internal methods tested
def setup_view(view, request, *args, **kwargs):

    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


# Some additional assert methods for testing user authorization.
class CommonTestCase(TestCase):

    view = None

    # call to test if the anonymous user fails the authorization test
    def assert_anonymous_user_auth_fail(self, url=None):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(url)

        # set the user to Anonymous
        request.user = AnonymousUser()

        view = setup_view(self.view, request)

        # It's expected the view  will have a test_func() method, if it doesn't this will end badly
        auth = view.test_func()

        self.assertFalse(auth)

    # call to test if a regular user fails the authorization test
    def assert_regular_user_auth_fail(self, url=None):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(url)

        # set the user to csas_user
        request.user = login_regular_user(self)

        view = setup_view(self.view, request)

        # It's expected the view  will have a test_func() method, if it doesn't this will end badly
        auth = view.test_func()

        self.assertFalse(auth)

    # call to test if a csas_admin_user passes the authorization test
    def assert_csas_admin_user_auth_pass(self, url=None):
        # have to initialize the view as though Django did it.
        req_factory = RequestFactory()
        request = req_factory.get(url)

        # login the csas_admin user
        request.user = login_csas_user(self)

        view = setup_view(self.view, request)

        auth = view.test_func()

        self.assertTrue(auth, "Check the view {}".format(self.view))
