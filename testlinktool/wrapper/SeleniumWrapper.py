"""

Copyright (c) 2016 "Vade Retro Technology"

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
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException
import logging
from subprocess import check_output

_log = logging.getLogger("testlinktool.selinum")
__doc__ = "Mixin collection to access selenium capabilities."


class SeleniumWrapperMixin:
    """
    Add some shortcut to access to Selenium driver functionalities.
    """
    driver = None
    local = True
    driver_log = None

    def get_firefox(self):

        if self.local:
            version = float(check_output(["firefox", "-v"]).decode("utf-8").strip().replace("Mozilla Firefox ", ""))
            marionette = version >= 47
            self.driver = webdriver.Firefox(capabilities={"marionette": marionette,
                                                          'binary': FirefoxBinary(log_file=self.driver_log)})
        else:
            self.driver = webdriver.Remote(
                command_executor=self.remote_server,
                desired_capabilities=DesiredCapabilities.FIREFOX)

    def get_htmlunit(self):
        self.driver = webdriver.Remote(command_executor=self.remote_server,
                                       desired_capabilities=DesiredCapabilities.HTMLUNITWITHJS)

    def get_chrome(self):
        self.driver = webdriver.Chrome()

    def get_phantomjs(self):
        self.driver = webdriver.PhantomJS()

    def wait_to_be_clickable_then_click(self, locator, rule, timeout):
        """wait for at most *timeout* seconds for the first element matching the rule to be clickable.\
        then trigger click event

        :param locator: the engine to process the rule
        :type locator: selenium.webdriver.common.by.By
        :param rule: the rule the element must match
        :type rule: str
        :param timeout: Number of second that we will poll the DOM. Once this is over, a TimeoutException is raised
        :type: int
        :raise selenium.common.exceptions.TimeoutException: when time is over and no element is found
        :raise selenium.common.exceptions.WebDriverException: if an element is found but is no \
        more clickable when click on it
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((locator, rule))
        )
        element.click()

    def element_does_not_appear(self, locator, rule):
        """check that an element dos not appear

        :param locator: the engine to process the rule
        :type locator: selenium.webdriver.common.by.By
        :param rule: the rule the element must match
        :type rule: str
        :return: True if element does not appear, False otherwise
        :rtype: bool
        """
        try:
            self.driver.find_element(by=locator, value=rule)
            return False
        except NoSuchElementException:
            return True

    def wait_element(self, locator, rule, timeout):
        """wait for element to be visible

        :param locator: the engine to process the rule
        :type locator: selenium.webdriver.common.by.By
        :param rule: the rule the element must match
        :type rule: str
        :param timeout: Number of second that we will poll the DOM. Once this is over, a TimeoutException is raised
        :type timeout: int
        :return:
        :rtype: bool
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((locator, rule))
            )
            return True
        except TimeoutException:
            return False

    def element_does_not_appear_after_waiting(self, locator, rule, timeout):
        """check that an element does not appear even after waiting for *timeout* seconds

        :param locator: the engine to process the rule
        :type locator: selenium.webdriver.common.by.By
        :param rule: the rule the element must match
        :type rule: str
        :param timeout: Number of second that we will poll the DOM. Once this is over, a TimeoutException is raised
        :type timeout: int
        :return:
        :rtype: bool
        """
        try:
            if self.element_does_not_appear(locator, rule):
                return not self.wait_element(locator, rule, timeout)
            else:
                WebDriverWait(self.driver, timeout).until_not(
                    EC.visibility_of_element_located((locator, rule))
                )
                return True
        except TimeoutException:
            return False

    def erase_then_put(self, element, new_value):
        """Erase element content then write it the wanted value

        :param element: The form field element
        :type element: selenium.webdriver.remote.webelement.WebElement
        :param new_value: the value to set
        :type new_value: str|int
        """
        element.click()
        if element.get_attribute("value") != "":
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
            element.send_keys(Keys.DELETE)
        if element.get_attribute("value") != "":
            ActionChains(self.driver).double_click(element).send_keys(Keys.DELETE).perform()
        if not isinstance(new_value, str):
            new_value = str(new_value)
        element.send_keys(new_value)

    def select_option_with_text(self, select_locator, select_rule, visible_text=None, value=None, wait_timeout=-1):
        """Select the write option in a <select> element

        :param select_locator: the engine to process the rule
        :type select_locator: selenium.webdriver.common.by.By
        :param select_rule: the rule the <select> element must match
        :type select_rule: str
        :param visible_text: the text inside <option> tag. Must be used only if value is None
        :type visible_text: str
        :param value: the text inside value attribute for <option> tag. Must be used only if visible_text is None
        :type value: str
        :param wait_timeout: Number of second that we will poll the DOM. Once this is over, a TimeoutException is raised\
        if wait_timeout is negative, no wait will be processed
        :type wait_timeout: int
        :raises TimeoutException: when wait_timeout is provided and the select element is not found before timeout
        :raises NoSuchElementException: when Select element is not found our there no <option> child matching your \
        requirements
        :raises WebDriverException: when element exist but can't be accessed or when your driver failed to process the \
        selection action
        """
        if value is not None and visible_text is not None:
            raise ValueError("Can't select by visible text AND value")
        if value is None and visible_text is None:
            raise ValueError("You must select by value OR by visible text")
        if wait_timeout < 0:
            select = Select(self.driver.find_element(by=select_locator, value=select_rule))
        else:
            element = WebDriverWait(self.driver, wait_timeout).until(
                EC.element_to_be_clickable((select_locator, select_rule))
            )
            select = Select(element)
        if visible_text is not None:
            select.select_by_visible_text(visible_text)
        if value is not None:
            select.select_by_value(value)

    def __find_option_or_raise(self, text, select_name="", select_id=""):
        options = None
        if select_name:
            options = self.driver.find_elements(By.CSS_SELECTOR, "select[name={}] option".format(select_name))
        if select_id:
            options = self.driver.find_elements(By.CSS_SELECTOR, "select#{} option".format(select_id))

        if not options:
            raise NoSuchElementException("No dropdown menu with id {} or name {}".format(select_id or "empty",
                                                                                         select_name or "empty"))
        return options


    def get_option_value_with_text(self, text, select_name="", select_id=""):
        """get value attribute of the option tag that contains text as visible text

        :param text: the text to match
        :param select_name: if set, the name attribute value for select element
        :param select_id: if set the select element unique id
        :return: value attribute
        :rtype: str
        :raises NoSuchElementException: if no select or option is found
        """
        options = self.__find_option_or_raise(text, select_name, select_id)
        for option in options:
            if text in option.text:
                return option.get_attribute("value")
        raise NoSuchElementException("No option with text {}".format(text))

    def _find_with_timemout_or_directly(self, locator, rule, timeout=-1, must_be_clickable=True):
        if timeout > 0:
            condition = EC.element_to_be_clickable
            waiter = WebDriverWait(self.driver, timeout)
            if not must_be_clickable:
                waiter.until_not(condition((locator, rule)))
                element = self.driver.find_element(locator, rule)
            else:
                element = waiter.until(condition((locator, rule)))
        else:
            element = self.driver.find_element(locator, rule)
            if must_be_clickable and not element.is_enabled():
                raise TimeoutException("Can't find clickable element")
        return element

    def close_driver(self):
        try:
            self.driver.close()
        except (ConnectionRefusedError, AttributeError, ResourceWarning, NoSuchWindowException) as e:

            _log.debug(e)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_driver()
