"""

Copyright (c) 201x "Vade Retro Technology"

...


This file is part of test-automation-framework.


test-automation-framework is free software: you can redistribute it and/or modify

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
import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from testlinktool.wrapper.TestLinkReport import TestLinkTestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from testlinktool.wrapper.SeleniumWrapper import SeleniumWrapperMixin


class UITestCase(unittest.TestCase, SeleniumWrapperMixin):
    """
    extends TestCase facility to deal with selenium webdriver
    """
    driver = None
    local = True
    maximize_window = True
    remote_server = ""
    """
    :var driver: the current webdriver
    :var local: if ``True`` use webdriver inside your path, get remote_server otherwise
    :type local: bool
    :var remote_server: the remote_server that host webdrivers
    """

    def run_test_on_current_browser(self):
        """
        this method contains your test logic. You must override it.
        """
        pass

    def setUpUi(self):
        """
        this method is called after driver is intialized to create preconditions
        """
        pass

    def get_firefox(self):
        try:
            super(UITestCase, self).get_firefox()
        except Exception:
            self.skipTest("No firefox web driver in your PATH")

    def testChrome(self):
        """
        Launch test scenario in Chrome Web Driver
        """
        try:
            if self.local:
                self.driver = webdriver.Chrome()
            else:
                self.driver = webdriver.Remote(
                    command_executor=self.remote_server,
                    desired_capabilities=DesiredCapabilities.CHROME)
        except Exception:
            self.skipTest("No chrome web driver in your PATH")
        if self.maximize_window:
            self.driver.maximize_window()
        self.setUpUi()
        self.run_test_on_current_browser()
    
    def testFirefox(self):
        """
        Lauch test scenario in Firefox Web Driver
        """
        self.get_firefox()
        if self.maximize_window:
            self.driver.maximize_window()
        self.setUpUi()
        self.run_test_on_current_browser()

    def assertElementDoesNotAppearAfterWaiting(self, locator, rule, timeout):
        """check that an element appears even after waiting for *timeout* seconds

        :param locator: the engine to process the rule
        :type locator: selenium.webdriver.common.by.By
        :param rule: the rule the element must match
        :type rule: str
        :param timeout: Number of second that we will poll the DOM. Once this is over, a TimeoutException is raised
        :type: int
        """
        self.assertTrue(self.element_does_not_appear_after_waiting(locator, rule, timeout))

    def assertElementAppearAfterWaiting(self, locator, rule, timeout):
        """check that an element appears after waiting for *timeout* seconds

        :param locator: the engine to process the rule
        :type locator: selenium.webdriver.common.by.By
        :param rule: the rule the element must match
        :type rule: str
        :param timeout: Number of second that we will poll the DOM. Once this is over, a TimeoutException is raised
        :type: int
        """
        self.assertTrue(self.wait_element(locator, rule, timeout))

    def assertElementIsPresent(self, locator, rule):
        """check that element is present in DOM.

        :param locator: the engine to process the rule
        :type locator: selenium.webdriver.common.by.By
        :param rule: the rule the element must match
        :type rule: str
        """
        self.assertFalse(self.element_does_not_appear(locator, rule))

    def assertNotChecked(self, locator, rule, timeout=-1):
        """assert a checkbox, radiobutton or option is not checked

        :param locator: the engine to process the rule
        :type locator: selenium.webdriver.common.by.By
        :param rule: the rule the element must match
        :type rule: str
        :param timeout: Number of second that we will poll the DOM. Once this is over, a TimeoutException is raised \
        if timeout is less than 0, no wait is processed
        :type timeout: int
        """
        try:
            if timeout > 0:
                element = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((locator, rule))
                )
            else:
                element = self.driver.find_element(locator, rule)
        except (NoSuchElementException, TimeoutException) as e:
            raise self.failureException(str(e))
        self.assertFalse(element.is_selected())

    def assertChecked(self, locator, rule, timeout=-1):
        """assert a checkbox, radiobutton or option is checked

        :param locator: the engine to process the rule
        :type locator: selenium.webdriver.common.by.By
        :param rule: the rule the element must match
        :type rule: str
        :param timeout: Number of second that we will poll the DOM. Once this is over, a TimeoutException is raised \
        if timeout is less than 0, no wait is processed
        :type timeout: int
        """
        try:
            if timeout > 0:
                element = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((locator, rule))
                )
            else:
                element = self.driver.find_element(locator, rule)
        except (NoSuchElementException, TimeoutException) as e:
            raise self.failureException(str(e))
        self.assertTrue(element.is_selected())

    def assertHasValue(self, locator, rule, value, timeout=-1, exact=True, case_sensitive=True):
        """assert the current form field has the requested value

        :param locator: the engine to process the rule
        :type locator: selenium.webdriver.common.by.By
        :param rule: the rule the element must match
        :type rule: str:
        :param value: the requested value
        :param timeout: if positive, driver will wait for the element to appear
        :type timeout: int
        :param exact: if ``True`` check the value is exactly the requested value. if ``False`` check ``value`` is a \
        substring of the field value attribute
        :type exact: bool
        :param case_sensitive: if ``True`` comparison will be case insensitive
        :type case_sensitive: bool
        """
        try:
            if timeout > 0:
                element = WebDriverWait(self.driver, timeout).until(
                        EC.element_to_be_clickable((locator, rule))
                )
            else:
                element = self.driver.find_element(locator, rule)
        except (NoSuchElementException, TimeoutException) as e:
            raise self.failureException(str(e))
        element_value = element.get_attribute("value")
        if not case_sensitive:
            value = value.lower()
            element_value = element_value.lower()
        if exact:
            self.assertEqual(element_value, value)
        else:
            self.assertIn(value, element_value)

    def assertIsNotClickable(self, locator, rule, timeout=-1):
        element = self._find_with_timemout_or_directly(locator, rule, timeout, must_be_clickable=False)
        self.assertFalse(element.is_enabled())

    def assertIsClickable(self, locator, rule, timeout=-1):
        element = self._find_with_timemout_or_directly(locator, rule, timeout, must_be_clickable=True)
        self.assertTrue(element.is_enabled())

    def tearDown(self):
        if self.driver:
            self.driver.close()


class UITestLinkTestCase(TestLinkTestCase, UITestCase):
    """
    Represents a UI test case that is linked to TestLink
    """
    driver = None
    local = True
    remote_server = "" 
