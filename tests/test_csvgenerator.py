# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file

import sys
import unittest
import tempfile
from randomdataset import StrFieldGen, IntFieldGen, FloatFieldGen, Dataset, CSVGenerator


class TestCSVGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.fields = [
            StrFieldGen("Name", 6, 12),
            IntFieldGen("Age", 1, 90),
            IntFieldGen("Height", 50, 250),
            FloatFieldGen("BMI", 16, 32)
        ]

        self.ds = Dataset("Humans", self.fields)

    def test_write(self):
        gen = CSVGenerator(self.ds, 10)

        with tempfile.TemporaryFile("w") as o:
            gen.write_stream(o)
