APP = {
    'domain': 'http://127.0.0.1:5000'
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

SHOP_STATUS_MAPPING = {
    "2": "禁用",
    "1": "上架中",
    "0": "未上架"
}


MINA_APP = {
    'appid':'wx871b8985c8c8c4ab',
    'appkey':'fcb9f2b868d4fede2a48c35e5c95d06d',
    'paykey':'',
    'mch_id':'',
    'callback_url':'/api/order/callback'
}
