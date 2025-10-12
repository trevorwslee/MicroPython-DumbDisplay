import setuptools
from setuptools.config.expand import find_packages


setuptools.setup(
  name='uDumbDisplayLib',
  version='0.6.5',
  author='Trevor Lee',
  author_email='trevorwslee@gmail.com',
  description='MicroPython DumbDisplay Library',
  long_description_content_type="text/markdown",
  url='https://github.com/trevorwslee/MicroPython-DumbDisplay',
  license='MIT',
  packages=find_packages(include=["dumbdisplay*"]),
  package_data={
    'space_shooting_resources': ['dumbdisplay_examples/space_shooting/*.png', 'dumbdisplay_examples/space_shooting/*.wav'],
  },
)
