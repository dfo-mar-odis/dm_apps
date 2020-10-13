from django.test import TestCase, tag
from django.core.files.base import ContentFile
from django.utils.six import BytesIO
from django.conf import settings

from PIL import Image

from whalesdb import models
from whalesdb.test import WhalesdbFactoryFloor as Factory

import os


class TestDep(TestCase):
    fixtures = ['initial_whale_data.json']

    @tag('dep', 'model', 'dep_model')
    def test_dep_station_events(self):
        dep = Factory.DepFactory()
        set = models.SetStationEventCode.objects.get(pk=1)

        self.assertEquals(dep.station_events.count(), 0)

        ste = Factory.SteFactory(dep=dep, set_type=set)

        self.assertEquals(dep.station_events.count(), 1)
        self.assertEquals(dep.station_events.first().dep, dep)
        self.assertEquals(dep.station_events.first().set_type, set)

class TestEmm(TestCase):

    fixtures = ['initial_whale_data.json']

    def setup(self):
        pass

    # Make and model objects if eqt_id == 4 are hydrophone equipment and have a one to one entry in the
    # EqhHydrophoneProperties table. The Eqh table has a related name on the emm object
    @tag('emm', 'model', 'emm_model')
    def test_emm_eqh_hydrophones(self):
        eqt = models.EqtEquipmentTypeCode.objects.get(pk=4)
        emm = Factory.EmmFactory(eqt=eqt)
        # create an Eqh object from the factory, in theory it should share the emm object
        # when emm.hydrophone is called there should be a single matching entry
        eqh = Factory.EqhFactory(emm=emm)

        hydrophone = emm.hydrophone
        self.assertEquals(eqh, hydrophone)

    # When a make and model is eqt_id == 1 it is a recorder type and channels should be accessable through the
    # related name emm.channels
    @tag('emm', 'model', 'emm_model')
    def test_emm_ecp_channels(self):
        eqt = models.EqtEquipmentTypeCode.objects.get(pk=1)
        emm = Factory.EmmFactory(eqt=eqt)

        eqr = Factory.EqrFactory(emm=emm)
        ecp1 = Factory.EcpFactory(eqr=eqr, ecp_channel_no=1)
        ecp2 = Factory.EcpFactory(eqr=eqr, ecp_channel_no=2)

        recorder = emm.recorder
        self.assertEquals(eqr, recorder)

        channels = recorder.channels.all()
        self.assertEquals(2, channels.count())

        self.assertIn(ecp1, channels)
        self.assertIn(ecp2, channels)


# The EDA table connects equipment to deployments. This can be used from deployments to see what equipment is
# currently attached to a deployment, what equipment was previously attached to a deployment or the reverse to see
# what deployment a piece of equipment was or is attached to. This doesn't need to be tested directly, but
# the relationships for dep.attachements and eqp.deploymnets if the page ends up broken because of a model change
# the test should explain why.
class TestEdaEquipmentAttachment(TestCase):

    fixtures = ['initial_whale_data.json']

    def setUp(self) -> None:
        pass

    @tag('dep', 'eqp', 'eda', 'relationship')
    def test_eda_relationship(self):
        emm = Factory.EmmFactory(pk=1)
        eqp = Factory.EqpFactory(emm=emm)
        dep_1 = Factory.DepFactory()
        dep_2 = Factory.DepFactory()

        eda = Factory.EdaFactory(eqp=eqp, dep=dep_1)

        self.assertEquals(1, dep_1.attachments.all().count())
        self.assertEquals(1, eqp.deployments.all().count())
        self.assertEquals(dep_1, eqp.deployments.all().last().dep)

        eda = Factory.EdaFactory(eqp=eqp, dep=dep_2)

        self.assertEquals(1, dep_2.attachments.all().count())
        self.assertEquals(2, eqp.deployments.all().count())
        self.assertEquals(dep_2, eqp.deployments.all().last().dep)


class TestMorMooringSetup(TestCase):

    def setUp(self) -> None:
        pass

    def test_create_mor(self):

        img_file_name = "MooringSetupTest.png"
        img_file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + img_file_name

        data = BytesIO()
        Image.open(img_file_path).save(data, "PNG")
        data.seek(0)
        file = ContentFile(data.read(), img_file_name)

        self.mooring_dic = {}

        mor_1 = models.MorMooringSetup(mor_name="MOR001", mor_max_depth=100,
                                       mor_link_setup_image="https://somelink.com", mor_setup_image=file)
        mor_1.save()

        # Check that the file was saved
        expected_path = os.path.join(settings.MEDIA_DIR, "whalesdb", "mooring_setup", img_file_name)
        self.assertTrue(os.path.exists(expected_path))
        self.assertTrue(os.path.isfile(expected_path))

        # Delete the image
        mor_1.delete()

        self.assertFalse(os.path.exists(expected_path))


class TestRstRecordingStage(TestCase):

    def setUp(self) -> None:
        pass

    @tag('rst', 'rsc', 'relationship')
    def test_rst_relationship(self):
        rsc = Factory.RscFactory()
        rst = Factory.RstFactory(rsc=rsc)

        self.assertEquals(1, rsc.stages.count())