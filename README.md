# Data Platform

A data platform to run:

- airbyte
- postgresql
- clickhouse
- redpanda
- airflow
- metabase

# Prerequisites

- Python
- Pip
- Venv
- Docker + Docker compose

# How to start

```bash
docker compose up
# or (if you want to run the containers as background processes) 
# docker compose up -d
```

# Credential

- Airbyte [http://localhost:8000](http://localhost:8000)
    - User: `airbyte`
    - Password: `admin`
- Airflow [http://localhost:8080](http://localhost:8080)
    - User: `airflow`
    - Password: `admin`
- Metabase [http://localhost:3000](http://localhost:3000)
- Redpanda [http://localhost:8081](http://localhost:8081)
    - User: `redpanda`
    - Password: `admin`
- Postgre `localhost:5432`
    - User: `postgres`
    - Password: `admin`
- Clickhouse: `localhost:8123`
    - User: `clickhouse`
    - Password: `admin`


# Schema

```

┌─────────────────┐                            ┌─────────────────┐
│                 │                            │                 │
│                 │                            │                 │
│   Other Data    ├──────────────┐             │    Metabase     │
│     Sources     │              │             │ (Visualization) │
│                 │              │             │                 │
│                 │              │             │                 │
└─────────────────┘              │             └────────▲────────┘
                                 │                      │
                                 │                      │
┌─────────────────┐     ┌────────▼────────┐    ┌────────┴────────┐
│                 │     │                 │    │                 │
│                 │     │                 │    │                 │
│      OLTP       ├─────►  Extract + Load ├────►      OLAP       │
│    (Postgre)    │     │    (Airbyte)    │    │   (Clickhouse)  │
│                 │     │                 │    │                 │
│                 │     │                 │    │                 │
└─────────────────┘     └────────┬────────┘    └─────┬──────▲────┘
                                 │                   │      │
                                 │                   │      │
                                 │                   │      │
                        ┌────────┴────────┐    ┌─────▼──────┴────┐
                        │                 │    │                 │
                        │                 │    │                 │
                        │  Orchestrator   ├────┤    Transform    │
                        │    (Airflow)    │    │      (DBT)      │
                        │                 │    │                 │
                        │                 │    │                 │
                        └─────────────────┘    └─────────────────┘
```

First, you have OLTP (Online Transaction Processing Database). This is your "day-to-day" transactional database.
You might also have other data sources like google analytics, spreadsheet, or external API.

When you want to do analytics tasks (for example creating monthly reports), you probably need a special type of database. This database is named OLAP (Online Analytical Processing). It is a good practice to separate OLAP from OLTP for some reasons:

- OLAP and OLTP need different technology. You will need a lot of `grouping` operations, and OLAPs are optimized for this use case.
- You want a dedicated resource for your OLTP. You don't want your user experiencing some glitch while you do some analytical processing.

To make your analytical tasks easier, you need to:

- Extract data from your data source (OLTP, spreadsheet, etc)
- Perform transformation (grouping, wrangling, etc)
- Load the data into your OLAP

Those processes are called `ETL (Extract Transform Load)` or `ELT (Extract Load Transform)`, depending on which one you perform first, transformation or loading. 

You also need some kind of orchestrator, so that you can trigger the ETL/ELT process on schedule. Typically people will use airflow, cron, prefect, or similar technology.

In most cases, you will also need to visualize your data. You can use Streamlit, Metabase, Redash, Tableau, Power BI, or similar technology.


# Steps

We will populate Postgre with some voting data, set up Airbyte for extract + load, create a DBT project for transformation, and visualize the data with Metabase.

## Prepare Postgre DB

First, we want to create a table named `voting` and populate it with some data.

- Open `DBeaver` or `psql`
- Run `postgre-voting.sql`

## Setup Airbyte connection

- Create a connection with the following source + destination config:
    - Source (Postgres)
        - Host: `host.docker.internal`
        - Port: `5432`
        - Database Name: `mydb`
        - Username: `postgres`
        - Password: `admin`
    - Destination (Clickhouse)
        - Host: `host.docker.internal`
        - Port: `8123`
        - Database Name: `mydb`
        - Username: `clickhouse`
        - Password (check on "Optional fields"): `admin`
- Set up replication as follow:
    - Sync Mode: `Incremental | Deduped + History`
    - Cursor Field: `vote_time`
    - Primary Key: `id`
- Synchronize the connection, verify that your voting data has been copied to Clickhouse

## Setup DBT

```bash
cd airflow
source prepare.sh

cd dags/dbt_project
dbt run
```

# Troubleshooting

## I messed up with docker's volume, I want to start everything from scratch

```bash
./reset.sh
```

## I have conflicting container names

You can change all containers prefixes by setting `CONTAINER_PREFIX` variable.

```bash
export CONTAINER_PREFIX=alta # Or whatever you like
docker compose up
```

## I have conflicting ports

You can set the following variables:

- `KAFKA_EXTERNAL_HOST_PORT`
- `KAFKA_INTERNAL_HOST_PORT`
- `PANDAPROXY_EXTERNAL_HOST_PORT`
- `PANDAPROXY_INTERNAL_HOST_PORT`
- `REDPANDA_CONSOLE_HOST_PORT`
- `POSTGRES_HOST_PORT`
- `CLICKHOUS_HOST_PORT`
- `METABASE_HOST_PORT`
- `AIRBYTE_PROXY_HOST_PORT`
- `AIRFLOW_HOST_PORT`
- `AIRFLOW_FLOWER_HOST_PORT`
