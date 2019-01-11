import decimal, hashlib, time, random, json
from application import db, app

from common.modal.shop_info import Shop_Info
from common.modal.pay.payOrder import PayOrder
from common.modal.pay.payordercallbackData import PayOrderCallbackData
from common.modal.pay.payOrderItem import PayOrderItem
from common.modal.shopSaleChangeLog import ShopSaleChangeLog
from common.modal.coupon_info import Coupon_Info
from common.libs.WebHelper import getCurrentDate
from common.libs.queueService import QueueService


class PayService():
    def __init__(self):
        pass

    def createOrder(self, member_id, items=None, coupon_Id=None, params=None, ):
        resp = {'code': 200, 'msg': "操作成功", 'data': {}}

        pay_price = decimal.Decimal(0.00)
        continue_count = 0
        foods_id = []
        items = [items]
        for item in items:
            if decimal.Decimal(item['price']) < 0:
                continue_count += 1
                continue
            pay_price = pay_price + decimal.Decimal(item['price'])
            foods_id.append(item['id'])

        if continue_count >= len(items):
            resp['code'] = -1
            resp['msg'] = "商品为空"
            return resp

        yun_price = 0
        note = ''

        yun_price = decimal.Decimal(yun_price)
        total_price = yun_price + pay_price

        # 并发处理
        try:
            # 开启事务
            tmp_food_list = db.session.query(Shop_Info).filter(Shop_Info.Id.in_(foods_id)).with_for_update().all()

            tmp_food_stock_mapping = {}
            for tmp_item in tmp_food_list:
                tmp_food_stock_mapping[tmp_item.Id] = tmp_item.Stock

            order_sn = self.geneOrderSn()
            if coupon_Id:
                coupon_info = Coupon_Info.query.filter_by(Id=coupon_Id).first()
                if coupon_info:
                    coupon_info.Order_sn = order_sn
                    total_price -= coupon_info.Coupon_Price
                    db.session.add(coupon_info)
            # 支付订单
            model_pay_order = PayOrder()
            model_pay_order.member_id = member_id
            model_pay_order.order_sn = order_sn
            model_pay_order.total_price = total_price
            model_pay_order.yun_price = yun_price
            model_pay_order.pay_price = pay_price
            model_pay_order.note = note
            model_pay_order.status = -8
            model_pay_order.express_status = -8
            model_pay_order.updated_time = model_pay_order.created_time = getCurrentDate()
            db.session.add(model_pay_order)

            for item in items:
                tmp_left_stock = tmp_food_stock_mapping[item['id']]
                if decimal.Decimal(item['price']) < 0:
                    continue
                if 1 > int(tmp_left_stock):  # int(item['number'])
                    raise Exception("该商品剩余: %s" % (tmp_left_stock))

                tmp_ret = Shop_Info.query.filter_by(Id=item['id']).update({
                    'Stock': int(tmp_left_stock) - 1
                })

                if not tmp_ret:
                    raise Exception("下单失败")

                tmp_pay_item = PayOrderItem()
                tmp_pay_item.pay_order_id = model_pay_order.id
                tmp_pay_item.member_id = member_id
                tmp_pay_item.quantity = 1
                tmp_pay_item.price = item['price']
                tmp_pay_item.food_id = item['id']
                tmp_pay_item.note = note
                tmp_pay_item.updated_time = tmp_pay_item.created_time = getCurrentDate()

                db.session.add(tmp_pay_item)

            # 提交事务
            db.session.commit()
            resp['data'] = {
                'id': model_pay_order.id,
                'order_sn': model_pay_order.order_sn,
                'total_price': str(model_pay_order.total_price)
            }

        except Exception as e:
            db.session.rollback()
            print(e)
            resp['code'] = -1
            resp['msg'] = "下单失败请重新下单"
            resp['msg'] = str(e)

        return resp

    def orderSuccess(self, pay_order_id=0, params=None):
        try:
            pay_order_info = PayOrder.query.filter_by(id=pay_order_id).first()
            if not pay_order_info or pay_order_info.status not in [-8, -7]:
                return True

            pay_order_info.pay_sn = params['pay_sn']
            pay_order_info.status = 1
            pay_order_info.express_status = -7
            pay_order_info.updated_time = getCurrentDate()
            pay_order_info.pay_time = getCurrentDate()
            db.session.add(pay_order_info)

            # 售卖记录
            pay_order_items = PayOrderItem.query.filter_by(pay_order_id=pay_order_id).all()
            for order_item in pay_order_items:
                tmp_model_sale_log = ShopSaleChangeLog()
                tmp_model_sale_log.food_id = order_item.food_id
                tmp_model_sale_log.quantity = order_item.quantity
                tmp_model_sale_log.price = order_item.price
                tmp_model_sale_log.member_id = order_item.member_id
                tmp_model_sale_log.created_time = getCurrentDate()

                db.session.add(tmp_model_sale_log)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return False

        QueueService.addQueue("pay", {
            "member_id": pay_order_info.member_id,
            "pay_order_id": pay_order_info.id
        })

    def addPayCallbackData(self, pay_order_id=0, type='pay', data=''):
        model_paycallback = PayOrderCallbackData()
        model_paycallback.pay_order_id = pay_order_id
        if type == "pay":
            model_paycallback.pay_data = data
            model_paycallback.refund_data = ''
        else:
            model_paycallback.pay_data = ''
            model_paycallback.refund_data = data
        model_paycallback.created_time = model_paycallback.updated_time = getCurrentDate()

        db.session.add(model_paycallback)
        db.session.commit()
        return True

    def geneOrderSn(self):
        m = hashlib.md5()
        sn = None
        while True:
            str = "%s-%s" % (int(round(time.time() * 1000)), random.randint(0, 9999999))
            m.update(str.encode("utf-8"))
            sn = m.hexdigest()
            if not PayOrder.query.filter_by(order_sn=sn).first():
                break

        return sn

    def closeOrder(self, pay_order_id=0):
        if pay_order_id < 1:
            return False
        pay_order_info = PayOrder.query.filter_by(id=pay_order_id, status=-8).first()
        if not pay_order_info:
            return False

        pay_order_items = PayOrderItem.query.filter_by(pay_order_id=pay_order_id).all()
        if pay_order_items:
            # 需要归还库存
            for item in pay_order_items:
                tmp_food_info = Shop_Info.query.filter_by(id=item.food_id).first()
                if tmp_food_info:
                    tmp_food_info.stock = tmp_food_info.stock + item.quantity
                    tmp_food_info.updated_time = getCurrentDate()
                    db.session.add(tmp_food_info)
                    db.session.commit()

        pay_order_info.status = 0
        pay_order_info.updated_time = getCurrentDate()
        db.session.add(pay_order_info)
        db.session.commit()
        return True
