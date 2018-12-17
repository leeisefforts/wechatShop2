from sqlalchemy import Column, Date, DateTime, Index, Integer, Numeric
from sqlalchemy.schema import FetchedValue
from application import db


class StatDailyFood(db.Model):
    __tablename__ = 'stat_daily_food'
    __table_args__ = (
        db.Index('date_food_id', 'date', 'food_id'),
    )

    id = db.Column(Integer, primary_key=True)
    date = db.Column(Date, nullable=False)
    food_id = db.Column(Integer, nullable=False, server_default=FetchedValue())
    total_count = db.Column(Integer, nullable=False, server_default=FetchedValue())
    total_pay_money = db.Column(Numeric(10, 2), nullable=False, server_default=FetchedValue())
    updated_time = db.Column(DateTime, nullable=False, server_default=FetchedValue())
    created_time = db.Column(DateTime, nullable=False, server_default=FetchedValue())