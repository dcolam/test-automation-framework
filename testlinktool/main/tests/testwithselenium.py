"""

Copyright (c) 201x "Vade Retro Technology"

...


This file is part of test-automation-framework.


xxxxx is free software: you can redistribute it and/or modify

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
