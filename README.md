# RandomDataset

[![Documentation Status](https://readthedocs.org/projects/randomdataset/badge/?version=latest)](https://randomdataset.readthedocs.io/en/latest/?badge=latest)
[![Testing](https://github.com/KCL-BMEIS/RandomDataset/workflows/Unittests/badge.svg)](https://github.com/KCL-BMEIS/RandomDataset/actions)
[![codecov](https://codecov.io/gh/KCL-BMEIS/RandomDataset/branch/master/graph/badge.svg)](https://codecov.io/gh/KCL-BMEIS/RandomDataset)

Generates random datasets for testing and fun.

This repository contains a simple library for generating random tabular datasets of virtually any size. It also serves
as an example repository for a Python code base with basic CI/CD integration and tools. 

Install this library from a git clone:

```bash
$ pip install .
```

Data is generated from a YAML schema describing the names of tables/datasets and the fields they have. The YAML file
consists of a sequence of dictionaries used to instantiate objects from the library or from other libraries present
in the Python path. This allows custom code to be injected into the generation process.

An example schema is used to generate a list of customer records in `customerschema.yaml`:

```yaml
- typename: randomdataset.generators.CSVGenerator
  num_lines: 10
  dataset:
    name: customers
    typename: randomdataset.Dataset
    fields:
    - name: id
      typename: randomdataset.UIDFieldGen
    - name: FirstName
      typename: randomdataset.StrFieldGen
      lmin: 6
      lmax: 14
    - name: LastName
      typename: randomdataset.StrFieldGen
      lmin: 6
      lmax: 14
```

This will create a single dataset "customers" stored in a CSV file `customers.csv`. This file is geneated by invoking
the included command:

```bash
$ generate_dataset customerschema.yaml .
```

This generates the `customers.csv` file:

```csv
id,FirstName,LastName
0,"QDFFgv4XBd5VW","O1Odro"
1,"Gp4mYq","82IPIChjBALg"
2,"LR7KVudB","HcAPBwM"
3,"6FfWGEYS0Q","5NbspSBJk"
4,"si1Tj0xSBB2","eChYKAaW5aa8R"
5,"DYP6OMerUUFOR","pYNXUTNLqdrv"
6,"ltfnhTgrJF","2Rctye"
7,"1tAoaDl57Lo5","xMkVKt6O"
8,"1yJImoqiwf","IJICD8W6B8k"
9,"XkYgS7","8owHyjR"
```

## Repository Setup

A relatively simple set of features which link into the code are set up on this repo to ensure good coding practice:

* Automatic documentation generation is done using ReadTheDocs, see [README.md](./docs/README.md)
* CI/CD implemented as flake8 and unit test execution using Github Actions, see [python-app.yml](./.github/workflows/python-app.yml)
* Code coverage is displayed using Codecov

Both ReadTheDocs and Codecov are integrated with the repo as webhooks. These can be setup through their respective sites
which require Github credentials to link with repos.

This repo mostly follows [GitFlow](http://datasift.github.io/gitflow/IntroducingGitFlow.html) with a `master` branch 
which is always the current release of the code, and a `dev` branch that is the development version of the code. 
Branch protection rules are in place for `master` which ensure that code can only be committed to the branch through 
reviewed PRs:

* Require pull request reviews before merging
* Require status checks to pass before merging ("build" action selected)
* Require branches to be up to date before merging 
* Require linear history 
* Include administrators

## PyPI Release

Whenever a new release is made this is uploaded automatically to PyPI using the default Github workflow "Publish Python 
Package". To upload to PyPI [these steps](https://packaging.python.org/tutorials/packaging-projects/) explain the 
process. For this repo the basic steps are:

1. Create account on pypi.org
2. Create a wheel file with `python setup.py bdist_wheel`, this creates `dist/RandomDataset-0.1.0-py3-none-any.whl`
3. Upload this package manually to PyPI with `python -m twine upload dist/*` (assuming you have twine already installed)
4. Get the API token for the new package and set it to the secret `PYPI_API_TOKEN` in the repository's settings
5. Add the workflow file `.github/workflows/python-publish.yml` from [here](https://github.com/actions/starter-workflows/blob/main/ci/python-publish.yml).
6. Commit changes and create a release for the project, this should upload to PyPI automatically

