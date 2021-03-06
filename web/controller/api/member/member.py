from application import app, db
from flask import jsonify, request, g
from web.controller.api import route_api
from common.modal.wxShare import WxShareHistory
from common.libs.WebHelper import getCurrentDate
from common.libs.MemberService import MemberService
from common.modal.member import Member
from common.modal.OauthMemberBind import OauthMemberBind
from common.modal.coupon_info import Coupon_Info
from common.modal.shop_info import Shop_Info
from sqlalchemy import and_

import random, decimal, datetime


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
    resp['data'] = {'token': token, 'openId': openid}
    return jsonify(resp)


@route_api.route("/member/share", methods=["POST"])
def memberShare():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    url = req['url'] if 'url' in req else ''
    shopId = req['shopId'] if 'shopId' in req else 0
    toOpenId = req['toOpenId'] if 'toOpenId' in req else ''
    memberId = req['memberId'] if 'memberId' in req else ''
    avatarUrl = req['avatarUrl'] if 'toOpenId' in req else ''
    nickName = req['nickName'] if 'toOpenId' in req else ''
    coupon_id = req['coupon_id'] if 'coupon_id' in req else ''

    member_info = Member.query.filter_by(Id=memberId).first()
    shop_info = Shop_Info.query.filter_by(Id=shopId).first()

    if member_info.Id == g.member_info.Id:
        resp['code'] = -1
        resp['msg'] = '不能给自己砍价'
        return jsonify(resp)

    coupon_price = 0
    if coupon_id and coupon_id != '0':
        modal_coupon = Coupon_Info.query.filter_by(Id=coupon_id).first()
        modal_coupon.UpdateTime = getCurrentDate()
        coupon_price = modal_coupon.Price
    else:
        modal_coupon = Coupon_Info()
        modal_coupon.Coupon_Name = (shop_info.ShopName + '-' + member_info.Nickname + '- 优惠券')
        modal_coupon.ShopId = shopId
        modal_coupon.Member_Id = member_info.Id
        modal_coupon.Price = shop_info.ShopPrice
        modal_coupon.Status = 1
        modal_coupon.CreateTime = modal_coupon.UpdateTime = getCurrentDate()
    if modal_coupon.Price == shop_info.ShopFloorPrice:
        resp['code'] = -1
        resp['msg'] = '已经是最低价了'
        return jsonify(resp)
    model_share = WxShareHistory()
    rule = and_(WxShareHistory.Coupon_Id == modal_coupon.Id, WxShareHistory.ToOpenId == toOpenId)
    ss = WxShareHistory.query.filter(rule).first()
    if ss:
        resp['code'] = -1
        resp['msg'] = '你已经帮忙砍过价了'
        return jsonify(resp)
    if member_info:
        model_share.Member_Id = member_info.Id
    model_share.Share_Url = url
    model_share.Shop_Id = shopId
    model_share.ToOpenId = toOpenId
    model_share.ToNickName = nickName
    model_share.ToAvatar = avatarUrl
    model_share.CreateTime = getCurrentDate()
    model_share.Coupon_Id = -1
    db.session.add(model_share)
    db.session.commit()

    pp = shop_info.ShopPrice - shop_info.ShopFloorPrice if coupon_price == 0 else coupon_price - shop_info.ShopFloorPrice
    yhprice = random.randint(1, int(pp))
    model_share.Price = yhprice
    if yhprice >= pp:
        modal_coupon.Price = shop_info.ShopFloorPrice  # 如果优惠金额低于底价 直接变成底价
        modal_coupon.Coupon_Price = decimal.Decimal(shop_info.ShopPrice - shop_info.ShopFloorPrice)
        modal_coupon.Status = 2  # 无法再进行砍价
    else:
        modal_coupon.Price -= yhprice
        pprice = modal_coupon.Coupon_Price
        if pprice:
            modal_coupon.Coupon_Price = decimal.Decimal(pprice) + decimal.Decimal(yhprice)
        else:
            modal_coupon.Coupon_Price = decimal.Decimal(yhprice)

    db.session.add(modal_coupon)
    db.session.commit()
    model_share.Coupon_Id = modal_coupon.Id
    db.session.add(model_share)
    db.session.commit()
    data = {
        'coupon_price': str(model_share.Price)
    }
    resp['data'] = data
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


@route_api.route("/share/list")
def share_list():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else -1
    list = WxShareHistory.query.filter_by(Coupon_Id=id).all()
    tmp_list = []
    for item in list:
        data = {
            'Id': item.Id,
            'ToOpenId': item.ToOpenId,
            'ToNickName': item.ToNickName,
            'ToAvatar': item.ToAvatar,
            'Price': str(item.Price),
            'CreateTime': item.CreateTime,
            'Shop_Id': item.Shop_Id,
            'Coupon_Id': item.Coupon_Id
        }
        tmp_list.append(data)
    resp['data'] = tmp_list
    return jsonify(resp)
