# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file
"""
Parses the YAML schema used to define datasets. The schema must be a list of dictionary definitions where each defines
an object type to instantiate and its constructor keyword arguments. Dictionaries are interpreted as new objects in any
place they are used and other values as literals. The top level list must be for creating Dataset instances. Every
dictionary must have a `typename` member stating the fully-qualified name for the type to instantiate, and a `name`
argument to pass to the constructor. For example, to create a single dataset item with a few random fields:

Example:
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

from typing import Union, IO, List, Dict
from enum import Enum
from inspect import signature, Signature
import yaml

from .generators import DataGenerator
from .utils import find_type_def

__all__ = ["parse_schema", "ConstrSchemaFields", "parse_obj_constr"]

DATASET_ELEM = "dataset"


class ConstrSchemaFields(Enum):
    TYPENAME = "typename"
    NAME = "name"


def parse_obj_constr(schema_dict: Dict[str, Union[dict, list, tuple]]):
    """
    Parse and construct an object from the given schema dictionary. The field `ConstrSchemaFields.TYPENAME` must be in
    this dictionary, which is keyed to the fully-qualified name of the type to construct. Other fields become keyword
    arguments in the constructor call. The provided schema must have a key "name" containing the name of the object
    to create (which will be passed as a constructor argument of the same name), a key "typename" giving the fully
    qualified type name of the object to create, and then whatever other constructor arguments are to follow. For
    example, a class can be instantiated from the "__main__" module.

    Example:
        class CreateTest:
            def __init__(self, name, a, b):
                self.name = name
                self.a = a
                self.b = b

        create_dict = {"name": "test", "typename": "__main__.CreateTest", "a": 1, "b": "two"}
        test = randomdataset.schemaparser.parse_obj_constr(create_dict)
        print(test.name, test.a, test.b)  # prints "name 1 two"
    """

    if ConstrSchemaFields.TYPENAME.value not in schema_dict:
        raise ValueError("Schema must include 'typename' value")

    schema_dict = dict(schema_dict)  # shallow copy to allow pop

    typename = schema_dict.pop(ConstrSchemaFields.TYPENAME.value)
    typeconstr = find_type_def(typename)

    sig = signature(typeconstr)

    missing_params = [k for k, v in sig.parameters.items() if k not in schema_dict and v.default is Signature.empty]

    if missing_params:
        raise ValueError(f"Missing values for these parameters of type '{typename}': {', '.join(missing_params)}")

    args = {}

    for key, value in schema_dict.items():
        if isinstance(value, dict):
            arg = parse_obj_constr(value)
        elif isinstance(value, (list, tuple)):
            arg = tuple(parse_obj_constr(item) if isinstance(item, dict) else item for item in value)
        else:
            arg = value

        args[key] = arg

    return typeconstr(**args)


def parse_schema(stream_or_file: Union[str, IO]) -> List[DataGenerator]:
    """
    Parse the given file or stream and return the list of Dataset objects it specifies.
    """
    if isinstance(stream_or_file, str):
        with open(stream_or_file) as o:
            schema = yaml.safe_load(o)
    else:
        schema = yaml.safe_load(stream_or_file)

    objs = [parse_obj_constr(s) for s in schema]

    return objs
