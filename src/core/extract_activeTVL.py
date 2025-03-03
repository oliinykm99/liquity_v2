import os
from dotenv import load_dotenv
from src.core.connection import EthereumConnection
from src.core.abi import activePool
from config import activePools

load_dotenv()
URL = os.getenv("URL")

eth_conn = EthereumConnection(URL=URL)
w3 = eth_conn.get_connection()

def fetch_activeTVL():
    results = {}
    for pool in activePools:
        try:
            pool_contract = w3.eth.contract(address=w3.to_checksum_address(pool), abi=activePool)
            value = pool_contract.functions.getCollBalance().call()
            results[pool] = value / 1e18
        except Exception as e:
            print(f"Error fetching TVL for {pool}: {e}")
    return results
