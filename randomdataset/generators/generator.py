# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file


from ..dataset import Dataset

from pathlib import Path
from typing import Union, IO, Any, Tuple

__all__ = ["DataGenerator", "StreamDataGenerator"]


class DataGenerator:
    def __init__(self, dataset: Dataset, num_lines: int):
        self.dataset = dataset
        self.num_lines = num_lines

    def generate_header(self) -> Tuple[str]:
        return self.dataset.field_names

    def generate_rows(self):
        while True:
            yield self.dataset.generate_row()

    def generate_fields(self, length: int):
        while True:
            fields = []
            for f in self.dataset.field_names:
                fields.append(self.dataset.generate_field(f, length))

            yield tuple(fields)

    def write_to_target(self, target: Any):
        pass


class StreamDataGenerator(DataGenerator):
    def __init__(self, dataset: Dataset, num_lines: int, file_mode: str = "w"):
        super().__init__(dataset, num_lines)
        self.file_mode = file_mode
        self.file_ext = ""

    def write_to_target(self, target: Any):
        if isinstance(target, str):
            path = Path(target)

            if path.is_dir():
                target_file = str(path / f"{self.dataset.name}{self.file_ext}")
                self.write_file(target_file)
            else:
                self.write_file(target)
        else:
            raise IOError(f"Unknown target type {type(target)}")

    def write_file(self, dest: Union[str, IO]):
        if isinstance(dest, str):
            with open(dest, self.file_mode) as o:
                self.write_stream(o)
        else:
            return self.write_stream(dest)

    def write_stream(self, stream: IO):
        pass
