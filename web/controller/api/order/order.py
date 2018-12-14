from application import db, app
from flask import jsonify, request, g
from web.controller.api import route_api
from common.libs.PayService import PayService
from common.modal.shop_info import Shop_Info
from common.modal.pay.payOrder import PayOrder
from common.modal.pay.payordercallbackData import PayOrderCallbackData
from common.modal.pay.payOrderItem import PayOrderItem
from common.modal.OauthMemberBind import OauthMemberBind
from common.libs.WechatService import WeChatService
from common.libs.UrlManager import UrlManager
import json, decimal


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

    resp = target.createOrder(member_info.Id, items, params=params)

    return jsonify(resp)


@route_api.route("/order/info", methods=["POST"])
def orderInfo():
    resp = {'code': 200, 'msg': "操作成功", 'data': {}}
    req = request.values
    params_goods = req['goods'] if 'goods' in req else None

    member_info = g.member_info
    goods_list = []
    if params_goods:
        goods_list = json.loads(params_goods)

    food_dic = {}
    for item in goods_list:
        food_dic[item['id']] = item['number']

    food_ids = food_dic.keys()
    food_list = Shop_Info.query.filter(Shop_Info.Id.in_(food_ids)).all()
    data_food_list = []

    yun_price = pay_price = decimal.Decimal(0.00)
    if food_list:
        for item in food_list:
            tmp_data = {
                'id': item.Id,
                'name': item.ShopName,
                'price': str(item.price),
                'pic_url': UrlManager.buildImageUrl(item.main_image),
                'number': food_dic[item.Id]
            }
            pay_price = pay_price + item.price
            data_food_list.append(tmp_data)

    # 获取地址

    resp['data']['food_list'] = data_food_list
    resp['data']['pay_price'] = str(pay_price)
    resp['data']['yun_price'] = str(yun_price)
    resp['data']['total_price'] = str(pay_price + yun_price)
    return jsonify(resp)


@route_api.route("/order/pay", methods=["POST"])
def orderPay():
    resp = {'code': 200, 'msg': "操作成功", 'data': {}}
    req = request.values
    member_info = g.member_info

    order_sn = req['order_sn'] if 'order_sn' in req else ''
    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info:
        resp['code'] = -1
        resp['code'] = "系统繁忙"
        return jsonify(resp)

    oauth_bind_info = OauthMemberBind.query.filter_by(Member_id=member_info.Id).first()
    if not oauth_bind_info:
        resp['code'] = -1
        resp['code'] = "系统繁忙"
        return jsonify(resp)

    config_mina = app.config["MINA_APP"]
    notify_url = app.config["APP"]["domain"] + config_mina['callback_url']
    target_wechat = WeChatService(merchant_key=config_mina["paykey"])

    data = {
        'appid': config_mina['appid'],
        'mch_id': config_mina['mch_id'],
        'nonce_str': target_wechat.get_nonce_str(),
        'body': "购买",
        'out_trade_no': pay_order_info.order_sn,
        'total_fee': int(pay_order_info.total_price * 100),
        'notify_url': notify_url,
        'trade_type': 'JSAPI',
        'openid': oauth_bind_info.Openid

    }

    pay_info = target_wechat.get_pay_info(data)

    # 保存prepay_id
    pay_order_info.prepay_id = pay_info['prepay_id']
    db.session.add(pay_order_info)
    db.session.commit()

    resp['data']['pay_info'] = pay_info

    return jsonify(resp)
