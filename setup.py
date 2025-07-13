import setuptools
from setuptools.config.expand import find_packages

setuptools.setup(
  name='uDumbDisplayLib',
  version='0.4.0',
  author='Trevor Lee',
  author_email='trevorwslee@gmail.com',
  description='MicroPython DumbDisplay Library',
  long_description='''
DumbDisplay MicroPython Library -- workable with Python 3 -- is a port of the [DumbDisplay Arduino Library](https://github.com/trevorwslee/Arduino-DumbDisplay)
to Micro-Python / Python 3 for the [DumbDisplay Android app](https://play.google.com/store/apps/details?id=nobody.trevorlee.dumbdisplay)
  ''',
  long_description_content_type="text/markdown",
  url='https://github.com/trevorwslee/MicroPython-DumbDisplay',
  project_urls = {
  },
  license='MIT',
  packages=find_packages(include=["dumbdisplay*"]),
  install_requires=[],
)
