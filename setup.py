import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name='uDumbDisplayLib',
  version='0.3.5',
  author='Trevor Lee',
  author_email='trevorwslee@gmail.com',
  description='MicroPython DumbDisplay Library',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/trevorwslee/MicroPython-DumbDisplay',
  project_urls = {
  },
  license='MIT',
  packages=setuptools.find_packages(exclude=['experiments', 'samples']),
  install_requires=[],
)
