"""

Copyright (c) 2016 "Vade Retro Technology"

...


This file is part of test-automation-framework.


xxxxx is free software: you can redistribute it and/or modify

it under the terms of the GNU General Public License as published by

the Free Software Foundation, either version 3 of the License, or

(at your option) any later version.


This program is distributed in the hope that it will be useful,

but WITHOUT ANY WARRANTY; without even the implied warranty of

MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the

GNU General Public License for more details.


You should have received a copy of the GNU General Public License

along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from time import sleep
from testlinktool.wrapper.UITestCase import UITestLinkTestCase


class ZDSIndex(UITestLinkTestCase):
    
    @classmethod
    def get_plan_name(cls):
        return "TestString"
      
    def test_firefox(self):
        try:
            driver = webdriver.Remote(
                command_executor='http://127.0.0.1:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.FIREFOX)
        except Exception:
            self.skipTest("Firefox does not seem to be installed")
        self._test_research(driver)
    
    def test_chrome(self):
        """driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)"""
        try:
            driver = webdriver.Chrome()
        except Exception:
            self.skipTest("Chrome does not seem to be installed")
        self._test_research(driver)
    
    def test_operea(self):
        try:
            driver = webdriver.Remote(
                command_executor='http://127.0.0.1:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.OPERA)
        except Exception:
            self.skipTest("Firefox does not seem to be installed")
    
    def _test_research(self, driver):
        driver.get("http://zestedesavoir.com")
        self.assertIn("zeste de savoir", driver.title.lower(), "has a good title")
        search_field = driver.find_element_by_id("search-home-input")
        search_field.send_keys("python")
        search_field.send_keys(Keys.RETURN)
        sleep(1)
        self.assertIn("rechercher/?q=python", driver.current_url)
        driver.get("http://zestedesavoir.com")
        search_field = driver.find_element_by_id("search-home-input")
        search_field.send_keys("python")
        element = driver.find_element_by_xpath('//form[@id="search-home"]/button')
        element.click()
        sleep(1.2)
        self.assertIn("rechercher/?q=python", driver.current_url)
        driver.close()