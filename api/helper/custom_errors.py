"""Custom errors
"""
class RuleError(Exception):
    """Error for rules

    Args:
        Exception (Exception): rule error
    """

    # Constructor or Initializer
    def __init__(self, value):
        self.value = value

    # __str__ is to print() the value
    def __str__(self):
        return repr(self.value)


class FormulaError(Exception):
    """Error for formulas

    Args:
        Exception (Exception): formula error
    """

    # Constructor or Initializer
    def __init__(self, value):
        self.value = value

    # __str__ is to print() the value
    def __str__(self):
        return repr(self.value)


class SalesCodeError(Exception):
    """Error for sales codes

    Args:
        Exception (Exception): sales code error
    """

    # Constructor or Initializer
    def __init__(self, value):
        self.value = value

    # __str__ is to print() the value
    def __str__(self):
        return repr(self.value)


class QueryError(Exception):
    """Error for query

    Args:
        Exception (Exception): query error
    """

    # Constructor or Initializer
    def __init__(self, value):
        self.value = value

    # __str__ is to print() the value
    def __str__(self):
        return repr(self.value)


class PropertyError(Exception):
    """Error for properties

    Args:
        Exception (Exception): property error
    """

    # Constructor or Initializer
    def __init__(self, property_name: str, message: str):
        self.property_name: str = property_name
        self.message = message

    # __str__ is to print() the value
    def __str__(self):
        return repr(self.message)


class MissingPropertyError(Exception):
    """Error for missing properties

    Args:
        Exception (Exception): missing properties error
    """

    # Constructor or Initializer
    def __init__(self, properties: list | set):
        self.properties = properties
        self.value = f"Properties ({properties}) are not set"

    # __str__ is to print() the value
    def __str__(self):
        return repr(self.value)

    def missing_properties(self):
        """List/set of properties missing

        Returns:
            list|set: properties missing
        """
        return self.properties


class InvalidPropertyValueError(Exception):
    """Error for invalid property value

    Args:
        Exception (Exception): invalid property value
    """

    # Constructor or Initializer
    def __init__(self, full_property_name=None, property_value=None, datatype=None):
        if full_property_name is None:
            self.value = "Invalid property value"
        elif property_value is None:
            self.value = f"{full_property_name} is not set to the proper datatype"
        elif datatype is None:
            self.value = f"{full_property_name} property value {property_value} is not set to \
                the proper datatype"
        else:
            self.value = f'{full_property_name} requires a {datatype}, but the property value \
                ("{property_value}") is not a {datatype}'

        self.full_property_name = full_property_name

    # __str__ is to print() the value
    def __str__(self):
        return repr(self.value)

    def property_in_error(self) -> str:
        """Get the property value that caused the error

        Returns:
            str: full property name
        """
        return self.full_property_name


class DataTypeError(Exception):
    """Invalid datatype error

    Args:
        Exception (Exception): Invalid datatype
    """

    # Constructor or Initializer
    def __init__(self, value: str, message: str, datatype: str):
        self.message: str = message
        self.value: str = value
        self.datatype: str = datatype

    # __str__ is to print() the value
    def __str__(self):
        return repr(self.message)


class NotFoundInDatabaseError(Exception):
    """Invalid datatype error

    Args:
        Exception (Exception): Invalid datatype
    """

    # Constructor or Initializer
    def __init__(self, object_not_found: str, message: str):
        self.object_not_found = object_not_found
        self.value = message

    # __str__ is to print() the value
    def __str__(self):
        return repr(self.value)
