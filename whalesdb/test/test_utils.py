from django.test import TestCase, RequestFactory, tag
from django.contrib import auth
from django.contrib.auth.models import AnonymousUser, User, Group
from django.urls import reverse

from whalesdb import utils


class UtilityTests(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()

    # anonymous user should not be authorized
    @tag('util', 'auth')
    def test_auth_anon_denied(self):
        authorized = utils.whales_authorized(AnonymousUser())

        self.assertFalse(authorized)

    # user not in whalesdb_admin should not be authorized
    @tag('util', 'auth')
    def test_auth_regular_denied(self):
        user = User.objects.create_user(username='Patrick', email="Patrick@dfo-mpo.gc.ca", password="secret")

        authorized = utils.whales_authorized(user)

        self.assertFalse(authorized)

    # user in whalesdb_admin should be authorized
    @tag('util', 'auth')
    def test_auth_whaleadmin_granted(self):
        user = User.objects.create_user(username='Patrick', email="Patrick@dfo-mpo.gc.ca", password="secret")

        whale_group = Group(name="whalesdb_admin")
        whale_group.save()

        user.groups.add(whale_group)

        authorized = utils.whales_authorized(user)

        self.assertTrue(authorized)
