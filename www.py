from application import app

from web.controller.interceptors.authIntercetor import *
from web.controller.interceptors.apiAuthInterceptor import *

from web.controller.index import route_index
from web.controller.static import route_static
from web.controller.admin import route_admin
from web.controller.upload import route_upload
from web.controller.api import route_api
from web.controller.chart.chart import route_chart


app.register_blueprint(route_index, url_prefix='/')
app.register_blueprint(route_static, url_prefix='/static')
app.register_blueprint(route_admin, url_prefix='/admin')
app.register_blueprint(route_upload, url_prefix='/upload')
app.register_blueprint(route_api, url_prefix='/api')
app.register_blueprint(route_chart, url_prefix='/chart')