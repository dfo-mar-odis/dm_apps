
import factory
from django.utils import timezone
from faker import Factory

from bio_diversity import models

faker = Factory.create()


class AnidcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AnimalDetCode

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    min_val = factory.lazy_attribute(lambda o: faker.random_int(1, 1000))
    max_val = factory.lazy_attribute(lambda o: faker.random_int(1000, 2000))
    unit_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.UnitFactory")
    ani_subj_flag = factory.lazy_attribute(lambda o: faker.boolean())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        unit = UnitFactory()
        obj = AnidcFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'min_val': obj.min_val,
            'max_val': obj.max_val,
            'unit_id': unit.pk,
            'ani_subj_flag': obj.ani_subj_flag,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class AdscFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AniDetSubjCode

    anidc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.AnidcFactory")
    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        anidc_id = AnidcFactory()
        obj = AdscFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'unit_id': anidc_id.pk,
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class CntFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Count

    loc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.LocFactory")
    contx_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ContxFactory")
    cntc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.CntcFactory")
    spec_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.SpecFactory")
    cnt = factory.lazy_attribute(lambda o: faker.random_int(1, 1000))
    est = factory.lazy_attribute(lambda o: faker.boolean())
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        loc = LocFactory()
        contx = ContxFactory()
        cntc = CntcFactory()
        spec = SpecFactory()

        obj = CntFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'loc_id': loc.pk,
            'contx_id': contx.pk,
            'cntc_id': cntc.pk,
            'spec_id': spec.pk,
            'cnt': obj.cnt,
            'est': obj.est,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class CntcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CountCode

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        obj = CntcFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class CntdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CountDet

    cnt_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.CntFactory")
    anidc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.AnidcFactory")
    adsc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.AdscFactory")
    det_val = factory.lazy_attribute(lambda o: faker.random_number(1, 1000))
    qual_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.QualFactory")
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        cnt = CntFactory()
        anidc = AnidcFactory()
        adsc = AdscFactory()
        qual = QualFactory()

        obj = CntdFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'cnt_id': cnt.pk,
            'anidc_id': anidc.pk,
            'adsc_id': adsc.pk,
            'det_val': obj.det_val,
            'qual_id': qual.pk,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data



class CollFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Collection

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        obj = CollFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class ContdcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ContainerDetCode

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    min_val = factory.lazy_attribute(lambda o: faker.random_int(1, 1000))
    max_val = factory.lazy_attribute(lambda o: faker.random_int(1000, 2000))
    unit_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.UnitFactory")
    cont_subj_flag = factory.lazy_attribute(lambda o: faker.random_letter())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        unit = UnitFactory()
        obj = ContdcFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'min_val': obj.min_val,
            'max_val': obj.max_val,
            'unit_id': unit.pk,
            'cont_subj_flag': obj.cont_subj_flag,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class ContxFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ContainerXRef

    evnt_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.EvntFactory")
    tank_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.TankFactory")
    trof_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.TrofFactory")
    tray_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.TrayFactory")
    heat_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.HeatFactory")
    draw_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.DrawFactory")
    cup_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.CupFactory")
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        evnt = EvntFactory()
        tank = TankFactory()
        obj = ContxFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'evnt_id': evnt.pk,
            'tank_id': tank.pk,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class CdscFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ContDetSubjCode

    contdc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ContdcFactory")
    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        contdc = ContdcFactory()
        obj = ContdcFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'contdc_id': contdc.pk,
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class CupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Cup

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        obj = CupFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class CupdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CupDet

    contdc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ContdcFactory")
    cup_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.CupFactory")

    det_value = factory.lazy_attribute(lambda o: faker.random_number(1, 1000))
    cdsc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.CdscFactory")
    start_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='-30y', end_date='today'))
    end_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='today', end_date='+30y'))
    det_valid = factory.lazy_attribute(lambda o: faker.boolean())
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        contdc = ContdcFactory()
        cup = CupFactory()
        cdsc = CdscFactory()
        obj = CupdFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'contdc_id': contdc.pk,
            'cup_id': cup.pk,
            'det_value': obj.det_value,
            'cdsc_id': cdsc.pk,
            'start_date': obj.start_date,
            'end_date': obj.end_date,
            'det_valid': obj.det_valid,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class DrawFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Drawer

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        obj = DrawFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class EnvFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EnvCondition

    contx_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ContxFactory")
    loc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.LocFactory")
    inst_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.InstFactory")
    envc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.EnvcFactory")
    env_val = factory.lazy_attribute(lambda o: faker.random_number(1, 1000))
    envsc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.EnvscFactory")
    env_start = factory.lazy_attribute(lambda o: faker.date_time_between(start_date='-30y', end_date='now'))
    env_starttime = factory.lazy_attribute(lambda o: faker.time())
    env_end = factory.lazy_attribute(lambda o: faker.date_time_between(start_date='now', end_date='+30y'))
    env_endtime = factory.lazy_attribute(lambda o: faker.time())
    env_avg = factory.lazy_attribute(lambda o: faker.boolean())
    qual_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.QualFactory")
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        contx = ContxFactory()
        loc = LocFactory()
        inst = InstFactory()
        envc = EnvcFactory()
        envsc = EnvscFactory()
        qual = QualFactory()

        obj = EnvFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'contx_id': contx.pk,
            'loc_id': loc.pk,
            'inst_id': inst.pk,
            'envc_id': envc.pk,
            'env_val': obj.env_val,
            'envsc_id': envsc.pk,
            'env_start': obj.env_start,
            'env_starttime': obj.env_starttime,
            'env_end': obj.env_end,
            'env_endtime': obj.env_endtime,
            'env_avg': obj.env_avg,
            'qual_id': qual.pk,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class EnvcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EnvCode

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    min_val = factory.lazy_attribute(lambda o: faker.random_number(1, 1000))
    max_val = factory.lazy_attribute(lambda o: faker.random_number(1, 1000))
    unit_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.UnitFactory")
    env_subj_flag = factory.lazy_attribute(lambda o: faker.boolean())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        unit = UnitFactory()

        obj = EnvcFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'min_val': obj.min_val,
            'max_val': obj.max_val,
            'unit_id': unit.pk,
            'env_subj_flag': obj.env_subj_flag,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class EnvscFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EnvSubjCode

    envc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.EnvcFactory")
    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        envc = EnvcFactory()
        obj = EnvscFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'envc_id': envc.pk,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class EvntFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Event

    facic_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.FacicFactory")
    evntc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.EvntcFactory")
    perc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.PercFactory")
    prog_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ProgFactory")
    team_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.TeamFactory")
    evnt_start = factory.lazy_attribute(lambda o: faker.date_time_between(start_date='-30y', end_date='now'))
    evnt_starttime = factory.lazy_attribute(lambda o: faker.time())
    evnt_end = factory.lazy_attribute(lambda o: faker.date_time_between(start_date='now', end_date='+30y'))
    evnt_endtime = factory.lazy_attribute(lambda o: faker.time())
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        fabic = FacicFactory()
        evntc = EvntcFactory()
        perc = PercFactory()
        prog = ProgFactory()
        team = TeamFactory()
        obj = EvntFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'facic_id': fabic.pk,
            'evntc_id': evntc.pk,
            'perc_id': perc.pk,
            'prog_id': prog.pk,
            'team_id': team.pk,
            'evnt_start': obj.evnt_start,
            'evnt_starttime': obj.evnt_starttime,
            'evnt_end': obj.evnt_end,
            'evnt_endtime': obj.evnt_endtime,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class EvntcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EventCode

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        obj = EvntcFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class FacicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FacilityCode

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        obj = FacicFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class FeedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Feeding

    contx_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ContxFactory")
    feedm_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.FeedmFactory")
    feedc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.FeedcFactory")
    lot_num = factory.lazy_attribute(lambda o: faker.word())
    amt = factory.lazy_attribute(lambda o: faker.random_number(1, 1000))
    unit_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.UnitFactory")
    freq = factory.lazy_attribute(lambda o: faker.word())
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        contx = ContxFactory()
        feedm = FeedmFactory()
        feedc = FeedcFactory()
        unit = UnitFactory()
        obj = FeedFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'contx_id': contx.pk,
            'feedm_id': feedm.pk,
            'feedc_id': feedc.pk,
            # 'lot_num': obj.lot_num,
            'amt': obj.amt,
            'unit_id': unit.pk,
            # 'freq': obj.freq,
            # 'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class FeedcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FeedCode

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    manufacturer = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        obj = FeedcFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'manufacturer': obj.manufacturer,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class FeedmFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FeedMethod

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        obj = FeedmFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class HeatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.HeathUnit

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    manufacturer = factory.lazy_attribute(lambda o: faker.word())
    inservice_date = factory.lazy_attribute(lambda o: faker.date())
    serial_number = factory.lazy_attribute(lambda o: faker.word())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        obj = HeatFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'manufacturer': obj.manufacturer,
            'inservice_date': obj.inservice_date,
            'serial_number': obj.serial_number,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class HeatdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.HeathUnitDet

    contdc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ContdcFactory")
    heat_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.HeatFactory")
    det_value = factory.lazy_attribute(lambda o: faker.random_number(1, 1000))
    cdsc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.CdscFactory")
    start_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='-30y', end_date='today'))
    end_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='today', end_date='+30y'))
    det_valid = factory.lazy_attribute(lambda o: faker.boolean())
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        contdc = ContdcFactory()
        heat = HeatFactory()
        cdsc = CdscFactory()
        obj = HeatdFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'contdc_id': contdc.pk,
            'heat_id': heat.pk,
            'det_value': obj.det_value,
            'cdsc_id': cdsc.pk,
            'start_date': obj.start_date,
            'end_date': obj.end_date,
            'det_valid': obj.det_valid,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class InstFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Instrument

    # needs an instcode id
    instc = factory.SubFactory("bio_diversity.test.BioFactoryFloor.InstcFactory")
    serial_number = factory.lazy_attribute(lambda o: faker.word())
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        # There are a couple of ways to get data out of a Factory
        #
        # Create an instance (BioFactoryFloor.InstFactory() or BioFactoryFloor.InstFactory.create()). This will make
        # an entry in the database and return the object.
        #
        # Build an instance (BioFactoryFloor.InstFactory.build()). This will create an instance of the object, but not
        # enter it in the database.
        #
        # Similar there are Create and Build batches (BioFactoryFloor.InstFactory.create_batch(),
        # BioFactoryFloor.InstFactory.build_batch()) which will produce multiple instances of objects.

        # In this case I created the data, as a dictionary, but didn't want that entered into the database. I just want
        # an dictionary of data to pass to the test method to ensure the creation form puts the data in the database
        # correctly.

        instc = InstcFactory()

        obj = InstFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'instc': instc.pk,
            'serial_number': obj.serial_number,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class InstcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.InstrumentCode

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        obj = InstcFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class InstdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.InstrumentDet

    # needs an inst id
    inst = factory.SubFactory("bio_diversity.test.BioFactoryFloor.InstFactory")
    instdc = factory.SubFactory("bio_diversity.test.BioFactoryFloor.InstdcFactory")
    det_value = factory.lazy_attribute(lambda o: faker.random_int(1, 1000))
    start_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='-30y', end_date='today'))
    end_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='today', end_date='+30y'))
    valid = factory.lazy_attribute(lambda o: faker.boolean())
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        # There are a couple of ways to get data out of a Factory
        #
        # Create an instance (BioFactoryFloor.InstFactory() or BioFactoryFloor.InstFactory.create()). This will make
        # an entry in the database and return the object.
        #
        # Build an instance (BioFactoryFloor.InstFactory.build()). This will create an instance of the object, but not
        # enter it in the database.
        #
        # Similar there are Create and Build batches (BioFactoryFloor.InstFactory.create_batch(),
        # BioFactoryFloor.InstFactory.build_batch()) which will produce multiple instances of objects.

        # In this case I created the data, as a dictionary, but didn't want that entered into the database. I just want
        # an dictionary of data to pass to the test method to ensure the creation form puts the data in the database
        # correctly.

        inst = InstFactory()
        instdc = InstdcFactory()

        obj = InstdFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'inst': inst.pk,
            'instdc': instdc.pk,
            'det_value': obj.det_value,
            'start_date': obj.start_date,
            'end_date': obj.end_date,
            'valid': obj.valid,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class InstdcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.InstDetCode

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        obj = InstdcFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class LocFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Location

    evnt_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.EvntFactory")
    locc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.LoccFactory")
    rive_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.RiveFactory")
    trib_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.TribFactory")
    subr_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.SubrFactory")
    relc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.RelcFactory")
    loc_lat = factory.lazy_attribute(lambda o: faker.random_number(1, 90))
    loc_lon = factory.lazy_attribute(lambda o: faker.random_number(1, 90))
    loc_date = factory.lazy_attribute(lambda o: faker.date_time(tzinfo=timezone.get_current_timezone()))
    loc_time = factory.lazy_attribute(lambda o: faker.time())
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        evnt = EvntFactory()
        locc = LoccFactory()
        rive = RiveFactory()
        trib = TribFactory()
        subr = SubrFactory()
        relc = RelcFactory()
        obj = LocFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'evnt_id': evnt.pk,
            'locc_id': locc.pk,
            'rive_id': rive.pk,
            'trib_id': trib.pk,
            'subr_id': subr.pk,
            'relc_id': relc.pk,
            'loc_lat': obj.loc_lat,
            'loc_lon': obj.loc_lon,
            'loc_date': obj.loc_date,
            'loc_time': obj.loc_time,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class LoccFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LocCode

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        obj = LoccFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class OrgaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Organization

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        obj = OrgaFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class PercFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PersonnelCode

    perc_first_name = factory.lazy_attribute(lambda o: faker.word())
    perc_last_name = factory.lazy_attribute(lambda o: faker.word())
    perc_valid = factory.lazy_attribute(lambda o: faker.boolean())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        obj = PercFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'perc_first_name': obj.perc_first_name,
            'perc_last_name': obj.perc_last_name,
            'perc_valid': obj.perc_valid,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class PrioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PriorityCode

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        obj = PrioFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class ProgFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Program

    prog_name = factory.lazy_attribute(lambda o: faker.word())
    prog_desc = factory.lazy_attribute(lambda o: faker.text())
    proga_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ProgaFactory")
    orga_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.OrgaFactory")
    start_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='-30y', end_date='today'))
    end_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='today', end_date='+30y'))
    valid = factory.lazy_attribute(lambda o: faker.boolean())
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        proga = ProgaFactory()
        orga = OrgaFactory()

        obj = ProgFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'prog_name': obj.prog_name,
            'prog_desc': obj.prog_desc,
            'proga_id': proga.pk,
            'orga_id': orga.pk,
            'start_date': obj.start_date,
            'end_date': obj.end_date,
            'valid': obj.valid,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class ProgaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProgAuthority

    proga_last_name = factory.lazy_attribute(lambda o: faker.word())
    proga_first_name = factory.lazy_attribute(lambda o: faker.word())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        obj = ProgaFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'proga_last_name': obj.proga_last_name,
            'proga_first_name': obj.proga_first_name,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class ProtFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Protocol

    prog_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ProgFactory")
    protc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ProtcFactory")
    # protf_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ProtfFactory")
    prot_desc = factory.lazy_attribute(lambda o: faker.text())
    start_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='-30y', end_date='today'))
    end_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='today', end_date='+30y'))
    valid = factory.lazy_attribute(lambda o: faker.boolean())
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        prog = ProgFactory()
        protc = ProtcFactory()
        # protf = ProtFactory()

        obj = ProtFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'prog_id': prog.pk,
            'protc_id': protc.pk,
            # 'protf_id' : protf.pk,
            'prot_desc': obj.prot_desc,
            'start_date': obj.start_date,
            'end_date': obj.end_date,
            'valid': obj.valid,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class ProtcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProtoCode

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        obj = ProtcFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class ProtfFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Protofile

    prot_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ProtFactory")
    protf_pdf = factory.lazy_attribute(lambda o: faker.url())
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        prot = ProtFactory()
        obj = ProtfFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'prot_id': prot.pk,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class QualFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.QualCode

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        obj = QualFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class RelcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ReleaseSiteCode

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    rive_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.RiveFactory")
    trib_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.TribFactory")
    subr_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.SubrFactory")
    min_lat = factory.lazy_attribute(lambda o: faker.random_number(1, 90))
    max_lat = factory.lazy_attribute(lambda o: faker.random_number(1, 90))
    min_lon = factory.lazy_attribute(lambda o: faker.random_number(1, 90))
    max_lon = factory.lazy_attribute(lambda o: faker.random_number(1, 90))

    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        rive = RiveFactory()
        trib = TribFactory()
        subr = SubrFactory()
        obj = RelcFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'rive_id': rive.pk,
            'trib_id': trib.pk,
            'subr_id': subr.pk,
            'min_lat': obj.min_lat,
            'max_lat': obj.max_lat,
            'min_lon': obj.min_lon,
            'max_lon': obj.max_lon,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class RiveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.RiverCode

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        obj = RiveFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.RoleCode

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        obj = RoleFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class SampFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Sample

    loc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.LocFactory")
    samp_num = factory.lazy_attribute(lambda o: faker.random_number(1, 1000))
    spec_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.SpecFactory")
    sampc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.SampcFactory")
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        loc = LocFactory()
        sampc = SampcFactory()
        spec = SpecFactory()

        obj = SampFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'loc_id': loc.pk,
            'samp_num': obj.samp_num,
            'spec_id': spec.pk,
            'sampc_id': sampc.pk,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class SampcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SampleCode

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        obj = SampcFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class SampdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SampleDet

    samp_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.SampFactory")
    anidc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.AnidcFactory")
    det_val = factory.lazy_attribute(lambda o: faker.random_number(1, 1000))
    adsc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.AdscFactory")
    qual_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.QualFactory")
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        samp = SampFactory()
        anidc = AnidcFactory()
        adsc = AdscFactory()
        qual = QualFactory()
        obj = SampdFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'samp_id': samp.pk,
            'anidc_id': anidc.pk,
            'det_val': obj.det_val,
            'adsc_id': adsc.pk,
            'qual_id': qual.pk,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class SpecFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SpeciesCode

    name = factory.lazy_attribute(lambda o: faker.word())
    species = factory.lazy_attribute(lambda o: faker.word())
    com_name = factory.lazy_attribute(lambda o: faker.word())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        obj = SpecFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'species': obj.species,
            'com_name': obj.com_name,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class StokFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.StockCode

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        obj = StokFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data

class SubrFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SubRiverCode

    rive_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.RiveFactory")
    trib_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.TribFactory")
    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        rive = RiveFactory()
        trib = TribFactory()
        obj = SubrFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'rive_id': rive.pk,
            'trib_id': trib.pk,
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class TankFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tank

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        obj = TankFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class TankdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TankDet

    contdc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ContdcFactory")
    tank_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.TankFactory")

    det_value = factory.lazy_attribute(lambda o: faker.random_number(1, 1000))
    cdsc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.CdscFactory")
    start_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='-30y', end_date='today'))
    end_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='today', end_date='+30y'))
    det_valid = factory.lazy_attribute(lambda o: faker.boolean())
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        contdc = ContdcFactory()
        tank = TankFactory()
        cdsc = CdscFactory()
        obj = TankdFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'contdc_id': contdc.pk,
            'tank_id': tank.pk,
            'det_value': obj.det_value,
            'cdsc_id': cdsc.pk,
            'start_date': obj.start_date,
            'end_date': obj.end_date,
            'det_valid': obj.det_valid,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Team

    perc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.PercFactory")
    role_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.RoleFactory")
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        perc = PercFactory()
        role = RoleFactory()

        obj = TeamFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'perc_id': perc.pk,
            'role_id': role.pk,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class TrayFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tray

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        obj = TrayFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class TraydFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TrayDet

    contdc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ContdcFactory")
    tray_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.TrayFactory")

    det_value = factory.lazy_attribute(lambda o: faker.random_number(1, 1000))
    cdsc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.CdscFactory")
    start_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='-30y', end_date='today'))
    end_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='today', end_date='+30y'))
    det_valid = factory.lazy_attribute(lambda o: faker.boolean())
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        contdc = ContdcFactory()
        tray = TrayFactory()
        cdsc = CdscFactory()
        obj = TraydFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'contdc_id': contdc.pk,
            'tray_id': tray.pk,
            'det_value': obj.det_value,
            'cdsc_id': cdsc.pk,
            'start_date': obj.start_date,
            'end_date': obj.end_date,
            'det_valid': obj.det_valid,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class TribFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tributary

    rive_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.RiveFactory")
    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        rive = RiveFactory()
        obj = TribFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'rive_id': rive.pk,
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class TrofFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Trough

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        obj = TrofFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class TrofdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TroughDet

    contdc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ContdcFactory")
    trof_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.TrofFactory")

    det_value = factory.lazy_attribute(lambda o: faker.random_number(1, 1000))
    cdsc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.CdscFactory")
    start_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='-30y', end_date='today'))
    end_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='today', end_date='+30y'))
    det_valid = factory.lazy_attribute(lambda o: faker.boolean())
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        contdc = ContdcFactory()
        trof = TrofFactory()
        cdsc = CdscFactory()
        obj = TrofdFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'contdc_id': contdc.pk,
            'trof_id': trof.pk,
            'det_value': obj.det_value,
            'cdsc_id': cdsc.pk,
            'start_date': obj.start_date,
            'end_date': obj.end_date,
            'det_valid': obj.det_valid,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class UnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.UnitCode

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        obj = UnitFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data