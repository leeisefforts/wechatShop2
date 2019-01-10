from application import db, app
from sqlalchemy import Integer, DateTime, String, DECIMAL
from sqlalchemy.schema import FetchedValue


class Merchant_Info(db.Model):
    __tablename__ = 'merchant_info'

    Id = db.Column(Integer, primary_key=True)
    Name = db.Column(String(128), nullable=False, server_default=FetchedValue())
    Address = db.Column(String(128), nullable=False, server_default=FetchedValue())
    ImageUrl = db.Column(String(128), nullable=False, server_default=FetchedValue())
    Phone = db.Column(Integer, nullable=False, server_default=FetchedValue())
    CreateTime = db.Column(DateTime, nullable=False, server_default=FetchedValue())
    Status = db.Column(Integer, nullable=False, server_default=FetchedValue())
    OpenId = db.Column(String(256), nullable=False, server_default=FetchedValue())
    TotalBalance = db.Column(DECIMAL, nullable=False, server_default=FetchedValue())
    FreezeBalance = db.Column(DECIMAL, nullable=False, server_default=FetchedValue())

    @property
    def Status_Desc(self):
        return app.config['STATUS_MAPPING'][str(self.Status)]
