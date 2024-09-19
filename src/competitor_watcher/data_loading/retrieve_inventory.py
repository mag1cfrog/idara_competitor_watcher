import os

from dotenv import load_dotenv
from sp_api.api import Inventories
import polars as pl


def get_inventory(credentials: dict):
    credentials=dict(
                refresh_token=os.getenv('sp_api_refresh_token'),
                lwa_app_id=os.getenv('sp_api_lwa_app_id'),
                lwa_client_secret=os.getenv('sp_api_lwa_client_secret'),
            )

    os.environ['ENV_DISABLE_DONATION_MSG'] = '1'