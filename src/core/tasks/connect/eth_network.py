import os
from dotenv import load_dotenv
from airflow.exceptions import AirflowException
from src.core.utils.connection import EthereumConnection

load_dotenv()
URLS = os.getenv("URLS").split(",") if os.getenv("URLS") else []

eth_conn = EthereumConnection(URLs=URLS)

def connect_to_ethereum(**kwargs):
    try:
        w3 = eth_conn.get_connection()
        
        if not w3.is_connected():
            eth_conn.rotate_endpoint()
            w3 = eth_conn.get_connection()
            
        block_number = w3.eth.block_number
        if not isinstance(block_number, int) or block_number < 0:
            eth_conn.rotate_endpoint()
            raise ValueError("Invalid block number")
        
        kwargs['ti'].xcom_push(key='node_url', value=eth_conn.URLs[eth_conn.current_url_index])
        kwargs['ti'].xcom_push(key='node_url_index', value=eth_conn.current_url_index)
        return block_number

    except ValueError as e:
        eth_conn.rotate_endpoint()
        return connect_to_ethereum(**kwargs)
        
    except Exception as e:
        raise AirflowException(f"All endpoints failed. Last error: {str(e)}")