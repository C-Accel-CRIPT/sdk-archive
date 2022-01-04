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
U = Unit = u.Unit
Q = Quantity = u.Quantity

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
from .secondary_nodes.load import load
from .secondary_nodes.export import export
from .secondary_nodes.cond import Cond
from .secondary_nodes.prop import Prop
from .primary_nodes.user import User
from .primary_nodes.group import Group
from .primary_nodes.publication import Publication
from .primary_nodes.collection import Collection
from .primary_nodes.experiment import Experiment
from .primary_nodes.inventory import Inventory
from .secondary_nodes.hazard import Hazard
from .secondary_nodes.spec import Spec
from .secondary_nodes.iden import Iden
from .primary_nodes.material import Material
from .secondary_nodes.ingr import Ingr
from .primary_nodes.process import Process
from .primary_nodes.simulation import Simulation
from .secondary_nodes.file import File
from .primary_nodes.data import Data
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
