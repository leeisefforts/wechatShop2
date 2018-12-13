from application import app, db
from flask import jsonify, request, g
from web.controller.api import route_api
from common.modal.wxShare import WxShareHistory
from common.libs.WebHelper import getCurrentDate
from common.libs.MemberService import MemberService
from common.modal.member import Member
from common.modal.OauthMemberBind import OauthMemberBind


@route_api.route("/member/login", methods=["GET", "POST"])
def login():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = "需要code"
        return jsonify(resp)

    openid = MemberService.getWeChatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用微信出错"
        return jsonify(resp)

    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''
    city = req['city'] if 'city' in req else ''
    '''
        判断是否已经测试过，注册了直接返回一些信息
    '''
    bind_info = OauthMemberBind.query.filter_by(Openid=openid, Type=1).first()
    if not bind_info:
        model_member = Member()
        model_member.Nickname = nickname
        model_member.Sex = sex
        model_member.Avatar = avatar
        model_member.City = city
        model_member.Salt = MemberService.geneSalt()
        model_member.UpdatedTime = model_member.CreatedTime = getCurrentDate()
        db.session.add(model_member)
        db.session.commit()

        model_bind = OauthMemberBind()
        model_bind.Member_id = model_member.Id
        model_bind.Type = 1
        model_bind.Openid = openid
        model_bind.Extra = ''
        model_bind.UpdateTime = model_bind.CreatTime = getCurrentDate()
        db.session.add(model_bind)
        db.session.commit()

        bind_info = model_bind

    member_info = Member.query.filter_by(Id=bind_info.Member_id).first()
    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.Id)
    resp['data'] = {'token': token, 'openId':openid}
    return jsonify(resp)


@route_api.route("/member/share", methods=["POST"])
def memberShare():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    url = req['url'] if 'url' in req else ''
    member_info = g.member_info
    model_share = WxShareHistory()
    if member_info:
        model_share.member_id = member_info.id
    model_share.share_url = url
    model_share.created_time = getCurrentDate()
    db.session.add(model_share)
    db.session.commit()
    return jsonify(resp)


@route_api.route("/member/info")
def memberInfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    member_info = g.member_info
    resp['data']['info'] = {
        "nickname": member_info.Nickname,
        "avatar_url": member_info.Avatar
    }
    return jsonify(resp)
