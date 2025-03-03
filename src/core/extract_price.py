import os
from dotenv import load_dotenv
from src.core.connection import EthereumConnection
from src.core.abi import priceFeed
from config import priceFeeds

load_dotenv()
URL = os.getenv("URL")

eth_conn = EthereumConnection(URL=URL)
w3 = eth_conn.get_connection()

def fetch_price():
    results = {}
    for pool in priceFeeds:
        try:
            pool_contract = w3.eth.contract(address=w3.to_checksum_address(pool), abi=priceFeed)
            value = pool_contract.functions.lastGoodPrice().call()
            results[pool] = value / 1e18
        except Exception as e:
            print(f"Error fetching Price for {pool}: {e}")
    return results