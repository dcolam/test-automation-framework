from unittest import main, defaultTestLoader
from wrapper.TestLinkReport import TestLinkRunner, TestLinkTestLoader
TEST_MODULE = "tests"
TESTLINK_API_KEY = ""
TESTLINK_SERVER = "http://127.0.0.1/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
TESTLINK_PROJECT_ID = 1
TESTLINK_PLATFORM_NAME = "TEST"
MUST_CREATE_BUILD = True
try:
    from config import *
except ImportError:
    print("Warning we are using default parameters")


if __name__ == "__main__":
    defaultTestLoader = TestLinkTestLoader()
    main(module=None,
         testRunner=TestLinkRunner(TESTLINK_SERVER, TESTLINK_PROJECT_ID, TESTLINK_PLATFORM_NAME,
                                   MUST_CREATE_BUILD, TESTLINK_API_KEY),
         argv=["", "discover", TEST_MODULE], testLoader=defaultTestLoader)
