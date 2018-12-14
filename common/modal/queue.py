from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db


class QueueList(db.Model):
    __tablename__ = 'queue_list'

    id = db.Column(Integer, primary_key=True)
    queue_name = db.Column(String(30), nullable=False, server_default=FetchedValue())
    data = db.Column(String(500), nullable=False, server_default=FetchedValue())
    status = db.Column(Integer, nullable=False, server_default=FetchedValue())
    updated_time = db.Column(DateTime, nullable=False, server_default=FetchedValue())
    created_time = db.Column(DateTime, nullable=False, server_default=FetchedValue())