from unittest import TestCase
from mock import Mock


class TestScreeshotCallback(TestCase):

    def setUp(self):
        from testlinktool.wrapper.UITestCase import UITestCase
        from testlinktool.wrapper.TestCallback import TakeScreenshotCallback, with_callback
        self.mocked = None
        inst = self
        @with_callback(TakeScreenshotCallback("testing_dir{status}"))
        class tested_Test(UITestCase):
            def setUp(self):
                self.get_phantomjs()
                self.driver.save_screenshot = Mock()

                inst.mocked = self.driver.save_screenshot

            def test_success(self):
                pass

            def test_failure(self):
                self.assertTrue(False)

            def test_error(self):
                raise Exception

            def test_skip(self):
                raise self.skipTest("bla")
        self.tested_Test = tested_Test

    def test_nothing_on_success(self):
        test = self.tested_Test("test_success")
        test.callbacks[0].on_error = Mock()
        result = test.defaultTestResult()
        result.startTest(test)
        test(result)
        self.mocked.assert_not_called()
        test.callbacks[0].on_error.assert_not_called()

    def test_screen_on_failure(self):
        test = self.tested_Test("test_failure")
        test.callbacks[0].on_error = Mock()
        result = test.defaultTestResult()
        result.startTest(test)
        test(result)
        self.mocked.assert_called_with("testing_dirfail")
        test.callbacks[0].on_error.assert_not_called()

    def test_screen_on_error(self):
        test = self.tested_Test("test_error")
        test.callbacks[0].on_failure = Mock()
        result = test.defaultTestResult()
        result.startTest(test)
        test(result)
        test.driver.save_screenshot.assert_called_with("testing_direrror")
        test.callbacks[0].on_failure.assert_not_called()