from datetime import datetime
from cache import Cache
import nhl_api
import logging
import time
import pytz

def Scores():
    while True:
        CurrentTime = datetime.now(pytz.utc)
        CurrentDay = CurrentTime.strftime("%d")
        CurrentHour = int(CurrentTime.strftime("%H"))

        FirstMatchTime = Cache.get("scores")["start_time"]
        FirstDay = datetime.strptime(FirstMatchTime,"%Y-%m-%dT%H:%M:%SZ").day
        FirstHour =  datetime.strptime(FirstMatchTime,"%Y-%m-%dT%H:%M:%SZ").hour
        
        if int(CurrentDay) != int(FirstDay): 
            CurrentHour += 24

        if FirstHour <= CurrentHour and not Cache.get("scores")["finished"]:
            logging.info("Begin Live Score Updates")
            while True:
                time.sleep(20)
                Scores = nhl_api.Scores()
                Cache.set("scores",Scores)

                if Scores["finished"]:
                    break
            logging.info("End Live Score Updates")
        time.sleep(1800)

def Daily():
    pass