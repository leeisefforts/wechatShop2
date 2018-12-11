from application import app, db
from flask import request, jsonify, g, make_response
from web.controller.admin import route_admin
from common.modal.s_userinfo import S_User_Info
from common.libs.WebHelper import ops_render
from common.libs.UserService import UserService
import json


@route_admin.route('/update', methods=['GET', 'POST'])
def update():
    resp_data = {}
    if request.method == 'GET':
        req = request.args
        id = req.get('id')
        info = S_User_Info.query.filter_by(Id=id).first()
        resp_data['info'] = info
        return ops_render('admin/update.html', resp_data)

    req = request.values
    userPwd = req['userPwd'] if 'userPwd' in req else ''

    if userPwd == '':
        resp_data['msg'] = '密码不能为空'
        resp_data['code'] = -1
    info = S_User_Info.query.filter_by(Id=g.current_user.Id).first()
    info.UserPwd = userPwd
    db.session.add(info)
    db.session.commit()

    resp_data['msg'] = '修改成功'
    resp_data['code'] = 200

    response = make_response(json.dumps(resp_data))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], "%s#%s" % (UserService.geneAuthCode(info), info.Id))
    return response


@route_admin.route('/add', methods=['GET', 'POST'])
def add():
    resp_data = {}
    if request.method == 'GET':
        return ops_render('admin/add.html')

    req = request.values
    userPwd = req['userPwd'] if 'userPwd' in req else ''
    userName = req['userName'] if 'userPwd' in req else ''

    if userName == '':
        resp_data['msg'] = '用户名不能为空'
        resp_data['code'] = -1
        return jsonify(resp_data)

    if userPwd == '':
        resp_data['msg'] = '密码不能为空'
        resp_data['code'] = -1
        return jsonify(resp_data)
    info = S_User_Info.query.filter_by(UserName = userName).first()
    if info:
        resp_data['msg'] = '用户已存在'
        resp_data['code'] = -1
        return jsonify(resp_data)

    info = S_User_Info()
    info.UserPwd = userPwd
    info.UserName = userName
    info.UserRole = 1
    db.session.add(info)
    db.session.commit()

    resp_data['msg'] = '添加成功'
    resp_data['code'] = 200
    return jsonify(resp_data)
