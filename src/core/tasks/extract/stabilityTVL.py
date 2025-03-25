from airflow.exceptions import AirflowException
from src.core.utils.connection import EthereumConnection
from src.core.utils.abi import stabilityPool
from config import stabilityPools

def fetch_stabilityTVL(**kwargs):
    URL = kwargs['ti'].xcom_pull(task_ids='connect_to_ethereum_task', key='node_url')
    eth_conn = EthereumConnection(URL=URL)
    w3 = eth_conn.get_connection()

    results = {}
    for pool in stabilityPools:
        try:
            pool_contract = w3.eth.contract(address=w3.to_checksum_address(pool), abi=stabilityPool)
            value = pool_contract.functions.getTotalBoldDeposits().call()
            
            if not isinstance(value, int) or value < 0:
                raise AirflowException(f"Invalid value received: {value}")

            results[pool] = value
        except Exception as e:
            raise AirflowException(f"Error fetching Debt for {pool}: {e}")
    return results