import datetime
import decimal
import math

import pytz
from django.core.exceptions import ValidationError, MultipleObjectsReturned, ObjectDoesNotExist
from django.db import IntegrityError
from django.http import JsonResponse
from decimal import Decimal
from bio_diversity import models
from bio_diversity.static.calculation_constants import *


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


def get_help_text_dict(model=None, title=''):
    my_dict = {}
    if not model:
        for obj in models.HelpText.objects.all():
            my_dict[obj.field_name] = str(obj)
    else:
        # If a model is supplied get the fields specific to that model
        for obj in models.HelpText.objects.filter(model=str(model.__name__)):
            my_dict[obj.field_name] = str(obj)

    return my_dict


def team_list_splitter(team_str, valid_only=True):
    team_str_list = team_str.split(",")
    team_str_list = [indv_str.strip() for indv_str in team_str_list]
    all_perc_qs = models.PersonnelCode.objects.filter(perc_valid=True)
    found_list = []
    not_found_list = []
    for inits in team_str_list:
        perc_qs = all_perc_qs.filter(initials__iexact=inits)
        try:
            found_list.append(perc_qs.get())
        except (MultipleObjectsReturned, ObjectDoesNotExist):
            not_found_list.append(inits)
    return found_list, not_found_list


def year_coll_splitter(full_str):
    coll = full_str.lstrip(' 0123456789')
    year = int(full_str[:len(full_str) - len(coll)])
    return year, coll.strip()


def val_unit_splitter(full_str):
    unit_str = full_str.lstrip(' 0123456789.')
    val = float(full_str[:len(full_str) - len(unit_str)])
    return val, unit_str.strip()


def daily_dev(degree_day):
    dev = 100 / math.exp(DEVELOPMENT_ALPHA * math.exp(DEVELOPMENT_BETA * degree_day))
    return dev


def parse_concentration(concentration_str):
    if "%" in concentration_str:
        return Decimal(float(concentration_str.rstrip("%"))/100)
    elif ":" in concentration_str:
        concentration_str = concentration_str.replace(" ", "")
        concentration_str = concentration_str.replace("1:", "", 1)
        return Decimal(1.0/float(concentration_str))
    else:
        return None


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


def get_cont_from_anix(anix, cont_key):
    if cont_key == "tank":
        return anix.contx_id.tank_id
    elif cont_key == "tray":
        return anix.contx_id.tray_id
    elif cont_key == "trof":
        return anix.contx_id.trof_id
    elif cont_key == "cup":
        return anix.contx_id.cup_id
    elif cont_key == "heat":
        return anix.contx_id.heat_id
    elif cont_key == "draw":
        return anix.contx_id.draw_id
    elif cont_key is None:
        all_conts = [anix.contx_id.tank_id, anix.contx_id.tray_id, anix.contx_id.trof_id, anix.contx_id.cup_id, anix.contx_id.heat_id, anix.contx_id.draw_id]
        return [cont for cont in all_conts if cont][0]
    else:
        return None


def get_cont_from_dot(dot_string, cleaned_data, start_date):
    dot_string = str(dot_string)
    cup = get_cup_from_dot(dot_string, cleaned_data, start_date)
    if cup:
        return cup
    else:
        draw = get_draw_from_dot(dot_string, cleaned_data)
        if draw:
            return draw
        else:
            return None


def get_cup_from_dot(dot_string, cleaned_data, start_date):
    cont_list = dot_string.split(".")
    if len(cont_list) == 3:
        heat, draw, cup = cont_list
    else:
        return None
    cup_qs = models.Cup.objects.filter(name=cup, draw_id__name=draw, draw_id__heat_id__name=heat, draw_id__heat_id__facic_id=cleaned_data["facic_id"], end_date__isnull=True)
    if cup_qs.exists():
        return cup_qs.get()
    else:
        cup_obj = models.Cup(name=cup,
                             start_date=start_date,
                             draw_id=models.Drawer.objects.filter(name=draw, heat_id__name=heat, heat_id__facic_id=cleaned_data["facic_id"]).get(),
                             description_en="Autogenerated by parser",
                             created_by=cleaned_data["created_by"],
                             created_date=cleaned_data["created_date"],
                             )
        try:
            cup_obj.clean()
            cup_obj.save()
        except (ValidationError, IntegrityError):
            return None
        return cup_obj


def get_draw_from_dot(dot_string, cleaned_data):
    cont_list = dot_string.split(".")
    if len(cont_list) == 2:
        heat, draw = cont_list
    else:
        return None
    draw_qs = models.Drawer.objects.filter(name=draw, heat_id__name=heat, heat_id__facic_id=cleaned_data["facic_id"])
    if draw_qs.exists():
        return draw_qs.get()
    else:
        return


def get_relc_from_point(shapely_geom):
    relc_qs = models.ReleaseSiteCode.objects.all()
    for relc in relc_qs:
        # need to add infinitesimal buffer to deal with rounding issue
        if relc.bbox:
            if relc.bbox.buffer(1e-14).intersects(shapely_geom):
                return relc
    return None


def comment_parser(comment_str, anix_indv, det_date):
    coke_dict = get_comment_keywords_dict()
    parser_list = coke_dict.keys()
    mortality = False
    parsed = False
    for term in parser_list:
        if term.lower() in comment_str.lower():
            parsed = True
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
        parsed = True
        anix_indv.indv_id.indv_valid = False
        anix_indv.indv_id.save()
    return parsed


def create_movement_evnt(origin, destination, cleaned_data, movement_date, indv_pk=None, grp_pk=None, return_end_contx=False):
    row_entered = False
    end_contx = False
    origin_conts = []
    movement_date = naive_to_aware(movement_date)
    new_cleaned_data = cleaned_data.copy()
    if origin == destination:
        row_entered = False
        return row_entered
    if cleaned_data["evnt_id"]:
        # link containers to parent event
        if not origin:
            # move indvidual or group to destination and clean up previous contx's
            if grp_pk:
                grp = models.Group.objects.filter(pk=grp_pk).get()
                origin_conts = grp.current_cont(movement_date)
        else:
            if enter_contx(origin, cleaned_data, None):
                row_entered = True

        if enter_contx(destination, cleaned_data, None):
            row_entered = True

    if destination:
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
        if origin:
            if enter_contx(origin, new_cleaned_data, False, indv_pk=indv_pk, grp_pk=grp_pk):
                row_entered = True
        elif origin_conts:
            for cont in origin_conts:
                if not cont == destination:
                    if enter_contx(cont, new_cleaned_data, False, indv_pk=indv_pk, grp_pk=grp_pk):
                        row_entered = True
        end_contx = enter_contx(destination, new_cleaned_data, True, indv_pk=indv_pk, grp_pk=grp_pk, return_contx=True)
        if end_contx:
            row_entered = True

    if return_end_contx:
        return end_contx
    else:
        return row_entered


def create_new_evnt(cleaned_data, evntc_name, evnt_date):
    new_cleaned_data = cleaned_data.copy()
    new_evnt = models.Event(evntc_id=models.EventCode.objects.filter(name=evntc_name).get(),
                            facic_id=cleaned_data["evnt_id"].facic_id,
                            perc_id=cleaned_data["evnt_id"].perc_id,
                            prog_id=cleaned_data["evnt_id"].prog_id,
                            start_datetime=evnt_date,
                            end_datetime=evnt_date,
                            created_by=cleaned_data["created_by"],
                            created_date=cleaned_data["created_date"],
                            )
    try:
        new_evnt.clean()
        new_evnt.save()
    except (ValidationError, IntegrityError):
        new_evnt = models.Event.objects.filter(evntc_id=new_evnt.evntc_id,
                                               facic_id=new_evnt.facic_id,
                                               prog_id=new_evnt.prog_id,
                                               start_datetime=new_evnt.start_datetime,
                                               end_datetime=new_evnt.end_datetime,
                                               ).get()

    new_cleaned_data["evnt_id"] = new_evnt
    return new_cleaned_data


def create_egg_movement_evnt(tray, cup, cleaned_data, movement_date, grp_pk, return_cup_contx=False):
    # moves eggs from trof-tray to heat.draw.cup, only use the final group as this splits groups
    # cup argument can also be a drawer object
    row_entered = False
    new_cleaned_data = cleaned_data.copy()

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
    if grp_pk:
        enter_anix(new_cleaned_data, grp_pk=grp_pk)
    tray_contx = enter_contx(tray, new_cleaned_data, False, None, grp_pk=grp_pk, return_contx=True)
    if tray_contx:
        row_entered = True
    cup_contx = enter_contx(cup, new_cleaned_data, True, None, grp_pk=grp_pk, return_contx=True)
    if cup_contx:
        row_entered = True
    if return_cup_contx:
        return cup_contx
    else:
        return row_entered


def create_picks_evnt(cleaned_data, tray, grp_pk, pick_cnt, pick_datetime, cnt_code):
    row_entered = False
    new_cleaned_data = cleaned_data.copy()

    pick_evnt = models.Event(evntc_id=models.EventCode.objects.filter(name="Picking").get(),
                             facic_id=cleaned_data["evnt_id"].facic_id,
                             perc_id=cleaned_data["evnt_id"].perc_id,
                             prog_id=cleaned_data["evnt_id"].prog_id,
                             start_datetime=pick_datetime,
                             end_datetime=pick_datetime,
                             created_by=new_cleaned_data["created_by"],
                             created_date=new_cleaned_data["created_date"],
                             )
    try:
        pick_evnt.clean()
        pick_evnt.save()
        row_entered = True
    except (ValidationError, IntegrityError):
        pick_evnt = models.Event.objects.filter(evntc_id=pick_evnt.evntc_id,
                                                facic_id=pick_evnt.facic_id,
                                                prog_id=pick_evnt.prog_id,
                                                start_datetime=pick_evnt.start_datetime,
                                                end_datetime=pick_evnt.end_datetime,
                                                ).get()

    new_cleaned_data["evnt_id"] = pick_evnt
    if grp_pk:
        enter_anix(new_cleaned_data, grp_pk=grp_pk)
    contx = enter_contx(tray, new_cleaned_data, None, grp_pk=grp_pk, return_contx=True)
    if contx:
        row_entered = True
        enter_cnt(cleaned_data, pick_cnt, contx_pk=contx.pk, cnt_code=cnt_code)

    return row_entered


def add_team_member(perc_id, evnt_id, loc_id=None, role_id=None):

    team = models.TeamXRef(perc_id=perc_id,
                           evnt_id=evnt_id,
                           loc_id=loc_id,
                           role_id=role_id,
                           created_by=evnt_id.created_by,
                           created_date=evnt_id.created_date,
                           )
    try:
        team.clean()
        team.save()
    except ValidationError:
        team = models.TeamXRef.objects.filter(perc_id=team.perc_id, evnt_id=team.evnt_id, loc_id=team.loc_id,
                                              role_id=team.role_id)
    if team:
        return True

    return False


def create_tray(trof, tray_name, start_date, cleaned_data, save=True):
    tray = models.Tray(trof_id=trof,
                       name=tray_name,
                       description_en="Auto generated tray",
                       start_date=start_date,
                       created_by=cleaned_data["created_by"],
                       created_date=cleaned_data["created_date"],
                       )
    try:
        if save:
            tray.clean()
            tray.save()
    except (ValidationError, IntegrityError):
        tray = models.Tray.objects.filter(trof_id=tray.trof_id, name=tray.name, start_date=tray.start_date).get()
    return tray


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


def enter_cnt(cleaned_data, cnt_value, contx_pk=None, loc_pk=None, cnt_code="Fish in Container", est=False):
    cnt = False
    if not math.isnan(cnt_value):
        cnt = models.Count(loc_id_id=loc_pk,
                           contx_id_id=contx_pk,
                           spec_id=models.SpeciesCode.objects.filter(name__iexact="Salmon").get(),
                           cntc_id=models.CountCode.objects.filter(name__iexact=cnt_code).get(),
                           cnt=int(cnt_value),
                           est=est,
                           created_by=cleaned_data["created_by"],
                           created_date=cleaned_data["created_date"],
                           )
        try:
            cnt.clean()
            cnt.save()
        except ValidationError:
            cnt = models.Count.objects.filter(loc_id=cnt.loc_id, contx_id=cnt.contx_id, cntc_id=cnt.cntc_id).get()
            if cnt_code == "Mortality":
                cnt.cnt += 1
                cnt.save()
    return cnt


def enter_cnt_det(cleaned_data, cnt, det_val, det_code, det_subj_code=None, qual="Good"):
    row_entered = False
    # checks for truthness of det_val and if its a nan. Fails for None and nan (nan == nan is false), passes for values
    det_val = nan_to_none(det_val)
    if type(det_val) != str:
        det_val = round(decimal.Decimal(det_val), 5)
    if det_val:
        if not det_subj_code:
            cntd = models.CountDet(cnt_id=cnt,
                                   anidc_id=models.AnimalDetCode.objects.filter(name__iexact=det_code).get(),
                                   det_val=det_val,
                                   qual_id=models.QualCode.objects.filter(name=qual).get(),
                                   created_by=cleaned_data["created_by"],
                                   created_date=cleaned_data["created_date"],
                                   )
        else:
            cntd = models.CountDet(cnt_id=cnt,
                                   anidc_id=models.AnimalDetCode.objects.filter(name__iexact=det_code).get(),
                                   adsc_id=models.AniDetSubjCode.objects.filter(name__iexact=det_subj_code).get(),
                                   det_val=det_val,
                                   qual_id=models.QualCode.objects.filter(name=qual).get(),
                                   created_by=cleaned_data["created_by"],
                                   created_date=cleaned_data["created_date"],
                                   )
        try:
            cntd.clean()
            cntd.save()
            row_entered = True
        except (ValidationError, IntegrityError):
            row_entered = False

        # update count total if needed:
        if det_code == "Program Group":
            new_cnt = sum([float(cnt) for cnt in models.CountDet.objects.filter(cnt_id=cnt, anidc_id__name__iexact=det_code).values_list('det_val', flat=True)])
            if new_cnt > cnt.cnt:
                cnt.cnt = int(new_cnt)
                cnt.save()

    return row_entered


def enter_env(env_value, env_date, cleaned_data, envc_id, envsc_id=None, loc_id=None, contx=None, inst_id=None,
              env_start=None, avg=False, save=True, qual_id=False):
    row_entered = False
    if isinstance(env_value, float):
        if math.isnan(env_value):
            return False
    if env_start:
        env_datetime = naive_to_aware(env_date, env_start)
    else:
        env_datetime = naive_to_aware(env_date)

    if not qual_id:
        qual_id = models.QualCode.objects.filter(name="Good").get()

    if envsc_id:
        env = models.EnvCondition(contx_id=contx,
                                  loc_id=loc_id,
                                  envc_id=envc_id,
                                  envsc_id=envsc_id,
                                  inst_id=inst_id,
                                  env_val=str(env_value),
                                  env_avg=avg,
                                  start_datetime=env_datetime,
                                  qual_id=qual_id,
                                  created_by=cleaned_data["created_by"],
                                  created_date=cleaned_data["created_date"],
                                  )
    else:
        env = models.EnvCondition(contx_id=contx,
                                  loc_id=loc_id,
                                  envc_id=envc_id,
                                  inst_id=inst_id,
                                  env_val=str(env_value),
                                  env_avg=avg,
                                  start_datetime=env_datetime,
                                  qual_id=qual_id,
                                  created_by=cleaned_data["created_by"],
                                  created_date=cleaned_data["created_date"],
                                  )
    if save:
        try:
            env.clean()
            env.save()
            row_entered = True
        except (ValidationError, IntegrityError):
            pass
        return row_entered
    else:
        try:
            env.clean()
            return env
        except (ValidationError, IntegrityError):
            return None


def enter_grpd(anix_pk, cleaned_data, det_date, det_value, anidc_str, adsc_str=None, frm_grp_id=None, comments=None):
    row_entered = False
    if isinstance(det_value, float):
        if math.isnan(det_value):
            return False
    if adsc_str:
        grpd = models.GroupDet(anix_id_id=anix_pk,
                               anidc_id=models.AnimalDetCode.objects.filter(name=anidc_str).get(),
                               adsc_id=models.AniDetSubjCode.objects.filter(name=adsc_str).get(),
                               frm_grp_id=frm_grp_id,
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
                               frm_grp_id=frm_grp_id,
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


def enter_mortality(indv, cleaned_data, mort_date):
    mortality_evnt = models.Event(evntc_id=models.EventCode.objects.filter(name="Mortality").get(),
                                  facic_id=cleaned_data["evnt_id"].facic_id,
                                  prog_id=cleaned_data["evnt_id"].prog_id,
                                  perc_id=cleaned_data["evnt_id"].perc_id,
                                  start_datetime=mort_date,
                                  end_datetime=mort_date,
                                  created_by=cleaned_data["created_by"],
                                  created_date=cleaned_data["created_date"],
                                  )
    try:
        mortality_evnt.clean()
        mortality_evnt.save()
    except (ValidationError, IntegrityError):
        mortality_evnt = models.Event.objects.filter(evntc_id=mortality_evnt.evntc_id,
                                                     facic_id=mortality_evnt.facic_id,
                                                     prog_id=mortality_evnt.prog_id,
                                                     start_datetime=mortality_evnt.start_datetime,
                                                     end_datetime=mortality_evnt.end_datetime,
                                                     ).get()
    new_cleaned_data = cleaned_data.copy()
    new_cleaned_data["evnt_id"] = mortality_evnt
    anix = enter_anix(new_cleaned_data, indv_pk=indv.pk)
    indv.indv_valid = False
    indv.save()
    return mortality_evnt, anix


def enter_spwnd(pair_pk, cleaned_data, det_value, spwndc_str, spwnsc_str, qual_code="Good", comments=None):
    row_entered = False
    if isinstance(det_value, float):
        if math.isnan(det_value):
            return False
    if spwnsc_str:
        spwnd = models.SpawnDet(pair_id_id=pair_pk,
                                anidc_id=models.SpawnDetCode.objects.filter(name=spwndc_str).get(),
                                adsc_id=models.SpawnDetSubjCode.objects.filter(name=spwnsc_str).get(),
                                det_val=det_value,
                                qual_id=models.QualCode.objects.filter(name=qual_code).get(),
                                comments=comments,
                                created_by=cleaned_data["created_by"],
                                created_date=cleaned_data["created_date"],
                                )
    else:
        spwnd = models.SpawnDet(pair_id_id=pair_pk,
                                spwndc_id=models.SpawnDetCode.objects.filter(name=spwndc_str).get(),
                                det_val=det_value,
                                qual_id=models.QualCode.objects.filter(name=qual_code).get(),
                                created_by=cleaned_data["created_by"],
                                created_date=cleaned_data["created_date"],
                                )
        try:
            spwnd.clean()
            spwnd.save()
            row_entered = True
        except ValidationError:
            pass
    return row_entered


def enter_contx(cont, cleaned_data, final_flag=None, indv_pk=None, grp_pk=None, return_contx=False):
    cont_type = type(cont)
    if cont_type == models.Tank:
        return enter_tank_contx(cont.name, cleaned_data, final_flag, indv_pk, grp_pk, return_contx)
    elif cont_type == models.Trough:
        return enter_trof_contx(cont.name, cleaned_data, final_flag, indv_pk, grp_pk, return_contx)
    elif cont_type == models.Tray:
        return enter_tray_contx(cont, cleaned_data, final_flag, indv_pk, grp_pk, return_contx)
    elif cont_type == models.Cup:
        return enter_cup_contx(cont, cleaned_data, final_flag, indv_pk, grp_pk, return_contx)
    elif cont_type == models.Drawer:
        return enter_draw_contx(cont, cleaned_data, final_flag, indv_pk, grp_pk, return_contx)
    elif cont_type == models.HeathUnit:
        return enter_heat_contx(cont, cleaned_data, final_flag, indv_pk, grp_pk, return_contx)


def enter_tank_contx(tank_name, cleaned_data, final_flag=None, indv_pk=None, grp_pk=None, return_contx=False):
    row_entered = False
    if not tank_name == "nan":
        contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                     tank_id=models.Tank.objects.filter(name=tank_name, facic_id=cleaned_data["facic_id"]).get(),
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
        if indv_pk or grp_pk:
            enter_anix(cleaned_data, indv_pk=indv_pk, grp_pk=grp_pk, contx_pk=contx.pk, final_flag=final_flag)
        if return_contx:
            return contx
        else:
            return row_entered
    else:
        return False


def enter_trof_contx(trof_name, cleaned_data, final_flag=None, indv_pk=None, grp_pk=None, return_contx=False):
    row_entered = False
    if not trof_name == "nan":
        contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                     trof_id=models.Trough.objects.filter(name=trof_name, facic_id=cleaned_data["facic_id"]).get(),
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
        if indv_pk or grp_pk:
            enter_anix(cleaned_data, indv_pk=indv_pk, grp_pk=grp_pk, contx_pk=contx.pk, final_flag=final_flag)
        if return_contx:
            return contx
        else:
            return row_entered
    else:
        return False


def enter_tray_contx(tray, cleaned_data, final_flag=None, indv_pk=None, grp_pk=None, return_contx=False):
    row_entered = False
    if not tray == "nan":
        contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                     tray_id=tray,
                                     created_by=cleaned_data["created_by"],
                                     created_date=cleaned_data["created_date"],
                                     )
        try:
            contx.clean()
            contx.save()
            row_entered = True
        except ValidationError:
            contx = models.ContainerXRef.objects.filter(evnt_id=contx.evnt_id,
                                                        tray_id=contx.tray_id).get()
        if indv_pk or grp_pk:
            enter_anix(cleaned_data, indv_pk=indv_pk, grp_pk=grp_pk, contx_pk=contx.pk, final_flag=final_flag)
        if return_contx:
            return contx
        else:
            return row_entered
    else:
        return False


def enter_cup_contx(cup, cleaned_data, final_flag=None, indv_pk=None, grp_pk=None, return_contx=False):
    row_entered = False
    if not cup == "nan":
        contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                     cup_id=cup,
                                     created_by=cleaned_data["created_by"],
                                     created_date=cleaned_data["created_date"],
                                     )
        try:
            contx.clean()
            contx.save()
            row_entered = True
        except ValidationError:
            contx = models.ContainerXRef.objects.filter(evnt_id=contx.evnt_id,
                                                        cup_id=contx.cup_id).get()

        draw_contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                          draw_id=cup.draw_id,
                                          created_by=cleaned_data["created_by"],
                                          created_date=cleaned_data["created_date"],
                                          )
        try:
            draw_contx.clean()
            draw_contx.save()
            row_entered = True
        except ValidationError:
            pass

        heat_contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                          heat_id=cup.draw_id.heat_id,
                                          created_by=cleaned_data["created_by"],
                                          created_date=cleaned_data["created_date"],
                                          )
        try:
            heat_contx.clean()
            heat_contx.save()
            row_entered = True
        except ValidationError:
            pass

        if indv_pk or grp_pk:
            enter_anix(cleaned_data, indv_pk=indv_pk, grp_pk=grp_pk, contx_pk=contx.pk, final_flag=final_flag)
        if return_contx:
            return contx
        else:
            return row_entered
    else:
        return False


def enter_draw_contx(draw, cleaned_data, final_flag=None, indv_pk=None, grp_pk=None, return_contx=False):
    row_entered = False
    if draw:
        contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                     draw_id=draw,
                                     created_by=cleaned_data["created_by"],
                                     created_date=cleaned_data["created_date"],
                                     )
        try:
            contx.clean()
            contx.save()
            row_entered = True
        except ValidationError:
            contx = models.ContainerXRef.objects.filter(evnt_id=contx.evnt_id,
                                                        draw_id=contx.draw_id).get()

        heat_contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                          heat_id=draw.heat_id,
                                          created_by=cleaned_data["created_by"],
                                          created_date=cleaned_data["created_date"],
                                          )
        try:
            heat_contx.clean()
            heat_contx.save()
            row_entered = True
        except ValidationError:
            pass

        if indv_pk or grp_pk:
            enter_anix(cleaned_data, indv_pk=indv_pk, grp_pk=grp_pk, contx_pk=contx.pk, final_flag=final_flag)
        if return_contx:
            return contx
        else:
            return row_entered
    else:
        return False


def enter_heat_contx(heat, cleaned_data, final_flag=None, indv_pk=None, grp_pk=None, return_contx=False):
    row_entered = False
    if heat:
        contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                     heat_id=heat,
                                     created_by=cleaned_data["created_by"],
                                     created_date=cleaned_data["created_date"],
                                     )
        try:
            contx.clean()
            contx.save()
            row_entered = True
        except ValidationError:
            contx = models.ContainerXRef.objects.filter(evnt_id=contx.evnt_id,
                                                        heat_id=contx.heat_id).get()

        if indv_pk or grp_pk:
            enter_anix(cleaned_data, indv_pk=indv_pk, grp_pk=grp_pk, contx_pk=contx.pk, final_flag=final_flag)
        if return_contx:
            return contx
        else:
            return row_entered
    else:
        return False


def ajax_get_fields(request):
    model_name = request.GET.get('model', None)

    # use the model name passed from the web page to find the model in the apps models file
    model = models.__dict__[model_name]

    # use the retrieved model and get the doc string which is a string in the format
    # SomeModelName(id, field1, field2, field3)
    # remove the trailing parentheses, split the string up based on ', ', then drop the first element
    # which is the model name and the id.
    match = str(model.__dict__['__doc__']).replace(")", "").split(", ")[1:]
    fields = list()
    for f in match:
        label = "---"
        attr = getattr(model, f).field
        if hasattr(attr, 'verbose_name'):
            label = attr.verbose_name

        fields.append([f, label])

    data = {
        'fields': fields
    }

    return JsonResponse(data)


def naive_to_aware(naive_date, naive_time=datetime.datetime.min.time()):
    # adds null time and timezone to dates
    return datetime.datetime.combine(naive_date, naive_time).replace(tzinfo=pytz.UTC)


def nan_to_none(test_item):
    if type(test_item) == float:
        if math.isnan(test_item):
            return None
    elif test_item == "nan":
        return None

    return test_item


def round_no_nan(data, precision):
    # data can be nan, decimal, float, etc.
    if math.isnan(data) or data is None:
        return None
    else:
        return round(decimal.Decimal(data), precision)
