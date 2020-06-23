from whalesdb import models

import os


def load_prj(file_name):
    file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + file_name
    model = models.PrjProject
    print("file: " + file_path)

    file = open(file_path, "r")
    first = True
    for line in file:
        if first:
            first = False
            continue

        data = line.strip().split(',')
        if not model.objects.filter(name=data[0]):
            try:
                model(name=data[0],
                      description_en=(None if data[1] == '' else data[1]),
                      prj_url=(None if data[2] == '' else data[2])).save()
            except:
                print("Could not load project: " + str(data))


def load_rtt(file_name):
    file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + file_name
    model = models.RttTimezoneCode
    print("file: " + file_path)

    file = open(file_path, "r")
    first = True
    for line in file:
        if first:
            first = False
            continue

        data = line.strip().split(',')
        if not model.objects.filter(rtt_abb=data[0]):
            print(str(data))
            model(rtt_abb=data[0],
                  rtt_name=(None if data[1] == '' else data[1]),
                  rtt_offset=(None if data[2] == '' else data[2])).save()


def load_set(file_name):
    file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + file_name
    model = models.SetStationEventCode
    print("file: " + file_path)

    file = open(file_path, "r")
    first = True
    for line in file:
        if first:
            first = False
            continue

        data = line.strip().split(',')
        if not model.objects.filter(name=data[0]):
            model(name=data[0],
                  description_en=(None if data[1] == '' else data[1])).save()


def load_stn(file_name):
    file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + file_name
    model = models.StnStation
    print("file: " + file_path)

    file = open(file_path, "r")
    first = True
    for line in file:
        if first:
            first = False
            continue

        data = line.strip().split(',')
        if not model.objects.filter(stn_name=data[0], stn_revision=data[2]):
            print(str(data))
            # Ignore data[3]
            # We were going to use a stn_status column to indicate 'past' and 'current' stations
            # but since the current station is always the one with the highest revision number
            # we figured it would cut down on potiential errors to exclude the status, which will
            # be easier to add in later.

            model(stn_name=data[0],
                  stn_code=(None if data[1] == '' else data[1]),
                  stn_revision=(None if data[2] == '' else data[2]),
                  stn_planned_lat=(None if data[4] == '' else data[4]),
                  stn_planned_lon=(None if data[5] == '' else data[5]),
                  stn_planned_depth=(None if data[6] == '' else data[6]),
                  stn_notes=(None if data[7] == '' else data[7])).save()


def load_tea(file_name):
    file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + file_name
    model = models.TeaTeamMember
    print("file: " + file_path)

    file = open(file_path, "r")
    first = True
    for line in file:
        if first:
            first = False
            continue

        data = line.strip().split(',')
        if not model.objects.filter(tea_last_name=data[1], tea_first_name=data[2]):
            model(tea_abb=data[0],
                  tea_last_name=data[1],
                  tea_first_name=data[2]).save()


def load_eqt(file_name):
    file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + file_name
    model = models.EqtEquipmentTypeCode
    print("file: " + file_path)

    file = open(file_path, "r")
    first = True
    for line in file:
        if first:
            first = False
            continue

        data = line.strip().split(',')
        if not model.objects.filter(eqt_name=data[0]):
            model(eqt_name=data[0]).save()


def load_eqa(file_name):
    file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + file_name
    model = models.EqaAdcBitsCode
    print("file: " + file_path)

    file = open(file_path, "r")
    first = True
    for line in file:
        if first:
            first = False
            continue

        data = line.strip().split(',')
        if not model.objects.filter(eqa_name=data[0]):
            model(eqa_name=data[0]).save()


def load_ret(file_name):
    file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + file_name
    model = models.RetRecordingEventType
    print("file: " + file_path)

    file = open(file_path, "r")
    first = True
    for line in file:
        if first:
            first = False
            continue

        data = line.strip().split(',')
        if not model.objects.filter(ret_name=data[0]):
            model(ret_name=data[0], ret_desc=data[1]).save()


def load_ret(file_name):
    file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + file_name
    model = models.EqoOwner
    print("file: " + file_path)

    file = open(file_path, "r")
    first = True
    for line in file:
        if first:
            first = False
            continue

        data = line.strip().split(',')
        if not model.objects.filter(eqo_institute=data[0]):
            model(eqo_institute=data[0]).save()


def load_prm(file_name):
    file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + file_name
    model = models.PrmParameterCode
    print("file: " + file_path)

    file = open(file_path, "r")
    first = True
    for line in file:
        if first:
            first = False
            continue

        data = line.strip().split(',')
        if not model.objects.filter(prm_name=data[0]):
            print(str(data))
            model(prm_name=data[0]).save()


def load_emm(file_name):
    file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + file_name
    model = models.EmmMakeModel
    print("file: " + file_path)

    file = open(file_path, "r")
    first = True
    for line in file:
        if first:
            first = False
            continue

        data = line.strip().split(',')
        if not model.objects.filter(emm_make=data[0], emm_model=data[1]):
            print(str(data))
            emm_make = data[0]
            emm_model = data[1]
            emm_depth_rating = data[2] if data[2] else 0
            emm_description = data[3]

            if not models.EqtEquipmentTypeCode.objects.filter(eqt_name=data[4]):
                print("Eqt '" + data[4] + "' was not found, making it")
                models.EqtEquipmentTypeCode(eqt_name=data[4]).save()

            eqt_type = models.EqtEquipmentTypeCode.objects.get(eqt_name=data[4])
            print(eqt_type)

            model(emm_make=emm_make, emm_model=emm_model, emm_depth_rating=emm_depth_rating,
                  emm_description=emm_description, eqt=eqt_type).save()

            try:
                emm = model.objects.get(emm_make=emm_make, emm_model=emm_model)

                if data[5]:
                    if not models.PrmParameterCode.objects.filter(prm_name=data[5]):
                        models.PrmParameterCode(prm_name=data[5]).save()

                    prm = models.PrmParameterCode.objects.get(prm_name=data[5])
                    models.EprEquipmentParameter(emm=emm, prm=prm).save()
                    print("prams added to '" + str(emm) + "'")

                if eqt_type.eqt_name == 'Acoustic recorder':
                    sub_type = data[6]
                    internal_hydro = data[7] is 'yes'

                    if not models.ErtRecorderType.objects.filter(ert_name=sub_type):
                        models.ErtRecorderType(ert_name=sub_type).save()

                    st = models.ErtRecorderType.objects.get(ert_name=sub_type)

                    models.EqrRecorderProperties(emm=emm, ert=st, eqr_internal_hydro=internal_hydro).save()

                    eqr = models.EqrRecorderProperties.objects.get(emm=emm)
                    print("Created Recorder Properties for: '" + str(eqr) + "'")
            except models.PrmParameterCode.DoesNotExist:
                print("Could not add parameter '" + data[4] + "' to equipment '" + str(emm) + "'")


def load_ecp(file_name):
    file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + file_name
    model = models.EcpChannelProperty
    print("file: " + file_path)

    file = open(file_path, "r")
    first = True
    for line in file:
        if first:
            first = False
            continue

        data = line.strip().split(',')
        try:
            emm_make = data[0]
            emm_model = data[1]

            emm = models.EmmMakeModel.objects.get(emm_make=emm_make, emm_model=emm_model)

            try:
                eqr = models.EqrRecorderProperties.objects.get(emm=emm)

                if not model.objects.filter(eqr=eqr, ecp_channel_no=data[2]):
                    print(str(data))

                    ecp_channel_no = data[2]
                    eqa_adc_bits = models.EqaAdcBitsCode.objects.get(eqa_name=(data[3] + "-bit"))
                    ecp_voltage_range_min = data[4] if data[4] else None
                    ecp_voltage_range_max = data[5] if data[5] else None

                    print("Setting Channel properties for '" + str(eqr) + "'")
                    models.EcpChannelProperty(eqr=eqr, ecp_channel_no=ecp_channel_no, eqa_adc_bits=eqa_adc_bits,
                                              ecp_voltage_range_min=ecp_voltage_range_min,
                                              ecp_voltage_range_max=ecp_voltage_range_max).save()
            except models.EqrRecorderProperties.DoesNotExist:
                print("no recorder matching emm: '" + str(emm) + "'")
        except models.EmmMakeModel.DoesNotExist:
            print("Could not find make/model '" + data[0] + "/" + data[1] + "'")


load_prj("PRJ-projects.csv")
load_rtt("RTT-timezone types.csv")
load_set("SET-station event types.csv")
load_stn("STN-stations.csv")
load_tea("TEA-team members.csv")
load_eqa("EQA-ADC bits.csv")
load_prm("PRM-parameter types.csv")
load_eqt("EQT-equipment types.csv")

load_emm("EMM-equipment make model.csv")
load_ecp("ECP-channel properties.csv")
