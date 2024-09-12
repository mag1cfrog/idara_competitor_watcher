import json
import duckdb
from loguru import logger
from competitor_watcher.utils.db_management import attach_db
from competitor_watcher.utils.email_sender import send_email


def analyze():

    with open("config.json", "r") as f:
        config = json.load(f)

    asin_list = config["competitor_asin_list"]

    droped_messages = []

    with duckdb.connect() as conn:
        conn = attach_db(conn)
        for asin in asin_list:
            sql_query_analysis = f"""
            WITH ranked_over_time AS (SELECT 
                ASIN, 
                CompetitivePrices_Price_LandedPrice_Amount,
                Timestamp,
                ROW_NUMBER() OVER (PARTITION BY ASIN ORDER BY Timestamp DESC) AS rn
            FROM db.item_pricing
            WHERE ASIN = '{asin}')
            SELECT *
            FROM ranked_over_time
            WHERE rn <= 2
            ORDER BY ASIN, Timestamp DESC;
            """
            results = conn.execute(sql_query_analysis).fetchall()

            if len(results) > 1:
                # Compare the last and the second last records
                latest_price = results[0][1]  # Assuming the second column is 'CompetitivePrices_Price_LandedPrice_Amount'
                second_latest_price = results[1][1]
                if latest_price < second_latest_price:
                    logger.info(f"Price dropped for ASIN {asin}: from {second_latest_price:.2f} to {latest_price:.2f}")
                    droped_messages.append(f"Price dropped for ASIN {asin}: from {second_latest_price:.2f} to {latest_price:.2f}")

                else:
                    logger.info(f"No price drop for ASIN {asin}: remains at {latest_price:.2f}")
                    
            elif len(results) == 1:
                logger.info(f"Only one record found for ASIN {asin}")
            else:
                logger.info(f"No records found for ASIN {asin}")

    if droped_messages:
        subject = "Price Drop Alert"
        body = "\n".join(droped_messages)
        to_addr = config["notification_email"]
        from_addr = config["email_sender"]
        send_email(subject, body, to_addr, from_addr)
        logger.info("Email sent successfully!")

if __name__ == "__main__":
    analyze()