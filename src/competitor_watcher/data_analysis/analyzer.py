import json
import duckdb
from loguru import logger
from competitor_watcher.utils.db_management import attach_db


def analyze():

    with open("config.json", "r") as f:
        config = json.load(f)

    asin_list = config["competitor_asin_list"]

    print(asin_list)

    with duckdb.connect() as conn:
        conn = attach_db(conn)
        for asin in asin_list:
            sql_query_analysis = f"""

            """



if __name__ == "__main__":
    analyze()