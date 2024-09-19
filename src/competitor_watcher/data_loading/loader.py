import sys

import duckdb
from loguru import logger
import polars as pl

from competitor_watcher.data_loading.retrieve_competitor_info import main as retrieve_competitor_info
from competitor_watcher.data_loading.transform_raw_data import transform_pl_df_and_generate_schema
from competitor_watcher.data_loading.data_preparation import prepare_data
from competitor_watcher.utils.db_management import attach_db
from competitor_watcher.utils.db_operations import create_table, insert_data
from competitor_watcher.utils.time_utils import get_current_timestamp


def load_attribute_data(conn: duckdb.DuckDBPyConnection, df: pl.DataFrame, schema: str) -> None:
    create_table(conn, 'db.item_attribute', schema)
    insert_data(conn, 'db.item_attribute', df, 'df', ['Identifiers_MarketplaceASIN_ASIN', 'Timestamp'])
    


def load_pricing_data(conn: duckdb.DuckDBPyConnection, df: pl.DataFrame, schema: str) -> None:
    create_table(conn, 'db.item_pricing', schema)
    insert_data(conn, 'db.item_pricing', df, 'df', ['ASIN', 'Timestamp', 'CompetitivePrices_condition'])


def data_loader():

    timestamp = get_current_timestamp()

    competitor_item_attribute, competitor_item_pricing = retrieve_competitor_info()
    item_attribute_df, item_pricing_df = prepare_data(timestamp, competitor_item_attribute, competitor_item_pricing)

    item_attribute_df_2, item_attribute_schema = transform_pl_df_and_generate_schema(item_attribute_df)

    item_pricing_df_2, item_pricing_schema = transform_pl_df_and_generate_schema(item_pricing_df)

    with duckdb.connect() as conn:
        conn = attach_db(conn)

        load_attribute_data(conn, item_attribute_df_2, item_attribute_schema)
        load_pricing_data(conn, item_pricing_df_2, item_pricing_schema)
    
    logger.info("Data loaded successfully")



if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    data_loader()
	
