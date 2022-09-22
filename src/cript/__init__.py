import logging
import importlib.metadata

import pint


# Set the default logging level for the package
logging.basicConfig(level=logging.WARNING)
logging.captureWarnings(True)
pint.util.logger.setLevel(logging.ERROR)  # Mute Pint warnings


# Single-sourcing the package version
__version__ = importlib.metadata.version("cript")
__short_version__ = __version__.rpartition(".")[0]


# Instantiate the Pint unit registry
# https://pint.readthedocs.io/en/stable/tutorial.html#using-pint-in-your-projects
# Note that this needs to be before the node imports below
pint_ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)


from cript import exceptions  # noqa 401 402
from cript.nodes import (  # noqa 402
    User,
    Group,
    Project,
    Reference,
    Citation,
    Collection,
    File,
    Data,
    Condition,
    SoftwareConfiguration,
    Computation,
    Property,
    Identifier,
    Material,
    Inventory,
    Quantity,
    Ingredient,
    Equipment,
    Process,
    Experiment,
    Software,
    Parameter,
    Algorithm,
    ComputationalProcess,
    ComputationalForcefield,
)

NODE_CLASSES = [
    User,
    Group,
    Project,
    Reference,
    Citation,
    Collection,
    File,
    Data,
    Condition,
    SoftwareConfiguration,
    Computation,
    Property,
    Identifier,
    Material,
    Inventory,
    Quantity,
    Ingredient,
    Equipment,
    Process,
    Experiment,
    Software,
    Parameter,
    Algorithm,
    ComputationalProcess,
    ComputationalForcefield,
]

from cript.api import API  # noqa 401 402
