from flask import Flask,render_template
import app.blueprints as blueprint
from cache import Cache
import os

def makeApp() -> Flask:
    TemplatePath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"templates")
    app = Flask(__name__, template_folder=TemplatePath)

    app.register_blueprint(blueprint.API)
    app.register_blueprint(blueprint.STANDINGS)

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/scores")
    def matches():
        return render_template("index.html",data=Cache.get("scores")["games"])

    return app