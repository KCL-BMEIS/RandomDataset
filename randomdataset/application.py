# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file

import os
from typing import List
from tempfile import TemporaryDirectory

import click

from .__init__ import __version__
from .generators import DataGenerator
from .schemaparser import parse_schema

__all__ = ["generate_dataset", "print_test"]


@click.command("generate_dataset")
@click.argument("schema", type=click.File('r', lazy=True))
@click.argument("output", type=click.Path(writable=True, resolve_path=True))
@click.version_option(__version__, message="%(version)s")
def generate_dataset(schema, output):
    """
    This script generates a random dataset from a given YAML schema. SCHEMA is the input YAML schema file describing the
    fields and length of the dataset to generate. OUTPUT is the output file or directory to store the dataset.
    """
    click.echo(f"Schema: '{schema}'")
    click.echo(f"Output: '{output}'")

    generators: List[DataGenerator] = parse_schema(schema)

    for gen in generators:
        gen.write_to_target(output)


def print_test():
    """
    Simple test routine which creates a schema, generates a small CSV file, and prints it to stdout.
    """
    schema = """
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
    """

    with TemporaryDirectory() as d:
        schema_file = os.path.join(d, "schema.yml")
        out_file = os.path.join(d, "out.csv")

        with open(schema_file, "w") as f:
            f.write(schema.strip())

        generate_dataset.callback(schema_file, out_file)

        with open(out_file) as f:
            print("out.csv:")
            for line in f.readlines():
                print("  ", line.strip())
