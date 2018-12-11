from application import db
from sqlalchemy import Integer, Column, DateTime, String, DECIMAL
from sqlalchemy.schema import FetchedValue


class S_User_Info(db.Model):
    __tablename__ = 's_userinfo'

    Id = db.Column(Integer, primary_key=True)
    UserName = db.Column(String(128), nullable=False, server_default=FetchedValue())
    UserPwd = db.Column(String(128), nullable=False, server_default=FetchedValue())
    UserRole = db.Column(Integer, nullable=False, server_default=FetchedValue())
    Login_Ip = db.Column(String(128), nullable=False, server_default=FetchedValue())
    Merchant_Id = db.Column(Integer, nullable=False, server_default=FetchedValue())
