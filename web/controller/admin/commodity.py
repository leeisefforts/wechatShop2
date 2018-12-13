from web.controller.admin import route_admin
from common.libs.WebHelper import ops_render
from flask import request, jsonify
from common.modal.shop_info import Shop_Info
from common.modal.merchant_info import Merchant_Info
from application import db, app
import json


@route_admin.route('/commodity', methods=['GET', 'POST'])
def commodity():
    resq = {}
    if request.method == 'GET':
        list = Shop_Info.query.order_by(Shop_Info.Id.desc()).all()
        resq['list'] = list
        return ops_render('admin/commodity.html', resq)


@route_admin.route('/commodity/info', methods=['GET', 'POST'])
def commodity_info():
    resq = {}
    id = request.args.get('id')
    if request.method == 'GET':
        resq['info'] = Shop_Info.query.filter_by(Id=id).first()
        resq['merchants'] = Merchant_Info.query.order_by(Merchant_Info.Id.desc()).all()
        return ops_render('shop/info.html', resq)


@route_admin.route('/commodity/edit', methods=['GET', 'POST'])
def edit():
    resq = {'code': 200, 'msg': '操作成功'}
    req = request.values
    id = req['id']
    status = req['status']
    shop = Shop_Info.query.filter_by(Id=id).first()
    shop.ShopStatus = status
    db.session.add(shop)
    db.session.commit()

    return jsonify(resq)
