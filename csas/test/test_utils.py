from django.test import TestCase, RequestFactory, tag
from django.contrib import auth
from django.contrib.auth.models import AnonymousUser, User, Group
from django.urls import reverse

from csas import utils


class UtilityTests(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()

    # anonymous user should not be authorized
    @tag('util', 'auth')
    def test_auth_anon_denied(self):
        authorized = utils.csas_authorized(AnonymousUser())

        self.assertFalse(authorized)

    # user not in csas_admin should not be authorized
    @tag('util', 'auth')
    def test_auth_regular_denied(self):
        user = User.objects.create_user(username='Patrick', email="Patrick@dfo-mpo.gc.ca", password="secret")

        authorized = utils.csas_authorized(user)

        self.assertFalse(authorized)

    # user in csas_admin or the csas_user group they should be authorized
    @tag('util', 'auth')
    def test_auth_csas_user_granted(self):
        user = User.objects.create_user(username='Patrick', email="Patrick@dfo-mpo.gc.ca", password="secret")

        csas_group = Group(name="csas_users")
        csas_group.save()

        user.groups.add(csas_group)

        authorized = utils.csas_authorized(user)

        self.assertTrue(authorized)

    # user in csas_admin or the csas_user group they should be authorized
    @tag('util', 'auth')
    def test_auth_csas_admin_granted(self):
        user = User.objects.create_user(username='Patrick', email="Patrick@dfo-mpo.gc.ca", password="secret")

        csas_group = Group(name="csas_admin")
        csas_group.save()

        user.groups.add(csas_group)

        authorized = utils.csas_admin(user)

        self.assertTrue(authorized)

    # user in csas_super, giving them permissions to modify lookup tables
    @tag('util', 'auth')
    def test_auth_csas_admin_granted(self):
        user = User.objects.create_user(username='Patrick', email="Patrick@dfo-mpo.gc.ca", password="secret")

        csas_group = Group(name="csas_super")
        csas_group.save()

        user.groups.add(csas_group)

        authorized = utils.csas_super(user)

        self.assertTrue(authorized)