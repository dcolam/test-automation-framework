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
from unittest import TestCase

from os.path import dirname, join

import time
from selenium.webdriver.common.by import By

from testlinktool.wrapper.UITestCase import UITestCase


class WaitingElement(TestCase):
    def setUp(self):
        self.tested_object = UITestCase()
        self.tested_object.get_phantomjs()
        self.tested_object.driver.get("file://" + join(dirname(__file__), "html_file.html"))
    def test_waiting_existing_element(self):
        self.assertTrue(self.tested_object.wait_element(By.ID, "already_existing", 5))

    def test_waiting_hidden_element(self):
        self.assertTrue(self.tested_object.element_does_not_appear_after_waiting(By.ID, "hidden", 5))

    def test_waiting_element_discovered_after_sometime(self):

        self.assertTrue(self.tested_object.element_does_not_appear(By.ID, "timeouted"))
        self.assertFalse(self.tested_object.element_does_not_appear_after_waiting(By.ID, "timeouted", 30))

    def test_clickable(self):
        self.assertRaises(AssertionError, self.tested_object.assertIsClickable, By.ID, "non_clickable")
        self.assertRaises(AssertionError, self.tested_object.assertIsClickable, By.ID, "timeout_non_clickable")
        self.tested_object.assertIsClickable(By.ID, "timeout_non_clickable", 30)
        self.assertRaises(AssertionError, self.tested_object.assertIsNotClickable, By.ID, "clickable")
        self.tested_object.assertIsNotClickable(By.ID, "timeout_clickable", 30)


class TestSelection(TestCase):

    def test_select_with_value(self):
        self.tested_object = UITestCase()
        self.tested_object.get_phantomjs()
        self.tested_object.driver.get("file://" + join(dirname(__file__), "html_file.html"))
        self.tested_object.select_option_with_text(By.NAME, "selected", value="1")
        self.tested_object.wait_to_be_clickable_then_click(By.NAME, "subform", 1)
        self.assertIn("selected=1", self.tested_object.driver.current_url)

    def test_select_with_text(self):
        self.tested_object = UITestCase()
        self.tested_object.get_phantomjs()
        self.tested_object.driver.get("file://" + join(dirname(__file__), "html_file.html"))
        self.tested_object.select_option_with_text(By.NAME, "selected", visible_text="number1")
        self.tested_object.wait_to_be_clickable_then_click(By.NAME, "subform", 1)
        self.assertIn("selected=1", self.tested_object.driver.current_url)

    def test_select_not_existing(self):
        self.tested_object = UITestCase()
        self.tested_object.get_phantomjs()
        self.tested_object.driver.get("file://" + join(dirname(__file__), "html_file.html"))
        self.assertRaises(Exception, self.tested_object.select_option_with_text, By.NAME, "selected", value="9")

