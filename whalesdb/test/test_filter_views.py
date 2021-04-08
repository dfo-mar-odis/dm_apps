from django.test import tag, TestCase
from django.urls import reverse_lazy

from whalesdb.test.common_views import CommonListTest


# The Cruise views requires a Whales_admin level of permissions to access since cruises are used by other apps
@tag('cru', 'filter')
class TesCruList(CommonListTest, TestCase):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_cru')
        self.login_required = True

    # make sure project list context returns expected context objects
    # The cruise view should use create_cru and details_cru for the create and details buttons
    def test_cru_list_context_fields(self):
        response = super().get_context()

        self.assertEqual("whalesdb:create_cru", response.context['create_url'])
        self.assertEqual("whalesdb:details_cru", response.context['details_url'])
        self.assertEqual("whalesdb:update_cru", response.context['update_url'])


@tag('dep', 'filter')
class TestDepList(CommonListTest, TestCase):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_dep')

    # make sure project list context returns expected context objects
    # The deployment view should use create_dep and details_dep for the create and details buttons
    def test_dep_list_context_fields(self):
        response = super().get_context()

        self.assertEqual("whalesdb:create_dep", response.context['create_url'])
        self.assertEqual("whalesdb:details_dep", response.context['details_url'])
        self.assertEqual("whalesdb:update_dep", response.context['update_url'])
        self.assertEqual("whalesdb:delete_dep", response.context['delete_url'])


@tag('eca', 'filter')
class TestEcaList(CommonListTest, TestCase):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_eca')

    def test_eca_list_context_fields(self):
        response = super().get_context()

        self.assertEqual("whalesdb:create_eca", response.context['create_url'])
        self.assertEqual("whalesdb:details_eca", response.context['details_url'])
        self.assertEqual("whalesdb:update_eca", response.context['update_url'])


@tag('emm', 'filter')
class TestEmmList(CommonListTest, TestCase):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_emm')


@tag('eqp', 'filter')
class TestEqpList(CommonListTest, TestCase):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_eqp')


@tag('etr', 'filter')
class TestEtrList(CommonListTest, TestCase):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_etr')


@tag('mor', 'filter')
class TestMorList(CommonListTest, TestCase):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_mor')

    # make sure project list context returns expected context objects
    # The mooring view should use create_mor and details_mor for the create and details buttons
    def test_mor_list_context_fields(self):
        response = super().get_context()

        self.assertEqual("whalesdb:create_mor", response.context['create_url'])
        self.assertEqual("whalesdb:details_mor", response.context['details_url'])
        self.assertEqual("whalesdb:update_mor", response.context['update_url'])


@tag('prj', 'filter')
class TestPrjList(CommonListTest, TestCase):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_prj')

    # make sure project list context returns expected context objects
    # The project view should use create_mor and details_prj for the create and details buttons
    def test_prj_list_context_fields(self):
        response = super().get_context()

        self.assertEqual("whalesdb:create_prj", response.context['create_url'])
        self.assertEqual("whalesdb:details_prj", response.context['details_url'])
        self.assertEqual("whalesdb:update_prj", response.context['update_url'])


@tag('rec', 'filter')
class TestRecList(CommonListTest, TestCase):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_rec')

    def test_rec_list_context_fields(self):
        response = super().get_context()

        self.assertEqual("whalesdb:create_rec", response.context['create_url'])


@tag('ret', 'filter')
class TestRetList(CommonListTest, TestCase):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_ret')

    def test_ret_list_context_fields(self):
        response = super().get_context()

        self.assertFalse(response.context['details_url'])


@tag('rsc', 'filter')
class TestRscList(CommonListTest, TestCase):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_rsc')

    def test_rsc_list_context_fields(self):
        response = super().get_context()

        self.assertEqual("whalesdb:create_rsc", response.context['create_url'])
        self.assertEqual("whalesdb:details_rsc", response.context['details_url'])

        self.assertEquals(True, response.context["editable"])


@tag('stn', 'filter')
class TestStnList(CommonListTest, TestCase):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_stn')

    # make sure project list context returns expected context objects
    # The station view should use create_stn and details_stn for the create and details buttons
    def test_stn_list_context_fields(self):
        response = super().get_context()

        self.assertEqual("whalesdb:create_stn", response.context['create_url'])
        self.assertEqual("whalesdb:details_stn", response.context['details_url'])
        self.assertEqual("whalesdb:update_stn", response.context['update_url'])


@tag('tea', 'filter')
class TestTeaList(CommonListTest, TestCase):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_tea')

    # make sure project list context returns expected context objects
    # The station view should use create_tea and details_tea for the create and details buttons
    def test_tea_list_context_fields(self):
        response = super().get_context()

        self.assertEqual("whalesdb:create_tea", response.context['create_url'])
