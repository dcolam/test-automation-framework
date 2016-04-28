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
import contextlib

import datetime
from collections import Counter
import time
import lxml as lxml

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from testlink import TestlinkAPIClient, TestLinkHelper
import os
import re
import sys
import types
import unittest
import logging

from fnmatch import fnmatch
from os.path import relpath
__doc__ = "All tools to run test and generate reports to testlink"
VALID_MODULE_NAME = re.compile(r'[_a-z]\w*\.py$', re.IGNORECASE)
_log = logging.getLogger("testlink-runner")


class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """
    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()

stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)


class _TestLinkTestResult(unittest.TestResult):
    """
    Inner class that is just here to send result to RTC server
    """

    # note: _TestLinkTestResult is a pure representation of results in order to be sent to RTC server
    execution_time = 0
    
    def __init__(self, verbosity=1):
        super(_TestLinkTestResult, self).__init__()
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.verbosity = verbosity

        # result is a list of result in 4 tuple
        # (
        #   result code (0: success; 1: fail; 2: error),
        #   TestCase object,
        #   Test output (byte string),
        #   stack trace,
        # )
        self.result = []

    def startTest(self, test):
        super(_TestLinkTestResult, self).startTest(test)
        _log.info(str(test))
        # just one buffer for both stdout and stderr
        self.outputBuffer = StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector

    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()

    def stopTest(self, test):
        """Clear the test even if something went wrong in addSuccess or addError

        :param test: current test
        """
        # Usually one of addSuccess, addError or addFailure would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be called.
        _log.warning(str(test) + " interrupted")
        self.complete_output()

    def addSuccess(self, test):
        """
        notify that the current test ended successfuly
        """
        self.success_count += 1
        super(_TestLinkTestResult, self).addSuccess(test)
        with contextlib.suppress(Exception):
            for callback in getattr(test, "callbacks", []):
                callback.on_success(test)
        output = self.complete_output()
        self.result.append((0, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write('ok ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.')

    def addError(self, test, err):
        """
        notify that the current test ended with an error (exception raised)
        """
        self.error_count += 1
        super(_TestLinkTestResult, self).addError(test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        with contextlib.suppress(Exception):
            for callback in getattr(test, "callbacks", []):
                callback.on_error(test)
        self.result.append((2, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('E  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')

    def addFailure(self, test, err):
        """
        notify that the current test failed
        """
        self.failure_count += 1
        super(_TestLinkTestResult, self).addFailure(test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        with contextlib.suppress(Exception):
            for callback in getattr(test, "callbacks", []):
                callback.on_failure(test)
        self.result.append((1, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')


class TestLinkRunner(object):
    """
    The object that is used to run the test in a testlink environment
    """
    startTime = datetime.datetime.now()
    endTime = datetime.datetime.now()
    testlink_key = ""
    testlink_client = None
    server_url = "/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
    translation = ('p', 'f', 'b')
    platformname = ""
    project_id = 0
    plans = []
    build = {}
    must_create_build = True
    xml = None
    failure = 0
    error = 0
    tests = 0

    def __init__(self, server_url, project_id,
                 platformname, must_create_build,
                 testlink_key, verbose=False, generate_xml=False):
        self.server_url = server_url
        self.generate_xml = generate_xml
        self.project_id = project_id
        self.platformname = platformname
        self.must_create_build = must_create_build
        self.testlink_key = testlink_key
        tl_helper = TestLinkHelper(self.server_url, self.testlink_key)
        self.testlink_client = tl_helper.connect(TestlinkAPIClient)
        self.plans = self.testlink_client.getProjectTestPlans(self.project_id)
        self.verbose = verbose
    
    def _sendReport(self, report):

        test_case = self.testlink_client.getTestCaseIDByName(report["testcaseid"])[0]
        plan = [p for p in self.plans if p["name"] == report['testsuitid']][0]
        if plan["name"] not in self.build and self.must_create_build:
            self.build[plan["name"]] = self.testlink_client.createBuild(plan["id"],
                                                                       "build-auto:" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                                       "auto build with python and selenium")
        result = self.testlink_client.reportTCResult(test_case["id"],
                                                     plan["id"],
                                                     None,
                                                     self.translation[report["state"]],
                                                     report["note"],
                                                     guess=True,
                                                     platformname=self.platformname)
        _log.debug(result)
        if self.verbose:
            print(result)

    def __init_xml(self):
        self.xml = lxml.etree.Element("testsuite", time=str(self.stopTime - self.start_time).encode("utf-8"))

    def __finalize_xml(self):
        self.xml.set("failures", str(self.failure))
        self.xml.set("errors", str(self.error))
        self.xml.set("tests", str(self.tests))
        with contextlib.suppress(OSError):
            os.makedirs("./test-reports")
        with open("./test-reports/TEST-" + str(time.time()) + ".xml", "wb") as xmlfile:
            xmlfile.write(lxml.etree.tostring(self.xml, pretty_print=True))

    def __push_xml(self, report):
        element = lxml.etree.SubElement(self.xml, "testcase", classname=str(report["testcaseid"]), name=report["name"])
        if report["state"] == 1:
            lxml.etree.SubElement(element, "failure", message=report["note"], type="AssertionError")
            self.failure += 1
        elif report["state"] == 2:
            lxml.etree.SubElement(element, 'error', message=report["note"], type=str(report["failureException"]))
            self.error += 1
        self.tests += 1

    def generateReport(self, test, result):
        """Send per-test report to testling and generate xml JUnit report if was asked

        :param test:
        :param result: test result object
        :type result: _TestLinkTestResult
        :return:
        """
        final_report = {}

        self.__init_xml()
        for testresult in result.result:

            try:
                testcaseid = testresult[1].__class__.__name__
                testsuitid = testresult[1].__class__.get_plan_name()
                if testcaseid not in final_report:
                    final_report[testcaseid] = {
                        "testcaseid": testcaseid,
                        "testsuitid": testsuitid,
                        "state": testresult[0],
                        "note": "",
                        "nb": 1,
                        "states": [testresult[0]],
                        "name": testcaseid + "." + testresult[1]._testMethodName
                    }
                if testresult[0] != 0:
                    final_report[testcaseid]["state"] = max(testresult[0], final_report[testcaseid]["state"])
                    final_report[testcaseid]["note"] += testresult[3] + "\n"
                    final_report[testcaseid]["nb"] += 1
                    final_report[testcaseid]["states"].append(testresult[0])
                self.__push_xml({
                        "testcaseid": testcaseid,
                        "testsuitid": testsuitid,
                        "state": testresult[0],
                        "note": testresult[3],
                        "nb": 1,
                        "states": [testresult[0]],
                        "name":  testcaseid + "." + testresult[1]._testMethodName,
                        "failure_exception": getattr(testresult[1], "failureException").__name__
                    })
            except Exception as e:
                _log.error("report was not sent due to " + str(e))
        for testcaseid in final_report:
            final_report[testcaseid]["states"] = Counter(final_report[testcaseid]["states"])

        for report in final_report.values():
            self._sendReport(report)
        if hasattr(self, "generate_xml") and self.generate_xml:
            self.__finalize_xml()

    def _init_cases(self, testsuite):
        for test in testsuite:
            if isinstance(test, TestLinkTestCase):
                test.populateCustomField(self.testlink_client, self.project_id)
            if isinstance(test, unittest.TestSuite):
                self._init_cases(test)

    def run(self, test):
        "Run the given test case or test suite."
        result = _TestLinkTestResult(2)
        self.start_time = time.time()
        self._init_cases(test)
        test(result)
        self.stopTime = time.time()
        result.execution_time = self.stopTime - self.start_time
        self.generateReport(test, result)
            
        return result


class TestLinkTestCase(unittest.TestCase):
    """
    A basic overload of TestCase to get create a bridge with testlink
    """

    customfield_names = []
    customfield_values = {}
    version = 1
    external_id = "EXT-ID-0"

    @classmethod
    def get_plan_name(cls):
        """Get testplan name : MANDATORY

        :return: the testplan name
        :rtype: str
        """
        raise NotImplementedError("must be overriden")

    def populateCustomField(self, testLinkClient, project_id):
        """get all customfields value from testlink test specification

        :param testLinkClient:
        :param project_id: the internal project id
        :type project_id: int
        """
        for fieldname in self.customfield_names:
            value = testLinkClient.getTestCaseCustomFieldDesignValue(self.external_id, self.version, project_id, fieldname, "value")
            self.customfield_values[fieldname] = value

    def assertEqualToCustomfield(self, value, customfieldname):
        """assert that the value is equal to the one given in the test case specification fieldname in testlink

        :param value: the value tu compare
        :param customfieldname: the testlink customfield name
        :type customfieldname: str
        """
        if customfieldname not in self.customfield_values:
            self.fail("{} not in registered fieldnames in test specification")
        self.assertEqual(value, self.customfield_values[customfieldname])


def _cmp(t1, t2):
    if t1 < t2:
        return -1
    if t1 == t2:
        return 0
    return 1


class TestLinkTestLoader(unittest.TestLoader):
    """
    This class is responsible for loading tests according to various criteria
    and returning them wrapped in a TestSuite
    This class was mainly inspired by django test framework
    """
    testMethodPrefix = 'test'
    sortTestMethodsUsing = _cmp
    suiteClass = unittest.TestSuite
    _top_level_dir = None
    test_name_pattern = ".+"
    id_list = None
    select_ui = True
    select_fonctional = True

    def __init__(self, **kwargs):
        self.select_ui = not kwargs.get("only_fonctional", False)
        self.select_fonctional = not kwargs.get("only_ui", False)
        if kwargs.get("ext_ids", None):
            self.id_list = kwargs.get("ext_ids")
        if len(kwargs.get("name_pattern", "")) > 0:
            self.test_name_pattern = kwargs.get("name_pattern")

    def loadTestsFromTestCase(self, testCaseClass):
        """Return a suite of all tests cases contained in testCaseClass"""
        if issubclass(testCaseClass, unittest.TestSuite):
            raise TypeError("Test cases should not be derived from TestSuite."
                            " Maybe you meant to derive from TestCase?")
        testCaseNames = self.getTestCaseNames(testCaseClass)
        if not testCaseNames and hasattr(testCaseClass, 'runTest'):
            testCaseNames = ['runTest']
        loaded_suite = self.suiteClass(map(testCaseClass, testCaseNames))
        return loaded_suite

    def __filter_module_names(self, module):
        from testlinktool.wrapper.UITestCase import UITestCase, UITestLinkTestCase

        def __filter(name):
            obj = getattr(module, name)
            is_a_test_object = isinstance(obj, type) and \
                               issubclass(obj, unittest.TestCase) and \
                               obj not in [UITestCase, UITestLinkTestCase]
            # a good name must fit this conditions :
            # match the name pattern if such a regex exists
            # is in selected ids if asked by the user
            # has the good tag if such filter is selected
            return is_a_test_object and self.is_authorized_by_tag_filter(obj) \
                   and self.is_authorized_by_id_filter(obj) and self.modul_name_regex.match(name)
        return __filter

    def is_authorized_by_tag_filter(self, obj):
        """checkout the test is authorized by "Only UI" or "Only functional" tags if asked by command

        :param obj:
        :return:
        :rtype: bool
        """
        from testlinktool.wrapper.UITestCase import UITestCase
        return (not issubclass(obj, UITestCase) and self.select_fonctional) or\
               (issubclass(obj, UITestCase) and self.select_ui)

    def is_authorized_by_id_filter(self, obj):
        """

        :param obj:
        :return:
        :rtype: bool
        """
        return not (self.id_list and (not issubclass(obj, TestLinkTestCase) or obj.external_id not in self.id_list))

    def loadTestsFromModule(self, module, use_load_tests=True):
        """Return a suite of all tests cases contained in the given module"""
        tests = []
        self.modul_name_regex = re.compile(self.test_name_pattern)
        names = filter(self.__filter_module_names(module), dir(module))
        for name in names:
            obj = getattr(module, name)
            tests.append(self.loadTestsFromTestCase(obj))

        load_tests = getattr(module, 'load_tests', None)
        tests = self.suiteClass(tests)
        if use_load_tests and load_tests is not None:
            try:
                return load_tests(self, tests, None)
            except Exception as e:
                return self._make_failed_load_tests(module.__name__, e,
                                               self.suiteClass)
        return tests

    def _make_failed_load_tests(self, module_name, error, suiteclass):
        sys.stderr.write("could not import {} due to {}".format(module_name, error))

    def loadTestsFromName(self, name, module=None):
        """Return a suite of all tests cases given a string specifier.

        The name may resolve either to a module, a test case class, a
        test method within a test case class, or a callable object which
        returns a TestCase or TestSuite instance.

        The method optionally resolves the names relative to a given module.
        """
        from testlinktool.wrapper.UITestCase import UITestCase, UITestLinkTestCase
        parts = name.split('.')
        if module is None:
            parts_copy = parts[:]
            while parts_copy:
                try:
                    module = __import__('.'.join(parts_copy))
                    break
                except ImportError:
                    del parts_copy[-1]
                    if not parts_copy:
                        raise
            parts = parts[1:]
        obj = module
        for part in parts:
            parent, obj = obj, getattr(obj, part)
        if isinstance(obj, types.ModuleType):
            return self.loadTestsFromModule(obj)
        elif isinstance(obj, type) and issubclass(obj, unittest.TestCase):
            return self.loadTestsFromTestCase(obj)
        elif (isinstance(obj, types.UnboundMethodType) and
              isinstance(parent, type) and
              issubclass(parent, unittest.TestCase)):
            return self.suiteClass([parent(obj.__name__)])
        elif isinstance(obj, unittest.TestSuite):
            return obj
        elif hasattr(obj, '__call__'):
            test = obj()
            if isinstance(test, unittest.TestSuite):
                return test
            elif isinstance(test, unittest.TestCase):
                return self.suiteClass([test])
            else:
                raise TypeError("calling %s returned %s, not a test" %
                                (obj, test))
        else:
            raise TypeError("don't know how to make test from: %s" % obj)

    def loadTestsFromNames(self, names, module=None):
        """Return a suite of all tests cases found using the given sequence
        of string specifiers. See 'loadTestsFromName()'.
        """
        suites = [self.loadTestsFromName(name, module) for name in names]
        return self.suiteClass(suites)

    def getTestCaseNames(self, testCaseClass):
        """Return a sorted sequence of method names found within testCaseClass
        """
        def is_test_method(attrname, testCaseClass=testCaseClass,
                         prefix=self.testMethodPrefix):
            return attrname.startswith(prefix) and \
                hasattr(getattr(testCaseClass, attrname), '__call__')
        testFnNames = filter(is_test_method, dir(testCaseClass))
        return testFnNames

    def discover(self, start_dir, pattern='test*.py', top_level_dir=None):
        """Find and return all test modules from the specified start
        directory, recursing into subdirectories to find them. Only test files
        that match the pattern will be loaded. (Using shell style pattern
        matching.)

        All test modules must be importable from the top level of the project.
        If the start directory is not the top level directory then the top
        level directory must be specified separately.

        If a test package name (directory with '__init__.py') matches the
        pattern then the package will be checked for a 'load_tests' function. If
        this exists then it will be called with loader, tests, pattern.

        If load_tests exists then discovery does  *not* recurse into the package,
        load_tests is responsible for loading all tests in the package.

        The pattern is deliberately not stored as a loader attribute so that
        packages can continue discovery themselves. top_level_dir is stored so
        load_tests does not need to pass this argument in to loader.discover().
        """
        set_implicit_top = False
        if top_level_dir is None and self._top_level_dir is not None:
            # make top_level_dir optional if called from load_tests in a package
            top_level_dir = self._top_level_dir
        elif top_level_dir is None:
            set_implicit_top = True
            top_level_dir = start_dir

        top_level_dir = os.path.abspath(top_level_dir)

        if not top_level_dir in sys.path:
            # all test modules must be importable from the top level directory
            # should we *unconditionally* put the start directory in first
            # in sys.path to minimise likelihood of conflicts between installed
            # modules and development versions?
            sys.path.insert(0, top_level_dir)
        self._top_level_dir = top_level_dir

        is_not_importable = False
        if os.path.isdir(os.path.abspath(start_dir)):
            start_dir = os.path.abspath(start_dir)
            if start_dir != top_level_dir:
                is_not_importable = not os.path.isfile(os.path.join(start_dir, '__init__.py'))
        else:
            is_not_importable, start_dir = self.__import_doted_module_name(is_not_importable, set_implicit_top,
                                                                           start_dir, top_level_dir)

        if is_not_importable:
            raise ImportError('Start directory is not importable: %r' % start_dir)

        tests = list(self._find_tests(start_dir, pattern))

        return self.suiteClass(tests)

    def __import_doted_module_name(self, is_not_importable, set_implicit_top, start_dir, top_level_dir):
        # support for discovery from dotted module names
        try:
            __import__(start_dir)
        except ImportError:
            is_not_importable = True
        else:
            the_module = sys.modules[start_dir]
            top_part = start_dir.split('.')[0]
            start_dir = os.path.abspath(os.path.dirname(the_module.__file__))
            if set_implicit_top:
                self._top_level_dir = os.path.abspath(os.path.dirname(os.path.dirname(sys.modules[top_part].__file__)))
                sys.path.remove(top_level_dir)
        return is_not_importable, start_dir

    def _get_name_from_path(self, path):
        path = os.path.splitext(os.path.normpath(path))[0]

        _relpath = relpath(path, self._top_level_dir)
        assert not os.path.isabs(_relpath), "Path must be within the project"
        assert not _relpath.startswith('..'), "Path must be within the project"

        name = _relpath.replace(os.path.sep, '.')
        return name

    def _get_module_from_name(self, name):
        __import__(name)
        return sys.modules[name]

    def _match_path(self, path, full_path, pattern):
        # override this method to use alternative matching strategy
        return fnmatch(path, pattern)

    def _find_tests(self, start_dir, pattern):
        """Used by discovery. Yields test suites it loads."""
        paths = os.listdir(start_dir)

        for path in paths:
            full_path = os.path.join(start_dir, path)
            if os.path.isfile(full_path):
                if not VALID_MODULE_NAME.match(path):
                    # valid Python identifiers only
                    continue
                if not self._match_path(path, full_path, pattern):
                    continue
                # if the test file matches, load it
                name = self._get_name_from_path(full_path)
                try:
                    module = self._get_module_from_name(name)
                except:
                    yield self._make_failed_import_test(name, self.suiteClass)
                else:
                    mod_file = os.path.abspath(getattr(module, '__file__', full_path))
                    realpath = os.path.splitext(mod_file)[0]
                    fullpath_noext = os.path.splitext(full_path)[0]
                    if realpath.lower() != fullpath_noext.lower():
                        module_dir = os.path.dirname(realpath)
                        mod_name = os.path.splitext(os.path.basename(full_path))[0]
                        expected_dir = os.path.dirname(full_path)
                        msg = ("%r module incorrectly imported from %r. Expected %r. "
                               "Is this module globally installed?")
                        raise ImportError(msg % (mod_name, module_dir, expected_dir))
                    yield self.loadTestsFromModule(module)
            elif os.path.isdir(full_path):
                if not os.path.isfile(os.path.join(full_path, '__init__.py')):
                    continue

                load_tests = None
                tests = None
                if fnmatch(path, pattern):
                    # only check load_tests if the package directory itself matches the filter
                    name = self._get_name_from_path(full_path)
                    package = self._get_module_from_name(name)
                    load_tests = getattr(package, 'load_tests', None)
                    tests = self.loadTestsFromModule(package, use_load_tests=False)

                if load_tests is None:
                    if tests is not None:
                        # tests loaded from package file
                        yield tests
                    # recurse into the package
                    for test in self._find_tests(full_path, pattern):
                        yield test
                else:
                    try:
                        yield load_tests(self, tests, pattern)
                    except Exception as e:
                        yield self._make_failed_load_tests(package.__name__, e, self.suiteClass)

if __name__ == "__main__":
    defaultTestLoader = TestLinkTestLoader()
