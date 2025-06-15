from airflow.exceptions import AirflowException
from src.core.utils.connection import EthereumConnection
from src.core.utils.abi import priceFeed
from config import priceFeeds

def fetch_price(**kwargs):
    endpoints = kwargs['ti'].xcom_pull(task_ids='connect_to_ethereum_task', key='endpoints')
    working_url_index = kwargs['ti'].xcom_pull(task_ids='connect_to_ethereum_task', key='node_url_index')
    block_number = kwargs['ti'].xcom_pull(task_ids='connect_to_ethereum_task', key='return_value')
    eth_conn = EthereumConnection(URLs=endpoints, current_url_index=working_url_index)

    results = {}
    remaining_pools = priceFeeds
    max_retries = len(endpoints)
    for _ in range(max_retries):
        try:
            w3 = eth_conn.get_connection()
            failed_pools = []

            for pool in remaining_pools:
                try:
                    contract = w3.eth.contract(address=w3.to_checksum_address(pool), abi=priceFeed)
                    value = contract.functions.lastGoodPrice().call(block_identifier=block_number)

                    if not isinstance(value, int) or value < 0:
                        raise ValueError(f"Invalid value received: {value}")

                    results[contract.address] = value
                
                except Exception:
                    failed_pools.append(pool)
            
            if not failed_pools:
                return results

            remaining_pools = failed_pools
            eth_conn.rotate_endpoint()
        
        except Exception as e:
            eth_conn.rotate_endpoint()

    raise AirflowException("All RPC endpoints failed or exhausted.")