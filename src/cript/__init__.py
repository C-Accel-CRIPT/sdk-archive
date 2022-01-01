import pkg_resources

__all__ = [
     "Unit", "load", "export", "CriptDB", "User", "Group", "Collection", "Publication", "Experiment",
     "Material", "Process", "Data", "Inventory", "Simulation", "Cond", "Prop", "Ingr", "Iden", "Path", "File"
]

# single-sourcing the package version
__version__ = pkg_resources.require("cript")[0].version
VERSION = 1
__short_version__ = __version__.rpartition(".")[0]


# Units
import pint
u = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)
Unit = u.Unit
Quantity = u.Quantity

# General Limits
float_limit = 1.79E308  # max of float64 can represent
str_limit = 500
degC_lower_limit = -273.15


class CRIPTError(Exception):

    def __init__(self, message):
        self.message = message


class CRIPTWarning(Warning):

    def __init__(self, message):
        self.message = message


# Core CRIPT objects (order important)
from .load_export import load, export
from .cond import Cond
from .prop import Prop
from .user import User
from .group import Group
from .publication import Publication
from .collection import Collection
from .experiment import Experiment
from .inventory import Inventory
from .data import Data, File
from .material import Iden, Material, __Iden
from .process import Ingr, Process
from .simulation import Simulation
from .database import CriptDB

# Get CRIPT types in a dict
from inspect import getmembers, isclass
import sys
cript_types = {pair[0]: pair[1] for pair in getmembers(sys.modules[__name__], isclass) if "cript." in str(pair[1])}
cript_types["Unit"] = Unit
cript_types["Quantity"] = Quantity
from pathlib import Path
cript_types["Path"] = Path

# Initialize CRIPT Types
for node in cript_types.values():
    if hasattr(node, "_init_"):
        node._init_()
