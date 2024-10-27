from flask import render_template,redirect,url_for
from cache import Cache
from app.blueprints import STANDINGS

@STANDINGS.route("/")
def default():
    return redirect(url_for("STANDINGS.league"))   

@STANDINGS.route("/league")
def league():
    return render_template("standings/league.html",data=Cache.get("STANDINGS:now"))

@STANDINGS.route("/conference")
def conference():
    return render_template("standings/conference.html",data=Cache.get("STANDINGS:now"))

@STANDINGS.route("/division")
def division():
    return render_template("standings/division.html",data=Cache.get("STANDINGS:now"))