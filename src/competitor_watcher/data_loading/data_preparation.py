from competitor_watcher.data_loading.transform_raw_data import unnest_and_explode
import polars as pl

def prepare_data(timestamp, competitor_item_attribute, competitor_item_pricing):
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
    return item_attribute_df, item_pricing_df
