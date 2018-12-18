APP = {
    'domain': 'https://17bctech.com'
}
AUTH_COOKIE_NAME = 'UserCookie'
SERVER_PORT = '5000'
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://bryant:leekobe24@cd-cdb-nmj4h99o.sql.tencentcdb.com:63625/wechat_shop'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ENCODING = "utf8mb4"
SQLALCHEMY_BINDS = {
    'wechat': "mysql+pymysql://bryant:leekobe24@cd-cdb-nmj4h99o.sql.tencentcdb.com:63625/wechat_shop"
}
## 过滤url
IGNORE_URLS = [
    "^/login",
    "^/upload"

]
PAGE_SIZE = 50
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    "2": "审核拒绝",
    "1": "审核通过",
    "0": "未审核"
}

API_IGNORE_URLS = [
    "^/api"
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]

UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/web/static/upload/',
    'prefix_url': '/static/upload/'
}

PAY_STATUS_MAPPING = {
    "1": "已支付",
    "-8": "待支付",
    "0": "已关闭"
}

PAY_STATUS_DISPLAY_MAPPING = {
    "0": "订单关闭",
    "1": "支付成功",
    "-8": "待支付",
    "-7": "待使用",
    "-6": "待确认"
}

SHOP_STATUS_MAPPING = {
    "2": "禁用",
    "1": "上架中",
    "0": "未上架"
}

MINA_APP = {
    'appid':'wx1f244139ab0c54c8',
    'appkey':'6e4fab0d29a50571678ba1559e627ebc',
    'paykey':'TM8KwVFRlp0hsTWMQTxLplfFIzmk7csr',
    'mch_id':'1513434041',
    'callback_url':'/api/order/callback'
}
