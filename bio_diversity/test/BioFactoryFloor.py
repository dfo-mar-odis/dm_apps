
import factory
import pytz
from django.utils import timezone
from faker import Factory

from bio_diversity import models

faker = Factory.create()


class AnidcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AnimalDetCode
        django_get_or_create = ('name',)

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    min_val = factory.lazy_attribute(lambda o: faker.random_int(1, 10))
    max_val = factory.lazy_attribute(lambda o: faker.random_int(20, 30))
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


class AnixFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AniDetailXref

    evnt_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.EvntFactory")
    contx_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ContxFactory")
    final_contx_flag = factory.lazy_attribute(lambda o: faker.boolean())
    loc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.LocFactory")
    indvt_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.IndvtFactory")
    indv_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.IndvFactory")
    pair_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.PairFactory")
    grp_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.GrpFactory")

    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        evnt = EvntFactory()
        contx = ContxFactory()
        loc = LocFactory()
        indvt = IndvtFactory()
        indv = IndvFactory()
        pair = PairFactory()
        grp = GrpFactory()
        obj = AnixFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'evnt_id': evnt.pk,
            'contx_id': contx.pk,
            'final_contx_flag': obj.final_contx_flag,
            'loc_id': loc.pk,
            'indvt_id': indvt.pk,
            'indv_id': indv.pk,
            'pair_id': pair.pk,
            'grp_id': grp.pk,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class AdscFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AniDetSubjCode
        django_get_or_create = ('name',)

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
            'anidc_id': anidc_id.pk,
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
    cnt = factory.lazy_attribute(lambda o: faker.random_int(1, 100))
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
        django_get_or_create = ('name',)

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
    det_val = factory.lazy_attribute(lambda o: faker.random_int(10, 20))
    qual_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.QualFactory")
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        cnt = CntFactory()
        adsc = AdscFactory()
        qual = QualFactory()
        anidc = AnidcFactory()
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
        django_get_or_create = ('name',)

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
        django_get_or_create = ('name',)

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    min_val = factory.lazy_attribute(lambda o: faker.random_int(0, 10))
    max_val = factory.lazy_attribute(lambda o: faker.random_int(20, 30))
    unit_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.UnitFactory")
    cont_subj_flag = factory.lazy_attribute(lambda o: faker.boolean())
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
        trof = TrofFactory()
        tray = TrayFactory()
        heat = HeatFactory()
        draw = DrawFactory()
        cup = CupFactory()
        obj = ContxFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'evnt_id': evnt.pk,
            'tank_id': tank.pk,
            'trof_id': trof.pk,
            'tray_id': tray.pk,
            'heat_id': heat.pk,
            'draw_id': draw.pk,
            'cup_id': cup.pk,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class CdscFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ContDetSubjCode
        django_get_or_create = ('name',)

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
        django_get_or_create = ('name',)

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    draw_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.DrawFactory")
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    start_date = factory.lazy_attribute(lambda o: faker.date())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        draw = DrawFactory()
        obj = CupFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'draw_id': draw.pk,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'start_date': obj.start_date,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class CupdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CupDet

    contdc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ContdcFactory")
    cup_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.CupFactory")

    det_value = factory.lazy_attribute(lambda o: faker.random_int(10, 20))
    cdsc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.CdscFactory")
    start_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='-30y', end_date='today'))
    end_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='today', end_date='+30y'))
    det_valid = True
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        cup = CupFactory()
        cdsc = CdscFactory()
        obj = CupdFactory.build(**kwargs)
        contdc = ContdcFactory()

        # Convert the data to a dictionary to be used in testing
        data = {
            'contdc_id': contdc.pk,
            'cup_id': cup.pk,
            'det_value': obj.det_value,
            'cdsc_id': cdsc.pk,
            'start_date': obj.start_date,
            'end_date': obj.end_date,
            'det_valid': True,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class DataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.DataLoader
    # only using one id for this test, can add more if necesary
    evnt_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.EvntFactory")
    evntc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.EvntcFactory")
    data_csv = factory.lazy_attribute(lambda o: faker.url())

    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        evnt = EvntFactory()
        evntc = EvntcFactory()
        obj = DataFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'evnt_id': evnt.pk,
            'evntc_id': evntc.pk,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class DrawFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Drawer
        django_get_or_create = ('name',)

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    heat_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.HeatFactory")
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        heat = HeatFactory()
        obj = DrawFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'heat_id': heat.pk,
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
    env_val = factory.lazy_attribute(lambda o: faker.random_int(10, 20))
    envsc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.EnvscFactory")
    start_datetime = factory.lazy_attribute(lambda o: faker.date_time_between(start_date='-30y', end_date='now',
                                                                              tzinfo=pytz.UTC))
    end_datetime = factory.lazy_attribute(lambda o: faker.date_time_between(start_date='now', end_date='+30y',
                                                                            tzinfo=pytz.UTC))
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
        envsc = EnvscFactory()
        qual = QualFactory()
        obj = EnvFactory.build(**kwargs)
        envc = EnvcFactory()

        # Convert the data to a dictionary to be used in testing
        data = {
            'contx_id': contx.pk,
            'loc_id': loc.pk,
            'inst_id': inst.pk,
            'envc_id': envc.pk,
            'env_val': obj.env_val,
            'envsc_id': envsc.pk,
            'start_date': obj.start_datetime.date(),
            'start_time': obj.start_datetime.time().strftime("%H:%M"),
            'end_date': obj.end_datetime.date(),
            'end_time': obj.end_datetime.time().strftime("%H:%M"),
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
        django_get_or_create = ('name',)

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    min_val = factory.lazy_attribute(lambda o: faker.random_int(0, 10))
    max_val = factory.lazy_attribute(lambda o: faker.random_int(20, 30))
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


class EnvcfFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EnvCondFile
    # only using one id for this test, can add more if necesary
    env_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.EnvFactory")
    env_pdf = factory.lazy_attribute(lambda o: faker.url())
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        env = EnvFactory()
        obj = EnvcfFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'env_id': env.pk,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class EnvscFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EnvSubjCode
        django_get_or_create = ('name',)

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


class EnvtFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EnvTreatment

    contx_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ContxFactory")
    envtc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.EnvtcFactory")
    lot_num = factory.lazy_attribute(lambda o: faker.word())
    amt = factory.lazy_attribute(lambda o: faker.random_int(1, 100))
    unit_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.UnitFactory")
    duration = factory.lazy_attribute(lambda o: faker.random_int(1, 100))
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        contx = ContxFactory()
        envtc = EnvtcFactory()
        unit = UnitFactory()
        obj = EnvtFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {

            'contx_id': contx.pk,
            'envtc_id': envtc.pk,
            'lot_num': obj.lot_num,
            'amt': obj.amt,
            'unit_id': unit.pk,
            'duration': obj.duration,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class EnvtcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EnvTreatCode
        django_get_or_create = ('name',)

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    rec_dose = factory.lazy_attribute(lambda o: faker.text())
    manufacturer = factory.lazy_attribute(lambda o: faker.word())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        obj = EnvtcFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {

            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'rec_dose': obj.rec_dose,
            'manufacturer': obj.manufacturer,
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
    start_datetime = factory.lazy_attribute(lambda o: faker.date_time_between(start_date='-30y', end_date='now',
                                                                          tzinfo=pytz.UTC))
    end_datetime = factory.lazy_attribute(lambda o: faker.date_time_between(start_date='now', end_date='+30y',
                                                                        tzinfo=pytz.UTC))
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
            'start_date': obj.start_datetime.date(),
            'start_time': obj.start_datetime.time().strftime("%H:%M"),
            'end_date': obj.end_datetime.date(),
            'end_time': obj.end_datetime.time().strftime("%H:%M"),
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class EvntcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EventCode
        django_get_or_create = ('name',)

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


class EvntfFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EventFile
    # only using one id for this test, can add more if necesary
    evnt_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.EvntFactory")
    evntfc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.EvntfcFactory")
    stok_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.StokFactory")
    evntf_xls = factory.lazy_attribute(lambda o: faker.url())
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        evnt = EvntFactory()
        evntfc = EvntfcFactory()
        stok = StokFactory()
        obj = EvntfFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'evnt_id': evnt.pk,
            'evntfc_id': evntfc.pk,
            'stok_id': stok.pk,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class EvntfcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EventFileCode
        django_get_or_create = ('name',)

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        obj = EvntfcFactory.build(**kwargs)

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
        django_get_or_create = ('name',)

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


class FecuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Fecundity

    # needs an inst id
    stok_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.StokFactory")
    coll_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.CollFactory")
    start_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='-30y', end_date='today'))
    end_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='today', end_date='+30y'))
    alpha = factory.lazy_attribute(lambda o: faker.random_int(1, 1000))
    beta = factory.lazy_attribute(lambda o: faker.random_int(1, 1000))
    valid = True
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        stok = StokFactory()
        coll = CollFactory()

        obj = FecuFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'stok_id': stok.pk,
            'coll_id': coll.pk,
            'start_date': obj.start_date,
            'end_date': obj.end_date,
            'alpha': obj.alpha,
            'beta': obj.beta,
            'valid': True,
            'comments': obj.comments,
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
    amt = factory.lazy_attribute(lambda o: faker.random_int(1, 100))
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
        django_get_or_create = ('name',)

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
        django_get_or_create = ('name',)

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


class GrpFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Group

    spec_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.SpecFactory")
    stok_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.StokFactory")
    coll_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.CollFactory")
    grp_year = factory.lazy_attribute(lambda o: faker.random_int(2000, 2020))
    grp_valid = True
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        spec = SpecFactory()
        stok = StokFactory()
        coll = CollFactory()
        obj = GrpFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {

            'spec_id': spec.pk,
            'stok_id': stok.pk,
            'grp_year': obj.grp_year,
            'coll_id': coll.pk,
            'grp_valid': True,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class GrpdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.GroupDet

    anix_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.AnixFactory")
    anidc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.AnidcFactory")
    det_val = factory.lazy_attribute(lambda o: faker.random_int(10, 20))
    detail_date = factory.lazy_attribute(lambda o: faker.date())
    adsc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.AdscFactory")
    qual_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.QualFactory")
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        anix = AnixFactory()
        adsc = AdscFactory()
        qual = QualFactory()
        anidc = AnidcFactory()
        obj = GrpdFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'anix_id': anix.pk,
            'anidc_id': anidc.pk,
            'det_val': obj.det_val,
            'detail_date': obj.detail_date,
            'adsc_id': adsc.pk,
            'qual_id': qual.pk,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class HeatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.HeathUnit
        django_get_or_create = ('name',)

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    facic_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.FacicFactory")
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    manufacturer = factory.lazy_attribute(lambda o: faker.word())
    inservice_date = factory.lazy_attribute(lambda o: faker.date())
    serial_number = factory.lazy_attribute(lambda o: faker.word())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        facic = FacicFactory()
        obj = HeatFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'facic_id': facic.pk,
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
    det_value = factory.lazy_attribute(lambda o: faker.random_int(10, 20))
    cdsc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.CdscFactory")
    start_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='-30y', end_date='today'))
    end_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='today', end_date='+30y'))
    det_valid = factory.lazy_attribute(lambda o: faker.boolean())
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        heat = HeatFactory()
        cdsc = CdscFactory()
        obj = HeatdFactory.build(**kwargs)
        contdc = ContdcFactory()

        # Convert the data to a dictionary to be used in testing
        data = {
            'contdc_id': contdc.pk,
            'heat_id': heat.pk,
            'det_value': obj.det_value,
            'cdsc_id': cdsc.pk,
            'start_date': obj.start_date,
            'end_date': obj.end_date,
            'det_valid': True,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class ImgFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Image
    # only using one id for this test, can add more if necesary
    imgc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ImgcFactory")
    tankd_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.TankdFactory")
    img_png = factory.lazy_attribute(lambda o: faker.url())
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        imgc = ImgcFactory()
        tankd = TankdFactory()
        obj = ImgFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'imgc_id': imgc.pk,
            'tankd_id': tankd.pk,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class ImgcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ImageCode
        django_get_or_create = ('name',)

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        obj = ImgcFactory.build(**kwargs)

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


class IndvFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Individual
        django_get_or_create = ('pit_tag',)

    grp_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.GrpFactory")
    spec_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.SpecFactory")
    stok_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.StokFactory")
    indv_year = factory.lazy_attribute(lambda o: faker.random_int(2000, 2020))
    coll_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.CollFactory")
    pit_tag = factory.lazy_attribute(lambda o: faker.word())
    indv_valid = True
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        grp = GrpFactory()
        spec = SpecFactory()
        stok = StokFactory()
        coll = CollFactory()
        obj = IndvFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {

            'grp_id': grp.pk,
            'spec_id': spec.pk,
            'stok_id': stok.pk,
            'coll_id': coll.pk,
            'indv_year': obj.indv_year,
            'pit_tag': obj.pit_tag,
            'indv_valid': True,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class IndvdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.IndividualDet

    anix_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.AnixFactory")
    anidc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.AnidcFactory")
    det_val = factory.lazy_attribute(lambda o: faker.random_int(10, 20))
    detail_date = factory.lazy_attribute(lambda o: faker.date())
    adsc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.AdscFactory")
    qual_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.QualFactory")
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        anix = AnixFactory()
        adsc = AdscFactory()
        qual = QualFactory()
        anidc = AnidcFactory()
        obj = IndvdFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'anix_id': anix.pk,
            'anidc_id': anidc.pk,
            'det_val': obj.det_val,
            "detail_date": obj.detail_date,
            'adsc_id': adsc.pk,
            'qual_id': qual.pk,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class IndvtFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.IndTreatment

    indvtc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.IndvtcFactory")
    lot_num = factory.lazy_attribute(lambda o: faker.word())
    dose = factory.lazy_attribute(lambda o: faker.random_int(1, 100))
    unit_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.UnitFactory")
    start_datetime = factory.lazy_attribute(lambda o: faker.date_time_between(start_date='-30y', end_date='now',
                                                                              tzinfo=pytz.UTC))
    end_datetime = factory.lazy_attribute(lambda o: faker.date_time_between(start_date='now', end_date='+30y',
                                                                            tzinfo=pytz.UTC))
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        indvtc = IndvtcFactory()
        unit = UnitFactory()
        obj = IndvtFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {

            'indvtc_id': indvtc.pk,
            'lot_num': obj.lot_num,
            'dose': obj.dose,
            'unit_id': unit.pk,
            'start_date': obj.start_datetime.date(),
            'start_time': obj.start_datetime.time().strftime("%H:%M"),
            'end_date': obj.end_datetime.date(),
            'end_time': obj.end_datetime.time().strftime("%H:%M"),
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class IndvtcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.IndTreatCode
        django_get_or_create = ('name',)

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    rec_dose = factory.lazy_attribute(lambda o: faker.text())
    manufacturer = factory.lazy_attribute(lambda o: faker.word())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        obj = IndvtcFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {

            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'rec_dose': obj.rec_dose,
            'manufacturer': obj.manufacturer,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class InstFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Instrument
        django_get_or_create = ('serial_number',)

    # needs an instcode id
    instc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.InstcFactory")
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
            'instc_id': instc.pk,
            'serial_number': obj.serial_number,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class InstcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.InstrumentCode
        django_get_or_create = ('name',)

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
    inst_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.InstFactory")
    instdc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.InstdcFactory")
    det_value = factory.lazy_attribute(lambda o: faker.random_int(10, 20))
    start_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='-30y', end_date='today'))
    end_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='today', end_date='+30y'))
    valid = True
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
            'inst_id': inst.pk,
            'instdc_id': instdc.pk,
            'det_value': obj.det_value,
            'start_date': obj.start_date,
            'end_date': obj.end_date,
            'valid': True,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class InstdcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.InstDetCode
        django_get_or_create = ('name',)

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
    loc_lat = factory.lazy_attribute(lambda o: faker.random_int(1, 90))
    loc_lon = factory.lazy_attribute(lambda o: faker.random_int(1, 90))
    loc_date = factory.lazy_attribute(lambda o: faker.date_time(tzinfo=pytz.UTC))
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
            'start_date': obj.loc_date.date(),
            'loc_date': obj.loc_date.date(),
            'start_time': obj.loc_date.time().strftime("%H:%M"),
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class LoccFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LocCode
        django_get_or_create = ('name',)

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
        django_get_or_create = ('name',)

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


class PairFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Pairing

    indv_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.IndvFactory")
    prio_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.PrioFactory")
    pair_prio_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.PrioFactory")
    start_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='-30y', end_date='today'))
    end_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='today', end_date='+30y'))
    cross = factory.lazy_attribute(lambda o: faker.random_int(1, 10))
    valid = True
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        indv = IndvFactory()
        prio = PrioFactory()
        pair_prio = PrioFactory()
        obj = PairFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'indv_id': indv.pk,
            'prio_id': prio.pk,
            'pair_prio_id': pair_prio.pk,
            'start_date': obj.start_date,
            'end_date': obj.end_date,
            'cross': obj.cross,
            'valid': True,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class PercFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PersonnelCode

    perc_first_name = factory.lazy_attribute(lambda o: faker.word())
    perc_last_name = factory.lazy_attribute(lambda o: faker.word())
    perc_valid = True
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        obj = PercFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'perc_first_name': obj.perc_first_name,
            'perc_last_name': obj.perc_last_name,
            'perc_valid': True,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class PrioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PriorityCode
        django_get_or_create = ('name',)

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
        django_get_or_create = ('prog_name',)

    prog_name = factory.lazy_attribute(lambda o: faker.word())
    prog_desc = factory.lazy_attribute(lambda o: faker.text())
    proga_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ProgaFactory")
    orga_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.OrgaFactory")
    start_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='-30y', end_date='today'))
    end_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='today', end_date='+30y'))
    valid = True
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
            'valid': True,
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
    evntc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.EvntcFactory")
    facic_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.FacicFactory")
    name = factory.lazy_attribute(lambda o: faker.word())
    prot_desc = factory.lazy_attribute(lambda o: faker.text())
    start_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='-30y', end_date='today'))
    end_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='today', end_date='+30y'))
    valid = True
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        prog = ProgFactory()
        protc = ProtcFactory()
        evntc = EvntcFactory()
        facic = FacicFactory()
        obj = ProtFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'prog_id': prog.pk,
            'protc_id': protc.pk,
            'evntc_id': evntc.pk,
            'facic_id': facic.pk,
            'name': obj.name,
            'prot_desc': obj.prot_desc,
            'start_date': obj.start_date,
            'end_date': obj.end_date,
            'valid': True,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class ProtcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProtoCode
        django_get_or_create = ('name',)

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
        django_get_or_create = ('name',)

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
        django_get_or_create = ('name',)

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    rive_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.RiveFactory")
    trib_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.TribFactory")
    subr_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.SubrFactory")
    min_lat = factory.lazy_attribute(lambda o: faker.random_int(1, 90))
    max_lat = factory.lazy_attribute(lambda o: faker.random_int(1, 90))
    min_lon = factory.lazy_attribute(lambda o: faker.random_int(1, 90))
    max_lon = factory.lazy_attribute(lambda o: faker.random_int(1, 90))

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
        django_get_or_create = ('name',)

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
        django_get_or_create = ('name',)

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
    samp_num = factory.lazy_attribute(lambda o: faker.random_int(1, 100))
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
        django_get_or_create = ('name',)

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
    det_val = factory.lazy_attribute(lambda o: faker.random_int(10, 20))
    adsc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.AdscFactory")
    qual_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.QualFactory")
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):

        samp = SampFactory()
        adsc = AdscFactory()
        qual = QualFactory()
        anidc = AnidcFactory()
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


class SireFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Sire

    prio_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.PrioFactory")
    pair_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.PairFactory")
    indv_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.IndvFactory")
    choice = factory.lazy_attribute(lambda o: faker.random_int(1, 10))
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        prio = PrioFactory()
        pair = PairFactory()
        indv = IndvFactory()
        obj = SireFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'prio_id': prio.pk,
            'pair_id': pair.pk,
            'indv_id': indv.pk,
            'choice': obj.choice,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class SpwndFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SpawnDet

    pair_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.PairFactory")
    spwndc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.SpwndcFactory")
    spwnsc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.SpwnscFactory")
    qual_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.QualFactory")
    det_val = factory.lazy_attribute(lambda o: faker.random_int(10, 20))
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        pair = PairFactory()
        spwnsc = SpwnscFactory()
        qual = QualFactory()
        obj = SpwndFactory.build(**kwargs)
        spwndc = SpwndcFactory()

        # Convert the data to a dictionary to be used in testing
        data = {
            'pair_id': pair.pk,
            'spwndc_id': spwndc.pk,
            'spwnsc_id': spwnsc.pk,
            'qual_id': qual.pk,
            'det_val': obj.det_val,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class SpwndcFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SpawnDetCode
        django_get_or_create = ('name',)

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    min_val = factory.lazy_attribute(lambda o: faker.random_int(0, 10))
    max_val = factory.lazy_attribute(lambda o: faker.random_int(20, 30))
    unit_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.UnitFactory")
    spwn_subj_flag = factory.lazy_attribute(lambda o: faker.boolean())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        unit = UnitFactory()
        obj = SpwndcFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'min_val': obj.min_val,
            'max_val': obj.max_val,
            'unit_id': unit.pk,
            'spwn_subj_flag': obj.spwn_subj_flag,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class SpwnscFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SpawnDetSubjCode
        django_get_or_create = ('name',)

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    spwndc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.SpwndcFactory")
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        spwndc = SpwndcFactory()
        obj = SpwnscFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'spwndc_id': spwndc.pk,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class SpecFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SpeciesCode
        django_get_or_create = ('name',)

    name = factory.lazy_attribute(lambda o: faker.text(max_nb_chars=10))
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
        django_get_or_create = ('name',)

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
        django_get_or_create = ('name',)

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
        django_get_or_create = ('name',)

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    facic_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.FacicFactory")
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        facic = FacicFactory()
        obj = TankFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'facic_id': facic.pk,
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

    det_value = factory.lazy_attribute(lambda o: faker.random_int(10, 20))
    cdsc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.CdscFactory")
    start_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='-30y', end_date='today'))
    end_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='today', end_date='+30y'))
    det_valid = True
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        tank = TankFactory()
        cdsc = CdscFactory()
        contdc = ContdcFactory()
        obj = TankdFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'contdc_id': contdc.pk,
            'tank_id': tank.pk,
            'det_value': obj.det_value,
            'cdsc_id': cdsc.pk,
            'start_date': obj.start_date,
            'end_date': obj.end_date,
            'det_valid': True,
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
        django_get_or_create = ('name',)

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    trof_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.TrofFactory")
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    start_date = factory.lazy_attribute(lambda o: faker.date())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        trof = TrofFactory()
        obj = TrayFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'trof_id': trof.pk,
            'description_en': obj.description_en,
            'description_fr': obj.description_fr,
            'start_date' : obj.start_date,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class TraydFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TrayDet

    contdc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.ContdcFactory")
    tray_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.TrayFactory")

    det_value = factory.lazy_attribute(lambda o: faker.random_int(10, 20))
    cdsc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.CdscFactory")
    start_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='-30y', end_date='today'))
    end_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='today', end_date='+30y'))
    det_valid = True
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        tray = TrayFactory()
        cdsc = CdscFactory()
        contdc = ContdcFactory()
        obj = TraydFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'contdc_id': contdc.pk,
            'tray_id': tray.pk,
            'det_value': obj.det_value,
            'cdsc_id': cdsc.pk,
            'start_date': obj.start_date,
            'end_date': obj.end_date,
            'det_valid': True,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class TribFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tributary
        django_get_or_create = ('name',)

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
        django_get_or_create = ('name',)

    name = factory.lazy_attribute(lambda o: faker.word())
    nom = factory.lazy_attribute(lambda o: faker.word())
    facic_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.FacicFactory")
    description_en = factory.lazy_attribute(lambda o: faker.text())
    description_fr = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        facic = FacicFactory()
        obj = TrofFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'name': obj.name,
            'nom': obj.nom,
            'facic_id': facic.pk,
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

    det_value = factory.lazy_attribute(lambda o: faker.random_int(10, 20))
    cdsc_id = factory.SubFactory("bio_diversity.test.BioFactoryFloor.CdscFactory")
    start_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='-30y', end_date='today'))
    end_date = factory.lazy_attribute(lambda o: faker.date_between(start_date='today', end_date='+30y'))
    det_valid = True
    comments = factory.lazy_attribute(lambda o: faker.text())
    created_by = factory.lazy_attribute(lambda o: faker.name())
    created_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def build_valid_data(**kwargs):
        trof = TrofFactory()
        cdsc = CdscFactory()
        contdc = ContdcFactory()
        obj = TrofdFactory.build(**kwargs)

        # Convert the data to a dictionary to be used in testing
        data = {
            'contdc_id': contdc.pk,
            'trof_id': trof.pk,
            'det_value': obj.det_value,
            'cdsc_id': cdsc.pk,
            'start_date': obj.start_date,
            'end_date': obj.end_date,
            'det_valid': True,
            'comments': obj.comments,
            'created_by': obj.created_by,
            'created_date': obj.created_date,
        }

        return data


class UnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.UnitCode
        django_get_or_create = ('name',)

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
