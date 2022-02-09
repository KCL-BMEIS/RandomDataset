# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file


from collections import defaultdict
from typing import Iterable, Optional, Tuple, Any, List, Mapping
from .fields import FieldGen, FieldTypes


class Dataset:
    _shared_state: Mapping[str, List[Any]] = defaultdict(list)
    
    def __init__(self, name: str, fields: Iterable[FieldGen]):
        self.name: str = name
        self._fields: Tuple[FieldGen] = tuple(fields)
        
        for f in self._fields:
            f.parent = self

    @property
    def fields(self) -> Iterable[FieldGen]:
        """Returns a tuple of the stored `FieldGen` objects."""
        return tuple(self._fields)

    @property
    def field_names(self) -> Tuple[str]:
        """Get a tuple of names of the stored fields."""
        return tuple(f.name for f in self._fields)

    @property
    def field_types(self) -> Tuple[FieldTypes]:
        """Get a tuple of types of the stored fields."""
        return tuple(f.field_type for f in self._fields)

    def has_field(self, name: str) -> bool:
        """Returns True if a field with given name is storede here."""
        for f in self._fields:
            if f.name == name:
                return True

        return False

    def get_field(self, name: str) -> FieldGen:
        """Get the field of the given name, raising ValueError if not found."""
        for f in self._fields:
            if f.name == name:
                return f

        raise ValueError(f"Field '{name}' not found")

    def get_row_data(self) -> Tuple[Any]:
        """Get the data for a row, that is one value from each field."""
        return tuple(f() for f in self._fields)

    def get_field_data(self, name: str, length: Optional[int] = None) -> Any:
        """Get a value, array of values if `length` provided, from the named field."""
        field = self.get_field(name)

        if length is not None:
            return field((length,))
        else:
            return field()
        
    def get_shared_state(self, state_name):
        """Get the shared state mapped to `state_name`, raising exception if key not present."""
        if state_name not in self._shared_state:
            raise ValueError(f"Key {state_name} not found in shared state")
            
        return self._shared_state[state_name]
    
    def append_shared_state(self, state_name:str, data:Any):
        """Append `data` to the list mapped to `state_name`, adding the new list if not present."""
        self._shared_state[state_name].append(data)

    def __repr__(self):
        return f"Dataset({self.name}, Fields: {[f.name for f in self.fields]})"
