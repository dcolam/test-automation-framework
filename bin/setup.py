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
      packages=['wrapper', 'tools'],
     )
