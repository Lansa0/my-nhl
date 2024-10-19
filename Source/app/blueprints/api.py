from flask import jsonify
from cache import Cache
from app.blueprints import API

@API.route("/standings")
def standings():
    return jsonify(Cache.get("standings"))

@API.route("/scores")
def scores():
    return jsonify(Cache.get("scores"))