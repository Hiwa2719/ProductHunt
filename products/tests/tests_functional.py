from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

User = get_user_model()


class PublicFunctionalTests(StaticLiveServerTestCase):
    fixtures = ['fixtures/database.json']

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.wait = WebDriverWait(self.browser, 10)
        self.browser.get(self.live_server_url + reverse('index'))

    def test_getting_index_view(self):
        self.assertIn('Navbar', self.browser.page_source)
        self.assertIn('Login', self.browser.page_source)
        self.assertIn('Signup', self.browser.page_source)
        self.assertIn('CPU', self.browser.page_source)

    def test_getting_login_page(self):
        """test accessing to login page"""
        self.browser.find_element_by_id('login').click()

    def tearDown(self) -> None:
        self.browser.quit()
