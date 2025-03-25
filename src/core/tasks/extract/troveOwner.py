from airflow.exceptions import AirflowException
from src.core.utils.connection import EthereumConnection
from src.core.utils.abi import troveManager, troveNFT

def fetch_troveOwner(**kwargs):
    URL = kwargs['ti'].xcom_pull(task_ids='connect_to_ethereum_task', key='node_url')
    troveIDs = kwargs['ti'].xcom_pull(task_ids='fetch_troveIDs_task') 
    
    eth_conn = EthereumConnection(URL=URL)
    w3 = eth_conn.get_connection()

    results = {}
    missing_troves = []
    for pool, ids in troveIDs.items():
        try:
            pool_contract = w3.eth.contract(address=w3.to_checksum_address(pool), abi=troveManager)
            troveNFT_address = pool_contract.functions.troveNFT().call()
            troveNFT_contract = w3.eth.contract(address=w3.to_checksum_address(troveNFT_address), abi=troveNFT)

            results[pool] = {}
            for id in ids:
                try:
                    troveOwner = troveNFT_contract.functions.ownerOf(id).call()
                    results[pool][id] = troveOwner
                except Exception as e:
                    missing_troves.append((pool, id))
                    print(f"Error fetching owner for pool {pool}, trove {id}: {e}")

        except Exception as e:
            missing_troves.extend([(pool, id) for id in ids])
            print(f"Error processing pool {pool}: {e}")
    
    if missing_troves:
        missing_details = ', '.join([f"(pool: {p}, id: {i})" for p, i in missing_troves])
        raise AirflowException(f"Failed to fetch owners for some troves: {missing_details}")
    
    for pool, ids in troveIDs.items():
        if pool not in results:
            raise AirflowException(f"Missing results for pool {pool}")
        for id in ids:
            if id not in results[pool]:
                raise AirflowException(f"Missing owner for trove ID {id} in pool {pool}")
    
    return results