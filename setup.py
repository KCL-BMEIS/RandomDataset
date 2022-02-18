# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file

import os
from setuptools import setup, find_packages
from pkg_resources import parse_requirements

# It's important to note that this file doesn't import randomdataset to get the version information, but interprets
# the _version.py file instead. This prevents the situation when installing using this file without all the depenencies
# already present, this file won't be runnable in this case. 

source_dir = os.path.abspath(os.path.dirname(__file__))

# read the version and other data from _version.py
with open(os.path.join(source_dir, "randomdataset/_version.py")) as o:
    exec(o.read())

# read install requirements from requirements.txt
#with open(os.path.join(source_dir, "requirements.txt")) as o:
#    requirements = [str(r) for r in parse_requirements(o.read())]

requirements = ['numpy>=1.18', 'pandas', 'click', 'pyyaml']
    
setup(
    name=__appname__,
    version=__version__,
    description=__description__,
    long_description=__long_description__,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license=__license__,
    packages=find_packages(),
    install_requires=requirements,
    entry_points={"console_scripts": ["generate_dataset = randomdataset:generate_dataset"]},
)
