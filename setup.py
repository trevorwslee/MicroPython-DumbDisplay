import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name='uDumbDisplayLib',
  version='0.2.0',
  author='Trevor Lee',
  author_email='trev_lee@hotmail.com',
  description='Micro-Python DumbDisplay Library',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/trevorwslee/MicroPython-DumbDisplay',
  project_urls = {
  },
  license='MIT',
  packages=[],
  install_requires=[],
)
