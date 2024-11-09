CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    country VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date TIMESTAMP,
    amount DECIMAL(10, 2)
);

COPY customers(customer_id, customer_name, country) 
FROM '/data/customers.csv' 
DELIMITER ',' 
CSV HEADER;

COPY orders(order_id, customer_id, order_date, amount) 
FROM '/data/orders.csv' 
DELIMITER ',' 
CSV HEADER;