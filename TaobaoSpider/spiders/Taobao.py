# -*- coding: utf-8 -*-
import re
import time
import datetime
import requests
import scrapy
import json
import hashlib
import base64
import sys
import traceback
import os
from bs4 import BeautifulSoup
from TaobaoSpider.items import BasicinfoItem, OrdersItem, GoodsItem, AddressItem
from scrapy_redis.spiders import RedisSpider
from TaobaoSpider.pipelines import TaobaospiderPipeline
from TaobaoSpider.use_proxy import ProxyPoolInfo

try:
    from ..yunxinjs import get_sign
except:
    from TaobaoSpider.yunxinjs import get_sign


class TbaobaoSpider(RedisSpider, TaobaospiderPipeline, ProxyPoolInfo):
    name = 'Taobao'
    redis_key = 'taobao'
    allowed_domains = ['taobao.com']
    timestamp = str(int(time.time() * 1000))
    generateqr_time2 = int(time.time() * 1000000)
    generateqr_time = int(time.time() * 1000)
    orders_headers = {
        'Host': 'buyertrade.taobao.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Accept': 'application / json, text / javascript, * / *; q = 0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
    }
    recyled_headers = {
        'Host': 'buyertrade.taobao.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Accept': 'application / json, text / javascript, * / *; q = 0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://buyertrade.taobao.com/trade/itemlist/list_recyled_items.htm',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
    }
    detail_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
                          (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-Requests': '1'
    }
    address_headers = {
        "Host": "h5api.m.taobao.com",
        "Referer": "http://member1.taobao.com/member/fresh/deliver_address.htm?spm=a1z09.2.a210b.8.77552e8dw14JoY",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Cookie": "t=1b660ec8243902d1b678e754be9292fd; cookie2=116ce21963d77cffd724070c22a0677f; v=0; _tb_token_=e6e958991f55e; cna=I4r6ExoHJDkCAat4c98lH1PM; publishItemObj=Ng%3D%3D; tracknick=%5Cu65E0%5Cu6CD5%5Cu6446%5Cu8131%5Cu4F602012; lgc=%5Cu65E0%5Cu6CD5%5Cu6446%5Cu8131%5Cu4F602012; dnk=%5Cu65E0%5Cu6CD5%5Cu6446%5Cu8131%5Cu4F602012; tg=0; _m_h5_tk=ebe3b0876930a679c5013e2d61aa0944_1534313022537; _m_h5_tk_enc=c40a523b1768b549eb286309ade13ded; thw=cn; unb=860963132; sg=22a; _l_g_=Ug%3D%3D; skt=cbe7d0528221f69d; cookie1=VFO7OYtPLa%2B4l8%2BNUD3wjHESjW9YNA9jQot%2FK1qV%2B%2BY%3D; csg=8083f81e; uc3=vt3=F8dBzrpKCKcPHc0Evd8%3D&id2=W89MXAb8ajng&nk2=rUf%2FBfweUxPktIw4ggg%3D&lg2=UIHiLt3xD8xYTw%3D%3D; existShop=MTUzNDMwNzkxMA%3D%3D; _cc_=U%2BGCWk%2F7og%3D%3D; _nk_=%5Cu65E0%5Cu6CD5%5Cu6446%5Cu8131%5Cu4F602012; cookie17=W89MXAb8ajng; mt=ci=99_1&np=; uc1=cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie21=UIHiLt3xTIkz&cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=false&pas=0&cookie14=UoTfL8nMAc7W0w%3D%3D&tag=8&lng=zh_CN; isg=BKamD91BwUJc-5X1xj7JDNCL9xzoL-rC8x3jIJBPmkmkE0Yt-BREUXflb086u-JZ",
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Referer': 'https://login.taobao.com/member/login.jhtml?spm=a21bo.2017.754894437.1.5af911d9Dc29LU&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F',
        'Accept': '*/*;q=0.8',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-Requests': '1'
    }
    # 检查二维码扫码成功地址
    check_url = 'https://qrlogin.taobao.com/qrcodelogin/qrcodeLoginCheck.do?lgToken={}&defaulturl=https%3A%2F%2Fwww.taobao.com%2F&_ksTS={}_74&callback=jsonp{}'
    # 解析个人资料，个人交易信息,安全设置，认证，评价页面地址
    baseInfoSet_url = 'https://i.taobao.com/user/baseInfoSet.htm'
    account_url = 'https://member1.taobao.com/member/fresh/account_profile.htm'
    security_url = 'https://member1.taobao.com/member/fresh/account_security.htm'
    certify_url = 'https://member1.taobao.com/member/fresh/certify_info.htm'
    my_rate_url = 'https://rate.taobao.com/myRate.htm'
    t_vip_url = "https://vip.taobao.com/ajax/getGoldUser.do?_input_charset=utf-8&from=diaoding&_ksTS={}_252&callback=jsonp253"
    # 解析收货，订单首页，回收站，已存在订单地址
    address_url = "http://h5api.m.taobao.com/h5/mtop.taobao.mbis.getdeliveraddrlist/1.0/?jsv=2.4.2&appKey=12574478&t={}&sign={}&api=mtop.taobao.mbis.getDeliverAddrList&v=1.0&ecode=1&needLogin=true&dataType=jsonp&type=jsonp&callback=mtopjsonp3&data=%7B%7D"
    page_url = 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm'
    recyled_url = 'https://buyertrade.taobao.com/trade/itemlist/asyncRecyledItems.htm?action=itemlist/RecyledQueryAction&event_submit_do_query=1&_input_charset=utf8'
    orders_url = 'https://buyertrade.taobao.com/trade/itemlist/asyncBought.htm?action=itemlist/BoughtQueryAction&event_submit_do_query=1&_input_charset=utf8'
    # 全局设置
    custom_settings = {
        "DOWNLOAD_TIMEOUT": 120,
        "CONCURRENT_REQUESTS": 32,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 32,
        "CONCURRENT_REQUESTS_PER_IP": 32,
        "HTTP_ALLOWED_CODE": [302, ],
        # CRITICAL - 严重错误
        # ERROR - 一般错误
        # WARNING - 警告信息
        # INFO - 一般信息
        # DEBUG - 调试信息
        # "LOG_LEVEL": "INFO",
        # "LOG_FILE": "log/TaoBao_Spider/TB-" + str(datetime.date.today()) + ".log",
        # "LOG_ENABLE": True,
        # "LOG_ENCODING": "UTF-8",
        # "LOG_ENABLED": True,  # 启用self.logger
        # "LOG_STDOUT": True,  # 在当前目录里创建self.logger输出文件的文件名
        # 'LOG_FORMAT': "%(asctime)s - %(levelname)s - %(message)s -%(funcName)s - %(lineno)d",
        # 'DATE_FORMAT': "%m/%d/%Y %H:%M:%S %p",
    }

    def __init__(self):
        TaobaospiderPipeline.__init__(self)
        ProxyPoolInfo.__init__(self)

    # 识别任务
    def make_request_from_data(self, data):
        proxy_ip_port = self.create_proxy()
        token = str(data.decode('utf8'))
        self.logger.info('redis库推送token数据成功，用户为：{}'.format(token))
        try:
            user_id, username, crawl_status, uid = self.select_crawl_user(token)
            if user_id:
                self.logger.info('成功接收到任务，用户为:{}'.format(token))
                self.change_crawl_status(token, '-22')  # 将爬虫任务设置为-22，开始执行任务
                umid_token = 'C{}{}'.format(int(time.time() * 100000000000000), int(time.time() * 1000000))
                url = 'https://qrlogin.taobao.com/qrcodelogin/generateQRCode4Login.do?adUrl=&adImage=&adText=&viewFd4PC=&viewFd4Mobile=&from=tbTop&appkey=00000000&umid_token={}'.format(
                    umid_token)
                # 生成去获取二维码的地址
                return scrapy.Request(
                    url=url,
                    headers=self.headers,
                    meta={
                        "cookiejar": int(user_id),
                        "proxy": proxy_ip_port,
                        "umid_token": umid_token,
                        "token": token,
                        "user_id": user_id,
                        "uid": uid,
                    },
                    callback=self.get_qr,
                    dont_filter=True, )
            else:
                self.logger.info('用户:{}账户信息user_id为空，无法进入认证'.format(token))
        except Exception as e:
            self.change_crawl_status(token, '-7')  # 将爬虫任务设置为-7,账户信息不全，无法进入认证
            self.logger.error('用户:{}账户信息不全，无法进入认证'.format(token))
            # 对抛出的异常进行处理
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fname = "".join(os.path.split(exc_traceback.tb_frame.f_code.co_filename))  # 异常抛出的文件
            lineno = exc_traceback.tb_lineno  # 异常出现在哪一行
            uid = "在查找用户的时候失败了"  # log表中的uid
            formatted_lines = traceback.format_exc().splitlines()  # 获取整个异常中
            # 异常描述
            message = "在数据库中查找用户时出现了问题,用户:{}-->异常：{}-->异常最后一行：{}".format(token, e, formatted_lines[-1])
            # 将抛出的异常存入数据库中
            self.insert_log(token=token, uid=uid, file_name=fname, line_no=lineno, message=message)

    # 提取二维码地址以及lotoken并检查扫描二维码状态
    def get_qr(self, response):
        token = response.meta["token"]
        uid = response.meta['uid']
        # 打印传递的参数
        try:
            qr_url = 'http:' + "".join(re.findall(re.compile(r'url":"(.*?g)",'), response.text))
            lg_token = "".join(re.findall(re.compile(r'lgToken":"(.*?)",'), response.text))
            # 去下载二维码图片
            response_image = requests.get(url=qr_url, headers=self.headers, timeout=120)
            image_base64 = base64.b64encode(response_image.content)
            self.insert_image_base64(token, image_base64)  # base64加密入库
            self.change_crawl_status(token, '-3')  # 将爬虫任务设置为-3,等待用户扫描二维码
            self.logger.info('入库二维码成功并设置爬虫任务设置为-3,等待用户{}扫描二维码'.format(token))
            with open('TaoBao.png', 'wb') as f:
                f.write(response_image.content)
                print('请扫描验证码')
            # 检验登没登二维码
            generate_qr_time3 = int(time.time() * 1000)
            num = 75
            yield scrapy.Request(
                url=self.check_url.format(lg_token, generate_qr_time3, num),
                headers=self.headers,
                meta={
                    "cookiejar": response.meta['user_id'],  # 清空cookie
                    "proxy": response.meta["proxy"],
                    "umid_token": response.meta['umid_token'],
                    "lg_token": lg_token,
                    "num": num,
                    "token": token,
                    "user_id": response.meta["user_id"],
                    "uid": uid
                },
                callback=self.success
            )
        except Exception as e:
            self.change_crawl_status(token, '-8')  # 将爬虫任务设置为-8,系统繁忙，请稍后重试
            self.logger.error("用户{}获取二维码异常：{}".format(token, e))
            # 对抛出的异常进行处理
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fname = "".join(os.path.split(exc_traceback.tb_frame.f_code.co_filename))  # 异常抛出的文件
            lineno = exc_traceback.tb_lineno  # 异常出现在哪一行
            uid = uid  # log表中的uid
            formatted_lines = traceback.format_exc().splitlines()  # 获取整个异常中
            # 异常描述
            message = "获取二维码异常问题，用户:{}-->异常：{}-->异常最后一行：{}".format(token, e, formatted_lines[-1])
            # 将抛出的异常存入数据库中
            self.insert_log(token=token, uid=uid, file_name=fname, line_no=lineno, message=message)

    # 二维码轮询
    def success(self, response):
        uid = response.meta['uid']
        token = response.meta["token"]
        try:
            num = response.meta["num"]
            num += 28
            code = "".join(re.findall(re.compile(r'code":"([0-9]{5})",'), response.text))
            print(code)
            if code == "10000":
                time.sleep(2)
                lg_token = response.meta["lg_token"]
                self.logger.info('等待用户{}扫码：{}'.format(token, code))
                generateqr_time3 = int(time.time() * 1000)
                yield scrapy.Request(
                    url=self.check_url.format(lg_token, generateqr_time3, num),
                    headers=self.headers,
                    meta={"cookiejar": response.meta["cookiejar"],
                          "proxy": response.meta["proxy"],
                          "umid_token": response.meta['umid_token'],
                          "lg_token": lg_token,
                          "num": num,
                          "token": token,
                          "user_id": response.meta["user_id"],
                          "uid": uid
                          },
                    dont_filter=True,
                    callback=self.success
                )
            # 扫码成功 等待确认
            elif code == "10001":
                time.sleep(2)
                self.change_crawl_status(token, '-14')  # 将爬虫任务设置为-14,请点击确认登录
                self.logger.info("用户{}扫码成功 等待点击确认操作:{}".format(token, code))
                lg_token = response.meta["lg_token"]
                generateqr_time3 = int(time.time() * 1000)
                yield scrapy.Request(
                    url=self.check_url.format(lg_token, generateqr_time3, num),
                    headers=self.headers,
                    meta={"cookiejar": response.meta["cookiejar"],
                          "proxy": response.meta["proxy"],
                          "umid_token": response.meta['umid_token'],
                          "lg_token": lg_token,
                          "num": num,
                          "token": token,
                          "user_id": response.meta["user_id"],
                          "uid": uid,
                          },
                    dont_filter=True,
                    callback=self.success
                )
            # 确认成功 跳转
            elif code == "10006":
                self.change_crawl_status(token, '1')  # 将爬虫任务设置为1,数据获取进行中
                self.logger.info('用户{}扫码 确认 成功：{}'.format(token, code))
                # 提取302重定向的URL地址
                success_url = "".join(
                    re.findall(re.compile(r'"url":"(ht.*?)"}\);'), response.text)) + '&umid_token={}'.format(
                    response.meta['umid_token'])
                if "".join(re.findall(re.compile(r'"url":"(ht.*?)"}\);'), response.text)):
                    self.logger.info('用户{}success_url登录淘宝url获取成功：{}'.format(token, success_url))
                else:
                    self.logger.info('用户{}success_url登录淘宝url获取失败：{}'.format(token, success_url))

                # 回调请求 更换cookie
                yield scrapy.Request(url=success_url,
                                     headers=self.headers,
                                     meta={
                                         "cookiejar": response.meta["user_id"],
                                         "proxy": response.meta["proxy"],
                                         "token": token,
                                         "uid": uid,
                                     },
                                     callback=self.redirect_url,
                                     dont_filter=True,
                                     )
            # 二维码失效 结束
            elif code == "10004":
                self.change_crawl_status(token, '-5')  # 将爬虫任务设置为-5,等待用户扫码超时,二维码失效 扫码失败
                self.logger.info("用户{}扫描的二维码失效 程序结束:{}".format(token, code))
            # 其他未知异常 结束
            else:
                self.change_crawl_status(token, '-8')  # 将爬虫任务设置为-8,系统繁忙，请稍后重试
                self.logger.info("用户{}二维码轮询异常：正则可能有问题:{}".format(token, code))
        except Exception as e:
            self.logger.error('二维码轮询返回response，解析code出错:{}用户:{}'.format(e, token))
            # 对抛出的异常进行处理
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fname = "".join(os.path.split(exc_traceback.tb_frame.f_code.co_filename))  # 异常抛出的文件
            lineno = exc_traceback.tb_lineno  # 异常出现在哪一行
            uid = uid  # log表中的uid
            formatted_lines = traceback.format_exc().splitlines()  # 获取整个异常中
            # 异常描述
            message = "二维码轮询出错，用户:{}-->异常：{}-->异常最后一行：{}".format(token, e, formatted_lines[-1])
            # 将抛出的异常存入数据库中
            self.insert_log(token=token, uid=uid, file_name=fname, line_no=lineno, message=message)

    # 转跳1
    def redirect_url(self, response):
        token = response.meta["token"]
        uid = response.meta['uid']
        yield scrapy.Request(url='https://www.taobao.com/',
                             headers=self.headers,
                             meta={
                                 "cookiejar": response.meta["cookiejar"],
                                 "proxy": response.meta["proxy"],
                                 "token": token,
                                 'uid': uid,
                             },
                             callback=self.redirect_url2,
                             dont_filter=True,
                             )

    # 转跳2
    def redirect_url2(self, response):
        token = response.meta["token"]
        uid = response.meta['uid']
        if '淘宝网' in response.text:
            yield scrapy.Request(url='https://member1.taobao.com/member/fresh/account_security.htm',
                                 headers=self.headers,
                                 meta={"cookiejar": response.meta["cookiejar"],
                                       "proxy": response.meta["proxy"],
                                       "token": token,
                                       'uid': uid,
                                       },
                                 callback=self.yes,
                                 dont_filter=True,
                                 )
        else:
            self.change_crawl_status(token, "-1")  # 将爬虫任务设置为-1,数据获取失败
            self.logger.info("跳转1失败用户:{}".format(token))

    def yes(self, response):
        token = response.meta["token"]
        uid = response.meta['uid']
        if '您的基础信息' in response.text:
            self.logger.info('用户{}登陆成功，开始解析'.format(token))
            yield scrapy.Request(url=self.baseInfoSet_url,
                                 headers=self.headers,
                                 meta={"cookiejar": response.meta["cookiejar"],
                                       "proxy": response.meta["proxy"],
                                       "token": token,
                                       'uid': uid,
                                       },
                                 callback=self.basic_info,
                                 dont_filter=True,
                                 )
        else:
            self.change_crawl_status(token, "-1")  # 将爬虫任务设置为-1,数据获取失败
            self.logger.info('跳转2失败：用户{}登陆失败'.format(token))

    #   以下为解析数据      #################################################
    # 解析个人资料，个人交易信息,安全设置，认证，评价页面
    # 昵称
    def basic_info(self, response):
        token = response.meta["token"]
        uid = response.meta['uid']
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            data_list = dict()
            data_list['nickName'] = "".join(soup.find(id="J_uniqueName-mask")['value'])  # 昵称
            yield scrapy.Request(url=self.account_url,
                                 headers=self.headers,
                                 meta={"cookiejar": response.meta["cookiejar"],
                                       "proxy": response.meta["proxy"],
                                       'data': data_list,
                                       "token": token,
                                       'uid': uid,
                                       },
                                 callback=self.account,
                                 dont_filter=True,
                                 )
        except Exception as e:
            self.logger.error('解析用户{}个人资料页请求昵称出错:{}'.format(token, e))
            # 对抛出的一场进行处理
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fname = "".join(os.path.split(exc_traceback.tb_frame.f_code.co_filename))  # 异常抛出的文件
            lineno = exc_traceback.tb_lineno  # 异常出现在哪一行
            uid = uid  # log表中的uid
            formatted_lines = traceback.format_exc().splitlines()  # 获取整个异常中
            # 异常描述
            message = "解析个人资料页请求昵称出错，用户:{}-->异常：{}-->异常最后一行：{}".format(token, e, formatted_lines[-1])
            # 将抛出的异常存入数据库中
            self.insert_log(token=token, uid=uid, file_name=fname, line_no=lineno, message=message)

    # 真实姓名，性别，出生日期
    def account(self, response):
        token = response.meta["token"]
        uid = response.meta['uid']
        try:
            name = "".join(response.xpath('//*[@id="ah:addressForm"]/li[1]/strong/text()').get())  # 真实姓名
            soup = BeautifulSoup(response.text, 'html.parser')
            gender = "".join(re.findall(
                re.compile(r'checked.*?/><label>(男|女)</label>'),
                response.text))
            if not gender:
                gender = "保密"
            year = "".join(soup.find('input', attrs={"class": "inputtext input-year"})['value'])
            month = "".join(soup.find('input', attrs={"class": "inputtext input-date"})['value'])
            day = "".join(soup.find('input', attrs={"name": "_fm.ed._0.bir"})['value'])
            birthday = year + '-' + month + '-' + day  # 出生日期
            # 更新data_list
            data_list = response.meta['data']
            data_list['name'] = name
            data_list['gender'] = gender
            data_list['birthday'] = birthday
            yield scrapy.Request(url=self.security_url,
                                 headers=self.headers,
                                 meta={"cookiejar": response.meta["cookiejar"],
                                       "proxy": response.meta["proxy"],
                                       'data': data_list,
                                       "token": token,
                                       'uid': uid,
                                       },
                                 callback=self.security,
                                 dont_filter=True,
                                 )
        except Exception as e:
            self.logger.error('解析用户{}个人资料页请求真实姓名，性别，出生日期出错:{}'.format(token, e))
            # 对抛出的一场进行处理
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fname = "".join(os.path.split(exc_traceback.tb_frame.f_code.co_filename))  # 异常抛出的文件
            lineno = exc_traceback.tb_lineno  # 异常出现在哪一行
            uid = uid  # log表中的uid
            formatted_lines = traceback.format_exc().splitlines()  # 获取整个异常中
            # 异常描述
            message = "解析个人资料页请求真实姓名，性别，出生日期出错，用户:{}-->异常：{}-->异常最后一行：{}".format(token, e, formatted_lines[-1])
            # 将抛出的异常存入数据库中
            self.insert_log(token=token, uid=uid, file_name=fname, line_no=lineno, message=message)

    # 手机号码，安全等级，用户名，邮箱
    def security(self, response):
        token = response.meta["token"]
        uid = response.meta['uid']
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            mobile = "".join(soup.find('span', attrs={"class": "default grid-msg"}).get_text().strip())  # 手机号码
            security_level = "".join(  # 安全等级
                response.xpath('//*[@id="main-content"]/dl/dd[2]/div/div/div[1]/span/text()').extract(
                ))  # 用户名
            username = "".join(
                response.xpath('//ul[@class="account-info"]/li[1]/span[2]/text()').extract())
            email = "".join(response.xpath('//ul[@class="account-info"]/li[2]/span[3]/text()').extract()) + \
                    "".join(
                        response.xpath('//ul[@class="account-info"]/li[2]/span[2]/text()').extract())  # 邮箱
            # 更新data_list
            data_list = response.meta['data']
            data_list['mobile'] = mobile
            data_list['security_level'] = security_level
            data_list['username'] = username
            data_list['email'] = email
            yield scrapy.Request(url=self.certify_url,
                                 headers=self.headers,
                                 meta={"cookiejar": response.meta["cookiejar"],
                                       "proxy": response.meta["proxy"],
                                       'data': data_list,
                                       "token": token,
                                       'uid': uid,
                                       },
                                 callback=self.certify,
                                 dont_filter=True,
                                 )
        except Exception as e:
            self.logger.error('解析用户{}安全设置页请求手机号码，安全等级，用户名，邮箱出错:{}'.format(token, e))
            # 对抛出的一场进行处理
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fname = "".join(os.path.split(exc_traceback.tb_frame.f_code.co_filename))  # 异常抛出的文件
            lineno = exc_traceback.tb_lineno  # 异常出现在哪一行
            uid = uid  # log表中的uid
            formatted_lines = traceback.format_exc().splitlines()  # 获取整个异常中
            # 异常描述
            message = "解析安全设置页请求手机号码，安全等级，用户名，邮箱出错，用户:{}-->异常：{}-->异常最后一行：{}".format(token, e, formatted_lines[-1])
            # 将抛出的异常存入数据库中
            self.insert_log(token=token, uid=uid, file_name=fname, line_no=lineno, message=message)

    # 认证渠道，身份证号码
    def certify(self, response):
        token = response.meta["token"]
        uid = response.meta['uid']
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            identity_channel = "".join(soup.find('div', attrs={'class': "left"}).get_text())  # 认证渠道
            identityno = soup.find('span', text='18位身份证号：')
            identity_no = "".join(identityno.next_sibling.next_sibling.get_text())  # 身份证号码
            # 更新data_list
            data_list = response.meta['data']
            data_list['identity_channel'] = identity_channel
            data_list['identity_no'] = identity_no
            yield scrapy.Request(url=self.my_rate_url,
                                 headers=self.headers,
                                 meta={"cookiejar": response.meta["cookiejar"],
                                       "proxy": response.meta["proxy"],
                                       'data': data_list,
                                       "token": token,
                                       'uid': uid,
                                       },
                                 callback=self.my_rate,
                                 dont_filter=True,
                                 )
        except Exception as e:
            self.logger.error('用户{}认证渠道，身份证号码页请求出错:{}'.format(token, e))
            # 对抛出的一场进行处理
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fname = "".join(os.path.split(exc_traceback.tb_frame.f_code.co_filename))  # 异常抛出的文件
            lineno = exc_traceback.tb_lineno  # 异常出现在哪一行
            uid = uid  # log表中的uid
            formatted_lines = traceback.format_exc().splitlines()  # 获取整个异常中
            # 异常描述
            message = "认证渠道，身份证号码页请求出错，用户:{}-->异常：{}-->异常最后一行：{}".format(token, e, formatted_lines[-1])
            # 将抛出的异常存入数据库中
            self.insert_log(token=token, uid=uid, file_name=fname, line_no=lineno, message=message)

    # 好评率，信用积分
    def my_rate(self, response):
        token = response.meta["token"]
        uid = response.meta['uid']
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            favorable_rate = "".join(
                soup.find('p', attrs={'class': "rate-summary"}).contents[1].get_text())  # 好评率
            credit_point = "".join(
                soup.find('h4', attrs={'class': "tb-rate-ico-bg ico-buyer"}).contents[1].get_text())  # 信用积分
            # 更新data_list
            data_list = response.meta['data']
            data_list['favorable_rate'] = favorable_rate
            data_list['credit_point'] = credit_point
            yield scrapy.Request(url=self.t_vip_url.format(self.timestamp),
                                 headers=self.headers,
                                 meta={"cookiejar": response.meta["cookiejar"],
                                       "proxy": response.meta["proxy"],
                                       'data': data_list,
                                       "token": token,
                                       'uid': uid,
                                       },
                                 callback=self.vip,
                                 dont_filter=True,
                                 )
        except Exception as e:
            self.logger.error('解析用户{}好评率，信用积分页请求出错:{}'.format(token, e))
            # 对抛出的一场进行处理
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fname = "".join(os.path.split(exc_traceback.tb_frame.f_code.co_filename))  # 异常抛出的文件
            lineno = exc_traceback.tb_lineno  # 异常出现在哪一行
            uid = uid  # log表中的uid
            formatted_lines = traceback.format_exc().splitlines()  # 获取整个异常中
            # 异常描述
            message = "解析好评率，信用积分页请求出错，用户:{}-->异常：{}-->异常最后一行：{}".format(token, e, formatted_lines[-1])
            # 将抛出的异常存入数据库中
            self.insert_log(token=token, uid=uid, file_name=fname, line_no=lineno, message=message)

    # 成长值，会员等级 (提交获取sign需要的token值url)
    def vip(self, response):
        # 解决请求过快
        time.sleep(1)
        token = response.meta["token"]
        uid = response.meta['uid']
        try:
            match1 = re.sub(r'jsonp\d+\(', '', response.text[:-2])
            dict1 = json.loads(match1)
            growth_value = dict1['data']['taoScore']
            if growth_value < 1000:
                vip_level = '普通会员'
            else:
                vip_level = '超级会员'  # 会员等级
                growth_value = str(growth_value)  # 成长值
            #
            item = BasicinfoItem()
            data_list = response.meta['data']
            item['token'] = token
            item['username'] = data_list['username']
            item['nickName'] = data_list['nickName']
            item['gender'] = data_list['gender']
            item['birthday'] = data_list['birthday']
            item['name'] = data_list['name']
            item['identity_no'] = data_list['identity_no']
            item['identity_channel'] = data_list['identity_channel']
            item['email'] = data_list['email']
            item['mobile'] = data_list['mobile']
            item['vip_level'] = vip_level
            item['growth_value'] = growth_value
            item['credit_point'] = data_list['credit_point']
            item['favorable_rate'] = data_list['favorable_rate']
            item['security_level'] = data_list['security_level']
            yield item
        except Exception as e:
            self.logger.error('解析用户{}成长值，会员等级出错:{}'.format(token, e))
            # 对抛出的一场进行处理
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fname = "".join(os.path.split(exc_traceback.tb_frame.f_code.co_filename))  # 异常抛出的文件
            lineno = exc_traceback.tb_lineno  # 异常出现在哪一行
            uid = uid  # log表中的uid
            formatted_lines = traceback.format_exc().splitlines()  # 获取整个异常中
            # 异常描述
            message = "解析成长值，会员等级出错,用户:{}-->异常：{}-->异常最后一行：{}".format(token, e, formatted_lines[-1])
            # 将抛出的异常存入数据库中
            self.insert_log(token=token, uid=uid, file_name=fname, line_no=lineno, message=message)
        # 随便给地址
        url = 'http://h5api.m.taobao.com/h5/mtop.cainiao.address.ua.global.area.list/1.0/?jsv=2.4.2&appKey=12574478&t=1534313870148&sign=a677552e4506da78c5886fd7fa60428c&api=mtop.cainiao.address.ua.global.area.list&v=1.0&dataType=jsonp&type=jsonp&callback=mtopjsonp1&data=%7B%22sn%22%3A%22suibianchuan%22%7D'
        yield scrapy.Request(url=url,
                             callback=self.parse_token,
                             meta={"cookiejar": response.meta["cookiejar"],
                                   "proxy": response.meta["proxy"],
                                   "token": token,
                                   'uid': uid,
                                   },
                             headers=self.address_headers,
                             dont_filter=True,
                             )

    # 去获取到加密sign的token参数
    def parse_token(self, response):
        token = response.meta["token"]
        uid = response.meta['uid']
        try:
            set_cookie = response.headers.getlist('Set-Cookie')
            token1 = self.get_token_from_cookie(set_cookie, token, uid)
            sign_time = int(time.time() * 1000)
            sign = self.get_sign(sign_time, token1, token, uid)
            yield scrapy.Request(url=self.address_url.format(sign_time, sign),
                                 headers=self.address_headers,
                                 meta={"cookiejar": response.meta["cookiejar"],
                                       "proxy": response.meta["proxy"],
                                       "token": token,
                                       'uid': uid,
                                       },
                                 callback=self.address,
                                 dont_filter=True,
                                 )
        except Exception as e:
            self.logger.error('用户{}随便给地址response,Set-Cookie出错:{}'.format(token, e))
            # 对抛出的一场进行处理
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fname = "".join(os.path.split(exc_traceback.tb_frame.f_code.co_filename))  # 异常抛出的文件
            lineno = exc_traceback.tb_lineno  # 异常出现在哪一行
            uid = uid  # log表中的uid
            formatted_lines = traceback.format_exc().splitlines()  # 获取整个异常中
            # 异常描述
            message = "随便给地址response,Set-Cookie出错，用户:{}-->异常：{}-->异常最后一行：{}".format(token, e, formatted_lines[-1])
            # 将抛出的异常存入数据库中
            self.insert_log(token=token, uid=uid, file_name=fname, line_no=lineno, message=message)

    # 解析收货地址页面 (提交订单页面url)
    def address(self, response):
        token = response.meta["token"]
        uid = response.meta['uid']
        item2 = AddressItem()
        try:
            data = ''.join(re.findall(re.compile(r'sonp3\((.+)'), response.text[:-1])
                           ).replace('\\', '').replace('\"[', '[').replace(']\"', ']')
            data_list = json.loads(data)
            for result in data_list['data']['returnValue']:
                address_detail = result["addressDetail"] if "addressDetail" in result else '-'
                full_address = result["fullAddress"] if "fullAddress" in result else '-'
                item2['token'] = token
                item2['name'] = result["fullName"] if "fullName" in result else '-'  # 收件人
                item2['mobile'] = result["mobile"] if "mobile" in result else '-'  # 收件人电话
                item2['zipCode'] = result["post"] if "post" in result else '-'  # 邮箱
                item2['isDefault'] = result["defaultCode"] if "defaultCode" in result else '-'  # 是否为默认地址
                item2['address'] = "{} {}".format(full_address, address_detail)  # 详细地址
                yield item2
        except Exception as e:
            item2['token'] = token
            item2['name'] = '-'
            item2['mobile'] = '-'
            item2['zipCode'] = '-'
            item2['address'] = '-'
            item2['isDefault'] = '-'
            yield item2
            self.logger.error('收货地址页解析用户{}出错:{}'.format(token, e))
            # 对抛出的一场进行处理
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fname = "".join(os.path.split(exc_traceback.tb_frame.f_code.co_filename))  # 异常抛出的文件
            lineno = exc_traceback.tb_lineno  # 异常出现在哪一行
            uid = uid  # log表中的uid
            formatted_lines = traceback.format_exc().splitlines()  # 获取整个异常中
            # 异常描述
            message = "收货地址页解析出错,用户:{}-->异常：{}-->异常最后一行：{}".format(token, e, formatted_lines[-1])
            # 将抛出的异常存入数据库中
            self.insert_log(token=token, uid=uid, file_name=fname, line_no=lineno, message=message)
        # 进入订单页面
        yield scrapy.Request(url=self.page_url,
                             headers=self.headers,
                             meta={"cookiejar": response.meta["cookiejar"],
                                   "proxy": response.meta["proxy"],
                                   "token": token,
                                   'uid': uid,
                                   },
                             callback=self.page,
                             dont_filter=True,
                             )

    # 已存在订单第一次请求
    def page(self, response):
        token = response.meta["token"]
        uid = response.meta['uid']
        page_num = 1
        orders_data = {
            'buyerNick': '',
            'dateBegin': '0',
            'dateEnd': '0',
            'lastStartRow': '',
            'logisticsService': '',
            'options': '0',
            'orderStatus': '',
            'pageNum': str(page_num),  # page
            'pageSize': '15',
            'queryBizType': '',
            'queryOrder': 'desc',
            'rateStatus': '',
            'refund': '',
            'sellerNick': '',
            'prePageNo': '1',
        }
        yield scrapy.FormRequest(url=self.orders_url,
                                 headers=self.orders_headers,
                                 meta={"cookiejar": response.meta["cookiejar"],
                                       "proxy": response.meta["proxy"],
                                       "page_num": page_num,  # #
                                       "token": token,
                                       'uid': uid,
                                       },
                                 formdata=orders_data,
                                 method='POST',
                                 callback=self.orders,
                                 dont_filter=True,
                                 )

    # 订单后面页数//解析订单详情url获取及提交详情url，解析订单商品信息，解析订单信息
    def orders(self, response):
        token = response.meta["token"]
        uid = response.meta['uid']
        try:
            if len(json.loads(response.text)["mainOrders"]) != 0:  # 判断页面加载完成
                # 记录完成订单数
                if response.url == self.orders_url:
                    self.logger.info('用户{}已存在订单完成{}页'.format(token, response.meta["page_num"]))
                else:
                    self.logger.info('用户{}回收站订单完成{}页'.format(token, response.meta["page_num2"]))
                # 解析
                try:  # 进行解析提取每个订单的url
                    data = json.loads(response.text)
                    for objects in data["mainOrders"]:
                        item = OrdersItem()
                        # 以下是订单信息
                        order_id = str(objects["id"])  # 订单号
                        order_createtime = objects["orderInfo"]["createTime"]  # 订单时间
                        order_rmb = objects["payInfo"]["actualFee"]  # 订单金额
                        order_status = objects["statusInfo"]["text"]  # 订单状态

                        # 以下是商品信息
                        # 解决一个订单多个商品
                        for goods in objects["subOrders"]:
                            item1 = GoodsItem()
                            goods_id = str(goods["itemInfo"]["id"]) if 'id' in goods else '-'  # 商品ID
                            goods_name = goods["itemInfo"]["title"] if "title" in goods[
                                "itemInfo"] else '-'  # 商品名称
                            goods_url = 'https:' + goods["itemInfo"]["itemUrl"] if "itemUrl" in goods[
                                "itemInfo"] else '-'  # 商品URL
                            goods_price = goods["priceInfo"]["realTotal"] if "realTotal" in goods[
                                "priceInfo"] else '-'  # 商品单价
                            goods_nums = goods["quantity"] if "quantity" in goods else '-'  # 商品数量
                            item1['token'] = token
                            item1['goods_id'] = goods_id
                            item1['goods_name'] = goods_name
                            item1['goods_url'] = goods_url
                            item1['goods_price'] = goods_price
                            item1['goods_nums'] = goods_nums
                            item1['order_id'] = order_id
                            yield item1
                        # 以下是解析物流信息而取请求详情页面
                        list_object = objects["statusInfo"]["operations"]
                        detail_url = self.get_detail_url(list_object, token, uid)
                        # 电影，火车，酒店，保险，
                        if 'dianying.taobao' in detail_url or 'trip.taobao' in detail_url \
                                or 'prod-baoxian' in detail_url:
                            item['token'] = token
                            item['order_id'] = order_id
                            item['order_createtime'] = order_createtime
                            item['order_rmb'] = order_rmb
                            item['order_status'] = order_status
                            item['deliver_type'] = '-'  # 运送方式
                            item['deliver_company'] = '-'  # 物流公司
                            item['deliver_no'] = '-'  # 运单号
                            item['consignee'] = '-'  # 收货人姓名
                            item['consignee_mobile'] = '-'  # 收货人电话
                            item['consignee_address'] = '-'  # 收货地址
                            yield item
                        # 没有详情
                        elif 'nourl' in detail_url:
                            item['token'] = token
                            item['order_id'] = order_id
                            item['order_createtime'] = order_createtime
                            item['order_rmb'] = order_rmb
                            item['order_status'] = order_status
                            item['deliver_type'] = '-'
                            item['deliver_company'] = '-'
                            item['deliver_no'] = '-'
                            item['consignee'] = '-'
                            item['consignee_mobile'] = '-'
                            item['consignee_address'] = '-'
                            yield item
                        # 天猫物流信息 提交url 给tmall函数解析
                        elif 'trade.tmall' in detail_url:
                            yield scrapy.Request(url=detail_url,
                                                 headers=self.detail_headers,
                                                 meta={"cookiejar": response.meta["cookiejar"],
                                                       "proxy": response.meta["proxy"],
                                                       'order_id': order_id,
                                                       'order_createtime': order_createtime,
                                                       'order_rmb': order_rmb,
                                                       'order_status': order_status,
                                                       "token": token,
                                                       'uid': uid,
                                                       },
                                                 callback=self.tmall_detail,
                                                 dont_filter=True,
                                                 )
                        # 淘宝物流信息 提交url 给taobao函数解析
                        else:
                            yield scrapy.Request(url=detail_url,
                                                 headers=self.detail_headers,
                                                 meta={"cookiejar": response.meta["cookiejar"],
                                                       "proxy": response.meta["proxy"],
                                                       'order_id': order_id,
                                                       'order_createtime': order_createtime,
                                                       'order_rmb': order_rmb,
                                                       'order_status': order_status,
                                                       "token": token,
                                                       'uid': uid,
                                                       },
                                                 callback=self.taobao_detail,
                                                 dont_filter=True,
                                                 )
                except Exception as e:
                    if response.url == self.orders_url:
                        self.logger.error('用户{}已存在订单第{}页详情url获取,解析订单商品信息，解析订单信息出错:{}'.format(
                            token, response.meta["page_num"], e))
                    else:
                        self.logger.error('用户{}回收站订单第{}页详情url获取,解析订单商品信息，解析订单信息出错:{}'.format(
                            token, response.meta["page_num2"], e))
                    # 对抛出的一场进行处理
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    fname = "".join(os.path.split(exc_traceback.tb_frame.f_code.co_filename))  # 异常抛出的文件
                    lineno = exc_traceback.tb_lineno  # 异常出现在哪一行
                    uid = uid  # log表中的uid
                    formatted_lines = traceback.format_exc().splitlines()  # 获取整个异常中
                    # 异常描述
                    message = "订单详情url获取,解析订单商品信息，解析订单信息出错,用户:{}-->异常：{}-->异常最后一行：{}".format(token, e,
                                                                                             formatted_lines[-1])
                    # 将抛出的异常存入数据库中
                    self.insert_log(token=token, uid=uid, file_name=fname, line_no=lineno, message=message)
                if len(json.loads(response.text)["mainOrders"]) == 15:
                    # 当前请求是正常订单的地址 /非回收站订单
                    if response.url == self.orders_url:
                        page_num = response.meta["page_num"]
                        orders_data = {
                            'buyerNick': '',
                            'dateBegin': '0',
                            'dateEnd': '0',
                            'lastStartRow': '',
                            'logisticsService': '',
                            'options': '0',
                            'orderStatus': '',
                            'pageNum': str(int(page_num) + 1),
                            'pageSize': '15',
                            'queryBizType': '',
                            'queryOrder': 'desc',
                            'rateStatus': '',
                            'refund': '',
                            'sellerNick': '',
                            'prePageNo': '1',
                        }
                        # 提交每一页的地址，自解析a
                        yield scrapy.FormRequest(url=self.orders_url,
                                                 headers=self.orders_headers,
                                                 meta={"cookiejar": response.meta["cookiejar"],
                                                       "proxy": response.meta["proxy"],
                                                       "page_num": str(int(page_num) + 1),
                                                       "token": token,
                                                       'uid': uid,
                                                       },
                                                 formdata=orders_data,
                                                 method='POST',
                                                 callback=self.orders,  # 自循环解析
                                                 dont_filter=True,
                                                 )
                    # 回收站订单
                    else:
                        page_num2 = response.meta["page_num2"]
                        fromdata = {
                            'pageNum': "{}".format(str(int(page_num2) + 1)),
                            'pageSize': '15',
                            'tabCode': 'recycle',
                            'prePageNo': '1',
                        }
                        yield scrapy.FormRequest(url=self.recyled_url,
                                                 headers=self.recyled_headers,
                                                 meta={"cookiejar": response.meta["cookiejar"],
                                                       "proxy": response.meta["proxy"],
                                                       "page_num2": str(int(page_num2) + 1),
                                                       "token": token,
                                                       'uid': uid,
                                                       },
                                                 formdata=fromdata,
                                                 method='POST',
                                                 callback=self.orders,
                                                 dont_filter=True,
                                                 )
                else:
                    if response.url == self.orders_url:
                        # 已存在订单已经完成了，开始请求回收站订单
                        page_num2 = 1
                        fromdata = {
                            'pageNum': str(page_num2),
                            'pageSize': '15',
                            'tabCode': 'recycle',
                            'prePageNo': '1',
                        }
                        yield scrapy.FormRequest(url=self.recyled_url,
                                                 headers=self.recyled_headers,
                                                 meta={"cookiejar": response.meta["cookiejar"],
                                                       "proxy": response.meta["proxy"],
                                                       "page_num2": page_num2,
                                                       "token": token,
                                                       'uid': uid,
                                                       },
                                                 formdata=fromdata,
                                                 method='POST',
                                                 callback=self.orders,
                                                 dont_filter=True,
                                                 )
                    # 已经是把回收站订单都爬完了
                    else:
                        self.change_crawl_status(token, '2')
                        self.logger.info('用户{}所有订单页面完成'.format(token))
            # 当前页订单为0
            else:
                # 已存在订单已经完成了，开始请求回收站订单
                if response.url == self.orders_url:
                    page_num2 = 1
                    fromdata = {
                        'pageNum': "{}".format(str(page_num2)),
                        'pageSize': '15',
                        'tabCode': 'recycle',
                        'prePageNo': '1',
                    }
                    yield scrapy.FormRequest(url=self.recyled_url,
                                             headers=self.recyled_headers,
                                             meta={"cookiejar": response.meta["cookiejar"],
                                                   "proxy": response.meta["proxy"],
                                                   "page_num2": str(page_num2),
                                                   "token": token,
                                                   'uid': uid,
                                                   },
                                             formdata=fromdata,
                                             method='POST',
                                             callback=self.orders,
                                             dont_filter=True,
                                             )
                # 如果订单数量为0 并且 是回收站订单 则 订单处理完成
                else:
                    self.change_crawl_status(token, '2')
                    self.logger.info('用户{}所有订单页面完成'.format(token))
        except Exception as e:
            self.logger.error('用户{}第一页订单页面请求返回数据异常：{}'.format(token, e))
            # 对抛出的异常进行处理
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fname = "".join(os.path.split(exc_traceback.tb_frame.f_code.co_filename))  # 异常抛出的文件
            lineno = exc_traceback.tb_lineno  # 异常出现在哪一行
            uid = uid  # log表中的uid
            formatted_lines = traceback.format_exc().splitlines()  # 获取整个异常中
            # 异常描述
            message = "第一页订单页面请求返回数据异常,用户:{}-->异常：{}-->异常最后一行：{}".format(token, e, formatted_lines[-1])
            # 将抛出的异常存入数据库中
            self.insert_log(token=token, uid=uid, file_name=fname, line_no=lineno, message=message)

    # 解析已存在和回收站详情订单获取淘宝物流信息，分俩种情况，json与HTML
    def taobao_detail(self, response):
        token = response.meta["token"]
        uid = response.meta['uid']
        item = OrdersItem()
        try:
            # 正则匹配物流
            data1 = "".join(re.findall(re.compile(r"JSON\.parse\('(.+?}})'\);"), response.text))  #
            data = data1.encode('utf8').decode('unicode_escape')
            if data:
                data_dict = json.loads(data)
                if "deliveryInfo" in data_dict:
                    deliver_type = data_dict["deliveryInfo"]["shipType"] if 'shipType' in data_dict[
                        'deliveryInfo'] else '-'  # 运送方式
                    deliver_company = data_dict["deliveryInfo"]["logisticsName"] if 'logisticsName' in data_dict[
                        'deliveryInfo'] else '-'  # 物流公司
                    deliver_no = data_dict["deliveryInfo"]["logisticsNum"] if "logisticsNum" in data_dict[
                        "deliveryInfo"] else '-'  # 运单号
                    if 'address' in data_dict['deliveryInfo']:
                        consignees = data_dict['deliveryInfo']['address'].replace('\n', '').replace('\t', '')
                        if '，' in consignees:
                            consignee_list2 = consignees.split('，')  # 中文逗号 #是一个list
                        elif ',' in consignees:
                            consignee_list2 = consignees.split(',')
                        else:
                            consignee_list2 = consignees.split()
                        if len(consignee_list2) == 0:  # 防止没有收货地址
                            # 收货人姓名
                            consignee = '-'
                            # 电话
                            consignee_mobile = '-'
                            # 地址
                            consignee_address = '-'
                        elif len(consignee_list2) == 1:
                            # 收货人姓名
                            consignee = consignee_list2[0]
                            # 电话
                            consignee_mobile = '-'
                            # 地址
                            consignee_address = '-'
                        elif len(consignee_list2) == 2:
                            # 收货人姓名
                            consignee = consignee_list2[0]
                            # 电话
                            consignee_mobile = consignee_list2[1]
                            # 地址
                            consignee_address = '-'
                        else:
                            # 收货人姓名
                            consignee = consignee_list2[0]
                            # 电话
                            consignee_mobile = consignee_list2[1]
                            # 地址
                            if consignee_list2[2] is None:
                                consignee_address = consignee_list2[3]
                            else:
                                consignee_address = consignee_list2[2]
                    else:
                        # 收货人姓名
                        consignee = '-'
                        # 电话
                        consignee_mobile = '-'
                        # 地址
                        consignee_address = '-'
                else:
                    deliver_type = '-'
                    deliver_company = '-'
                    deliver_no = '-'
                    consignee = '-'
                    consignee_mobile = '-'
                    consignee_address = '-'
                item['token'] = token
                item['order_id'] = response.meta['order_id']
                item['order_createtime'] = response.meta['order_createtime']
                item['order_rmb'] = response.meta['order_rmb']
                item['order_status'] = response.meta['order_status']
                item['deliver_type'] = deliver_type
                item['deliver_company'] = deliver_company
                item['deliver_no'] = deliver_no
                item['consignee'] = consignee
                item['consignee_mobile'] = consignee_mobile
                item['consignee_address'] = consignee_address
                yield item
            # 旧式页面  使用BS或者Xpath提取物流
            else:
                try:
                    # 运送方式
                    deliver_type = '快递'
                    # 物流公司
                    deliver_company = "".join(response.xpath(
                        '//table[@class="simple-list logistics-list"]/tbody/tr[5]/td[2]/text()').extract()).strip()
                    # 送货单号
                    deliver_no = "".join(response.xpath(
                        '//table[@class="simple-list logistics-list"]/tbody/tr[6]/td[2]/text()').extract())
                    deliver_no = deliver_no.replace('\n', '').replace(' ', '').replace('\t', '').strip()
                    # 收货人姓名 ，电话，地址
                    consignees1 = "".join(response.xpath(
                        '//table[@class="simple-list logistics-list"]/tbody/tr[3]/td[2]/text()').extract()) \
                        .replace('\n', '').replace('\t', '')
                    if '，' in consignees1 and ',' in consignees1:
                        consignee2 = consignees1.split(',')
                    elif '，' in consignees1:
                        consignee2 = consignees1.split('，')  # 中文逗号 ，是一个list
                    elif ',' in consignees1:
                        consignee2 = consignees1.split(',')
                    else:
                        consignee2 = consignees1.split()
                    if len(consignee2) == 0:  # 防止没有收货地址
                        # 收货人姓名
                        consignee = '-'
                        # 电话
                        consignee_mobile = '-'
                        # 地址
                        consignee_address = '-'
                    elif len(consignee2) == 1:
                        # 收货人姓名
                        consignee = consignee2[0].strip()
                        # 电话
                        consignee_mobile = '-'
                        # 地址
                        consignee_address = '-'
                    elif len(consignee2) == 2:
                        # 收货人姓名
                        consignee = consignee2[0].strip()
                        # 电话
                        consignee_mobile = consignee2[1].strip()
                        # 地址
                        consignee_address = '-'
                    else:
                        consignee = consignee2[0].strip()
                        # 电话
                        consignee_mobile = consignee2[1].strip()
                        # 地址
                        if consignee2[2] == '':
                            consignee_address = consignee2[3].strip()
                        else:
                            consignee_address = consignee2[2].strip()
                    item['token'] = token
                    item['order_id'] = response.meta['order_id']
                    item['order_createtime'] = response.meta['order_createtime']
                    item['order_rmb'] = response.meta['order_rmb']
                    item['order_status'] = response.meta['order_status']
                    item['deliver_type'] = deliver_type
                    item['deliver_company'] = deliver_company
                    item['deliver_no'] = deliver_no
                    item['consignee'] = consignee
                    item['consignee_mobile'] = consignee_mobile
                    item['consignee_address'] = consignee_address
                    yield item
                except Exception as e:
                    item['token'] = token
                    item['order_id'] = response.meta['order_id']
                    item['order_createtime'] = response.meta['order_createtime']
                    item['order_rmb'] = response.meta['order_rmb']
                    item['order_status'] = response.meta['order_status']
                    item['deliver_type'] = '-'
                    item['deliver_company'] = '-'
                    item['deliver_no'] = '-'
                    item['consignee'] = '-'
                    item['consignee_mobile'] = '-'
                    item['consignee_address'] = '-'
                    yield item
                    self.logger.error('淘宝旧式页面解析用户{}错误:{}订单号为：{}'.format(token, e, response.meta['order_id']))
                    # 对抛出的一场进行处理
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    fname = "".join(os.path.split(exc_traceback.tb_frame.f_code.co_filename))  # 异常抛出的文件
                    lineno = exc_traceback.tb_lineno  # 异常出现在哪一行
                    uid = uid  # log表中的uid
                    formatted_lines = traceback.format_exc().splitlines()  # 获取整个异常中
                    # 异常描述
                    message = "淘宝旧式页面解析错误订单号为：{},用户:{}-->异常：{}-->异常最后一行：{}".format(
                        response.meta['order_id'], token, e, formatted_lines[-1])
                    # 将抛出的异常存入数据库中
                    self.insert_log(token=token, uid=uid, file_name=fname, line_no=lineno, message=message)

        except Exception as e:
            item['token'] = token
            item['order_id'] = response.meta['order_id']
            item['order_createtime'] = response.meta['order_createtime']
            item['order_rmb'] = response.meta['order_rmb']
            item['order_status'] = response.meta['order_status']
            item['deliver_type'] = '-'
            item['deliver_company'] = '-'
            item['deliver_no'] = '-'
            item['consignee'] = '-'
            item['consignee_mobile'] = '-'
            item['consignee_address'] = '-'
            yield item
            self.logger.error('淘宝物流的解析用户{}出错:{}订单号为：{} ，订单url：'.format(
                token, e, response.meta['order_id'], response.url))
            # 对抛出的一场进行处理
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fname = "".join(os.path.split(exc_traceback.tb_frame.f_code.co_filename))  # 异常抛出的文件
            lineno = exc_traceback.tb_lineno  # 异常出现在哪一行
            uid = uid  # log表中的uid
            formatted_lines = traceback.format_exc().splitlines()  # 获取整个异常中
            # 异常描述
            message = "淘宝物流的解析出错订单号为：{},用户:{}-->异常：{}-->异常最后一行：{}".format(response.meta['order_id'], token, e,
                                                                          formatted_lines[-1])
            # 将抛出的异常存入数据库中
            self.insert_log(token=token, uid=uid, file_name=fname, line_no=lineno, message=message)

    # 解析已存在和回收站详情订单获取天猫物流信息
    def tmall_detail(self, response):
        token = response.meta["token"]
        uid = response.meta['uid']
        item = OrdersItem()
        try:
            # 新版本：用正则解析
            # script1 = re.search(r'\{\"ad\"\:.+', response.text).group(0)
            script1 = "".join(re.findall(re.compile(r'\{\"ad\"\:.+'), response.text))
            if script1:
                dict_data = json.loads(script1)
                if 'logistic' in dict_data['orders']['list'][0]:
                    if 'content' in dict_data['orders']['list'][0]['logistic']:
                        if 'companyName' in dict_data['orders']['list'][0]['logistic']['content'][0]:
                            deliver_type = '快递'
                            if 'companyName' in dict_data['orders']['list'][0]['logistic']['content'][0]:
                                deliver_company = dict_data['orders']['list'][0]['logistic']['content'][0][
                                    'companyName']
                            else:
                                deliver_company = '-'
                            if 'mailNo' in dict_data['orders']['list'][0]['logistic']['content'][0]:
                                deliver_no = dict_data['orders']['list'][0]['logistic']['content'][0]['mailNo']
                            else:
                                deliver_no = '-'
                            consignee = dict_data['basic']['lists'][0]['content'][0]['text'].replace('\n', '').replace(
                                '\t', '')
                            if '，' in consignee and ',' in consignee:
                                consignee3 = consignee.split(',')
                            elif '，' in consignee:
                                consignee3 = consignee.split('，')  # 中文逗号 #是一个list
                            elif ',' in consignee:
                                consignee3 = consignee.split(',')
                            else:
                                consignee3 = consignee.split()
                            if len(consignee3) == 0:  # 防止没有收货地址
                                # 收货人姓名
                                consignee = '-'
                                # 电话
                                consignee_mobile = '-'
                                # 地址
                                consignee_address = '-'

                            elif len(consignee3) == 1:
                                # 收货人姓名
                                consignee = consignee3[0].strip()
                                # 电话
                                consignee_mobile = '-'
                                # 地址
                                consignee_address = '-'
                            elif len(consignee3) == 2:
                                # 收货人姓名
                                consignee = consignee3[0].strip()
                                # 电话
                                consignee_mobile = consignee3[1].strip()
                                # 地址
                                consignee_address = '-'
                            else:
                                consignee = consignee3[0].strip()
                                # 电话
                                consignee_mobile = consignee3[1].strip()
                                # 地址
                                if consignee3[2] is '':
                                    consignee_address = consignee3[3].strip()
                                else:
                                    consignee_address = consignee3[2].strip()
                            item['token'] = token
                            item['order_id'] = response.meta['order_id']
                            item['order_createtime'] = response.meta['order_createtime']
                            item['order_rmb'] = response.meta['order_rmb']
                            item['order_status'] = response.meta['order_status']
                            item['deliver_type'] = deliver_type
                            item['deliver_company'] = deliver_company
                            item['deliver_no'] = deliver_no
                            item['consignee'] = consignee
                            item['consignee_mobile'] = consignee_mobile
                            item['consignee_address'] = consignee_address
                            yield item
                        else:
                            item['token'] = token
                            item['order_id'] = response.meta['order_id']
                            item['order_createtime'] = response.meta['order_createtime']
                            item['order_rmb'] = response.meta['order_rmb']
                            item['order_status'] = response.meta['order_status']
                            item['deliver_type'] = '-'
                            item['deliver_company'] = '-'
                            item['deliver_no'] = '-'
                            item['consignee'] = '-'
                            item['consignee_mobile'] = '-'
                            item['consignee_address'] = '-'
                            yield item
                    else:
                        item['token'] = token
                        item['order_id'] = response.meta['order_id']
                        item['order_createtime'] = response.meta['order_createtime']
                        item['order_rmb'] = response.meta['order_rmb']
                        item['order_status'] = response.meta['order_status']
                        item['deliver_type'] = '-'
                        item['deliver_company'] = '-'
                        item['deliver_no'] = '-'
                        item['consignee'] = '-'
                        item['consignee_mobile'] = '-'
                        item['consignee_address'] = '-'
                        yield item
                else:
                    item['token'] = token
                    item['order_id'] = response.meta['order_id']
                    item['order_createtime'] = response.meta['order_createtime']
                    item['order_rmb'] = response.meta['order_rmb']
                    item['order_status'] = response.meta['order_status']
                    item['deliver_type'] = '-'
                    item['deliver_company'] = '-'
                    item['deliver_no'] = '-'
                    item['consignee'] = '-'
                    item['consignee_mobile'] = '-'
                    item['consignee_address'] = '-'
                    yield item
                    self.logger.info('新版本解析用户{}天猫可能出错：订单状态：{}订单id：{}'.format(token, response.meta['order_status'],
                                                                             response.meta['order_id']))
            # 如果不是新版本，以下为旧版本xpath解析
            else:
                item['token'] = token
                item['order_id'] = response.meta['order_id']
                item['order_createtime'] = response.meta['order_createtime']
                item['order_rmb'] = response.meta['order_rmb']
                item['order_status'] = response.meta['order_status']
                item['deliver_type'] = '-'
                item['deliver_company'] = '-'
                item['deliver_no'] = '-'
                item['consignee'] = '-'
                item['consignee_mobile'] = '-'
                item['consignee_address'] = '-'
                yield item
                self.logger.error('新版本正则匹配不到，出现旧版本天猫物流信息解析,用户：{}订单id：{}'.format(token, response.meta['order_id']))
        except Exception as e:
            item['token'] = token
            item['order_id'] = response.meta['order_id']
            item['order_createtime'] = response.meta['order_createtime']
            item['order_rmb'] = response.meta['order_rmb']
            item['order_status'] = response.meta['order_status']
            item['deliver_type'] = '-'
            item['deliver_company'] = '-'
            item['deliver_no'] = '-'
            item['consignee'] = '-'
            item['consignee_mobile'] = '-'
            item['consignee_address'] = '-'
            yield item
            self.logger.error('解析用户{}订单号为：{}详情订单获取天猫物流信息出错:{}'.format(token, response.meta['order_id'], e))
            # 对抛出的一场进行处理
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fname = "".join(os.path.split(exc_traceback.tb_frame.f_code.co_filename))  # 异常抛出的文件
            lineno = exc_traceback.tb_lineno  # 异常出现在哪一行
            uid = uid  # log表中的uid
            formatted_lines = traceback.format_exc().splitlines()  # 获取整个异常中
            # 异常描述
            message = "解析详情订单获取天猫物流信息出错订单号为：{}, 用户:{}-->异常：{}-->异常最后一行：{}".format(
                response.meta['order_id'], token, e, formatted_lines[-1])
            # 将抛出的异常存入数据库中
            self.insert_log(token=token, uid=uid, file_name=fname, line_no=lineno, message=message)

    # 静态方法2 单独解析获取详情页url
    def get_detail_url(self, list_object, token, uid):
        try:
            detail_url = 'nourl'
            for index, data in enumerate(list_object):
                if '订单详情' in data['text']:
                    detail_url = 'https:' + data['url']
                    break
            return detail_url
        except Exception as e:
            self.logger.error('静态方法单独解析用户{}获取详情页url出错:{}'.format(token, e))
            # 对抛出的一场进行处理
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fname = "".join(os.path.split(exc_traceback.tb_frame.f_code.co_filename))  # 异常抛出的文件
            lineno = exc_traceback.tb_lineno  # 异常出现在哪一行
            uid = uid  # log表中的uid
            formatted_lines = traceback.format_exc().splitlines()  # 获取整个异常中
            # 异常描述
            message = "静态方法单独解析获取详情页url出错,用户:{}-->异常：{}-->异常最后一行：{}".format(token, e, formatted_lines[-1])
            # 将抛出的异常存入数据库中
            self.insert_log(token=token, uid=uid, file_name=fname, line_no=lineno, message=message)

    # 静态方法3 从cookie中提取token值
    def get_token_from_cookie(self, cookies, token, uid):
        try:
            data_dic = {}
            for cookie in cookies:
                cookie = cookie.decode('utf-8')
                datas = cookie.split(';')
                for data in datas:
                    key, value = data.split('=')[0], data.split('=')[1]
                    data_dic[key] = value
            return data_dic['_m_h5_tk'][:-14]
        except Exception as e:
            self.logger.error('用户{}静态方法get_token_from_cookie中的sign构造的set cookie解析出错:{}'.format(token, e))
            # 对抛出的一场进行处理
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fname = "".join(os.path.split(exc_traceback.tb_frame.f_code.co_filename))  # 异常抛出的文件
            lineno = exc_traceback.tb_lineno  # 异常出现在哪一行
            uid = uid  # log表中的uid
            formatted_lines = traceback.format_exc().splitlines()  # 获取整个异常中
            # 异常描述
            message = "静态方法get_token_from_cookie中的sign构造的set cookie解析出错，用户:{}-->异常：{}-->异常最后一行：{}".format(
                token, e, formatted_lines[-1])
            # 将抛出的异常存入数据库中
            self.insert_log(token=token, uid=uid, file_name=fname, line_no=lineno, message=message)

    # 静态方法4 生成sign签名
    def get_sign(self, sign_time, token1, token, uid):
        try:
            data = token1 + '&' + str(sign_time) + '&12574478&{}'
            hl = hashlib.md5()
            hl.update(data.encode(encoding='utf8'))
            sign = hl.hexdigest()
            return sign
        except Exception as e:
            self.logger.error('用户{}address_url中的sign构造MD5失败：{}'.format(token, e))
            # 对抛出的一场进行处理
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fname = "".join(os.path.split(exc_traceback.tb_frame.f_code.co_filename))  # 异常抛出的文件
            lineno = exc_traceback.tb_lineno  # 异常出现在哪一行
            uid = uid  # log表中的uid
            formatted_lines = traceback.format_exc().splitlines()  # 获取整个异常中
            # 异常描述
            message = "address_url中的sign构造MD5失败,用户:{}-->异常：{}-->异常最后一行：{}".format(token, e, formatted_lines[-1])
            # 将抛出的异常存入数据库中
            self.insert_log(token=token, uid=uid, file_name=fname, line_no=lineno, message=message)
