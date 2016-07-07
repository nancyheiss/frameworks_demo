import json
import os
import unittest
import random
import sys

from nose_parameterized import parameterized
from sauceclient import SauceClient
from selenium import webdriver

import page


sauce_client = SauceClient(YOUR_SAUCE_USERNAME, YOUR_SAUCE_ACCESS_KEY)


class PythonOrgSearch(unittest.TestCase):
    """A sample test class to show how page object works"""
    
    def setUp(self):
        # Configure the SAUCE_ONDEMAND_BROWSERS in your Jenkins job
        browsers = json.loads(os.environ["SAUCE_ONDEMAND_BROWSERS"])
        # Randomly select a browser for each test
        random_browser = random.choice(browsers)
        desired_cap = {
            'platform': random_browser['platform'],
            'browserName': random_browser['browser'],
            'version': random_browser['browser-version'],
        }

        self.driver = webdriver.Remote(
            command_executor='http://YOUR_SAUCE_USERNAME:YOUR_SAUCE_ACCESS_KEY@ondemand.saucelabs.com:80/wd/hub',
            desired_capabilities=desired_cap)
        # Print this line so that Jenkins will pick up your test results (including the video) from SauceLabs
        print("SauceOnDemandSessionID={} job-name={}".format(self.driver.session_id, self.id()))
        self.driver.get("http://www.python.org")

    def tearDown(self):
        self.driver.quit()
        # Update the SauceLabs dashboard with the pass/fail result
        if sys.exc_info() == (None, None, None):
            sauce_client.jobs.update_job(self.driver.session_id, passed=True)
        else:
            sauce_client.jobs.update_job(self.driver.session_id, passed=False)

    @parameterized.expand([
        ("pycon", True),
        ("pyladies", True),
        ("fdsafdsafdsafdsa", False),
        ("raspberry pi", True),
    ])
    def test_search_in_python_org(self, search_term, expected_result):
        """
        Tests python.org search feature. Searches for the word "pycon" then verified that some results show up.
        Note that it does not look for any particular text in search results page. This test verifies that
        the results were not empty.
        """

        #Load the main page. In this case the home page of Python.org.
        main_page = page.MainPage(self.driver)
        #Checks if the word "Python" is in title
        assert main_page.is_title_matches(), "python.org title doesn't match."
        #Sets the text of search textbox to the search_term
        main_page.search_text_element = search_term
        main_page.click_go_button()
        search_results_page = page.SearchResultsPage(self.driver)
        #Verifies that the results page is not empty, (unless it's supposed to be, for the negative case)
        self.assertEquals(search_results_page.is_results_found(), expected_result)