from logging import getLogger
from typing import Union

from beartype import beartype

from cript.cache import get_cached_api_session
from cript.data_model.exceptions import UniqueNodeError
from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.group import Group
from cript.data_model.utils import set_node_attributes

logger = getLogger(__name__)


class Reference(BaseNode):
    """The <a href="../reference" target="_blank">`Reference`</a>
    object represents a bibliographic resource, such as a journal article,
    operating manual, encyclopedia, or handbook.

    Args:
        group (Union[Group, str]): `Group` object that manages the reference
        title (str): Reference title
        doi (Union[str, None], optional): Reference digital object identifier (DOI)
        authors (Union[list[str], None], optional): List of reference authors
        journal (Union[str, None], optional): Journal name (if applicable)
        publisher (Union[str, None], optional): Publisher name (if applicable)
        year (Union[int, None], optional): Publication year
        volume (Union[int, None], optional): Publication volume (if applicable)
        issue (Union[int, None], optional): Publication issue (if applicable)
        pages (Union[list[int], None], optional): Relevant pages (if applicable)
        issn (Union[str, None], optional): International standard serial number (ISSN)
        arxiv_id (Union[str, None], optional): ArXiv ID (if applicable)
        pmid (Union[int, None], optional): PubMed ID (if applicable)
        website (Union[str, None], optional): Reference website (if applicable)
        notes (Union[str, None], optional): Reference notes
        public (bool, optional): _description_. Whether the reference is publicly viewable

    !!! warning "Saving references is permanent"
        Once created, a <a href="../reference" target="_blank">`Reference`</a> object becomes locked
        and cannot be edited or deleted. This allows others to link to it using a
        <a href="/../subobjects/citation" target="_blank">`Citation`</a> object. 

    !!! success "Use <a href='../base_node' target='_blank'>`BaseNode`</a> methods to manipulate this object"
        Since this object inherits from the <a href="../base_node" target="_blank">`BaseNode`</a> object,
        all the <a href="../base_node" target="_blank">`BaseNode`</a> object methods can be used to manipulate it.
        These include `get()`, `create()`, `delete()`, `save()`, `search()`, `update()`, and `refresh()` methods.
        See the <a href="../base_node" target="_blank">`BaseNode`</a> documentation to learn more about these methods
        and see examples of their use.

    ``` py title="Example"
    # get an existing group
    my_group = Group.get(name="My group")

    # create a new reference in the existing group
    my_ref = Reference.create(
        group=my_group,
        title="Lange's handbook of chemistry",
        authors=["James G. Speight"],
        publisher="McGraw-Hill Education",
        year=2017,
        notes="Used for tabulating dfensities of solvent solutions",
    )
    ```

    ``` json title="Example of a `Reference` object in JSON format"
    {
        "url": "https://criptapp.org/api/reference/9ce2a749-9909-4ccd-95c6-25e6e2c02eae/",
        "uid": "9ce2a749-9909-4ccd-95c6-25e6e2c02eae",
        "group": "https://criptapp.org/api/group/04726d53-e734-4c7b-9cc5-d92bcbde15ca/",
        "title": "Interaction of plastics in mixed-plastics pyrolysis",
        "authors": [
            "Paul T. Williams",
            "Elizabeth A. Williams"
        ],
        "journal": "Energy & Fuels",
        "publisher": null,
        "year": 1999,
        "volume": 13,
        "issue": null,
        "pages": [
            188,
            196
        ],
        "doi": "10.1021/ef980163x",
        "issn": null,
        "arxiv_id": null,
        "pmid": null,
        "website": null,
        "notes": null,
        "public": true,
        "created_at": "2022-12-19T15:33:58.368094Z",
        "updated_at": "2022-12-19T15:33:58.368120Z"
    }
    ```
    """

    node_name = "Reference"
    slug = "reference"

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        title: str,
        doi: Union[str, None] = None,
        authors: Union[list[str], None] = None,
        journal: Union[str, None] = None,
        publisher: Union[str, None] = None,
        year: Union[int, None] = None,
        volume: Union[int, None] = None,
        issue: Union[int, None] = None,
        pages: Union[list[int], None] = None,
        issn: Union[str, None] = None,
        arxiv_id: Union[str, None] = None,
        pmid: Union[int, None] = None,
        website: Union[str, None] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        **kwargs,
    ):
        super().__init__(public=public, **kwargs)
        self.title = title
        self.doi = doi
        self.authors = authors if authors else []
        self.journal = journal
        self.publisher = publisher
        self.year = year
        self.volume = volume
        self.issue = issue
        self.pages = pages if pages else []
        self.issn = issn
        self.arxiv_id = arxiv_id
        self.pmid = pmid
        self.website = website
        self.notes = notes
        self.group = group

    @beartype
    def save(self, get_level: int = 1, update_existing: bool = False):
        """Save a <a href="../reference" target="_blank">`Reference`</a> object.

        Args:
            get_level (int, optional): Level to recursively get nested nodes
            update_existing (bool, optional): Whether to update an existing node with the same unique fields

        Raises:
            UniqueNodeError: This reference already exists and cannot be edited.
        
        ``` py title="Example"
        # get an existing group
        my_group = Group.get(name="My group")

        # create a new reference in the existing group
        my_ref = Reference(
            group=my_group,
            title="Lange's handbook of chemistry",
            authors=["James G. Speight"],
            publisher="McGraw-Hill Education",
            year=2017,
            notes="Used for tabulating dfensities of solvent solutions",
        )

        # save the reference
        my_ref.save()
        ```
        """
        api = get_cached_api_session(self.url)

        # Create a new object via POST
        response = api.post(
            url=f"{api.url}/{self.slug}/",
            data=self._to_json(),
            valid_codes=[201, 400],
        )

        # Check if a unique error was returned
        if "unique" in response:
            unique_url = response.pop("unique")
            if unique_url and update_existing:
                # Update existing unique node
                self.url = unique_url
                self.save(get_level=get_level)
                return
            else:
                raise UniqueNodeError(response["errors"][0])

        set_node_attributes(self, response)
        self._generate_nested_nodes(get_level=get_level)
        logger.info(f"{self.node_name} node has been saved to the database.")
