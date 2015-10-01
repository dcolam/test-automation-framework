import argparse
from testlink import TestlinkAPIClient, TestLinkHelper
from unittest import defaultTestLoader, TestSuite
from json import load as json_read_file
from os.path import exists, join
from os import mkdir, getcwd

try:
    execfile
except NameError:
    def execfile(filename):
        global_namespace = {
            "__file__": __file__,
            "__name__": "__main__",
        }
        exec(compile(open(filename, "rb").read(), filename, 'exec'), global_namespace)


def get_test_names(suite):
    for t in suite:
        if isinstance(t, TestSuite):
            for i in get_test_names(t):
                yield i
        else:
            yield t.__class__.__name__


def __is_a_functions(precondition):
    states = {
        "NAME":
          {
              "(": "ARGS",
              " ": "BAD",
              ")": "BAD"
          },
        "ARGS":
            {
                "(": "TUPLE",
                ")": "NAME",
            },
            "TUPLE":{
                ")": "ARGS"
            }
    }
    curr_state = "NAME"
    for char in precondition.strip():
        if curr_state == "BAD":
            return False
        if char in states[curr_state]:
            curr_state = states[curr_state][char]
    return curr_state == "NAME"



def create_test_file(test_data, dest_dir, is_ui, plan, verbose=False):
    """generate the test structuyre

    :param test_data:
    :param dest_dir:
    :param is_ui:
    :param plan:
    :param verbose:
    :return:
    """
    if not exists(dest_dir):
        mkdir(dest_dir)
    # must have "test" in name because unittest explore by fetching this word
    name = test_data["suite"].lower().replace('-', '_') + ".py"
    if not name.startswith('test'):
        name = "test_" + name
    if not exists(join(dest_dir, name)):
        f = open(join(dest_dir, name), "w")
        f.write("from testlinktool.wrapper.TestLinkReport import TestLinkTestCase\n"\
                "from testlinktool.wrapper.UITestCase import UITestLinkTestCase\n\n")
    else:
        f = open(join(dest_dir, name), "a")
    try:
        f.write("\n")
        if is_ui:
            f.write("class {}(UITestLinkTestCase):\n".format(test_data["tcase_name"]))
        else:
            f.write("class {}(TestLinkTestCase):\n".format(test_data["tcase_name"]))
        f.write("    external_id = '{}'\n".format(test_data["full_external_id"]))
        f.write("    version = {}\n".format(test_data["version"]))
        f.write("    customfield_names = [{}]\n\n".format(",".join(['"' + name + '"' for name, _ in test_data["custom_fields"].items() if _["value"] != ""])))
        f.write("    @classmethod\n"\
                "    def get_plan_name(cls):\n"\
                "        return '{}'\n\n".format(plan))
        preconditions = test_data.get('preconditions', '').replace('</p>', "").replace("\n", "\n        ").replace('&quot;', "'").split("<p>")
        is_all_function = preconditions and all([__is_a_functions(p) for p in preconditions if p.strip() != ''])
        if is_ui:
            f.write("    def run_test_on_current_browser(self):\n" +
                    '        """{}\n        """\n'.format(test_data['summary'].strip().replace("\n", "\n        ")) +
                    "        pass\n\n")


            if not is_all_function and preconditions:
                f.write("    def setUpUi(self):\n")
                f.write('        """{}"""\n        pass\n'.format("\n        ".join(preconditions)))
            elif preconditions:
                f.write("    def setUpUi(self):\n")
                preconditions = [p.strip().replace('driver', 'self.driver') for p in preconditions]
                f.write('    {}\n\n'.format("\n        ".join(preconditions)))
        else:

            if not is_all_function and preconditions:
                f.write("    def setUp(self):\n")
                f.write('        """{}\n        """\n        pass\n'.format("\n        ".join(preconditions)))
            else:
                f.write("    def setUp(self):\n")
                f.write('    {}\n\n'.format("\n        ".join(preconditions)))
            if len(test_data['steps']) == 0:
                f.write("    def testStep0(self):\n" +
                        '        """some test\n'\
                        '            expected:\n'\
                        '            Unknown"""\n'+
                        "        pass\n\n")
            else:
                for i, step in enumerate(test_data['steps']):
                    f.write("    def testStep{}(self):\n".format(i) +
                            '        """{}\n'\
                            '            expected:\n'\
                            '            {}"""\n'.format(step["actions"].strip().replace("\n", "\n        "),
                                                         step["expected_results"].strip().replace("\n", "\n        "))+
                            "        pass\n\n")
        f.write("\n")
    except Exception:
        pass
    finally:
        f.close()


def get_tests(testlink_client, keyword, plan, TESTLINK_PROJECT_ID, CUSTOM_FIELD_NAME_LIST):
    if keyword:
        cases = testlink_client.getTestCasesForTestPlan(plan, details="full", keywords=keyword, executiontype=2)
    else:
        cases = testlink_client.getTestCasesForTestPlan(plan, details="full", keywords=keyword, executiontype=2)

    temp = cases.values()
    cases = []
    if isinstance(temp, dict): # in case of deepest formating.
        temp = temp.values()
    for values in temp:
        for v in values:
            v["keyword"] = keyword
        cases += values
    for test in cases:
        test.update(testlink_client.getTestCase(testcaseid=test["tc_id"])[0])
        test["custom_fields"] = {}
        for field in CUSTOM_FIELD_NAME_LIST:
            test["custom_fields"][field] = testlink_client.getTestCaseCustomFieldDesignValue(test["full_external_id"],
                                                                                int(test["version"]),
                                                                                TESTLINK_PROJECT_ID,
                                                                                field, "simple")
    return cases


def main(config_module=None):
    from testlinktool.main.config import TESTLINK_SERVER, TESTLINK_PROJECT_ID, TESTLINK_PROJECT_NAME,\
                                         TESTLINK_API_KEY, CUSTOM_FIELD_NAME_LIST, UI_TEST_KEYWORD

    try:
        
        if config_module is not None:
            TESTLINK_SERVER = getattr(config_module, "TESTLINK_SERVER")
            TESTLINK_PROJECT_ID = getattr(config_module, "TESTLINK_PROJECT_ID")
            TESTLINK_PROJECT_NAME = getattr(config_module, "TESTLINK_PROJECT_NAME")
            TESTLINK_API_KEY = getattr(config_module, "TESTLINK_API_KEY")
            CUSTOM_FIELD_NAME_LIST = getattr(config_module, "CUSTOM_FIELD_NAME_LIST")
            UI_TEST_KEYWORD = getattr(config_module, "UI_TEST_KEYWORD")
        elif exists(join(getcwd(), 'config.py')):
            execfile(join(getcwd(), 'config.py'))
        elif exists(join(getcwd(), 'config.json')):
            with open(join(getcwd(), 'config.json')) as j_file:
                conf_dic = json_read_file(j_file)
                TESTLINK_SERVER = conf_dic["TESTLINK_SERVER"]
                TESTLINK_PROJECT_ID = conf_dic["TESTLINK_PROJECT_ID"]
                TESTLINK_PROJECT_NAME = conf_dic["TESTLINK_PROJECT_NAME"]
                TESTLINK_API_KEY = conf_dic["TESTLINK_API_KEY"]
                CUSTOM_FIELD_NAME_LIST = conf_dic["CUSTOM_FIELD_NAME_LIST"]
                UI_TEST_KEYWORD = conf_dic["UI_TEST_KEYWORD"]
    except ImportError:
        print("Warning we are using default parameters")
    parser = argparse.ArgumentParser(description='')
    group = parser.add_argument_group()
    group.add_argument('-d', '--test-dir', dest='dest_dir',
                       help="The directory path where generated tests will be sent (defaults to 'tests')",
                       default="tests")
    group.add_argument('-p', '--plan', dest='plan', help="the test plan", default=None, required=True)
    group.add_argument('-a', '--download-all', dest='download_all', default=False, action="store_true",
                       help="if used will download all tests, even those which are already coded")
    group.add_argument('-v', '--verbose', dest='verbose', default=False, action="store_true",
                       help="verbosity")
    
    args = parser.parse_args()

    tl_helper = TestLinkHelper(TESTLINK_SERVER, TESTLINK_API_KEY)
    testlink_client = tl_helper.connect(TestlinkAPIClient)
    plan_id = int(testlink_client.getTestPlanByName(TESTLINK_PROJECT_NAME, args.plan)[0]['id'])
    suites = testlink_client.getTestSuitesForTestPlan(plan_id)
    suites_tc_dic = {
        suite["id"]: suite["name"] for suite in suites
    }
    
    cases = get_tests(testlink_client, UI_TEST_KEYWORD, plan_id, TESTLINK_PROJECT_ID, CUSTOM_FIELD_NAME_LIST)
    names = [n["tcase_name"] for n in cases]
    other_cases = get_tests(testlink_client, None, plan_id, TESTLINK_PROJECT_ID, CUSTOM_FIELD_NAME_LIST)
    cases += [n for n in other_cases if n["tcase_name"] not in names]
    for case in cases:
        case["suite"] = suites_tc_dic[case["testsuite_id"]]
    #print(json.dumps(cases, indent=4))
    tests = []
    if not args.download_all:
        tests += list(set([a for a in get_test_names(defaultTestLoader.discover(args.dest_dir))]))
    print(tests)
    for to_be_created in cases:
        if to_be_created["tcase_name"] not in tests:
            create_test_file(to_be_created, args.dest_dir, to_be_created["keyword"] == UI_TEST_KEYWORD, args.plan)
    
        

if __name__ == "__main__":
    main()
