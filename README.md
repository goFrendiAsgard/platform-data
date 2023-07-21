# Platform Data

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