from flask import Flask,render_template,redirect,url_for
import app.blueprints as blueprint
import nhl_api
from cache import Cache
from datetime import datetime
import logging
import os

def makeApp() -> Flask:
    TemplatePath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"templates")
    app = Flask(__name__, template_folder=TemplatePath)

    # app.register_blueprint(blueprint.API)
    app.register_blueprint(blueprint.STANDINGS)
    app.register_blueprint(blueprint.SCORES)
    
    @app.route("/")
    def home():
        return render_template("home.html")

    return app