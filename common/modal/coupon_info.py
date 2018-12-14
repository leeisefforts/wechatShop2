from application import db
from sqlalchemy import Integer, Column, DateTime, String, DECIMAL
from sqlalchemy.schema import FetchedValue


class Coupon_Info(db.Model):
    __tablename__ = 'coupon_info'

    Id = db.Column(Integer, primary_key=True)
    Coupon_Name = db.Column(String(128), nullable=False, server_default=FetchedValue())
    ShopId = db.Column(Integer, nullable=False, server_default=FetchedValue())
    Coupon_Price = db.Column(DECIMAL, nullable=False, server_default=FetchedValue())
    Member_Id = db.Column(Integer, nullable=False, server_default=FetchedValue())
    Price = db.Column(DECIMAL, nullable=False, server_default=FetchedValue())
    CreateTime = db.Column(DateTime, nullable=False, server_default=FetchedValue())
    UpdateTime = db.Column(DateTime, nullable=False, server_default=FetchedValue())
    Status = db.Column(Integer, nullable=False, server_default=FetchedValue())
    QrCode_Url = db.Column(String(128), nullable=False, server_default=FetchedValue())
