from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from time import sleep
from wrapper.UITestCase import UITestLinkTestCase
from wrapper.TestLinkReport import TestLinkTestCase

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


class TestStringMethods(TestLinkTestCase):

  @classmethod
  def get_plan_name(cls):
      return "TestString"

  def test_upper(self):
      print("test")
      self.assertEqual('foo'.upper(), 'FOO')

  def test_isupper(self):
      self.assertTrue('FOO'.isupper())
      self.assertFalse('Foo'.isupper())

  def test_split(self):
      s = 'hello world'
      self.assertEqual(s.split(), ['hello', 'world'])
      # check that s.split fails when the separator is not a string
      with self.assertRaises(TypeError):
          s.split(2)

class TestStringMethods2(TestLinkTestCase):
  @classmethod
  def get_plan_name(cls):
      return "TestString"

  def test_upper(self):
      self.assertEqual('foo'.upper(), 'FOO')

  def test_isupper(self):
      self.assertTrue('FOO'.isupper())
      self.assertFalse('Foo'.isupper())

  def test_split(self):
      s = 'hello world'
      self.assertEqual(s.split(), ['hello', 'worlds'])
      # check that s.split fails when the separator is not a string
      with self.assertRaises(TypeError):
          s.split(2)
