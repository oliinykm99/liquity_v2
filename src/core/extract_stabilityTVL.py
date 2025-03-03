import os
from dotenv import load_dotenv
from src.core.connection import EthereumConnection
from src.core.abi import stabilityPool
from config import stabilityPools

load_dotenv()
URL = os.getenv("URL")

eth_conn = EthereumConnection(URL=URL)
w3 = eth_conn.get_connection()

def fetch_stabilityTVL():
    results = {}
    for pool in stabilityPools:
        try:
            pool_contract = w3.eth.contract(address=w3.to_checksum_address(pool), abi=stabilityPool)
            value = pool_contract.functions.getTotalBoldDeposits().call()
            results[pool] = value / 1e18
        except Exception as e:
            print(f"Error fetching Debt for {pool}: {e}")
    return results