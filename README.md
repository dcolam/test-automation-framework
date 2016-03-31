[![Documentation Status](https://readthedocs.org/projects/test-automation-framework/badge/?version=latest)](http://test-automation-framework.readthedocs.org/en/latest/?badge=latest)
[![Requirements Status](https://requires.io/github/VadeRetro/test-automation-framework/requirements.svg?branch=master)](https://requires.io/github/VadeRetro/test-automation-framework/requirements/?branch=master)
[![Licence GPL](http://img.shields.io/badge/license-GPL-yellow.svg)](http://www.gnu.org/licenses/quick-guide-gplv3.fr.html)

# test-automation-framework
Unittest wrapper to create interactions between testlink and python tests

This wrapper contains two parts so that you can build up fancy system and integration tests.

We provide you a easy to use way to report your test results to testlink and a unittest oriented API for running web UI tests.

# Install with pip

```bash
virtualenv test_selenium --python=python3
source test_selenium/bin/activate
python setup.py install
pip install test-automation-framework
cd main
# configurer correctement le config.py
python generate_test.py
python lauchtestlinktests.py
```

# Test framework

You also need PhantomJS to be able to launch tests : `apt-get install phantomjs`.

Clone the repo and run `python setup.py test -s tests`.
