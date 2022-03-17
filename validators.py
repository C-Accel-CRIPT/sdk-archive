from . import pint_ureg
from .errors import (
    InvalidKeyError,
    InvalidValueRangeError,
    InvalidUnitError,
    RequiredUnitError,
    APISessionRequiredError,
)


def validate_key(key_name, key_category):
    """
    Validates a key name to ensure it's in the controlled vocabulary.

    :param key_name: Name of the key.
    :key_category: Name of the relevant key category.
    """
    # Skip keys that are not defined
    if not key_name:
        return None

    key_name = key_name.strip().lower()

    # Skip validation for custom fields
    if key_name[0] == "+":
        return key_name

    key_parameters = _get_key_parameters(key_name, key_category)
    return key_parameters["name"]


def validate_key_value(value, unit, key_name, key_category):
    """
    Validates a key value is within the defined parameters.

    :param key_name: Name of the key.
    :key_category: Name of the relevant key category.
    """
    # Skip validation for custom fields
    if key_name[0] == "+":
        return value

    key_parameters = _get_key_parameters(key_name, key_category)
    value_range = key_parameters["range"]
    si_unit = key_parameters["si_unit"]

    if value_range:
        min, max = value_range[0], value_range[1]

        if si_unit:
            si_value = _unit_conversion(value, unit, si_unit)
        else:
            si_value = value

        if min <= si_value <= max:
            return value
        else:
            raise InvalidValueRangeError(key_name, value, min, max, si_unit)


def validate_key_unit(unit, key_name, key_category):
    """
    Validates a key unit exists and can be converted to SI unit.

    :param key_name: Name of the key.
    :key_category: Name of the relevant key category.
    """
    key_parameters = _get_key_parameters(key_name, key_category)
    si_unit = key_parameters["si_unit"]

    # Check if unit is required
    if si_unit and not unit:
        raise RequiredUnitError(f"A unit is required for {key_name}.")
    elif unit and not si_unit:
        raise RequiredUnitError(f"{key_name} does not allow a unit definition.")

    # Check if unit is valid
    try:
        pint_ureg[unit]
    except:
        raise InvalidUnitError(key_name, unit)

    # Skip further validation for custom fields
    if key_name[0] == "+":
        return unit

    # Test unit conversion with dummy value (1)
    try:
        _unit_conversion(1, unit, si_unit)
        return unit
    except:
        raise InvalidUnitError(key_name, unit)


def _get_key_parameters(key_name, key_category):
    """Get the parameters for a given key from full keys dictionary."""
    from .connect import API

    all_keys = API.keys
    key_name = key_name.strip().lower()

    if all_keys:
        # Fetch relevant keys
        if key_category == "property-key":
            keys = all_keys["material-property-key"] + all_keys["step-property-key"]
        else:
            keys = all_keys[key_category]

        for key in keys:
            if key_name == key["name"]:
                return key

        raise InvalidKeyError(key_name, key_category.replace("-", " "))
    else:
        raise APISessionRequiredError


def _unit_conversion(value, unit, si_unit):
    """Converts a value to SI units."""
    original_quantity = pint_ureg.Quantity(value, unit)
    si_value = original_quantity.to(si_unit).magnitude
    return si_value
