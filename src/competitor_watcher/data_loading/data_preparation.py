
import polars as pl

from competitor_watcher.data_loading.retrieve_competitor_info import retrieve_competitor_info
from competitor_watcher.data_loading.retrieve_inventory import retrieve_inventory
from competitor_watcher.utils.load_credential import load_credentials

def prepare_data(timestamp):

    credentials = load_credentials()

    (
        (item_attribute_df, item_attribute_schema),
        (item_pricing_df, item_pricing_schema)
    ) = retrieve_competitor_info(credentials)


    item_attribute_df = item_attribute_df.with_columns(
        pl.lit(timestamp).str.to_datetime().alias('Timestamp')
    )

    item_attribute_schema += ",\nTimestamp TIMESTAMP WITH TIME ZONE"

    item_pricing_df = item_pricing_df.with_columns(
        pl.lit(timestamp).str.to_datetime().alias('Timestamp')
    )

    item_pricing_schema += ",\nTimestamp TIMESTAMP WITH TIME ZONE"

    # inventory_df, inventory_schema = retrieve_inventory(credentials)

    # inventory_df_2 = inventory_df.with_columns(
    #     pl.lit(timestamp).str.to_datetime().alias('Timestamp')
    # )




    return (
            (item_attribute_df, item_attribute_schema), 
            (item_pricing_df, item_pricing_schema),

        ) 
