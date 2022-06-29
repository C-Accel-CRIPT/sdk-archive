from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes.primary.group import Group
from cript.nodes.primary.collection import Collection
from cript.validators import validate_required
from cript.utils import auto_assign_group


logger = getLogger(__name__)


class Experiment(BasePrimary):
    """
    Object representing an experiment.
    """

    node_name = "Experiment"
    slug = "experiment"
    list_name = "experiments"
    required = ["group", "collection", "name"]
    unique_together = ["collection", "name"]

    @beartype
    def __init__(
        self,
        group: Union[Group, str] = None,
        collection: Union[Collection, str] = None,
        name: str = None,
        processes=None,
        data=None,
        funding: list[Union[str, None]] = None,
        notes: Union[str, None] = None,
        public: bool = False,
    ):
        super().__init__()
        self.url = None
        self.uid = None
        self.group = auto_assign_group(group, collection)
        self.collection = collection
        self.name = name
        self.funding = funding if funding else []
        self.notes = notes
        self.notes = notes
        self.processes = processes if processes else []
        self.data = data if data else []
        self.public = public
        self.created_at = None
        self.updated_at = None
        validate_required(self)
