from django.test import TestCase
from selenium import webdriver

# Create your tests here.


class FunctionalTestCase(TestCase):

    # getting browser ready
    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_homepage_running(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('install', self.browser.page_source)

    # closing browser after testing
    def tearDown(self):
        self.browser.quit()