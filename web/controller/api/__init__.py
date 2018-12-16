from flask import Blueprint
from common.libs.UploadService import UploadService
from flask import jsonify

route_api = Blueprint('api_page', __name__)

from web.controller.api.member.member import *
from web.controller.api.shop.shop import *
from web.controller.api.merchant.merchant import *
from web.controller.api.order.order import *
from web.controller.api.coupon.coupon import *


@route_api.route('/')
def index():
    return 'API Success'


@route_api.route('/upload', methods=['GET', 'POST'])
def upload():
    resp = {'code': 200, 'data': ''}
    file_target = request.files
    img_url = uploadImg(file_target)
    resp['data'] = img_url
    return jsonify(resp)


def uploadImg(file_target):
    file_target = request.files
    upfile = file_target['pic'] if 'pic' in file_target else None
    if upfile is None:
        url = ''

    ret = UploadService.uploadByFile(upfile)

    url = ret['data']['file_key']
    return url
