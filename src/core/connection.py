from web3 import Web3

class EthereumConnection:
    def __init__(self, URL):
        self.URL = URL
        self.w3 = Web3(Web3.HTTPProvider(self.URL))
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to Ethereum node")

    def get_connection(self):
        return self.w3
    
    def is_connected(self):
        return self.w3.is_connected()

