from web.controller.admin import route_admin
from common.libs.WebHelper import ops_render
from common.modal.member import Member
from flask import request


@route_admin.route('/user', methods=['GET', 'POST'])
def user():
    resp = {}
    if request.method == 'GET':
        list = Member.query.order_by(Member.Id.desc()).all()
        resp['list'] = list
        return ops_render('admin/user.html', resp)
