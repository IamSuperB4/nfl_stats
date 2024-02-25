""" Handle different types of conversions
"""

import pandas as pd

from helper.custom_errors import PropertyError


def to_lookup_table_name(table_name: str, is_view: bool) -> str:
    """Convert lookup table name to database table name

    Args:
        table_name (str): name of table
        is_view (bool): if table is a view

    Returns:
        str: database table name
    """
    table_type_letter = "v" if is_view else "t"
    return "dbo.look" + table_type_letter + "0000_" + table_name

def get_query_parameter_value(
    source: str, filtered_properties_df: pd.DataFrame
):
    """Converts Experlogix property/table name to database equivalents
        - used for lookup table names and MPC property values

    Args:
        source (string): Experlogix property/table name

    Raises:
        Exception: if source is not a recognized value

    Returns:
        string: value that can be put into a database query
    """
    # if lookup table, convert to database table name
    if source.startswith("[&Lookup:"):
        # check if lookup table is a view
        is_view = "view" in source.lower()

        # remove "[&Lookup:" from beginning of string
        table_name = source[9:]

        # if view, remove ";View]", otherwise just remove closing bracket "]"
        table_name = table_name[:-6] if is_view else table_name[:-1]

        # convert to lookup table name
        return to_lookup_table_name(table_name, is_view)

    ###################################################################
    # this needs to be removed one day and be in the Property values
    ###################################################################
    if source.find("MPC.uxce_pr_lvl_no") != -1:
        return 144

    # if literal value/constant
    if source.startswith("[@"):
        if '"' in source:
            constant = source.split('"')[1]
        else:
            constant = source.split("]")[1][2:]

        return constant

    # if property
    if source.startswith("["):
        property_value_row = filtered_properties_df[
            filtered_properties_df["FullPropertyName"] == source[1:-1]
        ]

        if len(property_value_row) > 0:
            return property_value_row.iloc[0]["PropertyValue"]

        raise PropertyError(source, f'Property {source} was not found')

    # if parameter was not set
    if source == "":
        return ""

    # something is wrong if it got here
    raise ValueError("Unknown variable: " + source)
