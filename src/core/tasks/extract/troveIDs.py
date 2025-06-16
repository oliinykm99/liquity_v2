from airflow.exceptions import AirflowException
from src.core.utils.connection import EthereumConnection
from src.core.utils.abi import troveManager, sortedTrove

def fetch_troveIDs(**kwargs):
    endpoints = kwargs['ti'].xcom_pull(task_ids='connect_to_ethereum_task', key='endpoints')
    working_url_index = kwargs['ti'].xcom_pull(task_ids='connect_to_ethereum_task', key='node_url_index')
    block_number = kwargs['ti'].xcom_pull(task_ids='connect_to_ethereum_task', key='return_value')
    eth_conn = EthereumConnection(URLs=endpoints, current_url_index=working_url_index)
    sortedTroves = kwargs['ti'].xcom_pull(task_ids='fetch_troveSizes_task') 


    results = {}
    remaining_pools = list(sortedTroves.keys())
    max_retries = len(endpoints)
    for _ in range(max_retries):
        try:
            w3 = eth_conn.get_connection()
            failed_pools = []

            for pool in remaining_pools:
                try:
                    pool_contract = w3.eth.contract(address=w3.to_checksum_address(pool), abi=sortedTrove)
                    troveManager_address = pool_contract.functions.troveManager().call(block_identifier=block_number)
                    troveManager_contract = w3.eth.contract(address=w3.to_checksum_address(troveManager_address), abi=troveManager)

                    results[troveManager_contract.address] = []
                    for i in range(sortedTroves[pool]):
                        troveID = troveManager_contract.functions.getTroveFromTroveIdsArray(i).call(block_identifier=block_number)
                        results[troveManager_contract.address].append(troveID)

                except Exception:
                    failed_pools.append(pool)                    
        
            if not failed_pools:
                return results
            
            remaining_pools = failed_pools
            eth_conn.rotate_endpoint()
        
        except Exception as e:
            eth_conn.rotate_endpoint()

    raise AirflowException("All RPC endpoints failed or exhausted.")