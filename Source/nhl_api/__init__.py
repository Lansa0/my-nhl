from datetime import datetime
import pytz
import json

import nhl_api.raw as raw

TeamColours = {
    "ANA": "#FC4C02",  # Anaheim Ducks
    "ARI": "#8C2633",  # Arizona Coyotes
    "BOS": "#FCB514",  # Boston Bruins
    "BUF": "#003087",  # Buffalo Sabres
    "CGY": "#D2001C",  # Calgary Flames
    "CAR": "#CE1126",  # Carolina Hurricanes
    "CHI": "#CF0A2C",  # Chicago Blackhawks
    "COL": "#6F263D",  # Colorado Avalanche
    "CBJ": "#002654",  # Columbus Blue Jackets
    "DAL": "#006847",  # Dallas Stars
    "DET": "#CE1126",  # Detroit Red Wings
    "EDM": "#041E42",  # Edmonton Oilers
    "FLA": "#B9975B",  # Florida Panthers
    "LAK": "#111111",  # Los Angeles Kings
    "MIN": "#AF2324",  # Minnesota Wild
    "MTL": "#AF1E2D",  # Montréal Canadiens
    "NSH": "#FFB81C",  # Nashville Predators
    "NJD": "#CE1126",  # New Jersey Devils
    "NYI": "#00539B",  # New York Islanders
    "NYR": "#0038A8",  # New York Rangers
    "OTT": "#DA1A32",  # Ottawa Senators
    "PHI": "#F74902",  # Philadelphia Flyers
    "PIT": "#FCB514",  # Pittsburgh Penguins
    "SJS": "#006D75",  # San Jose Sharks
    "SEA": "#99D9D9",  # Seattle Kraken
    "STL": "#002F87",  # St. Louis Blues
    "TBL": "#FFFFFF",  # Tampa Bay Lightning
    "TOR": "#FFFFFF",  # Toronto Maple Leafs
    "UTA": "#71AFE5",  # Utah Hockey Club
    "VAN": "#00205B",  # Vancouver Canucks
    "VGK": "#B9975B",  # Vegas Golden Knights
    "WSH": "#041E42",  # Washington Capitals
    "WPG": "#041E42",  # Winnipeg Jets
}

def Scores(date : str = "now") -> list:
    """
    Returns a list of NHL scores during the given date\n
    Modified version of the raw json given from the NHL api endpoint
    """
    
    Data = raw.getScores(date)
    Games = Data["games"]

    if len(Games) == 0:
        return {
            "next" : Data["nextDate"],
            "now" : Data["currentDate"],
            "back" : Data["prevDate"],
            "start_time" : "2000-01-01T00:00:00Z",
            "finished" : True,
            "games" : []
        }

    ToReturn : dict  = {
        "next" : Data["nextDate"],
        "now" : Data["currentDate"],
        "back" : Data["prevDate"],
        "start_time" : Games[0]["startTimeUTC"],
        "finished" : None,
        "games" : []
    }

    FinishedCounter = 0
    for game_info in Games:
        Game = {}

        Game["type"] = game_info["gameType"]

        UTC_Time = game_info["startTimeUTC"]
        UTC_Time = datetime.strptime(UTC_Time, "%Y-%m-%dT%H:%M:%SZ")
        UTC_Time = pytz.utc.localize(UTC_Time)
        EST_Time = UTC_Time.astimezone(pytz.timezone("America/Toronto"))

        Game["start"] = EST_Time.strftime("%H:%M %Z")

        Game["home"] = {
            "name" : game_info["homeTeam"]["abbrev"],
            "logo" : game_info["homeTeam"]["logo"],
            "colour" : TeamColours[game_info["homeTeam"]["abbrev"]],
        }

        Game["away"] = {
            "name" : game_info["awayTeam"]["abbrev"],
            "logo" : game_info["awayTeam"]["logo"],
            "colour" : TeamColours[game_info["awayTeam"]["abbrev"]],
        }

        if game_info["gameState"] not in ["FUT","PRE"]:
            Game["home"]["score"] = game_info["homeTeam"]["score"]
            Game["away"]["score"] = game_info["awayTeam"]["score"]

            Game["home"]["sog"] = game_info["homeTeam"]["sog"]
            Game["away"]["sog"] = game_info["awayTeam"]["sog"]
            
            GoalList = []
            CurrentPeriod = 0

            try:
                for goal_info in game_info["goals"]:
                    GoalInfo = {}

                    if goal_info["period"] > CurrentPeriod:
                        CurrentPeriod = goal_info["period"]
                        GoalInfo["period"] = CurrentPeriod
                    else:
                        GoalInfo["period"] = 0
                    
                    GoalInfo["team"] = goal_info["teamAbbrev"]
                    GoalInfo["goal"] = goal_info["firstName"]["default"] + " " + goal_info["lastName"]["default"] + ", " + goal_info["timeInPeriod"] + "'"
                    
                    if len(goal_info["assists"]) > 0:
                        String = ""
                        for assist_info in goal_info["assists"]:
                            String += assist_info["name"]["default"] + ", "
                        String = String[:-2]
                        GoalInfo["assist"] = String
                    else:
                        GoalInfo["assist"] = 0

                    GoalList.append(GoalInfo)
            except KeyError:
                with open(f"GOAL_ERROR:{datetime.now().strftime('%y:%m:%d - %H:%M:%S')}.json","w") as f:
                    json.dump(Data,f,indent=4)

            Game["goals"] = GoalList
            
        if game_info["gameState"] in ["LIVE","CRIT"]:
            if game_info["clock"]["inIntermission"]:
                Game["clock"] = "INTERMISSION " + game_info["clock"]["timeRemaining"]
            else:
                Game["clock"] = "PERIOD " +  str(game_info["period"]) + " - " + game_info["clock"]["timeRemaining"]

        if game_info["gameState"] in ["OFF","FINAL"] or game_info["gameScheduleState"] == "PPD":
            FinishedCounter += 1
            Game["state"] = 2
        elif game_info["gameState"] in ["LIVE","CRIT"]:
            Game["state"] = 1
        else:
            Game["state"] = 0 
        
        ToReturn["games"].append(Game) 

    ToReturn["finished"] = (FinishedCounter == len(Games))
    return ToReturn

def Standings() -> list:
    Data = raw.getStandings()
    Standings = Data["standings"]

    ToReturn : list = []
    for team_info in Standings:
        Team = {
            "colour" : TeamColours[team_info["teamAbbrev"]["default"]],
            "league_position" : team_info["leagueSequence"],
            "conference_position" : team_info["conferenceSequence"],
            "division_position" : team_info["divisionSequence"],
            "name" : team_info["teamName"]["default"],
            "logo" : team_info["teamLogo"],
            "points" : team_info["points"],
            "played" : team_info["gamesPlayed"],
            "wins" : team_info["wins"],
            "losses" : team_info["losses"],
            "otl" : team_info["otLosses"],
            "for" : team_info["goalFor"],
            "against" : team_info["goalAgainst"],
            "differential" : team_info["goalDifferential"],
            "conference" : team_info["conferenceAbbrev"],
            "division" : team_info["divisionAbbrev"]
        }
        ToReturn.append(Team)
    return ToReturn