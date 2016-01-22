=======================
Framework Installation
=======================

This framework is based on Python 3. Lower version are not supported.

virtualenv
==========

Linux Systems (Ubuntu 14+ and other debian-like example)
--------------------------------------------------------

.. sourcecode:: bash

    sudo apt-get install python-dev python3-dev
    sudo pip install virtualenv

    # go to the directory you want to handle the environment. Ensure not being logged as root.
    virtualenv virtualenv_name --python=python3
    source virtualenv_name/bin/activate

.. information:

    Your "virtual environment" is a basic directory where python, setuptools and other lib are correctly installed.
    Nothing of your virtualenv is shared to other.


On  Windows
-----------

Open powershell and launch ``(Invoke-WebRequest https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py).Content | python3``

Extract binaries and install setuptools. Then @python easy_install.py pip@
Restart powershell as administrator

.. sourcecode:: bash

    pip install virtualenv
    pip install virtualenvwrapper-powershell
    Set-ExecutionPolicy RemoteSigned
    set $env:WORKON_HOME
    Import-Module virtualenvwrapper # it could need to be launched twice
    New-VirtualEnvironment virtualenv_name --no-site-packages

As a not-privileged user you can now use ``workon virtualenv_name``.

Install with pip
================

You need to install lxml dependencies:

..sourcecode:: bash

    sudo apt-get install libz-dev libxml2-dev libxslt-dev python3-dev

Just use ``pip install git+https://github.com/vaderetro/testlink-test-wrapper``

Install with setup.py
=====================

.. sourcecode:: bash

    git clone git+https://github.com/vaderetro/testlink-test-wrapper
    cd test_automation_framework
    python setup.py install
