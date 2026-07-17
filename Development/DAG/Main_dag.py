from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from datetime import datetime
import requests

# ======================================
# dbt Cloud Details
# ======================================

DBT_ACCOUNT_ID = "70506183148598"
DBT_JOB_ID = "70506183135154"


def trigger_dbt_job():

    conn = BaseHook.get_connection("dbt_cloud")

    token = conn.password
    host = conn.host

    if not host.startswith("http"):
        host = f"https://{host}"

    url = f"{host}/api/v2/accounts/{DBT_ACCOUNT_ID}/jobs/{DBT_JOB_ID}/run/"

    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "cause": "Triggered automatically from Airflow after Databricks Job Success"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to start dbt Job:\n{response.text}")

    print("====================================")
    print("dbt Job Triggered Successfully")
    print(response.json())
    print("====================================")


with DAG(
    dag_id="prod_etl_load",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["Databricks", "dbt", "Energy"],
) as dag:

    # Run Databricks Workflow
    run_databricks = DatabricksRunNowOperator(
        task_id="run_databricks_job",
        databricks_conn_id="databricks_default",
        job_id=709190840874776,
    )

    # Trigger dbt Cloud Job
    run_dbt = PythonOperator(
        task_id="run_dbt_cloud_job",
        python_callable=trigger_dbt_job,
    )

    # Workflow
    run_databricks >> run_dbt