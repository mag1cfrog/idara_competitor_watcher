import os
from datetime import datetime

from dotenv import load_dotenv
from loguru import logger
import polars as pl

from sp_api.api import Catalog
from sp_api.api import Products
from sp_api.base import Marketplaces
from competitor_watcher.data_loading.transform_raw_data import unnest_and_explode, transform_pl_df_and_generate_schema
from competitor_watcher.utils.config_loader import load_config




def get_competitor_info(asin_list: list, credentials: dict):
    logger.trace("Retrieving competitor information")
    os.environ['ENV_DISABLE_DONATION_MSG'] = '1'

    catalog_client = Catalog(
        credentials=credentials
    )

    product_client = Products(
        credentials=credentials,
        marketplace=Marketplaces.US
    )
    try:
        # Get competitor's asin item attribute    
        competitor_item_attribute = get_competitor_item_attribute(asin_list, catalog_client)
        
        # Get competitor's asin item pricing
        competitor_item_pricing = get_competitor_item_pricing(asin_list, product_client)
    except Exception as e:
        logger.error(f"Error: {e}")
    else:
        logger.trace("Competitor information retrieved")

    return competitor_item_attribute, competitor_item_pricing
    


def get_competitor_item_attribute(asin_list: list, catalog_client: object):
    total_item_attributes = []
    for asin in asin_list:
        response = catalog_client.get_item(
            MarketplaceId="ATVPDKIKX0DER",
            asin=asin
        )
        total_item_attributes.append(response())
    
    return total_item_attributes


def get_competitor_item_pricing(asin_list: list, product_client: object):

    response = product_client.get_competitive_pricing_for_asins(
        asin_list=asin_list
    )
    
    return response()


def retrieve_competitor_info(credentials: dict):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger.add(f"log/file_{timestamp}.log", rotation="10 MB")

    config = load_config()

    asin_list = set(asin for sublist in config['competitor_asin_dict'].values() for asin in sublist)

    competitor_item_attribute, competitor_item_pricing = get_competitor_info(asin_list, credentials)


    item_attribute_df = unnest_and_explode(
        pl.DataFrame(competitor_item_attribute)
    )

    item_pricing_df = unnest_and_explode(
        pl.DataFrame(competitor_item_pricing).unnest('Product').unnest('CompetitivePricing')
    )

    item_attribute_df_2, item_attribute_schema = transform_pl_df_and_generate_schema(item_attribute_df)
    item_pricing_df_2, item_pricing_schema = transform_pl_df_and_generate_schema(item_pricing_df)

    return (
        (item_attribute_df_2, item_attribute_schema),
        (item_pricing_df_2, item_pricing_schema)
    )


    