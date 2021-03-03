from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from django.test import tag
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select

from bio_diversity.models import EventCode, LocCode, Tank, ProtoCode, Pairing, EnvCode, Program, StockCode
from bio_diversity.test import BioFactoryFloor
from shared_models.test.SharedModelsFactoryFloor import UserFactory, GroupFactory
from django.contrib.auth.models import User


class CommonFunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        super().setUp()  # used to import fixtures
        # need to download the webdriver and stick it in the path/point to it here:
        # can be downloaded from: https://chromedriver.chromium.org/downloads
        self.browser = webdriver.Chrome('bio_diversity/test/functional_test/chromedriver.exe')
        self.browser.maximize_window()
        # generate a user
        user_data = UserFactory.get_valid_data()
        self.user = User.objects.create_superuser(username=user_data['username'], email=user_data['email1'],
                                                  password=UserFactory.get_test_password())
        bio_group = GroupFactory(name='bio_diversity_admin')
        self.user.groups.add(bio_group)
        self.user.first_name = user_data["first_name"]
        self.user.last_name = user_data["last_name"]
        self.user.save()

        self.browser.get(self.live_server_url + '/en/')
        self.client.force_login(self.user)  # Native django test client
        cookie = self.client.cookies['sessionid']  # grab the login cookie
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.browser.refresh()  # selenium will set cookie domain based on current page domain

    def tearDown(self):
        # self.browser.quit()  # causes connection was forcibly closed errors due to chrome being out of date
        super().tearDown()


def scroll_n_click(driver, element):
    # scroll to bring element to bottom of screen, then scroll up once to move element off of banners and click on it
    driver.execute_script("arguments[0].scrollIntoView(false);", element)
    driver.implicitly_wait(5)
    driver.execute_script("window.scrollBy(0,50)")
    element.click()


def get_col_val(row, col):
    # get text in col'th column of a row on list view
    return row.find_elements_by_tag_name("td")[col].text


def fill_n_submit_form(browser, data, exclude=[]):
    # browser must be on a create page
    # data should be a dict output from a factory build_valid_data method
    for field_key in data.keys():
        if field_key not in exclude:
            form_field = browser.find_element_by_xpath("//*[@name='{}']".format(field_key))
            if field_key[-3:] == "_id":
                # foreign key fields
                select = Select(form_field)
                select.select_by_value(str(data[field_key]))
            elif 'date' in form_field.get_attribute("class") and field_key not in ["created_date"]:
                # date fields
                browser.execute_script('document.getElementsByName("{}")[0].removeAttribute("readonly")'
                                       .format(field_key))
                form_field.clear()
                form_field.send_keys(str(data[field_key]))
            elif field_key not in ["created_by", "created_date"]:
                # text fields
                form_field.send_keys(str(data[field_key]).replace("\n", " "))
    submit_btn = browser.find_element_by_xpath("//button[@class='btn btn-success']")
    scroll_n_click(browser, submit_btn)


def open_n_fill_popup(self, button, data, parent_code=""):
    # self should be a common functional test class
    # button should be a clickable element that opens a pop up create form
    scroll_n_click(self.browser, button)
    self.browser.switch_to.window(self.browser.window_handles[1])

    if parent_code:
        fill_n_submit_form(self.browser, data, ["{}_id".format(parent_code)])
    else:
        fill_n_submit_form(self.browser, data)
    self.browser.switch_to.window(self.browser.window_handles[0])
    self.browser.refresh()


def add_feature(self, feature_data, feature_tag, object_tag="", clone=False):
    # browser must be on details view with the feature.
    # feature data should be output from factory.build_valid_data()
    # returns rows in details table to be compared with input feature data

    # user adds a feature to the object from the object's detail page
    feature_details = self.browser.find_element_by_xpath('//div[@name="{}-details"]'.format(feature_tag))
    if clone:
        # will probably break if there are multiple instances in details table...
        feature_btn = feature_details.find_element_by_xpath('//a[@name="clone-{}-btn"]'.format(feature_tag))
    else:
        feature_btn = feature_details.find_element_by_xpath('//a[@name="add-new-{}-btn"]'.format(feature_tag))
    open_n_fill_popup(self, feature_btn, feature_data, object_tag)
    try:
        details_table = self.browser.find_element_by_xpath("//div[@name='{}-details']//table/tbody".format(feature_tag))
    except NoSuchElementException:
        return self.fail("No {} features in details table".format(feature_tag))
    rows = details_table.find_elements_by_tag_name("tr")
    return rows


@tag("Functional", "Basic")
class TestHomePageTitle(CommonFunctionalTest):

    def test_home_page_title(self):
        self.browser.get(self.live_server_url)
        self.assertIn('DM Apps', self.browser.title, "not on correct page")
        biod_btn = self.browser.find_element_by_xpath("//h4[contains(text(), 'Biodiversity')]")
        scroll_n_click(self.browser, biod_btn)
        self.assertIn('Biodiversity', self.browser.title, "not on correct page")


@tag("Functional", "Evnt")
class TestEvntFunctional(CommonFunctionalTest):
    # put factories in setUp and not in class to make factory boy use selenium database.
    def setUp(self):
        super().setUp()
        self.object_verbose = 'Event'
        self.object_data = BioFactoryFloor.EvntFactory.build_valid_data()

    def test_create_interaction(self):
        # user starts on app homepage:
        self.browser.get("{}{}".format(self.live_server_url, "/en/bio_diversity/"))

        # user clicks on a common lookup, ends up a list view
        lookup_btn = self.browser.find_element_by_xpath("//a[@class='btn btn-secondary btn-lg' and contains(text(), "
                                                        "'{}')]".format(self.object_verbose))
        scroll_n_click(self.browser, lookup_btn)
        self.assertIn(self.object_verbose, self.browser.title, "not on correct page")

        # user creates a new instance of the lookup
        self.browser.find_element_by_xpath("//a[@class='btn btn-primary' and contains(text(), '+')]").click()
        fill_n_submit_form(self.browser, self.object_data)

        # user checks to make sure that the instance is created
        details_table = self.browser.find_element_by_xpath("//table[@id='details_table']/tbody")
        evntc_used = EventCode.objects.filter(pk=self.object_data["evntc_id"]).get().__str__()
        rows = details_table.find_elements_by_tag_name("tr")
        self.assertIn(evntc_used, [get_col_val(row, 1) for row in rows])


@tag("Functional", "Evnt")
class TestEvntDetailsFunctional(CommonFunctionalTest):
    # put factories in setUp and not in class to make factory boy use selenium database.
    def setUp(self):
        super().setUp()
        self.evnt_data = BioFactoryFloor.EvntFactory()
        self.evnt_data.prog_id.valid = True

    def nav_to_details_view(self):
        # user navigates to a details view for an event
        self.browser.get("{}{}{}".format(self.live_server_url, "/en/bio_diversity/details/evnt/", self.evnt_data.id))
        self.assertIn('Event', self.browser.title, "not on correct page")

    def test_add_locations(self):
        self.nav_to_details_view()
        # user adds a location to the event
        location_data = BioFactoryFloor.LocFactory.build_valid_data()
        rows = add_feature(self, location_data, "loc", "evnt")
        locc_used = LocCode.objects.filter(pk=location_data["locc_id"]).get().__str__()
        self.assertIn(locc_used, [get_col_val(row, 0) for row in rows])

    def test_add_individual(self):
        self.nav_to_details_view()
        # user adds a new individual to the event
        indv_data = BioFactoryFloor.IndvFactory.build_valid_data()
        rows = add_feature(self, indv_data, "indv", "")
        ufid_used = indv_data["ufid"]
        self.assertIn(ufid_used, [get_col_val(row, 0) for row in rows])

    def test_add_existing_individual_nav_back_btn(self):
        self.nav_to_details_view()
        # user adds an existing individual to the event:
        indv = BioFactoryFloor.IndvFactory()
        indv_details = self.browser.find_element_by_xpath('//div[@name="indv-details"]')
        indv_btn = indv_details.find_element_by_xpath('//a[@name="add-existing_indv-btn"]')
        indv_data = {"indv_id": indv.pk}
        open_n_fill_popup(self, indv_btn, indv_data)
        try:
            details_table = self.browser.find_element_by_xpath("//div[@name='indv-details']//table/tbody")
        except NoSuchElementException:
            return self.fail("No individuals in details table")
        ufid_used = indv.ufid
        rows = details_table.find_elements_by_tag_name("tr")
        self.assertIn(ufid_used, [get_col_val(row, 0) for row in rows])

        # User clicks on first individual reviews its details and returns to the event details
        first_ufid = rows[0].find_element_by_tag_name("td").text
        indv_btn = rows[0].find_element_by_name("indv-details-btn")
        scroll_n_click(self.browser, indv_btn)
        description_ufid = self.browser.find_element_by_xpath("//span[@class='font-weight-bold' and contains(text(), "
                                                              "'ABL Fish UFID :')]/following-sibling::span")
        self.assertEqual(first_ufid, description_ufid.text)
        self.browser.find_element_by_name("back-btn").click()
        try:
            details_table = self.browser.find_element_by_xpath("//div[@name='indv-details']//table/tbody")
        except NoSuchElementException:
            return self.fail("No individuals in details table")
        rows = details_table.find_elements_by_tag_name("tr")
        self.assertIn(first_ufid, [get_col_val(row, 0) for row in rows])

    def test_clone_individual(self):
        self.nav_to_details_view()

        # user adds a new individual to the event
        indv_data = BioFactoryFloor.IndvFactory.build_valid_data()
        rows = add_feature(self, indv_data, "indv", "")
        ufid_used = indv_data["ufid"]
        self.assertIn(ufid_used, [get_col_val(row, 0) for row in rows])

        # user clones this indivdual:
        indv_clone_data = {"ufid": "new_ufid"}
        rows = add_feature(self, indv_clone_data, "indv", "", True)
        self.assertIn("new_ufid", [get_col_val(row, 0) for row in rows])

    def test_add_group(self):
        self.nav_to_details_view()
        # user adds a new individual to the event
        grp_data = BioFactoryFloor.GrpFactory.build_valid_data()
        rows = add_feature(self, grp_data, "grp", "")
        stok_used = StockCode.objects.filter(pk=grp_data["stok_id"]).get().__str__()
        self.assertIn(stok_used, [get_col_val(row, 0) for row in rows])

    def test_add_contx(self):
        self.nav_to_details_view()
        # user add a container cross reference to the event
        contx_data = BioFactoryFloor.ContxFactory.build_valid_data()
        rows = add_feature(self, contx_data, "contx", "evnt")
        tank_used = Tank.objects.filter(pk=contx_data["tank_id"]).get().__str__()
        self.assertIn(tank_used, [get_col_val(row, 0) for row in rows])

    def test_add_protocol(self):
        self.nav_to_details_view()
        # user adds a protocol to the event
        prot_data = BioFactoryFloor.ProtFactory.build_valid_data()
        prot_data["valid"] = True
        prot_data["evntc_id"] = self.evnt_data.evntc_id.id
        evnt_prog = Program.objects.filter(pk=self.evnt_data.prog_id.id).get()
        evnt_prog.valid = True
        evnt_prog.save()
        rows = add_feature(self, prot_data, "prot", "prog")
        evntc_used = EventCode.objects.filter(pk=prot_data["evntc_id"]).get().__str__()
        self.assertIn(evntc_used, [get_col_val(row, 0) for row in rows])


@tag("Functional", "Instc")
class InstcTestSimpleLookup(CommonFunctionalTest):

    def setUp(self):
        super().setUp()
        self.lookup_verbose = 'Instrument Code'
        self.lookup_data = BioFactoryFloor.InstcFactory.build_valid_data()

    def test_full_interaction(self):
        # user starts on app homepage:
        self.browser.get("{}{}".format(self.live_server_url, "/en/bio_diversity/"))

        # user clicks on a common lookup, ends up a list view
        lookup_btn = self.browser.find_element_by_xpath("//a[@class='btn btn-secondary btn-lg' and contains(text(), "
                                                        "'{}')]".format(self.lookup_verbose))
        scroll_n_click(self.browser, lookup_btn)
        self.assertIn(self.lookup_verbose, self.browser.title, "not on correct page")

        # user creates a new instance of the lookup
        self.browser.find_element_by_xpath("//a[@class='btn btn-primary' and contains(text(), '+')]").click()
        fill_n_submit_form(self.browser, self.lookup_data)

        # user checks to make sure that the instance is created
        details_table = self.browser.find_element_by_xpath("//table[@id='details_table']/tbody")
        rows = details_table.find_elements_by_tag_name("tr")
        self.assertIn(self.lookup_data["name"], [get_col_val(row, 0) for row in rows])

        # user looks at details of newly created object:
        new_object_row = False
        for row in rows:
            name_cell = row.find_elements_by_tag_name("td")[0]
            if name_cell.text == self.lookup_data["name"]:
                new_object_row = row
        new_object_row.find_element_by_xpath("//a[@class='btn btn-primary btn-sm my-1' and contains(text(), "
                                             "'Details')]").click()
        description_detail_element = self.browser.find_element_by_xpath("//span[@class='font-weight-bold'and "
                                                                        "contains(text(), 'Description (en) : ')]"
                                                                        "/following-sibling::span")
        self.assertEqual(description_detail_element.text, self.lookup_data["description_en"].replace("\n", " "),
                         "Description does not match input")

        # user updates the instances details and goes on their way
        self.browser.find_element_by_xpath("//a[@class='btn btn-primary' and@title='Update']").click()
        name_field = self.browser.find_element_by_xpath("//input[@name='name']")
        name_field.clear()
        new_name = "updated name"
        name_field.send_keys(new_name)
        submit_btn = self.browser.find_element_by_xpath("//button[@class='btn btn-success']")
        scroll_n_click(self.browser, submit_btn)

        details_table = self.browser.find_element_by_xpath("//table[@id='details_table']/tbody")
        rows = details_table.find_elements_by_tag_name("tr")  # get all of the rows in the table
        self.assertNotIn(self.lookup_data["name"], [get_col_val(row, 0) for row in rows])
        self.assertIn(new_name, [get_col_val(row, 0) for row in rows])


@tag("Functional", "Instdc")
class InstdcTestSimpleLookup(CommonFunctionalTest):

    def setUp(self):
        super().setUp()
        self.lookup_verbose = 'Instrument Detail Code'
        self.lookup_data = BioFactoryFloor.InstdcFactory.build_valid_data()

    def test_full_interaction(self):
        # user starts on app homepage:
        self.browser.get("{}{}".format(self.live_server_url, "/en/bio_diversity/"))

        # user clicks on a common lookup, ends up a list view
        lookup_btn = self.browser.find_element_by_xpath("//a[@class='btn btn-secondary btn-lg' and contains(text(), "
                                                        "'{}')]".format(self.lookup_verbose))
        scroll_n_click(self.browser, lookup_btn)
        self.assertIn(self.lookup_verbose, self.browser.title, "not on correct page")

        # user creates a new instance of the lookup
        self.browser.find_element_by_xpath("//a[@class='btn btn-primary' and contains(text(), '+')]").click()
        fill_n_submit_form(self.browser, self.lookup_data)

        # user checks to make sure that the instance is created
        details_table = self.browser.find_element_by_xpath("//table[@id='details_table']/tbody")
        rows = details_table.find_elements_by_tag_name("tr")
        self.assertIn(self.lookup_data["name"], [get_col_val(row, 0) for row in rows])

        # user looks at details of newly created object:
        new_object_row = False
        for row in rows:
            name_cell = row.find_elements_by_tag_name("td")[0]
            if name_cell.text == self.lookup_data["name"]:
                new_object_row = row

        new_object_row.find_element_by_xpath("//a[@class='btn btn-primary btn-sm my-1' and contains(text(), "
                                             "'Details')]").click()
        description_detail_element = self.browser.find_element_by_xpath("//span[@class='font-weight-bold'and "
                                                                        "contains(text(), 'Description (en) : ')]"
                                                                        "/following-sibling::span")
        self.assertEqual(description_detail_element.text, self.lookup_data["description_en"].replace("\n", " "),
                         "Description does not match input")

        # user updates the instances details and goes on their way
        self.browser.find_element_by_xpath("//a[@class='btn btn-primary' and@title='Update']").click()
        name_field = self.browser.find_element_by_xpath("//input[@name='name']")
        name_field.clear()
        new_name = "updated name"
        name_field.send_keys(new_name)
        submit_btn = self.browser.find_element_by_xpath("//button[@class='btn btn-success']")
        scroll_n_click(self.browser, submit_btn)

        details_table = self.browser.find_element_by_xpath("//table[@id='details_table']/tbody")
        rows = details_table.find_elements_by_tag_name("tr")  # get all of the rows in the table
        self.assertNotIn(self.lookup_data["name"], [get_col_val(row, 0) for row in rows])
        self.assertIn(new_name, [get_col_val(row, 0) for row in rows])


@tag("Functional", "Loc")
class TestLocDetailsFunctional(CommonFunctionalTest):
    # put factories in setUp and not in class to make factory boy use selenium database.
    def setUp(self):
        super().setUp()
        self.loc_data = BioFactoryFloor.LocFactory()

    def nav_to_details_view(self):
        # user navigates to a details view for a location
        self.browser.get("{}{}{}".format(self.live_server_url, "/en/bio_diversity/details/loc/", self.loc_data.id))
        self.assertIn('Location', self.browser.title, "not on correct page")

    def test_add_env(self):
        self.nav_to_details_view()

        # user adds a new environment condition to the location
        env_data = BioFactoryFloor.EnvFactory.build_valid_data()
        rows = add_feature(self, env_data, "env", "loc")
        envc_used = EnvCode.objects.filter(pk=env_data["envc_id"]).get().__str__()
        self.assertIn(envc_used, [get_col_val(row, 0) for row in rows])


@tag("Functional", "Prog")
class TestProgDetailsFunctional(CommonFunctionalTest):
    # put factories in setUp and not in class to make factory boy use selenium database.
    def setUp(self):
        super().setUp()
        self.prog_data = BioFactoryFloor.ProgFactory(valid=True)

    def nav_to_details_view(self):
        # user navigates to a details view for a program
        self.browser.get("{}{}{}".format(self.live_server_url, "/en/bio_diversity/details/prog/", self.prog_data.id))
        self.assertIn('Program', self.browser.title, "not on correct page")

    def test_add_protocol_nav_back_btn(self):
        self.nav_to_details_view()

        # user adds a new protocol to the program
        prot_data = BioFactoryFloor.ProtFactory.build_valid_data()
        rows = add_feature(self, prot_data, "prot", "prog")
        protc_used = ProtoCode.objects.filter(pk=prot_data["protc_id"]).get().__str__()
        self.assertIn(protc_used, [get_col_val(row, 0) for row in rows])

        # User clicks on first protocol, reviews its details and returns to the program details
        try:
            details_table = self.browser.find_element_by_xpath("//div[@name='prot-details']//table/tbody")
        except NoSuchElementException:
            return self.fail("No protocols in details table")
        rows = details_table.find_elements_by_tag_name("tr")
        first_protc = rows[0].find_element_by_tag_name("td").text
        scroll_n_click(self.browser, rows[0])
        description_ufid = self.browser.find_element_by_xpath("//span[@class='font-weight-bold' and contains(text(), "
                                                              "'Protocol Code :')]/following-sibling::span")
        self.assertEqual(first_protc, description_ufid.text)
        self.browser.find_element_by_name("back-btn").click()
        try:
            details_table = self.browser.find_element_by_xpath("//div[@name='prot-details']//table/tbody")
        except NoSuchElementException:
            return self.fail("No protocols in details table")
        rows = details_table.find_elements_by_tag_name("tr")
        self.assertIn(first_protc, [get_col_val(row, 0) for row in rows])


@tag("Functional", "Prot")
class TestProtDetailsFunctional(CommonFunctionalTest):
    # put factories in setUp and not in class to make factory boy use selenium database.
    def setUp(self):
        super().setUp()
        self.prot_data = BioFactoryFloor.ProtFactory(valid=True)
        self.prot_data.prog_id.valid = True

    def nav_to_details_view(self):
        # user navigates to a details view for a protocol
        self.browser.get("{}{}{}".format(self.live_server_url, "/en/bio_diversity/details/prot/", self.prot_data.id))
        self.assertIn('Protocol', self.browser.title, "not on correct page")

    def test_add_protf(self):
        self.nav_to_details_view()

        # user adds a new protocol file to the protocol
        protf_data = BioFactoryFloor.ProtfFactory.build_valid_data()
        rows = add_feature(self, protf_data, "protf", "prot")
        self.assertTrue(len(rows) > 0)
