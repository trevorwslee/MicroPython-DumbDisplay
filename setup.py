import setuptools
from setuptools.config.expand import find_packages


# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
  name='uDumbDisplayLib',
  version='0.5.0',
  author='Trevor Lee',
  author_email='trevorwslee@gmail.com',
  description='MicroPython DumbDisplay Library',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/trevorwslee/MicroPython-DumbDisplay',
  project_urls = {
  },
  license='MIT',
  packages=find_packages(include=["dumbdisplay*"]),
  install_requires=[],
)
