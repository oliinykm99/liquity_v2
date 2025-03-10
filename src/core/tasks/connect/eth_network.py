import os
from dotenv import load_dotenv
from src.core.utils.connection import EthereumConnection

load_dotenv()
URL = os.getenv("URL")

eth_conn = EthereumConnection(URL=URL)
w3 = eth_conn.get_connection()

def connect_to_ethereum(**kwargs):
    try:
        if w3.is_connected():
            return URL
        else:
            raise Exception("Connection failed after initialization.")
    except Exception as e:
        print(f"Error: {e}")
        raise