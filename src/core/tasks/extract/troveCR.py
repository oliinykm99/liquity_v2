from airflow.exceptions import AirflowException
from src.core.utils.connection import EthereumConnection
from src.core.utils.abi import troveManager
from config import troveManagers, priceFeeds

def fetch_troveCR(**kwargs):
    URL = kwargs['ti'].xcom_pull(task_ids='connect_to_ethereum_task', key='node_url')
    troveIDs = kwargs['ti'].xcom_pull(task_ids='fetch_troveIDs_task') 
    prices = kwargs['ti'].xcom_pull(task_ids='fetch_price_task') 

    eth_conn = EthereumConnection(URL=URL)
    w3 = eth_conn.get_connection()

    results = {}
    missing_troves = []

    for index, pool in enumerate(troveManagers):
        try:
            pool_contract = w3.eth.contract(address=w3.to_checksum_address(pool), abi=troveManager)
            price_feed_address = priceFeeds[index]  
            if price_feed_address not in prices:
                raise AirflowException(f"Missing price for price feed {price_feed_address}")

            price = prices[price_feed_address]
            results[pool] = {}
            for id in troveIDs[pool]:
                try:
                    troveICR = pool_contract.functions.getCurrentICR(id, price).call()
                    results[pool][id] = troveICR
                except Exception as e:
                    missing_troves.append((pool, id))
                    print(f"Error fetching ICR for pool {pool}, trove {id}: {e}")

        except Exception as e:
            missing_troves.extend([(pool, id) for id in troveIDs.get(pool, [])])
            print(f"Error processing pool {pool}: {e}")

    if missing_troves:
        missing_details = ', '.join([f"(pool: {p}, id: {i})" for p, i in missing_troves])
        raise AirflowException(f"Failed to fetch ICRs for some troves: {missing_details}")

    return results