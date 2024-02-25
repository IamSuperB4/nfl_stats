import os
from dotenv import load_dotenv
from pyodbc import drivers
from sqlalchemy import Engine, create_engine

def create_sql_server_engine(environment_variable: str, echo: bool = False) -> Engine:
    connection_string = create_sql_server_connection_string(environment_variable)
    
    return create_engine(connection_string, echo=echo)

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