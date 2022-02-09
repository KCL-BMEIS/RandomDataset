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


class FlatIterator:
    def __init__(self,data):
        self.data=data
        self.indices=[]
        
        for i, item in enumerate(data):
            if isinstance(item,(list,tuple)):
                self.indices+=[(i,j) for j in range(len(item))]
            else:
                self.indices.append((i,None))
                
    def __len__(self):
        return len(self.indices)
    
    def __getitem__(self, item):
        idx,subidx = self.indices[item]
        if subidx is None:
            return self.data[idx]
        else:
            return self.data[idx][subidx]
                
    def __iter__(self):
        yield from (self[i] for i in range(len(self)))
                