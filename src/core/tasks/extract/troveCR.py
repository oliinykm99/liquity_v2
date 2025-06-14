from airflow.exceptions import AirflowException
from src.core.utils.connection import EthereumConnection
from src.core.utils.abi import troveManager

def fetch_troveCR(**kwargs):
    URL = kwargs['ti'].xcom_pull(task_ids='connect_to_ethereum_task', key='node_url')
    troveIDs = kwargs['ti'].xcom_pull(task_ids='fetch_troveIDs_task') 
    prices = kwargs['ti'].xcom_pull(task_ids='fetch_price_task') 

    eth_conn = EthereumConnection(URLs=[URL])
    w3 = eth_conn.get_connection()

    results = {}
    missing_troves = []

    for index, pool in enumerate(troveIDs.keys()):
        try:
            pool_contract = w3.eth.contract(address=w3.to_checksum_address(pool), abi=troveManager)
            price_feed_address = list(prices.keys())[index]  
            if price_feed_address not in prices:
                raise AirflowException(f"Missing price for price feed {price_feed_address}")

            price = prices[price_feed_address]
            results[pool_contract.address] = {}
            for id in troveIDs[pool_contract.address]:
                try:
                    troveICR = pool_contract.functions.getCurrentICR(id, price).call()
                    results[pool_contract.address][id] = troveICR
                except Exception as e:
                    missing_troves.append((pool_contract.address, id))
                    raise AirflowException(f"Error fetching ICR for pool {pool_contract.address}, trove {id}: {e}")

        except Exception as e:
            missing_troves.extend([(pool_contract.address, id) for id in troveIDs.get(pool_contract.address, [])])
            raise AirflowException(f"Error processing pool {pool_contract.address}: {e}")

    if missing_troves:
        missing_details = ', '.join([f"(pool: {p}, id: {i})" for p, i in missing_troves])
        raise AirflowException(f"Failed to fetch ICRs for some troves: {missing_details}")

    return results