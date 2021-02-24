import datetime
import math

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
                                     evnt_start=movement_date,
                                     evnt_end=movement_date,
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
                                                        evnt_start=movement_evnt.evnt_start,
                                                        evnt_end=movement_evnt.evnt_end,
                                                        ).get()

        new_cleaned_data["evnt_id"] = movement_evnt
        if indv_pk:
            enter_anix_indv(indv_pk, new_cleaned_data)
        if grp_pk:
            enter_anix_grp(grp_pk, new_cleaned_data)
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

        anix = models.AniDetailXref(evnt_id_id=cleaned_data["evnt_id"].pk,
                                    indv_id_id=indv_pk,
                                    grp_id_id=grp_pk,
                                    contx_id_id=contx.pk,
                                    final_contx_flag=final_flag,
                                    created_by=cleaned_data["created_by"],
                                    created_date=cleaned_data["created_date"],
                                    )
        try:
            anix.clean()
            anix.save()
            row_entered = True
        except (ValidationError, IntegrityError):
            pass

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
        env_datetime = datetime.datetime.combine(env_date, env_start).replace(tzinfo=timezone.get_current_timezone())
    else:
        env_datetime = datetime.datetime.combine(env_date, datetime.datetime.min.time())
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


def enter_anix_indv(indv_pk, cleaned_data):
    if indv_pk:
        anix_indv = models.AniDetailXref(evnt_id_id=cleaned_data["evnt_id"].pk,
                                         indv_id_id=indv_pk,
                                         created_by=cleaned_data["created_by"],
                                         created_date=cleaned_data["created_date"],
                                         )
        try:
            anix_indv.clean()
            anix_indv.save()
            return anix_indv
        except ValidationError:
            anix_indv = models.AniDetailXref.objects.filter(evnt_id=anix_indv.evnt_id,
                                                            indv_id=anix_indv.indv_id,
                                                            contx_id__isnull=True,
                                                            loc_id__isnull=True,
                                                            pair_id__isnull=True,
                                                            grp_id__isnull=True,
                                                            indvt_id__isnull=True,
                                                            ).get()
            return anix_indv


def enter_anix_grp(grp_pk, cleaned_data):
    if grp_pk:
        anix_grp = models.AniDetailXref(evnt_id_id=cleaned_data["evnt_id"].pk,
                                        grp_id_id=grp_pk,
                                        created_by=cleaned_data["created_by"],
                                        created_date=cleaned_data["created_date"],
                                        )
        try:
            anix_grp.clean()
            anix_grp.save()
            return anix_grp
        except ValidationError:
            anix_grp = models.AniDetailXref.objects.filter(evnt_id=anix_grp.evnt_id,
                                                           grp_id=anix_grp.grp_id,
                                                           contx_id__isnull=True,
                                                           loc_id__isnull=True,
                                                           pair_id__isnull=True,
                                                           indv_id__isnull=True,
                                                           indvt_id__isnull=True,
                                                           ).get()
            return anix_grp


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

        anix_contx = models.AniDetailXref(evnt_id_id=cleaned_data["evnt_id"].pk,
                                          contx_id=contx,
                                          created_by=cleaned_data["created_by"],
                                          created_date=cleaned_data["created_date"],
                                          )
        try:
            anix_contx.clean()
            anix_contx.save()
            return anix_contx
        except ValidationError:
            anix_contx = models.AniDetailXref.objects.filter(evnt_id=anix_contx.evnt_id,
                                                             contx_id=anix_contx.contx_id,
                                                             indv_id__isnull=True,
                                                             loc_id__isnull=True,
                                                             pair_id__isnull=True,
                                                             grp_id__isnull=True,
                                                             indvt_id__isnull=True,
                                                             ).get()
            return anix_contx
