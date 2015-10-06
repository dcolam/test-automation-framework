import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from testlinktool.wrapper.TestLinkReport import TestLinkTestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class UITestCase(unittest.TestCase):
    driver = None
    local = True
    maximize_window = True
    remote_server = "" 

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

    def testChrome(self):
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
        try:
            if self.local:
                self.driver = webdriver.Firefox()
            else:
                self.driver = webdriver.Remote(
                    command_executor=self.remote_server,
                    desired_capabilities=DesiredCapabilities.FIREFOX)
        except Exception:
            self.skipTest("No firefox web driver in your PATH")
        if self.maximize_window:
            self.driver.maximize_window()
        self.setUpUi()
        self.run_test_on_current_browser()

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
        :return:
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
        :return:
        :rtype: bool
        """
        try:
            self.driver.find_element(by=locator, value=rule)
            return False
        except NoSuchElementException:
            return True

    def element_does_not_appear_after_waiting(self, locator, rule, timeout):
        """check that an element dos not appear even after waiting for *timeout* seconds

        :param locator: the engine to process the rule
        :type locator: selenium.webdriver.common.by.By
        :param rule: the rule the element must match
        :type rule: str
        :param timeout: Number of second that we will poll the DOM. Once this is over, a TimeoutException is raised
        :type: int
        :return:
        :rtype: bool
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((locator, rule))
            )
            return element is None
        except TimeoutException:
            return True

    def assertElementDoesNotAppearAfterWaiting(self, locator, rule, timeout):
        self.assertTrue(self.element_does_not_appear_after_waiting(locator, rule, timeout))

    def assertElementAppearAfterWaiting(self, locator, rule, timeout):
        self.assertFalse(self.element_does_not_appear_after_waiting(locator, rule, timeout))

    def assertElementIsPresent(self, locator, rule):
        self.assertFalse(self.element_does_not_appear(locator, rule))

    def erase_then_put(self, element, new_value):
        """Erase element content then write it the wanted value

        :param element:
        :param new_value:
        :return:
        """
        element.click()
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        element.send_keys(Keys.DELETE)
        if element.get_attribute("value") != "":
            element.double_click()
            element.send_keys(Keys.DELETE)
        if not isinstance(new_value, str):
            new_value = str(new_value)
        element.send_keys(new_value)

    def select_option_with_text(self, select_locator, select_rule, visible_text=None, value=None, wait_timeout=-1):
        """

        :param select_locator: the engine to process the rule
        :type select_locator: selenium.webdriver.common.by.By
        :param select_rule: the rule the <select> element must match
        :type select_rule: str
        :param visible_text: the text inside <option> tag. Must be used only if value is None
        :type visible_text; str
        :param value: the text inside value attribute for <option> tag. Must be used only if visible_text is None
        :type value: str
        :param wait_timeout: Number of second that we will poll the DOM. Once this is over, a TimeoutException is raised\
        if wait_timeout is negative, no wait will be processed
        :type wait_timeout: int
        :raise TimeoutException: when wait_timeout is provided and the select element is not found before timeout
        :raise NoSuchElementException: when Select element is not found our there no <option> child matching your \
        requirements
        :raise WebDriverException: when element exist but can't be accessed or when your driver failed to process the \
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

    def assertNotChecked(self, locator, rule, timeout=-1):
        try:
            if timeout > 0:
                element = WebDriverWait(self.driver, timeout).until(
                        EC.element_to_be_clickable((locator, rule))
                )
            else:
                element = self.driver.find_element(locator, rule)
        except (NoSuchElementException, TimeoutException) as e:
            raise self.failureException(str(e))
        self.assertFalse(element.is_selected())

    def assertChecked(self, locator, rule, timeout=-1):
        try:
            if timeout > 0:
                element = WebDriverWait(self.driver, timeout).until(
                        EC.element_to_be_clickable((locator, rule))
                )
            else:
                element = self.driver.find_element(locator, rule)
        except (NoSuchElementException, TimeoutException) as e:
            raise self.failureException(str(e))
        self.assertTrue(element.is_selected())

    def assertHasValue(self, locator, rule, value, timeout=-1, exact=True, case_sensitive=True):
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

    def tearDown(self):
        if self.driver:
            self.driver.close()


class UITestLinkTestCase(TestLinkTestCase, UITestCase):
    driver = None
    local = True
    remote_server = "" 

