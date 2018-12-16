from application import app, db
from web.controller.api import route_api
from common.modal.coupon_info import Coupon_Info
from common.libs.WebHelper import getCurrentDate
from common.libs.UrlManager import UrlManager
from flask import jsonify, request, g
from sqlalchemy import or_
import json


@route_api.route('/coupon/list')
def couponlist():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values

    mix_kw = str(req['mix_kw']) if 'mix_kw' in req else ''
    p = int(req['p']) if 'p' in req else 1

    if p < 1:
        p = 1

    page_size = 10
    offset = (p - 1) * page_size
    query = Coupon_Info.query.filter_by(Member_Id=g.member_info.Id)

    if mix_kw:
        rule = or_(Coupon_Info.Coupon_Name.ilike("%{0}%".format(mix_kw)))
        query = query.filter(rule)

    shop_list = query.order_by(Coupon_Info.Id.desc()) \
        .offset(offset).limit(page_size).all()

    data_food_list = []
    if shop_list:
        for item in shop_list:
            tmp_data = {
                'id': item.Id,
                'name': "%s" % (item.Coupon_Name),
                'price': str(item.Coupon_Price),
                'min_price': str(item.Price),
                'createTime': str(item.CreateTime),
                'status': str(item.Status)
            }
            data_food_list.append(tmp_data)
    resp['data']['list'] = data_food_list
    resp['data']['has_more'] = 0 if len(data_food_list) < page_size else 1
    return jsonify(resp)


@route_api.route('/coupon/info', methods=['GET', 'POST'])
def couponInfo():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else 0
    info = Coupon_Info.query.filter_by(Id=id).first()
    resp['data'] = {
        'name': info.Coupon_Name,
        'price': str(info.Coupon_Price),
        'min_price': str(info.Price),
        'qrCode_Url': info.QrCode_Url if info.QrCode_Url else '',
        'status': str(info.Status)
    }

    return jsonify(resp)