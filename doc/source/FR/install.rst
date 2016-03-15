=========================
Installation du framework
=========================

Le framework de test est compatible python 2.7 et 3.4. Python 3.4 est fortement conseillé.
L'installation du framework se fait selon l'une des méthodes standard dans l'écosystème python pip ou setup.py.
Il est fortement conseillé de travailler dans un virtualenv

virtualenv
==========

Sur Linux (exemple pris sur ubuntu et autre debianlike)
-------------------------------------------------------

.. sourcecode:: bash

    sudo apt-get install python-dev python3-dev
    sudo pip install virtualenv

    # allez dans le dossier adéquat, veillez à ne pas être en superutilisateur
    virtualenv nom_de_votre_virtualenv --python=python3
    source nom_de_votre_virtualenv/bin/activate

.. information:

    la commande @virtualenv@ génère l'environnement dans un dossier portant le nom que vous lui spécifié et le place dans le répertoir actuel. Il peut être adéquat de mettre ces environnement dans /opt/ pour ne pas polluer vos espaces de travail


Sur Windows
-----------

.. information:

    il vous faut installer turtoise svn et vous assurer que l'executable de svn-cli se trouve dans votre PATH, il en est de même avec python

Ouvrez powershell et entrez ``(Invoke-WebRequest https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py).Content | python3``

Dézippez l'archive setuptools et entrez ensuite @python easy_install.py pip@
Redémarrez powershell en mode administrateur pour que l'environnement et PATH soient mis à jour.

.. sourcecode:: bash

    pip install virtualenv
    pip install virtualenvwrapper-powershell
    Set-ExecutionPolicy RemoteSigned
    set $env:WORKON_HOME
    Import-Module virtualenvwrapper # si powershell vous envoie une erreur, lancez la commande une seconde fois, elle passera
    New-VirtualEnvironment nom_de_votre_virtualenv --no-site-packages

fermez la fenêtre adminstrateur et relancez un powershell en utilisateur normal pour lancer ``workon nom_de_votre_virtualenv``

Installer avec pip
==================

Installez les dépendances à lxml:

..sourcecode:: bash

    sudo apt-get install libz-dev libxml2-dev libxslt-dev python3-dev

Lancez simplement ``pip install test-automation-framework``

Installer avec setup.py
=======================

.. sourcecode:: bash

    svn co git+https://github.com/vaderetro/testlink-test-wrapper
    cd test_automation_framework/bin
    python setup.py install
