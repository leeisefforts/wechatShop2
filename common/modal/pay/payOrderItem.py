from sqlalchemy import BigInteger, Column, DateTime, Integer, Numeric, Text
from sqlalchemy.schema import FetchedValue
from application import db


class PayOrderItem(db.Model):
    __tablename__ = 'pay_order_item'

    id = db.Column(Integer, primary_key=True)
    pay_order_id = db.Column(Integer, nullable=False, index=True, server_default=FetchedValue())
    member_id = db.Column(BigInteger, nullable=False, server_default=FetchedValue())
    quantity = db.Column(Integer, nullable=False, server_default=FetchedValue())
    price = db.Column(Numeric(10, 2), nullable=False, server_default=FetchedValue())
    food_id = db.Column(Integer, nullable=False, index=True, server_default=FetchedValue())
    note = db.Column(Text, nullable=False)
    status = db.Column(Integer, nullable=False, server_default=FetchedValue())
    updated_time = db.Column(DateTime, nullable=False, server_default=FetchedValue())
    created_time = db.Column(DateTime, nullable=False, server_default=FetchedValue())