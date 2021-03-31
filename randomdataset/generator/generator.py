# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file


from ..dataset import Dataset

import shutil
from pathlib import Path
from typing import Union, IO, Any, Tuple
from tempfile import TemporaryDirectory

__all__ = ["DataGenerator", "StreamDataGenerator"]


class DataGenerator:
    def __init__(self, dataset: Dataset):
        self.dataset = dataset

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
    def __init__(self, dataset: Dataset, check_file_exists: bool = True, use_temp_dir: bool = True):
        super().__init__(dataset)
        self.check_file_exists = check_file_exists
        self.use_temp_dir = use_temp_dir
        self.file_mode = "w"

    def write_to_target(self, target: Any):
        if isinstance(target, str):
            self.write_file(target)

        raise IOError(f"Unknown target type {type(target)}")

    def write_file(self, dest: Union[str, IO]):
        if isinstance(dest, str):
            path = Path(dest).absolute()

            if not path.parent.exists():
                raise IOError(f"Base directory of {path} does not exist")

            if self.check_file_exists and path.exists():
                raise IOError(f"File {path} already exists")

            if self.use_temp_dir:
                with TemporaryDirectory() as tempdir:
                    tempfile = tempdir / path
                    with open(str(tempfile), self.file_mode) as o:
                        self.write_stream(o)

                    shutil.move(str(tempfile), str(path))
            else:
                with open(str(path), self.file_mode) as o:
                    self.write_stream(o)
        else:
            return self.write_stream(dest)

    def write_stream(self, stream: IO):
        pass
