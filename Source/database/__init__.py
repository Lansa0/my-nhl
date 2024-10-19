from cache import Cache
from database import updates
import nhl_api
import threading
import json

def _writeJSON(data,file_name:str):
    """
    For debugging / Temporary substitiute for proper database
    """
    with open(f"Source/database/jsons/{file_name}.json","w") as f:
        json.dump(data,f,indent=4)

def run():
    Scores = nhl_api.Scores()
    _writeJSON(Scores,"scores")
    Cache.set("scores",Scores)

    Standings = nhl_api.Standings()
    _writeJSON(Standings,"standings")
    Cache.set("standings",Standings)

    ScoresUpdates = threading.Thread(target=updates.Scores,daemon=True)
    ScoresUpdates.start()

    # DailyUpdates = threading.Thread(target=updates.Daily,daemon=True)
    # DailyUpdates.start()
