import sys

import duckdb
from loguru import logger
import polars as pl

from competitor_watcher.data_loading.data_preparation import prepare_data
from competitor_watcher.storage.db_management import attach_db
from competitor_watcher.storage.db_operations import create_table, insert_data
from competitor_watcher.utils.time_utils import get_current_timestamp


def load_attribute_data(conn: duckdb.DuckDBPyConnection, df: pl.DataFrame, schema: str) -> None:
    create_table(conn, 'db.item_attribute', schema)
    insert_data(conn, 'db.item_attribute', df, 'df', ['Identifiers_MarketplaceASIN_ASIN', 'Timestamp'])
    


def load_pricing_data(conn: duckdb.DuckDBPyConnection, df: pl.DataFrame, schema: str) -> None:
    create_table(conn, 'db.item_pricing', schema)
    insert_data(conn, 'db.item_pricing', df, 'df', ['ASIN', 'Timestamp', 'CompetitivePrices_condition'])


def load_inventory_data(conn: duckdb.DuckDBPyConnection, df: pl.DataFrame, schema: str) -> None:
    create_table(conn, 'db.inventory', schema)
    insert_data(conn, 'db.inventory', df, 'df', ['ASIN', 'Timestamp'])


def data_loader():

    timestamp = get_current_timestamp()

    
    (
        (item_attribute_df_2, item_attribute_schema),
        (item_pricing_df_2, item_pricing_schema),
        (inventory_df_2, inventory_schema)
     ) = prepare_data(timestamp)



    with duckdb.connect() as conn:
        conn = attach_db(conn)
        load_attribute_data(conn, item_attribute_df_2, item_attribute_schema)
        load_pricing_data(conn, item_pricing_df_2, item_pricing_schema)
        load_inventory_data(conn, inventory_df_2, inventory_schema)
    
    logger.trace("Data loaded successfully")



if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    data_loader()
	
