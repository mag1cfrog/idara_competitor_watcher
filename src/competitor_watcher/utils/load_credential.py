import os

from dotenv import load_dotenv
from loguru import logger

def load_credentials() -> dict:
    """
    Load credentials from .env file
    """
    # Print out current directory
    logger.debug(f"Current directory: {os.getcwd()}")
    try:
        dotenv_path = os.path.join(os.getcwd(), '.env')
        logger.debug(f"Starting to load env virable from .env file: { dotenv_path }")
        load_dotenv(dotenv_path)
        logger.trace("Env virable loaded successfully")
    except Exception as e:
        logger.error(f"Error loading env virable from .env file: {e}")

    if any([os.getenv('sp_api_refresh_token') is None, os.getenv('sp_api_lwa_app_id') is None, os.getenv('sp_api_lwa_client_secret') is None]):
        logger.error("Missing required environment variables")
        raise ValueError("Missing required environment variables")
    else:
        credentials=dict(
                refresh_token=os.getenv('sp_api_refresh_token'),
                lwa_app_id=os.getenv('sp_api_lwa_app_id'),
                lwa_client_secret=os.getenv('sp_api_lwa_client_secret'),
            )
        
    return credentials