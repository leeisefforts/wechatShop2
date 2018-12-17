from sqlalchemy import Column, DateTime, Integer, Numeric
from sqlalchemy.schema import FetchedValue
from common.modal.member import Member
from application import db


class ShopSaleChangeLog(db.Model):
    __tablename__ = 'shop_sale_change_log'

    id = db.Column(Integer, primary_key=True)
    food_id = db.Column(Integer, nullable=False, index=True, server_default=FetchedValue())
    quantity = db.Column(Integer, nullable=False, server_default=FetchedValue())
    price = db.Column(Numeric(10, 2), nullable=False, server_default=FetchedValue())
    member_id = db.Column(Integer, nullable=False, server_default=FetchedValue())
    created_time = db.Column(DateTime, nullable=False, server_default=FetchedValue())

    @property
    def member_name(self):
        member = Member.query.filter_by(Id=self.member_id).first()
        return member.Nickname
