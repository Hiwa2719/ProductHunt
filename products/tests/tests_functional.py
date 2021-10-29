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

    def test_getting_index_view(self):
        self.assertIn('Navbar', self.browser.page_source)
        self.assertIn('Login', self.browser.page_source)
        self.assertIn('Signup', self.browser.page_source)
        self.assertIn('CPU', self.browser.page_source)

    def test_getting_login_page(self):
        """test accessing to login page"""
        self.browser.find_element_by_id('login').click()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#id_username')))
        self.assertEqual(self.live_server_url + reverse('login'), self.browser.current_url)
        self.assertTrue(self.browser.find_element_by_id('id_password'))

    def test_getting_signup_page(self):
        """test accessing signup page"""
        self.browser.find_element_by_id('signup').click()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#id_password2')))
        self.assertEqual(self.live_server_url + reverse('signup'), self.browser.current_url)
        self.assertTrue(self.browser.find_element_by_id('id_password1'))

    def test_clicking_on_vote(self):
        """test clicking on vote button on index page"""
        self.browser.find_elements_by_class_name('vote')[1].click()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#id_username')))
        pattern = self.live_server_url + reverse('login') + r'\?next=/products/vote/[0-9]+/'
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
