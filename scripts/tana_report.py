import xlsxwriter as xlsxwriter

from projects import models
from shared_models import models as shared_models


def generate_tana_report():
    output_file = "Tana_report.xls"

    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(output_file)
    worksheet1 = workbook.add_worksheet(name="Tana's Tab")

    # create formatting
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#8C96A0', "align": 'normal',
         "text_wrap": True})

    normal_format = workbook.add_format({"align": 'left', "valign": 'top', "text_wrap": True})

    header = [
        "REGION",
        "FISCAL YEAR",
        "SUBMITTED",
        "PRJ_ID",
        "PRJ_TITLE",
        "SECTION",
        "DIVISION",
        "TAGS/KEYWORDS",
        "PRJ_LEAD",
        "PRJ_STAFF",
        "PRJ_COLLABORATORS"
    ]

    worksheet1.write_row(0, 0, header, header_format)

    region = shared_models.Region.objects.get(name="Maritimes")
    section_list = shared_models.Section.objects.filter(division__branch__region_id=region.id)
    fiscal_year = shared_models.FiscalYear.objects.get(full="2020-2021")
    project_list = models.Project.objects.filter(section__in=section_list, year=fiscal_year, submitted=True)

    row = 1
    for project in project_list:
        staff_list = ','.join(map(str, models.Staff.objects.filter(project=project)))

        collab_list = ','.join(map(str, models.Collaborator.objects.filter(project=project)))

        tags = ','.join(map(str, project.tags.all()))

        data = [str(region), str(project.year), str(project.submitted), str(project.id), str(project.project_title),
                str(project.section), str(project.section.division), str(tags), str(project.project_leads),
                str(staff_list), str(collab_list)]

        worksheet1.write_row(row, 0, data, normal_format)
        row += 1

    workbook.close()


generate_tana_report()
