from airflow.exceptions import AirflowException
from src.core.utils.connection import EthereumConnection
from src.core.utils.abi import priceFeed
from config import priceFeeds

def fetch_price(**kwargs):
    URL = kwargs['ti'].xcom_pull(task_ids='connect_to_ethereum_task', key='node_url')
    eth_conn = EthereumConnection(URLs=[URL])
    w3 = eth_conn.get_connection()

    results = {}
    for pool in priceFeeds:
        try:
            pool_contract = w3.eth.contract(address=w3.to_checksum_address(pool), abi=priceFeed)
            value = pool_contract.functions.lastGoodPrice().call()

            if not isinstance(value, int) or value < 0:
                raise AirflowException(f"Invalid value received: {value}")

            results[pool_contract.address] = value
        except Exception as e:
            raise AirflowException(f"Error fetching Price for {pool_contract.address}: {e}")
    return results