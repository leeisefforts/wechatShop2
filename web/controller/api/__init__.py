from flask import Blueprint
route_api = Blueprint('api_page', __name__)


from web.controller.api.member.member import *
from web.controller.api.shop.shop import *
from web.controller.api.merchant.merchant import *


@route_api.route('/')
def index():
    return 'API Success'
