import os
from pathlib import Path

import duckdb
from loguru import logger
from dotenv import load_dotenv


def attach_db(conn: duckdb.DuckDBPyConnection) -> duckdb.DuckDBPyConnection:
    load_dotenv()

    storage_type = os.getenv('STORAGE_TYPE')

    if storage_type == 'POSTGRES':
        conn = setup_postgre(conn)
        logger.info("Attaching Postgres database to DuckDB")
        conn.execute("ATTACH '' AS db (TYPE POSTGRES, SECRET postgres_secret_one);")
    
    else:
        # Local DuckDB Storage
        logger.info("Attaching local database to DuckDB")
        storage_directory = Path(os.getenv('STORAGE_DIRECTORY')).resolve()
        storage_directory.mkdir(parents=True, exist_ok=True)
        storage_file = storage_directory / "storage.duckdb"
        conn.execute(f"ATTACH '{str(storage_file)}' AS db ;")
    
    return conn


def setup_postgre(conn: duckdb.DuckDBPyConnection) -> duckdb.DuckDBPyConnection:

    sql_query_setup_postgre = f"""
    INSTALL postgres;
    LOAD postgres;

    CREATE SECRET postgres_secret_one (
        TYPE POSTGRES,
        HOST '{os.getenv('POSTGRES_HOST')}',
        PORT 5432,
        DATABASE {os.getenv('POSTGRES_DBNAME')},
        USER 'postgres',
        PASSWORD '{os.getenv('POSTGRES_PASSWORD')}'
    );
    """

    conn.execute(sql_query_setup_postgre)

    return conn


