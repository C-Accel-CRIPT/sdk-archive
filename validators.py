from . import pint_ureg
from .errors import (
    InvalidKeyError,
    InvalidValueTypeError,
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
    # Skip validation for custom and undefined keys
    if not key_name or key_name[0] == "+":
        return key_name

    key_name = key_name.strip().lower()
    key_parameters = _get_key_parameters(key_name, key_category)
    return key_parameters["name"]


def validate_value(value, unit, key_name, key_category):
    """
    Validates a key value is within the defined parameters.

    :param key_name: Name of the key.
    :key_category: Name of the relevant key category.
    """
    # Skip validation for custom fields
    if key_name[0] == "+":
        return value

    key_parameters = _get_key_parameters(key_name, key_category)
    value_range = key_parameters.get("range")
    value_type = key_parameters.get("value_type")
    si_unit = key_parameters.get("si_unit")

    if value_type:
        _validate_value_type(key_name, value, value_type)
    if value_range:
        _validate_value_range(key_name, value, value_range, unit, si_unit)

    return value


def _validate_value_type(key_name, value, value_type):
    """Validate that the value is of the expected type."""
    value_types = {
        "number": (int, float),
        "integer": int,
        "float": float,
        "string": str,
        "list[number]": (int, float),
        "list[integer]": int,
        "list[float]": float,
        "list[string]": str,
    }
    value_type = value_types[value_type]

    if not isinstance(value, value_type):
        raise InvalidValueTypeError(key_name)


def _validate_value_range(key_name, value, value_range, unit, si_unit):
    """Validates a value is within the defined range."""
    min, max = value_range[0], value_range[1]

    # convert to SI units if defined
    if si_unit:
        si_value = _unit_conversion(value, unit, si_unit)
    else:
        si_value = value

    if not min <= si_value <= max:
        raise InvalidValueRangeError(key_name, value, min, max, si_unit)


def validate_unit(unit, key_name, key_category):
    """
    Validates that the unit exists and can be converted to SI units.

    :param key_name: Name of the key.
    :key_category: Name of the relevant key category.
    """
    key_parameters = _get_key_parameters(key_name, key_category)
    si_unit = key_parameters["si_unit"]

    # Check if unit should be defined
    if not unit and not si_unit:
        return unit
    if si_unit and not unit:
        raise RequiredUnitError(f"A unit is required for {key_name}.")
    elif unit and not si_unit:
        raise RequiredUnitError(f"A unit is not permitted for {key_name}.")

    # Check if unit is valid
    try:
        pint_ureg[unit]
    except:
        raise InvalidUnitError(f"{unit} is not a recognized unit of measure.")

    # Skip further validation for custom fields
    if key_name[0] == "+":
        return unit

    # Test unit conversion with dummy value (1)
    try:
        _unit_conversion(1, unit, si_unit)
        return unit
    except:
        raise InvalidUnitError(
            f"{unit} is not a recognized unit of measure for {key_name}."
        )


def _get_key_parameters(key_name, key_category):
    """Get the parameters for a given key from full keys dictionary."""
    from .connect import API

    if API.keys:
        # Fetch relevant keys
        if key_category == "property-key":
            keys = API.keys["material-property-key"] + API.keys["step-property-key"]
        else:
            keys = API.keys[key_category]

        key_name = key_name.strip().lower()
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
