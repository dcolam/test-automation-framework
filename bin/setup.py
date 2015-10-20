from setuptools import setup

setup(name='testlink_runner',
      version='1.0.1',
      description='Unittest wrapper to create interactions between testlink and python tests',
      author='Vade Retro technology',
      url='',
      install_requires=[
        "TestLink-API-Python-client",
        "selenium",
        "jsonpickle"
      ],
      packages=['testlinktool.wrapper', 'testlinktool.main',
                'vrc-kit-service'],
      entry_points={
          'console_scripts': [
              'generate_testlink_test = testlinktool.main.generate_test:main',
              'launch_testlink_test = testlinktool.main.lauchtestlinktests:launch',
          ],
      })
