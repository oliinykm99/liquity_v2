from src.core.utils.connection import EthereumConnection
from src.core.utils.abi import sortedTrove
from config import sortedTroves

def fetch_troveSizes(**kwargs):
    URL = kwargs['ti'].xcom_pull(task_ids='connect_to_ethereum_task', key='node_url')
    eth_conn = EthereumConnection(URL=URL)
    w3 = eth_conn.get_connection()

    results = {}
    for pool in sortedTroves:
        try:
            pool_contract = w3.eth.contract(address=w3.to_checksum_address(pool), abi=sortedTrove)
            value = pool_contract.functions.getSize().call()
            results[pool] = value
        except Exception as e:
            print(f"Error fetching trove sizes for {pool}: {e}")
    return results