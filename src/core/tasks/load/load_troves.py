import os
from airflow.exceptions import AirflowException
from src.core.utils.db_manager import DBManager
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DB")

def load_troves(**kwargs):
    data = kwargs['ti'].xcom_pull(task_ids='aggregate_troves_task')
    if data is None:
        raise AirflowException("No data found in XCom from 'aggregate_pools_task'. Ensure the upstream task succeeded.")

    db_manager = DBManager(db_url=db_url)

    try:
        db_manager.connect()
        db_manager.create_trove_table()
        db_manager.store_trove_data(data)
    except Exception as e:
        raise AirflowException(f"Database operation failed: {e}")
    finally:
        db_manager.close()
