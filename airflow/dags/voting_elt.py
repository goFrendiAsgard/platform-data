from __future__ import annotations

import datetime

import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
import os


AIRBYTE_CONN_ID = 'airbyte_voting'
CONNECTION_ID = os.getenv('VOTING_AIRBYTE_CONNECTION_ID', 'aad992b4-e014-4854-955e-2e65ddf3f051')

with DAG(
    dag_id='voting_elt',
    schedule='0 0 * * *',
    start_date=pendulum.datetime(2021, 1, 1, tz='UTC'),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=['example', 'example2'],
    params={'example_key': 'example_value'},
) as dag:
    # https://docs.airbyte.com/operator-guides/using-the-airflow-airbyte-operator/
    sync_voting = AirbyteTriggerSyncOperator(
        task_id='sync_voting',
        airbyte_conn_id=AIRBYTE_CONN_ID,
        connection_id=CONNECTION_ID,
        asynchronous=False,
        timeout=3600,
        wait_seconds=3
    )

    transform = BashOperator(
        task_id='transform',
        bash_command=' && '.join([
            'export CLICKHOUSE_HOST=host.docker.internal',
            'cd /opt/airflow/dags',
            'source prepare.sh', 
            'cd dbt_project', 
            'dbt run && dbt test',
        ]) 
    )

    sync_voting >> transform

if __name__ == '__main__':
    dag.test()