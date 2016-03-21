from unittest import TestCase
from testlinktool.wrapper.TestLinkReport import _TestLinkTestResult
from mock import Mock


class TestResultWrapper(TestCase):

    def test_add_success(self):
        class FalseTest(TestCase):
            def test_useless(self):
                pass

        result = _TestLinkTestResult()
        fake = FalseTest("test_useless")
        result.startTest(fake)
        result.addSuccess(fake)
        self.assertEqual(1, result.success_count)
        self.assertEqual(1, len(result.result))
        self.assertEqual(0, result.failure_count)

    def test_add_failure(self):
        class FalseTest(TestCase):
            def test_useless(self):
                pass

        result = _TestLinkTestResult()
        result.complete_output = Mock()
        fake = FalseTest("test_useless")
        result.startTest(fake)
        result.addFailure(fake, (AssertionError, AssertionError("bla"), None))
        self.assertEqual(1, result.failure_count)
        self.assertEqual(1, len(result.result))
        self.assertEqual(1, len(result.failures))
        self.assertEqual(0, result.success_count)
        self.assertEqual(1, result.complete_output.call_count)
