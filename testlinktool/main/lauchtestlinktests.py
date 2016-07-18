"""

Copyright (c) 2016 "Vade Secure"

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
from unittest import main
from xvfbwrapper import Xvfb
from testlinktool.wrapper.TestLinkReport import TestLinkRunner, TestLinkTestLoader
import argparse
from os import getcwd
from os.path import exists, join
from json import load as json_read_file
import logging
try:
    execfile
except NameError:
    def execfile(filename):
        global_namespace = {
            "__file__": __file__,
            "__name__": "__main__",
        }
        exec(compile(open(filename, "rb").read(), filename, 'exec'), global_namespace)
_log = logging.getLogger("testlinkrunner")


class StoreExtId(argparse.Action):
    def __call__(self,  parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.split(","))


def launch(config_module=None):
    # get configuration
    try:
        from testlinktool.main.config import TESTLINK_SERVER, TESTLINK_PROJECT_ID, TESTLINK_PLATFORM_NAME,\
                                             MUST_CREATE_BUILD, TESTLINK_API_KEY, TEST_MODULE
        _log.debug(join(getcwd(), 'config.py'))
        
        if config_module is not None:
            TESTLINK_SERVER = getattr(config_module, "TESTLINK_SERVER")
            TESTLINK_PROJECT_ID = getattr(config_module, "TESTLINK_PROJECT_ID")
            TESTLINK_PLATFORM_NAME = getattr(config_module, "TESTLINK_PLATFORM_NAME")
            TESTLINK_API_KEY = getattr(config_module, "TESTLINK_API_KEY")
            MUST_CREATE_BUILD = getattr(config_module, "MUST_CREATE_BUILD")
            TEST_MODULE = getattr(config_module, "TEST_MODULE")
        elif exists(join(getcwd(), 'config.py')):
            execfile(join(getcwd(), 'config.py'))
        elif exists(join(getcwd(), 'config.json')):
            with open(join(getcwd(), 'config.json')) as j_file:
                conf_dic = json_read_file(j_file)
                TESTLINK_SERVER = conf_dic["TESTLINK_SERVER"]
                TESTLINK_PROJECT_ID = conf_dic["TESTLINK_PROJECT_ID"]
                TESTLINK_PLATFORM_NAME = conf_dic["TESTLINK_PLATFORM_NAME"]
                TESTLINK_API_KEY = conf_dic["TESTLINK_API_KEY"]
                MUST_CREATE_BUILD = conf_dic["MUST_CREATE_BUILD"]
                TEST_MODULE = conf_dic["TEST_MODULE"]

    except ImportError:
        _log.warning("We are using default parameters")
    parser = argparse.ArgumentParser(description='Lauch test from test link repository')
    group = parser.add_argument_group()
    group.add_argument('-d', '--virtual_display', dest='is_virtual', default=False, action="store_true",
                       help="verbosity")
    group.add_argument('-v', '--verbose', dest='verbose', default=False, action="store_true",
                       help="verbosity")
    filter_group = group.add_argument_group()
    filter_group.add_argument("-p", "--pattern", dest="pattern", default=None, help="pattern that test file must match")
    tag_group = filter_group.add_mutually_exclusive_group()
    tag_group.add_argument("-u", "--uitag", dest="only_ui", default=False,
                           action="store_true", help="run only uitagged tests")
    tag_group.add_argument("-f", "--foncttag", dest="only_fonctional", default=False,
                           action="store_true", help="run only fonctional tagged tests")
    ext_id_group = filter_group.add_mutually_exclusive_group()
    ext_id_group.add_argument('-I', "-idlist", dest="ext_ids", action=StoreExtId, default=None,
                              help="Comma separated list of external ids")
    ext_id_group.add_argument('-N', "--name-pattern", dest="name_pattern", default="")

    args = parser.parse_args()

    filter_args = {
        "only_ui": args.only_ui,
        "only_fonctional": args.only_fonctional,
        "ext_ids": args.ext_ids,
        "name_pattern": args.name_pattern,
        "generate_xml": True
    }
    if args.is_virtual:
        with Xvfb(1920, 1080, extension="RANDR"):  # will force to use randr to avoid
            # extension "RANDR" missing on display freezing error
            _lauch_runner(TESTLINK_SERVER, TESTLINK_PROJECT_ID, TESTLINK_PLATFORM_NAME,
                          MUST_CREATE_BUILD, TESTLINK_API_KEY, TEST_MODULE, test_pattern=args.pattern,
                          verbose=args.verbose, **filter_args)
    else:
        _lauch_runner(TESTLINK_SERVER, TESTLINK_PROJECT_ID, TESTLINK_PLATFORM_NAME,
                      MUST_CREATE_BUILD, TESTLINK_API_KEY, TEST_MODULE, test_pattern=args.pattern, verbose=args.verbose,
                      **filter_args)


def _lauch_runner(TESTLINK_SERVER, TESTLINK_PROJECT_ID, TESTLINK_PLATFORM_NAME,
                  MUST_CREATE_BUILD, TESTLINK_API_KEY, TEST_MODULE, verbose=False, test_pattern=None, **kwargs):
    defaultTestLoader = TestLinkTestLoader(**kwargs)
    args = ["", "discover", "-s", TEST_MODULE]
    if test_pattern:
        args.append("-p")
        args.append(str(test_pattern))
    main(module=None,
         testRunner=TestLinkRunner(TESTLINK_SERVER, TESTLINK_PROJECT_ID, TESTLINK_PLATFORM_NAME,
                                   MUST_CREATE_BUILD, TESTLINK_API_KEY, verbose=verbose, generate_xml=True),
         argv=args, testLoader=defaultTestLoader)
