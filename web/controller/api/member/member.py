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

import random, decimal


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
    avatarUrl = req['avatarUrl'] if 'toOpenId' in req else ''
    nickName = req['nickName'] if 'toOpenId' in req else ''

    member_info = g.member_info
    model_share = WxShareHistory()
    if member_info:
        model_share.Member_Id = member_info.Id
    model_share.Share_Url = url
    model_share.Shop_Id = shopId
    model_share.ToOpenId = toOpenId
    model_share.ToNickName = nickName
    model_share.ToAvatar = avatarUrl
    model_share.CreateTime = getCurrentDate()
    db.session.add(model_share)
    db.session.commit()

    shop_info = Shop_Info.query.filter_by(Id=shopId).first()
    rule = and_(Coupon_Info.Member_Id == member_info.Id, Coupon_Info.ShopId == shopId)
    coupon_info = Coupon_Info.query.filter(rule).first()

    coupon_price = 0
    if coupon_info:
        modal_coupon = coupon_info
        modal_coupon.UpdateTime = getCurrentDate()
        coupon_price = modal_coupon.Price
    else:
        modal_coupon = Coupon_Info()
        modal_coupon.Coupon_Name = (shop_info.ShopName + '-' + member_info.Nickname)
        modal_coupon.ShopId = shopId
        modal_coupon.Member_Id = member_info.Id
        modal_coupon.Price = shop_info.ShopPrice
        modal_coupon.Status = 1
        modal_coupon.CreateTime = modal_coupon.UpdateTime = getCurrentDate()

    pp = shop_info.ShopPrice - shop_info.ShopFloorPrice if coupon_price == 0 else coupon_price - shop_info.ShopFloorPrice
    yhprice = random.randint(0, int(pp))
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
