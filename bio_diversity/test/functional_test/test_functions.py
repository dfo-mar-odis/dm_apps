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
                form_field.clear()
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


@tag("Functional", "Indv")
class TestIndvFunctional(CommonFunctionalTest):
    # put factories in setUp and not in class to make factory boy use selenium database.
    def setUp(self):
        super().setUp()
        self.object_verbose = 'Individual'
        self.object_data = BioFactoryFloor.IndvFactory()

    def test_create_interaction(self):
        # user starts on app homepage:
        self.browser.get("{}{}".format(self.live_server_url, "/en/bio_diversity/"))

        # user clicks on a common lookup, ends up a list view
        lookup_btn = self.browser.find_element_by_xpath("//a[@class='btn btn-secondary btn-lg' and contains(text(), "
                                                        "'{}')]".format(self.object_verbose))
        scroll_n_click(self.browser, lookup_btn)
        self.assertIn(self.object_verbose, self.browser.title, "not on correct page")

        # user checks to make sure that the instance is created
        details_table = self.browser.find_element_by_xpath("//table[@id='details_table']/tbody")
        stok_used = self.object_data.stok_id.__str__()
        rows = details_table.find_elements_by_tag_name("tr")
        self.assertIn(stok_used, [get_col_val(row, 2) for row in rows])


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
