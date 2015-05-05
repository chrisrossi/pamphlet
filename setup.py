from setuptools import setup
from setuptools import find_packages

VERSION = '0.1dev'

requires = [
    'pyramid',
    'pyramid_chameleon',
    'toolz',
]

setup(name='tikibar',
      version=VERSION,
      description="Toolbar for basic CRUD operations on content.",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
     )
