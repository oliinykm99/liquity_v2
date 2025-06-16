from airflow.exceptions import AirflowException
from src.core.utils.connection import EthereumConnection
from src.core.utils.abi import troveManager

def fetch_troveCR(**kwargs):
    endpoints = kwargs['ti'].xcom_pull(task_ids='connect_to_ethereum_task', key='endpoints')
    working_url_index = kwargs['ti'].xcom_pull(task_ids='connect_to_ethereum_task', key='node_url_index')
    block_number = kwargs['ti'].xcom_pull(task_ids='connect_to_ethereum_task', key='return_value')
    troveIDs = kwargs['ti'].xcom_pull(task_ids='fetch_troveIDs_task') 
    prices = kwargs['ti'].xcom_pull(task_ids='fetch_price_task') 
    eth_conn = EthereumConnection(URLs=endpoints, current_url_index=working_url_index)

    results = {}
    remaining_pools = list(troveIDs.keys())
    max_retries = len(endpoints)
    for _ in range(max_retries):
        try:
            w3 = eth_conn.get_connection()
            failed_pools = []

            for pool in remaining_pools:
                try:
                    pool_contract = w3.eth.contract(address=w3.to_checksum_address(pool), abi=troveManager)
                    price_feed_address = list(prices.keys())[list(troveIDs.keys()).index(pool)]

                    if price_feed_address not in prices:
                        raise AirflowException(f"Missing price for price feed {price_feed_address}")
                    
                    price = prices[price_feed_address]
                    results[pool_contract.address] = {}

                    for id in troveIDs[pool]:
                        troveICR = pool_contract.functions.getCurrentICR(id, price).call(block_identifier=block_number)
                        results[pool_contract.address][id] = troveICR

                except Exception:
                    failed_pools.append(pool)

            if not failed_pools:
                return results
            
            remaining_pools = failed_pools
            eth_conn.rotate_endpoint()
        
        except Exception as e:
            eth_conn.rotate_endpoint()
    
    raise AirflowException("All RPC endpoints failed or exhausted.")
