import re

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

User = get_user_model()


class PublicFunctionalTests(StaticLiveServerTestCase):
    fixtures = ['fixtures/database2.json']

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.wait = WebDriverWait(self.browser, 10)
        self.browser.get(self.live_server_url + reverse('index'))
        self.login_url = self.live_server_url + reverse('login')

    def test_getting_index_view(self):
        self.assertIn('Navbar', self.browser.page_source)
        self.assertIn('Login', self.browser.page_source)
        self.assertIn('Signup', self.browser.page_source)
        self.assertIn('CPU', self.browser.page_source)

    def test_getting_login_page(self):
        """test accessing to login page"""
        self.browser.find_element_by_id('login').click()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#id_username')))
        self.assertEqual(self.login_url, self.browser.current_url)
        self.assertTrue(self.browser.find_element_by_id('id_password'))

    def test_getting_signup_page(self):
        """test accessing signup page"""
        self.browser.find_element_by_id('signup').click()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#id_password2')))
        self.assertEqual(self.live_server_url + reverse('signup'), self.browser.current_url)
        self.browser.find_element_by_id('id_username').send_keys('George_W_bush')
        self.browser.find_element_by_id('id_password1').send_keys('HiWa_asdf')
        self.browser.find_element_by_id('id_password2').send_keys('HiWa_asdf')
        self.browser.find_element_by_css_selector('input[type="submit"]').click()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#id_username')))
        self.assertEqual(self.browser.current_url, self.login_url)

    def test_clicking_on_vote(self):
        """test clicking on vote button on index page"""
        self.browser.find_elements_by_class_name('vote')[1].click()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#id_username')))
        pattern = self.login_url + r'\?next=/products/vote/[0-9]+/'
        match = re.search(pattern, self.browser.current_url)
        self.assertTrue(match)

    def test_getting_to_product_detail_page(self):
        product = self.browser.find_elements_by_class_name('product-item')[0]
        href = product.get_attribute('href')
        product.click()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img')))
        self.assertEqual(href, self.browser.current_url)

    def tearDown(self) -> None:
        self.browser.quit()


class PrivateFunctionalTestCase(StaticLiveServerTestCase):
    fixtures = ['fixtures/database2.json']

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.wait = WebDriverWait(self.browser, 10)
        self.index_url = self.live_server_url + reverse('index')
        self.login_url = self.live_server_url + reverse('login')
        self.login()

    def login(self):
        self.browser.get(self.login_url)
        self.browser.find_element_by_id('id_username').send_keys('hiwa@gmail.com')
        self.browser.find_element_by_id('id_password').send_keys('asdf')
        self.browser.find_element_by_css_selector('input[value="Login"]').click()
        self.wait.until(EC.url_to_be(self.index_url))
        self.assertTrue(self.browser.find_element_by_id('logout'))

    def test_vote(self):
        pass

    def test_creating_a_product(self):
        pass

    def test_logout(self):
        pass

    def tearDown(self) -> None:
        self.browser.quit()
