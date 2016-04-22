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
