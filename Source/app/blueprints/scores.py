from flask import render_template,redirect,url_for
from app.blueprints import SCORES
from datetime import datetime
from cache import Cache
import nhl_api

@SCORES.route("/")
def default():
    return redirect(url_for("SCORES.scores",date="now"))   

@SCORES.route("/<date>")
def scores(date : str):
    try:
        if date != "now":
            GivenDate : datetime.date = datetime.strptime(date, "%Y-%m-%d").date()
            TodaysDate : datetime.date = datetime.today().date()

            if GivenDate == TodaysDate:
                date = datetime.now().strftime("%Y-%m-%d")
        else:
            date = datetime.now().strftime("%Y-%m-%d")

        Scores = Cache.get(f"SCORES:{date}")
        if not Scores:
            Scores : list = nhl_api.Scores(date)
            Cache.set(f"SCORES:{date}",Scores)
            
        return render_template("scores.html",data=Scores)
    except ValueError:
        return "Invalid Date Parameter",404