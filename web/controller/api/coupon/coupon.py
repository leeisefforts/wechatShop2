from application import app, db
from web.controller.api import route_api
from common.modal.coupon_info import Coupon_Info
from common.modal.merchant_info import Merchant_Info
from common.modal.Blance_Log import Balance_Log
from common.modal.shop_info import Shop_Info
from common.modal.pay.payOrderItem import PayOrderItem
from common.modal.pay.payOrder import PayOrder
from common.libs.WebHelper import getCurrentDate
from common.libs.UrlManager import UrlManager
from common.modal.shop_info import Shop_Info
from flask import jsonify, request, g, redirect
from sqlalchemy import or_
import json, decimal


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

    shop_list = query.order_by(Coupon_Info.Id.desc()).all()

    data_food_list = []
    if shop_list:
        for item in shop_list:
            s_info = Shop_Info.query.filter_by(Id=item.ShopId).first()
            tmp_data = {
                'id': item.Id,
                'name': "%s" % (item.Coupon_Name),
                'price': str(item.Coupon_Price),
                'min_price': str(item.Price),
                'createTime': str(item.CreateTime),
                'status': str(item.Status),
                'shop_info': {

                }
            }
            if s_info:
                tmp_data['shop_info'] = {
                    'id': s_info.Id,
                    'name': "%s" % (s_info.ShopName),
                    'desc': "%s" % (s_info.ShopDesc),
                    'price': str(s_info.ShopPrice),
                    'min_price': str(s_info.ShopFloorPrice),
                    'stock': str(s_info.Stock),
                    'totalCount': str(s_info.TotalCount),
                    'pic_url': UrlManager.buildImageUrl(s_info.ShopImageUrl)
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

    if info:
        resp['data'] = {
            'name': info.Coupon_Name,
            'price': str(info.Coupon_Price),
            'min_price': str(info.Price),
            'qrCode_Url': app.config["APP"][
                              "domain"] + UrlManager.buildStaticUrl(info.QrCode_Url) if info.QrCode_Url else '',
            'status': str(info.Status),
            'shop_info': {

            }
        }

        s_info = Shop_Info.query.filter_by(Id=info.ShopId).first()
        if s_info:
            merchant = Merchant_Info.query.filter_by(Id=s_info.ShopMerchantId).first()
            resp['merchant'] = {
                'name': merchant.Name,
                'address': merchant.Address,
                'imageUrl': merchant.ImageUrl,
                'phone': merchant.Phone
            }
            resp['data']['shop_info'] = {
                'id': s_info.Id,
                'name': "%s" % (s_info.ShopName),
                'desc': "%s" % (s_info.ShopDesc),
                'price': str(s_info.ShopPrice),
                'min_price': str(s_info.ShopFloorPrice),
                'stock': str(s_info.Stock),
                'totalCount': str(s_info.TotalCount),
                'pic_url': UrlManager.buildImageUrl(s_info.ShopImageUrl)
            }
    return jsonify(resp)


@route_api.route('/coupon/writeoff', methods=['GET', 'POST'])
def writeoff():
    resp = {'code': 200, 'msg': '操作成功'}
    req = request.values
    order_sn = req['order_sn'] if 'order_sn' in req else ''
    couponId = req['couponId'] if 'couponId' in req else ''
    merchantId = req['merchantId'] if 'merchantId' in req else ''

    order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    coupon_info = Coupon_Info.query.filter_by(Id=couponId).first()
    merchant_info = Merchant_Info.query.filter_by(Id=merchantId).first()

    if order_info:
        shop_id = PayOrderItem.query.filter_by(pay_order_id=order_info.id).first().food_id

        shopMerchantId = Shop_Info.query.filter_by(Id=shop_id).first().ShopMerchantId
        if int(shopMerchantId) != int(merchantId):
            resp['code'] = -1
            resp['msg'] = '商户不匹配'
            return jsonify(resp)

        order_info.express_status = 1
        db.session.add(order_info)
        db.session.commit()

    if coupon_info:
        coupon_info.Status = 4
        db.session.add(coupon_info)
        db.session.commit()

    # 计算余额
    merchant_info.TotalBalance += order_info.total_price
    db.session.add(merchant_info)
    db.session.commit()

    # 余额写入日志
    balance_log = Balance_Log()
    balance_log.createtime = balance_log.updatetime = getCurrentDate()
    balance_log.status = 1
    balance_log.merchant_id = merchantId,
    balance_log.operating = 1,  # 1 添加操作
    balance_log.balance = order_info.total_price
    balance_log.total_balance = merchant_info.TotalBalance
    balance_log.freeze_balance = 0
    db.session.add(balance_log)
    db.session.commit()
    return jsonify(resp)


@route_api.route('/receipt', methods=['POST'])
def receipt_balance():
    resp = {'code': 200, 'msg': '提现申请已提交'}
    req = request.values
    merchantId = req['merchantId'] if 'merchantId' in req else -1
    balance = req['balance'] if 'balance' in req else 0
    receipt_qrcode = req['qrcode'] if 'qrcode' in req else ''

    merchant_info = Merchant_Info.query.filter_by(Id=merchantId).first()
    merchant_info.FreezeBalance = decimal.Decimal(balance)
    merchant_info.TotalBalance -= merchant_info.FreezeBalance

    balance_log = Balance_Log()
    balance_log.createtime = balance_log.updatetime = getCurrentDate()
    balance_log.status = 4
    balance_log.merchant_id = merchantId,
    balance_log.operating = 4,  # 4 提现申请  status =1 提现审核 status=2 已提现
    balance_log.balance = balance
    balance_log.total_balance = merchant_info.TotalBalance
    balance_log.freeze_balance = merchant_info.FreezeBalance
    balance_log.receipt_qrcode = receipt_qrcode
    db.session.add(balance_log)
    db.session.commit()
    return jsonify(resp)
