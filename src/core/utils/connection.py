from web3 import Web3
from typing import List

class EthereumConnection:
    def __init__(self, URLs: List[str]):
        self.URLs = URLs
        self.current_url_index = 0
        self.w3 = None
        self._connect()

    def _connect(self):
        for i, url in enumerate(self.URLs[self.current_url_index:], start=self.current_url_index):
            self.w3 = Web3(Web3.HTTPProvider(url))
            if self.w3.is_connected():
                self.current_url_index = i
                return
        
        raise ConnectionError(f'Failed to connect to all Ethereum nodes {self.URLs}')

    def get_connection(self):
        if not self.w3:
            return False
        return self.w3
    
    def is_connected(self):
        if not self.w3:
            return False
        return self.w3.is_connected()
    
    def rotate_endpoint(self):
        self.current_url_index = (self.current_url_index + 1) % len(self.URLs)
        self._connect()

