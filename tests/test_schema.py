# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file

import os
from io import StringIO
import unittest
import tempfile

from randomdataset import parse_schema, Dataset, FieldGen

ex1 = """
- name: testset
  typename: randomdataset.Dataset
  fields: []
"""

ex2 = """
- name: testset
  typename: randomdataset.Dataset
  fields:
  - name: Name
    typename: randomdataset.StrFieldGen
    lmin: 6
    lmax: 14
  - name: Age
    typename: randomdataset.IntFieldGen
    vmin: 18
    vmax: 90
  - name: is_employed
    typename: randomdataset.BoolFieldGen  
"""


ex3 = """
- name: testset
  typename: randomdataset.Dataset
"""

class TestSchema(unittest.TestCase):
    def test_simple_schema(self):
        s = StringIO(ex1)
        s.seek(0)

        ds = parse_schema(s)

        self.assertIsInstance(ds, list)
        self.assertEqual(len(ds), 1)
        self.assertIsInstance(ds[0], Dataset)

    def test_simple_schema_file(self):
        with tempfile.TemporaryDirectory() as t:
            filename = os.path.join(t, 'schema.yaml')

            with open(filename, "w") as o:
                o.write(ex1)

            ds = parse_schema(filename)

        self.assertIsInstance(ds, list)
        self.assertEqual(len(ds), 1)
        self.assertIsInstance(ds[0], Dataset)

    def test_field_gen(self):
        s = StringIO(ex2)
        s.seek(0)

        ds = parse_schema(s)
        ds0 = ds[0]

        self.assertEqual(len(ds0.fields), 3)

        for f in ds0.fields:
            self.assertTrue(isinstance(f, FieldGen), f"{f} not FieldGen")
            
    def test_missing_param(self):
        s = StringIO(ex3)
        s.seek(0)

        with self.assertRaises(ValueError):
            ds = parse_schema(s)
