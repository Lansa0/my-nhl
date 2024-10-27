import logging

class __Cache:
    def __init__(self):
        self.cache = {}

    def get(self,key : str) -> str:
        try:
            return self.cache[key]
        except KeyError:
            return False
    
    def set(self,key : str,data):
        self.cache[key] = data
        logging.info(f"Cache Updated ({key})")

Cache = __Cache()