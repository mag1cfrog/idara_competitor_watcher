
import polars as pl

from competitor_watcher.data_loading.transform_raw_data import unnest_and_explode
from competitor_watcher.data_loading.retrieve_competitor_info import retrieve_competitor_info
from competitor_watcher.data_loading.transform_raw_data import transform_pl_df_and_generate_schema

def prepare_data(timestamp):

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

    return (
            (item_attribute_df_2, item_attribute_schema), 
            (item_pricing_df_2, item_pricing_schema),

        ) 
