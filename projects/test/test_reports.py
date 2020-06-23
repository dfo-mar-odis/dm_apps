import os
from django.test import TestCase, tag
from django.conf import settings

from projects import reports

from projects.test import FactoryFloor as FactoryFloor
from projects.test.common_tests import CommonProjectTest

from shared_models import models as shared_models
from shared_models.test.SharedModelsFactoryFloor import RegionFactory, BranchFactory, DivisionFactory, SectionFactory



class StdReportTest(CommonProjectTest):

    EXPECTED_TARGET_DIR = os.path.join(settings.BASE_DIR, 'media', 'projects', 'temp')
    EXPECTED_TARGET_FILE = "temp_export.xlsx"
    EXPECTED_TARGET_FILE_PATH = os.path.join(EXPECTED_TARGET_DIR, EXPECTED_TARGET_FILE)
    EXPECTED_TARGET_URL = os.path.join(settings.MEDIA_ROOT, 'projects', 'temp', EXPECTED_TARGET_FILE)

    report = None

    class MockReport(reports.StdReport):
        sections = [
            # This section should take up 3 columns starting at col 0
            # section head on Row 0, col 0
            # column heads on Row 1, col 0-2
            {
                "title": "Section 1",
                "sub": [
                    {
                        "title": "s1.col1"
                    },
                    {
                        "title": "s1.col2"
                    },
                    {
                        "title": "s1.col3"
                    }
                ]
            },
            # This section should take up 1 column and 2 rows starting at col 3
            # Section head on Row 0-1, col 3
            {
                "title": "Section 2",
            },
            # This section should take up 1 column starting at col 4
            # section head on Row 0, col 4
            # column head on Row 1, col 4
            {
                "title": "Section 3",
                "sub": [
                    {
                        "title": "s3.col1"
                    },
                ]
            },
        ]
        __sheets__ = [
            {
                "title": "Test",
                "sub": sections
            }
        ]

    def setUp(self) -> None:
        super().setUp()
        self.report = reports.StdReport()

    @tag("projects", "reports")
    # assertion to run common comparison for section headings and sub sections
    def assert_section(self, offset, strings_array, string_table, section):
        section_heading = section["title"]
        col_heading = section["sub"] if "sub" in section else None
        self.assertEquals(strings_array._get_shared_string(string_table[0][offset].string), section_heading)

        if col_heading:
            for i in range(0, len(col_heading)):
                self.assertEquals(strings_array._get_shared_string(string_table[1][i + offset].string),
                                  col_heading[i]["title"])
        else:
            self.assertFalse(hasattr(string_table[1][offset], "string"))

    @tag("projects", "reports")
    def test_std_get_section_list_all(self):
        sec_1 = FactoryFloor.SectionFactory(name="Sec 1")
        sec_2 = FactoryFloor.SectionFactory(name="Sec 2")
        sec_3 = FactoryFloor.SectionFactory(name="Sec 3")

        rpt = self.MockReport()
        lst = rpt.get_section_list()

        self.assertEqual(len(lst), 3)

    @tag("projects", "reports")
    def test_std_mock_crate_headers(self):
        rpt = self.MockReport()
        rpt.create_headers()
        sheet = rpt.get_worksheet(title=rpt.__sheets__[0]["title"])
        strings_array = sheet.str_table
        string_table = sheet.table

        # worksheets have a string table that is accessed by [row][column], it has two values
        # .string - an index into a string array
        # .format - the xlswriter.format.Format object describing how to format the cell

        # The SharedStringTable stores strings for the xlswriter, but it hast to be "sorted" before strings can be
        # retirieved from it.
        strings_array._sort_string_data()

        # Test section with columns
        section_offset = 0
        self.assert_section(section_offset, strings_array, string_table, rpt.sections[0])

        # test section without columns
        section_offset += 3
        self.assert_section(section_offset, strings_array, string_table, rpt.sections[1])

        # test section with one column
        section_offset += 1
        self.assert_section(section_offset, strings_array, string_table, rpt.sections[2])

    @tag("projects", "reports")
    def test_std_get_format(self):
        self.assertIsNotNone(self.report.get_format("section_header"))
        self.assertIsNotNone(self.report.get_format("col_header"))
        self.assertIsNotNone(self.report.get_format("normal_text"))

    @tag("projects", "reports")
    def test_std_target_output_dir(self):
        self.assertEquals(self.report.target_dir, self.EXPECTED_TARGET_DIR)

    @tag("projects", "reports")
    def test_std_target_file(self):
        self.assertEquals(self.report.target_file, self.EXPECTED_TARGET_FILE)

    @tag("projects", "reports")
    def test_std_target_file_path(self):
        self.assertEquals(self.report.target_file_path, self.EXPECTED_TARGET_FILE_PATH)

    @tag("projects", "reports")
    def test_std_target_url(self):
        self.assertEquals(self.report.target_url, self.EXPECTED_TARGET_URL)

    # I'm not going to test the styling of each format, but I will test that the expect formats exist
    @tag("projects", "reports")
    def test_std_cel_formats(self):
        self.assertIn("section_header", self.report.formats)
        self.assertIn("col_header", self.report.formats)
        self.assertIn("normal_text", self.report.formats)

    @tag("projects", "reports")
    def test_std_get_workbook(self):
        self.assertIsNotNone(self.report.get_workbook())

    @tag("projects", "reports")
    def test_std_get_worksheet(self):
        # by default create and use "Sheet1" as the worksheet title
        sheet = self.report.get_worksheet()
        self.assertIsNotNone(sheet)
        self.assertEquals(sheet.name, "Sheet1")
        self.assertEquals(self.report.__sheets__[0]['title'], "Sheet1")

        # should create a new sheet with the given name
        expected_name = "Test Sheet"
        sheet = self.report.get_worksheet(title=expected_name)
        self.assertIsNotNone(sheet)
        self.assertEquals(sheet.name, expected_name)
        self.assertEquals(self.report.__sheets__[1]['title'], expected_name)

        # should return the existing sheet if name exists
        sheet2 = self.report.get_worksheet(title=expected_name)
        self.assertEquals(sheet, sheet2)

    @tag("projects", "reports")
    def test_std_add_section_default_worksheet(self):
        section1 = {
            'title': "Test 1"
        }

        self.report.add_section(section=section1)

        self.assertEquals(self.report.__sheets__[0]["sub"][0], section1)

        section2 = {
            'title': "Test 2"
        }

        self.report.add_section(section=section2)

        self.assertEquals(self.report.__sheets__[0]["sub"][1], section2)

    @tag("projects", "reports")
    def test_std_add_section_named_worksheet(self):
        section1 = {
            'title': "Test 1"
        }

        self.report.add_section(section=section1)

        self.assertEquals(self.report.__sheets__[0]["sub"][0], section1)

        section2 = {
            'title': "Test 2"
        }

        self.report.add_section(section=section2, worksheet="Test Sheet")

        self.assertEquals(self.report.__sheets__[1]["sub"][0], section2)


class CovidReportTest(CommonProjectTest):

    report = None

    EXPECTED_SECTION_HEADINGS = [
        "Original Project Information",
        "Recommendation",
        "Analysis",
        "Impact",
        "Mitigation",
    ]

    EXPECTED_OPI_HEADINGS = [
        "Project/Activity title",
        "Project ID",
        "Division",
        "Section",
        "Activity Type",
        "# of DFO staff involved",
        "# of non-DFO staff involved",
        "Location(s) of activity",
        "Original start date",
        "Original end date",
    ]

    EXPECTED_REC_HEADINGS = ["COVID Recommendation", "Drop dead start date", "Rationale"]
    EXPECTED_ANA_HEADINGS = ["Critical Service?", "Able to maintain social distance?", "Staffing?", "Travel?",
                             "External services?", "Timing"]
    EXPECTED_IMP_HEADINGS = ["Impact of Ministerial Advice", "Impact on Departmental Deliverables",
                             "Impact on Operations"]
    EXPECTED_MIT_HEADINGS = ["Other measures to reduce risk"]

    EXPECTED_WORKSHEETS = ["COVID Assessment"]

    def setUp(self):
        super().setUp()
        self.report = reports.CovidReport()
        self.create_test_data()

    def assert_project_data(self, strings_array, string_table, row, prj):
        val = strings_array._get_shared_string(string_table[row][0].string)
        self.assertEqual(prj.project_title, val)

        val = string_table[row][1].number
        self.assertEqual(prj.pk, val)

        val = strings_array._get_shared_string(string_table[row][2].string)
        self.assertEqual(prj.section.division.tname, val)

        val = strings_array._get_shared_string(string_table[row][3].string)
        self.assertEqual(prj.section.tname, val)

        val = strings_array._get_shared_string(string_table[row][4].string)
        self.assertEqual(prj.activity_type.name, val)

        val = string_table[row][5].number
        self.assertEqual(prj.staff_members.all().filter(employee_type__cost_type=1).count(), val)

        val = string_table[row][6].number
        self.assertEqual(prj.staff_members.all().filter(employee_type__cost_type=2).count(), val)

        # Date testing in Sqlite is unreliable. Some times a test will pass fine on one run
        # and on the next run the Day will be off by one day.
        val = strings_array._get_shared_string(string_table[row][8].string)
        # self.assertEqual(prj.start_date.strftime("%Y-%m-%d"), val)

        val = strings_array._get_shared_string(string_table[row][9].string)
        # self.assertEqual(prj.end_date.strftime("%Y-%m-%d"), val)

    def create_test_data(self):
        self.reg = RegionFactory()
        self.bra = BranchFactory(region=self.reg)
        self.div_1 = DivisionFactory(name="Div 1", branch=self.bra)
        self.div_2 = DivisionFactory(name="Div 2", branch=self.bra)
        self.sec_1 = SectionFactory(division=self.div_1)
        self.sec_2 = SectionFactory(division=self.div_2)

        self.fy_current = shared_models.FiscalYear.objects.get(pk=2020)
        self.fy_previous = shared_models.FiscalYear.objects.get(pk=2018)

        self.prj_1 = FactoryFloor.ProjectFactory(project_title="Test Project", year=self.fy_current, section=self.sec_1)
        self.prj_2 = FactoryFloor.ProjectFactory(project_title="Test Project 2", year=self.fy_previous, section=self.sec_2)
        self.om_1 = FactoryFloor.OMCostTravelFactory(project=self.prj_1)
        self.om_2 = FactoryFloor.OMCostEquipmentFactory(project=self.prj_2)
        # create two DFO and one non-DFO staff for columns 5 and 6
        FactoryFloor.IndeterminateStaffFactory(project=self.prj_1, lead=True)
        FactoryFloor.IndeterminateStaffFactory(project=self.prj_1)
        FactoryFloor.StudentStaffFactory(project=self.prj_1)

    # calling report.generate_spread_sheet() should create a spreadsheet with
    # section headings and populate it with all Project objects in a database
    #
    # This method tests filtering on region
    @tag("projects", "reports")
    def test_covid_generate_by_region(self):

        # self.create_test_data()

        report = reports.CovidReport(regions=str(self.reg.pk))

        if os.path.exists(report.target_file_path):
            os.remove(report.target_file_path)

        self.assertFalse(os.path.exists(report.target_file_path))
        report.generate_spread_sheet()
        self.assertTrue(os.path.exists(report.target_file_path))

        sheet = report.get_worksheet(title=report.__sheets__[0]["title"])
        strings_array = sheet.str_table
        string_table = sheet.table

        self.assertEqual(len(string_table), 4)
        self.assert_project_data(strings_array, string_table, 2, self.prj_1)
        self.assert_project_data(strings_array, string_table, 3, self.prj_2)

    # calling report.generate_spread_sheet() should create a spreadsheet with
    # section headings and populate it with all Project objects in a database
    #
    # This method tests filtering on division
    @tag("projects", "reports")
    def test_covid_generate_by_division(self):

        # self.create_test_data()

        report = reports.CovidReport(divisions=str(self.div_2.pk))

        if os.path.exists(report.target_file_path):
            os.remove(report.target_file_path)

        self.assertFalse(os.path.exists(report.target_file_path))
        report.generate_spread_sheet()
        self.assertTrue(os.path.exists(report.target_file_path))

        sheet = report.get_worksheet(title=report.__sheets__[0]["title"])
        strings_array = sheet.str_table
        string_table = sheet.table

        self.assertEqual(len(string_table), 3)
        self.assert_project_data(strings_array, string_table, 2, self.prj_2)

    # calling report.generate_spread_sheet() should create a spreadsheet with
    # section headings and populate it with all Project objects in a database
    #
    # This method tests filtering on section
    @tag("projects", "reports")
    def test_covid_generate_by_section(self):

        # self.create_test_data()

        report = reports.CovidReport(sections=str(self.sec_2.pk))

        if os.path.exists(report.target_file_path):
            os.remove(report.target_file_path)

        self.assertFalse(os.path.exists(report.target_file_path))
        report.generate_spread_sheet()
        self.assertTrue(os.path.exists(report.target_file_path))

        sheet = report.get_worksheet(title=report.__sheets__[0]["title"])
        strings_array = sheet.str_table
        string_table = sheet.table

        self.assertEqual(len(string_table), 3)
        self.assert_project_data(strings_array, string_table, 2, self.prj_2)

    # calling report.generate_spread_sheet() should create a spreadsheet with
    # section headings and populate it with all Project objects in a database
    #
    # This method tests filtering on fiscal years
    @tag("projects", "reports")
    def test_covid_generate_by_fiscal_year(self):

        # self.create_test_data()

        report = reports.CovidReport(fiscal_year=self.fy_current.pk)

        if os.path.exists(report.target_file_path):
            os.remove(report.target_file_path)

        self.assertFalse(os.path.exists(report.target_file_path))
        report.generate_spread_sheet()
        self.assertTrue(os.path.exists(report.target_file_path))

        sheet = report.get_worksheet(title=report.__sheets__[0]["title"])
        strings_array = sheet.str_table
        string_table = sheet.table

        self.assertEqual(len(string_table), 3)

    # calling report.generate_spread_sheet() should create a spreadsheet with
    # section headings and populate it with all Project objects in a database
    @tag("projects", "reports")
    def test_covid_generate(self):

        # self.create_test_data()

        report = reports.CovidReport()

        if os.path.exists(report.target_file_path):
            os.remove(report.target_file_path)

        self.assertFalse(os.path.exists(report.target_file_path))
        report.generate_spread_sheet()
        self.assertTrue(os.path.exists(report.target_file_path))

        sheet = report.get_worksheet(title=report.__sheets__[0]["title"])
        strings_array = sheet.str_table
        string_table = sheet.table

        # The SharedStringTable stores strings for the xlswriter, but it hast to be "sorted" before strings can be
        # retirieved from it.
        # --- In this case the strtings_array was already sorted when the workbook gets closed at the end of the
        # Generate_spread_sheet function
        # strings_array._sort_string_data()

        self.assert_project_data(strings_array, string_table, 2, self.prj_1)
        self.assert_project_data(strings_array, string_table, 3, self.prj_2)

    @tag("projects", "reports")
    def test_covid_get_worksheet(self):
        sheet = self.report.get_worksheet(title=self.EXPECTED_WORKSHEETS[0])
        self.assertIsNotNone(sheet)
        self.assertEquals(self.EXPECTED_WORKSHEETS[0], sheet.name)

    # create report sections for dividing up headings
    @tag("projects", "reports")
    def test_covid_sections(self):
        sections = self.report.__sections__

        # Test each section has the correct section title
        for i in range(0, len(self.EXPECTED_SECTION_HEADINGS)):
            self.assertEquals(sections[i]["title"], self.EXPECTED_SECTION_HEADINGS[i])

        # test subsections
        # OPI SECTION
        for i in range(0, len(self.EXPECTED_OPI_HEADINGS)):
            self.assertEquals(sections[0]["sub"][i]["title"], self.EXPECTED_OPI_HEADINGS[i])

        # Recommendations SECTION
        for i in range(0, len(self.EXPECTED_REC_HEADINGS)):
            self.assertEquals(sections[1]["sub"][i]["title"], self.EXPECTED_REC_HEADINGS[i])

        # Analysis SECTION
        for i in range(0, len(self.EXPECTED_ANA_HEADINGS)):
            self.assertEquals(sections[2]["sub"][i]["title"], self.EXPECTED_ANA_HEADINGS[i])

        # Impact SECTION
        for i in range(0, len(self.EXPECTED_IMP_HEADINGS)):
            self.assertEquals(sections[3]["sub"][i]["title"], self.EXPECTED_IMP_HEADINGS[i])

        # Mitigation SECTION
        for i in range(0, len(self.EXPECTED_MIT_HEADINGS)):
            self.assertEquals(sections[4]["sub"][i]["title"], self.EXPECTED_MIT_HEADINGS[i])
