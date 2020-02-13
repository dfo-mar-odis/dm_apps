import xlsxwriter as xlsxwriter
from django.conf import settings
from django.template.defaultfilters import yesno
from lib.functions.custom_functions import nz
from lib.functions.verbose_field_name import verbose_field_name
from . import models
import os


def generate_cfts_spreadsheet(fiscal_year=None, trip_request=None, trip=None):
    # figure out the filename
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'travel', 'temp')
    target_file = "temp_export.xlsx"
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'travel', 'temp', target_file)

    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path)
    ws = workbook.add_worksheet(name="CFTS report")

    # create formatting
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#8C96A0', "align": 'normal',
         "text_wrap": True})
    normal_format = workbook.add_format({"align": 'left', "valign": 'top', "text_wrap": True, 'num_format': '[$$-409]#,##0.00'})

    # spreadsheet: Project List #
    #############################

    # get a request list
    if trip_request:
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

    # create the col_max column to store the length of each header
    # should be a maximum column width to 100
    col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]

    ws.write_row(0, 0, header, header_format)

    if trip_request_list:
        i = 1
        for tr in trip_request_list:

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

            # REASON
            if tr.parent_request:
                my_reason = str(tr.parent_request.reason) if tr.parent_request.reason else "n/a"
            else:
                my_reason = str(tr.reason) if tr.reason else "n/a"

            # TRIP NAME
            if tr.parent_request:
                my_trip_name = str(tr.parent_request.trip) if tr.parent_request.trip else "n/a"
            else:
                my_trip_name = str(tr.trip) if tr.trip else "n/a"

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

            # NON DFO COSTS
            if tr.parent_request:
                my_non_dfo_costs = nz(tr.parent_request.non_dfo_costs, 0)
            else:
                my_non_dfo_costs = nz(tr.non_dfo_costs, 0)

            # PURPOSE
            if tr.parent_request:
                my_purpose = tr.parent_request.purpose_long_text
            else:
                my_purpose = tr.purpose_long_text


            my_role = "{} - {}".format(
                nz(tr.role, "MISSING"),
                nz(tr.role_of_participant, "No description provided")
            )

            my_name = "{}, {}".format(tr.last_name, tr.first_name)
            if tr.is_research_scientist:
                my_name += " (RES)"

            data_row = [
                my_name,
                str(tr.region) if tr.region else "n/a",
                my_role,
                my_reason,
                my_trip_name,
                my_dest,
                my_start,
                my_end,
                tr.total_cost,
                my_non_dfo_costs,
                my_purpose,
                notes,
            ]

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
