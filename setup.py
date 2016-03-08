from setuptools import setup

setup(name='testlink_runner',
      version='1.0.1',
      description='Unittest wrapper to create interactions between testlink and python tests',
      author='Vade Retro technology',
      author_email="support@vade-retro.com",
      url='',
      keywords=["test", "reporting", "unittest"],
      classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
        ],
      long_description="""
      This library aims to create a bridge between unittest and testlink.

      As Testlink deals with integration and system testing more than bare unit tests, we include a simple API to
      add assertions related to your UI. This uses selenium.
      """,
      install_requires=[
        "TestLink-API-Python-client==0.6.2",
        "selenium==2.52.0",
        "xvfbwrapper==0.2.8",
        "lxml==3.5.0"
      ],
      packages=['testlinktool.wrapper', 'testlinktool.main'],
      entry_points={
          'console_scripts': [
              'generate_testlink_test = testlinktool.main.generate_test:main',
              'launch_testlink_test = testlinktool.main.lauchtestlinktests:launch',
          ],
      })
