from wrapper.TestLinkReport import TestLinkTestCase
from wrapper.UITestCase import UITestLinkTestCase

class LoginVRC(UITestLinkTestCase):
    external_id = 'POC-SEL-4'
    version = 1
    customfield_names = ["execution_server"]
    @classmethod
    def get_plan_name(cls):
        return 'TestString'
    def run_test_on_current_browser(self):
        """<p>
        	tries to log to vrc</p>"""
        pass
