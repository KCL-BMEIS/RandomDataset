# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file
"""
Parses the YAML schema used to define datasets. The schema must be a list of dictionary definitions where each defines
an object type to instantiate and its constructor keyword arguments. Dictionaries are interpreted as new objects in any
place they are used and other values as literals. The top level list must be for creating Dataset instances. Every
dictionary must have a `typename` member stating the fully-qualified name for the type to instantiate, and a `name`
argument to pass to the constructor. For example, to create a single dataset item with a few random fields:

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

from typing import Union, IO, List
from enum import Enum
import yaml

from .dataset import Dataset
from .utils import find_type_def

__all__ = ["parse_schema","ConstrSchemaFields"]

DATASET_ELEM = "dataset"


class ConstrSchemaFields(Enum):
    TYPENAME = "typename"
    NAME = "name"


def parse_obj_constr(schema_dict):
    for f in ConstrSchemaFields:
        if f.value not in schema_dict:
            raise ValueError(f"Field `{f.value}` missing from schema, keys are {list(schema_dict)}")

    schema_dict = dict(schema_dict)  # shallow copy to allow pop

    typename = schema_dict.pop(ConstrSchemaFields.TYPENAME.value)
    name = schema_dict.pop(ConstrSchemaFields.NAME.value)

    typeconstr = find_type_def(typename)

    args = {}

    for key, value in schema_dict.items():
        if isinstance(value, dict):
            arg = parse_obj_constr(value)
        elif isinstance(value, (list, tuple)):
            arg = tuple(parse_obj_constr(item) if isinstance(item, dict) else item for item in value)
        else:
            arg = value

        args[key] = arg

    return typeconstr(name=name, **args)


def parse_schema(stream_or_file: Union[str, IO]) -> List[Dataset]:
    """
    Parse the given file or stream and return the list of Dataset objects it specifies.
    """
    if isinstance(stream_or_file, str):
        with open(stream_or_file) as o:
            schema = yaml.safe_load(o)
    else:
        schema = yaml.safe_load(stream_or_file)

    if not isinstance(schema, list):
        raise ValueError("Schema should be a list of `dataset` definitions")

    datasets = [parse_obj_constr(s) for s in schema]

    if not all(isinstance(d, Dataset) for d in datasets):
        raise ValueError("Schema should be a list of `dataset` definitions")

    return datasets
