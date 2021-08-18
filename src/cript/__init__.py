import pkg_resources

__all__ = [
    "VERSION", "__version__", "__short_version__", "Unit", "load", "CriptDB",
    "User", "Group", "Collection", "Publication", "Experiment", "Material", "Process", "Data",
    "Inventory", "Simulation", "Cond", "Prop", "Qty", "Ingr"
]


# single-sourcing the package version
__version__ = pkg_resources.require("cript")[0].version

VERSION = __version__
__short_version__ = __version__.rpartition(".")[0]


# Units
import pint
u = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)
Unit = u.Unit
Quantity = u.Quantity


class CRIPTError(Exception):

    def __init__(self, message):
        self.message = message


class CRIPTWarning(Warning):

    def __init__(self, message):
        self.message = message


# Core CRIPT objects (order important)
from .base import *
from .cond import *
from .prop import *
from .user import *
from .group import *
from .publication import *
from .collection import *
from .data import *
from .experiment import *
from .inventory import *
from .material import *
from .process import *
from .simulation import *
from .database import *

# Get CRIPT types in a dict
from inspect import getmembers, isclass
cript_types = {pair[0]: pair[1] for pair in getmembers(sys.modules[__name__], isclass) if "cript." in str(pair[1])}
cript_types["Unit"] = Unit
cript_types["Quantity"] = Quantity
cript_types_tuple = tuple(cript_types.values())


Cond._init_()
Prop._init_()


