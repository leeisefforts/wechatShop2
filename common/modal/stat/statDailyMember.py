from sqlalchemy import Column, Date, DateTime, Index, Integer, Numeric
from sqlalchemy.schema import FetchedValue
from application import db


class StatDailyMember(db.Model):
    __tablename__ = 'stat_daily_member'
    __table_args__ = (
        db.Index('idx_date_member_id', 'date', 'member_id'),
    )

    id = db.Column(Integer, primary_key=True)
    date = db.Column(Date, nullable=False)
    member_id = db.Column(Integer, nullable=False, server_default=FetchedValue())
    total_shared_count = db.Column(Integer, nullable=False, server_default=FetchedValue())
    total_pay_money = db.Column(Numeric(10, 2), nullable=False, server_default=FetchedValue())
    updated_time = db.Column(DateTime, nullable=False, server_default=FetchedValue())
    created_time = db.Column(DateTime, nullable=False, server_default=FetchedValue())