from flask import Blueprint

API = Blueprint("API",__name__,url_prefix="/api")
STANDINGS = Blueprint("STANDINGS",__name__,url_prefix="/standings")
SCORES = Blueprint("SCORES",__name__,url_prefix="/scores")

from .api import *
from .standings import *
from .scores import *