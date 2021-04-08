# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file


from typing import Iterable, Optional, Tuple
from .fields import FieldGen, FieldTypes


class Dataset:
    def __init__(self, name: str, fields: Iterable[FieldGen]):
        self.name = name
        self._fields = tuple(fields)

        for f in self._fields:
            f.parent = self

    @property
    def fields(self) -> Iterable[FieldGen]:
        return tuple(self._fields)

    @property
    def field_names(self) -> Tuple[str]:
        return tuple(f.name for f in self._fields)

    @property
    def field_types(self) -> Tuple[FieldTypes]:
        return tuple(f.field_type for f in self._fields)

    def has_field(self, name: str) -> bool:
        for f in self._fields:
            if f.name == name:
                return True

        return False

    def get_field(self, name: str) -> FieldGen:
        for f in self._fields:
            if f.name == name:
                return f

        raise ValueError(f"Field '{name}' not found")

    def generate_row(self):
        return tuple(f() for f in self._fields)

    def generate_field(self, name: str, length: Optional[int] = None):
        field = self.get_field(name)
        return field((length,)) if length is not None else field()

    def __repr__(self):
        return f"Dataset({self.name}, Fields: {[f.name for f in self.fields]})"
