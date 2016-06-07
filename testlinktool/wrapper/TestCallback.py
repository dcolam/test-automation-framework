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
import time
__doc__ = "Test callback API and decorators."


class TestCallback:
    """
    This represents actions that will be executed at the end of a test
    """
    def on_success(self, test):
        """
        called on success
        :param test:
        :type test: unittest.TestCase
        """
        pass

    def on_failure(self, test):
        """
        called on failure
        :param test:
        :type test: unittest.TestCase
        """
        pass

    def on_error(self, test):
        """
        called on error (i.e when an unexpected Exception is raised)
        :param test:
        :type test: unittest.TestCase
        """
        pass

    def on_skip(self, test):
        """
        called on skipping test
        :param test:
        :type test: unittest.TestCase
        """
        pass


class TakeScreenshotCallback(TestCallback):
    """
    This callback will take screenshot on failure or error
    """
    def __init__(self, filepath_format):
        self.filepath_format = filepath_format

    def __get_data(self, test, **kwargs):
        default = dict(
            name = test.id(),
            status = "fail",
            time=int(time.time())
        )
        default.update(kwargs)
        return default

    def on_failure(self, test):
        if hasattr(test, "driver") and test.driver:
            test.driver.save_screenshot(self.filepath_format.format(**self.__get_data(test)))

    def on_error(self, test):
        if hasattr(test, "driver") and test.driver:
            test.driver.save_screenshot(self.filepath_format.format(**self.__get_data(test, status="error")))


def with_callback(callback):
    """
    Decorator to be used for registering a callback
    :param callback:
    :type callback: TestCallback
    """
    def __wrapper(cls):
        class NewTest(cls):
            @classmethod
            def get_name(cls):
                return cls.__name__

            def __init__(self, *args, **kwargs):
                super(NewTest, self).__init__(*args, **kwargs)
                if not hasattr(self, "callbacks"):
                    self.callbacks = []
                self.callbacks.append(callback)
        return NewTest
    return __wrapper
