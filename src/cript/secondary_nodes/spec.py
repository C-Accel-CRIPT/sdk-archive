"""
Material Specification

"""
from typing import Union
from datetime import datetime

from .. import Quantity
from ..utils import Serializable, convert_to_list, loading_with_units, loading_with_datetime
from ..validator import type_check
from .cond import Cond
from .hazard import Hazard


class Spec(Serializable):
    """ Material Specification

    Attributes
    ----------
    vendor: str
        company the material was obtain from
    lot_number: str
        batch number
    storage_cond: list[Cond]
        storage conditions
    storage_loc: str
        storage location
    hazard: Hazard
        See help(Hazard)
    quantity: Quantity
        how much material left
    initial_quantity: Quantity
        how much material started with
    container: str
        type, or size of container
    origin_date: datetime
        date the material was created/received
    expiration_date: datetime
        date the material should be discarded

    """

    def __init__(self,
                 vendor: str = None,
                 lot_number: str = None,
                 storage_cond: Union[list[Cond], Cond] = None,
                 storage_loc: str = None,
                 hazard: Hazard = None,
                 quantity: Quantity = None,
                 initial_quantity: Quantity = None,
                 container: str = None,
                 origin_date: datetime = None,
                 expiration_date: datetime = None,
                 ):
        self._vendor = None
        self.vendor = vendor

        self._lot_number = None
        self.lot_number = lot_number

        self._storage_cond = None
        self.storage_cond = storage_cond

        self._storage_loc = None
        self.storage_loc = storage_loc

        self._hazard = None
        self.hazard = hazard

        self._quantity = None
        self.quantity = quantity

        self._initial_quantity = None
        self.initial_quantity = initial_quantity

        self._container = None
        self.container = container

        self._origin_date = None
        self.origin_date = origin_date

        self._expiration_date = None
        self.expiration_date = expiration_date

    @property
    def vendor(self):
        return self._vendor

    @vendor.setter
    @type_check(str)
    def vendor(self, vendor):
        self._vendor = vendor

    @property
    def lot_number(self):
        return self._lot_number

    @lot_number.setter
    @type_check(str)
    def lot_number(self, lot_number):
        self._lot_number = lot_number

    @property
    def storage_cond(self):
        return self._storage

    @storage_cond.setter
    @type_check(list[Cond])
    @convert_to_list
    @loading_with_units(Cond)
    def storage_cond(self, storage):
        self._storage = storage

    @property
    def hazard(self):
        return self._hazard

    @hazard.setter
    @type_check(Hazard)
    def hazard(self, hazard):
        self._hazard = hazard

    @property
    def quantity(self):
        return self._hazard

    @quantity.setter
    @type_check(Quantity)
    def quantity(self, quantity):
        self._quantity = quantity

    @property
    def initial_quantity(self):
        return self._initial_quantity

    @initial_quantity.setter
    @type_check(Quantity)
    def initial_quantity(self, initial_quantity):
        self._initial_quantity = initial_quantity

    @property
    def container(self):
        return self._container

    @container.setter
    @type_check(str)
    def container(self, container):
        self._container = container

    @property
    def origin_date(self):
        return self._container

    @origin_date.setter
    @type_check(datetime)
    @loading_with_datetime
    def origin_date(self, origin_date):
        self._origin_date = origin_date

    @property
    def expiration_date(self):
        return self._expiration_date

    @expiration_date.setter
    @type_check(datetime)
    @loading_with_datetime
    def expiration_date(self, expiration_date):
        self._expiration_date = expiration_date
