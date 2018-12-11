from application import db
from sqlalchemy import Integer, Column, DateTime, String, DECIMAL
from sqlalchemy.schema import FetchedValue


class Order_Info(db.Model):
    __tablename__ = 'order_info'

    Id = db.Column(Integer, primary_key=True)
    Order_Code = db.Column(String(128), nullable=False, server_default=FetchedValue())
    Order_ShopId = db.Column(Integer, nullable=False, server_default=FetchedValue())
    Order_Price = db.Column(DECIMAL, nullable=False, server_default=FetchedValue())
    Order_User_Id = db.Column(Integer, nullable=False, server_default=FetchedValue())
    Status = db.Column(Integer, nullable=False, server_default=FetchedValue())
    CreateTime = db.Column(DateTime, nullable=False, server_default=FetchedValue())
