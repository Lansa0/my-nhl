import logging

class __Cache:
    def __init__(self):
        self.cache = {}

    def get(self,key : str) -> dict:
        return self.cache[key]
    
    def set(self,key : str,data):
        self.cache[key] = data
        logging.info(f"Cache Updated ({key})")

Cache = __Cache()