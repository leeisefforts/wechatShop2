from sqlalchemy import BigInteger, Column, DateTime, Index, Integer, Numeric, String, Text
from sqlalchemy.schema import FetchedValue
from application import db,app


class PayOrder(db.Model):
    __tablename__ = 'pay_order'
    __table_args__ = (
        db.Index('idx_member_id_status', 'member_id', 'status'),
    )

    id = db.Column(Integer, primary_key=True)
    order_sn = db.Column(String(40), nullable=False, unique=True, server_default=FetchedValue())
    member_id = db.Column(BigInteger, nullable=False, server_default=FetchedValue())
    total_price = db.Column(Numeric(10, 2), nullable=False, server_default=FetchedValue())
    yun_price = db.Column(Numeric(10, 2), nullable=False, server_default=FetchedValue())
    pay_price = db.Column(Numeric(10, 2), nullable=False, server_default=FetchedValue())
    pay_sn = db.Column(String(128), nullable=False, server_default=FetchedValue())
    prepay_id = db.Column(String(128), nullable=False, server_default=FetchedValue())
    note = db.Column(Text, nullable=False)
    status = db.Column(Integer, nullable=False, server_default=FetchedValue())
    express_status = db.Column(Integer, nullable=False, server_default=FetchedValue())
    comment_status = db.Column(Integer, nullable=False, server_default=FetchedValue())
    pay_time = db.Column(DateTime, nullable=False, server_default=FetchedValue())
    updated_time = db.Column(DateTime, nullable=False, server_default=FetchedValue())
    created_time = db.Column(DateTime, nullable=False, server_default=FetchedValue())


    @property
    def pay_status(self):
        tmp_status = self.status
        if self.status == 1:
            tmp_status = self.express_status
            if self.express_status == 1 and self.comment_status == 0:
                tmp_status = -5
            if self.express_status == 1 and self.comment_status == 1:
                tmp_status = 1
        return tmp_status

    @property
    def status_desc(self):
        return app.config['PAY_STATUS_DISPLAY_MAPPING'][ str( self.pay_status )]

    @property
    def order_number(self):
        order_number = self.created_time.strftime("%Y%m%d%H%M%S")
        order_number = order_number + str(self.id).zfill(5)
        return order_number