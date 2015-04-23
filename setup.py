from setuptools import setup
from setuptools import find_packages

VERSION = '0.1dev'

requires = [
    'dumpling',
    'pyramid',
]

setup(name='pamphlet',
      version=VERSION,
      description="Low powered CMS with focuse on ease of use for small "
                  "number of non-expert content authors.",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      """)

