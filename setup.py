from setuptools import setup, find_packages
import sys, os

version = '1.0dev'

setup(name='torrents_streamer',
      version=version,
      description="Pipe line torrents files streamer",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='torrents tream',
      author='Maxym Enkidu Shalenyi',
      author_email='supamaxy@gmail.com',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "docopt",
          "requests",
          "tempdir",
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      [console_scripts]
      tstream = torrents_streamer.cli:cli
      # -*- Entry points: -*-
      """,
      )
