from application import db, app
from flask import jsonify, request, g
from web.controller.api import route_api
from common.libs.WebHelper import getCurrentDate, selectFilterObj, getFormatDate, getDictFilterField, createQrCode_Url
from common.libs.PayService import PayService
from common.modal.shop_info import Shop_Info
from common.modal.pay.payOrder import PayOrder
from common.modal.pay.payordercallbackData import PayOrderCallbackData
from common.modal.pay.payOrderItem import PayOrderItem
from common.modal.OauthMemberBind import OauthMemberBind
from common.libs.WechatService import WeChatService
from common.libs.UrlManager import UrlManager
import json, decimal, datetime


@route_api.route('/order/create', methods=['GET', 'POST'])
def create():
    resp = {'code': 200, 'msg': "操作成功", 'data': {}}
    req = request.values

    params_goods = req['goods'] if 'goods' in req else None
    coupon_Id = req['coupon_Id'] if 'coupon_Id' in req else ''

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

    resp = target.createOrder(member_info.Id, items, coupon_Id, params=params)

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


@route_api.route("/order/list")
def myIndex():
    resp = {'code': 200, 'msg': "操作成功", 'data': {}}
    req = request.values
    member_info = g.member_info

    status = int(req['status']) if 'status' in req else 0
    query = PayOrder.query.filter_by(member_id=member_info.Id)

    if status == -8:
        query = query.filter(PayOrder.status == -8)
    elif status == -7:  # 待发货
        query = query.filter(PayOrder.status == 1, PayOrder.express_status == -7, PayOrder.comment_status == 0)
    elif status == -6:  # 待确认
        query = query.filter(PayOrder.status == 1, PayOrder.express_status == -6, PayOrder.comment_status == 0)
    elif status == -5:
        query = query.filter(PayOrder.status == 1, PayOrder.express_status == 1, PayOrder.comment_status == 0)
    elif status == 1:
        query = query.filter(PayOrder.status == 1, PayOrder.express_status == 1)
    else:
        query = query.filter(PayOrder.status == 0)

    pay_order_list = query.order_by(PayOrder.id.desc()).all()
    data_pay_order_list = []
    if pay_order_list:
        pay_order_ids = selectFilterObj(pay_order_list, "id")
        pay_order_item_list = PayOrderItem.query.filter(PayOrderItem.pay_order_id.in_(pay_order_ids)).all()
        food_ids = selectFilterObj(pay_order_item_list, "food_id")
        food_map = getDictFilterField(Shop_Info, Shop_Info.Id, "Id", food_ids)
        pay_order_item_map = {}
        if pay_order_item_list:
            for item in pay_order_item_list:
                if item.pay_order_id not in pay_order_item_map:
                    pay_order_item_map[item.pay_order_id] = []

                tmp_food_info = food_map[item.food_id]
                pay_order_item_map[item.pay_order_id].append({
                    'id': item.id,
                    'food_id': item.food_id,
                    'quantity': item.quantity,
                    'pic_url': UrlManager.buildImageUrl(tmp_food_info.ShopImageUrl),
                    'name': tmp_food_info.ShopName
                })

        for item in pay_order_list:
            tmp_data = {
                'status': item.pay_status,
                'status_desc': item.status_desc,
                'date': item.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                'order_number': item.order_number,
                'order_sn': item.order_sn,
                'note': item.note,
                'total_price': str(item.total_price),
                'goods_list': pay_order_item_map[item.id]
            }

            data_pay_order_list.append(tmp_data)

    resp['data']['pay_order_list'] = data_pay_order_list
    return jsonify(resp)


@route_api.route("/order/info", methods=['GET', 'POST'])
def myOrderInfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    member_info = g.member_info
    req = request.values
    order_sn = req['order_sn'] if 'order_sn' in req else ''
    pay_order_info = PayOrder.query.filter_by(member_id=member_info.Id, order_sn=order_sn).first()
    if not pay_order_info:
        resp['code'] = -1
        resp['msg'] = "系统繁忙，请稍后再试~~"
        return jsonify(resp)

    tmp_deadline = pay_order_info.created_time + datetime.timedelta(minutes=30)
    info = {
        "order_sn": pay_order_info.order_sn,
        "status": pay_order_info.pay_status,
        "status_desc": pay_order_info.status_desc,
        "pay_price": str(pay_order_info.pay_price),
        "yun_price": str(pay_order_info.yun_price),
        "total_price": str(pay_order_info.total_price),
        "goods": [],
        "deadline": tmp_deadline.strftime("%Y-%m-%d %H:%M")
    }

    pay_order_items = PayOrderItem.query.filter_by(pay_order_id=pay_order_info.id).all()
    if pay_order_items:
        food_ids = selectFilterObj(pay_order_items, "food_id")
        food_map = getDictFilterField(Shop_Info, Shop_Info.Id, "Id", food_ids)
        for item in pay_order_items:
            tmp_food_info = food_map[item.food_id]
            tmp_data = {
                "name": tmp_food_info.ShopName,
                "price": str(item.price),
                "unit": item.quantity,
                "pic_url": UrlManager.buildImageUrl(tmp_food_info.ShopImageUrl),
            }
            info['goods'].append(tmp_data)
    resp['data']['info'] = info
    return jsonify(resp)


@route_api.route("/order/callback", methods=["POST"])
def orderCallback():
    result_data = {
        'return_code': 'SUCCESS',
        'return_msg': 'OK'
    }

    header = {'Content-Type': 'application/xml'}
    config_mina = app.config['MINA_APP']

    target_wechat = WeChatService(merchant_key=config_mina['paykey'])
    callback_data = target_wechat.xml_to_dict(request.data)

    sign = callback_data['sign']
    callback_data.pop('sign')
    gene_sign = target_wechat.create_sign(callback_data)

    if sign != gene_sign:
        result_data['return_code'] = result_data['return_msg'] = "FAIL1"
        return target_wechat.dict_to_xml(result_data), header

    order_sn = callback_data['out_trade_no']
    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info:
        result_data['return_code'] = result_data['return_msg'] = "FAIL2"
        return target_wechat.dict_to_xml(result_data), header

    if pay_order_info.status == 1:
        return target_wechat.dict_to_xml(result_data), header

    target_pay = PayService()
    qurl = createQrCode_Url(pay_order_info)
    target_pay.orderSuccess(pay_order_info.id, params={'pay_sn': callback_data['transaction_id'], 'qrcode_url': qurl})

    # 生成二维码


    # 微信回调加入日志
    target_pay.addPayCallbackData(pay_order_id=pay_order_info.id, data=request.data)

    return target_wechat.dict_to_xml(result_data), header


@route_api.route("/order/ops", methods=["POST"])
def orderOps():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    member_info = g.member_info
    order_sn = req['order_sn'] if 'order_sn' in req else ''
    act = req['act'] if 'act' in req else ''
    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn, member_id=member_info.id).first()
    if not pay_order_info:
        resp['code'] = -1
        resp['msg'] = "系统繁忙,请稍后再试"
        return jsonify(resp)

    if act == "cancel":
        target_pay = PayService()
        ret = target_pay.closeOrder(pay_order_id=pay_order_info.id)
        if not ret:
            resp['code'] = -1
            resp['msg'] = "系统繁忙,请稍后再试"
            return jsonify(resp)
    elif act == "confirm":
        pay_order_info.express_status = 1
        pay_order_info.updated_time = getCurrentDate()
        db.session.add(pay_order_info)
        db.session.commit()

    return jsonify(resp)
