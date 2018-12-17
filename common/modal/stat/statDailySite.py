from sqlalchemy import Column, Date, DateTime, Integer, Numeric
from sqlalchemy.schema import FetchedValue
from application import db


class StatDailySite(db.Model):
    __tablename__ = 'stat_daily_site'

    id = db.Column(Integer, primary_key=True)
    date = db.Column(Date, nullable=False, index=True)
    total_pay_money = db.Column(Numeric(10, 2), nullable=False, server_default=FetchedValue())
    total_member_count = db.Column(Integer, nullable=False)
    total_new_member_count = db.Column(Integer, nullable=False)
    total_order_count = db.Column(Integer, nullable=False)
    total_shared_count = db.Column(Integer, nullable=False)
    updated_time = db.Column(DateTime, nullable=False, server_default=FetchedValue())
    created_time = db.Column(DateTime, nullable=False, server_default=FetchedValue())