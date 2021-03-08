from datetime import timedelta

import pytz

from django.forms import model_to_dict
from django.test import tag
from datetime import datetime
from bio_diversity import forms
from bio_diversity.test import BioFactoryFloor
from shared_models.test.common_tests import CommonTest
from bio_diversity.models import PersonnelCode, Pairing, Program, Individual


@tag("Anix", 'forms')
class TestAnixForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.Form = forms.AnixForm
        self.data = BioFactoryFloor.AnixFactory.build_valid_data()

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_null_unique(self):
        instance = BioFactoryFloor.AnixFactory(contx_id=None)
        invalid_data = model_to_dict(instance)
        del invalid_data["id"]
        self.assert_form_invalid(self.Form, data=invalid_data)
        invalid_data["contx_id"] = 1
        self.assert_form_valid(self.Form, data=invalid_data)


@tag("Contx", 'forms')
class TestContxForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.Form = forms.ContxForm
        self.data = BioFactoryFloor.ContxFactory.build_valid_data()

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_null_unique(self):
        instance = BioFactoryFloor.ContxFactory(tank_id=None, trof_id=None, tray_id=None, heat_id=None, draw_id=None)
        invalid_data = model_to_dict(instance)
        del invalid_data["id"]
        self.assert_form_invalid(self.Form, data=invalid_data)
        invalid_data["tank_id"] = 1
        self.assert_form_valid(self.Form, data=invalid_data)


@tag("Cntd", 'forms')
class TestCntdForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.Form = forms.CntdForm
        self.data = BioFactoryFloor.CntdFactory.build_valid_data()

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_invalid_val(self):
        # cannot use values outside of anidc min-max range
        invalid_data = self.data.copy()
        test_anidc = BioFactoryFloor.AnidcFactory(max_val=(invalid_data['det_val'] - 1))
        invalid_data['anidc_id'] = test_anidc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

        invalid_data = self.data.copy()
        test_anidc = BioFactoryFloor.AnidcFactory(min_val=(invalid_data['det_val'] + 1))
        invalid_data['anidc_id'] = test_anidc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

    def test_null_val(self):
        invalid_data = self.data.copy()
        invalid_data["det_val"] = None
        self.assert_form_valid(self.Form, data=invalid_data)

    def test_null_unique(self):
        instance = BioFactoryFloor.CntdFactory(adsc_id=None)
        invalid_data = model_to_dict(instance)
        del invalid_data["id"]
        self.assert_form_invalid(self.Form, data=invalid_data)
        invalid_data["adsc_id"] = 1
        self.assert_form_valid(self.Form, data=invalid_data)


@tag("Cupd", 'forms')
class TestCupdForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.Form = forms.CupdForm
        self.data = BioFactoryFloor.CupdFactory.build_valid_data()

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_invalid_val(self):
        # cannot use values outside of contdc min-max range
        invalid_data = self.data.copy()
        test_contdc = BioFactoryFloor.ContdcFactory(max_val=(invalid_data['det_value'] - 1))
        invalid_data['contdc_id'] = test_contdc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

        invalid_data = self.data.copy()
        test_contdc = BioFactoryFloor.ContdcFactory(min_val=(invalid_data['det_value'] + 1))
        invalid_data['contdc_id'] = test_contdc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)
    

@tag("Env", 'forms')
class TestEnvForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.Form = forms.EnvForm
        self.data = BioFactoryFloor.EnvFactory.build_valid_data()

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_invalid_val(self):
        # cannot use values outside of envc min-max range
        invalid_data = self.data.copy()
        test_envc = BioFactoryFloor.EnvcFactory()
        test_envc.max_val = invalid_data['env_val'] - 1
        test_envc.save()
        invalid_data['envc_id'] = test_envc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

        invalid_data = self.data.copy()
        test_envc = BioFactoryFloor.EnvcFactory()
        test_envc.min_val = invalid_data['env_val'] + 1
        test_envc.save()
        invalid_data['envc_id'] = test_envc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

    def test_null_unique(self):
        instance = BioFactoryFloor.EnvFactory()
        instance.contx_id = None
        instance.start_datetime = datetime.strptime(instance.start_datetime.strftime("%Y%m%d%H%M"), "%Y%m%d%H%M").replace(tzinfo=pytz.UTC)
        instance.save()
        invalid_data = model_to_dict(instance)
        invalid_data["start_date"] = invalid_data["start_datetime"].date()
        invalid_data["start_time"] = invalid_data["start_datetime"].time().strftime("%H:%M")
        del invalid_data["id"]
        self.assert_form_invalid(self.Form, data=invalid_data)
        invalid_data["contx_id"] = 1
        self.assert_form_valid(self.Form, data=invalid_data)


@tag("Evnt", 'forms')
class TestEvntForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.Form = forms.EvntForm
        self.data = BioFactoryFloor.EvntFactory.build_valid_data()

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_invalid_perc(self):
        # cannot use invalid personnel code
        invalid_data = self.data.copy()
        non_valid_perc = BioFactoryFloor.PercFactory(perc_valid=False)
        invalid_data['perc_id'] = non_valid_perc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

    def test_invalid_prog(self):
        # cannot use invalid program
        invalid_data = self.data.copy()
        non_valid_prog = BioFactoryFloor.ProgFactory(valid=False)
        invalid_data['prog_id'] = non_valid_prog.pk
        try:
            self.assert_form_invalid(self.Form, data=invalid_data)
        except Program.DoesNotExist:
            pass


@tag("Fecu", 'forms')
class TestFecuForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.Form = forms.FecuForm
        self.data = BioFactoryFloor.FecuFactory.build_valid_data()

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_null_unique(self):
        instance = BioFactoryFloor.FecuFactory(coll_id=None)
        invalid_data = model_to_dict(instance)
        del invalid_data["id"]
        self.assert_form_invalid(self.Form, data=invalid_data)
        invalid_data["coll_id"] = 1
        self.assert_form_valid(self.Form, data=invalid_data)


@tag("Grpd", 'forms')
class TestGrpdForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.Form = forms.GrpdForm
        self.data = BioFactoryFloor.GrpdFactory.build_valid_data()

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_invalid_val(self):
        # cannot use values outside of anidc min-max range
        invalid_data = self.data.copy()
        test_anidc = BioFactoryFloor.AnidcFactory(max_val=(invalid_data['det_val'] - 1))
        invalid_data['anidc_id'] = test_anidc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

        invalid_data = self.data.copy()
        test_anidc = BioFactoryFloor.AnidcFactory(min_val=(invalid_data['det_val'] + 1))
        invalid_data['anidc_id'] = test_anidc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

    def test_null_val(self):
        invalid_data = self.data.copy()
        invalid_data["det_val"] = None
        self.assert_form_valid(self.Form, data=invalid_data)

    def test_null_unique(self):
        instance = BioFactoryFloor.GrpdFactory(adsc_id=None)
        invalid_data = model_to_dict(instance)
        del invalid_data["id"]
        self.assert_form_invalid(self.Form, data=invalid_data)
        invalid_data["adsc_id"] = 1
        self.assert_form_valid(self.Form, data=invalid_data)


@tag("Heatd", 'forms')
class TestHeatdForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.Form = forms.HeatdForm
        self.data = BioFactoryFloor.HeatdFactory.build_valid_data()

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_invalid_val(self):
        # cannot use values outside of contdc min-max range
        invalid_data = self.data.copy()
        test_contdc = BioFactoryFloor.ContdcFactory(max_val=(invalid_data['det_value'] - 1))
        invalid_data['contdc_id'] = test_contdc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

        invalid_data = self.data.copy()
        test_contdc = BioFactoryFloor.ContdcFactory(min_val=(invalid_data['det_value'] + 1))
        invalid_data['contdc_id'] = test_contdc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)


@tag("Img", 'forms')
class TestImgForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.Form = forms.ImgForm
        self.data = BioFactoryFloor.ImgFactory.build_valid_data()

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_null_unique(self):
        instance = BioFactoryFloor.ImgFactory(tankd_id=None)
        invalid_data = model_to_dict(instance)
        del invalid_data["id"]
        self.assert_form_invalid(self.Form, data=invalid_data)
        invalid_data["tankd_id"] = 1
        self.assert_form_valid(self.Form, data=invalid_data)


@tag("Indv", 'forms')
class TestIndvForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.data = BioFactoryFloor.IndvFactory.build_valid_data()
        self.Form = forms.IndvForm

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_invalid_grp(self):
        # cannot use invalid group code
        invalid_data = self.data.copy()
        non_valid_grp = BioFactoryFloor.GrpFactory(grp_valid=False)
        invalid_data['grp_id'] = non_valid_grp.pk
        self.assert_form_invalid(self.Form, data=invalid_data)


@tag("Indvd", 'forms')
class TestIndvdForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.Form = forms.IndvdForm
        self.data = BioFactoryFloor.IndvdFactory.build_valid_data()

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_invalid_val(self):
        # cannot use values outside of anidc min-max range
        invalid_data = self.data.copy()
        test_anidc = BioFactoryFloor.AnidcFactory(max_val=(invalid_data['det_val'] - 1))
        invalid_data['anidc_id'] = test_anidc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

        invalid_data = self.data.copy()
        test_anidc = BioFactoryFloor.AnidcFactory(min_val=(invalid_data['det_val'] + 1))
        invalid_data['anidc_id'] = test_anidc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

    def test_null_val(self):
        invalid_data = self.data.copy()
        invalid_data["det_val"] = None
        self.assert_form_valid(self.Form, data=invalid_data)

    def test_null_unique(self):
        instance = BioFactoryFloor.IndvdFactory(adsc_id=None)
        invalid_data = model_to_dict(instance)
        del invalid_data["id"]
        self.assert_form_invalid(self.Form, data=invalid_data)
        invalid_data["adsc_id"] = 1
        self.assert_form_valid(self.Form, data=invalid_data)


@tag("Instd", 'forms')
class TestInstdForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.Form = forms.InstdForm
        self.data = BioFactoryFloor.InstdFactory.build_valid_data()

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

 
@tag("Loc", 'forms')
class TestLocForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.Form = forms.LocForm
        self.data = BioFactoryFloor.LocFactory.build_valid_data()

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_null_unique(self):
        instance = BioFactoryFloor.LocFactory(subr_id=None)
        invalid_data = model_to_dict(instance)
        invalid_data["start_date"] = invalid_data["loc_date"].date()
        del invalid_data["id"]
        self.assert_form_invalid(self.Form, data=invalid_data)
        invalid_data["subr_id"] = 1
        self.assert_form_valid(self.Form, data=invalid_data)


@tag("Pair", 'forms')
class TestPairForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.data = BioFactoryFloor.PairFactory.build_valid_data()
        self.Form = forms.PairForm

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_invalid_indv(self):
        # cannot use invalid individual code
        invalid_data = self.data.copy()
        non_valid_indv = BioFactoryFloor.IndvFactory(indv_valid=False)
        invalid_data['indv_id'] = non_valid_indv.pk
        try:
            self.assert_form_invalid(self.Form, data=invalid_data)
        except Individual.DoesNotExist:
            pass

        # cannot use individual code with null pit_tag
        invalid_data = self.data.copy()
        non_valid_indv = BioFactoryFloor.IndvFactory(pit_tag=None)
        invalid_data['indv_id'] = non_valid_indv.pk
        try:
            self.assert_form_invalid(self.Form, data=invalid_data)
        except Individual.DoesNotExist:
            pass


@tag("Prot", 'forms')
class TestProtForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.data = BioFactoryFloor.ProtFactory.build_valid_data()
        self.Form = forms.ProtForm

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_invalid_prog(self):
        # cannot use invalid program
        invalid_data = self.data.copy()
        non_valid_prog = BioFactoryFloor.ProgFactory(valid=False)
        invalid_data['prog_id'] = non_valid_prog.pk
        try:
            self.assert_form_invalid(self.Form, data=invalid_data)
        except Program.DoesNotExist:
            pass


@tag("Protf", 'forms')
class TestProtfForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.data = BioFactoryFloor.ProtfFactory.build_valid_data()
        self.Form = forms.ProtfForm

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_invalid_prot(self):
        # cannot use invalid protocol
        invalid_data = self.data.copy()
        non_valid_prot = BioFactoryFloor.ProtFactory(valid=False)
        invalid_data['prot_id'] = non_valid_prot.pk
        self.assert_form_invalid(self.Form, data=invalid_data)


@tag("Sampd", 'forms')
class TestSampdForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.Form = forms.SampdForm
        self.data = BioFactoryFloor.SampdFactory.build_valid_data()

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_invalid_val(self):
        # cannot use values outside of anidc min-max range
        invalid_data = self.data.copy()
        test_anidc = BioFactoryFloor.AnidcFactory(max_val=(invalid_data['det_val'] - 1))
        invalid_data['anidc_id'] = test_anidc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

        invalid_data = self.data.copy()
        test_anidc = BioFactoryFloor.AnidcFactory(min_val=(invalid_data['det_val'] + 1))
        invalid_data['anidc_id'] = test_anidc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

    def test_null_val(self):
        invalid_data = self.data.copy()
        invalid_data["det_val"] = None
        self.assert_form_valid(self.Form, data=invalid_data)

    def test_null_unique(self):
        instance = BioFactoryFloor.SampdFactory(adsc_id=None)
        invalid_data = model_to_dict(instance)
        del invalid_data["id"]
        self.assert_form_invalid(self.Form, data=invalid_data)
        invalid_data["adsc_id"] = 1
        self.assert_form_valid(self.Form, data=invalid_data)


@tag("Sire", 'forms')
class TestSireForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.data = BioFactoryFloor.SireFactory.build_valid_data()
        self.Form = forms.SireForm

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_invalid_pair(self):
        # cannot use invalid pair code
        invalid_data = self.data.copy()
        non_valid_pair = BioFactoryFloor.PairFactory(valid=False)
        invalid_data['pair_id'] = non_valid_pair.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

    def test_invalid_indv(self):
        # cannot use invalid individual code
        invalid_data = self.data.copy()
        non_valid_indv = BioFactoryFloor.IndvFactory(indv_valid=False)
        invalid_data['indv_id'] = non_valid_indv.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

        # cannot use individual code with null pit tag
        invalid_data = self.data.copy()
        non_valid_indv = BioFactoryFloor.IndvFactory(pit_tag=None)
        invalid_data['indv_id'] = non_valid_indv.pk
        self.assert_form_invalid(self.Form, data=invalid_data)


@tag("Spwnd", 'forms')
class TestSpwndForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.Form = forms.SpwndForm
        self.data = BioFactoryFloor.SpwndFactory.build_valid_data()

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_invalid_val(self):
        # cannot use values outside of spwndc min-max range
        invalid_data = self.data.copy()
        test_spwndc = BioFactoryFloor.SpwndcFactory(max_val=(invalid_data['det_val'] - 1))
        invalid_data['spwndc_id'] = test_spwndc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

        invalid_data = self.data.copy()
        test_spwndc = BioFactoryFloor.SpwndcFactory(min_val=(invalid_data['det_val'] + 1))
        invalid_data['spwndc_id'] = test_spwndc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

    def test_null_val(self):
        invalid_data = self.data.copy()
        invalid_data["det_val"] = None
        self.assert_form_valid(self.Form, data=invalid_data)

    def test_null_unique(self):
        instance = BioFactoryFloor.SpwndFactory(spwnsc_id=None)
        invalid_data = model_to_dict(instance)
        del invalid_data["id"]
        self.assert_form_invalid(self.Form, data=invalid_data)
        invalid_data["spwnsc_id"] = 1
        self.assert_form_valid(self.Form, data=invalid_data)


@tag("Tankd", 'forms')
class TestTankdForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.Form = forms.TankdForm
        self.data = BioFactoryFloor.TankdFactory.build_valid_data()

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_invalid_val(self):
        # cannot use values outside of contdc min-max range
        invalid_data = self.data.copy()
        test_contdc = BioFactoryFloor.ContdcFactory(max_val=(invalid_data['det_value'] - 1))
        invalid_data['contdc_id'] = test_contdc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

        invalid_data = self.data.copy()
        test_contdc = BioFactoryFloor.ContdcFactory(min_val=(invalid_data['det_value'] + 1))
        invalid_data['contdc_id'] = test_contdc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)


@tag("Team", 'forms')
class TestTeamForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.data = BioFactoryFloor.TeamFactory.build_valid_data()
        self.Form = forms.TeamForm

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_invalid_perc(self):
        # cannot use invalid personnel code
        invalid_data = self.data.copy()
        non_valid_perc = BioFactoryFloor.PercFactory(perc_valid=False)
        invalid_data['perc_id'] = non_valid_perc.pk
        try:
            self.assert_form_invalid(self.Form, data=invalid_data)
        except PersonnelCode.DoesNotExist:
            pass


@tag("Trayd", 'forms')
class TestTraydForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.Form = forms.TraydForm
        self.data = BioFactoryFloor.TraydFactory.build_valid_data()

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_invalid_val(self):
        # cannot use values outside of contdc min-max range
        invalid_data = self.data.copy()
        test_contdc = BioFactoryFloor.ContdcFactory(max_val=(invalid_data['det_value'] - 1))
        invalid_data['contdc_id'] = test_contdc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

        invalid_data = self.data.copy()
        test_contdc = BioFactoryFloor.ContdcFactory(min_val=(invalid_data['det_value'] + 1))
        invalid_data['contdc_id'] = test_contdc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)


@tag("Trofd", 'forms')
class TestTrofdForm(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.Form = forms.TrofdForm
        self.data = BioFactoryFloor.TrofdFactory.build_valid_data()

    def test_valid_data(self):
        # get valid data
        self.assert_form_valid(self.Form, data=self.data)

    def test_invalid_val(self):
        # cannot use values outside of contdc min-max range
        invalid_data = self.data.copy()
        test_contdc = BioFactoryFloor.ContdcFactory(max_val=(invalid_data['det_value'] - 1))
        invalid_data['contdc_id'] = test_contdc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)

        invalid_data = self.data.copy()
        test_contdc = BioFactoryFloor.ContdcFactory(min_val=(invalid_data['det_value'] + 1))
        invalid_data['contdc_id'] = test_contdc.pk
        self.assert_form_invalid(self.Form, data=invalid_data)
