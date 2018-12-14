from sqlalchemy import Column, DateTime, Integer, Text
from sqlalchemy.schema import FetchedValue
from application import db


class PayOrderCallbackData(db.Model):
    __tablename__ = 'pay_order_callback_data'

    id = db.Column(Integer, primary_key=True)
    pay_order_id = db.Column(Integer, nullable=False, unique=True, server_default=FetchedValue())
    pay_data = db.Column(Text, nullable=False)
    refund_data = db.Column(Text, nullable=False)
    updated_time = db.Column(DateTime, nullable=False, server_default=FetchedValue())
    created_time = db.Column(DateTime, nullable=False, server_default=FetchedValue())