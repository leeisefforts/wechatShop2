# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue

from application import db

class Image(db.Model):
    __tablename__ = 'images'

    Id = db.Column(Integer, primary_key=True)
    File_key = db.Column(String(60), nullable=False, server_default=FetchedValue())
    CreateTime = db.Column(DateTime, nullable=False, server_default=FetchedValue())