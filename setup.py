from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

setup(
  name = 'texplotting',
  packages = ['texplotting'],
  include_package_data = True,
  description = 'Provides a function to save processed versions of matplotlib',
  author = 'Chris MacMackin',
  author_email = 'cmacmackin@gmail.com',
  install_requires = ['matplotlib',],
)
