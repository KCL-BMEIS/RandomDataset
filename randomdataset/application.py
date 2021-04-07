# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file

import click
from .generators import DataGenerator
from .schemaparser import parse_schema
from .utils import find_type_def

__all__ = ["generate_dataset"]


@click.command()
@click.argument("schema", type=click.File('r', lazy=True))
@click.argument("output", type=click.Path(writable=True, resolve_path=True))
@click.option("-n", "num_lines", help="Number of lines to generate for each dataset", default=10, type=int,
              show_default=True)
@click.option("-g", "generator", help="Generator type name", default="randomdataset.generators.CSVGenerator", type=str,
              show_default=True)
def generate_dataset(schema, output, num_lines, generator):
    """
    This script generates a random dataset from a given YAML schema.
    """
    print(f"Schema: '{schema}'")
    print(f"Output: '{output}'")
    print(f"Generating {num_lines} lines with '{generator}'")

    datasets = parse_schema(schema)
    gen_type = find_type_def(generator)

    for ds in datasets:
        gen: DataGenerator = gen_type(dataset=ds, num_lines=num_lines)
        gen.write_to_target(output)
