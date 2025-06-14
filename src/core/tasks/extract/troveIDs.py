from airflow.exceptions import AirflowException
from src.core.utils.connection import EthereumConnection
from src.core.utils.abi import troveManager, sortedTrove

def fetch_troveIDs(**kwargs):
    URL = kwargs['ti'].xcom_pull(task_ids='connect_to_ethereum_task', key='node_url')
    sortedTroves = kwargs['ti'].xcom_pull(task_ids='fetch_troveSizes_task') 
    
    eth_conn = EthereumConnection(URLs=[URL])
    w3 = eth_conn.get_connection()

    results = {}
    for pool, trove_count in sortedTroves.items():
        try:
            pool_contract = w3.eth.contract(address=w3.to_checksum_address(pool), abi=sortedTrove)
            troveManager_address = pool_contract.functions.troveManager().call()
            troveManager_contract = w3.eth.contract(address=w3.to_checksum_address(troveManager_address), abi=troveManager)

            results[troveManager_contract.address] = []
            for i in range(trove_count + 1):
                troveID = troveManager_contract.functions.getTroveFromTroveIdsArray(i).call()
                results[troveManager_contract.address].append(troveID)
        
        except Exception as e:
            raise AirflowException(f"Error fetching trove IDs for {pool_contract.address}: {e}")
    
    return results