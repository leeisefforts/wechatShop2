from flask import Blueprint, request, jsonify, make_response, g, redirect
from application import db, app
from common.libs.WebHelper import ops_render, getFormatDate
from common.libs.UserService import UserService
from common.libs.UrlManager import UrlManager
from common.modal.s_userinfo import S_User_Info
from common.modal.stat.statDailySite import StatDailySite
import json, datetime

route_index = Blueprint('index_page', __name__)


@route_index.route("/")
@route_index.route('/index', methods=['GET', 'POST'])
def index():
    resp_data = {
        'data': {
            'finance': {
                'today': 0,
                'month': 0
            },
            'member': {
                'today_new': 0,
                'month_new': 0,
                'total': 0
            },
            'order': {
                'today': 0,
                'month': 0
            },
            'shared': {
                'today': 0,
                'month': 0
            },
        }
    }

    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    date_to = getFormatDate(date=now, format="%Y-%m-%d")

    list = StatDailySite.query.filter(StatDailySite.date >= date_from) \
        .filter(StatDailySite.date <= date_to).order_by(StatDailySite.id.asc()) \
        .all()
    data = resp_data['data']
    if list:

        for item in list:
            data['finance']['month'] += item.total_pay_money
            data['member']['month_new'] += item.total_new_member_count
            data['member']['total'] = item.total_member_count
            data['order']['month'] += item.total_order_count
            data['shared']['month'] += item.total_shared_count
            if getFormatDate(date=item.date, format="%Y-%m-%d") == date_to:
                data['finance']['today'] = item.total_pay_money
                data['member']['today_new'] = item.total_new_member_count
                data['order']['today'] = item.total_order_count
                data['shared']['today'] = item.total_shared_count

    return ops_render("index.html", resp_data)


@route_index.route("/logout")
def logout():
    response = make_response(redirect(UrlManager.buildUrl("/login")))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response


@route_index.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        if g.current_user:
            return redirect(UrlManager.buildUrl("/admin/index"))
        return ops_render('login.html')

    result = {'code': 200, 'msg': '登录成功'}
    value = request.values
    login_name = value['login_name'] if 'login_name' in value else ''
    login_pwd = value['login_pwd'] if 'login_pwd' in value else ''

    if login_name is None or len(login_name) < 1:
        result['code'] = -1
        result['msg'] = 'error'
        return jsonify(result)

    if login_pwd is None or len(login_pwd) < 1:
        result['code'] = -1
        result['msg'] = 'error'
        return jsonify(result)

    user_info = S_User_Info.query.filter_by(UserName=login_name).first()
    if not user_info:
        result['code'] = -1
        result['msg'] = '账号错误'
        return jsonify(result)

    if user_info.UserPwd != login_pwd:
        result['code'] = -1
        result['msg'] = '密码错误'
        return jsonify(result)

    response = make_response(json.dumps(result))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], "%s#%s" % (UserService.geneAuthCode(user_info), user_info.Id))

    return response
