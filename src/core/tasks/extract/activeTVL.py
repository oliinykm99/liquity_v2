from src.core.utils.connection import EthereumConnection
from src.core.utils.abi import activePool
from config import activePools

def fetch_activeTVL(**kwargs):
    ti = kwargs['ti']
    URL = ti.xcom_pull(task_ids='connect_to_ethereum_task')
    eth_conn = EthereumConnection(URL=URL)
    w3 = eth_conn.get_connection()
    
    results = {}
    for pool in activePools:
        try:
            pool_contract = w3.eth.contract(address=w3.to_checksum_address(pool), abi=activePool)
            value = pool_contract.functions.getCollBalance().call()
            results[pool] = value
        except Exception as e:
            print(f"Error fetching TVL for {pool}: {e}")
    return results