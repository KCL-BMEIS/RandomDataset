# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file

import click
from .fields import StrFieldGen, IntFieldGen, FloatFieldGen
from .dataset import Dataset
from .generator import CSVGenerator

__all__ = ["simple_csv"]

field_template = {
    "name": StrFieldGen("Name", 6, 12),
    "age": IntFieldGen("Age", 1, 90),
    "height": IntFieldGen("Height", 50, 250),
    "bmi": FloatFieldGen("BMI", 16, 32)
}


@click.command()
@click.argument("output", type=click.File('w'))
@click.option("-f", "fields", multiple=True, nargs=1, type=str)
@click.option("-n", "num_lines", default=10, type=int)
def simple_csv(output, fields, num_lines):
    chosen = [field_template[f] for f in fields]
    ds = Dataset("ds", chosen)

    csv = CSVGenerator(ds, num_lines)

    csv.write_file(output)
