from django.test import tag
from django.urls import reverse_lazy

from django.core.files.base import ContentFile
from django.utils.six import BytesIO

from PIL import Image

from whalesdb.test.common_views import CommonCreateTest

from whalesdb import views, forms, models

import os
from whalesdb.test import WhalesdbFactoryFloor as Factory


class TestDepCreate(CommonCreateTest):

    def setUp(self):
        super().setUp()
        self.data = Factory.DepFactory.get_valid_data()
        self.test_url = reverse_lazy('whalesdb:create_dep')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_success_url = reverse_lazy('whalesdb:list_dep')

        self.expected_view = views.DepCreate
        self.expected_form = forms.DepForm

    # Users must be logged in to create new objects
    @tag('dep', 'create', 'response', 'access')
    def test_create_dep_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to create new objects
    @tag('dep', 'create', 'response', 'access')
    def test_create_dep_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('dep', 'create', 'response', 'access')
    def test_create_dep_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('dep', 'create', 'form')
    def test_create_dep_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('dep', 'create', 'context')
    def test_create_dep_context_fields(self):
        response = super().assert_create_view_context_fields()

        # Deploymnets also need to return a JSON formatted list of Station Codes
        self.assertIn("station_json", response.context)
        self.assertIn("java_script", response.context)
        self.assertEquals("whalesdb/_entry_dep_js.html", response.context['java_script'])

    # test that given some valid data the view will redirect to the list
    @tag('dep', 'create', 'redirect')
    def test_create_dep_successful_url(self):
        super().assert_successful_url()


class TestEdaCreate(CommonCreateTest):

    def setUp(self):
        super().setUp()

        self.data = Factory.EdaFactory.get_valid_data()

        # ['deployment id', 'Equipment_id', 'set_to_popup']
        args = [self.data['dep'], 'pop']

        self.test_url = reverse_lazy('whalesdb:create_eda', args=args)

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_success_url = reverse_lazy('shared_models:close_me_no_refresh')

        self.expected_view = views.EdaCreate
        self.expected_form = forms.EdaForm

    # Users must be logged in to create new objects
    @tag('eda', 'create', 'response', 'access')
    def test_create_eda_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to create new objects
    @tag('eda', 'create', 'response', 'access')
    def test_create_eda_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('eda', 'create', 'response', 'access')
    def test_create_eda_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('eda', 'create', 'form')
    def test_create_eda_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('eda', 'create', 'context')
    def test_create_eda_context_fields(self):
        response = super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('eda', 'create', 'redirect')
    def test_create_eda_successful_url(self):
        super().assert_successful_url()


class TestEmmCreate(CommonCreateTest):

    emm_id = 1

    def setUp(self):
        super().setUp()

        # test for eqt_id = 3 - 'otn recorder' which doesn't have special pages for the success field
        self.data = Factory.EmmFactory.get_valid_data(3)

        # Hydrophone properties requires a make and model emm_id
        self.test_url = reverse_lazy('whalesdb:create_emm')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_success_url = reverse_lazy('whalesdb:list_emm')

        self.expected_view = views.EmmCreate
        self.expected_form = forms.EmmForm

    # Users must be logged in to create new objects
    @tag('emm', 'create', 'response', 'access')
    def test_create_emm_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to create new objects
    @tag('emm', 'create', 'response', 'access')
    def test_create_emm_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('emm', 'create', 'response', 'access')
    def test_create_emm_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('emm', 'create', 'form')
    def test_create_emm_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('emm', 'create', 'context')
    def test_create_emm_context_fields(self):
        response = super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('emm', 'create', 'redirect')
    def test_create_emm_successful_url(self):
        super().assert_successful_url()

    # If the created emm object is a Hydrophone type user should be sent to the details page to add
    # hydrophone details
    @tag('emm', 'create', 'redirect', 'eqh')
    def test_create_emm_hydrophone_successful_url(self):
        data = Factory.EmmFactory.get_valid_data(4)

        self.login_whale_user()
        response = self.client.post(self.test_url, data)

        # should only be one EMM object in the db
        emm_id = models.EmmMakeModel.objects.all()[0].pk
        self.assertRedirects(response=response, expected_url=reverse_lazy('whalesdb:details_emm', args=(emm_id,)))


class TestEqhCreate(CommonCreateTest):

    emm_id = 1

    def setUp(self):
        super().setUp()

        self.data = Factory.EqhFactory.get_valid_data()

        # Hydrophone properties requires a make and model emm_id
        self.test_url = reverse_lazy('whalesdb:create_eqh', args=(self.emm_id, 'pop',))

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_success_url = reverse_lazy('shared_models:close_me_no_refresh')

        self.expected_view = views.EqhCreate
        self.expected_form = forms.EqhForm

    # Users must be logged in to create new objects
    @tag('eqh', 'create', 'response', 'access')
    def test_create_eqh_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to create new objects
    @tag('eqh', 'create', 'response', 'access')
    def test_create_eqh_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('eqh', 'create', 'response', 'access')
    def test_create_eqh_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('eqh', 'create', 'form')
    def test_create_eqh_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('eqh', 'create', 'context')
    def test_create_eqh_context_fields(self):
        response = super().assert_create_view_context_fields()

        self.assertIn("form", response.context)
        self.assertIn("emm", response.context['form'].initial)
        self.assertEquals(self.emm_id, response.context['form'].initial['emm'])

    # test that given some valid data the view will redirect to the list
    @tag('eqh', 'create', 'redirect')
    def test_create_eqh_successful_url(self):
        super().assert_successful_url()


class TestEqpCreate(CommonCreateTest):

    def setUp(self):
        super().setUp()

        self.data = Factory.EqpFactory.get_valid_data()

        self.test_url = reverse_lazy('whalesdb:create_eqp')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_success_url = reverse_lazy('whalesdb:list_eqp')

        self.expected_view = views.EqpCreate
        self.expected_form = forms.EqpForm

    # Users must be logged in to create new objects
    @tag('eqp', 'create', 'response', 'access')
    def test_create_eqp_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to create new objects
    @tag('eqp', 'create', 'response', 'access')
    def test_create_eqp_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('eqp', 'create', 'response', 'access')
    def test_create_eqp_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('eqp', 'create', 'form')
    def test_create_eqp_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('eqp', 'create', 'context')
    def test_create_eqp_context_fields(self):
        response = super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('eqp', 'create', 'redirect')
    def test_create_eqp_successful_url(self):
        super().assert_successful_url()


class TestEqrCreate(CommonCreateTest):

    emm_id = 1

    def setUp(self):
        super().setUp()

        self.data = Factory.EqrFactory.get_valid_data()

        # Hydrophone properties requires a make and model emm_id
        self.test_url = reverse_lazy('whalesdb:create_eqr', args=(self.emm_id, 'pop',))

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_success_url = reverse_lazy('shared_models:close_me_no_refresh')

        self.expected_view = views.EqrCreate
        self.expected_form = forms.EqrForm

    # Users must be logged in to create new objects
    @tag('eqr', 'create', 'response', 'access')
    def test_create_eqr_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to create new objects
    @tag('eqr', 'create', 'response', 'access')
    def test_create_eqr_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('eqr', 'create', 'response', 'access')
    def test_create_eqr_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('eqr', 'create', 'form')
    def test_create_eqr_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('eqr', 'create', 'context')
    def test_create_eqr_context_fields(self):
        response = super().assert_create_view_context_fields()

        self.assertIn("form", response.context)
        self.assertIn("emm", response.context['form'].initial)
        self.assertEquals(self.emm_id, response.context['form'].initial['emm'])

    # test that given some valid data the view will redirect to the list
    @tag('eqr', 'create', 'redirect')
    def test_create_eqr_successful_url(self):
        super().assert_successful_url()


class TestMorCreate(CommonCreateTest):
    img_file_name = None
    img_file_path = None

    def setUp(self):
        super().setUp()

        self.data = Factory.MorFactory.get_valid_data()
        self.test_url = reverse_lazy('whalesdb:create_mor')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_success_url = reverse_lazy('whalesdb:list_mor')

        self.expected_view = views.MorCreate
        self.expected_form = forms.MorForm

        self.img_file_name = "MooringSetupTest.png"
        self.img_file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + \
                             self.img_file_name

        data = BytesIO()
        Image.open(self.img_file_path).save(data, "PNG")
        data.seek(0)

        file = ContentFile(data.read(), self.img_file_name)
        # add the image to the data array
        self.data['mor_setup_image'] = self.img_file_path

    def tearDown(self):
        mors = models.MorMooringSetup.objects.all()
        for mor in mors:
            mor.delete()

    # Users must be logged in to create new objects
    @tag('mor', 'create', 'response', 'access')
    def test_create_mor_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to create new objects
    @tag('mor', 'create', 'response', 'access')
    def test_create_mor_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('mor', 'create', 'response', 'access')
    def test_create_mor_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('mor', 'create', 'form')
    def test_create_mor_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('mor', 'create', 'context')
    def test_create_mor_context_fields(self):
        super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('mor', 'create', 'redirect')
    def test_create_mor_successful_url(self):
        super().assert_successful_url()


class TestPrjCreate(CommonCreateTest):

    def setUp(self):
        super().setUp()

        self.data = Factory.PrjFactory.get_valid_data()
        self.test_url = reverse_lazy('whalesdb:create_prj')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_success_url = reverse_lazy('whalesdb:list_prj')

        self.expected_view = views.PrjCreate

        self.expected_form = forms.PrjForm

    # Users must be logged in to create new objects
    @tag('prj', 'create', 'response', 'access')
    def test_create_prj_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to create new objects
    @tag('prj', 'create', 'response', 'access')
    def test_create_prj_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('prj', 'create', 'response', 'access')
    def test_create_prj_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('prj', 'create', 'form')
    def test_create_prj_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('prj', 'create', 'context')
    def test_create_prj_context_fields(self):
        super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('prj', 'create', 'redirect')
    def test_create_prj_successful_url(self):
        super().assert_successful_url()


class TestRciCreate(CommonCreateTest):

    def setUp(self):
        super().setUp()

        self.data = Factory.RciFactory.get_valid_data()

        args = [self.data['rec_id'], 'pop']
        # the STE entry from should only be accessed via popup arguments are dep (deployment),
        # set(Station Event Type) and 'pop' for popup
        self.test_url = reverse_lazy('whalesdb:create_rci', args=args)

        # because STE entry is a popup it should use the close_me_no_refresh
        self.expected_success_url = reverse_lazy('shared_models:close_me_no_refresh')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.RciCreate

        self.expected_form = forms.RciForm

    # Users must be logged in to create new stations
    @tag('rci', 'create', 'response', 'access')
    def test_create_rci_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to create new stations
    @tag('rci', 'create', 'response', 'access')
    def test_create_rci_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('rci', 'create', 'response', 'access')
    def test_create_rci_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('rci', 'create', 'form')
    def test_create_rci_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('rci', 'create', 'context')
    def test_create_rci_context_fields(self):
        super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('rci', 'create', 'redirect')
    def test_create_rci_successful_url(self):
        super().assert_successful_url()


class TestRecCreate(CommonCreateTest):

    def setUp(self):
        super().setUp()

        self.data = Factory.RecFactory.get_valid_data()
        self.test_url = reverse_lazy('whalesdb:create_rec')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.RecCreate

        self.expected_form = forms.RecForm

        self.expected_success_url = reverse_lazy('whalesdb:list_rec')

    # Users must be logged in to create new stations
    @tag('rec', 'create', 'response', 'access')
    def test_create_rec_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to create new stations
    @tag('rec', 'create', 'response', 'access')
    def test_create_rec_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('rec', 'create', 'response', 'access')
    def test_create_rec_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('rec', 'create', 'form')
    def test_create_rec_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('rec', 'create', 'context')
    def test_create_rec_context_fields(self):
        response = super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('rec', 'create', 'redirect')
    def test_create_prj_successful_url(self):
        super().assert_successful_url()


class TestRscCreate(CommonCreateTest):

    def setUp(self):
        super().setUp()

        self.data = Factory.RscFactory.get_valid_data()
        self.test_url = reverse_lazy('whalesdb:create_rsc')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.RscCreate

        self.expected_form = forms.RscForm

        self.expected_success_url = "whalesdb:details_rsc"

    # Users must be logged in to create new stations
    @tag('rsc', 'create', 'response', 'access')
    def test_create_rsc_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to create new stations
    @tag('rsc', 'create', 'response', 'access')
    def test_create_rsc_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('rsc', 'create', 'response', 'access')
    def test_create_rsc_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('rsc', 'create', 'form')
    def test_create_rsc_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('rsc', 'create', 'context')
    def test_create_rsc_context_fields(self):
        response = super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('rsc', 'create', 'redirect')
    def test_create_rsc_successful_url(self):
        super().assert_successful_url(signature="whalesdb:details_rsc")


class TestRstCreate(CommonCreateTest):

    rsc_id = 1

    def setUp(self):
        super().setUp()

        self.data = Factory.RstFactory.get_valid_data()
        self.test_url = reverse_lazy('whalesdb:create_rst', args=[self.rsc_id, 'pop'])

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.RstCreate

        self.expected_form = forms.RstForm

        self.expected_success_url = reverse_lazy("shared_models:close_me_no_refresh")

    # Users must be logged in to create new stations
    @tag('rst', 'create', 'response', 'access')
    def test_create_rst_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to create new stations
    @tag('rst', 'create', 'response', 'access')
    def test_create_rst_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('rst', 'create', 'response', 'access')
    def test_create_rst_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('rst', 'create', 'form')
    def test_create_rst_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('rst', 'create', 'context')
    def test_create_rst_context_fields(self):
        response = super().assert_create_view_context_fields()

        self.assertIn("form", response.context)
        self.assertIn("rsc", response.context['form'].initial)
        self.assertEquals(self.rsc_id, response.context['form'].initial['rsc'])

    # test that given some valid data the view will redirect to the list
    @tag('rst', 'create', 'redirect')
    def test_create_rst_successful_url(self):
        super().assert_successful_url()


class TestRttCreate(CommonCreateTest):

    rtt_id = 1

    def setUp(self):
        super().setUp()

        self.data = Factory.RttFactory.get_valid_data()
        self.test_url = reverse_lazy('whalesdb:create_rtt')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.RstCreate

        self.expected_form = forms.RstForm

        self.expected_success_url = reverse_lazy("shared_models:close_me_no_refresh")

    # Users must be logged in to create new stations
    @tag('rtt', 'create', 'response', 'access')
    def test_create_rtt_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to create new stations
    @tag('rtt', 'create', 'response', 'access')
    def test_create_rtt_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('rtt', 'create', 'response', 'access')
    def test_create_rtt_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()


class TestSteCreate(CommonCreateTest):

    def setUp(self):
        super().setUp()

        self.data = Factory.SteFactory.get_valid_data()

        args = [self.data['dep'], 1, 'pop']
        # the STE entry from should only be accessed via popup arguments are dep (deployment),
        # set(Station Event Type) and 'pop' for popup
        self.test_url = reverse_lazy('whalesdb:create_ste', args=args)

        # because STE entry is a popup it should use the close_me_no_refresh
        self.expected_success_url = reverse_lazy('shared_models:close_me_no_refresh')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.SteCreate

        self.expected_form = forms.SteForm

    # Users must be logged in to create new stations
    @tag('ste', 'create', 'response', 'access')
    def test_create_ste_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to create new stations
    @tag('ste', 'create', 'response', 'access')
    def test_create_ste_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('ste', 'create', 'response', 'access')
    def test_create_ste_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('ste', 'create', 'form')
    def test_create_ste_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('ste', 'create', 'context')
    def test_create_ste_context_fields(self):
        super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('ste', 'create', 'redirect')
    def test_create_ste_successful_url(self):
        super().assert_successful_url()


class TestStnCreate(CommonCreateTest):

    def setUp(self):
        super().setUp()

        self.data = Factory.StnFactory.get_valid_data()
        self.test_url = reverse_lazy('whalesdb:create_stn')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.StnCreate

        self.expected_form = forms.StnForm

        self.expected_success_url = reverse_lazy('whalesdb:list_stn')

    # Users must be logged in to create new stations
    @tag('stn', 'create', 'response', 'access')
    def test_create_stn_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to create new stations
    @tag('stn', 'create', 'response', 'access')
    def test_create_stn_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('stn', 'create', 'response', 'access')
    def test_create_stn_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('stn', 'create', 'form')
    def test_create_stn_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('stn', 'create', 'context')
    def test_create_stn_context_fields(self):
        response = super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('stn', 'create', 'redirect')
    def test_create_stn_successful_url(self):
        super().assert_successful_url()


class TestTeaCreate(CommonCreateTest):

    def setUp(self):
        super().setUp()

        self.data = Factory.TeaFactory.get_valid_data()
        self.test_url = reverse_lazy('whalesdb:create_tea')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.TeaCreate

        self.expected_form = forms.TeaForm

        self.expected_success_url = reverse_lazy('whalesdb:list_tea')

    # Users must be logged in to create new stations
    @tag('tea', 'create', 'response', 'access')
    def test_create_tea_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to create new stations
    @tag('tea', 'create', 'response', 'access')
    def test_create_tea_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the shared_entry_form.html template
    @tag('tea', 'create', 'response', 'access')
    def test_create_tea_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('tea', 'create', 'form')
    def test_create_tea_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('tea', 'create', 'context')
    def test_create_tea_context_fields(self):
        response = super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('tea', 'create', 'redirect')
    def test_create_tea_successful_url(self):
        super().assert_successful_url()
