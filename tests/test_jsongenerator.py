# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file

import unittest
import io
import json
from randomdataset import (
    StrFieldGen,
    IntFieldGen,
    Dataset,
    JSONGenerator,
)


class TestJSONGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.fields = [
            StrFieldGen("Name", 6, 12),
            IntFieldGen("Age", 1, 90),
            IntFieldGen("Height", 50, 250),
        ]

        self.ds = Dataset("Humans", self.fields)
        self.temp=io.StringIO()

    def _write_temp(self, gen):
        gen.write_stream(self.temp)
        return json.loads(self.temp.getvalue())

    def test_write(self):
        gen = JSONGenerator(self.ds, 10)
        data = self._write_temp(gen)

        self.assertGreater(self.temp.tell(), 0)

        self.assertSetEqual({"header", "data"}, set(data.keys()))

        self.assertEqual(len(data["data"]), 10)
        self.assertEqual(len(data["data"][0]), 3)

    def test_write_empty(self):
        gen = JSONGenerator(self.ds, 0)
        data = self._write_temp(gen)

        self.assertSetEqual({"header", "data"}, set(data.keys()))

        self.assertEqual(len(data["data"]), 0)

    def test_write_no_header(self):
        gen = JSONGenerator(self.ds, 10, False)
        data = self._write_temp(gen)

        self.assertSetEqual({"data"}, set(data.keys()))

        self.assertEqual(len(data["data"]), 10)
        self.assertEqual(len(data["data"][0]), 3)
