# Rahnema College Data Engineering Bootcamp Entrance Task

## Question 1

## Section 1: Project Overview

This project is containerized using Docker Compose, with configurations defined in `compose.yaml`.
The project structure is organized as follows:

```bash
├── Chalenge-Data Engineering.pdf
├── README.md
├── app
│   ├── Dockerfile
│   ├── redis_postgres_syncer.py
│   └── requirements.txt
├── compose.yaml
├── pg
│   ├── data
│   ├── init
│   │   └── importing_data.sql
│   └── init-data
│       ├── customers.csv
│       └── orders.csv
└── queries
    └── solution.sql
```

- `redis_postgres_syncer.py` contains the logic for data transfer from PostgreSQL to Redis.
- SQL and CSVs are used to initialize data in PostgreSQL.
- To configure environment variables, rename `.env.example` to `.env`.

### Section 2: Data Import and Table Setup

The [`importing_data.sql`](pg/init/importing_data.sql) script in the `pg/init` folder creates the
necessary tables and imports data from the `customers.csv` and `orders.csv` files into the
PostgreSQL database.

### Section 3: Strategies for Efficient Data Loading

In case, the data size increases significantly, we can opt for the following strategies for bringing
in the data efficiently:

1. File Splitting and Parallelization
   - Split large files into smaller parts for parallel processing.
   - Use Airflow to orchestrate parallel COPY commands for each part, with a DAG managing task dependencies.
2. Staging Tables
   - Load data quickly into staging tables without indexes or constraints.
3. Index Management
   - Temporarily disable indexes and constraints before loading data:
4. Batch Processing with Airflow
   - Divide data into batches and load each batch iteratively.
   - Use Airflow to manage batches in sequence and retry failed loads.

### Section 4 to 7: Query Solutions

The SQL solutions for sections 4 to 7 are stored in [`queries/solution.sql`](queries/solution.sql).

## Question 2: Data Transfer Between PostgreSQL and Redis

To improve the process of transferring data from PostgreSQL to Redis, consider these optimizations:

1. Automated Scheduling with Airflow
   - Automate the data transfer process using an Airflow DAG to periodically fetch data from PostgreSQL and load it into Redis. This approach enables scheduling, retries, and monitoring.
2. Incremental Data Fetching
   - Implement incremental data loading by querying only new or modified records, tracked by timestamps. Store the last processed timestamp in Redis to ensure only necessary data is transferred.
