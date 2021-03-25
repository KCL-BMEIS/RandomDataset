# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file


import unittest

from randomdataset import StrFieldGen, IntFieldGen


class TestStrFieldGen(unittest.TestCase):
    def test_str_basic(self):
        gen = StrFieldGen("test", 8, 9)

        s = gen()

        self.assertIsInstance(s, str)
        self.assertEqual(len(s), 8)

    def test_int_basic(self):
        gen = IntFieldGen("test", 0, 10)

        s = gen()

        self.assertIsInstance(s, int)
        self.assertTrue(0 <= s < 10)
