# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file

import os
from tempfile import TemporaryDirectory
from io import StringIO
from contextlib import redirect_stdout

import unittest

from randomdataset import generate_dataset, print_csv_test

schema = """
- typename: randomdataset.generators.CSVGenerator
  num_lines: 10
  dataset:
    name: customers
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


class TestApplication(unittest.TestCase):
    def test_generate_dataset(self):
        with TemporaryDirectory() as d:
            schema_file = os.path.join(d, "schema.yml")
            out_file = os.path.join(d, "out.csv")

            with open(schema_file, "w") as o:
                o.write(schema)

            tmp_out = StringIO()
            with redirect_stdout(tmp_out):
                generate_dataset.callback(schema_file, out_file)

            self.assertTrue(os.path.isfile(out_file))
            self.assertGreater(tmp_out.tell(), 0)

    def test_print_test(self):
        tmp_out = StringIO()
        with redirect_stdout(tmp_out):
            print_csv_test()

        self.assertGreater(tmp_out.tell(), 0)
