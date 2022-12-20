# trunk-ignore-all(flake8/F401)
# trunk-ignore-all(flake8/E402)

import importlib.metadata
import logging

import pint

# Set the default logging level for the package
logging.basicConfig(level=logging.WARNING)
logging.captureWarnings(True)
pint.util.logger.setLevel(logging.ERROR)  # Mute Pint warnings


# Single-sourcing the package version
__version__ = importlib.metadata.version("cript")
__short_version__ = __version__.rpartition(".")[0]

__api_version__ = "0.6.0"

# Instantiate the Pint unit registry
# https://pint.readthedocs.io/en/stable/tutorial.html#using-pint-in-your-projects
# Note that this needs to be before the data model imports below
pint_ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)


from cript.data_model import Collection  # noqa 402
from cript.data_model import (
    Algorithm,
    Citation,
    Computation,
    ComputationalForcefield,
    ComputationalProcess,
    Condition,
    Data,
    Equipment,
    Experiment,
    File,
    Group,
    Identifier,
    Ingredient,
    Inventory,
    Material,
    Parameter,
    Process,
    Project,
    Property,
    Quantity,
    Reference,
    Software,
    SoftwareConfiguration,
    User,
)
from cript.data_model.paginator import Paginator

DATA_MODEL_CLASSES = [
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

DATA_MODEL_NAMES: list[str] = [node.node_name.lower() for node in DATA_MODEL_CLASSES]

from cript.api.local import APILocal
from cript.api.rest import API  # noqa 401 402
