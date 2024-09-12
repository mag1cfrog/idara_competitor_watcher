import os
from datetime import datetime
import duckdb
import polars as pl
from loguru import logger
from dotenv import load_dotenv
from competitor_watcher.data_loading.retrieve_competitor_info import main as retrieve_competitor_info
from competitor_watcher.data_loading.transform_raw_data import unnest_and_explode, transform_pl_df_and_generate_schema
from competitor_watcher.utils.db_management import attach_db




def load_attribute_data(conn: duckdb.DuckDBPyConnection, item_attribute_df_2: pl.DataFrame, item_attribute_schema: str) -> None:
    sql_query_create_table_item_attribute = f"""
    CREATE TABLE IF NOT EXISTS db.item_attribute (
        {item_attribute_schema}
    );
    """


    sql_query_insert_data_item_attribute = f"""
    INSERT INTO db.item_attribute
    SELECT *
    FROM item_attribute_df_2 t
    WHERE NOT EXISTS (
        SELECT 1
        FROM db.item_attribute i
        WHERE i.Identifiers_MarketplaceASIN_ASIN = t.Identifiers_MarketplaceASIN_ASIN
        AND i.Timestamp = t.Timestamp
    );
    """

    conn.execute(sql_query_create_table_item_attribute)

    conn.execute(sql_query_insert_data_item_attribute)


def load_pricing_data(conn: duckdb.DuckDBPyConnection, item_pricing_df_2: pl.DataFrame, item_pricing_schema: str) -> None:
    
    sql_query_cerate_table_item_pricing = f"""
    CREATE TABLE IF NOT EXISTS db.item_pricing (
        {item_pricing_schema}
    );
    """

    sql_query_insert_data_item_pricing = f"""
    INSERT INTO db.item_pricing
    SELECT *
    FROM item_pricing_df_2 t
    WHERE NOT EXISTS (
        SELECT 1
        FROM db.item_pricing i
        WHERE i.ASIN = t.ASIN
        AND i.Timestamp = t.Timestamp
        AND i.CompetitivePrices_condition = t.CompetitivePrices_condition
    );
    """

    conn.execute(sql_query_cerate_table_item_pricing)

    conn.execute(sql_query_insert_data_item_pricing)



def data_loader():

    load_dotenv()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    competitor_item_attribute, competitor_item_pricing = retrieve_competitor_info()
    item_attribute_df = unnest_and_explode(
          pl.DataFrame(competitor_item_attribute)
        ).with_columns(
              pl.lit(timestamp).str.to_datetime().alias('Timestamp')
            )

    item_pricing_df = unnest_and_explode(
          pl.DataFrame(competitor_item_pricing).unnest('Product').unnest('CompetitivePricing')
        ).with_columns(
              pl.lit(timestamp).str.to_datetime().alias('Timestamp')
            )
    item_attribute_df_2, item_attribute_schema = transform_pl_df_and_generate_schema(item_attribute_df)
    item_pricing_df_2, item_pricing_schema = transform_pl_df_and_generate_schema(item_pricing_df)

    with duckdb.connect() as conn:
        conn = attach_db(conn)

        load_attribute_data(conn, item_attribute_df_2, item_attribute_schema)
        load_pricing_data(conn, item_pricing_df_2, item_pricing_schema)
    
    print("Data loaded successfully")

    return timestamp


if __name__ == "__main__":
	data_loader()
	
