from flask import Blueprint

route_admin = Blueprint('admin_page', __name__)
from web.controller.admin.merchant import *
from web.controller.admin.user import *
from web.controller.admin.report import *
from web.controller.admin.update import *
from web.controller.admin.commodity import *


@route_admin.route('/admin')
def index():
    return ''
