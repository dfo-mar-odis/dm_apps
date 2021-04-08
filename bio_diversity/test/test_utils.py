import datetime

from django.test import tag
from bio_diversity.test import BioFactoryFloor
from bio_diversity import models, utils
from shared_models.test.common_tests import CommonTest
from random import randint


@tag("Grp", "Move", "Utils")
class TestGrpMove(CommonTest):
    fixtures = ["initial_data.json"]

    def setUp(self):
        super().setUp()  # used to import fixtures

        # create group, tank and evnt
        self.grp = BioFactoryFloor.GrpFactory()
        self.evnt = BioFactoryFloor.EvntFactory()
        self.tank = BioFactoryFloor.TankFactory()
        self.tank.facic_id = self.evnt.facic_id
        self.tank.save()
        self.final_tank = BioFactoryFloor.TankFactory()
        self.final_tank.facic_id = self.evnt.facic_id
        self.final_tank.save()
        self.cleaned_data = {
            "facic_id": self.evnt.facic_id,
            "evnt_id": self.evnt,
            "created_by": self.evnt.created_by,
            "created_date": self.evnt.created_date,
        }

    def test_grp_in_cont(self):
        # test a group with a contx is in one and only one tank:
        utils.enter_contx(self.tank, self.cleaned_data, True, grp_pk=self.grp.pk)
        self.assertEqual(self.grp.current_cont()[0], self.tank)
        self.assertEqual(len(self.grp.current_cont()), 1)

    def test_cont_has_grp(self):
        # test a tank with a contx has one and only one group in it:
        utils.enter_contx(self.tank, self.cleaned_data, True, grp_pk=self.grp.pk)
        indv_list, grp_list = self.tank.fish_in_cont()
        self.assertEqual(len(grp_list), 1)
        self.assertIn(self.grp, grp_list)

    def test_move_grp(self):
        # grp in one tank, gets moved, is in second tank and not in first tank
        utils.enter_contx(self.tank, self.cleaned_data, True, grp_pk=self.grp.pk)
        indv_list, grp_list = self.tank.fish_in_cont()
        self.assertIn(self.grp, grp_list)
        move_date = datetime.datetime.now().date()
        utils.create_movement_evnt(self.tank, self.final_tank, self.cleaned_data, move_date, grp_pk=self.grp.pk)
        indv_list, grp_list = self.tank.fish_in_cont()
        self.assertNotIn(self.grp, grp_list)
        indv_list, grp_list = self.final_tank.fish_in_cont()
        self.assertIn(self.grp, grp_list)

    def test_two_grps_one_tank(self):
        #  put two grps into a single tank, make sure both are located:
        second_grp = BioFactoryFloor.GrpFactory()
        utils.enter_contx(self.tank, self.cleaned_data, True, grp_pk=self.grp.pk)
        utils.enter_contx(self.tank, self.cleaned_data, True, grp_pk=second_grp.pk)
        indv_list, grp_list = self.tank.fish_in_cont()
        self.assertEqual(len(grp_list), 2)
        self.assertIn(self.grp, grp_list)
        self.assertIn(second_grp, grp_list)

    def test_fix_jumped_tanks(self):
        # simulate accidentally recording group in wrong tank and correcting:
        # ie A->B, C->D (fish is in both B and D) ->E should correct this
        tank_a = BioFactoryFloor.TankFactory()
        tank_a.facic_id = self.evnt.facic_id
        tank_a.save()
        tank_b = BioFactoryFloor.TankFactory()
        tank_b.facic_id = self.evnt.facic_id
        tank_b.save()
        tank_c = BioFactoryFloor.TankFactory()
        tank_c.facic_id = self.evnt.facic_id
        tank_c.save()
        tank_d = BioFactoryFloor.TankFactory()
        tank_d.facic_id = self.evnt.facic_id
        tank_d.save()
        tank_e = BioFactoryFloor.TankFactory()
        tank_e.facic_id = self.evnt.facic_id
        tank_e.save()
        # need three dates to ensure unique moving events, to keep django test env happy
        move_a_date = (datetime.datetime.now() - datetime.timedelta(days=2)).date()
        move_b_date = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
        move_c_date = datetime.datetime.now().date()

        utils.create_movement_evnt(tank_a, tank_b, self.cleaned_data, move_a_date, grp_pk=self.grp.pk)
        utils.create_movement_evnt(tank_c, tank_d, self.cleaned_data, move_b_date, grp_pk=self.grp.pk)
        self.assertIn(tank_b, self.grp.current_cont())
        self.assertIn(tank_d, self.grp.current_cont())
        utils.create_movement_evnt(None, tank_e, self.cleaned_data, move_c_date, grp_pk=self.grp.pk)
        self.assertIn(tank_e, self.grp.current_cont())
        self.assertNotIn(tank_c, self.grp.current_cont())
        self.assertNotIn(tank_d, self.grp.current_cont())


@tag("Grp", "Cnt", "Utils")
class TestGrpCnt(CommonTest):
    fixtures = ["initial_data.json"]

    def setUp(self):
        super().setUp()  # used to import fixtures

        # create group, put them in a tank:
        self.grp = BioFactoryFloor.GrpFactory()
        self.evnt = BioFactoryFloor.EvntFactory()
        self.tank = BioFactoryFloor.TankFactory()
        self.tank.facic_id = self.evnt.facic_id
        self.tank.save()
        self.final_tank = BioFactoryFloor.TankFactory()
        self.final_tank.facic_id = self.evnt.facic_id
        self.final_tank.save()
        self.cleaned_data = {
            "facic_id": self.evnt.facic_id,
            "evnt_id": self.evnt,
            "created_by": self.evnt.created_by,
            "created_date": self.evnt.created_date,
        }
        self.contx = utils.enter_contx(self.tank, self.cleaned_data, True, grp_pk=self.grp.pk, return_contx=True)

    def test_zero_cnt(self):
        # test that with no details present, count returns zero
        self.assertEqual(self.grp.count_fish_in_group(), 0)

    def test_simple_cnt(self):
        # test groups record a single count correctly
        cnt_val = randint(0, 100)
        utils.enter_cnt(self.cleaned_data, cnt_val, self.contx.pk, cnt_code="Fish in Container")
        self.assertEqual(self.grp.count_fish_in_group(), cnt_val)

    def test_two_cnts_one_grp(self):
        # add two counts in different containers and make sure group record proper count
        cnt_val = randint(0, 100)
        utils.enter_cnt(self.cleaned_data, cnt_val, self.contx.pk, cnt_code="Fish in Container")
        contx = utils.enter_contx(self.final_tank, self.cleaned_data, True, grp_pk=self.grp.pk, return_contx=True)
        utils.enter_cnt(self.cleaned_data, cnt_val, contx.pk, cnt_code="Fish in Container")
        self.assertEqual(self.grp.count_fish_in_group(), 2 * cnt_val)

    def test_program_grp_cnt(self):
        #  take two types of eggs from group in same event.
        init_cnt = randint(300, 500)
        cnt_one_val = randint(0, 100)
        cnt_two_val = randint(0, 100)
        utils.enter_cnt(self.cleaned_data, init_cnt, self.contx.pk, cnt_code="Eggs Added")
        cnt = utils.enter_cnt(self.cleaned_data, 0, self.contx.pk, cnt_code="Eggs Removed")
        utils.enter_cnt_det(self.cleaned_data, cnt, cnt_one_val, "Program Group", "EQU")
        utils.enter_cnt_det(self.cleaned_data, cnt, cnt_two_val, "Program Group", "PEQU")
        self.assertEqual(self.grp.count_fish_in_group(), init_cnt - cnt_one_val - cnt_two_val)

    def test_aboslute_cnt(self):
        #  take eggs from a group and then record absolute count the following day.
        init_cnt = randint(300, 500)
        cnt_one_val = randint(5, 100)
        cnt_final_val = randint(0, 5)
        next_day_evnt = BioFactoryFloor.EvntFactory()
        next_day_evnt.facic_id = self.evnt.facic_id
        next_day_evnt.start_datetime = self.evnt.start_datetime + datetime.timedelta(days=1)
        next_day_evnt.save()
        new_cleaned_data = self.cleaned_data.copy()
        new_cleaned_data["evnt_id"] = next_day_evnt
        end_contx = utils.enter_contx(self.tank, new_cleaned_data, None, grp_pk=self.grp.pk, return_contx=True)

        utils.enter_cnt(self.cleaned_data, init_cnt, self.contx.pk, cnt_code="Eggs Added")
        cnt = utils.enter_cnt(self.cleaned_data, 0, self.contx.pk, cnt_code="Eggs Removed")
        utils.enter_cnt_det(self.cleaned_data, cnt, cnt_one_val, "Program Group", "EQU")
        utils.enter_cnt(new_cleaned_data, cnt_final_val, end_contx.pk, cnt_code="Egg Count")
        self.assertEqual(self.grp.count_fish_in_group(), cnt_final_val)


