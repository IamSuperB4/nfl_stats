"""Store tables and get .pkl from files
"""

import os
import time
import pandas as pd

from helper.database_handler_old import DatabaseHandler
from console_writer import ConsoleWriter
from helper.file_reader import get_files_in_folder_with_filetype


class Tables:
    """
    This module handles retrieving and storing SQL tables

    Import:
        from helper.tables import Tables

    Example:

        usage:
            tables.get_table('CatProp')

    Attributes:

    @Author: Bradley Knorr
    @Date: 1/22/2024
    """

    def __init__(
        self,
        db: DatabaseHandler = None,
        console_writer: ConsoleWriter = None,
        store_in_memory=True,
    ):
        if DatabaseHandler is None:
            self.db = DatabaseHandler()
        else:
            self.db = db

        self.console_writer = console_writer
        self.store_in_memory = store_in_memory

        self.dataframes = dict()
        self.queries_list = dict()

        self.table_collections: dict = {
            "properties": [
                "category_extension_queries",
                "catprop_queries",
                "CT_Category",
                "CT_CatProp_with_lookup",
                "properties_master",
                "CT_ExtensionQuery",
                "CT_Formula",
                "CT_OptionProp",
                "dotnet",
                "lists",
                "model_series",
                "properties_master",
                "properties",
                "queries",
                "sales_codes_category",
            ]
        }

    def update_tables(self, tables: str | list):
        """Update .pkl files with current SQL query results through one of three methods:
            1. Run a list of pre-defined queries in the table_collections
            2. Run list of queries passed in
            3. Run a single query passed in

        Args:
            tables (str | list): query collection name, query name, or list of query names

        Raises:
            TypeError: str or list was not passed in
        """
        # start stopwatch
        start = time.time()

        ## get list of files to run SQL query and save results for ##

        # if a string was passed in, it is either a collection name or a query name
        if isinstance(tables, str):
            # run all queries in folder
            if tables.lower() == "all":
                files = get_files_in_folder_with_filetype("queries", "sql")
                queries_to_run = [x[:-4] for x in files]
            # if collection name, set list to all queries in collection
            elif tables in self.table_collections:
                queries_to_run = self.table_collections[tables]
            # otherwise it is a query name, so set list to single query
            else:
                queries_to_run = [tables]
        # if list was passed in, it is a list of query names, so set queries_to_run to list
        elif isinstance(tables, list):
            queries_to_run = tables
        else:
            raise TypeError(
                f"set_tables() does not accept parameter of type {type(tables)} ({tables})"
            )

        # run each SQL query and save results to .pkl file
        for query_name in queries_to_run:
            self.db.run_query(f"{query_name}.sql").to_pickle(
                f"saved_query_results/{query_name}.pkl"
            )

        # stop stopwatch
        end = time.time()

        # print how long it took to run and save all queries
        if self.console_writer is not None:
            self.console_writer.print(
                1,
                f"Query and Extension Query .pkl files updated in {round(end - start, 4)} seconds",
            )
        else:
            print(f"Query .pkl files updated in {round(end - start, 4)} seconds")

    ###############################################
    # Get SQL tables from .pkl files
    ###############################################
    def get_table(self, query_name: str) -> pd.DataFrame:
        """Gets table from database with sales codes and static properties

        Args:
            query_name (str): query file name in queries folder to run

        Returns:
            Dataframe: dataframe in .pkl file
        """
        # if query results are already stored in memory
        if query_name in self.dataframes:
            return self.dataframes[query_name]

        # attempt to get query result from .pkl file

        # if there is a .sql file in queries/, but no .pkl file in
        #   saved_query_results/, create the .pkl file
        if not os.path.isfile(
            f"saved_query_results/{query_name}.pkl"
        ) and os.path.isfile(f"queries/{query_name}.sql"):
            self.update_tables(query_name)

        # if there is a stored .pkl file for this query in saved_query_results
        df = pd.read_pickle(f"saved_query_results/{query_name}.pkl")

        # if storing tables in memory, set the dictionary value
        if self.store_in_memory:
            self.dataframes[query_name] = df

        return df
