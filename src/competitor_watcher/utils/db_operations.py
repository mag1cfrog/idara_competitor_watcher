import duckdb
from loguru import logger
import polars as pl


@logger.catch
def create_table(conn: duckdb.DuckDBPyConnection, table_name: str, schema: str):
    sql_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {schema}
    );
    """
    
    conn.execute(sql_query)
    logger.trace(f"Table {table_name} created successfully/already exists")

@logger.catch
def insert_data(conn: duckdb.DuckDBPyConnection, table_name: str, df: pl.DataFrame, df_name: str, unique_columns: list):
    unique_conditions = ' AND '.join(f'i.{col} = t.{col}' for col in unique_columns)
    sql_query = f"""
    INSERT INTO {table_name}
        SELECT *
        FROM {df_name} t
    WHERE NOT EXISTS (
        SELECT 1
        FROM {table_name} i
        WHERE {unique_conditions}
    );
    """
    logger.trace("Inserting data into db.item_attribute")
    conn.execute(sql_query)
    logger.trace("Data inserted successfully")