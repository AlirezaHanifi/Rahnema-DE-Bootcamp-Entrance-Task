# Rahnema College Data Engineering Bootcamp Entrance Task

## Question 1

## Section 1: Project Overview

This project is containerized using Docker Compose, with configurations defined in `compose.yaml`.
The project structure is organized as follows:

```bash
├── Chalenge-Data Engineering.pdf      # Task instructions in PDF format.
├── README.md                          # Project overview and setup instructions.                  
├── app                                # Source code and dependencies for syncing PostgreSQL data into Redis.
│   ├── Dockerfile                    
│   ├── redis_postgres_syncer.py       
│   └── requirements.txt               
├── compose.yaml                       # Docker Compose configuration for PostgreSQL, Redis, and syncer.
├── data
│   ├── pg                            
│   │   ├── data                       # PostgreSQL data volume for Docker.
│   │   ├── init                       
│   │   │   └── importing_data.sql     # SQL script to set up PostgreSQL tables and load data.
│   │   └── init-data                  
│   │       ├── customers.csv          # CSV file with customer data for PostgreSQL.
│   │       └── orders.csv             # CSV file with order data for PostgreSQL.
│   └── redis                          # Redis data volume for Docker.
└── queries
    └── solution.sql                   # SQL queries for solving the tasks.
```

- To configure environment variables, rename `.env.example` to `.env`.

### Section 2: Data Import and Table Setup

The [`importing_data.sql`](data/pg/init/importing_data.sql) script in the `data/pg/init/` folder creates the
necessary tables and imports data from the `customers.csv` and `orders.csv` files into the
PostgreSQL database.

### Section 3: Strategies for Efficient Data Loading

In case, the data size increases significantly, we can opt for the following strategies for bringing
in the data efficiently:

1. File Splitting and Parallelization
   - Split large files into smaller parts for parallel processing.
   - Use Airflow to orchestrate parallel COPY commands for each part.
2. Staging Tables
   - Load data quickly into staging tables without indexes or constraints.
3. Index Management
   - Temporarily disable indexes and constraints before loading data:

### Section 4 to 7: Query Solutions

The SQL solutions for sections 4 to 7 are stored in [`queries/solution.sql`](queries/solution.sql).

## Question 2: Data Transfer Between PostgreSQL and Redis

To improve the process of transferring data from PostgreSQL to Redis, we can consider these optimizations:

1. Automated Scheduling with Airflow
   - Automate the data transfer process using an Airflow DAG to periodically fetch data from PostgreSQL and load it into Redis. This approach enables scheduling, retries, and monitoring.
2. Incremental Data Fetching
   - Implement incremental data loading by querying only new or modified records, tracked by timestamps. Store the last processed timestamp in Redis to ensure only necessary data is transferred.
