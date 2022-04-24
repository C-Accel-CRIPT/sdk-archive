from cript import pint_ureg
from cript.exceptions import (
    InvalidKeyError,
    InvalidValueTypeError,
    InvalidValueRangeError,
    InvalidUnitError,
    RequiredUnitError,
    APISessionRequiredError,
    RequiredFieldsError,
)


def validate_required(node):
    """Validate that required fields are defined."""
    for field in node.required:
        if not hasattr(node, field) or not getattr(node, field):
            raise RequiredFieldsError(node.required)


def validate_key(key_category, key):
    """
    Validates a key name to ensure it's in the controlled vocabulary.

    :key_category: Name of the relevant key category.
    :param key: Name of the key.
    """
    # Skip validation for custom and undefined keys
    if not key or key[0] == "+":
        return key

    key = key.strip().lower()
    key_parameters = _get_key_parameters(key_category, key)
    return key_parameters["name"]


def validate_value(key_category, key, value, unit=None):
    """
    Validates a value is within the defined parameters.

    :key_category: Name of the relevant key category.
    :param key: Name of the key.
    :param value: Value to be validated.
    :param unit: The value's unit of measurement.
    """
    # Skip validation for custom fields
    if key[0] == "+":
        return value

    key_parameters = _get_key_parameters(key_category, key)
    value_range = key_parameters.get("range")
    si_unit = key_parameters.get("si_unit")

    # Check if value is expected
    value_type = key_parameters.get("value_type")
    if not value and value_type:
        raise ValueError(f"A value must be defined for {key}.")
    elif value and not value_type:
        raise ValueError(f"A value is not expected for {key}")
    elif not value and not value_type:
        return value

    if value_type:
        _validate_value_type(key, value, value_type)
    if value_range:
        _validate_value_range(key, value, value_range, unit, si_unit)

    return value


def _validate_value_type(key, value, value_type):
    """Validate that the value is of the expected type."""
    value_types = {
        "number": (int, float),
        "integer": int,
        "float": float,
        "string": str,
        "list[number]": [(int, float)],
        "list[integer]": [int],
        "list[float]": [float],
        "list[string]": [str],
    }
    value_type = value_types[value_type]

    # Handle lists
    if isinstance(value_type, list):
        if not isinstance(value, list) or not all(
            isinstance(i, value_type[0]) for i in value
        ):
            raise InvalidValueTypeError(key)

    elif not isinstance(value, value_type):
        raise InvalidValueTypeError(key)


def _validate_value_range(key, value, value_range, unit, si_unit):
    """Validates a value is within the defined range."""
    min, max = value_range[0], value_range[1]

    # convert to SI units if defined
    if si_unit:
        value = _unit_conversion(value, unit, si_unit)

    if not min <= value <= max:
        raise InvalidValueRangeError(key, value, min, max, si_unit)


def validate_unit(key_category, key, unit):
    """
    Validates that the unit exists and can be converted to SI units.

    :key_category: Name of the relevant key category.
    :param key: Name of the key.
    :param unit: Unit to be validated.
    """
    _validate_unit_exists(unit)

    # Skip further validation for custom fields
    if key[0] == "+":
        return unit

    key_parameters = _get_key_parameters(key_category, key)
    si_unit = key_parameters["si_unit"]

    # Check if unit should be defined
    if not unit and not si_unit:
        return unit
    if si_unit and not unit:
        raise RequiredUnitError(f"A unit is required for {key}.")
    elif unit and not si_unit:
        raise RequiredUnitError(f"A unit is not permitted for {key}.")

    _validate_unit_exists(unit)

    _validate_unit_conversion(key, unit, si_unit)

    return unit


def _validate_unit_exists(unit):
    """Validates that the unit exists."""
    try:
        pint_ureg[unit]
    except:
        raise InvalidUnitError(f"{unit} is not a recognized unit of measure.")


def _validate_unit_conversion(key, unit, si_unit):
    """Validates that the unit can be converted to appropriate SI units."""
    try:
        _unit_conversion(1, unit, si_unit)
    except:
        raise InvalidUnitError(f"{unit} is not a recognized unit of measure for {key}.")


def _unit_conversion(value, unit, si_unit):
    """Converts a value to SI units."""
    original_quantity = pint_ureg.Quantity(value, unit)
    si_value = original_quantity.to(si_unit).magnitude
    return si_value


def _get_key_parameters(key_category, key):
    """Get the parameters for a given key from full keys dictionary."""
    from cript.session import API

    if API.keys:
        # Fetch relevant keys
        if key_category == "property-key":
            keys_info = (
                API.keys["material-property-key"] + API.keys["process-property-key"]
            )
        else:
            keys_info = API.keys[key_category]

        key = key.strip().lower()
        for key_info in keys_info:
            if key == key_info["name"]:
                return key_info

        raise InvalidKeyError(key, key_category.replace("-", " "))
    else:
        raise APISessionRequiredError
