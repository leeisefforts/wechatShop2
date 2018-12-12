from flask import Blueprint
from web.controller.api.member import *
from web.controller.api.shop import *
from web.controller.api.merchant import *

route_api = Blueprint('api_page', __name__)


@route_api.route('/')
def index():
    return 'API Success'
