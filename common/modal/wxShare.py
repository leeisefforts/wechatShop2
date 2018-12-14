from sqlalchemy import Column, DateTime, Integer, String, DECIMAL
from sqlalchemy.schema import FetchedValue
from application import db


class WxShareHistory(db.Model):
    __tablename__ = 'wxshare'

    Id = db.Column(db.Integer, primary_key=True)
    Member_Id = db.Column(Integer, nullable=False, server_default=FetchedValue())
    Share_Url = db.Column(String(200), nullable=False, server_default=FetchedValue())
    ToOpenId = db.Column(String(200), nullable=False, server_default=FetchedValue())
    ToNickName = db.Column(String(200), nullable=False, server_default=FetchedValue())
    ToAvatar = db.Column(String(200), nullable=False, server_default=FetchedValue())
    Price = db.Column(DECIMAL, nullable=False, server_default=FetchedValue())
    CreateTime = db.Column(DateTime, nullable=False, server_default=FetchedValue())
    Shop_Id = db.Column(Integer, nullable=False, server_default=FetchedValue())
