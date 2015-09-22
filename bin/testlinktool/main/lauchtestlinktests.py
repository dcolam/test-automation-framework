from unittest import main, defaultTestLoader
from testlinktool.wrapper.TestLinkReport import TestLinkRunner, TestLinkTestLoader
TEST_MODULE = "tests"
TESTLINK_API_KEY = ""
TESTLINK_SERVER = "http://127.0.0.1/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
TESTLINK_PROJECT_ID = 1
TESTLINK_PLATFORM_NAME = "TEST"
MUST_CREATE_BUILD = True 

def launch(config_module=None):
    try:
        if config_module is not None:
            TESTLINK_SERVER = getattr(config_module, "TESTLINK_SERVER")
            TESTLINK_PROJECT_ID = getattr(config_module, "TESTLINK_PROJECT_ID")
            TESTLINK_PLATFORM_NAME = getattr(config_module, "TESTLINK_PLATFORM_NAME")
            TESTLINK_API_KEY = getattr(config_module, "TESTLINK_API_KEY")
            MUST_CREATE_BUILD = getattr(config_module, "MUST_CREATE_BUILD")
            
    except ImportError:
        print("Warning we are using default parameters")
    defaultTestLoader = TestLinkTestLoader()
    main(module=None,
         testRunner=TestLinkRunner(TESTLINK_SERVER, TESTLINK_PROJECT_ID, TESTLINK_PLATFORM_NAME,
                                   MUST_CREATE_BUILD, TESTLINK_API_KEY),
         argv=["", "discover", TEST_MODULE], testLoader=defaultTestLoader)
