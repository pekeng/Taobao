# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 用户基本信息
class BasicinfoItem(scrapy.Item):
    token = scrapy.Field()
    username = scrapy.Field()
    nickName = scrapy.Field()
    gender = scrapy.Field()
    birthday = scrapy.Field()
    name = scrapy.Field()
    identity_no = scrapy.Field()
    identity_channel = scrapy.Field()
    email = scrapy.Field()
    mobile = scrapy.Field()
    vip_level = scrapy.Field()
    growth_value = scrapy.Field()
    credit_point = scrapy.Field()
    favorable_rate = scrapy.Field()
    security_level = scrapy.Field()


# 收货地址信息
class AddressItem(scrapy.Item):
    token = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    mobile = scrapy.Field()
    zipCode = scrapy.Field()
    isDefault = scrapy.Field()


# 订单信息
class OrdersItem(scrapy.Item):
    token = scrapy.Field()
    order_id = scrapy.Field()
    order_createtime = scrapy.Field()
    order_rmb = scrapy.Field()
    order_status = scrapy.Field()
    deliver_type = scrapy.Field()
    deliver_company = scrapy.Field()
    deliver_no = scrapy.Field()
    consignee = scrapy.Field()
    consignee_mobile = scrapy.Field()
    consignee_address = scrapy.Field()


# 商品信息
class GoodsItem(scrapy.Item):
    token = scrapy.Field()
    goods_id = scrapy.Field()
    goods_name = scrapy.Field()
    goods_url = scrapy.Field()
    goods_price = scrapy.Field()
    goods_nums = scrapy.Field()
    order_id = scrapy.Field()
