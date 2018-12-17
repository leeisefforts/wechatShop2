from flask import render_template, g
from application import app, db
from common.modal.pay.payOrder import PayOrder
from common.modal.coupon_info import Coupon_Info
from werkzeug.utils import secure_filename
from common.libs.UrlManager import UrlManager
import datetime, qrcode

'''
统一渲染
'''


def ops_render(template, context={}):
    if 'current_user' in g:
        if g.current_user:
            g.current_user.Id = str(g.current_user.Id)  # 不知道为什么路由需要str类型
        context['current_user'] = g.current_user

    return render_template(template, **context)


'''
自定义分页类
'''


def iPagination(params):
    import math

    ret = {
        "is_prev": 1,
        "is_next": 1,
        "from": 0,
        "end": 0,
        "current": 0,
        "total_pages": 0,
        "page_size": 0,
        "total": 0,
        "url": params['url']
    }

    total = int(params['total'])
    page_size = int(params['page_size'])
    page = int(params['page'])
    display = int(params['display'])
    total_pages = int(math.ceil(total / page_size))
    total_pages = total_pages if total_pages > 0 else 1
    if page <= 1:
        ret['is_prev'] = 0

    if page >= total_pages:
        ret['is_next'] = 0

    semi = int(math.ceil(display / 2))

    if page - semi > 0:
        ret['from'] = page - semi
    else:
        ret['from'] = 1

    if page + semi <= total_pages:
        ret['end'] = page + semi
    else:
        ret['end'] = total_pages

    ret['current'] = page
    ret['total_pages'] = total_pages
    ret['page_size'] = page_size
    ret['total'] = total
    ret['range'] = range(ret['from'], ret['end'] + 1)
    return ret


'''
获取当前时间
'''


def getCurrentDate(format="%Y-%m-%d %H:%M:%S"):
    # return datetime.datetime.now().strftime( format )
    return datetime.datetime.now()


'''
获取格式化的时间
'''


def getFormatDate(date=None, format="%Y-%m-%d %H:%M:%S"):
    if date is None:
        date = datetime.datetime.now()

    return date.strftime(format)


def selectFilterObj(obj, filed):
    ret = []
    for item in obj:
        if not hasattr(item, filed):
            continue
        if getattr(item, filed) in ret:
            continue

        ret.append(getattr(item, filed))

    return ret


def getDictListFilterField(db_model, select_filed, key_field, id_list):
    ret = {}
    query = db_model.query
    if id_list and len(id_list) > 0:
        query = query.filter(select_filed.in_(id_list))

    list = query.all()
    if not list:
        return ret
    for item in list:
        if not hasattr(item, key_field):
            break
        if getattr(item, key_field) not in ret:
            ret[getattr(item, key_field)] = []

        ret[getattr(item, key_field)].append(item)
    return ret


def getDictFilterField(db_model, select_filed, key_field, id_list):
    ret = {}
    query = db_model.query
    if id_list and len(id_list) > 0:
        query = query.filter(select_filed.in_(id_list))

    list = query.all()
    if not list:
        return ret
    for item in list:
        if not hasattr(item, key_field):
            break

        ret[getattr(item, key_field)] = item
    return ret


def createQrCode_Url(pay_order_info):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    url = app.config["APP"]["domain"] + '/api/coupon/writeoff?order_sn=' + pay_order_info.order_sn + '&couponId=-1'
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image()
    filename = secure_filename(pay_order_info.order_sn + '.png')
    filepath = app.root_path + '/web/static/qrcode/' + filename
    img.save(filepath)

    info = Coupon_Info.query.filter(Order_sn=pay_order_info.order_sn).first()
    if info:
        info.QrCode_Url = filepath
        db.session.add(info)
        db.session.commit()
    return filepath
