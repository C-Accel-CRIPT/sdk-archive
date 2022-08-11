from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes.primary.group import Group
from cript.nodes.primary.collection import Collection
from cript.utils import auto_assign_group


logger = getLogger(__name__)


class Experiment(BasePrimary):
    """
    Object representing an experiment.
    """

    node_name = "Experiment"
    slug = "experiment"
    list_name = "experiments"
    unique_together = ["collection", "name"]

    @beartype
    def __init__(
        self,
        collection: Union[Collection, str],
        name: str,
        processes=None,
        data=None,
        funding: list[Union[str, None]] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        group: Union[Group, str] = None,
    ):
        super().__init__(public=public)
        self.collection = collection
        self.name = name
        self.funding = funding if funding else []
        self.processes = processes if processes else []
        self.data = data if data else []
        self.notes = notes
        self.group = auto_assign_group(group, collection)
