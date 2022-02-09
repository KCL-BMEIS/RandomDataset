# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file

from abc import abstractmethod, ABC
from enum import Enum
from typing import Optional, Tuple, Any
import numpy as np

__all__ = ["FieldTypes", "FieldGen", "OptRandStateType", "OptShapeType"]


class FieldTypes(Enum):
    """Data types produced by FieldGen objects."""
    STRING = str
    INTEGER = int
    FLOAT = float
    BOOL = bool


OptShapeType = Optional[Tuple[int, ...]]
OptRandStateType = Optional[np.random.RandomState]


class FieldGen(ABC):
    """
    Base class for generating field data. Inheriting classes will generate data corresponding to their `field_type`
    attribute, using the default random state `R` or the one passed through the constructor
    
    Args:
        name: name of the field
        field_type: type of data produced by the generator, or np.ndarray structures thereof
        rand_state: random state to generate data from
        shared_state_name: if provided, data is stored in the dataset when generated for sharing with other fields
    """
    R: np.random.RandomState = np.random.RandomState()
    
    def __init__(self, name: str, field_type: FieldTypes, rand_state: OptRandStateType = None, shared_state_name=None):
        self.name: str = name
        self.field_type: FieldTypes = field_type
        self._parent: Optional[Any] = None
        self._shared_state_name = shared_state_name

        if rand_state is not None:
            self.R = rand_state

    def __call__(self, shape: OptShapeType = None):
        data=self.generate(shape)
        self.append_shared_state(data)
        return data
    
    @abstractmethod
    def generate(self, shape: OptShapeType = None):
        """Called by __call__, generate a single datum if `shape` is None, otherwise array of data with that shape."""

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent
        
    @property
    def shared_state_name(self):
        return _shared_state_name
    
    def append_shared_state(self, data):
        if self._parent is not None and self._shared_state_name is not None:
            self._parent.append_shared_state(self._shared_state_name, data)
