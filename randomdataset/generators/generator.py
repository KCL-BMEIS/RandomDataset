# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file


from ..dataset import Dataset

from pathlib import Path
from typing import Union, IO, Any, Tuple

__all__ = ["DataGenerator"]


class DataGenerator:
    def __init__(
        self, dataset: Dataset, num_lines: int, file_mode: str = "w", file_ext: str = ""
    ):
        self.dataset = dataset
        self.num_lines = num_lines
        self.file_mode = file_mode
        self.file_ext = file_ext

    def get_header(self) -> Tuple[str]:
        """Return the header for a table, default is the tuple of field names."""
        return tuple(self.dataset.field_names)

    def generate_rows(self):
        """Yields `self.num_lines` of rows from the dataset."""
        for _ in range(self.num_lines):
            yield self.dataset.get_row_data()

    def generate_fields(self, length: int):
        """Yields an of data `length` long from each field in the dataset."""
        for f in self.dataset.field_names:
            yield self.dataset.get_field_data(f, length)

    def write_to_target(self, target: Any):
        """
        Write a dataset to the given target, which can be a string path to a file or directory, or some other object
        type expected by the override of this method in a subclass.
        """
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
        """Write a dataset to the given file path or file-like object."""
        if isinstance(dest, str):
            with open(dest, self.file_mode) as o:
                self.write_stream(o)
        else:
            return self.write_stream(dest)

    def write_stream(self, stream: IO):
        """Write a dataset to the given file-like object."""
        pass
