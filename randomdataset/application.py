# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file

import click

from .__init__ import __version__
from .generators import DataGenerator
from .schemaparser import parse_schema
from .utils import find_type_def

__all__ = ["generate_dataset"]


@click.command("generate_dataset")
@click.argument("schema", type=click.File('r', lazy=True))
@click.argument("output", type=click.Path(writable=True, resolve_path=True))
@click.version_option(__version__, message="%(version)s")
def generate_dataset(schema, output):
    """
    This script generates a random dataset from a given YAML schema.
    """
    print(f"Schema: '{schema}'")
    print(f"Output: '{output}'")

    generators = parse_schema(schema)
    
    for gen in generators:
        gen.write_to_target(output)
