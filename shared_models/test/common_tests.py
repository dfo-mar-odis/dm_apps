import os

from django.conf import settings
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils.translation import activate
from html2text import html2text

from shared_models.test.SharedModelsFactoryFloor import UserFactory, GroupFactory

fixtures_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fixtures')
standard_fixtures = [file for file in os.listdir(fixtures_dir)]


def setup_view(view, request, *args, **kwargs):
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


###########################################################################################
# Common Test for all views, this includes checking that a view is accessible or provides
# a redirect if permissions are required to access a view
###########################################################################################
class CommonTest(TestCase):
    fixtures = standard_fixtures

    login_url_base = '/accounts/login/?next='
    login_url_en = login_url_base + "/en/"
    login_url_fr = login_url_base + "/fr/"
    expected_form = None

    # use when a user needs to be logged in.
    def get_and_login_user(self, user=None, in_group=None, is_superuser=False):
        """
        this function is a handy way to log in a user to the testing client.
        :param user: optional user to be logged in
        :param in_group: optional group to have the user assigned to
        :param is_superuser: is the user a superuser?
        """
        if not user:
            user = UserFactory()
        login_successful = self.client.login(username=user.username, password=UserFactory.get_test_password())
        self.assertEqual(login_successful, True)
        if in_group:
            group = GroupFactory(name=in_group)
            user.groups.add(group)
        if is_superuser:
            user.is_superuser = True
            user.save()
        return user

    def assert_user_access_denied(self, test_url, user, locales=('en', 'fr'), expected_code=302,
                                  login_search_term=None):
        """
        this test will ensure that a specified user does not have access to a given url
       :param test_url: the url to test
       :param user: user to test access
       :param locales: the locales to test
       :param expected_code: the expected http response code; default would be a 302 since we are expecting redirection
       :param login_search_term: the search term to use when confirming a login redirect
       """
        self.client.logout()
        # perform this test for each locale
        for l in locales:
            activate(l)
            login_url = f"{self.login_url_base}{test_url}" if not login_search_term else login_search_term

            # login a user
            self.get_and_login_user(user=user)
            # get a response
            response = self.client.get(test_url)
            # we are expecting to see the login url
            self.assertEquals(expected_code, response.status_code)
            self.assertIn(f"{login_url}", response.url)
            self.client.logout()

    def assert_non_public_view(self, test_url, locales=('en', 'fr'), expected_template=None, user=None,
                               expected_code=200, login_search_term=None, bad_user_list=[]):
        """
        This test will ensure a view requires a user to be logged in in order to access it. Part 1, will test to see
        what happens when an anonymous user tries accessing the url. Part 2 attempt the same this with a logged in user.
        If the `user` arg is provided, it will be used for Part 2.
        :param test_url: the url to test
        :param locales: the locales to test
        :param expected_template: the expected template file
        :param expected_code: the expected http response code
        :param user: an optional user to use for the second part of this test
        :param login_search_term: the search term to use when confirming a login redirect
        :param bad_user_list: a list of users to check to make sure that they do not have access
        """

        # perform this test for each locale
        for l in locales:
            activate(l)
            login_url = f"{self.login_url_base}{test_url}" if not login_search_term else login_search_term

            # PART 1: try accessing with an Anonymous user

            # make sure there is no one already logged in
            self.client.logout()
            response = self.client.get(test_url)
            # with Anonymous User, a 302 response is expected
            self.assertEquals(302, response.status_code)
            # we are expecting to see the login url
            self.assertIn(f"{login_url}", response.url)

            # PART 2: try accessing with the bad users
            for u in bad_user_list:
                # make sure there is no one already logged in
                self.client.logout()
                self.get_and_login_user(user=u)
                response = self.client.get(test_url)
                # a 403 response would be expected here
                possibility_1 = 403 == response.status_code
                possibility_2 = 302 == response.status_code and "denied" in response.url
                self.assertTrue(possibility_1 or possibility_2)

            # PART 3: try with a logged in user. user the User provided in args, if available
            # login a random user if one was not provided by args
            self.get_and_login_user(user=user)

            # must get a new response, but don't know which.
            response = self.client.get(test_url)
            self.assertEquals(expected_code, response.status_code)
            # there is a problem here. If the expected response is a 302, it will be hard to differentiate between this
            # and the login redirect. So we will make sure that the redirect url (if present) does not contain the
            # `accounts/login ...`
            if hasattr(response, "url"):
                self.assertNotIn(f"{login_url}", response.url)

            # if an expected template was provided, test it against the template_name in the response
            if expected_template:
                self.assertIn(expected_template, response.template_name)
            self.client.logout()

    def assert_public_view(self, test_url, locales=('en', 'fr'), expected_template=None, expected_code=200,
                           login_search_term=None):
        """
        ensure a view is a public view, ie. it is accessible to an Anonymous user with a
        :param test_url: the url to test
        :param locales: the locales to test
        :param expected_template: the expected template file
        :param expected_code: the expected http response code
        :param login_search_term: the search term to use when confirming a login redirect
        """
        for l in locales:
            activate(l)
            login_url = f"{self.login_url_base}{test_url}" if not login_search_term else login_search_term

            response = self.client.get(test_url)
            self.assertEquals(expected_code, response.status_code)

            # there is a problem here. If the expected response is a 302, it will be hard to differentiate between this and the login
            # redirect. So we will make sure that the redirect url (if present) does not contain the `accounts/login ...`
            if hasattr(response, "url"):
                self.assertNotIn(f"{login_url}", response.url)

            # if an expected template was provided, test it against the template_name in the response
            if expected_template:
                self.assertIn(expected_template, response.template_name)
            self.client.logout()

    def assert_good_response(self, test_url, locales=('en', 'fr'), anonymous=True):
        """
        This will test check to see if the test url returns something bad like a 404 or a 500 response
        :param test_url: the url to test
        :param locales: the locales to test
        :param anonymous: should the test be run anonymously? default is True
        """
        if anonymous:
            self.client.logout()
        # perform this test for each locale
        for l in locales:
            # make sure we use an anonymous user
            activate(l)
            response = self.client.get(test_url)
            self.assertNotIn(response.status_code, [404, 500, ])

    def assert_inheritance(self, test_child_class, test_parent_class):
        """
        this will test to see if the child is a subclass of the parent.
        :param test_child_class:
        :param test_parent_class:
        """
        # perform this test for each locale
        self.assertTrue(issubclass(test_child_class, test_parent_class))

    def assert_field_in_field_list(self, test_url, name_of_field_list, fields_to_test, user=None):
        """
        this test looks for a field list in the context variable and checks to see if there is a specific field name in
        there
        :param test_url:
        :param name_of_field_list: the name of the field list (e.g. `field_list`)
        :param fields_to_test: list of fields to check for
        :param user: an optional user to use for producing the http response
        """
        activate('en')
        self.get_and_login_user(user=user)
        response = self.client.get(test_url)
        for field in fields_to_test:
            self.assertIn(field, response.context[name_of_field_list])

    def assert_field_not_in_field_list(self, test_url, name_of_field_list, fields_to_test, user=None):
        """
        this test looks for a field list in the context variable and checks to confirm a specific field name is not in there
        :param test_url:
        :param name_of_field_list: the name of the field list (e.g. `field_list`)
        :param fields_to_test: list of fields to check for
        :param user: an optional user to use for producing the http response
        """
        activate('en')
        self.get_and_login_user(user=user)
        response = self.client.get(test_url)
        for field in fields_to_test:
            self.assertNotIn(field, response.context[name_of_field_list])

    def assert_presence_of_context_vars(self, test_url, context_var_list, user=None):
        """
        this test looks to ensure that a specific context var is present in the template context variable
        :param test_url:
        :param context_var_list: a list of name of context var to search for
        :param user: an optional user to use for producing the http response
        """
        activate('en')
        reg_user = self.get_and_login_user(user=user)
        response = self.client.get(test_url)
        for context_var in context_var_list:
            self.assertIn(context_var, response.context)

    def assert_value_of_context_var(self, test_url, context_var, expected_value, user=None):
        """
        this test looks to ensure that a specific context var is present in the template context variable
        :param test_url:
        :param context_var: name of context var to search for
        :param expected_value: expected value of context var
        :param user: an optional user to use for producing the http response
        """
        activate('en')
        reg_user = self.get_and_login_user(user=user)
        response = self.client.get(test_url)

        self.assertIn(context_var, response.context)
        self.assertEqual(response.context.get(context_var), expected_value)

    def assert_correct_url(self, test_url_name, expected_url_path, test_url_args=None):
        # arbitrarily activate the english locale
        activate('en')
        my_path = reverse(test_url_name, args=test_url_args)
        self.assertEqual(my_path, f'{expected_url_path}')

    # Tests for API views
    #################
    def assert_dict_has_keys(self, my_dict, keys):
        # arbitrarily activate the english locale
        for key in keys:
            self.assertIn(key, my_dict)

    # Tests for forms (create, update, delete and form views)
    #################

    def assert_correct_form_class(self, test_view, expected_form_class):
        """
        check that the formview is using the correct form class
        :param test_view: the view to test
        :param expected_form_class: the expected form class
        """
        activate("en")
        self.assertEquals(test_view, expected_form_class)

    def assert_success_url(self, test_url, data=None, user=None, expected_url_name=None, expected_success_url=None,
                           use_anonymous_user=False, file_field_name=None):
        """
        test that upon a successful form the view redirects to the expected success url
        :param test_url: URL being tested
        :param data: optional data to use when submitting the form
        :param user: an optional user that can be used to generate the response
        :param expected_url_name: the name of the url to which a successful submission should be redirected
        :param expected_success_url: the url to which a successful submission should be redirected
        :param use_anonymous_user: should this function be run without logging in a uer? if so, set this optional arg
        to true
        :param file_field_name: For the occasion a file is created for a model this is the name of the column the file
        data will be stored in
        """
        # arbitrarily activate the english locale
        activate('en')

        # if a user is provided in the arg, log in with that user
        if not use_anonymous_user:
            self.get_and_login_user(user)

        if data and file_field_name:
            with open(os.path.join(settings.BASE_DIR, "static", "img", "inventory", "good to go.jpg"), mode='rb') as fp:
                data[file_field_name] = fp
                response = self.client.post(test_url, data=data, )
        else:
            response = self.client.post(test_url, data=data)

        if response.context and 'form' in response.context:
            # If the data in this test is invaild the response will be invalid
            self.assertTrue(response.context_data['form'].is_valid(),
                            msg=f"\n\nTest data was likely invalid. \n\nHere's the error log from the form:\n"
                                f" {html2text(str(response.context_data['form'].errors))}"
                                f"Here's the data from the form:\n{response.context_data['form'].data}")

        # should always result in a redirect response
        self.assertEquals(302, response.status_code)

        # if a url name was provided
        if expected_url_name:
            self.assertEquals(expected_url_name, resolve(response.url).view_name)

        if expected_success_url:
            self.assertRedirects(response=response, expected_url=expected_success_url)

    def assert_form_valid(self, form_class, data, instance=None, initial=None):
        """
        assert that upon submission a form is valid.
        :param Form: the form instance to test
        :param data: the data to use when testing the form
        :param instance: an instance of some model to use when testing the form. applicable to ModelForms only
        :param initial: initial kwargs to pass into the form upon initialization
        """
        if instance:
            form = form_class(data=data, instance=instance, initial=initial)
        else:
            form = form_class(data=data, initial=initial)
        self.assertTrue(form.is_valid(),
                        msg=f"\n\nTest data was likely invalid. \n\nHere's the error log from the form: \n{html2text(str(form.errors))}"
                            f"Here's the data from the form:\n{form.data}")

    def assert_form_invalid(self, form_class, data, instance=None, initial=None):
        """
        assert that upon submission a form is invalid.
        :param Form: the form instance to test
        :param data: the data to use when testing the form
        :param instance: an instance of some model to use when testing the form. applicable to ModelForms only
        """
        if instance:
            form = form_class(data, instance=instance, initial=initial)
        else:
            form = form_class(data, initial=initial)
        self.assertFalse(form.is_valid())

    def assert_field_in_form(self, Form, field_name, instance=None, initial=None):
        """
        assert that a form contains a specific field
        :param Form: the form instance to test
        :param field_name: the name of the field to check for
        :param instance: an instance of some model to use when testing the form. applicable to ModelForms only
        """

        if instance:
            form = Form(instance=instance, initial=initial)
        else:
            form = Form(initial=initial)
        self.assertIn(field_name, form.fields)

    def assert_field_not_in_form(self, Form, field_name, instance=None, initial=None):
        """
        assert that a form does not contains a specific field
        :param Form: the form instance to test
        :param field_name: the name of the field to check for
        :param instance: an instance of some model to use when testing the form. applicable to ModelForms only
        """
        if instance:
            form = Form(instance=instance, initial=initial)
        else:
            form = Form(initial=initial)
        self.assertNotIn(field_name, form.fields)

    # Tests for models
    ##################
    def assert_unique_fields(self, model, field_names):
        """
        assert that a field within a model is unique
        :param model: the model class to test
        :param field_names: list of  field names to check
        """
        for field_name in field_names:
            field = [field for field in model._meta.fields if field.name == field_name][0]
            self.assertTrue(field.unique)

    def assert_mandatory_fields(self, model, field_names):
        """
        assert that a field within a model is mandatory (blank=False, null=False)
        :param model: the model class to test
        :param field_names: list of  field names to check
        """
        for field_name in field_names:
            field = [field for field in model._meta.fields if field.name == field_name][0]
            self.assertFalse(field.blank)
            self.assertFalse(field.null)

    def assert_non_mandatory_fields(self, model, field_names):
        """
        assert that a field within a model is not mandatory (blank=True, null=True)
        :param model: the model class to test
        :param field_names: list of  field names to check
        """
        for field_name in field_names:
            field = [field for field in model._meta.fields if field.name == field_name][0]
            self.assertTrue(field.blank)
            self.assertTrue(field.null)

    def assert_has_fields(self, model, fields):
        """
        assert that a model has specified field names
        :param model: the model class to test
        :param fields: list of  field names to check
        """
        model_field_list = [field.name for field in model._meta.fields]
        for field in fields:
            self.assertIn(field, model_field_list)

    def assert_has_props(self, model, props):
        """
        assert that a model has specified props
        :param model: the model class to test
        :param props: list of  field names to check
        """
        for prop in props:
            self.assertTrue(hasattr(model, prop))
