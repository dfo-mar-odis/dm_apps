import factory
from faker import Factory

from whalesdb import models
from shared_models import models as shared_models

_stn_codes_ = ['ABC', 'DEF', 'GHI', 'JKL', 'MNO', 'PQR', 'STU', 'VWX', 'YZZ']
_set_codes_ = ['Deployment', 'Recovery']
_eqt_codes_ = ['Acoustic recorder', 'Environmental sensor', 'OTN reciever', 'Hydrophone']

faker = Factory.create()


class EmmFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EmmMakeModel

    eqt = factory.lazy_attribute(lambda o: models.EqtEquipmentTypeCode.objects.get(pk=faker.random_int(1, 4)))
    emm_make = factory.lazy_attribute(lambda o: faker.word())
    emm_model = factory.lazy_attribute(lambda o: faker.word())
    emm_depth_rating = factory.lazy_attribute(lambda o: faker.random_int(10, 10000))
    emm_description = factory.lazy_attribute(lambda o: faker.text())

    # if providing an eqt_type use the WhalesdbFactory._eqt_type_codes array
    @staticmethod
    def get_valid_data(eqt_id=None):

        eqt_id = eqt_id if eqt_id else faker.random_int(1, 4)
        eqt = models.EqtEquipmentTypeCode.objects.get(pk=eqt_id)

        valid_data = {
            'eqt': eqt.pk,
            'emm_make': faker.word(),
            'emm_model': faker.word(),
            'emm_depth_rating': faker.random_int(10, 10000),
            'emm_description': faker.text()
        }

        return valid_data


class EqhFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EqhHydrophoneProperty

    emm = factory.lazy_attribute(lambda o: EmmFactory(pk=4))
    eqh_range_min = factory.lazy_attribute(lambda o: faker.random_int(0, 100))
    eqh_range_max = factory.lazy_attribute(lambda o: faker.random_int(100, 1000))

    @staticmethod
    def get_valid_data():
        # specifically testing when an equipment is a Hydrophone
        eqt = models.EqtEquipmentTypeCode.objects.get(pk=4)
        emm = EmmFactory(eqt=eqt)

        valid_data = {
            'emm': emm.pk,
            'eqh_range_min': faker.random_int(0, 100),
            'eqh_range_max': faker.random_int(100, 1000)
        }

        return valid_data


class EqrFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EqrRecorderProperties

    emm = factory.SubFactory(EmmFactory)
    ert = factory.lazy_attribute(lambda o: models.ErtRecorderType.objects.get(pk=faker.random_int(1, 4)))
    eqr_internal_hydro = factory.lazy_attribute(lambda o: faker.boolean())

    @staticmethod
    def get_valid_data():
        # specifically testing when an equipment is an Acoustic Recorder
        eqt = models.EqtEquipmentTypeCode.objects.get(pk=1)
        emm = EmmFactory(eqt=eqt)

        valid_data = {
            'emm': emm.pk,
            'ert': faker.random_int(1, 4),
            'eqr_internal_hydro': faker.boolean()
        }

        return valid_data


class EcpFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EcpChannelProperty

    eqr = factory.SubFactory(EqrFactory)
    ecp_channel_no = factory.lazy_attribute(lambda o: faker.random_int(1, 9))
    eqa_adc_bits = factory.lazy_attribute(lambda o: models.EqaAdcBitsCode.objects.get(pk=faker.random_int(1, 3)))
    ecp_voltage_range_min = factory.lazy_attribute(lambda o: faker.random_int(1, 1000))
    ecp_voltage_range_max = factory.lazy_attribute(lambda o: o.ecp_voltage_range_min + faker.random_int(1, 1000))

    @staticmethod
    def get_valid_data():
        # specifically testing when an equipment is an Acoustic Recorder
        eqr = EqrFactory()
        min_volt = faker.random_int(1, 1000)
        valid_data = {
            'eqr':  eqr.pk,
            'ecp_channel_no':  faker.random_int(1, 9),
            'eqa_adc_bits':  models.EqaAdcBitsCode.objects.get(pk=faker.random_int(1, 3)),
            'ecp_voltage_range_min':  min_volt,
            'ecp_voltage_range_max':  min_volt + faker.random_int(1, 1000),
        }

        return valid_data


class EqoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EqoOwner


class EqpFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EqpEquipment

    emm = factory.SubFactory(EmmFactory)
    eqp_serial = factory.lazy_attribute(lambda o: faker.random_int(1, 1000000000))
    eqp_asset_id = factory.Sequence(lambda n: "DFO-{}".format(faker.random_int(9000000, 9999999)))
    eqp_date_purchase = factory.lazy_attribute(lambda o: faker.date())
    eqp_notes = factory.lazy_attribute(lambda o: faker.text())
    eqp_retired = factory.lazy_attribute(lambda o: faker.boolean())
    eqo_owned_by = factory.SubFactory(EqoFactory)

    @staticmethod
    def get_valid_data():

        emm = EmmFactory()
        eqo = EqoFactory()

        valid_data = {
            "emm": emm.pk,
            'eqp_serial': faker.random_int(1, 1000000000),
            'eqp_asset_id': "DFO-{}".format(faker.random_int(9000000, 9999999)),
            'eqp_date_purchase': faker.date(),
            'eqp_notes': faker.text(),
            'eqp_retired': faker.boolean(),
            'eqo_owned_by': eqo.pk
        }

        return valid_data


class MorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MorMooringSetup
        django_get_or_create = ('mor_name',)

    mor_name = factory.lazy_attribute(lambda o: faker.name())
    mor_max_depth = factory.lazy_attribute(lambda o: faker.random_int(0, 1000))
    mor_link_setup_image = factory.lazy_attribute(lambda o: faker.url())
    mor_additional_equipment = factory.lazy_attribute(lambda o: faker.sentence())
    mor_general_moor_description = factory.lazy_attribute(lambda o: faker.text())
    mor_notes = factory.lazy_attribute(lambda o: faker.text())

    @staticmethod
    def get_valid_data():
        valid_data = {
            "mor_name": faker.name(),
            "mor_max_depth": faker.random_int(0, 1000),

            "mor_link_setup_image": faker.url(),
            "mor_additional_equipment": faker.sentence(),
            "mor_general_moor_description": faker.text(),
            "mor_notes": faker.text()
        }

        return valid_data


class PrjFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PrjProject
        django_get_or_create = ('name',)

    name = factory.lazy_attribute(lambda o: faker.name())
    description_en = factory.lazy_attribute(lambda o: faker.text())
    prj_url = factory.lazy_attribute(lambda o: faker.url())

    @staticmethod
    def get_valid_data():
        valid_data = {
            "name": faker.name(),
            "description_en": faker.text(),
            "prj_url": faker.url()
        }

        return valid_data


class StnFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.StnStation
        django_get_or_create = ('stn_code',)

    stn_name = factory.lazy_attribute(lambda o: faker.name())
    stn_code = factory.Iterator(_stn_codes_)
    stn_revision = 1
    stn_planned_lat = factory.lazy_attribute(lambda o: faker.pydecimal(left_digits=2, right_digits=5))
    stn_planned_lon = factory.lazy_attribute(lambda o: faker.pydecimal(left_digits=2, right_digits=5))
    stn_planned_depth = factory.lazy_attribute(lambda o: faker.random_int(0, 1000))
    stn_notes = factory.lazy_attribute(lambda o: faker.text())

    @staticmethod
    def get_valid_data():

        valid_data = {
            "stn_name": faker.name(),
            "stn_code": _stn_codes_[faker.random_int(0, len(_stn_codes_)-1)],
            "stn_revision": 1,
            "stn_planned_lat": faker.pydecimal(left_digits=2, right_digits=5),
            "stn_planned_lon": faker.pydecimal(left_digits=2, right_digits=5),
            "stn_planned_depth": faker.random_int(0, 1000),
            "stn_notes": faker.text()
        }

        return valid_data


class DepFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.DepDeployment
        django_get_or_create = ("stn", "prj", "mor", "dep_name",)

    stn = factory.SubFactory(StnFactory)
    prj = factory.SubFactory(PrjFactory)
    mor = factory.SubFactory(MorFactory)
    dep_year = factory.lazy_attribute(lambda o: faker.random_int(1980, 2060))
    dep_month = factory.lazy_attribute(lambda o: faker.random_int(1, 12))
    dep_name = "{}-{}-{}".format(
        factory.LazyAttribute(lambda o: o.stn_code),
        factory.LazyAttribute(lambda o: o.dep_year),
        factory.LazyAttribute(lambda o: o.dep_month)
    )

    @staticmethod
    def get_valid_data():

        stn = StnFactory()
        prj = PrjFactory()
        mor = MorFactory()
        year = faker.random_int(1980, 2060)
        month = faker.random_int(1, 12)
        valid_data = {
            'stn': stn.pk,
            'dep_year': year,
            'dep_month': month,
            'dep_name': "{}-{}-{}".format(stn.stn_code, year, month),
            'prj': prj.pk,
            'mor': mor.pk,
        }

        return valid_data


class CruiseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = shared_models.Cruise


class SteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SteStationEvent

    dep = factory.SubFactory(DepFactory)
    set_type = factory.lazy_attribute(lambda o: models.SetStationEventCode.objects.all()[
        faker.random_int(0, models.SetStationEventCode.objects.count() - 1)])

    crs = factory.SubFactory(CruiseFactory)
    ste_date = factory.lazy_attribute(lambda o: faker.date())

    @staticmethod
    def get_valid_data():

        dep = DepFactory()
        crs = CruiseFactory()
        ste = SteFactory.build()

        valid_data = {
            "dep": dep.pk,
            "set_type": ste.set_type.pk,
            "crs": crs.pk,
            "ste_date": ste.ste_date
        }

        return valid_data


class EdaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EdaEquipmentAttachment

    dep = factory.SubFactory(DepFactory)
    eqp = factory.SubFactory(EqpFactory)

    @staticmethod
    def get_valid_data():
        dep = DepFactory()

        # Eda will only show recorders, so no hydrophones here
        emm = EmmFactory(pk=1)
        eqp = EqpFactory(emm=emm)

        valid_data = {
            "dep": dep.pk,
            "eqp": eqp.pk
        }

        return valid_data


class RscFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.RscRecordingSchedule

    rsc_name = factory.lazy_attribute(lambda o: faker.word())
    rsc_period = factory.lazy_attribute(lambda o: faker.random_int(1, 1000000))

    @staticmethod
    def get_valid_data():

        valid_data = {
            "rsc_name": faker.word(),
            "rsc_period": faker.random_int(1, 1000000)
        }

        return valid_data


class RstFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.RstRecordingStage

    rst_channel_no = factory.lazy_attribute(lambda o: faker.random_int(0, 9))
    rsc = factory.SubFactory(RscFactory)
    rst_active = factory.lazy_attribute(lambda o: faker.random_element(elements=("A", "S")))
    rst_duration = factory.lazy_attribute(lambda o: faker.random_int(0, 10000))
    rst_rate = factory.lazy_attribute(lambda o: faker.pyfloat(left_digits=5, right_digits=2))

    @staticmethod
    def get_valid_data():

        rsc = RscFactory()

        valid_data = {
            "rst_channel_no": faker.random_int(0, 9),
            "rsc": rsc.pk,
            "rst_active": faker.random_element(elements=("A", "S")),
            "rst_duration": faker.random_int(0, 10000),
            "rst_rate": faker.pyfloat(left_digits=5, right_digits=2)
        }

        return valid_data


class RttFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.RttTimezoneCode

    rtt_abb = factory.lazy_attribute(lambda o: faker.word()[0:5])
    rtt_name = factory.lazy_attribute(lambda o: faker.word())
    rtt_offset = factory.lazy_attribute(lambda o: faker.random_int(-12, 12))

    @staticmethod
    def get_valid_data():
        valid_data = {
            'rtt_name': faker.word(),
            'rtt_abb': 'ASDFG',
            'rtt_offset': faker.random_int(-12, 12)
        }

        return valid_data


class RecFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.RecDataset

    eda_id = factory.SubFactory(EdaFactory)
    rsc_id = factory.SubFactory(RscFactory)
    rtt_in_water = factory.SubFactory(RttFactory)
    rtt_dataset = factory.SubFactory(RttFactory)

    @staticmethod
    def get_valid_data():

        eda_id = EdaFactory()
        rsc_id = RscFactory()
        rtt_in_water = RttFactory()
        rtt_dataset = RttFactory()

        valid_data = {
            'eda_id': eda_id.pk,
            'rsc_id': rsc_id.pk,
            'rtt_in_water': rtt_in_water.pk,
            'rtt_dataset': rtt_dataset.pk
        }

        return valid_data


class RciFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.RciChannelInfo

    rec_id = factory.SubFactory(RecFactory)
    rci_name = factory.lazy_attribute(lambda o: faker.word())
    rci_size = factory.lazy_attribute(lambda o: faker.random_int(0, 12))
    rci_gain = factory.lazy_attribute(lambda o: faker.random_int(0, 12))
    rci_volts = factory.lazy_attribute(lambda o: faker.pyfloat(left_digits=3, right_digits=1))

    @staticmethod
    def get_valid_data():

        rec = RecFactory()
        valid_data = {
            "rec_id": rec.pk,
            "rci_name": faker.word(),
            "rci_size": faker.random_int(0, 12),
            "rci_gain": faker.random_int(0, 12),
            "rci_volts": faker.pyfloat(left_digits=3, right_digits=1)
        }

        return valid_data


class TeaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TeaTeamMember

    tea_abb = factory.lazy_attribute(lambda o: faker.word())
    tea_last_name = factory.lazy_attribute(lambda o: faker.word())
    tea_first_name = factory.lazy_attribute(lambda o: faker.word())

    @staticmethod
    def get_valid_data():

        valid_data = {
            "tea_abb": faker.word(),
            "tea_last_name": faker.word(),
            "tea_first_name": faker.word(),
        }

        return valid_data


class ReeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ReeRecordingEvent

    rec_id = factory.SubFactory(RecFactory)
    ret_id = factory.lazy_attribute(lambda o: models.RetRecordingEventType.objects.get(pk=faker.random_int(1, 6)))
    rtt_id = factory.SubFactory(RttFactory)
    ree_date = factory.lazy_attribute(lambda o: faker.date())
    ree_time = factory.lazy_attribute(lambda o: faker.time())
    tea_id = factory.SubFactory(TeaFactory)

    @staticmethod
    def get_valid_data():
        rec = RecFactory()
        ret = models.RetRecordingEventType.objects.get(pk=faker.random_int(1, 6))
        rtt = RttFactory()
        tea = TeaFactory()

        valid_data = {
            'rec_id': rec.pk,
            'ret_id': ret.pk,
            'rtt_id': rtt.pk,
            'ree_date': faker.date(),
            'ree_time': faker.time(),
            'tea_id': tea.pk
        }

        return valid_data
