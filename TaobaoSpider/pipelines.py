# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import datetime
import logging
from .items import OrdersItem, BasicinfoItem, GoodsItem, AddressItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from TaobaoSpider.models import TbOrderModel, TbBsinfoModel, TbGoodsModel, TbAddressModel, TbLoginModel, TbLogModel
from TaobaoSpider.settings import db_host, db_user, db_pawd, db_name, db_port

# 创建对象的基类:
Base = declarative_base()


# 淘宝pipeline

class TaobaospiderPipeline(object):
    def __init__(self):  # '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
        engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'
                               .format(db_user, db_pawd, db_host, db_port, db_name), max_overflow=500)
        # 创建DBSession类型:
        db_session = sessionmaker(bind=engine)
        self.session = db_session()

    def process_item(self, item, spider):
        if isinstance(item, OrdersItem):
            info = TbOrderModel(
                token=item['token'],
                orderId=item['order_id'],
                orderTime=item['order_createtime'],
                orderAmt=item['order_rmb'],
                orderStatus=item['order_status'],
                deliverType=item['deliver_type'],
                deliverCompany=item['deliver_company'],
                deliverNo=item['deliver_no'],
                consignee=item['consignee'],
                consigneeMobile=item['consignee_mobile'],
                consigneeAddress=item['consignee_address'],
                add_time=datetime.datetime.now(),
            )

            # self.order_nums = self.order_nums + 1
            # logging.info('用户{}订单数{}'.format(item['token'], self.order_nums))
        elif isinstance(item, BasicinfoItem):
            info = TbBsinfoModel(
                token=item['token'],
                username=item['username'],
                nickName=item['nickName'],
                gender=item['gender'],
                birthday=item['birthday'],
                name=item['name'],
                identityNo=item['identity_no'],
                identityChannel=item['identity_channel'],
                email=item['email'],
                mobile=item['mobile'],
                vipLevel=item['vip_level'],
                growthValue=item['growth_value'],
                creditPoint=item['credit_point'],
                favorableRate=item['favorable_rate'],
                securityLevel=item['security_level'],
                add_time=datetime.datetime.now()
            )

        elif isinstance(item, GoodsItem):
            info = TbGoodsModel(
                token=item['token'],
                itemId=item['goods_id'],
                itemName=item['goods_name'],
                itemUrl=item['goods_url'],
                itemPrice=item['goods_price'],
                itemQuantity=item['goods_nums'],
                orderId=item['order_id'],
                add_time=datetime.datetime.now()
            )


        elif isinstance(item, AddressItem):
            info = TbAddressModel(
                token=item['token'],
                name=item['name'],
                address=item['address'],
                mobile=item['mobile'],
                zipCode=item['zipCode'],
                isDefault=item['isDefault'],
                add_time=datetime.datetime.now()
            )

        else:
            info = ''
            logging.info('数据yield失败')
        try:
            self.session.add(info)
            self.session.commit()
        except Exception as e:
            logging.error("[UUU] 淘宝插入数据异常 Error :{}".format(e))
            self.session.rollback()
        return item

    # 更改登陆状态
    '''
    crawl_state 爬虫工作状态。0：登陆成功  1：登陆失败 2：登陆等待中  -1：队列等待登陆
    :param token:
    '''

    def change_login_state(self, token, login_state):
        try:
            self.session.query(TbLoginModel).filter(TbLoginModel.token == token).update(
                {TbLoginModel.login_state: login_state})
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logging.error('更改登陆状态失败:{}'.format(e))

    # 更改爬虫状态
    '''
    crawl_state 爬虫工作状态。0：未爬过的用户  1：正在爬取数据  2：数据爬取结束且成功返回  -1：爬取失败
    :param token:
    '''

    def change_crawl_status(self, token, crawl_status):
        try:
            self.session.query(TbLoginModel).filter(TbLoginModel.token == token).update(
                {TbLoginModel.crawl_status: crawl_status})
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logging.error('更改爬虫状态失败:{}'.format(e))

    # 插入图片
    def insert_image_base64(self, token, image_base64):
        try:
            self.session.query(TbLoginModel).filter(TbLoginModel.token == token).update(
                {TbLoginModel.image_base64: image_base64, TbLoginModel.image_save_time: int(time.time())})
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logging.error('图片插入失败:{}'.format(e))

    # 查询要爬的用户，并返回用户名和密码
    def select_crawl_user(self, token):
        try:
            result = self.session.query(TbLoginModel).filter(TbLoginModel.token == token, ).first()
            if result:
                user_id = result.id
                uid = result.uid
                username = result.username
                crawl_status = result.crawl_status
                return user_id, username, crawl_status, uid
            else:
                logging.info('没有结果')
                return None
        except Exception as e:
            logging.error("数据库查询异常：{}".format(e))

    # 将异常日志存入数据库中
    def insert_log(self, uid, token, file_name, line_no, message):
        try:
            adds = TbLogModel(
                uid=uid,
                token=token,
                file_name=file_name,
                line_no=line_no,
                message=message,
                log_time=datetime.datetime.now()
            )
            self.session.add(adds)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logging.info("将日志存入数据库中异常：{}".format(e))
