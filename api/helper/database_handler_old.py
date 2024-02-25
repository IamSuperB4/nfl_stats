"""Handles database interactions
"""

import os
from dotenv import load_dotenv
import pandas as pd
import pyodbc
import sqlalchemy as sal
from helper.file_reader import read_file

class DatabaseHandler:
    """
    This module creates a database connection to specified environment and runs SQL queries

    Import:
        from helper import Database_Handler

    Example:
        initialization:
            db = Database_Handler(environment)
            db = Database_Handler(environment, False) -> does not create connection
                on initialization

        usage:
            Connect to database: db.connect_to_database()
            Run query string:
                - db.run_query('example_query.sql')
                - db.run_query('SQL query string')
            Run parameterized query:
                - db.run_query_parameterized('example_query.sql',
                    { parameter (key): parameter_value (value) })
                - db.run_query_parameterized('SQL query string',
                    { parameter (key): parameter_value (value) })

    Attributes:
        server (string): Which server to connect to (ie SalesTool or EASOP)
        database (string): Which database to connect to.
            Or Experlogix environment or EASOP database
        engine (sqlalchemy MockConnection): sqlalchemy db engine
        conn (sqlalchemy MockConnection): sqlalchemy db connection

    @Author: Bradley Knorr
    @Date: 8/31/2023
    @Credit:
    """

    engine: sal.Engine
    conn: sal.Connection

    def __init__(self, environment_variable: str, create_connection=True):
        """Initialzes database connection if create_connection is True

        Args:
            server (string): Database server
            database (string): Experlogix environment or database name
            create_connection (bool, optional): creates database connection if True.
                Defaults to True.
        """
        load_dotenv()
        connection_string = os.getenv(environment_variable)

        if create_connection:
            self.create_db_connection(connection_string)

    def create_db_connection(self, connection_string):
        """Create a database instance

        Args:
            server (string): SQL server name to pass into connection string
            database (string): SQL database name to pass into connection string

        Raises:
            Exception: if driver could not be found
        """
        driver_name = ""
        # get list of SQL Server drivers available
        driver_names = [x for x in pyodbc.drivers() if x.endswith(" for SQL Server")]

        # if there were valid driver_names returned, use first one
        if driver_names:
            driver_name = driver_names[0]
        # if driver was found
        if driver_name:
            full_connection_string = connection_string + f"&driver={driver_name}"

            # create sal engine using connection string and create database connection
            self.engine = sal.create_engine(full_connection_string)
            self.conn = self.engine.connect()
        else:
            print("(No suitable driver found. Cannot connect to database.)")
            raise DatabaseError("No suitable driver found. Cannot connect to database.")

    def get_query(self, query_file_name: str) -> str:
        """Get SQL query from .sql file in queries folder

        Args:
            query_file_name (str): file name with SQL query

        Raises:
            Exception: invalid file extension, only accepts .sql

        Returns:
            str: _description_
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
            raise ValueError("Invalid file extension (only .sql)")

    def run_query(self, query_string_or_file: str, is_file_name=False) -> pd.DataFrame:
        """Run a straight SQL query to current connection and returns result as a dataframe
            Accepts:
                - A straight query string
                - A .sql file with query string

        Args:
            query_string_or_file (string): query string for file with
                query string in queries/ folder
            is_file_name (bool, optional): manual check if a .sql file is being based in
                instead of a query string. Defaults to False.

        Returns:
            Dataframe: result from database query as a dataframe
        """
        # if query is in a .sql file, read and extract it from the file
        if query_string_or_file.endswith(".sql") or is_file_name:
            query_string = self.get_query(query_string_or_file)
        # if an entire query was passes in
        else:
            query_string = query_string_or_file

        # execute query and get results as a dataframe
        sql_query = pd.read_sql_query(query_string, self.engine)

        return pd.DataFrame(sql_query)

    def run_query_parameterized(
        self, query_string_or_file: str, parameters: dict, is_file_name=False
    ) -> pd.DataFrame:
        """Run a parameterized SQL query to current connection and returns result as a dataframe
            Accepts:
                - A straight query string
                - A .sql file with query string

        Args:
            query_string_or_file (string): query string for file with
                query string in queries/ folder
            parameters (dict): parameter mapping: { parameter: parameter_value }
            is_file_name (bool, optional): manual check if a .sql file is being based in
                instead of a query string. Defaults to False.

        Returns:
            Dataframe: result from database query as a dataframe
        """
        # if query_string_or_file is in a .sql file, read and extract it from the file
        if query_string_or_file.endswith(".sql") or is_file_name:
            query_string = self.get_query(query_string_or_file)
        # if an entire query was passes in
        else:
            query_string = query_string_or_file

        # print(query_string)

        # set query statement and SQL parameters
        stmt = sal.sql.text(query_string)
        result = self.conn.execute(stmt, parameters)

        # execute query and get results as a dataframe
        df = pd.DataFrame(result.fetchall())

        return df

    def sql_evaluator_run_multiple_queries(
        self, query_strings: list, parameters: list
    ) -> list:
        """Used for the SQL_Evaluator object to run multiple SQL queries at once to reduce time
            it takes to run a batch of SQL queries. This makes many assumptions becaus
            Experlogix queries are being run:


        Args:
            query_string_or_file (list): query strings or file with query strings in queries/ folder
            parameters (list): list parameter mappings: { parameter: parameter_value }

        Returns:
            list: list of results (sqlalchemny "Row" objects)
        """
        query_results_list = [None] * len(query_strings)

        for i, query_string in enumerate(query_strings):
            try:
                # set query statement and SQL parameters
                stmt = sal.sql.text(query_string)
                result = self.conn.execute(stmt, parameters[i])

                # execute query and get results as a dataframe
                query_results_list[i] = result.first()
            except DatabaseError:
                query_results_list[i] = "error"

        return query_results_list

    def run_query_in_list(
        self, query_string_or_file: str, parameter_list: list, is_file_name=False
    ) -> pd.DataFrame:
        """Run a straight SQL query to current connection with the list in the WHERE clause and
            returns result as a dataframe

            Accepts:
                - A straight query string
                - A .sql file with query string

            Note:
                - Put ":list" in query to replace that with the list

        Args:
            query_string_or_file (string): query string for file with query string
                in queries/ folder
            parameter_list (list): list of items for WHERE IN clause
            is_file_name (bool, optional): manual check if a .sql file is being based in instead
                of a query string. Defaults to False.

        Returns:
            Dataframe: result from database query as a dataframe
        """
        # if query is in a .sql file, read and extract it from the file
        if query_string_or_file.endswith(".sql") or is_file_name:
            query_string = self.get_query(query_string_or_file)
        # if an entire query was passes in
        else:
            query_string = query_string_or_file
        # if more than one item in list that will be after the "in" condition
        if len(parameter_list) > 1:
            query_string = query_string.replace(":list", str(tuple(parameter_list)))
        # if only one item in list that will be after the "in" condition
        else:
            #
            query_string = query_string.replace(
                ":list", "('" + next(iter(parameter_list)) + "')"
            )  # able to handle 0 items in list

        # execute query and get results as a dataframe
        sql_query = pd.read_sql_query(query_string, self.engine)

        return pd.DataFrame(sql_query)

    def close(self):
        """Close database connection"""
        self.conn.close()
