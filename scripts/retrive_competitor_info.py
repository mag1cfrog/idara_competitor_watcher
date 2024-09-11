import os
import json
from datetime import datetime
from loguru import logger
from dotenv import load_dotenv
from sp_api.api import Catalog
from sp_api.api import Products
from sp_api.base import Marketplaces



def get_competitor_info(asin_list: list, credentials: dict):
    logger.info("Retrieving competitor information")
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
        logger.info("Competitor information retrieved")

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


def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger.add(f"log/file_{timestamp}.log", rotation="10 MB")

    load_dotenv()

    credentials=dict(
            refresh_token=os.getenv('sp_api_refresh_token'),
            lwa_app_id=os.getenv('sp_api_lwa_app_id'),
            lwa_client_secret=os.getenv('sp_api_lwa_client_secret'),
        )
    
    with open("config.json") as f:
        config = json.load(f)

    asin_list = config['competitor_asin_list']

    competitor_item_attribute, competitor_item_pricing = get_competitor_info(asin_list, credentials)

    return competitor_item_attribute, competitor_item_pricing


if __name__ == "__main__":
    main()
    