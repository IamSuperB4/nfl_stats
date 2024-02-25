import asyncio
from contextlib import _GeneratorContextManager
import pandas as pd
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection
from database_handler import create_sql_server_connection_string

async def async_run_multiple_select_queries(
    environment_variable: str,
    query_info_list: list[tuple[str, dict]],
    echo=False
) -> list[pd.DataFrame]:
    """Run multiple SELECT SQL queries concurrently

    Args:
        environment_variable (str): environment variable containing a connection string
        query_info_list (list[tuple[str, dict]]): query info
        echo (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    # create SQL engine using connection string and create database connection
    engine: AsyncEngine = await create_async_engine(
        create_sql_server_connection_string(environment_variable),
        echo=echo
    )

    async with engine.begin() as db:
        results = await asyncio.gather(*[async_run_single_select_query(db, query_string, parameters) for query_string, parameters in query_info_list])
        
        dataframe_results = [pd.DataFrame(result) for result in results]
        
        return dataframe_results
    
async def async_run_single_select_query(db: AsyncConnection, query_string: str, parameters: dict):
    result = await db.execute(text(query_string), parameters)
    
    # execute query and get results as a dataframe
    return result.fetchall()