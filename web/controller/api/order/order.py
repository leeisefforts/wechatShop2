from application import db, app
from flask import jsonify, request, g
from web.controller.api import route_api
from common.libs.PayService import PayService
import json


@route_api.route('/order/create', methods=['GET', 'POST'])
def create():
    resp = {'code': 200, 'msg': "操作成功", 'data': {}}
    req = request.values

    params_goods = req['goods'] if 'goods' in req else None

    items = []
    if params_goods:
        items = json.loads(params_goods)

    if len(items) < 1:
        resp['code'] = -1
        resp['msg'] = "下单失败: 没有选择商品"
        return jsonify(resp)

    member_info = g.member_info
    target = PayService()

    params = {

    }

    resp = target.createOrder(member_info.Id, items, params= params)

    return jsonify(resp)
