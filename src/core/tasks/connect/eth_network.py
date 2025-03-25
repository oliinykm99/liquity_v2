import os
from dotenv import load_dotenv
from airflow.exceptions import AirflowException
from src.core.utils.connection import EthereumConnection

load_dotenv()
URL = os.getenv("URL")

eth_conn = EthereumConnection(URL=URL)
w3 = eth_conn.get_connection()

def connect_to_ethereum(**kwargs):
    try:
        if not w3:
            raise AirflowException('Web3 instance is not initialized.')
        
        if not w3.is_connected():
            raise AirflowException('Failed to connect to Ethereum network.')
        
        block_number = w3.eth.block_number
        if not isinstance(block_number, int) or block_number < 0:
            raise AirflowException(f"Invalid block number received: {block_number}")
        
        kwargs['ti'].xcom_push(key='node_url', value=URL)
        return block_number

    except Exception as e:
        raise AirflowException(f"Error: {e}")