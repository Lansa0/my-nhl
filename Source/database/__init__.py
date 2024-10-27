from datetime import datetime
from database import updates
from cache import Cache
import threading
import nhl_api
import json

def _writeJSON(data,file_name:str):
    """For debugging """
    with open(f"Source/database/jsons/{file_name}.json","w") as f:
        json.dump(data,f,indent=4)

def run():
    CurrentDate = datetime.now().strftime("%Y-%m-%d")
    Scores = nhl_api.Scores(CurrentDate)
    _writeJSON(Scores,"scores")
    Cache.set(f"SCORES:{CurrentDate}",Scores)

    Standings = nhl_api.Standings()
    Cache.set("STANDINGS:now",Standings)

    ScoresUpdates = threading.Thread(target=updates.Scores,daemon=True)
    ScoresUpdates.start()

    # DailyUpdates = threading.Thread(target=updates.Daily,daemon=True)
    # DailyUpdates.start()
