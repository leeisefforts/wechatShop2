from flask import Blueprint, request, jsonify, redirect
from common.libs.UploadService import UploadService
from common.libs.UrlManager import UrlManager
from common.modal.shop_info import Shop_Info
from common.libs.WebHelper import getCurrentDate
from application import app, db
import re, json

route_upload = Blueprint('upload_page', __name__)


@route_upload.route('/edit', methods=['GET', 'POST'])
def edit():
    resp = {'code': '200', 'msg': '操作成功'}
    file_target = request.files
    req = request.values
    if len(file_target) > 0:
        img_url = uploadImg(file_target)
    else:
        img_url = req['ShopImageUrl']


    if len(req['shopname']) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入商品名'

    if len(req['shopdesc']) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入商品描述'

    if req['merchant'] and int(req['merchant']) < 0:
        resp['code'] = -1
        resp['msg'] = '请选择商家'

    if req['price'] and int(req['price']) < 0:
        resp['code'] = -1
        resp['msg'] = '请输入价格'

    if req['price'] < req['floorprice']:
        resp['code'] = -1
        resp['msg'] = '当前售价不能小于底价'


    info = Shop_Info.query.filter_by(Id=req['id']).first()
    if info:
        modal_shop = info
    else:
        modal_shop = Shop_Info()
        modal_shop.CreatTime = getCurrentDate()
        modal_shop.ShopStatus = 1

    modal_shop.ShopName = req['shopname']
    modal_shop.ShopDesc = req['shopdesc']
    modal_shop.ShopFloorPrice = req['price']
    modal_shop.ShopPrice = req['floorprice']
    modal_shop.ShopImageUrl = img_url
    modal_shop.ShopMerchantId = req['merchant']

    modal_shop.UpdateTime = getCurrentDate()

    db.session.add(modal_shop)
    db.session.commit()
    return redirect(UrlManager.buildUrl("/admin/commodity"))


def uploadImg(file_target):
    file_target = request.files
    upfile = file_target['pic'] if 'pic' in file_target else None
    if upfile is None:
        url = ''

    ret = UploadService.uploadByFile(upfile)

    url = ret['data']['file_key']
    return url
