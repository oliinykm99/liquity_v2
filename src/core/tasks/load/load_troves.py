from src.core.utils.db_manager import DBManager
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DB")

def load_troves(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='aggregate_troves_task')

    db_manager = DBManager(db_url=db_url)
    db_manager.connect()
    db_manager.create_trove_table()
    db_manager.store_trove_data(data)
    db_manager.close()
