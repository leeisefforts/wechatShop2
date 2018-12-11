from web.controller.admin import route_admin
from common.libs.WebHelper import ops_render


@route_admin.route('/report', methods=['GET', 'POST'])
def report():
    return ops_render('admin/report.html')
