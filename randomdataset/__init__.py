# RandomDataset
# Copyright (c) 2021 Eric Kerfoot, KCL, see LICENSE file

from .application import *
from .fields import *
from .dataset import Dataset
from .generators import *
from .schemaparser import *

__appname__ = "RandomDataset"
__version_info__ = (0, 1, 0)  # global application version, major/minor/patch
__version__ = "%i.%i.%i" % __version_info__
__author__ = "Eric Kerfoot, KCL"
__copyright__ = "Copyright (c) 2021 Eric Kerfoot, King's College London, all rights reserved. Licensed under MIT License (see LICENSE.txt)."
