from setuptools import setup, find_packages
import sys, os

version = '0.2'

setup(name='twhst',
      version=version,
      description="Follow and store tweets from twitter",
      long_description="""\
      twhst stores tweets which complains predefinied rules. It uses Twitter's
      search api.
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='twitter',
      author='Aitzol Naberan',
      author_email='anaberan@codesyntax.com',
      url='http://github.com/codesyntax/twhst',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'tweepy',
          'django'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
