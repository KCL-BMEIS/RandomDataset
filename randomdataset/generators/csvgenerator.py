# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file

import json
from itertools import islice, starmap
from typing import IO

from ..dataset import Dataset
from .generator import DataGenerator
from ..fields import FieldTypes

__all__ = ["CSVGenerator"]


class CSVGenerator(DataGenerator):
    def __init__(self, dataset: Dataset, num_lines: int, write_header: bool = True):
        super().__init__(dataset, num_lines, file_ext=".csv")
        self.write_header: bool = write_header
        self.sep = ","

    def _format_value(self, value, ftype) -> str:
        if ftype == FieldTypes.STRING:
            return json.dumps(value)

        return str(value)

    def write_stream(self, stream: IO):
        field_types = self.dataset.field_types

        if self.write_header:
            line = self.get_header()
            line = self.sep.join(line)
            stream.write(line + "\n")

        for line in self.generate_rows():
            line_values = starmap(self._format_value, zip(line, field_types))
            line_values = self.sep.join(line_values)
            stream.write(line_values + "\n")
