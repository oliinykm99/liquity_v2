from src.core.utils.db_manager import DBManager
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DB")

def load(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='aggregate_pools_task')

    db_manager = DBManager(db_url=db_url)
    db_manager.connect()
    db_manager.create_table()
    db_manager.store_liquity_data(data)
    db_manager.close()
