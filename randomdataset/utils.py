# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file

__all__ = ["find_type_def"]


def find_type_def(qualified_name: str):
    if "." not in qualified_name:
        modname, defname = "builtins", qualified_name
    else:
        modname, defname = qualified_name.rsplit(".", 1)

    mod = __import__(modname)
    return getattr(mod, defname)
