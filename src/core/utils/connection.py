from web3 import Web3
from typing import List

class EthereumConnection:
    def __init__(self, URLs: List[str], current_url_index: int = 0):
        self.URLs = URLs
        self.current_url_index = current_url_index
        self.failed_endpoints = []
        self.w3 = None
        self._connect()

    def _connect(self):
        self.failed_endpoints = []
        for i, url in enumerate(self.URLs[self.current_url_index:], start=self.current_url_index):
            self.w3 = Web3(Web3.HTTPProvider(url))
            if self.w3.is_connected():
                self.current_url_index = i
                return
            else:
                self.failed_endpoints.append(url)
        raise ConnectionError(f'Failed to connect to all Ethereum nodes {self.URLs}')

    def get_connection(self):
        if not self.w3 or not self.w3.is_connected():
            self.rotate_endpoint()
        return self.w3
    
    def is_connected(self):
        if not self.w3:
            return False
        return self.w3.is_connected()
    
    def rotate_endpoint(self):
        self.current_url_index = (self.current_url_index + 1) % len(self.URLs)
        self._connect()

    def get_failed_endpoints(self) -> List[str]:
        return self.failed_endpoints

