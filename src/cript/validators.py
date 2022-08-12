from cript import pint_ureg
from cript.exceptions import (
    InvalidKeyError,
    InvalidValueTypeError,
    InvalidValueRangeError,
    InvalidUnitError,
    RequiredUnitError,
    APISessionRequiredError,
)


def validate_key(key_category, key):
    """
    Validates that the key name is in the controlled vocabulary.

    :param key_category: Name of the relevant key category.
    :param key: Name of the key.
    :return: The validated key name.
    :rtype: str
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

    :param key_category: Name of the relevant key category.
    :param key: Name of the key.
    :param value: Value to be validated.
    :param unit: The value's unit of measurement.
    :return: The validated value.
    :rtype: Union[int, float, str]
    """
    # Skip validation for empty values and custom fields
    if not key or key[0] == "+":
        return value

    key_parameters = _get_key_parameters(key_category, key)
    value_range = key_parameters.get("range")
    si_unit = key_parameters.get("si_unit")

    # Check if value is expected
    value_type = key_parameters.get("value_type")
    if value is None and value_type:
        raise ValueError(f"A value must be defined for {key}.")
    elif value is not None and not value_type:
        return None
    elif value is None and not value_type:
        return value

    if value_type:
        _validate_value_type(key, value, value_type)
    if value_range:
        _validate_value_range(key, value, value_range, unit, si_unit)

    return value


def _validate_value_type(key, value, value_type):
    """
    Validate that the value is of the expected type.

    :param key: Name of the key.
    :param value: Value to be validated.
    :param value_type: The expected value type as listed in the key tables.
    """
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
    """
    Validates a value is within the defined range.

    :param key: Name of the key.
    :param value: Value to be validated.
    :param value_range: The upper and lower bounds for the value.
    :param unit: The unit entered by the user.
    :param si_unit: The SI unit for the specific attribute.
    """
    min_, max_ = value_range[0], value_range[1]

    # convert to SI units if defined
    if si_unit:
        pint_unit = _validate_unit(key, unit, si_unit)
        pint_quantity = value * pint_unit
        value = pint_quantity.to(si_unit).magnitude

    if not min_ <= value <= max_:
        raise InvalidValueRangeError(key, value, min_, max_, si_unit)


def validate_unit(key_category, key, unit):
    """
    Validates that the unit exists and can be converted to SI units.

    :param key_category: Name of the relevant key category.
    :param key: Name of the key.
    :param unit: Unit to be validated.
    :return: The validated unit.
    :rtype: str
    """
    # Skip further validation for custom fields
    if not key or key[0] == "+":
        if unit:
            _validate_pint_unit(unit)
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

    _validate_unit(key, unit, si_unit)

    return unit


def _validate_unit(key, unit, si_unit) -> pint_ureg.Unit:
    """
    Validates that the unit can be converted to appropriate SI units.

    :param key: Name of the key.
    :param unit: The unit entered by the user.
    :param si_unit: The SI unit for the specific attribute.
    """
    pint_unit = _validate_pint_unit(unit)

    if pint_unit.dimensionality != pint_ureg.Unit(si_unit).dimensionality:
        raise InvalidUnitError(f"{unit} is not a recognized unit of measure for {key}.")

    return pint_unit


def _validate_pint_unit(unit) -> pint_ureg.Unit:
    """
    Validates that the unit can be converted to appropriate SI units.

    :param unit: The unit entered by the user.
    """
    try:
        pint_unit = pint_ureg.Unit(unit)
    except Exception as e:
        raise InvalidUnitError(f"{unit} is not a recognized unit of measure.")

    return pint_unit


def _get_key_parameters(key_category, key):
    """
    Get the parameters for a given key from full keys dictionary.

    :param key_category: Name of the relevant key category.
    :param key: Name of the key.
    """
    from cript.api import API

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
