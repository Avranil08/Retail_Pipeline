from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os

# Add project path
sys.path.append("/opt/airflow/project")

from main import run_pipeline


def run_etl():
    run_pipeline()


with DAG(
    dag_id="retail_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    task = PythonOperator(
        task_id="run_retail_etl",
        python_callable=run_etl
    )

    task