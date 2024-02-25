"""Dataframe and Dictionary/List Conversions
"""

import pandas as pd


def df_first_row_to_dict(df: pd.DataFrame) -> dict:
    """Helper function to convert the first row of a dataframe to a dictionary
        - Key: column name
        - Value: value of column in first row

    Args:
        df (Dataframe): dataframe (supposed to have one row)

    Returns:
        dict: dictionary with first row values mapped to column names
    """
    if len(df) < 1:
        return dict()

    top_row_df = df.iloc[0]
    return_value: dict = top_row_df.to_dict()

    return return_value

def df_two_columns_to_dict(
    df: pd.DataFrame, key_column_name, value_column_name
) -> dict:
    """Convert two dataframe columns to a dictionary
        *NOTE Items will be removed from dictionary if keys are the same

    Args:
        df (pd.DataFrame): dataframe
        key (any): column name of dict key
        value (any): column name of dict value

    Returns:
        dict: dictionary of 2 columns
    """
    return pd.Series(
        df[value_column_name].values, index=df[key_column_name]
    ).to_dict()

def dictionaries_as_rows_to_dataframe(
    dictionaries: dict | list, column_names: list
) -> pd.DataFrame:
    """Create a dataframe from a dictionary or a list of dictionaries when the dictionary
        values are rows

    Args:
        dictionaries (dict | list): list of dictionaries or dictionary object
        column_names (list): list of column names

    Raises:
        ValueError: Not enough column names passed in

    Returns:
        pd.DataFrame: Dataframe from dictionaries as rows
    """
    series_dict = dict()

    if isinstance(dictionaries, list):
        # not enough column names passed in
        if len(dictionaries) + 1 < len(column_names):
            raise ValueError(
                f"There are not enough column names passed in. There were \
                {len(column_names)} column names passed in for the required \
                {len(dictionaries) + 1}"
            )

        # attach a series to a column name in a dictionary for each dictionary passed in
        for i, column_name in enumerate(column_names[1:]):
            series_dict[column_name] = pd.Series(dictionaries[i])
    else:
        # not enough column names passed in
        if len(column_names) < 2:
            raise ValueError(
                f"There are not enough column names passed in. There were \
                {len(column_names)} column names passed in for the required 2"
            )

        # attach a series to a column name in a dictionary from "dictionaries"
        series_dict[column_name[1]] = pd.Series(dictionaries)

    # create dataframe from series_dict
    df = pd.DataFrame(series_dict)

    # make index column the first column
    df[column_names[0]] = df.index

    return df

def list_of_lists_to_dataframe(lists: list, column_names: list) -> pd.DataFrame:
    """Convert a list of lists to a Dataframe

    Args:
        lists (list): list of lists
        column_names (list): column names

    Returns:
        pd.DataFrame: Dataframe from list of lists
    """
    return pd.DataFrame(lists, columns=column_names)
