#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from selenium import webdriver
import time
import copy
import re
import requests
import datetime


def get_cookie():
    # 构造所需的cookie信息俩个：cookies_success和cookies
    # driver = webdriver.PhantomJS()
    # driver.implicitly_wait(120)
    # driver.get('https://login.taobao.com/member/login.jhtml')
    # time.sleep(2)
    # if 'login-box no-longlogin module-quick' in driver.page_source:
    #     umid_token = re.findall(re.compile(r';umid_token=(.*?);'), driver.page_source)
    # else:
    #     driver.find_element_by_id('J_Static2Quick').click()
    #     # 必须为2秒！！
    #     time.sleep(2)
    #     umid_token = re.findall(re.compile(r'&umid_token=(.*?)&'), driver.page_source)
    # if len(umid_token) > 0:
    #     print(umid_token[0].replace('&amp', ''))
    # 构造所需的cookie信息俩个：cookies_success和cookies
    driver = webdriver.PhantomJS()
    driver.implicitly_wait(120)
    driver.get('https://login.taobao.com/member/login.jhtml')
    cookies_success = dict()
    for cook in driver.get_cookies():
        cookies_success[cook["name"]] = cook["value"]  # cookies_success为最后一步登陆所用的cookie
    cookies = copy.deepcopy(cookies_success)  # cookies为后面登陆所用的通用cookie
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',

    }
    response = requests.get(url='https://login.taobao.com/member/login.jhtml', headers=headers)
    print(response.cookies)
    try:
        print('cookies_success里面的数据为{}'.format(cookies_success))
        cookies.pop('_uab_collina')
        cookies.pop('cookieCheck')
        cookies.pop('um')
        cookies.pop('_umdata')
        cookies.pop('isg')
    except:
        pass
    print('cookies里面的数据为{}'.format(cookies))
    # if 'login-box no-longlogin module-quick' in driver.page_source:
    #     driver.find_element_by_id('J_Quick2Static').click()
    #     url1 = re.findall(re.compile(r'<script src="(.*?)" async=""></script>'), driver.page_source)
    # else:
    #     # 必须为2秒！！
    #     time.sleep(2)
    #     url1 = re.findall(re.compile(r'<script src="(.*?)" async=""></script>'), driver.page_source)
    # if len(url1) > 0:
    #     url = url1[-3].replace(';', '&')
    #     umid_token = re.findall(re.compile(r'&umid_token=(.*?)&'), url)
    #     if umid_token:
    #         umid_token = umid_token[0]
    #         print(umid_token)
    #     else:
    #         self.logger.error("获取umid_token重要数据出错!")
    # else:
    #     url = ''
    #     umid_token = ""
    #     self.logger.error("获取产生二维码地址出错!")


if __name__ == '__main__':
    get_cookie()
    print('C{}{}'.format(int(time.time() * 100000000000000), int(time.time() * 1000000)))
    print(int(time.time() * 1000000))
# def lian_tong():
#     url = 'http://uac.10010.com/oauth2/genqr?timestamp={}'.format(int(time.time() * 1000))
#     headers = {
#         'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
#     }
#     headers2 = {
#
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
#     }
#     response = requests.get(url=url, headers=headers)
#     unisecid = response.cookies.get('unisecid')
#     print(unisecid)
#     with open('liantong.png', 'wb') as f:
#         f.write(response.content)
#         print('请扫描验证码')
#     print(response.status_code)
#     url_check = 'http://uac.10010.com/qrcode/qrcode_hbt?secsnid={}&_={}'
#     print(url_check)
#
#     for i in range(200):
#         response2 = requests.get(url=url_check.format(unisecid, int(time.time() * 1000)), headers=headers2)
#         try:
#             code = "".join(re.findall(re.compile(r'resultcode":"(\d+)"'), response2.text))
#             print(response2.text)
#             if '00' in code:
#                 time.sleep(2)
#                 print(code)
#
#             elif '10' in code:
#                 time.sleep(2)
#                 print(code + "等待用户确认.......")
#             elif '11' in code:
#                 pass
#             else:
#                 print("check二维码出现错误或者失效")
#                 break
#
#         except Exception as e:
#             print("出错{}".format(e))

# def yi_dong():
#     url2 = 'http://login.10086.cn/genqr.htm'
#     header = {
#         'Accept': '*/*',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'zh-CN,zh;q=0.9',
#         'Connection': 'keep-alive',
#         'Host': 'shop.10086.cn',
#         'Referer': 'https://login.10086.cn/login.html?channelID=12034&backUrl=http%3A%2F%2Fwww.10086.cn%2Findex%2Fsx%2Findex_351_354.html',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
#     }
#     session = requests.session()
#     header.update({'Host': 'login.10086.cn'})
#     # 获取二维码图片
#     res3 = session.get(url=url2, headers=header)
#     cookies = res3.headers.get("Set-Cookie")
#     lgToken = re.findall(re.compile(r"lgToken=(.*?);"), cookies)
#     if lgToken:
#         lgToken = lgToken[0]
#
#     # 保存图片
#     with open('yidong.png', 'wb') as f:
#         f.write(res3.content)
#         print('请扫描验证码')
#
#     # 二维码轮询
#     url_check = 'https://login.10086.cn/chkqr.htm'
#     for i in range(33):
#         response1 = session.post(url=url_check, headers=header,
#                                  data={"lgToken": lgToken,
#                                        'targetChannelID': '12034',
#                                        'backUrl': 'http%3A%2F%2Fwww.10086.cn%2Findex%2Fsx%2Findex_351_354.html'})
#
#         code = re.findall(re.compile(r'"resultCode":"(\d+)",'), response1.text)
#         try:
#             if '0000' in code:
#                 print(response1.text)
#                 print('二维码轮询的cookie{}'.format(session.cookies))
#                 artifact1 = re.findall(re.compile(r'"artifact":"(.*?)"'), response1.text)
#                 if artifact1:
#                     artifact = artifact1[0]
#                     success_url = 'http://www1.10086.cn/web-Center/authCenter/receiveArtifact.do?backUrl=http%3A%2F%2Fwww.10086.cn%2Findex%2Fsx%2Findex_351_354.html&artifact={}'.format(
#                         artifact)
#                     header.update({'Host': 'www1.10086.cn'})
#                     # 验证1
#                     redirect_res0 = session.get(url=success_url, headers=header, allow_redirects=False)
#                     redirect_url = redirect_res0.headers['Location']
#                     header.update({'Referer': ''})
#                     redirect_res1 = session.get(url=redirect_url, headers=header, )
#                     # redirect_res1.encoding = 'utf-8'
#                     # print(redirect_res1.text)
#                     # print(session.cookies)
#                     # 验证2
#                     header.update({'Host': 'login.10086.cn'})
#                     header.update({'Referer': 'https://shop.10086.cn/i/?f=home'})
#
#                     ur3 = 'https://login.10086.cn/SSOCheck.action?channelID=12034&backUrl=https://shop.10086.cn/i/?f=home'
#                     auth_response1 = session.get(url=ur3, headers=header, verify=False, allow_redirects=False)
#                     print(auth_response1.text)
#                     artifact2 = re.findall(re.compile(r'artifact=(.*?)&'), auth_response1.text)
#                     if artifact2:
#                         header.update({'Host': 'shop.10086.cn'})
#                         redirect_url2 = 'https://shop.10086.cn/i/v1/auth/getArtifact?artifact={}&backUrl=https%3A%2F%2Fshop.10086.cn%2Fi%2F%3Ff%3Dhome'.format(
#                             artifact2[0])
#                         redirect_res2 = session.get(url=redirect_url2, headers=header, verify=False)
#
#                         # 成功验证？？
#                         Referer = redirect_res2.url
#                         header.update({'Referer': Referer})
#                         header.update({'Host': 'shop.10086.cn'})
#                         print(header)
#                         ur4 = 'https://shop.10086.cn/i/v1/auth/loginfo?_={}'.format(int(time.time() * 1000))
#                         successauth_response1 = session.get(url=ur4, headers=header, verify=False)
#                         print("成功验证???{}".format(successauth_response1.text))
#
#                         # 获取个人信息
#
#                         break
#             elif '8020' in code:
#                 print(response1.text + "二维码失效！！！")
#                 break
#             else:
#                 time.sleep(2)
#                 print('请扫码并确认！！')
#         except Exception as e:
#             print("出错{}".format(e))
#
#
# if __name__ == '__main__':
#     yi_dong()
# print(str(datetime.datetime.now().date()).replace('-', ''))
# print(time.strftime('%Y%m'))
# print(int(time.strftime('%Y%m'))-2)
# time1 = int(time.strftime('%Y%m'))
# tem = copy.deepcopy(time1)
# for i in range(5):
#     tem = tem - 1
#     print(tem)
# zhangdan_url2 = 'https://shop.10086.cn/i/v1/fee/detailbillinfojsonp/{}?\
# curCuror=1&step=100&qryMonth={}&billType=01&_={}'
# print(zhangdan_url2.format(123, int(time.strftime('%Y%m')), int(time.time() * 1000)))
# detail_time = 201810
# for v in range(6):
#     zhangdan_url2 = 'https://shop.10086.cn/i/v1/fee/detailbillinfojsonp/{}?curCuror=1&step=1000&qryMonth={}&billType={}&_={}'
#     url = zhangdan_url2.format(
#         1, 1, detail_time, int(time.time() * 1000)),
#     detail_time -= 1
#     print(url)

# a = """null({"data":null,"retCode":"520001","retMsg":"临时身份凭证不存在。","sOperTime":null})"""
# print('临时身份凭证不存在' in a)
# print(int(time.strftime('%Y%m%d')))
# print(int(time.strftime('%Y%m%d')))
# t=(datetime.datetime.now() + datetime.timedelta(days=-365)).date()
# print(t.strftime('%Y%m%d'))
