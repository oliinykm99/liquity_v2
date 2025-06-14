import os
from dotenv import load_dotenv
from airflow.exceptions import AirflowException
from src.core.utils.connection import EthereumConnection

load_dotenv()
URLS = os.getenv("URLS").split(",") if os.getenv("URLS") else []

eth_conn = EthereumConnection(URLs=URLS)

def connect_to_ethereum(**kwargs):
    failed_endpoints = set()
    
    for _ in range(len(eth_conn.URLs)):
        try:
            w3 = eth_conn.get_connection()

            if not w3.is_connected():
                failed_endpoints.append(eth_conn.URLs[eth_conn.current_url_index])
                eth_conn.rotate_endpoint()
                continue

            block_number = w3.eth.block_number
            if not isinstance(block_number, int) or block_number < 0:
                failed_endpoints.append(eth_conn.URLs[eth_conn.current_url_index])
                eth_conn.rotate_endpoint()
                continue

            kwargs['ti'].xcom_push(key='node_url', value=eth_conn.URLs[eth_conn.current_url_index])
            kwargs['ti'].xcom_push(key='node_url_index', value=eth_conn.current_url_index)
            if failed_endpoints:
                kwargs['ti'].xcom_push(key='failed_endpoints', value=failed_endpoints)

            return block_number

        except Exception:
            failed_endpoints.append(eth_conn.URLs[eth_conn.current_url_index])
            eth_conn.rotate_endpoint()
            continue

    raise AirflowException(f"All endpoints failed. Failed URLs: {failed_endpoints}")