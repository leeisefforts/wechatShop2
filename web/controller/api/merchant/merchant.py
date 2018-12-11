from application import db, app
from flask import request, jsonify
from web.controller.api import route_api


@route_api.route('/addmerchant', methods=['GET', 'POST'])
def addmerchant():
    resp = {'code': 200, 'msg': '申请成功'}
    req = request.values
    return jsonify(req)
