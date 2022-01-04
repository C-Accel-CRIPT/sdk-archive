"""
Tools for loading and exporting mongodb documents
"""

from ..primary_nodes.base import CriptTypes


class Load(CriptTypes):
    """ Load

    Given a document (dictionary) from the database convert it into a CRIPT object.

    """

    def __call__(self, ddict: dict):
        """ Load

        Parameters
        ----------
        ddict: dict
            dictionary (JSON) you want to turn back into CRIPT node

        Returns
        -------
        obj:
            CRIPT Node
        """
        if "_id" in ddict.keys():
            ddict["uid"] = str(ddict.pop("_id"))
        class_ = ddict.pop("class_")
        obj = self.cript_types[class_](**ddict)
        return obj


load = Load()



