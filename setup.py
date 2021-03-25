# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file

from setuptools import setup, find_packages

setup(
    name="RandomDataset",
    version="0.0.1",
    description="Random dataset generation tool",
    author="Eric Kerfoot",
    author_email="eric.kerfoot@kcl.ac.uk",
    packages=find_packages(),
    install_requires=["numpy", "pandas", "click"],
    entry_points={"console_scripts": ["simplecsv = randomdataset:simple_csv"]},
)
