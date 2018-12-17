from application import app, db
from common.libs.WebHelper import getFormatDate, getCurrentDate
from common.modal.member import Member
from common.modal.pay.payOrder import PayOrder
from common.modal.stat.statDailyFood import StatDailyFood
from common.modal.stat.statDailySite import StatDailySite
from common.modal.stat.statDailyMember import StatDailyMember
from common.modal.wxShare import WxShareHistory
from common.modal.shopSaleChangeLog import ShopSaleChangeLog
from sqlalchemy import func
import random

'''
python manager.py runjob -m stat/daily -a member|food|site -p 2018-07-01
'''


class JobTask():
    def __init__(self):
        pass

    def run(self, params):
        act = params['act'] if 'act' in params else ''
        date = params['param'][0] if params['param'] and len(params['param']) else getFormatDate(format="%Y-%m-%d")
        if not act:
            return

        date_from = date + " 00:00:00"
        date_to = date + " 23:59:59"
        func_params = {
            'act': act,
            'date': date,
            'date_from': date_from,
            'date_to': date_to
        }
        if act == "member":
            self.statMember(func_params)
        elif act == "food":
            self.statFood(func_params)
        elif act == "site":
            self.statSite(func_params)
        elif act == "test":
            self.test()

        app.logger.info("it's over~~")
        return

    '''
    会员统计
    '''

    def statMember(self, params):
        act = params['act']
        date = params['date']
        date_from = params['date_from']
        date_to = params['date_to']
        app.logger.info("act:{0},from:{1},to:{2}".format(act, date_from, date_to))

        member_list = Member.query.all()
        if not member_list:
            app.logger.info("no member list")
            return

        for member_info in member_list:
            tmp_stat_member = StatDailyMember.query.filter_by(date=date, member_id=member_info.Id).first()
            if tmp_stat_member:
                tmp_model_stat_member = tmp_stat_member
            else:
                tmp_model_stat_member = StatDailyMember()
                tmp_model_stat_member.date = date
                tmp_model_stat_member.member_id = member_info.Id
                tmp_model_stat_member.created_time = getCurrentDate()

            tmp_stat_pay = db.session.query(func.sum(PayOrder.total_price).label("total_pay_money")) \
                .filter(PayOrder.member_id == member_info.Id, PayOrder.status == 1) \
                .filter(PayOrder.created_time >= date_from, PayOrder.created_time <= date_to).first()
            tmp_stat_share_count = WxShareHistory.query.filter(PayOrder.member_id == member_info.Id) \
                .filter(PayOrder.created_time >= date_from, PayOrder.created_time <= date_to).count()

            tmp_model_stat_member.total_shared_count = tmp_stat_share_count
            tmp_model_stat_member.total_pay_money = tmp_stat_pay[0] if tmp_stat_pay[0] else 0.00
            '''
            为了测试效果模拟数据
            '''
            # tmp_model_stat_member.total_shared_count = random.randint(50, 100)
            # tmp_model_stat_member.total_pay_money = random.randint(1000, 1010)

            tmp_model_stat_member.updated_time = getCurrentDate()
            db.session.add(tmp_model_stat_member)
            db.session.commit()

        return

    '''
    Food统计
    '''

    def statFood(self, params):
        act = params['act']
        date = params['date']
        date_from = params['date_from']
        date_to = params['date_to']
        app.logger.info("act:{0},from:{1},to:{2}".format(act, date_from, date_to))

        stat_food_list = db.session.query(ShopSaleChangeLog.food_id,
                                          func.sum(ShopSaleChangeLog.quantity).label("total_count"),
                                          func.sum(ShopSaleChangeLog.price).label("total_pay_money")) \
            .filter(ShopSaleChangeLog.created_time >= date_from, ShopSaleChangeLog.created_time <= date_to) \
            .group_by(ShopSaleChangeLog.food_id).all()

        if not stat_food_list:
            app.logger.info("no data")
            return

        for item in stat_food_list:
            tmp_food_id = item[0]
            tmp_stat_food = StatDailyFood.query.filter_by(date=date, food_id=tmp_food_id).first()
            if tmp_stat_food:
                tmp_model_stat_food = tmp_stat_food
            else:
                tmp_model_stat_food = StatDailyFood()
                tmp_model_stat_food.date = date
                tmp_model_stat_food.food_id = tmp_food_id
                tmp_model_stat_food.created_time = getCurrentDate()

            tmp_model_stat_food.total_count = item[1]
            tmp_model_stat_food.total_pay_money = item[2]
            tmp_model_stat_food.updated_time = getCurrentDate()

            '''
            为了测试效果模拟数据
            '''
            # tmp_model_stat_food.total_count = random.randint(50, 100)
            # tmp_model_stat_food.total_pay_money = random.randint(1000, 1010)

            db.session.add(tmp_model_stat_food)
            db.session.commit()

        return

    '''
    site统计
    '''

    def statSite(self, params):
        act = params['act']
        date = params['date']
        date_from = params['date_from']
        date_to = params['date_to']
        app.logger.info("act:{0},from:{1},to:{2}".format(act, date_from, date_to))

        stat_pay = db.session.query(func.sum(PayOrder.total_price).label("total_pay_money")) \
            .filter(PayOrder.status == 1) \
            .filter(PayOrder.created_time >= date_from, PayOrder.created_time <= date_to).first()

        stat_member_count = Member.query.count()
        stat_new_member_count = Member.query.filter(Member.CreatedTime >= date_from,
                                                    Member.CreatedTime <= date_to).count()

        stat_order_count = PayOrder.query.filter_by(status=1) \
            .filter(PayOrder.created_time >= date_from, PayOrder.created_time <= date_to) \
            .count()

        stat_share_count = WxShareHistory.query.filter(WxShareHistory.CreateTime >= date_from
                                                       , WxShareHistory.CreateTime <= date_to).count()

        tmp_stat_site = StatDailySite.query.filter_by(date=date).first()
        if tmp_stat_site:
            tmp_model_stat_site = tmp_stat_site
        else:
            tmp_model_stat_site = StatDailySite()
            tmp_model_stat_site.date = date
            tmp_model_stat_site.created_time = getCurrentDate()

        tmp_model_stat_site.total_pay_money = stat_pay[0] if stat_pay[0] else 0.00
        tmp_model_stat_site.total_new_member_count = stat_new_member_count
        tmp_model_stat_site.total_member_count = stat_member_count
        tmp_model_stat_site.total_order_count = stat_order_count
        tmp_model_stat_site.total_shared_count = stat_share_count
        tmp_model_stat_site.updated_time = getCurrentDate()
        '''
        为了测试效果模拟数据
        '''
        # tmp_model_stat_site.total_pay_money = random.randint(1000, 1010)
        # tmp_model_stat_site.total_new_member_count = random.randint(50, 100)
        # tmp_model_stat_site.total_member_count += tmp_model_stat_site.total_new_member_count
        # tmp_model_stat_site.total_order_count = random.randint(900, 1000)
        # tmp_model_stat_site.total_shared_count = random.randint(1000, 2000)
        db.session.add(tmp_model_stat_site)
        db.session.commit()

    def test(self):
        import datetime
        from common.libs.WebHelper import getFormatDate
        now = datetime.datetime.now()
        for i in reversed(range(1, 30)):
            date_before = now + datetime.timedelta(days=-i)
            date = getFormatDate(date=date_before, format="%Y-%m-%d")
            tmp_params = {
                'act': 'test',
                'date': date,
                'date_from': date + " 00:00:00",
                'date_to': date + " 23:59:59"
            }
            self.statFood(tmp_params)
            self.statMember(tmp_params)
            self.statSite(tmp_params)
