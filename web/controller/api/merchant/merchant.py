from application import db, app
from flask import request, jsonify
from web.controller.api import route_api
from common.libs.WebHelper import getCurrentDate
from common.modal.merchant_info import Merchant_Info
from common.modal.shop_info import Shop_Info


@route_api.route('/addmerchant', methods=['GET', 'POST'])
def addmerchant():
    resp = {'code': 200, 'msg': '申请成功'}
    req = request.values

    id = req['id'] if 'id' in req else -1
    name = req['name'] if 'name' in req else ''
    phone = req['phone'] if 'phone' in req else ''
    address = req['address'] if 'address' in req else ''
    imageUrl = req['imageUrl'] if 'imageUrl' in req else ''
    openId = req['openId'] if 'openId' in req else ''

    info = Merchant_Info.query.filter_by(Id=id).first()
    if info:
        modal_info = info
    else:
        modal_info = Merchant_Info()
        modal_info.CreateTime = getCurrentDate()

    modal_info.Name = name
    modal_info.Address = address
    modal_info.Phone = phone
    modal_info.ImageUrl = imageUrl
    modal_info.OpenId = openId
    modal_info.Status = 1
    db.session.add(modal_info)
    db.session.commit()

    return jsonify(resp)


@route_api.route('/merchant/info', methods=['GET', 'POST'])
def info():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else 0
    info = Merchant_Info.query.filter_by(OpenId=id).first()
    if info:
        resp['data'] = {
            'name': info.Name,
            'address': info.Address,
            'phone': info.Phone,
            'imageUrl': info.ImageUrl
        }

    shop_list = Shop_Info.query.filter_by(ShopMerchantId= id).all()
    if len(shop_list) == 1:
        resp['shop_list'] = [{
            'ShopName': shop_list[0].ShopName,
            'ShopDesc': shop_list[0].ShopDesc,
            'TotalCount': shop_list[0].TotalCount,
            'Stock': shop_list[0].Stock,
            'ShopImageUrl': shop_list[0].ShopImageUrl
        }]
    else:
        resp['shop_list'] = shop_list

    return jsonify(resp)
