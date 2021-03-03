import os
from datetime import datetime

import xlsxwriter as xlsxwriter
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import yesno
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext

from lib.functions.custom_functions import nz, listrify
from lib.templatetags.custom_filters import currency
from lib.templatetags.verbose_names import get_verbose_label, get_field_value
from shared_models import models as shared_models
from . import models, utils


def generate_cfts_spreadsheet(fiscal_year=None, region=None, trip_request=None, trip=None, user=None, from_date=None, to_date=None):
    # figure out the filename
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'temp')
    target_file = "temp.xlsx"
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'temp', target_file)

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
        travellers = models.Traveller.objects.all()
        if fiscal_year:
            travellers = travellers.filter(request__fiscal_year_id=fiscal_year)
        if region:
            travellers = travellers.filter(request__section__division__branch__region_id=region)
        if user:
            travellers = travellers.filter(user_id=user)
        if trip:
            travellers = travellers.filter(request__trip_id=trip)
        if from_date:
            my_date = datetime.strptime(from_date, "%Y-%m-%d").replace(tzinfo=timezone.get_current_timezone())
            travellers = travellers.filter(
                start_date__gte=my_date)
        if to_date:
            my_date = datetime.strptime(to_date, "%Y-%m-%d").replace(tzinfo=timezone.get_current_timezone())
            travellers = travellers.filter(
                start_date__lt=my_date)

    elif trip_request:
        travellers = get_object_or_404(models.TripRequest, pk=trip_request).travellers.all()
    elif trip:
        travellers = get_object_or_404(models.Trip, pk=trip).travellers.all()
    else:
        travellers = None

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
        "Part of Learning Plan",
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
        title += f" ({models.Trip.objects.get(pk=trip).tname})"

    ws.write(0, 0, title, title_format)
    ws.write_row(2, 0, header, header_format)

    if travellers:
        i = 3
        for t in travellers.order_by("request__trip__start_date"):
            # Build the Notes field
            notes = "TRAVELLER COST BREAKDOWN: " + t.cost_breakdown

            if t.non_dfo_org:
                notes += "\n\nORGANIZATIONS PAYING NON-DFO COSTS: " + t.non_dfo_org

            if t.request.late_justification:
                notes += "\n\nJUSTIFICATION FOR LATE SUBMISSION: " + t.request.late_justification

            if t.request.funding_source:
                notes += "\n\nFUNDING SOURCE: {}".format(t.request.funding_source)

            # Request status
            my_status = str(t.request.get_status_display())

            # DESTINATION
            my_dest = t.request.trip.location

            # START DATE OF TRAVEL
            my_start = t.start_date.strftime("%d/%m/%Y") if t.start_date else "n/a"

            # END DATE OF TRAVEL
            my_end = t.end_date.strftime("%d/%m/%Y") if t.end_date else "n/a"

            # PURPOSE
            my_purpose = t.purpose_long_text

            my_role = "{}".format(nz(t.role, "MISSING"), )

            my_name = "{}, {}".format(t.last_name, t.first_name)
            if t.is_research_scientist:
                my_name += " (RES)"

            data_row = [
                my_name,
                str(t.request.region),
                my_role,
                str(t.request.trip.trip_subcategory),
                str(t.request.trip),
                my_dest,
                my_start,
                my_end,
                t.total_dfo_funding,
                t.total_non_dfo_funding,
                my_purpose,
                yesno(t.learning_plan),
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
    if settings.AZURE_STORAGE_ACCOUNT_NAME:
        utils.upload_to_azure_blob(target_file_path, f'temp/{target_file}')
    return target_url


def generate_trip_list(fiscal_year, region, adm, from_date, to_date, site_url):
    # figure out the filename
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'temp')
    target_file = "temp.xlsx"
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'temp', target_file)
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
    trip_list = models.Trip.objects.all()

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
            for request in trip.requests.all():
                # if the traveller is in the region of interest, add the request tp the list
                if request.region.id == int(region):
                    # add the request
                    request_list.append(request)
                    break
        trip_list = trip_list.filter(requests__in=request_list)

    if from_date:
        my_date = datetime.strptime(from_date, "%Y-%m-%d").replace(tzinfo=timezone.get_current_timezone())
        trip_list = trip_list.filter(
            start_date__gte=my_date,
        )

    if to_date:
        my_date = datetime.strptime(to_date, "%Y-%m-%d").replace(tzinfo=timezone.get_current_timezone())
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

        "total_cost|Total trip cost",
        "total_non_dfo_cost|Total non-DFO funding",
        "total_non_dfo_funding_sources|Non-DFO funding sources",
        "total_dfo_cost|Total DFO cost",
        "non_res_total_cost|Total DFO cost (non RES)",
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
        j = 0
        for field in field_list:

            if "travellers" in field:
                my_list = list()
                for t in trip.travellers.all():
                    my_list.append(f'{t.smart_name} ({t.request.region}) - {currency(t.total_dfo_funding)}')
                my_val = listrify(my_list, "\n")
                my_ws.write(i, j, my_val, normal_format)

            elif "fiscal_year" in field:
                my_val = str(get_field_value(trip, field))
                my_ws.write(i, j, my_val, normal_format)

            elif field == "name":
                my_val = str(get_field_value(trip, field))
                my_ws.write_url(i, j,
                                url=f'{site_url}/{reverse("travel:trip_detail", args=[trip.id])}',
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
    if settings.AZURE_STORAGE_ACCOUNT_NAME:
        utils.upload_to_azure_blob(target_file_path, f'temp/{target_file}')
    return target_url


def generate_upcoming_trip_list(site_url):
    # figure out the filename
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'temp')
    target_file = "temp.xlsx"
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'temp', target_file)
    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path, {'remove_timezone': True})

    # create formatting variables
    title_format = workbook.add_format({'bold': True, "align": 'normal', 'font_size': 24, })
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#D6D1C0', "align": 'normal', "text_wrap": True})
    total_format = workbook.add_format({'bold': True, "align": 'left', "text_wrap": True, 'num_format': '$#,##0'})
    normal_format = workbook.add_format({"align": 'left', "text_wrap": True, })
    date_format = workbook.add_format({'num_format': "yyyy-mm-dd", "align": 'left', })

    # get the trip list
    trip_list = models.Trip.objects.filter(start_date__gte=timezone.now())

    field_list = [
        "fiscal_year",
        "name",
        "status",
        "location",
        "lead",
        "travellers",
        "date_eligible_for_adm_review",
        "start_date",
        "end_date",
        "is_adm_approval_required",
        "registration_deadline",
        "abstract_deadline",
    ]

    # define the header
    header = [get_verbose_label(trip_list.first(), field) for field in field_list]
    # header.append('Number of projects tagged')
    title = gettext("Upcoming Trips and Meetings")

    # define a worksheet
    my_ws = workbook.add_worksheet(name="list")
    my_ws.write(0, 0, title, title_format)
    my_ws.write_row(2, 0, header, header_format)

    i = 3
    for trip in trip_list.order_by("date_eligible_for_adm_review"):
        # create the col_max column to store the length of each header
        # should be a maximum column width to 100
        col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]

        data_row = list()
        j = 0
        for field in field_list:
            if "travellers" in field:
                my_val = get_field_value(trip, field).count()
                my_ws.write(i, j, my_val, normal_format)

            elif "fiscal_year" in field:
                my_val = str(get_field_value(trip, field))
                my_ws.write(i, j, my_val, normal_format)
            elif "date" in field or "deadline" in field:
                my_val = getattr(trip, field)
                if my_val:
                    my_ws.write_datetime(i, j, my_val, date_format)
                else:
                    my_ws.write(i, j, my_val, normal_format)
            elif field == "name":
                my_val = str(get_field_value(trip, field))
                my_ws.write_url(i, j,
                                url=f'{site_url}/{reverse("travel:trip_detail", args=[trip.id])}',
                                string=my_val)
            else:
                my_val = str(get_field_value(trip, field))
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
    if settings.AZURE_STORAGE_ACCOUNT_NAME:
        utils.upload_to_azure_blob(target_file_path, f'temp/{target_file}')
    return target_url
