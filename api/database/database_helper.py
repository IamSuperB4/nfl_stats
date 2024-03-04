"""Database helper functions"""

from dataclasses import dataclass
import os
from dotenv import load_dotenv
from sqlalchemy import URL, Engine, create_engine, engine
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)


@dataclass(frozen=True)
class DatabaseEnvVariables:
    """Database Connection class for NFL_Stats database ORM"""

    server: str
    database: str


async def async_create_session_engine(
    environment_variables: DatabaseEnvVariables, echo: bool = False
) -> AsyncSession:
    """Create an async SQLAlchemy engine for connecting to a SQL Server database.

    Args:
        environment_variables (DatabaseEnvVariables): The database environment variables.
        echo (bool, optional): Whether to echo SQL statements to the console. Defaults to False.

    Returns:
        AsyncSession: The async SQLAlchemy engine for connecting to the SQL Server database.
    """
    async_engine: AsyncEngine = await async_create_sql_server_engine(
        environment_variables, echo
    )
    return async_sessionmaker(async_engine, expire_on_commit=True)


async def async_create_sql_server_engine(
    environment_variables: DatabaseEnvVariables, echo: bool = False
) -> AsyncEngine:
    """Create a SQLAlchemy engine for connecting to a SQL Server database.

    Args:
        environment_variable (str): The name of the environment variable containing the
            SQL Server connection string.
        echo (bool, optional): Whether to echo SQL statements to the console. Defaults to False.

    Returns:
        Engine: The SQLAlchemy engine for connecting to the SQL Server database.

    Raises:
        DatabaseError: If no suitable SQL Server driver is found.
    """
    connection_url: URL = create_sql_server_connection_string(
        environment_variables, is_async=True
    )

    return create_async_engine(connection_url, echo=echo)


def create_sql_server_engine(
    environment_variables: DatabaseEnvVariables, echo: bool = False
) -> Engine:
    """Create a SQLAlchemy engine for connecting to a SQL Server database.

    Args:
        environment_variable (str): The name of the environment variable containing the
            SQL Server connection string.
        echo (bool, optional): Whether to echo SQL statements to the console. Defaults to False.

    Returns:
        Engine: The SQLAlchemy engine for connecting to the SQL Server database.

    Raises:
        DatabaseError: If no suitable SQL Server driver is found.
    """
    connection_url: URL = create_sql_server_connection_string(environment_variables)

    return create_engine(connection_url, echo=echo)


def create_sql_server_connection_string(
    environment_variables: DatabaseEnvVariables, is_async: bool = False
) -> URL:
    """Create a connection string for a SQL Server database from an environment variable.

    Args:
        environment_variable (str): The name of the environment variable containing the
            SQL Server connection string.

    Returns:
        str: The SQL Server connection string.
    """
    # Get the connection string from the environment variable
    load_dotenv()
    server = os.getenv(environment_variables.server)
    database = os.getenv(environment_variables.database)

    if is_async:
        driver_name = "mssql+aioodbc"
    else:
        driver_name = "mssql+pyodbc"

    return engine.URL.create(
        drivername=driver_name,
        host=server,
        database=database,
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "Trusted_Connection": "Yes",
            "TrustServerCertificate": "Yes",
        },
    )


class DatabaseError(Exception):
    """An error occurred with the database."""

    def __init__(self, message):
        self.value = message

    def __str__(self):
        return repr(self.value)
