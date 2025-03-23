from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta

from src.core.tasks.connect import connect_to_ethereum
from src.core.tasks.extract import (fetch_troveSizes, fetch_troveIDs, fetch_troveOwner, 
                                    fetch_price, fetch_troveCR, fetch_troveData,
                                    extract_requiredTroveData)
from src.core.tasks.clean import (clean_troveCR, clean_troveRequiredData)
from src.core.tasks.aggregate import aggregate_troves

default_args = {
    "owner": "admin",
    "retries": 2,
    "retry_delay": timedelta(seconds=15)
}

dag = DAG(
    dag_id="extract_troves_dag",
    default_args=default_args,
    description="Fetch Liquity V2 Troves",
    schedule_interval=None,
    catchup=False
)

connect_to_ethereum_task = PythonOperator(
    task_id = "connect_to_ethereum_task",
    python_callable=connect_to_ethereum,
    dag=dag,
)

fetch_troveSizes_task = PythonOperator(
    task_id = "fetch_troveSizes_task",
    python_callable=fetch_troveSizes,
    dag=dag, 
)

fetch_troveIDs_task = PythonOperator(
    task_id = "fetch_troveIDs_task",
    python_callable=fetch_troveIDs,
    dag=dag,
)

fetch_troveOwner_task = PythonOperator(
    task_id = "fetch_troveOwner_task",
    python_callable=fetch_troveOwner,
    dag=dag,
)

fetch_troveCR_task = PythonOperator(
    task_id = "fetch_troveCR_task",
    python_callable=fetch_troveCR,
    dag=dag,
)

fetch_price_task = PythonOperator(
    task_id = "fetch_price_task",
    python_callable=fetch_price,
    dag=dag,
)

fetch_troveData_task = PythonOperator(
    task_id = "fetch_troveData_task",
    python_callable=fetch_troveData,
    dag=dag
)

extract_requiredTroveData_task = PythonOperator(
    task_id = "extract_requiredTroveData_task",
    python_callable=extract_requiredTroveData,
    dag=dag,
)

clean_troveCR_task = PythonOperator(
    task_id = "clean_troveCR_task",
    python_callable=clean_troveCR,
    dag=dag,
)

clean_troveRequiredData_task = PythonOperator(
    task_id = "clean_troveRequiredData_task",
    python_callable=clean_troveRequiredData,
    dag=dag,
)

aggregate_troves_task = PythonOperator(
    task_id = "aggregate_troves_task",
    python_callable=aggregate_troves,
    dag=dag,
)


connect_to_ethereum_task >> fetch_troveSizes_task >> fetch_troveIDs_task
connect_to_ethereum_task >> fetch_price_task
fetch_troveIDs_task >> fetch_troveOwner_task
[fetch_price_task, fetch_troveIDs_task] >> fetch_troveCR_task >> clean_troveCR_task
fetch_troveIDs_task >> fetch_troveData_task >> extract_requiredTroveData_task >> clean_troveRequiredData_task
[fetch_troveOwner_task, clean_troveCR_task, clean_troveRequiredData_task] >> aggregate_troves_task