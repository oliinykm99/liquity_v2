from airflow.exceptions import AirflowException
from src.core.utils.connection import EthereumConnection
from src.core.utils.abi import troveManager

def fetch_troveData(**kwargs):
    URL = kwargs['ti'].xcom_pull(task_ids='connect_to_ethereum_task', key='node_url')
    troveIDs = kwargs['ti'].xcom_pull(task_ids='fetch_troveIDs_task') 
    
    eth_conn = EthereumConnection(URL=URL)
    w3 = eth_conn.get_connection()

    results = {}
    missing_troves = []
    for pool, ids in troveIDs.items():
        try:
            pool_contract = w3.eth.contract(address=w3.to_checksum_address(pool), abi=troveManager)
            results[pool_contract.address] = {}
            for id in ids:
                try:
                    troveData = pool_contract.functions.getLatestTroveData(id).call()
                    results[pool_contract.address][id] = troveData
                except Exception as e:
                    missing_troves.append((pool_contract.address, id))
                    raise AirflowException(f"Error fetching data for pool {pool_contract.address}, trove {id}: {e}")

        except Exception as e:
            missing_troves.extend([(pool_contract.address, id) for id in ids])
            raise AirflowException(f"Error processing pool {pool_contract.address}: {e}")
    
    if missing_troves:
        missing_details = ', '.join([f"(pool: {p}, id: {i})" for p, i in missing_troves])
        raise AirflowException(f"Failed to fetch data for some troves: {missing_details}")
    
    for pool, ids in troveIDs.items():
        if pool not in results:
            raise AirflowException(f"Missing results for pool {pool}")
        for id in ids:
            if id not in results[pool]:
                raise AirflowException(f"Missing data for trove ID {id} in pool {pool}")
    
    return results