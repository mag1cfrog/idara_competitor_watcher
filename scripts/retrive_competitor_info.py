import os
import json
from datetime import datetime
from loguru import logger
from dotenv import load_dotenv

def get_competitor_info():
    logger.info("Retrieving competitor information")
    credentials = {
        "username": os.getenv("COMPETITOR_USERNAME"),
        "password": os.getenv("COMPETITOR_PASSWORD"),
    }
    logger.info("Competitor information retrieved")


def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger.add(f"log/file_{timestamp}.log", rotation="10 MB")
    load_dotenv()
    with open("config.json") as f:
        config = json.load(f)
    print(config['competitor_asin_list'], type(config['competitor_asin_list']))


if __name__ == "__main__":
    main()
    