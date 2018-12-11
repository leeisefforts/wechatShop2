from application import db, app
from sqlalchemy import Integer, Column, DateTime, String, DECIMAL
from sqlalchemy.schema import FetchedValue


class Shop_Info(db.Model):
    __tablename__ = 'shop_info'

    Id = db.Column(Integer, primary_key=True)
    ShopName = db.Column(String(128), nullable=False, server_default=FetchedValue())
    ShopMerchantId = db.Column(Integer, nullable=False, server_default=FetchedValue())
    ShopImageUrl = db.Column(String(128), nullable=False, server_default=FetchedValue())
    ShopDesc = db.Column(String(256), nullable=False, server_default=FetchedValue())
    ShopPrice = db.Column(DECIMAL, nullable=False, server_default=FetchedValue())
    ShopFloorPrice = db.Column(DECIMAL, nullable=False, server_default=FetchedValue())
    CreatTime = db.Column(DateTime, nullable=False, server_default=FetchedValue())
    UpdateTime = db.Column(DateTime, nullable=False, server_default=FetchedValue())
    ShopStatus = db.Column(Integer, nullable=False, server_default=FetchedValue())

    @property
    def Status_Desc(self):
        return app.config['SHOP_STATUS_MAPPING'][str(self.ShopStatus)]
