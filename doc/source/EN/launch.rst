=============
Launch  tests
=============

Basic configuration
===================

Everything is handled by a ``config.json`` file as this one:

.. sourcecode:: json

    {
        "TEST_MODULE": "tests",
        "TESTLINK_API_KEY": "your_key_as_hexadecimal_32_char_long_string",
        "CUSTOM_FIELD_NAME_LIST": [
            "customfield1", "customfield_2"
        ],
        "MUST_CREATE_BUILD": false, //true if you want the runner to mark this run as a new build
        "TESTLINK_PROJECT_ID": 1124,
        "TESTLINK_SERVER": "http://testlink_address/testlink/lib/api/xmlrpc/v1/xmlrpc.php",
        "TESTLINK_PROJECT_NAME": "ProjectName",
        "TESTLINK_PLATFORM_NAME": "TestingPlatformName",
        "UI_TEST_KEYWORD": "UI"//optional, only if you want to filter the test cases by using a keyworld differencing UI (selenium) TC and pure system tests. Those keywords depend on your TestLink configuration
    }


Basically you can use two ways :

- Your tests are autonomous or everything you depends on is in your PATH : ``launch_testlink_test`` is here for you. It will use the config.json in current working dir.
- You need to use non registered dependencies or centralize every commands:  just import and call ``testlinktool.main.lauchtestlinktests.launch``

Example
-------

.. sourcecode:: python

    from testlinktool.main.lauchtestlinktests import launch
    import logging
    from logging import FileHandler, Formatter
    handler = FileHandler("text_execution.log")
    handler.setFormatter(Formatter("[%(asctime)s]:%(levelname)s: %(name)s: %(message)s"))
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.DEBUG)

    launch()


Command man
===========

``launch_testlink_test -h`` :

.. sourcecode:: bash

    usage: launch_testlink_test [-h] [-d] [-v] [-p PATTERN] [-u | -f]
                            [-I EXT_IDS | -N NAME_PATTERN]
    Lauch test from test link repository

    optional arguments:
      -h, --help            show this help message and exit

      -d, --virtual_display
      -v, --verbose         verbosity

