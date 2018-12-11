from application import app

from web.controller.interceptors.authIntercetor import *

from web.controller.index import route_index
from web.controller.static import route_static
from web.controller.admin import route_admin
from web.controller.upload import route_upload


app.register_blueprint(route_index, url_prefix='/')
app.register_blueprint(route_static, url_prefix='/static')
app.register_blueprint(route_admin, url_prefix='/admin')
app.register_blueprint(route_upload, url_prefix='/upload')