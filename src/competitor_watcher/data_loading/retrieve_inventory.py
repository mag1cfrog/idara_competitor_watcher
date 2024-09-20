import os

from dotenv import load_dotenv
from sp_api.api import Inventories
import polars as pl

from competitor_watcher.data_loading.transform_raw_data import transform_pl_df_and_generate_schema
from competitor_watcher.utils import config_loader


def retrieve_inventory(credentials: dict):
    load_dotenv()
    os.environ['ENV_DISABLE_DONATION_MSG'] = '1'

    inventory_client = Inventories(
        credentials=credentials
    )

    res = inventory_client.get_inventory_summary_marketplace(**{
        'details': True,
    }
    )

    df = pl.DataFrame(res()).unnest(
        "granularity", "inventorySummaries"
        ).unnest(
            "inventoryDetails"
            ).unnest(
                "reservedQuantity", "researchingQuantity", "unfulfillableQuantity", "futureSupplyQuantity"
                )
    


    config = config_loader.load_config()

    own_asin_list = set(asin for asin in config['competitor_asin_dict'].keys())

    # Cast lastUpdatedTime to datetime
    df = df.with_columns(
        pl.col("lastUpdatedTime").str.to_datetime(strict=False)
        )

    df = df.filter(
        (pl.col("asin").is_in(own_asin_list)) & 
        (pl.col("lastUpdatedTime").is_not_null())
        )
    
    # For each ASIN, should only have one row with the most recent lastUpdatedTime
    df = df.sort("lastUpdatedTime", descending=True).unique(subset=["asin"], keep="first")

    return transform_pl_df_and_generate_schema(df)
