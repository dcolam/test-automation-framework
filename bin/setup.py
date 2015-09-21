from setuptools import setup

setup(name='testlink_runner',
      version='1.0.0',
      description='Unittest wrapper to create interactions between testlink and python tests',
      author='Vade Retro technology',
      url='',
      install_requires=[
        "TestLink-API-Python-client",
        "selenium"
      ],
      packages=['testlinktool.wrapper', 'testlinktool.tools', 'testlinktool.main'],
      entry_points={
          'console_scripts': [
              'generate_test = testlinktool.main:generate_test',
              'launch_test = testlinktool.main:lauch_test',
          ],
      })
