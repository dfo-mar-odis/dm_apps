from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from . import models


def special_capitalize(raw_string):
    """ Little dance to make sure the first letter is capitalized.
    Do not want to use the capitalize() method since it makes the remaining portion of str lowercase. This is problematic in
     cases like: `DFO employee` since that would become `Dfo employee`"""
    first_letter = raw_string[0].upper()
    str_list = list(raw_string)
    str_list[0] = first_letter
    raw_string = "".join(str_list)
    return raw_string


def get_section_choices(full_name=True, region_filter=None, branch_filter=None, division_filter=None):
    if full_name:
        my_attr = "full_name"
    else:
        my_attr = _("name")

    if region_filter:
        reg_kwargs = {
            "division__branch__region_id": region_filter
        }
    else:
        reg_kwargs = {
            "division__branch__region_id__isnull": False
        }

    if branch_filter:
        branch_kwargs = {
            "division__branch_id": branch_filter
        }
    else:
        branch_kwargs = {
            "division__branch__isnull": False
        }

    if division_filter:
        div_kwargs = {
            "division_id": division_filter
        }
    else:
        div_kwargs = {
            "division_id__isnull": False
        }

    my_choice_list = [(s.id, getattr(s, my_attr)) for s in
                      models.Section.objects.order_by(
                          "division__branch__region",
                          "division__branch",
                          "division",
                          "name"
                      ).filter(**div_kwargs).filter(**reg_kwargs).filter(**branch_kwargs)]

    return my_choice_list


def get_division_choices(region_filter=None, branch_filter=None):
    division_list = set(
        [models.Section.objects.get(pk=s[0]).division_id for s in
         get_section_choices(region_filter=region_filter, branch_filter=branch_filter)])
    return [(d.id, str(d)) for d in
            models.Division.objects.filter(id__in=division_list).order_by("branch__region", "name")]


def get_branch_choices(region_filter=None):
    branch_list = set(
        [models.Division.objects.get(pk=d[0]).branch_id for d in get_division_choices(region_filter=region_filter)])
    return [(b.id, str(b)) for b in
            models.Branch.objects.filter(id__in=branch_list).order_by("region", "name")]


def get_region_choices():
    region_list = set(
        [models.Division.objects.get(pk=d[0]).branch.region_id for d in get_division_choices()])
    return [(r.id, str(r)) for r in
            models.Region.objects.filter(id__in=region_list).order_by("name", )]


def get_metadata_string(created_at=None, created_by=None, updated_at=None, last_modified_by=None, with_tz=False, with_time=True):
    format_str = '%Y-%m-%d'
    if with_time:
        format_str += " %H:%M:%S"
    if with_tz:
        format_str += " %Z"
    my_str = None
    str_by = _("by")
    str_created = _("Created:")
    str_updated = _("Last updated:")
    if created_by:
        my_str = f"<u>{str_created}</u> {created_at.strftime(format_str)}"
        my_str += f" {str_by} {created_by}"
    if updated_at:
        if not my_str:
            my_str = f"<u>{str_updated}</u> {updated_at.strftime(format_str)}"
        else:
            my_str += f"<br><u>{str_updated}</u> {updated_at.strftime(format_str)}"
        if last_modified_by:
            my_str += f" {str_by} {last_modified_by}"

    return mark_safe(my_str)


# https://stackoverflow.com/questions/2579535/convert-dd-decimal-degrees-to-dms-degrees-minutes-seconds-in-python (thanks)
def decdeg2dm(dd):
    is_positive = dd >= 0
    dd = abs(dd)
    minutes, seconds = divmod(dd * 3600, 60)
    degrees, minutes = divmod(minutes, 60)
    degrees = degrees if is_positive else -degrees
    decmin = minutes + seconds / 60
    return (degrees, decmin)


def dm2decdeg(d, m):
    try:
        is_positive = d >= 0
        dd = abs(d)

        mm = (abs(m) / 60) + ((m - abs(m)) / 3600)

        return dd + mm if is_positive else (dd + mm) * -1
    except Exception as E:
        # print(E)
        pass


def format_coordinates(lat, lng, output_format, sep="/"):
    """
    @param lat: latitude (dd)
    @param lng: longitude (dd)
    @param output_format: dd | dm
    @param sep: the separator used to separate lat and long
    @return: formatted html string
    """
    try:
        if output_format == "dm":
            dmx = decdeg2dm(lat)
            dmy = decdeg2dm(lng)
            mystr = mark_safe(f"lat: {int(dmx[0])}° {format(dmx[1], '4f')}'  / lng: {int(dmy[0])}° {format(dmy[1], '4f')}'")
        else:
            mystr = mark_safe(f"lat: {format(lat, '4f')}°  {sep} lng: {format(lng, '4f')}°")

        return mystr
    except:
        return "---"


def get_labels(model):
    labels = {}
    for field in model._meta.get_fields():
        if hasattr(field, "name") and hasattr(field, "verbose_name"):
            labels[field.name] = special_capitalize(field.verbose_name)
    return labels
