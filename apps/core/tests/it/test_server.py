from django.test import TestCase
from selenium import webdriver


# commented out for now because of github actions
# class TestFunctional(TestCase):

#     # getting browser ready
#     def setUp(self):
#         self.browser = webdriver.Firefox()

#     def test_homepage_running(self):
#         self.browser.get('http://127.0.0.1:8000')
#         self.assertIn('install', self.browser.page_source)

#     # closing browser after testing
#     def tearDown(self):
#         self.browser.quit()
