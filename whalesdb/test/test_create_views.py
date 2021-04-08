from django.test import tag
from django.urls import reverse_lazy

from django.core.files.base import ContentFile
from six import BytesIO
from django.utils.translation import activate

from django.test import TestCase

from PIL import Image

from whalesdb.test.common_views import CommonCreateTest

from whalesdb import views, forms, models

import os
from whalesdb.test import WhalesdbFactoryFloor as Factory
from shared_models.test import SharedModelsFactoryFloor as SharedFactory


@tag('cru', 'create')
class TestCruCreate(CommonCreateTest, TestCase):

    def setUp(self):
        super().setUp()
        self.data = SharedFactory.CruiseFactory.get_valid_data()
        self.test_url = reverse_lazy('whalesdb:create_cru')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_success_url = reverse_lazy('whalesdb:list_cru')

        self.expected_view = views.CruCreate
        self.expected_form = forms.CruForm


@tag('dep', 'create')
class TestDepCreate(CommonCreateTest, TestCase):

    def setUp(self):
        super().setUp()
        self.data = Factory.DepFactory.get_valid_data()
        self.test_url = reverse_lazy('whalesdb:create_dep')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_success_url = reverse_lazy('whalesdb:list_dep')

        self.expected_view = views.DepCreate
        self.expected_form = forms.DepForm

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    def test_create_dep_context_fields(self):
        response = super().get_context()

        # Deploymnets also need to return a JSON formatted list of Station Codes
        self.assertIn("station_json", response.context)
        self.assertIn("java_script", response.context)
        self.assertEquals("whalesdb/_entry_dep_js.html", response.context['java_script'])


@tag('eca', 'create')
class TestEcaCreate(CommonCreateTest, TestCase):

    def setUp(self):
        super().setUp()
        self.data = Factory.EcaFactory.get_valid_data()
        self.test_url = reverse_lazy('whalesdb:create_eca')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_success_url = reverse_lazy('whalesdb:list_eca')

        self.expected_view = views.EcaCreate
        self.expected_form = forms.EcaForm


@tag('ecc', 'create')
class TestEccCreate(CommonCreateTest, TestCase):

    def setUp(self):
        super().setUp()
        self.eca = Factory.EcaFactory()

        self.data = Factory.EccFactory.get_valid_data()

        args = [self.eca.pk, 'pop']

        self.test_url = reverse_lazy('whalesdb:create_ecc', args=args)

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_success_url = reverse_lazy('shared_models:close_me_no_refresh')

        self.expected_view = views.EcaCreate
        self.expected_form = forms.EcaForm

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('ecc', 'create', 'context')
    def test_create_ecc_context_fields(self):
        response = super().get_context()

        self.assertIn("form", response.context)
        self.assertIn("eca", response.context['form'].initial)
        self.assertEquals(self.eca.pk, response.context['form'].initial['eca'])


@tag('eda', 'create')
class TestEdaCreate(CommonCreateTest, TestCase):

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

    def test_create_eda_eqp_filter(self):
        activate('en')

        dep = Factory.DepFactory()
        emm = Factory.EmmFactory(eqt=models.EqtEquipmentTypeCode.objects.get(pk=1))
        eqp1 = Factory.EqpFactory(emm=emm)
        eqp2 = Factory.EqpFactory(emm=emm)
        eqp3 = Factory.EqpFactory(emm=emm)

        models.EdaEquipmentAttachment(dep=dep, eqp=eqp1).save()

        models.EdaEquipmentAttachment(dep=dep, eqp=eqp2).save()

        test_url = reverse_lazy('whalesdb:create_eda', args=(dep.pk,))

        self.login_whale_user()
        response = self.client.get(test_url)

        eqp_field = response.context_data["form"].fields['eqp']

        # Confusing, but there are four pieces of equipment at this point, one is created in the setup function.
        # Two of the four have been attached to the deployment created in this test case, so only two pieces of
        # equipment should be returned in the queryset.

        self.assertEqual(2, eqp_field.queryset.count())


@tag('emm', 'create')
class TestEmmCreate(CommonCreateTest, TestCase):

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

    # If the created emm object is a Hydrophone type user should be sent to the details page to add
    # hydrophone details
    def test_create_emm_hydrophone_successful_url(self):
        data = Factory.EmmFactory.get_valid_data(4)

        self.login_whale_user()
        response = self.client.post(self.test_url, data)

        # should only be one EMM object in the db
        emm_id = models.EmmMakeModel.objects.all()[0].pk
        self.assertRedirects(response=response, expected_url=reverse_lazy('whalesdb:details_emm', args=(emm_id,)))


@tag('ehe', 'create')
class TestEheCreate(CommonCreateTest, TestCase):

    def setUp(self):
        super().setUp()

        self.data = Factory.EheFactory.get_valid_data()

        self.test_url = reverse_lazy('whalesdb:create_ehe', args=(self.data['hyd'], self.data['ecp_channel_no'], 'pop',))

        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_success_url = reverse_lazy('shared_models:close_me_no_refresh')

        self.expected_view = views.EheCreate
        self.expected_form = forms.EheForm


@tag('eqh', 'create')
class TestEqhCreate(CommonCreateTest, TestCase):

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

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    def test_create_eqh_context_fields(self):
        response = super().get_context()

        self.assertIn("form", response.context)
        self.assertIn("emm", response.context['form'].initial)
        self.assertEquals(self.emm_id, response.context['form'].initial['emm'])


@tag('eqp', 'create')
class TestEqpCreate(CommonCreateTest, TestCase):

    def setUp(self):
        super().setUp()

        self.data = Factory.EqpFactory.get_valid_data()

        self.test_url = reverse_lazy('whalesdb:create_eqp')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_success_url = reverse_lazy('whalesdb:list_eqp')

        self.expected_view = views.EqpCreate
        self.expected_form = forms.EqpForm


@tag('eqr', 'create')
class TestEqrCreate(CommonCreateTest, TestCase):

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

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    def test_create_eqr_context_fields(self):
        response = super().get_context()

        self.assertIn("form", response.context)
        self.assertIn("emm", response.context['form'].initial)
        self.assertEquals(self.emm_id, response.context['form'].initial['emm'])


@tag('etr', 'create')
class TestEtrCreate(CommonCreateTest, TestCase):

    def setUp(self):
        super().setUp()

        self.data = Factory.EtrFactory.get_valid_data()

        # Hydrophone properties requires a make and model emm_id
        self.test_url = reverse_lazy('whalesdb:create_etr')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_success_url = reverse_lazy('whalesdb:list_etr')

        self.expected_view = views.EtrCreate
        self.expected_form = forms.EtrForm


@tag('mor', 'create')
class TestMorCreate(CommonCreateTest, TestCase):
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


@tag('prj', 'create')
class TestPrjCreate(CommonCreateTest, TestCase):

    def setUp(self):
        super().setUp()

        self.data = Factory.PrjFactory.get_valid_data()
        self.test_url = reverse_lazy('whalesdb:create_prj')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_success_url = reverse_lazy('whalesdb:list_prj')

        self.expected_view = views.PrjCreate

        self.expected_form = forms.PrjForm


@tag('rci', 'create')
class TestRciCreate(CommonCreateTest, TestCase):

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


@tag('rec', 'create')
class TestRecCreate(CommonCreateTest, TestCase):

    def setUp(self):
        super().setUp()

        self.data = Factory.RecFactory.get_valid_data()
        self.test_url = reverse_lazy('whalesdb:create_rec')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.RecCreate

        self.expected_form = forms.RecForm

        self.expected_success_url = reverse_lazy('whalesdb:list_rec')


@tag('rec', 'create')
class TestRecCreateFromDep(CommonCreateTest, TestCase):

    def setUp(self):
        super().setUp()
        self.eda = Factory.EdaFactory()

        self.data = Factory.RecFactory.get_valid_data()
        self.test_url = reverse_lazy('whalesdb:create_rec', args=(self.eda.pk,))

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.RecCreate

        self.expected_form = forms.RecForm

        self.expected_success_url = reverse_lazy('whalesdb:details_dep', args=(self.eda.dep.pk,))

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    def test_create_rec_dep_context_fields(self):
        response = super().get_context()

        self.assertIn("form", response.context)
        self.assertIn("eda_id", response.context['form'].initial)
        self.assertEquals(self.eda, response.context['form'].initial['eda_id'])


@tag('rsc', 'create')
class TestRscCreate(CommonCreateTest, TestCase):

    def setUp(self):
        super().setUp()

        self.data = Factory.RscFactory.get_valid_data()
        self.test_url = reverse_lazy('whalesdb:create_rsc')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.RscCreate

        self.expected_form = forms.RscForm

        self.expected_success_url = "whalesdb:details_rsc"

    def test_successful_url(self):
        super().assert_successful_url(signature=self.expected_success_url)


@tag('rst', 'create')
class TestRstCreate(CommonCreateTest, TestCase):

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

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    def test_create_rst_context_fields(self):
        response = super().get_context()

        self.assertIn("form", response.context)
        self.assertIn("rsc", response.context['form'].initial)
        self.assertEquals(self.rsc_id, response.context['form'].initial['rsc'])


@tag('ste', 'create')
class TestSteCreate(CommonCreateTest, TestCase):

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


@tag('stn', 'create')
class TestStnCreate(CommonCreateTest, TestCase):

    def setUp(self):
        super().setUp()

        self.data = Factory.StnFactory.get_valid_data()
        self.test_url = reverse_lazy('whalesdb:create_stn')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.StnCreate

        self.expected_form = forms.StnForm

        self.expected_success_url = reverse_lazy('whalesdb:list_stn')


@tag('tea', 'create')
class TestTeaCreate(CommonCreateTest, TestCase):

    def setUp(self):
        super().setUp()

        self.data = Factory.TeaFactory.get_valid_data()
        self.test_url = reverse_lazy('whalesdb:create_tea')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'shared_models/shared_entry_form.html'

        self.expected_view = views.TeaCreate

        self.expected_form = forms.TeaForm

        self.expected_success_url = reverse_lazy('whalesdb:list_tea')
