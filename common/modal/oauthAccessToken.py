from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db


class OauthAccessToken(db.Model):
    __tablename__ = 'oauth_access_token'

    Id = db.Column(db.Integer, primary_key=True)
    Access_token = db.Column(db.String(600), nullable=False, server_default=db.FetchedValue())
    Expired_time = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    Created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
