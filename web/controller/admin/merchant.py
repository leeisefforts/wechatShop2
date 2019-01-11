from web.controller.admin import route_admin
from common.libs.WebHelper import ops_render, iPagination
from flask import request, g, jsonify
from application import app, db
from sqlalchemy import or_
from common.modal.merchant_info import Merchant_Info
from common.modal.Blance_Log import Balance_Log

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


@route_admin.route('/merchant/edit', methods=['GET', 'POST'])
def medit():
    resp = {'code': 200, 'msg': '审核成功'}
    req = request.values
    id = req['id']
    status = req['status']
    mer = Merchant_Info.query.filter_by(Id=id).first()
    mer.Status = status

    db.session.add(mer)
    db.session.commit()

    return jsonify(resp)


@route_admin.route('/balance_info')
def balance_info_admin():
    resp = {'code': 200, 'msg': '查询成功'}
    req = request.values
    merchantId = req['id'] if 'id' in req else -1
    merchant_info = Merchant_Info.query.filter_by(Id=merchantId).first()
    list = Balance_Log.query.filter_by(merchant_id=merchantId).all()
    tmp_list = []
    for item in list:
        tmp_data = {
            'id': item.id,
            'merchant_id': item.merchant_id,
            'merchant_name': merchant_info.Name,
            'createtime': item.createtime,
            'updatetime': item.updatetime,
            'status_Desc': item.Status_Desc,
            'balance': str(item.balance),
            'operating_Desc': str(item.Operating_Desc),
            'status': str(item.status),
            'operating': str(item.operating),
            'total_balance': str(item.total_balance),
            'receipt_qrcode': item.receipt_qrcode
        }
        tmp_list.append(tmp_data)
    resp['list'] = tmp_list
    return ops_render("admin/balance_info.html", resp)


@route_admin.route('/receipt')
def balance_list_admin():
    resp = {'code': 200, 'msg': '查询成功'}
    req = request.values

    list = Balance_Log.query.order_by(Balance_Log.id.desc()).all()
    tmp_list = []
    for item in list:
        merchant_info = Merchant_Info.query.filter_by(Id=item.merchant_id).first()
        tmp_data = {
            'id': item.id,
            'merchant_id': item.merchant_id,
            'merchant_name': merchant_info.Name,
            'createtime': item.createtime,
            'updatetime': item.updatetime,
            'status_Desc': item.Status_Desc,
            'balance': str(item.balance),
            'operating_Desc': str(item.Operating_Desc),
            'status': str(item.status),
            'operating': str(item.operating),
            'total_balance': str(item.total_balance),
            'receipt_qrcode': item.receipt_qrcode
        }
        tmp_list.append(tmp_data)
    resp['list'] = tmp_list
    return ops_render("admin/report.html", resp)


@route_admin.route('/receipt/edit', methods=['POST'])
def recepit_edit():
    resp = {'code': 200, 'msg': '操作成功'}
    req = request.values
    id = req['id'] if 'id' in req else 0
    info = Balance_Log.query.filter_by(id=id).first()
    info.status = 5
    info.total_balance -= info.freeze_balance
    info.freeze_balance = 0
    db.session.add(info)
    db.session.commit()

    m_info = Merchant_Info.query.filter_by(Id=info.merchant_id).first()
    m_info.TotalBalance -= m_info.FreezeBalance
    m_info.FreezeBalance = 0
    db.session.add(m_info)
    db.session.commit()
    return jsonify(resp)
