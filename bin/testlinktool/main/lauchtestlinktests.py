from unittest import main
from xvfbwrapper import Xvfb
from testlinktool.wrapper.TestLinkReport import TestLinkRunner, TestLinkTestLoader
import argparse
from os import getcwd
from os.path import exists, join
from json import load as json_read_file
try:
    execfile
except NameError:
    def execfile(filename):
        global_namespace = {
            "__file__": __file__,
            "__name__": "__main__",
        }
        exec(compile(open(filename, "rb").read(), filename, 'exec'), global_namespace)


def launch(config_module=None):
    try:
        from testlinktool.main.config import TESTLINK_SERVER, TESTLINK_PROJECT_ID, TESTLINK_PLATFORM_NAME,\
                                             MUST_CREATE_BUILD, TESTLINK_API_KEY, TEST_MODULE
        print(join(getcwd(), 'config.py'))
        
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
        print("Warning we are using default parameters")
    parser = argparse.ArgumentParser(description='Lauch test from test link repository')
    group = parser.add_argument_group()
    group.add_argument('-d', '--virtual_display', dest='is_virtual', default=False, action="store_true",
                       help="verbosity")
    group.add_argument('-v', '--verbose', dest='verbose', default=False, action="store_true",
                       help="verbosity")

    args = parser.parse_args()
    if args.is_virtual:
        with Xvfb(1920, 1080):
            _lauch_runner(TESTLINK_SERVER, TESTLINK_PROJECT_ID, TESTLINK_PLATFORM_NAME,
                   MUST_CREATE_BUILD, TESTLINK_API_KEY, TEST_MODULE)
    else:
        _lauch_runner(TESTLINK_SERVER, TESTLINK_PROJECT_ID, TESTLINK_PLATFORM_NAME,
               MUST_CREATE_BUILD, TESTLINK_API_KEY, TEST_MODULE)


def _lauch_runner(TESTLINK_SERVER, TESTLINK_PROJECT_ID, TESTLINK_PLATFORM_NAME,
                  MUST_CREATE_BUILD, TESTLINK_API_KEY, TEST_MODULE):
            defaultTestLoader = TestLinkTestLoader()
            main(module=None,
                 testRunner=TestLinkRunner(TESTLINK_SERVER, TESTLINK_PROJECT_ID, TESTLINK_PLATFORM_NAME,
                                           MUST_CREATE_BUILD, TESTLINK_API_KEY),
                 argv=["", "discover", TEST_MODULE], testLoader=defaultTestLoader)
