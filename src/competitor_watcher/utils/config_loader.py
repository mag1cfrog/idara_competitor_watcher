import os
import json
from loguru import logger

def load_config():
    try:
        json_config_path = os.path.join(os.getcwd(), "config.json")
        logger.debug(f"Loading config from {json_config_path}")
        with open(json_config_path) as f:
                config = json.load(f)
        logger.trace("Config loaded successfully")
        return config
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        raise e