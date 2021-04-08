# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file

import datetime
from typing import Optional

import numpy as np

from .fieldgen import FieldGen, FieldTypes, OptShapeType, OptRandStateType

__all__ = [
    "IntFieldGen", "FloatFieldGen", "StrFieldGen", "ASCIIFieldGen", "SetFieldGen", "BoolFieldGen", "DateTimeFieldGen",
    "UIDFieldGen"
]


class IntFieldGen(FieldGen):
    def __init__(self, name: str, vmin: int = 0, vmax: int = 100, rand_state: OptRandStateType = None):
        super().__init__(name, FieldTypes.INTEGER, rand_state)
        self.vmin: int = vmin
        self.vmax: int = vmax

    def __call__(self, shape: OptShapeType = None):
        return self.R.randint(self.vmin, self.vmax, shape)


class UIDFieldGen(FieldGen):
    def __init__(self, name: str, start_value: int = 0, rand_state: OptRandStateType = None):
        super().__init__(name, FieldTypes.INTEGER, rand_state)
        self.value = start_value

    def __call__(self, shape: OptShapeType = None):
        if shape is None:
            self.value += 1
            return self.value - 1
        else:
            values = np.arange(self.value, self.value + np.product(*shape))
            self.value = values[-1]
            return values.reshape(shape)


class FloatFieldGen(FieldGen):
    def __init__(self, name: str, vmin: float = 0, vmax: float = 1.0, rand_state: OptRandStateType = None):
        super().__init__(name, FieldTypes.FLOAT, rand_state)
        self.vmin: float = vmin
        self.vmax: float = vmax

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
    def __init__(self, name: str, as_string=False, rand_state: OptRandStateType = None):
        super().__init__(name, FieldTypes.STRING if as_string else FieldTypes.BOOL, rand_state)
        self.as_string = as_string

    def __call__(self, shape: OptShapeType = None):
        result = self.R.randint(0, 2) == 1

        return str(result) if self.as_string else result


class DateTimeFieldGen(FieldGen):
    def __init__(self, name: str, start_time: Optional[float] = None, end_time: Optional[float] = None,
                 as_string: bool = False, rand_state: OptRandStateType = None, ftimeformat: Optional[str] = None):
        super().__init__(name, FieldTypes.STRING if as_string else FieldTypes.BOOL, rand_state)
        self.as_string = as_string
        self.ftimeformat = ftimeformat

        if start_time is None:
            self.start_time = (datetime.datetime.now() - datetime.timedelta(days=365)).timestamp()
        else:
            self.start_time = start_time

        if end_time is None:
            self.end_time = datetime.datetime.now().timestamp()
        else:
            self.end_time = end_time

    def _format(self, timestamp):
        dt = datetime.datetime.fromtimestamp(timestamp)

        if self.ftimeformat is not None:
            return dt.strftime(self.ftimeformat)
        else:
            return str(dt)

    def __call__(self, shape: OptShapeType = None):
        rand_val = self.R.rand() if shape is None else self.R.rand(*shape)
        rand_time = rand_val * (self.end_time - self.start_time) + self.start_time

        if self.as_string:
            if shape is None:
                return self._format(rand_time)
            else:
                return list(map(self._format, rand_time))
        else:
            return rand_time
