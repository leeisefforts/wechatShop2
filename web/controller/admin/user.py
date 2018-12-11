from web.controller.admin import route_admin
from common.libs.WebHelper import ops_render


@route_admin.route('/user', methods=['GET', 'POST'])
def user():
    return ops_render('admin/user.html')
