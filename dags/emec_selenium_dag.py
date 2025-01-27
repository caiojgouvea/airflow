from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../scripts"))
from web_scrap_emec import main as run_selenium_script

default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 10, 1),
    "retries": 1,
}

dag = DAG(
    "emec_web_scrap",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
)

task = PythonOperator(
    task_id="run_selenium_script",
    python_callable=run_selenium_script,
    dag=dag,
)
