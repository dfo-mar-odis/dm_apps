from datetime import datetime

import xlsxwriter as xlsxwriter
from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import yesno
from django.urls import reverse
from django.utils import timezone

from lib.functions.custom_functions import nz, listrify
from lib.functions.verbose_field_name import verbose_field_name
from lib.templatetags.custom_filters import currency
from lib.templatetags.verbose_names import get_verbose_label, get_field_value
from . import models
from shared_models import models as shared_models
import os


def generate_cfts_spreadsheet(fiscal_year=None, region=None, trip_request=None, trip=None, user=None, from_date=None, to_date=None):
    # figure out the filename
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'travel', 'temp')
    target_file = "temp_export.xlsx"
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'travel', 'temp', target_file)

    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path)
    ws = workbook.add_worksheet(name="CFTS report")

    # create formatting
    title_format = workbook.add_format({'bold': True, "align": 'normal', 'font_size': 24, })
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#8C96A0', "align": 'normal',
         "text_wrap": True})
    normal_format = workbook.add_format({"align": 'left', "valign": 'top', "text_wrap": True, 'num_format': '[$$-409]#,##0.00'})

    if fiscal_year == "None":
        fiscal_year = None
    if region == "None":
        region = None
    if trip == "None":
        trip = None
    if user == "None":
        user = None

    if from_date == "None":
        from_date = None
    else:
        fiscal_year = None  # should not filter on both criteria

    if to_date == "None":
        to_date = None
    else:
        fiscal_year = None  # should not filter on both criteria

    include_trip_request_status = False
    # get a request list
    if fiscal_year or region or user or from_date or to_date:
        include_trip_request_status = True
        # if this report is being called from the reports page...
        trip_request_list = models.TripRequest.objects.all()
        if fiscal_year:
            trip_request_list = trip_request_list.filter(fiscal_year_id=fiscal_year)
        if region:
            trip_request_list = trip_request_list.filter(section__division__branch__region_id=region)

        if user:
            trip_request_list = trip_request_list.filter(user_id=user)

        if trip:
            trip_request_list = trip_request_list.filter(trip_id=trip)

        if from_date:
            my_date = datetime.strptime(from_date, "%Y-%m-%d").replace(tzinfo=timezone.get_current_timezone())
            trip_request_list = trip_request_list.filter(
                start_date__gte=my_date,
            )

        if to_date:
            my_date = datetime.strptime(to_date, "%Y-%m-%d").replace(tzinfo=timezone.get_current_timezone())
            trip_request_list = trip_request_list.filter(
                start_date__lt=my_date,
            )

        # at this point, the trip will also include parent trips. We must exclude them
        trip_request_id_list = list()
        for tr in trip_request_list:
            if tr.is_group_request:
                trip_request_id_list.extend([child_tr.id for child_tr in tr.children_requests.all()])
            else:
                trip_request_id_list.append(tr.id)

        trip_request_list = models.TripRequest.objects.filter(id__in=trip_request_id_list)

    elif trip_request:
        my_trip_request = models.TripRequest.objects.get(pk=trip_request)
        if my_trip_request.is_group_request:
            is_group = True
            trip_request_list = my_trip_request.children_requests.all()
        else:
            is_group = False
            trip_request_list = models.TripRequest.objects.filter(pk=trip_request)

    elif trip:
        my_trip = models.Conference.objects.get(pk=trip)
        trip_request_list = my_trip.get_connected_requests()
    else:
        trip_request_list = None
        # non_group_trip_list = models.Trip.objects.all()

    # we need a list of ADM unapproved but recommended
    # group travellers need to be on one row

    header = [
        "Name",
        "Region",
        "Primary Role of Traveller",
        "Primary Reason for Travel",
        "Event",
        "Location",
        "Start Date",
        "End Date",
        "Est. DFO Cost",
        "Est. Non-DFO Cost",
        "Purpose",
        "Notes",
    ]
    if include_trip_request_status:
        header.insert(0, "Request Status")

    # create the col_max column to store the length of each header
    # should be a maximum column width to 100
    col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]

    title = "CFTS-styled Report on DFO Science Trip Requests"
    if fiscal_year:
        title += f" for {shared_models.FiscalYear.objects.get(pk=fiscal_year)}"
    elif from_date and not to_date:
        title += f" from {from_date} Onwards"
    elif to_date and not from_date:
        title += f" up until {to_date}"
    elif to_date and from_date:
        title += f" ranging from {from_date} to {to_date}"

    if region:
        title += f" ({shared_models.Region.objects.get(pk=region)})"
    if user:
        title += f" ({User.objects.get(pk=user)})"
    if trip:
        title += f" ({models.Conference.objects.get(pk=trip).tname})"

    ws.write(0, 0, title, title_format)
    ws.write_row(2, 0, header, header_format)

    if trip_request_list:
        i = 3
        for tr in trip_request_list.order_by("trip__start_date"):
            # Build the Notes field
            notes = "TRAVELLER COST BREAKDOWN: " + tr.cost_breakdown

            if tr.parent_request:
                if tr.parent_request.non_dfo_org:
                    notes += "\n\nORGANIZATIONS PAYING NON-DFO COSTS: " + tr.parent_request.non_dfo_org
            else:
                if tr.non_dfo_org:
                    notes += "\n\nORGANIZATIONS PAYING NON-DFO COSTS: " + tr.non_dfo_org

            if tr.parent_request:
                if tr.parent_request.late_justification:
                    notes += "\n\nJUSTIFICATION FOR LATE SUBMISSION: " + tr.parent_request.late_justification
            else:
                if tr.late_justification:
                    notes += "\n\nJUSTIFICATION FOR LATE SUBMISSION: " + tr.late_justification

            if tr.parent_request:
                if tr.parent_request.funding_source:
                    notes += "\n\nFUNDING SOURCE: {}".format(tr.parent_request.funding_source)
            else:
                if tr.funding_source:
                    notes += "\n\nFUNDING SOURCE: {}".format(tr.funding_source)

            # Request status
            if tr.parent_request:
                my_status = str(tr.parent_request.status)
            else:
                my_status = str(tr.status)

            # DESTINATION
            if tr.parent_request:
                my_dest = str(tr.parent_request.destination) if tr.parent_request.destination else "n/a"
            else:
                my_dest = str(tr.destination) if tr.destination else "n/a"

            # START DATE OF TRAVEL
            if tr.parent_request:
                my_start = tr.parent_request.start_date.strftime("%d/%m/%Y") if tr.parent_request.start_date else "n/a"
            else:
                my_start = tr.start_date.strftime("%d/%m/%Y") if tr.start_date else "n/a"

            # END DATE OF TRAVEL
            if tr.parent_request:
                my_end = tr.parent_request.end_date.strftime("%d/%m/%Y") if tr.parent_request.end_date else "n/a"
            else:
                my_end = tr.end_date.strftime("%d/%m/%Y") if tr.end_date else "n/a"

            # PURPOSE
            if tr.parent_request:
                my_purpose = tr.parent_request.purpose_long_text
            else:
                my_purpose = tr.purpose_long_text

            my_role = "{}".format(nz(tr.role, "MISSING"), )

            my_name = "{}, {}".format(tr.last_name, tr.first_name)
            if tr.is_research_scientist:
                my_name += " (RES)"

            data_row = [
                my_name,
                str(tr.region) if tr.region else "n/a",
                my_role,
                str(tr.smart_trip.trip_subcategory),
                str(tr.smart_trip),
                my_dest,
                my_start,
                my_end,
                tr.total_dfo_funding,
                tr.total_non_dfo_funding,
                my_purpose,
                notes,
            ]

            if include_trip_request_status:
                data_row.insert(0, my_status)

            # adjust the width of the columns based on the max string length in each col
            ## replace col_max[j] if str length j is bigger than stored value

            j = 0
            for d in data_row:
                # if new value > stored value... replace stored value
                if len(str(d)) > col_max[j]:
                    if len(str(d)) < 100:
                        col_max[j] = len(str(d))
                    else:
                        col_max[j] = 100
                j += 1

            ws.write_row(i, 0, data_row, normal_format)
            i += 1

        for j in range(0, len(col_max)):
            ws.set_column(j, j, width=col_max[j] * 1.1)

    workbook.close()
    return target_url


def generate_trip_list(fiscal_year, region, adm, from_date, to_date, site_url):
    # figure out the filename
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'travel', 'temp')
    target_file = "temp_data_export_{}.xlsx".format(timezone.now().strftime("%Y-%m-%d"))
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'travel', 'temp', target_file)
    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path)

    # create formatting variables
    title_format = workbook.add_format({'bold': True, "align": 'normal', 'font_size': 24, })
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#D6D1C0', "align": 'normal', "text_wrap": True})
    total_format = workbook.add_format({'bold': True, "align": 'left', "text_wrap": True, 'num_format': '$#,##0'})
    normal_format = workbook.add_format({"align": 'left', "text_wrap": True, })
    currency_format = workbook.add_format({'num_format': '#,##0.00'})

    if fiscal_year == "None":
        fiscal_year = None
    if adm == "None":
        adm = None
    if region == "None":
        region = None
    if from_date == "None":
        from_date = None
    else:
        fiscal_year = None  # should not filter on both criteria
    if to_date == "None":
        to_date = None
    else:
        fiscal_year = None  # should not filter on both criteria

    # get the trip list
    trip_list = models.Conference.objects.all()

    if fiscal_year:
        trip_list = trip_list.filter(fiscal_year=fiscal_year)

    # optional filter on trips for adm_approval_required
    if adm:
        adm = bool(int(adm))
        trip_list = trip_list.filter(is_adm_approval_required=adm)

    # optional filter on trips for regional lead
    if region:
        # too dangerous to only filter by the lead field... we should look at each request / traveller and determine
        # if they are the correct region
        request_list = list()
        # for each trip
        for trip in trip_list:
            # look at a list of the requests...
            for request in trip.trip_requests.all():
                # if group request, focus on children
                if request.is_group_request:
                    for child_request in request.children_requests.all():
                        # if the traveller is in the region of interest, add the request tp the list
                        if child_request.region_id == region:
                            # add the parent request
                            request_list.append(request)
                            break
                else:
                    # if the traveller is in the region of interest, add the request tp the list
                    if request.region_id == int(region):
                        # add the request
                        request_list.append(request)
                        break
        trip_list = trip_list.filter(trip_requests__in=request_list)

    if from_date:
        my_date = datetime.strptime(from_date, "%Y-%m-%d").replace(tzinfo=timezone.get_current_timezone())
        print(my_date)
        trip_list = trip_list.filter(
            start_date__gte=my_date,
        )

    if to_date:
        my_date = datetime.strptime(to_date, "%Y-%m-%d").replace(tzinfo=timezone.get_current_timezone())
        print(my_date)
        trip_list = trip_list.filter(
            start_date__lt=my_date,
        )

    field_list = [
        "fiscal_year",
        "name",
        "is_adm_approval_required",
        "location",
        "start_date",
        "end_date",
        "number_of_days|Number of days",
        "travellers|Travellers (region)",
        "non_res_total_cost|Total trip cost (excluding RES)",
        "total_cost|Total trip cost",
    ]

    # get_cost_comparison_dict

    # define the header
    header = [get_verbose_label(trip_list.first(), field) for field in field_list]
    # header.append('Number of projects tagged')
    title = "DFO Science Trips"
    if fiscal_year:
        title += f" for {shared_models.FiscalYear.objects.get(pk=fiscal_year)}"
    elif from_date and not to_date:
        title += f" from {from_date} Onwards"
    elif to_date and not from_date:
        title += f" up until {to_date}"
    elif to_date and from_date:
        title += f" ranging from {from_date} to {to_date}"

    if region:
        title += f" ({shared_models.Region.objects.get(pk=region)})"
    if adm is not None:
        if adm:
            title += " (Trip requiring ADM approval only)"
        else:
            title += " (Only trips NOT requiring ADM approval)"

    # define a worksheet
    my_ws = workbook.add_worksheet(name="trip list")
    my_ws.write(0, 0, title, title_format)
    my_ws.write_row(2, 0, header, header_format)

    i = 3
    for trip in trip_list.order_by("start_date"):
        # create the col_max column to store the length of each header
        # should be a maximum column width to 100
        col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]

        data_row = list()
        my_dict = trip.get_cost_comparison_dict
        j = 0
        for field in field_list:

            if "travellers" in field:
                my_list = list()
                for tr in my_dict.get("trip_requests"):
                    my_list.append(f'{tr.requester_name} ({tr.region}) - {currency(my_dict["trip_requests"][tr]["total"])}')
                my_val = listrify(my_list, "\n")

                my_ws.write(i, j, my_val, normal_format)

            elif "fiscal_year" in field:
                my_val = str(get_field_value(trip, field))
                my_ws.write(i, j, my_val, normal_format)

            elif field == "name":
                my_val = str(get_field_value(trip, field))
                my_ws.write_url(i, j,
                                url=f'{settings.SITE_FULL_URL}/{reverse("travel:trip_detail", kwargs={"pk": trip.id})}',
                                string=my_val)
            elif "cost" in field:
                my_val = nz(get_field_value(trip, field), 0)
                my_ws.write(i, j, my_val, currency_format)
            else:
                my_val = get_field_value(trip, field)
                my_ws.write(i, j, my_val, normal_format)

            # adjust the width of the columns based on the max string length in each col
            ## replace col_max[j] if str length j is bigger than stored value

            # if new value > stored value... replace stored value
            if len(str(my_val)) > col_max[j]:
                if len(str(my_val)) < 75:
                    col_max[j] = len(str(my_val))
                else:
                    col_max[j] = 75
            j += 1
        i += 1

        # set column widths
        for j in range(0, len(col_max)):
            my_ws.set_column(j, j, width=col_max[j] * 1.1)

    workbook.close()
    return target_url
