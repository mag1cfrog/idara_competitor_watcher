import os
import duckdb
from loguru import logger
from dotenv import load_dotenv


def attach_db(conn: duckdb.DuckDBPyConnection) -> duckdb.DuckDBPyConnection:
    load_dotenv()

    sql_query_attach_db = f"""
    LOAD postgres;

    CREATE SECRET postgres_secret_one (
        TYPE POSTGRES,
        HOST '{os.getenv('POSTGRES_HOST')}',
        PORT 5432,
        DATABASE {os.getenv('POSTGRES_DBNAME')},
        USER 'postgres',
        PASSWORD '{os.getenv('POSTGRES_PASSWORD')}'
    );

    ATTACH '' AS db (TYPE POSTGRES, SECRET postgres_secret_one);

    """
    logger.info("Attaching Postgres database to DuckDB")
    
    conn.execute(sql_query_attach_db)
    
    return conn
