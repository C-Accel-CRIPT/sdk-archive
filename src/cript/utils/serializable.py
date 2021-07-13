import abc


class Serializable(abc.ABC):
    """Base abstract class for a serializable object."""

    def as_dict(self):
        """Convert and return object as dictionary."""
        keys = {k.lstrip("_") for k in vars(self)}
        attr = {k: Serializable._to_dict(self.__getattribute__(k)) for k in keys}
        return attr

    @staticmethod
    def _to_dict(obj):
        """Convert obj to a dictionary, and return it."""
        if isinstance(obj, list):
            return [Serializable._to_dict(i) for i in obj]
        elif hasattr(obj, "as_dict"):
            return obj.as_dict()
        else:
            return obj

    @classmethod
    def from_dict(cls, ddict):
        """Construct an object from the input dictionary."""
        return cls(**ddict)




