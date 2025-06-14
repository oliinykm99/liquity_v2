import os
from dotenv import load_dotenv
from airflow.exceptions import AirflowException
from src.core.utils.connection import EthereumConnection

load_dotenv()
URLS = os.getenv("URLS").split(",") if os.getenv("URLS") else []

def connect_to_ethereum(**kwargs):
    try:
        eth_conn = EthereumConnection(URLs=URLS)
        w3 = eth_conn.get_connection()

        block_number = w3.eth.block_number
        
        kwargs['ti'].xcom_push(key='node_url', value=eth_conn.URLs[eth_conn.current_url_index])
        kwargs['ti'].xcom_push(key='node_url_index', value=eth_conn.current_url_index)
        kwargs['ti'].xcom_push(key='failed_endpoints', value=eth_conn.get_failed_endpoints())

        return block_number

    except Exception as e:
        raise AirflowException(f"Failed to connect to Ethereum RPC. Error: {str(e)}")