import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from testlinktool.wrapper.TestLinkReport import TestLinkTestCase

class UITestCase(unittest.TestCase):
    driver = None
    local = True
    remote_server = "" 

    def run_test_on_current_browser(self):
        """
        this method contains your test logic. You must override it.
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
        self.run_test_on_current_browser()
    
    def tearDown(self):
        if self.driver:
            self.driver.close()


class UITestLinkTestCase(TestLinkTestCase, UITestCase):
    driver = None
    local = True
    remote_server = "" 
    
