# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file

import json
from itertools import islice, starmap
from typing import IO

from ..dataset import Dataset
from .generator import StreamDataGenerator
from ..fields import FieldTypes

__all__ = ["CSVGenerator"]


class CSVGenerator(StreamDataGenerator):
    def __init__(self, dataset: Dataset, num_lines: int, write_header: bool = True, check_file_exists: bool = True,
                 use_temp_dir: bool = True):
        super().__init__(dataset, check_file_exists, use_temp_dir)
        self.num_lines: int = num_lines
        self.write_header: bool = write_header
        self.sep = ", "

    def _format_value(self, value, ftype) -> str:
        if ftype == FieldTypes.STRING:
            return json.dumps(value)

        return str(value)

    def write_stream(self, stream: IO):
        def _get_line(line_values, line_types):
            line_values = starmap(self._format_value, zip(line_values, line_types))
            return self.sep.join(line_values)

        if self.write_header:
            line = self.dataset.field_names
            line = _get_line(line, [FieldTypes.STRING] * len(line))
            stream.write(line + "\n")

        field_types = self.dataset.field_types
        for line in islice(self.generate_rows(), self.num_lines):
            stream.write(_get_line(line, field_types) + "\n")
