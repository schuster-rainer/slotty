from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='slotty',
      version=version,
      description="Web Racing Management System",
      long_description="""\
""",
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='RMS flask Slotcar',
      author='Rainer Schuster',
      author_email='rainerschuster79@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points={
          'slotty.publisher': [
              'carrera unit simulator = slotty.datasimulator:poll_sensor',
          ]},
      )
