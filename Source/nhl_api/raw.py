import requests
import logging

def _requestHandler(url : str):
    try:
        Response = requests.get(url)
        Response.raise_for_status()
    
        Data = Response.json()
        logging.info(f"\"{url}\" Request Successful")
        return Data
    
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP ERROR : {e}")
    except ValueError as e:
        logging.error(f"JSON DECODE ERROR : {e}")
    return {}

def getScores() -> dict:
    URL = "https://api-web.nhle.com/v1/score/now"
    return _requestHandler(URL)

def getStandings() -> dict:
    URL = "https://api-web.nhle.com/v1/standings/now"
    return _requestHandler(URL)