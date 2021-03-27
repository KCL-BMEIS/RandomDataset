# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file


from enum import Enum
from typing import Optional, Tuple
import numpy as np

__all__ = [
    "FieldTypes", "FieldGen", "IntFieldGen", "FloatFieldGen", "StrFieldGen", "ASCIIFieldGen", "SetFieldGen",
    "BoolFieldGen"
]


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

        if rand_state is not None:
            self.R = rand_state

    def __call__(self, shape: OptShapeType = None):
        pass


class IntFieldGen(FieldGen):
    def __init__(self, name: str, vmin=0, vmax=100, rand_state: OptRandStateType = None):
        super().__init__(name, FieldTypes.INTEGER, rand_state)
        self.vmin = vmin
        self.vmax = vmax

    def __call__(self, shape: OptShapeType = None):
        return self.R.randint(self.vmin, self.vmax, shape)


class FloatFieldGen(FieldGen):
    def __init__(self, name: str, vmin=0, vmax=1.0, rand_state: OptRandStateType = None):
        super().__init__(name, FieldTypes.FLOAT, rand_state)
        self.vmin = vmin
        self.vmax = vmax

    def __call__(self, shape: OptShapeType = None):
        if shape is not None:
            rand = self.R.rand(*shape)
        else:
            rand = self.R.rand()

        return (rand * (self.vmax - self.vmin)) + self.vmin


class StrFieldGen(FieldGen):
    CHARS = list(range(ord("A"), ord("Z"))) + list(range(ord("a"), ord("z"))) + list(range(ord("0"), ord("9")))

    def __init__(self, name: str, lmin=5, lmax=10, rand_state: OptRandStateType = None):
        super().__init__(name, FieldTypes.STRING, rand_state)
        self.lmin = lmin
        self.lmax = lmax

    def __call__(self, shape: OptShapeType = None):
        length = self.R.randint(self.lmin, self.lmax)
        randinds = self.R.randint(0, len(self.CHARS), (length,))

        return "".join(chr(self.CHARS[i]) for i in randinds)


class ASCIIFieldGen(StrFieldGen):
    CHARS = list(range(128))


class SetFieldGen(FieldGen):
    def __init__(self, name: str, values: set, field_type: FieldTypes, rand_state: OptRandStateType = None):
        super().__init__(name, field_type, rand_state)
        self.values = tuple(values)

    def __call__(self, shape: OptShapeType = None):
        idx = self.R.randint(0, len(self.values))
        return self.values[idx]


class BoolFieldGen(FieldGen):
    def __init__(self, name: str, as_string=True, rand_state: OptRandStateType = None):
        super().__init__(name, FieldTypes.STRING if as_string else FieldTypes.BOOL, rand_state)
        self.as_string = as_string

    def __call__(self, shape: OptShapeType = None):
        result = self.R.randint(0, 2) == 1

        return str(result) if self.as_string else result
