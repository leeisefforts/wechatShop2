from sqlalchemy import Column, DateTime, Index, Integer, String, Text
from sqlalchemy.schema import FetchedValue
from application import db


class OauthMemberBind(db.Model):
    __tablename__ = 'oauth_member_bind'
    __table_args__ = (
        db.Index('idx_type_openid', 'type', 'openid'),
    )

    Id = db.Column(Integer, primary_key=True)
    Member_id = db.Column(Integer, nullable=False, server_default=FetchedValue())
    Client_type = db.Column(String(20), nullable=False, server_default=FetchedValue())
    Type = db.Column(Integer, nullable=False, server_default=FetchedValue())
    Openid = db.Column(String(80), nullable=False, server_default=FetchedValue())
    Unionid = db.Column(String(100), nullable=False, server_default=FetchedValue())
    Extra = db.Column(Text, nullable=False)
    UpdateTime = db.Column(DateTime, nullable=False, server_default=FetchedValue())
    CreatTime = db.Column(DateTime, nullable=False, server_default=FetchedValue())