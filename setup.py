from setuptools import setup
setup(
  name = 'gee_toolbox',
  py_modules = ['gee'],
  version = '0.0.0.7',
  description = 'A convenience module and command line tool for GEE.',
  author = 'Brookie Guzder-Williams',
  author_email = 'bguzder-williams@wri.org',
  url = 'https://github.com/wri/gee_toolbox',
  download_url = 'https://github.com/wri/gee_toolbox/tarball/0.1',
  keywords = ['gee', 'earth engine','gis'],
  classifiers = [],
  install_requires=[
      'cryptography<=1.4',
      'oauth2client<=1.5.2',
      'earthengine-api'
  ],
  entry_points={
      'console_scripts': [
          'gee=gee:main',
      ],
  }
)