from django import forms as d_forms
from django.test import tag
from faker import Factory

from whalesdb.test.common_views import CommonFormTest
from whalesdb import forms, models

import whalesdb.test.WhalesdbFactoryFloor as factory

# used to create fake data
faker = Factory.create()


class TestDepForm(CommonFormTest):

    def setUp(self) -> None:
        super().setUp()
        self.form_class = forms.DepForm
        self.test_factory = factory.DepFactory

    @tag('dep', 'form', 'valid')
    def test_dep_valid_data(self):
        self.assert_valid_data()

    # test that the required fields exists and that they has a "create_url" attribute
    @tag('dep', 'form', 'field')
    def test_dep_field_create(self):
        form = self.form_class()
        self.assertIn("prj", form.fields)
        self.assertIn("stn", form.fields)
        self.assertIn("mor", form.fields)

        self.assertTrue(hasattr(form.fields['stn'], 'create_url'))
        self.assertEquals(form.fields['stn'].create_url, 'whalesdb:create_stn')

        self.assertTrue(hasattr(form.fields['prj'], 'create_url'))
        self.assertEquals(form.fields['prj'].create_url, 'whalesdb:create_prj')

        self.assertTrue(hasattr(form.fields['mor'], 'create_url'))
        self.assertEquals(form.fields['mor'].create_url, 'whalesdb:create_mor')

    # The deployment form should have a minimum height and width used to resize popup windows
    @tag('dep', 'form', 'properties')
    def test_dep_properties(self):
        form = self.form_class()
        self.assertTrue(hasattr(form, 'min_height'))
        self.assertTrue(hasattr(form, 'min_width'))


class TestEdaForm(CommonFormTest):

    def setUp(self) -> None:
        super().setUp()
        self.form_class = forms.EdaForm
        self.test_factory = factory.EdaFactory

    @tag('eda', 'form', 'valid')
    def test_eda_valid_data(self):
        self.assert_valid_data()

    # test that the required fields exists and that they has a "create_url" attribute
    @tag('eda', 'form', 'field')
    def test_eda_field_create(self):
        form = self.form_class()
        self.assertIn("dep", form.fields)
        self.assertIsInstance(form.fields['dep'].widget, d_forms.HiddenInput)

    # The only Recorders should be able to be attached to a deployment so the equipment drop down should
    # filter out hydrophones
    @tag('eda', 'form', 'field')
    def test_eda_field_filter(self):
        recorder = factory.EmmFactory(pk=1)
        hydrophone = factory.EmmFactory(pk=4)

        rec_1 = factory.EqpFactory.create(emm=recorder)
        rec_2 = factory.EqpFactory.create(emm=recorder)

        hydro_1 = factory.EqpFactory(emm=hydrophone)

        form = self.form_class()

        self.assertIn("eqp", form.fields)
        self.assertIn(rec_1, form.fields['eqp'].queryset)
        self.assertIn(rec_2, form.fields['eqp'].queryset)
        self.assertNotIn(hydro_1, form.fields['eqp'].queryset)


class TestEqhForm(CommonFormTest):

    def setUp(self) -> None:
        super().setUp()
        self.form_class = forms.EqhForm
        self.test_factory = factory.EqhFactory

    @tag('eqh', 'form', 'valid')
    def test_eqh_valid_data(self):
        self.assert_valid_data()

    # test that the required fields exists and that they has a "create_url" attribute
    @tag('eqh', 'form', 'field')
    def test_eqh_field_create(self):
        form = self.form_class()
        self.assertIn("emm", form.fields)
        self.assertIsInstance(form.fields['emm'].widget, d_forms.HiddenInput)


class TestEqpForm(CommonFormTest):

    def setUp(self) -> None:
        super().setUp()
        self.form_class = forms.EqpForm
        self.test_factory = factory.EqpFactory

    @tag('eqp', 'form', 'valid')
    def test_eqp_valid_data(self):
        self.assert_valid_data()

    # test that the required fields exists and that they has a "create_url" attribute
    @tag('eqp', 'form', 'field')
    def test_eqp_field_create(self):
        form = self.form_class()
        self.assertIn("emm", form.fields)
        self.assertIn("eqo_owned_by", form.fields)

        self.assertTrue(hasattr(form.fields['emm'], 'create_url'))
        self.assertEquals(form.fields['emm'].create_url, 'whalesdb:create_emm')

        self.assertTrue(hasattr(form.fields['eqo_owned_by'], 'create_url'))
        self.assertEquals(form.fields['eqo_owned_by'].create_url, 'whalesdb:create_eqo')

    # The form should have a minimum height and width used to resize popup windows
    @tag('eqp', 'form', 'properties')
    def test_eqp_properties(self):
        form = self.form_class()
        self.assertTrue(hasattr(form, 'min_height'))
        self.assertTrue(hasattr(form, 'min_width'))


class TestEmmForm(CommonFormTest):

    def setUp(self) -> None:
        super().setUp()
        self.form_class = forms.EmmForm
        self.test_factory = factory.EmmFactory

    @tag('mor', 'form', 'valid')
    def test_mor_valid_data(self):
        self.assert_valid_data()

    # The MooringSetup form should have a minimum height and width used to resize popup windows
    @tag('mor', 'form', 'properties')
    def test_mor_properties(self):
        form = self.form_class()
        self.assertTrue(hasattr(form, 'min_height'))
        self.assertTrue(hasattr(form, 'min_width'))


class TestMorForm(CommonFormTest):

    def setUp(self) -> None:
        super().setUp()
        self.form_class = forms.MorForm
        self.test_factory = factory.MorFactory

    @tag('mor', 'form', 'valid')
    def test_mor_valid_data(self):
        self.assert_valid_data()

    # The MooringSetup form should have a minimum height and width used to resize popup windows
    @tag('mor', 'form', 'properties')
    def test_mor_properties(self):
        form = self.form_class()
        self.assertTrue(hasattr(form, 'min_height'))
        self.assertTrue(hasattr(form, 'min_width'))


class TestPrjForm(CommonFormTest):

    def setUp(self) -> None:
        super().setUp()
        self.form_class = forms.PrjForm
        self.test_factory = factory.PrjFactory

    @tag('prj', 'form', 'valid_data')
    def test_prj_valid_data(self):
        self.assert_valid_data()


class TestRciForm(CommonFormTest):

    def setUp(self) -> None:
        super().setUp()
        self.form_class = forms.RciForm
        self.test_factory = factory.RciFactory

    @tag('rci', 'form', 'valid_data')
    def test_rci_valid_data(self):
        self.assert_valid_data()

    # The Rci form should have a minimum height and width used to resize popup windows
    @tag('rci', 'form', 'properties')
    def test_rci_properties(self):
        form = self.form_class()
        self.assertTrue(hasattr(form, 'min_height'))
        self.assertTrue(hasattr(form, 'min_width'))

    # This form has some fields that should be hidden
    @tag('rci', 'form', 'widgets')
    def test_rci_widgets(self):
        form = self.form_class()

        self.assertTrue(hasattr(form.fields['rec_id'], 'widget'))
        self.assertIsInstance(form.fields['rec_id'].widget, d_forms.HiddenInput)


class TestRecForm(CommonFormTest):

    def setUp(self) -> None:
        super().setUp()
        self.form_class = forms.RecForm
        self.test_factory = factory.RecFactory

    @tag('rec', 'form', 'valid_data')
    def test_rec_valid_data(self):
        self.assert_valid_data()

    # This form has some fields that should be hidden
    @tag('rec', 'form', 'widgets')
    def test_rec_widgets(self):
        form = self.form_class()

        self.assertTrue(hasattr(form.fields['rec_start_date'], 'widget'))
        self.assertIsInstance(form.fields['rec_start_date'].widget, d_forms.DateInput)


class TestReeForm(CommonFormTest):

    def setUp(self) -> None:
        super().setUp()
        self.form_class = forms.ReeForm
        self.test_factory = factory.ReeFactory

    @tag('ree', 'form', 'valid_data')
    def test_ree_valid_data(self):
        self.assert_valid_data()

    # The Ree form should have a minimum height and width used to resize popup windows
    @tag('ree', 'form', 'properties')
    def test_ree_properties(self):
        form = self.form_class()
        self.assertTrue(hasattr(form, 'min_height'))
        self.assertTrue(hasattr(form, 'min_width'))

    # This form has some fields that should be hidden
    @tag('ree', 'form', 'widgets')
    def test_ree_widgets(self):
        form = self.form_class()

        self.assertTrue(hasattr(form.fields['rec_id'], 'widget'))
        self.assertIsInstance(form.fields['rec_id'].widget, d_forms.HiddenInput)


class TestRscForm(CommonFormTest):

    def setUp(self) -> None:
        super().setUp()
        self.form_class = forms.RscForm
        self.test_factory = factory.RscFactory

    @tag('rsc', 'form', 'valid_data')
    def test_rsc_valid_data(self):
        self.assert_valid_data()


class TestRstForm(CommonFormTest):

    def setUp(self) -> None:
        super().setUp()
        self.form_class = forms.RstForm
        self.test_factory = factory.RstFactory

    @tag('rst', 'form', 'valid_data')
    def test_rst_valid_data(self):
        self.assert_valid_data()

    # This form has some fields that should be hidden
    @tag('rst', 'form', 'widgets')
    def test_rst_widgets(self):
        form = self.form_class()

        self.assertTrue(hasattr(form.fields['rsc'], 'widget'))
        self.assertIsInstance(form.fields['rsc'].widget, d_forms.HiddenInput)


class TestRttForm(CommonFormTest):

    def setUp(self) -> None:
        super().setUp()
        self.form_class = forms.RttForm
        self.test_factory = factory.RttFactory

    @tag('rtt', 'form', 'valid_data')
    def test_rtt_valid_data(self):
        self.assert_valid_data()


class TestSteForm(CommonFormTest):

    def setUp(self) -> None:
        super().setUp()
        self.form_class = forms.SteForm
        self.test_factory = factory.SteFactory

    @tag('ste', 'form', 'valid_data')
    def test_ste_valid_data(self):
        self.assert_valid_data()

    # The Ste form should have a minimum height and width used to resize popup windows
    @tag('ste', 'form', 'properties')
    def test_ste_properties(self):
        form = self.form_class()
        self.assertTrue(hasattr(form, 'min_height'))
        self.assertTrue(hasattr(form, 'min_width'))

    # This form has some fields that should be hidden
    @tag('ste', 'form', 'widgets')
    def test_ste_widgets(self):
        form = self.form_class()

        self.assertTrue(hasattr(form.fields['ste_date'], 'widget'))
        self.assertIsInstance(form.fields['ste_date'].widget, d_forms.DateInput)

        self.assertTrue(hasattr(form.fields['dep'], 'widget'))
        self.assertIsInstance(form.fields['dep'].widget, d_forms.HiddenInput)

        self.assertTrue(hasattr(form.fields['set_type'], 'widget'))
        self.assertIsInstance(form.fields['set_type'].widget, d_forms.HiddenInput)


class TestStnForm(CommonFormTest):

    def setUp(self) -> None:
        super().setUp()
        self.form_class = forms.StnForm
        self.test_factory = factory.StnFactory

    @tag('stn', 'form', 'valid_data')
    def test_stn_valid_data(self):
        self.assert_valid_data()

    # The Station form should have a minimum height and width used to resize popup windows
    @tag('stn', 'form', 'properties')
    def test_stn_properties(self):
        form = self.form_class()
        self.assertTrue(hasattr(form, 'min_height'))
        self.assertTrue(hasattr(form, 'min_width'))


class TestTeaForm(CommonFormTest):

    def setUp(self) -> None:
        super().setUp()
        self.form_class = forms.TeaForm
        self.test_factory = factory.TeaFactory

    @tag('tea', 'form', 'valid_data')
    def test_tea_valid_data(self):
        self.assert_valid_data()

    # The Station form should have a minimum height and width used to resize popup windows
    @tag('tea', 'form', 'properties')
    def test_tea_properties(self):
        pass
        # form = self.form_class()
