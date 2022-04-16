import pkg_resources
import pint


# Instantiate the Pint unit registry
# https://pint.readthedocs.io/en/stable/tutorial.html#using-pint-in-your-projects
# Note that this needs to be before the node imports below
pint_ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)


from cript.nodes import (  # noqa 402
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

NODE_CLASSES = [
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

from cript.session import API  # noqa 401 402


# single-sourcing the package version
version_file = pkg_resources.resource_filename("cript", "VERSION.txt")
with open(version_file, "r") as fr:
    __version__ = fr.read().strip()

VERSION = __version__
__short_version__ = __version__.rpartition(".")[0]
