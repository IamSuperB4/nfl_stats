from sqlalchemy import Engine, MetaData
from db_tables import meta
from database_helper import create_sql_server_engine


def create_database_tables(db_meta_object: MetaData, envrironment_variable: str) -> None:
    """Create database tables

    Args:
        db_meta_object (MetaData): MetaData object containing table information
        envrironment_variable (str): environment variable that contains the connections string
    """
    engine: Engine = create_sql_server_engine(envrironment_variable, True)
    db_meta_object.create_all(engine)
    

if __name__ == "__main__":
  create_database_tables(meta, 'NFL_Stats')
