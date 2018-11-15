import datetime
from sqlalchemy import Column, String, create_engine, Integer, DateTime, TEXT
from sqlalchemy.ext.declarative import declarative_base
from TaobaoSpider.settings import db_host, db_user, db_pawd, db_name, db_port

# 创建对象的基类:
Base = declarative_base()


# 淘宝订单
class TbOrderModel(Base):
    # 表的名字:
    __tablename__ = 'taobaov1_tborder'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    token = Column(String(64), default='')
    orderId = Column(String(200), )
    orderTime = Column(String(200), )
    orderAmt = Column(String(200), )
    orderStatus = Column(String(200), )
    deliverType = Column(String(200), )
    deliverCompany = Column(String(200), )
    deliverNo = Column(String(200), )
    consignee = Column(String(200), )
    consigneeMobile = Column(String(200), )
    consigneeAddress = Column(String(200), )
    add_time = Column(DateTime, default=datetime.datetime.now)


# 用户基本信息表
class TbBsinfoModel(Base):
    # 表的名字:
    __tablename__ = 'taobaov1_tbbasicinfo'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    token = Column(String(64), default='')
    username = Column(String(300), )
    nickName = Column(String(300), )
    gender = Column(String(300), )
    birthday = Column(String(300), )
    name = Column(String(300), )
    identityNo = Column(String(300), )
    identityChannel = Column(String(300), )
    email = Column(String(300), )
    mobile = Column(String(300), )
    vipLevel = Column(String(300), )
    growthValue = Column(String(300), )
    creditPoint = Column(String(300), )
    favorableRate = Column(String(300), )
    securityLevel = Column(String(300), )
    add_time = Column(DateTime, default=datetime.datetime.now)


# 收货地址表
class TbAddressModel(Base):
    # 表的名字:
    __tablename__ = 'taobaov1_tbaddresses'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    token = Column(String(300), default='')
    name = Column(String(300), )
    address = Column(String(300), )
    mobile = Column(String(300), )
    zipCode = Column(String(300), )
    isDefault = Column(String(300), )
    add_time = Column(DateTime, default=datetime.datetime.now)


# 商品信息表
class TbGoodsModel(Base):
    # 表的名字:
    __tablename__ = 'taobaov1_tbitem'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    token = Column(String(300), default='')
    itemId = Column(String(300), )
    itemName = Column(String(300), )
    itemUrl = Column(String(300), )
    itemPrice = Column(String(300), )
    itemQuantity = Column(String(300), )
    orderId = Column(String(300), )
    add_time = Column(DateTime, default=datetime.datetime.now)


# 淘宝登陆信息表
class TbLoginModel(Base):
    # 表的名字:
    __tablename__ = 'taobaov1_tblogin'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    token = Column(String(300), default='')
    username = Column(String(300), )
    password = Column(String(300), )
    identityNo = Column(String(300), )
    name = Column(String(300), )
    uid = Column(String(300), )
    accessType = Column(String(300), )
    loginType = Column(String(300), )
    cookie = Column(TEXT, )
    login_state = Column(String(300), )
    crawl_status = Column(String(300), )
    create_data = Column(String(300), )
    target_crawl = Column(String(300), )
    msg_code = Column(String(300), )
    image_base64 = Column(TEXT, )
    image_save_time = Column(Integer, )
    add_time = Column(DateTime, )


# 日志信息模块
class TbLogModel(Base):
    # 表的名字:
    __tablename__ = "taobaov1_tblog"
    # 表的结构:
    id = Column(Integer, unique=True, primary_key=True)
    uid = Column(String(255), )
    token = Column(String(255), )
    file_name = Column(String(255), )
    line_no = Column(String(255), )
    message = Column(TEXT, )
    log_time = Column(DateTime, )


if __name__ == "__main__":
    engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'
                           .format(db_user, db_pawd, db_host, db_port, db_name), max_overflow=500)
    Base.metadata.create_all(engine)
