from flask import Blueprint

API = Blueprint("API",__name__,url_prefix="/api")
STANDINGS = Blueprint("STANDINGS",__name__,url_prefix="/standings")

from .api import *
from .standings import *