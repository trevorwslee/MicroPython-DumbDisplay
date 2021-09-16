import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name='dumbdisplay',
  version='0.0.1',
  author='Trevor Lee',
  author_email='trev_lee@hotmail.com',
  description='DumbDisplay for Micro-Python',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/trevorwslee/MicroPython-DumbDisplay',
  project_urls = {
  },
  license='MIT',
  packages=[],
  install_requires=[],
)
