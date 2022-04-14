import pkg_resources
import pint

from .nodes import (
    User,
    Group,
    Reference,
    Citation,
    Collection,
    File,
    Data,
    Condition,
    Property,
    Identifier,
    Component,
    Material,
    Inventory,
    Quantity,
    Ingredient,
    Process,
    Experiment,
)
from .connect import API


__all__ = ["VERSION", "__version__", "__short_version__", "node_classes"]


# single-sourcing the package version
version_file = pkg_resources.resource_filename("cript", "VERSION.txt")
with open(version_file, "r") as fr:
    __version__ = fr.read().strip()

VERSION = __version__
__short_version__ = __version__.rpartition(".")[0]


# Instantiate the Pint registry.
# For context, check out https://pint.readthedocs.io/en/stable/tutorial.html#using-pint-in-your-projects.
pint_ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)

node_classes = [
    User,
    Group,
    Reference,
    Citation,
    Collection,
    File,
    Data,
    Condition,
    Property,
    Identifier,
    Component,
    Material,
    Inventory,
    Quantity,
    Ingredient,
    Process,
    Experiment,
]

