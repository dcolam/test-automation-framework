================
Lancer les tests
================

Configurer et lancer
====================

Tout d'abord il vous faudra configurer le module à l'aide d'un fichier ``config.json`` qui se présente ainsi:

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
        "UI_TEST_KEYWORD": "UI"//optional, only if you want to filter the test cases by using a keyworld differencing UI (selenium) TC and pure system tests
    }


Ensuite deux solutions s'offrent à vous :

- soit vos tests sont dans un projet autonome et n'utilise pas d'import au sein de ce projet : la commande ``launch_testlink_test`` est utilisable comme le veut son manuel d'utilisation
- soit vous intégrez le dossier dans lequel les tests sont lancés dans votre path ou créez un fichier tel que launch.py qui ne fera qu'importer et appeler ``testlinktool.main.lauchtestlinktests.launch``

Exemples
--------

.. sourcecode:: python

    from testlinktool.main.lauchtestlinktests import launch
    import logging
    from logging import FileHandler, Formatter
    handler = FileHandler("text_execution.log")
    handler.setFormatter(Formatter("[%(asctime)s]:%(levelname)s: %(name)s: %(message)s"))
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.DEBUG)

    launch()


Manuel d'utilisation de la commande
===================================

``launch_testlink_test -h`` :

.. sourcecode:: bash

    usage: launch_testlink_test [-h] [-d] [-v] [-p PATTERN] [-u | -f]
                            [-I EXT_IDS | -N NAME_PATTERN]
    Lauch test from test link repository

    optional arguments:
      -h, --help            show this help message and exit

      -d, --virtual_display
                        verbosity
      -v, --verbose         verbosity

