from application import db
from sqlalchemy import Integer, Column, DateTime, String, DECIMAL
from sqlalchemy.schema import FetchedValue


class S_User_Role(db.Model):
    __tablename__ = 's_user_role'

    Id = db.Column(Integer, primary_key=True)
    RoleName = db.Column(String(128), nullable=False, server_default=FetchedValue())
