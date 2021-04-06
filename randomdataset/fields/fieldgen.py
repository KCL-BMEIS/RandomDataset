# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file

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


OptShapeType = Optional[Tuple[int]]
OptRandStateType = Optional[np.random.RandomState]


class FieldGen:
    """
    Base class for generating field data. Inheriting classes will generate data corresponding to their `field_type`
    attribute, using the default random state `R` or the one passed through the constructor
    
    Args:
        name: name of the field
        field_type: type of data produced by the generator, or np.ndarray structures thereof
        rand_state: random state to generate data from
    """
    R: np.random.RandomState = np.random.RandomState()

    def __init__(self, name: str, field_type: FieldTypes, rand_state: OptRandStateType = None):
        self.name: str = name
        self.field_type: FieldTypes = field_type
        self._parent: Optional[Any] = None

        if rand_state is not None:
            self.R = rand_state

    def __call__(self, shape: OptShapeType = None):
        pass

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent
