import datetime
import math

import pytz
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone

from bio_diversity import models


def bio_diverisity_authorized(user):
    # return user.is_user and user.groups.filter(name='bio_diversity_user').exists()
    return user.groups.filter(name='bio_diversity_user').exists() or bio_diverisity_admin(user)


def bio_diverisity_admin(user):
    # return user.is_authenticated and user.groups.filter(name='bio_diversity_admin').exists()
    return user.groups.filter(name='bio_diversity_admin').exists()


def get_comment_keywords_dict():
    my_dict = {}
    for obj in models.CommentKeywords.objects.all():
        my_dict[obj.keyword] = obj.adsc_id
    return my_dict


def get_help_text_dict(model=None):
    my_dict = {}
    if not model:
        for obj in models.HelpText.objects.all():
            my_dict[obj.field_name] = str(obj)
    else:
        # If a model is supplied get the fields specific to that model
        for obj in models.HelpText.objects.filter(model=str(model.__name__)):
            my_dict[obj.field_name] = str(obj)

    return my_dict


def year_coll_splitter(full_str):
    coll = full_str.lstrip(' 0123456789')
    year = int(full_str[:len(full_str) - len(coll)])
    return year, coll.strip()


def val_unit_splitter(full_str):
    unit_str = full_str.lstrip(' 0123456789.')
    val = float(full_str[:len(full_str) - len(unit_str)])
    return val, unit_str.strip()


def get_cont_evnt(contx_tuple):
    # input should be in the form (contx, bool/null)
    contx = contx_tuple[0]
    in_out_dict = {None: "", False: "Origin", True: "Destination"}
    output_list = [contx.evnt_id.evntc_id.__str__(), contx.evnt_id.start_date, in_out_dict[contx_tuple[1]]]
    for cont in [contx.tank_id, contx.cup_id, contx.tray_id, contx.trof_id, contx.draw_id, contx.heat_id]:
        if cont:
            output_list.append("{}".format(cont.__str__()))
            break
    return output_list


def comment_parser(comment_str, anix_indv, det_date):
    coke_dict = get_comment_keywords_dict()
    parser_list = coke_dict.keys()
    mortality = False
    for term in parser_list:
        if term.lower() in comment_str.lower():
            adsc = coke_dict[term]
            if adsc.name == "Mortality":
                mortality = True
            indvd_parsed = models.IndividualDet(anix_id_id=anix_indv.pk,
                                                anidc_id=adsc.anidc_id,
                                                adsc_id=adsc,
                                                qual_id=models.QualCode.objects.filter(name="Good").get(),
                                                detail_date=det_date,
                                                comments=comment_str,
                                                created_by=anix_indv.created_by,
                                                created_date=anix_indv.created_date,
                                                )
            try:
                indvd_parsed.clean()
                indvd_parsed.save()
            except (ValidationError, IntegrityError):
                pass
    if mortality:
        anix_indv.indv_id.indv_valid = False
        anix_indv.indv_id.save()


def enter_indvd(anix_pk, cleaned_data, det_date, det_value, anidc_str, adsc_str, comments=None):
    row_entered = False
    if isinstance(det_value, float):
        if math.isnan(det_value):
            return False
    if adsc_str:
        indvd = models.IndividualDet(anix_id_id=anix_pk,
                                     anidc_id=models.AnimalDetCode.objects.filter(name=anidc_str).get(),
                                     adsc_id=models.AniDetSubjCode.objects.filter(name=adsc_str).get(),
                                     det_val=det_value,
                                     detail_date=det_date,
                                     qual_id=models.QualCode.objects.filter(name="Good").get(),
                                     comments=comments,
                                     created_by=cleaned_data["created_by"],
                                     created_date=cleaned_data["created_date"],
                                     )
    else:
        indvd = models.IndividualDet(anix_id_id=anix_pk,
                                     anidc_id=models.AnimalDetCode.objects.filter(name=anidc_str).get(),
                                     det_val=det_value,
                                     detail_date=det_date,
                                     qual_id=models.QualCode.objects.filter(name="Good").get(),
                                     created_by=cleaned_data["created_by"],
                                     created_date=cleaned_data["created_date"],
                                     )
    try:
        indvd.clean()
        indvd.save()
        row_entered = True
    except (ValidationError, IntegrityError):
        pass
    return row_entered


def enter_grpd(anix_pk, cleaned_data, det_date, det_value, anidc_str, adsc_str=None, comments=None):
    row_entered = False
    if isinstance(det_value, float):
        if math.isnan(det_value):
            return False
    if adsc_str:
        grpd = models.GroupDet(anix_id_id=anix_pk,
                               anidc_id=models.AnimalDetCode.objects.filter(name=anidc_str).get(),
                               adsc_id=models.AniDetSubjCode.objects.filter(name=adsc_str).get(),
                               det_val=det_value,
                               detail_date=det_date,
                               qual_id=models.QualCode.objects.filter(name="Good").get(),
                               comments=comments,
                               created_by=cleaned_data["created_by"],
                               created_date=cleaned_data["created_date"],
                               )
    else:
        grpd = models.GroupDet(anix_id_id=anix_pk,
                               anidc_id=models.AnimalDetCode.objects.filter(name=anidc_str).get(),
                               det_val=det_value,
                               detail_date=det_date,
                               qual_id=models.QualCode.objects.filter(name="Good").get(),
                               created_by=cleaned_data["created_by"],
                               created_date=cleaned_data["created_date"],
                               )
    try:
        grpd.clean()
        grpd.save()
        row_entered = True
    except (ValidationError, IntegrityError):
        pass
    return row_entered


def create_movement_evnt(origin, destination, cleaned_data, movement_date=None, indv_pk=None, grp_pk=None):
    row_entered = False
    new_cleaned_data = cleaned_data.copy()

    if enter_tank_contx(origin, cleaned_data, None):
        row_entered = True

    if enter_tank_contx(destination, cleaned_data, None):
        row_entered = True

    if not origin == "nan" and not destination == "nan":
        movement_evnt = models.Event(evntc_id=models.EventCode.objects.filter(name="Movement").get(),
                                     facic_id=cleaned_data["evnt_id"].facic_id,
                                     perc_id=cleaned_data["evnt_id"].perc_id,
                                     prog_id=cleaned_data["evnt_id"].prog_id,
                                     start_datetime=movement_date,
                                     end_datetime=movement_date,
                                     created_by=new_cleaned_data["created_by"],
                                     created_date=new_cleaned_data["created_date"],
                                     )
        try:
            movement_evnt.clean()
            movement_evnt.save()
            row_entered = True
        except (ValidationError, IntegrityError):
            movement_evnt = models.Event.objects.filter(evntc_id=movement_evnt.evntc_id,
                                                        facic_id=movement_evnt.facic_id,
                                                        prog_id=movement_evnt.prog_id,
                                                        start_datetime=movement_evnt.start_datetime,
                                                        end_datetime=movement_evnt.end_datetime,
                                                        ).get()

        new_cleaned_data["evnt_id"] = movement_evnt
        if indv_pk:
            enter_anix(new_cleaned_data, indv_pk=indv_pk)
        if grp_pk:
            enter_anix(new_cleaned_data, grp_pk=grp_pk)
        if enter_tank_contx(origin, new_cleaned_data, False, indv_pk=indv_pk, grp_pk=grp_pk):
            row_entered = True
        if enter_tank_contx(destination, new_cleaned_data, True, indv_pk=indv_pk, grp_pk=grp_pk):
            row_entered = True

        return row_entered


def enter_tank_contx(tank, cleaned_data, final_flag, indv_pk=None, grp_pk=None, return_contx=False):
    row_entered = False
    if not tank == "nan":
        contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                     tank_id=models.Tank.objects.filter(name=tank, facic_id=cleaned_data["facic_id"]).get(),
                                     created_by=cleaned_data["created_by"],
                                     created_date=cleaned_data["created_date"],
                                     )
        try:
            contx.clean()
            contx.save()
            row_entered = True
        except ValidationError:
            contx = models.ContainerXRef.objects.filter(evnt_id=contx.evnt_id,
                                                        tank_id=contx.tank_id).get()
        enter_anix(cleaned_data, indv_pk=indv_pk, grp_pk=grp_pk, contx_pk=contx.pk, final_flag=final_flag)
        if return_contx:
            return contx
        else:
            return row_entered
    else:
        return False


def enter_trof_contx(trof, cleaned_data, final_flag, indv_pk=None, grp_pk=None, return_contx=False):
    row_entered = False
    if not trof == "nan":
        contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                     tro_id=models.Trough.objects.filter(name=trof, facic_id=cleaned_data["facic_id"]).get(),
                                     created_by=cleaned_data["created_by"],
                                     created_date=cleaned_data["created_date"],
                                     )
        try:
            contx.clean()
            contx.save()
            row_entered = True
        except ValidationError:
            contx = models.ContainerXRef.objects.filter(evnt_id=contx.evnt_id,
                                                        trof_id=contx.trof_id).get()

        enter_anix(cleaned_data, indv_pk=indv_pk, grp_pk=grp_pk, contx_pk=contx.pk, final_flag=final_flag)

        if return_contx:
            return contx
        else:
            return row_entered
    else:
        return False


def enter_env(env_value, env_date, cleaned_data, envc_str, envsc_str=None, loc_id=None, contx=None, inst_id=None, env_start=None, avg=False):
    row_entered = False
    if isinstance(env_value, float):
        if math.isnan(env_value):
            return False
    if env_start:
        env_datetime = datetime.datetime.combine(env_date, env_start).replace(tzinfo=pytz.UTC)
    else:
        env_datetime = datetime.datetime.combine(env_date, datetime.datetime.min.time()).replace(tzinfo=pytz.UTC)
    if envsc_str:
        env = models.EnvCondition(contx_id=contx,
                                  loc_id=loc_id,
                                  envc_id=models.EnvCode.objects.filter(name=envc_str).get(),
                                  envsc_id=models.EnvSubjCode.objects.filter(name=envsc_str).get(),
                                  inst_id=inst_id,
                                  env_val=str(env_value),
                                  env_avg=avg,
                                  start_datetime=env_datetime,
                                  qual_id=models.QualCode.objects.filter(name="Good").get(),
                                  created_by=cleaned_data["created_by"],
                                  created_date=cleaned_data["created_date"],
                                  )
    else:
        env = models.EnvCondition(contx_id=contx,
                                  loc_id=loc_id,
                                  envc_id=models.EnvCode.objects.filter(name=envc_str).get(),
                                  inst_id=inst_id,
                                  env_val=str(env_value),
                                  env_avg=avg,
                                  start_datetime=env_datetime,
                                  qual_id=models.QualCode.objects.filter(name="Good").get(),
                                  created_by=cleaned_data["created_by"],
                                  created_date=cleaned_data["created_date"],
                                  )
    try:
        env.clean()
        env.save()
        row_entered = True
    except (ValidationError, IntegrityError):
        pass
    return row_entered


def enter_anix(cleaned_data, indv_pk=None, contx_pk=None, loc_pk=None, pair_pk=None, grp_pk=None, indvt_pk=None, final_flag=None):
    if any([indv_pk, contx_pk, loc_pk, pair_pk, grp_pk, indvt_pk]):
        anix = models.AniDetailXref(evnt_id_id=cleaned_data["evnt_id"].pk,
                                    indv_id_id=indv_pk,
                                    contx_id_id=contx_pk,
                                    loc_id_id=loc_pk,
                                    pair_id_id=pair_pk,
                                    grp_id_id=grp_pk,
                                    indvt_id_id=indvt_pk,
                                    final_contx_flag=final_flag,
                                    created_by=cleaned_data["created_by"],
                                    created_date=cleaned_data["created_date"],
                                    )
        try:
            anix.clean()
            anix.save()
            return anix
        except ValidationError:
            anix = models.AniDetailXref.objects.filter(evnt_id=anix.evnt_id,
                                                       indv_id=anix.indv_id,
                                                       contx_id=anix.contx_id,
                                                       loc_id=anix.loc_id,
                                                       pair_id=anix.pair_id,
                                                       grp_id=anix.grp_id,
                                                       indvt_id=anix.indvt_id,
                                                       ).get()
            return anix


def enter_anix_contx(tank, cleaned_data):
    if tank:
        contx = models.ContainerXRef(evnt_id=cleaned_data["evnt_id"],
                                     tank_id=tank,
                                     created_by=cleaned_data["created_by"],
                                     created_date=cleaned_data["created_date"],
                                     )
        try:
            contx.clean()
            contx.save()
            return contx
        except ValidationError:
            contx = models.ContainerXRef.objects.filter(evnt_id=contx.evnt_id,
                                                        tank=contx.tank_id,
                                                        ).get()

        anix_contx = enter_anix(cleaned_data, contx_pk=contx.pk)
        return anix_contx
