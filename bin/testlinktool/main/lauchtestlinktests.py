from unittest import main, defaultTestLoader
from testlinktool.wrapper.TestLinkReport import TestLinkRunner, TestLinkTestLoader

from os import getcwd
from os.path import exists, join
try:
    execfile
except NameError:
    def execfile(filename):
        exec(compile(open(filename, "rb").read(), filename, 'exec'))

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
        elif exists(join(getcwd(), 'config.py')):
            execfile(join(getcwd(), 'config.py'))
    except ImportError:
        print("Warning we are using default parameters")
    defaultTestLoader = TestLinkTestLoader()
    main(module=None,
         testRunner=TestLinkRunner(TESTLINK_SERVER, TESTLINK_PROJECT_ID, TESTLINK_PLATFORM_NAME,
                                   MUST_CREATE_BUILD, TESTLINK_API_KEY),
         argv=["", "discover", TEST_MODULE], testLoader=defaultTestLoader)
