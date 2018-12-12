from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db


class Member(db.Model):
    __tablename__ = 'member'

    Id = db.Column(Integer, primary_key=True)
    Nickname = db.Column(String(100), nullable=False, server_default=FetchedValue())
    City = db.Column(String(100), nullable=False, server_default=FetchedValue())
    Sex = db.Column(Integer, nullable=False, server_default=FetchedValue())
    Avatar = db.Column(String(64), nullable=False, server_default=FetchedValue())
    Salt = db.Column(String(64), nullable=False, server_default=FetchedValue())
    UpdatedTime = db.Column(DateTime, nullable=False, server_default=FetchedValue())
    CreatedTime = db.Column(DateTime, nullable=False, server_default=FetchedValue())
