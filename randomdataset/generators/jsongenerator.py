# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file

import json
from itertools import starmap
from typing import IO

from ..dataset import Dataset
from .generator import DataGenerator
from ..fields import FieldTypes

__all__ = ["JSONGenerator"]


class JSONGenerator(DataGenerator):
    def __init__(self, dataset: Dataset, num_lines: int, write_header: bool = True):
        super().__init__(dataset, num_lines, file_ext=".json")
        self.write_header: bool = write_header
        self.sep = ","

    def write_stream(self, stream: IO):
        field_types = self.dataset.field_types

        stream.write("{\n")
        if self.write_header:
            line = self.get_header()
            stream.write(f'    "header": {json.dumps(line)},\n')

        stream.write('    "data": [')
        end = "\n"
        for line in self.generate_rows():
            line_str = f"{end}        {json.dumps(line)}"
            stream.write(line_str)
            end = ",\n"

        stream.write("\n    ]\n}\n")
