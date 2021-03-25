# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file


import unittest
import numpy as np
from randomdataset import StrFieldGen, IntFieldGen, Dataset


class TestDataset(unittest.TestCase):
    def test_row_basic(self):
        field = StrFieldGen("field", 8, 9)
        ds = Dataset("TestDS", [field])

        row = ds.generate_row()

        self.assertEqual(len(row), 1)
        self.assertIsInstance(row, tuple)
        self.assertIsInstance(row[0], str)

    def test_row_two_fields(self):
        field1 = StrFieldGen("field1", 8, 9)
        field2 = IntFieldGen("field2", 0, 10)
        ds = Dataset("TestDS", [field1, field2])

        row = ds.generate_row()

        self.assertEqual(len(row), 2)
        self.assertIsInstance(row, tuple)
        self.assertIsInstance(row[0], str)
        self.assertIsInstance(row[1], int)

    def test_field_basic(self):
        field = IntFieldGen("field", 0, 10)
        ds = Dataset("TestDS", [field])

        col = ds.generate_field("field", 10)

        self.assertEqual(len(col), 10)
        self.assertIsInstance(col, np.ndarray)
