from unittest import TestCase

from os.path import dirname, join

from selenium.webdriver.common.by import By

from testlinktool.wrapper.UITestCase import UITestCase


class WaitingElement(TestCase):

    def test_waiting_existing_element(self):
        self.tested_object = UITestCase()
        self.tested_object.get_firefox()
        self.tested_object.driver.get("file://" + join(dirname(__file__), "html_file.html"))
        self.assertTrue(self.tested_object.wait_element(By.ID, "already_existing", 5))

    def test_waiting_hidden_element(self):
        self.tested_object = UITestCase()
        self.tested_object.get_firefox()
        self.tested_object.driver.get("file://" + join(dirname(__file__), "html_file.html"))

        self.assertTrue(self.tested_object.element_does_not_appear_after_waiting(By.ID, "timeouted", 5))

    def tearDown(self):
        if hasattr(self, "tested_object"):
            self.tested_object.close_driver()