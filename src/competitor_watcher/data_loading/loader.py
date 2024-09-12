import os
import duckdb
from dotenv import load_dotenv


load_dotenv()

sql_query_attach_db = f"""
LOAD postgres;

CREATE SECRET postgres_secret_one (
	TYPE POSTGRES,
	HOST '{os.getenv('POSTGRES_HOST')}',
    PORT 5432,
	DATABASE {os.getenv('POSTGRES_DBNAME')},
    USER 'postgres',
	PASSWORD '{os.getenv('POSTGRES_PASSWORD')}'
);

ATTACH '' AS db (TYPE POSTGRES, SECRET postgres_secret_one);

"""
