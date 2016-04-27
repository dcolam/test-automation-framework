"""

Copyright (c) 2016 "Vade Retro Technology"

...


This file is part of test-automation-framework.


test-automation-framework is free software: you can redistribute it and/or modify

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
from setuptools import setup

with open("README.md") as desc_file:
    long_desc = desc_file.read()

__doc__ = long_desc

with open("requirements.txt") as req_file:
    requirements = list(filter(None, req_file.read().split("\n")))

setup(name='test-automation-framework',
      version='1.0.0',
      description='Unittest wrapper to create interactions between testlink and python tests',
      author='Vade Retro technology',
      author_email="support@vade-retro.com",
      url='https://github.com/VadeRetro/test-automation-framework',
      keywords=["test", "reporting", "unittest"],
      classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
        ],
      long_description=long_desc,
      install_requires=requirements,
      packages=['testlinktool.wrapper', 'testlinktool.main'],
      entry_points={
          'console_scripts': [
              'generate_testlink_test = testlinktool.main.generate_test:main',
              'launch_testlink_test = testlinktool.main.lauchtestlinktests:launch',
          ]
      }
      )
