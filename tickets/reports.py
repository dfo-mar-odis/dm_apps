import xlsxwriter as xlsxwriter
from django.conf import settings
from django.utils import timezone
from . import models
import os


def generate_finance_spreadsheet():
    # figure out the filename
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'tickets', 'temp')
    target_file = "temp_data_export.xlsx"
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'tickets', 'temp', target_file)

    # get a sample list for the site / year
    tickets = models.Ticket.objects.filter(financial_follow_up_needed=True).filter(
        sd_ref_number__isnull=False).order_by("-date_opened")

    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path)
    worksheet1 = workbook.add_worksheet(name="DM Tickets")

    header_format = workbook.add_format(
        {'bold': True, 'bg_color': '#8C96A0'})

    header_eng = [
        "Fiscal Year",
        "DM Ticket #",
        "Service Desk #",
        "Section",
        "Primary Client",
        "Title",
        "Request Type",
        "Estimated Cost",
        "Coding",
        "Status",
        "Date Opened",
        "Date Closed",
    ]

    worksheet1.write_row(0, 0, header_eng, header_format)
    i = 1
    for ticket in tickets:

        if ticket.date_opened:
            date_opened = ticket.date_opened.strftime('%Y-%m-%d')
        else:
            date_opened = None

        if ticket.date_closed:
            date_closed = ticket.date_closed.strftime('%Y-%m-%d')
        else:
            date_closed = None

        row_data = [
            ticket.fiscal_year,
            ticket.id,
            ticket.sd_ref_number,
            ticket.section.section_name,
            "{} {}".format(ticket.primary_contact.first_name, ticket.primary_contact.last_name),
            ticket.title,
            ticket.request_type.request_type,
            ticket.estimated_cost,
            ticket.financial_coding,
            ticket.get_status_display(),
            date_opened,
            date_closed,
        ]
        worksheet1.write_row(i, 0, row_data)
        i += 1
    workbook.close()
    return target_url
