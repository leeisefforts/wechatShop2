from web.controller.api import route_api
from common.modal.shop_info import Shop_Info
from flask import request, jsonify, g
from common.libs.UrlManager import UrlManager
from sqlalchemy import or_


@route_api.route('/shoplist', methods=['GET', 'POST'])
def shoplist():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values

    mix_kw = str(req['mix_kw']) if 'mix_kw' in req else ''
    p = int(req['p']) if 'p' in req else 1

    if p < 1:
        p = 1

    page_size = 10
    offset = (p - 1) * page_size
    query = Shop_Info.query.filter_by(ShopStatus=1)

    if mix_kw:
        rule = or_(Shop_Info.ShopName.ilike("%{0}%".format(mix_kw)))
        query = query.filter(rule)

    shop_list = query.order_by(Shop_Info.Id.desc()) \
        .offset(offset).limit(page_size).all()

    data_food_list = []
    if shop_list:
        for item in shop_list:
            tmp_data = {
                'id': item.Id,
                'name': "%s" % (item.ShopName),
                'desc': "%s" % (item.ShopDesc),
                'price': str(item.ShopPrice),
                'min_price': str(item.ShopFloorPrice),
                'pic_url': UrlManager.buildImageUrl(item.ShopImageUrl)
            }
            data_food_list.append(tmp_data)
    resp['data']['list'] = data_food_list
    resp['data']['has_more'] = 0 if len(data_food_list) < page_size else 1
    return jsonify(resp)


@route_api.route('/shopinfo', methods=['GET', 'POST'])
def shopinfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.args
    id = req.get('id')

    info = Shop_Info.query.filter_by(Id=id).first()
    resp['data'] = {
        'id': info.Id,
        'name': "%s" % (info.ShopName),
        'desc': "%s" % (info.ShopDesc),
        'price': str(info.ShopPrice),
        'min_price': str(info.ShopFloorPrice),
        'stock': str(info.Stock),
        'totalCount': str(info.TotalCount),
        'pic_url': UrlManager.buildImageUrl(info.ShopImageUrl)
    }
    return jsonify(resp)
