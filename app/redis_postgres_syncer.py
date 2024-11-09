import logging
import os
import time

import psycopg2
import redis
import schedule
from psycopg2 import OperationalError, sql

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

POSTGRES_SETTINGS = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", 5432)),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

REDIS_SETTINGS = {
    "host": os.getenv("REDIS_HOST", "localhost"),
    "port": int(os.getenv("REDIS_PORT", 6379)),
    "db": 0,
}


def get_postgres_connection():
    """Establish and return a connection to the PostgreSQL database."""
    try:
        return psycopg2.connect(**POSTGRES_SETTINGS)
    except OperationalError as e:
        logging.error(f"PostgreSQL connection error: {e}")
        return None


def fetch_data(cursor):
    """Execute query to fetch data from PostgreSQL and return the results."""
    query = sql.SQL("""
        select c.country,
            count(distinct c.customer_id) users_counts,
            sum(o.amount)                 order_amount
        from public.orders o
                join public.customers c
                    on c.customer_id = o.customer_id
        group by c.country;
    """)
    cursor.execute(query)
    return cursor.fetchall()


def store_data_in_redis(results):
    """Store data in Redis using a pipeline to optimize performance."""
    r = redis.Redis(**REDIS_SETTINGS)
    with r.pipeline() as pipe:
        for country, users_counts, order_amount in results:
            key = f"country:{country}"
            pipe.hset(
                name=key,
                mapping={
                    "users_counts": int(users_counts),
                    "order_amount": float(order_amount),
                },
            )
        pipe.execute()
    logging.info("Data stored in Redis successfully.")


def fetch_and_store_data():
    """Fetch data from PostgreSQL and store it in Redis."""
    conn = get_postgres_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cursor:
            results = fetch_data(cursor)
            store_data_in_redis(results)
    except Exception as e:
        logging.error(f"An error occurred during data fetch/store: {e}")
    finally:
        conn.close()


schedule.every(1).minutes.do(fetch_and_store_data)
logging.info("Scheduler started. Fetching data every 1 minute...")

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
