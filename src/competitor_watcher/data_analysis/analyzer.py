import json
import duckdb
from loguru import logger
from competitor_watcher.utils.db_management import attach_db
from competitor_watcher.utils.email_sender import send_email
from competitor_watcher.utils.config_loader import load_config


def analyze():

    
    config = load_config()

    asin_list = config["competitor_asin_list"]

    dropped_messages = []

    with duckdb.connect() as conn:
        conn = attach_db(conn)
        for asin in asin_list:
            sql_query_analysis = f"""
            WITH ranked_over_time AS (SELECT 
                ASIN, 
                CompetitivePrices_subcondition,
                CompetitivePrices_Price_LandedPrice_Amount,
                Timestamp,
                ROW_NUMBER() OVER (PARTITION BY ASIN, CompetitivePrices_subcondition ORDER BY Timestamp DESC) AS rn
            FROM db.item_pricing
            WHERE ASIN = '{asin}')
            SELECT *
            FROM ranked_over_time
            WHERE rn <= 2
            ORDER BY ASIN, Timestamp DESC;
            """
            results = conn.execute(sql_query_analysis).fetchall()

            prices = {}

            for result in results:
                asin, condition, price, _, rn = result
                if (asin, condition) not in prices:
                    prices[(asin, condition)] = [None, None]  # [latest_price, second_latest_price]
                if rn == 1:
                    prices[(asin, condition)][0] = price
                elif rn == 2:
                    prices[(asin, condition)][1] = price

            # Now check for price drops
            for (asin, condition), (latest_price, second_latest_price) in prices.items():
                if None not in (latest_price, second_latest_price):  # Ensure both prices are available
                    if latest_price < second_latest_price:
                        message = f"Price dropped for ASIN {asin} with condition '{condition}': from {second_latest_price:.2f} to {latest_price:.2f}"
                        logger.info(message)
                        dropped_messages.append(message)
                    else:
                        logger.info(f"No price drop for ASIN {asin} with condition '{condition}': remains at {latest_price:.2f}")
                elif latest_price is not None:
                    logger.info(f"Only one record found for ASIN {asin} with condition '{condition}'")

    if dropped_messages:
        subject = "Price Drop Alert"
        body = "\n".join(dropped_messages)
        to_addr = config["notification_email"]
        from_addr = config["email_sender"]
        send_email(subject, body, to_addr, from_addr)
        logger.info("Email sent successfully!")

if __name__ == "__main__":
    analyze()