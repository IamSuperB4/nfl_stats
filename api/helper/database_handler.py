"""Handles synchronous database interactions"""

import os
from dotenv import load_dotenv
from pandas import DataFrame
from pyodbc import drivers
from sqlalchemy import Engine, text, create_engine
from helper.file_reader import read_file


def run_select_query(
    environment_variable: str, query_string: str, parameters: dict = None, echo=False
) -> DataFrame:
    """Run a SELECT query

    Args:
        environment_variable (str): environment variable with connection string
        query_string (str): query string
        parameters (dict, optional): SQL parameters. Defaults to None.
        echo (bool, optional): echo SQL calls. Defaults to False.

    Returns:
        DataFrame: Dataframe with query results
    """
    # create SQL engine using connection string and create database connection
    engine: Engine = create_engine(
        create_sql_server_connection_string(environment_variable), echo=echo
    )

    # connect to the database and run the query in the connection
    with engine.connect() as db:
        # execute query
        result = db.execute(text(query_string), parameters)

        # create a dataframe from results
        return DataFrame(result.fetchall())
    

def create_sql_server_connection_string(environment_variable: str) -> str:
    """Create a connection string from an environment variable containing a connection string
        and a SQL Server driver

    Args:
        environment_variable (str): environment variable with connection string

    Returns:
        str: SQL Server connection string
    """
    # get connection string from environment variable
    load_dotenv()
    connection_string = os.getenv(environment_variable)

    driver_name = get_sql_server_driver_name()

    # add driver to connection string
    connection_string += f"&driver={driver_name}"

    return connection_string


def get_sql_server_driver_name() -> str:
    """Get a SQL Server driver name

    Raises:
        DatabaseError: No suitable driver found. Cannot connect to database.

    Returns:
        str: first valid SQL Server driver
    """
    # get list of SQL Server drivers available
    driver_names = [x for x in drivers() if x.endswith(" for SQL Server")]

    # if there were valid driver_names returned, use first one
    if driver_names:
        driver_name = driver_names[0]
    # if driver was found
    if driver_name:
        return driver_name

    raise DatabaseError("No suitable driver found. Cannot connect to database.")


def get_query_from_file(query_file_name: str) -> str:
    """Get SQL query from .sql file in queries folder

    Args:
        query_file_name (str): file name with SQL query

    Raises:
        Exception: invalid file extension, only accepts .sql

    Returns:
        str: query string
    """
    # only .sql files are accepted
    if query_file_name.endswith(".sql"):
        # if no .SQL file extension (just the file name), append it to file name
        if ".sql" not in query_file_name:
            query_file_name += ".sql"

        # read .SQL file and return contents
        return read_file(f"queries/{query_file_name}")
    # throw error if not a .sql file
    else:
        raise ValueError("Invalid file extension. Only .sql files are accepted")


def populate_lists_in_query(query_string: str, list_parameters: list[list]) -> str:
    """Put a lists in a query
        - Replace ":listN" with "(item1, item2, item3...)"

    Args:
        query_string (str): query string with ":list" in it
        parameter_list (list): list of

    Returns:
        str: query with lists replaces for "in" statements
    """
    for i, list_parameter in enumerate(list_parameters):
        # if more than one item in list that will be after the "in" condition
        if len(list_parameter) > 1:
            query_string = query_string.replace(f":list{i}", str(tuple(list_parameter)))
        # if only one item in list that will be after the "in" condition
        else:
            query_string = query_string.replace(
                f":list{i}", f"('{next(iter(list_parameter))}')"
            )  # next(iter()) able to handle 0 items in list

    return query_string


class DatabaseError(Exception):
    """Invalid datatype error

    Args:
        Exception (Exception): Invalid datatype
    """

    # Constructor or Initializer
    def __init__(self, message):
        self.value = message

    # __str__ is to print() the value
    def __str__(self):
        return repr(self.value)
