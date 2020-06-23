from django.test import tag, RequestFactory
from django.urls import reverse_lazy

from whalesdb.test.common_views import CommonUpdateTest, setup_view
from whalesdb.test import WhalesdbFactoryFloor as Factory

from whalesdb import views, forms, models


class TestDepUpdate(CommonUpdateTest):

    def setUp(self):
        super().setUp()

        self.data = Factory.DepFactory.get_valid_data()

        obj = Factory.DepFactory()

        self.test_url = reverse_lazy('whalesdb:update_dep', args=(obj.pk,))

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.DepUpdate

        self.expected_form = forms.DepForm

        self.expected_success_url = reverse_lazy("whalesdb:list_dep")

    # Users must be logged in to update object
    @tag('dep', 'update_dep', 'response', 'access')
    def test_update_dep_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to update object
    @tag('dep', 'update_dep', 'response', 'access')
    def test_update_dep_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('dep', 'update_dep', 'response', 'access')
    def test_update_dep_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('dep', 'update_dep', 'form')
    def test_update_dep_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('dep', 'update_dep', 'context')
    def test_update_dep_context_fields(self):
        response = super().assert_create_view_context_fields()

        # Deploymnets also need to return a JSON formatted list of Station Codes
        self.assertIn("station_json", response.context)
        self.assertIn("java_script", response.context)
        self.assertEquals("whalesdb/_entry_dep_js.html", response.context['java_script'])

    # test that given some valid data the view will redirect to the list
    @tag('dep', 'update_dep', 'redirect')
    def test_update_dep_successful_url(self):
        super().assert_successful_url()

    # If a deployment event has been issued, a deployment should no longer be editable and the
    # test_func method should return false. This is to prevent URL hijacking and letting a user
    # paste in data to a url to update a view
    @tag('dep', 'update_dep', 'access')
    def test_update_dep_test_func_denied(self):
        dep = Factory.DepFactory()

        # have to create the request and setup the view
        req_factory = RequestFactory()
        request = req_factory.get(reverse_lazy("whalesdb:update_dep", kwargs={'pk': dep.pk, 'pop': 'pop'}))
        request.user = self.login_whale_user()
        view = setup_view(views.DepUpdate(), request, pk=dep.pk)

        # check to see if a deployment that's not been deployed can be edited
        self.assertTrue(view.test_func())

        # create a deployment event
        set_type = models.SetStationEventCode.objects.get(pk=1)  # 1 == Deployment event
        dep_evt = Factory.SteFactory(dep=dep, set_type=set_type)

        # deployment should no longer be editable
        self.assertFalse(view.test_func())


class TestEmmUpdate(CommonUpdateTest):

    def setUp(self):
        super().setUp()

        self.data = Factory.EmmFactory.get_valid_data()

        obj = Factory.EmmFactory()

        self.test_url = reverse_lazy('whalesdb:update_emm', args=(obj.pk,))

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.EmmUpdate

        self.expected_form = forms.EmmForm

        self.expected_success_url = reverse_lazy("whalesdb:list_emm")

    # Users must be logged in to update object
    @tag('emm', 'update_emm', 'response', 'access')
    def test_update_emm_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to update object
    @tag('emm', 'update_emm', 'response', 'access')
    def test_update_emm_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('emm', 'update_emm', 'response', 'access')
    def test_update_emm_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('emm', 'update_emm', 'form')
    def test_update_emm_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('emm', 'update_emm', 'context')
    def test_update_emm_context_fields(self):
        response = super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('emm', 'update_emm', 'redirect')
    def test_update_emm_successful_url(self):
        super().assert_successful_url()


class TestEqhUpdate(CommonUpdateTest):

    def setUp(self):
        super().setUp()

        self.data = Factory.EqhFactory.get_valid_data()

        emm = Factory.EmmFactory(pk=4)
        obj = Factory.EqhFactory(emm=emm)

        self.test_url = reverse_lazy('whalesdb:update_eqh', args=(obj.pk, 'pop',))

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.EqhUpdate

        self.expected_form = forms.EqhForm


    # Users must be logged in to update object
    @tag('eqh', 'update_eqh', 'response', 'access')
    def test_update_eqh_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to update object
    @tag('eqh', 'update_eqh', 'response', 'access')
    def test_update_eqh_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('eqh', 'update_eqh', 'response', 'access')
    def test_update_eqh_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('eqh', 'update_eqh', 'form')
    def test_update_eqh_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('eqh', 'update_eqh', 'context')
    def test_update_eqh_context_fields(self):
        response = super().assert_create_view_context_fields()

        # Emm field should NOT be in the update dialog
        self.assertNotIn("emm", response.context)

    # test that given some valid data the view will redirect to the list
    @tag('eqh', 'update_eqh', 'redirect')
    def test_update_eqh_successful_url(self):
        super().assert_successful_url()


class TestEqpUpdate(CommonUpdateTest):

    def setUp(self):
        super().setUp()

        self.data = Factory.EqpFactory.get_valid_data()

        emm = Factory.EmmFactory()
        obj = Factory.EqpFactory(emm=emm)

        self.test_url = reverse_lazy('whalesdb:update_eqp', args=(obj.pk, 'pop',))

        # Since this is intended to be used as a pop-out form, use the no nav entry form
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.EqpUpdate

        self.expected_form = forms.EqpForm

        self.expected_success_url = reverse_lazy("whalesdb:list_eqp")

    # Users must be logged in to update object
    @tag('eqp', 'update_eqp', 'response', 'access')
    def test_update_eqp_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to update object
    @tag('eqp', 'update_eqp', 'response', 'access')
    def test_update_eqp_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('eqp', 'update_eqp', 'response', 'access')
    def test_update_eqp_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('eqp', 'update_eqp', 'form')
    def test_update_eqp_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('eqp', 'update_eqp', 'context')
    def test_update_eqp_context_fields(self):
        response = super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('eqp', 'update_eqp', 'redirect')
    def test_update_eqp_successful_url(self):
        super().assert_successful_url()


class TestEqrUpdate(CommonUpdateTest):

    def setUp(self):
        super().setUp()

        self.data = Factory.EqrFactory.get_valid_data()

        obj = Factory.EqrFactory()

        self.test_url = reverse_lazy('whalesdb:update_eqr', args=(obj.pk, 'pop',))

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.EqrUpdate

        self.expected_form = forms.EqrForm


    # Users must be logged in to update object
    @tag('eqr', 'update_eqr', 'response', 'access')
    def test_update_eqr_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to update object
    @tag('eqr', 'update_eqr', 'response', 'access')
    def test_update_eqr_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('eqr', 'update_eqr', 'response', 'access')
    def test_update_eqr_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('eqr', 'update_eqr', 'form')
    def test_update_eqr_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('eqr', 'update_eqr', 'context')
    def test_update_eqr_context_fields(self):
        response = super().assert_create_view_context_fields()

        # Emm field should NOT be in the update dialog
        self.assertNotIn("emm", response.context)

    # test that given some valid data the view will redirect to the list
    @tag('eqr', 'update_eqr', 'redirect')
    def test_update_eqr_successful_url(self):
        super().assert_successful_url()


class TestMorUpdate(CommonUpdateTest):

    def setUp(self):
        super().setUp()

        self.data = Factory.MorFactory.get_valid_data()

        obj = Factory.MorFactory()

        self.test_url = reverse_lazy('whalesdb:update_mor', args=(obj.pk,))

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.MorUpdate

        self.expected_form = forms.MorForm

        self.expected_success_url = reverse_lazy("whalesdb:list_mor")

    # Users must be logged in to update object
    @tag('mor', 'update_mor', 'response', 'access')
    def test_update_mor_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to update object
    @tag('mor', 'update_mor', 'response', 'access')
    def test_update_mor_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('mor', 'update_mor', 'response', 'access')
    def test_update_mor_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('mor', 'update_mor', 'form')
    def test_update_mor_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('mor', 'update_mor', 'context')
    def test_update_mor_context_fields(self):
        super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('mor', 'update_mor', 'redirect')
    def test_update_mor_successful_url(self):
        super().assert_successful_url()


class TestPrjUpdate(CommonUpdateTest):

    def setUp(self):
        super().setUp()

        self.data = Factory.PrjFactory.get_valid_data()

        obj = Factory.PrjFactory()

        self.test_url = reverse_lazy('whalesdb:update_prj', args=(obj.pk,))

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.PrjUpdate

        self.expected_form = forms.PrjForm

        self.expected_success_url = reverse_lazy("whalesdb:list_prj")

    # Users must be logged in to create new stations
    @tag('prj', 'update_prj', 'response', 'access')
    def test_update_prj_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to update object
    @tag('prj', 'update_prj', 'response', 'access')
    def test_update_prj_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('prj', 'update_prj', 'response', 'access')
    def test_update_prj_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('prj', 'update_prj', 'form')
    def test_update_prj_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('prj', 'update_prj', 'context')
    def test_update_prj_context_fields(self):
        super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('prj', 'update_prj', 'redirect')
    def test_update_prj_successful_url(self):
        super().assert_successful_url()


class TestStnUpdate(CommonUpdateTest):

    def setUp(self):
        super().setUp()

        self.data = Factory.StnFactory.get_valid_data()

        obj = Factory.StnFactory()

        self.test_url = reverse_lazy('whalesdb:update_stn', args=(obj.pk,))

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.StnUpdate

        self.expected_form = forms.StnForm
        
        self.expected_success_url = reverse_lazy("whalesdb:list_stn")

    # Users must be logged in to create new stations
    @tag('stn', 'update_stn', 'response', 'access')
    def test_update_stn_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to update object
    @tag('stn', 'update_stn', 'response', 'access')
    def test_update_stn_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('stn', 'update_stn', 'response', 'access')
    def test_update_stn_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('stn', 'update_stn', 'form')
    def test_update_stn_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('stn', 'update_stn', 'context')
    def test_update_stn_context_fields(self):
        response = super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('stn', 'update_stn', 'redirect')
    def test_update_stn_successful_url(self):
        super().assert_successful_url()


class TestRecUpdate(CommonUpdateTest):

    def setUp(self):
        super().setUp()

        self.data = Factory.RecFactory.get_valid_data()

        obj = Factory.RecFactory()

        self.test_url = reverse_lazy('whalesdb:update_rec', args=(obj.pk,))

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.RecUpdate

        self.expected_form = forms.RecForm

        self.expected_success_url = reverse_lazy("whalesdb:details_rec", args=(obj.pk,))

    # Users must be logged in to create new stations
    @tag('rec', 'update_rec', 'response', 'access')
    def test_update_rec_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to update object
    @tag('rec', 'update_rec', 'response', 'access')
    def test_update_rec_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('rec', 'update_rec', 'response', 'access')
    def test_update_rec_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('rec', 'update_rec', 'form')
    def test_update_rec_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('rec', 'update_rec', 'context')
    def test_update_rec_context_fields(self):
        super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('rec', 'update_rec', 'redirect')
    def test_update_rec_successful_url(self):
        super().assert_successful_url()
