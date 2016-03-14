Le projet est compatible python 2.7 et 3.4.

- une lib divisée en deux parties:
   - wrapper : contient l'ensemble des classes qui permettent de créer un lien entre unittest, selenium et TestLink, notamment TestLinkRunner, TestLinkTestCase, UITestLinkTestCase
   - tools : contient des briques logicielles qui permettront de tester fonctionnellement notre outil. Actuellement tu trouvera SMTPBuilder et SMTPTester qui permettent respectivement de créer un mail avec une API "intuitive" et de tester le succès ou l'échec d'un envoie de mail.

- un fichier d'installation (setup.py) compatible easy_install/pip
- un exemple d'utilisation

pour l'utiliser : je conseille de faire ça dans un virtualenv pour éviter de polluer le python racine


```bash
virtualenv test_selenium --python=python3
source test_selenium/bin/activate
python setup.py install 
# ou bien pip install svn+file://path/to/project --upgrade (pour l'archive svn)
 # ou bien pip install git+file://path/to/project --upgrade (pour le dépôt git)
cd main
# configurer correctement le config.py
python generate_test.py
python lauchtestlinktests.py 
```
