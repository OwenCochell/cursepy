"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""


# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

# Import cursepy so we can get our metadata:

import cursepy

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Set the project homepage
home = 'https://github.com/Owen-Cochell/cursepy'

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='cursepy',
    version=cursepy.__version__,
    description='CurseForge API written in python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=home,
    author='Owen Cochell',
    author_email='owencochell@hotmail.com',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',
        # Stating that we are platform independent:
        'Operating System :: OS Independent',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='curseforge, api, curseforge-api',
    packages=find_packages(),
    python_requires='>=3.7, <4',
    package_data={},
    project_urls={
        'Bug Reports': f'{home}/issues',
        'Source': home,
        'Documentation': 'https://cursepy.readthedocs.io/',
    },
)
