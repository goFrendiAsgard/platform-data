#!/bin/bash

if [ ! -d ".venv" ]
then
    python -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt

# Set DBT profile directory.
# Alternatively, you can pass --dbt-profiles-dir argument:
# dbt run --profiles-dir ../dbt_profile
export DBT_PROFILES_DIR=$(realpath ./dbt_profile)
