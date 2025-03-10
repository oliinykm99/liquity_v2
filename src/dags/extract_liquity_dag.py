from airflow import DAG
from airflow.operators.python import PythonOperator

from src.core.tasks.connect import connect_to_ethereum
from src.core.tasks.extract import (fetch_stabilityTVL, fetch_activeDEBT,
                                    fetch_activeTVL, fetch_price)
from src.core.tasks.clean import (clean_stabilityTVL, clean_prices,
                                  clean_activeDEBT)

default_args = {
    "owner": "admin",
    "retries": 1,
}

dag = DAG(
    dag_id="extract_liquity_dag",
    default_args=default_args,
    description="Fetch Liquity",
    schedule_interval=None,
    catchup=False
)

connect_to_ethereum_task = PythonOperator(
    task_id = "connect_to_ethereum_task",
    python_callable=connect_to_ethereum,
    dag=dag,
)

fetch_ActiveTVL_task = PythonOperator(
    task_id = "fetch_activeTVL_task",
    python_callable=fetch_activeTVL,
    dag=dag,
)

fetch_activeDEBT_task = PythonOperator(
    task_id = 'fetch_activeDEBT_task',
    python_callable=fetch_activeDEBT,
    dag=dag,
)

fetch_stabilityTVL_task = PythonOperator(
    task_id = 'fetch_stabilityTVL_task',
    python_callable=fetch_stabilityTVL,
    dag=dag,
)

fetch_price_task = PythonOperator(
    task_id = 'fetch_price_task',
    python_callable=fetch_price,
    dag=dag,
)

clean_stabilityTVL_task = PythonOperator(
    task_id = 'clean_stabilityTVL_task',
    python_callable=clean_stabilityTVL,
    dag=dag,
)

clean_prices_task = PythonOperator(
    task_id = 'clean_prices_task',
    python_callable=clean_prices,
    dag=dag,
)

clean_activeDEBT_task = PythonOperator(
    task_id = 'clean_activeDEBT_task',
    python_callable=clean_activeDEBT,
    dag=dag,
)



connect_to_ethereum_task >> [fetch_activeDEBT_task, fetch_ActiveTVL_task, fetch_stabilityTVL_task, fetch_price_task]
fetch_stabilityTVL_task >> clean_stabilityTVL_task
fetch_price_task >> clean_prices_task
fetch_activeDEBT_task >> clean_activeDEBT_task