import os
import time
from decimal import Decimal

import psycopg2
import redis
import schedule

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = 0


def get_postgres_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )


def fetch_data(cursor):
    query = """
        select c.country,
            count(distinct c.customer_id) users_counts,
            sum(o.amount)                 order_amount
        from public.orders o
                join public.customers c
                    on c.customer_id = o.customer_id
        group by c.country;
    """
    cursor.execute(query)
    return cursor.fetchall()


def store_data_in_redis(results):
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    for country, users_counts, order_amount in results:
        key = f"country:{country}"
        r.hset(
            name=key,
            mapping={
                "users_counts": users_counts,
                "order_amount": float(order_amount)
                if isinstance(order_amount, Decimal)
                else order_amount,
            },
        )
    print("Data stored in Redis successfully.")


def fetch_and_store_data():
    cursor = None
    conn = None
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        results = fetch_data(cursor)
        store_data_in_redis(results)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


schedule.every(1).minutes.do(fetch_and_store_data)

print("Scheduler started. Fetching data every 1 minute...")

while True:
    schedule.run_pending()
    time.sleep(1)
