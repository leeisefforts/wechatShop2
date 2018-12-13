from application import db, app
from web.controller.api import route_api


@route_api.route('create', methods=['GET', 'POST'])
def create():
    pass
