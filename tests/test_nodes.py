"""Unit tests for CRIPT nodes."""

"""
Notes:
All old style classes -> new style classes
Split up classes into different modules?
Logging module
"""

from cript.nodes import Base
from cript.nodes import User
from cript.nodes import Group
from cript.nodes import Reference
from cript.nodes import Citation
from cript.nodes import Collection
from cript.nodes import Experiment
from cript.nodes import Data
from cript.nodes import File
from cript.nodes import Condition
from cript.nodes import Property
from cript.nodes import Identifier
from cript.nodes import Quantity
from cript.nodes import Component
from cript.nodes import Material
from cript.nodes import Inventory
from cript.nodes import Ingredient
from cript.nodes import Process


def test_base_as_dict():
    pass


def test_base_to_json():
    pass


def test_base_prep_for_upload():
    pass


def test_base_add_node():
    pass


def test_base_remove_node():
    pass


def test_user_init():
    pass


def test_group_init():
    pass


def test_group_add_user():
    pass


def test_group_remove_user():
    pass


def test_reference_init():
    pass


def test_citation_init():
    pass


def test_collection_init():
    pass


def test_collection_add_citation():
    pass


def test_collection_remove_citation():
    pass


def test_experiment_init():
    pass


def test_data_init():
    pass


def test_data_add_citation():
    pass


def test_data_remove_citation():
    pass
