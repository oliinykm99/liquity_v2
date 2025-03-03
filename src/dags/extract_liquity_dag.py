from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from src.core.extract_activeTVL import fetch_activeTVL
from src.core.extract_activeDEBT import fetch_activeDEBT
from src.core.extract_price import fetch_price
from src.core.extract_stabilityTVL import fetch_stabilityTVL

default_args = {
    "owner": "admin",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 3),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    dag_id="extract_liquity_dag",
    default_args=default_args,
    description="Fetch Liquity",
    schedule_interval=timedelta(minutes=30),
    catchup=False
)

fetch_ActiveTVL_task = PythonOperator(
    task_id = "fetch_ActiveTVL_task",
    python_callable=fetch_activeTVL,
    dag=dag,
)

fetch_activeDEBT_task = PythonOperator(
    task_id = 'fetch_activeDEBT_task',
    python_callable=fetch_activeDEBT,
    dag=dag,
)

fetch_price_task = PythonOperator(
    task_id = 'fetch_price_task',
    python_callable=fetch_price,
    dag=dag,
)

fetch_stabilityTVL_task = PythonOperator(
    task_id = 'fetch_stabilityTVL_task',
    python_callable=fetch_stabilityTVL,
    dag=dag,
)