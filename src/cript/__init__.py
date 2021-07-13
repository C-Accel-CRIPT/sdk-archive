import pkg_resources

__all__ = ["VERSION", "__version__", "__short_version__"]

# single-sourcing the package version
version_file = pkg_resources.resource_filename("cript", "VERSION.txt")
with open(version_file, "r") as fr:
    __version__ = fr.read().strip()

VERSION = __version__
__short_version__ = __version__.rpartition(".")[0]


from .base import *
from .user import *
from .group import *
from .collection import *
from .data import *
from .experiment import *
from .inventory import *
from .material import *
from .process import *
from .sample import *
from .simulation import *
