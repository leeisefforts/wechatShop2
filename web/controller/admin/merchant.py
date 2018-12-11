from web.controller.admin import route_admin
from common.libs.WebHelper import ops_render, iPagination
from flask import request, g, jsonify
from application import app
from sqlalchemy import or_
from common.modal.merchant_info import Merchant_Info

import json, datetime


@route_admin.route('/merchant', methods=['GET', 'POST'])
def merchant():
    resq = {}
    if request.method == 'GET':
        resq = {}
        req = request.values
        query = Merchant_Info.query
        page = int(req['p']) if ('p' in req and req['p']) else 1

        if 'mix_kw' in req:
            rule = or_(Merchant_Info.UserName.ilike("%{0}%".format(req['mix_kw'])),
                       Merchant_Info.Phone.ilike("%{0}%".format(req['mix_kw'])))
            query = query.filter(rule)

        if 'status' in req and int(req['status']) > -1:
            query = query.filter(Merchant_Info.Status == int(req['status']))

        count = query.count()
        page_params = {
            'total': count,
            'page_size': app.config['PAGE_SIZE'],
            'page': page,
            'display': app.config['PAGE_DISPLAY'],
            'url': request.full_path.replace("&p={}".format(page), "")
        }
        pages = iPagination(page_params)
        offset = (page - 1) * app.config['PAGE_SIZE']
        limit = app.config['PAGE_SIZE'] * page
        list = query.order_by(Merchant_Info.Id.desc()).all()
        resq['list'] = list
        resq['pages'] = pages
        resq['search_con'] = req
        resq['status_mapping'] = app.config['STATUS_MAPPING']
        return ops_render("admin/index.html", resq)
