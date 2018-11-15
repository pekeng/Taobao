# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:TaobaoSpider
FileName = PyCharm
Version:1.0
CreateDay:2018/8/7 16:51
"""
import time
import execjs
import hashlib
import requests


def get_sign(data):
    # f = open("D:/WorkSpace/MyWorkSpace/jsdemo/js/des_rsa.js",'r',encoding='UTF-8')
    f = open("E:\work\TaobaoSpider\TaobaoSpider\sign.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    ex = execjs.compile(htmlstr)
    sign = ex.call('h', data)
    return sign


def get_sign2(_m_h5_tk, _m_h5_tk_enc):
    # 解析收货地址 31337be9d5d1dea0afc88f73e1421ad9
    # address_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.mbis.getdeliveraddrlist/1.0/?jsv=2.4.2&appKey=12574478\
    #    &t={}&sign={}&api=mtop.taobao.mbis.getDeliverAddrList&v=1.0\
    #    &ecode=1&needLogin=true&dataType=jsonp&type=jsonp&callback=mtopjsonp3&data=%7B%7D'
    sign_time = int(time.time() * 1000)
    token = _m_h5_tk[:-14]
    token = '8ece8f34a570386c376404da1311f26c'
    print("TOKEN:{}".format(token))
    data = token + '&' + str(sign_time) + '&12574478&{}'
    hl = hashlib.md5()
    hl.update(data.encode(encoding='utf8'))
    print('MD5加密后为 ：' + hl.hexdigest())
    sign = hl.hexdigest()
    headers = {
        "Host": "h5api.m.taobao.com",
        "Referer": "http://member1.taobao.com/member/fresh/deliver_address.htm?spm=a1z09.2.a210b.8.77552e8dw14JoY",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        # "Cookie": "t=cc5218c55a8dd743e0e7c894fa6b04b2; cookie2=1b4a1336bf637149b0523aff42d8295b; v=0; _tb_token_=ee73938b833ba; cna=I4r6ExoHJDkCAat4c98lH1PM; unb=860963132; sg=22a; _l_g_=Ug%3D%3D; skt=9f5f911c290e9d99; publishItemObj=Ng%3D%3D; cookie1=VFO7OYtPLa%2B4l8%2BNUD3wjHESjW9YNA9jQot%2FK1qV%2B%2BY%3D; csg=9fb69174; uc3=vt3=F8dBzrpLtZFhlMKsVrM%3D&id2=W89MXAb8ajng&nk2=rUf%2FBfweUxPktIw4ggg%3D&lg2=UIHiLt3xD8xYTw%3D%3D; existShop=MTUzNDMxMzgyMA%3D%3D; tracknick=%5Cu65E0%5Cu6CD5%5Cu6446%5Cu8131%5Cu4F602012; lgc=%5Cu65E0%5Cu6CD5%5Cu6446%5Cu8131%5Cu4F602012; _cc_=VFC%2FuZ9ajQ%3D%3D; dnk=%5Cu65E0%5Cu6CD5%5Cu6446%5Cu8131%5Cu4F602012; _nk_=%5Cu65E0%5Cu6CD5%5Cu6446%5Cu8131%5Cu4F602012; cookie17=W89MXAb8ajng; tg=0; thw=cn; mt=ci=99_1; uc1=cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&cookie21=VT5L2FSpczFp&cookie15=UIHiLt3xD8xYTw%3D%3D&existShop=false&pas=0&cookie14=UoTfL8nNDBNqQQ%3D%3D&tag=8&lng=zh_CN; isg=BEJCOLtvrW7tCbEhukqVkJRHk0hku0aut8HH1Ixbq7Vg3-NZdKDHPWgJiZsGj77F,_m_h5_tk={},_m_h5_tk_enc={}".format(
        #     _m_h5_tk, _m_h5_tk_enc),
        "cookie": "t=cc5218c55a8dd743e0e7c894fa6b04b2; cookie2=1b4a1336bf637149b0523aff42d8295b; v=0; _tb_token_=ee73938b833ba; cna=I4r6ExoHJDkCAat4c98lH1PM; unb=860963132; sg=22a; _l_g_=Ug%3D%3D; skt=9f5f911c290e9d99; publishItemObj=Ng%3D%3D; cookie1=VFO7OYtPLa%2B4l8%2BNUD3wjHESjW9YNA9jQot%2FK1qV%2B%2BY%3D; csg=9fb69174; uc3=vt3=F8dBzrpLtZFhlMKsVrM%3D&id2=W89MXAb8ajng&nk2=rUf%2FBfweUxPktIw4ggg%3D&lg2=UIHiLt3xD8xYTw%3D%3D; existShop=MTUzNDMxMzgyMA%3D%3D; tracknick=%5Cu65E0%5Cu6CD5%5Cu6446%5Cu8131%5Cu4F602012; lgc=%5Cu65E0%5Cu6CD5%5Cu6446%5Cu8131%5Cu4F602012; _cc_=VFC%2FuZ9ajQ%3D%3D; dnk=%5Cu65E0%5Cu6CD5%5Cu6446%5Cu8131%5Cu4F602012; _nk_=%5Cu65E0%5Cu6CD5%5Cu6446%5Cu8131%5Cu4F602012; cookie17=W89MXAb8ajng; tg=0; thw=cn; mt=ci=99_1; uc1=cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&cookie21=VT5L2FSpczFp&cookie15=UIHiLt3xD8xYTw%3D%3D&existShop=false&pas=0&cookie14=UoTfL8nNDBNqQQ%3D%3D&tag=8&lng=zh_CN; _m_h5_tk=8ece8f34a570386c376404da1311f26c_1534322868935; _m_h5_tk_enc=f9580ab896bda8b5efcf0218e6b2b546; isg=BKenjw6wsM0AvjRSb8W400mQNtuxhHuNmtYCB3kU3zZdaMcqgf7eXpNujijTgFOG"
    }
    url = "http://h5api.m.taobao.com/h5/mtop.taobao.mbis.getdeliveraddrlist/1.0/?jsv=2.4.2&appKey=12574478&t={}&sign={}&api=mtop.taobao.mbis.getDeliverAddrList&v=1.0&ecode=1&needLogin=true&dataType=jsonp&type=jsonp&callback=mtopjsonp3&data=%7B%7D"

    response = requests.get(url=url.format(sign_time, sign), headers=headers)
    print(response)
    print(response.text)


def get_token():
    session = requests.Session()
    headers = {
        "Host": "h5api.m.taobao.com",
        "Referer": "http://member1.taobao.com/member/fresh/deliver_address.htm?spm=a1z09.2.a210b.8.77552e8dw14JoY",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Cookie": "t=cc5218c55a8dd743e0e7c894fa6b04b2; cookie2=1b4a1336bf637149b0523aff42d8295b; v=0; _tb_token_=ee73938b833ba; cna=I4r6ExoHJDkCAat4c98lH1PM; unb=860963132; sg=22a; _l_g_=Ug%3D%3D; skt=9f5f911c290e9d99; publishItemObj=Ng%3D%3D; cookie1=VFO7OYtPLa%2B4l8%2BNUD3wjHESjW9YNA9jQot%2FK1qV%2B%2BY%3D; csg=9fb69174; uc3=vt3=F8dBzrpLtZFhlMKsVrM%3D&id2=W89MXAb8ajng&nk2=rUf%2FBfweUxPktIw4ggg%3D&lg2=UIHiLt3xD8xYTw%3D%3D; existShop=MTUzNDMxMzgyMA%3D%3D; tracknick=%5Cu65E0%5Cu6CD5%5Cu6446%5Cu8131%5Cu4F602012; lgc=%5Cu65E0%5Cu6CD5%5Cu6446%5Cu8131%5Cu4F602012; _cc_=VFC%2FuZ9ajQ%3D%3D; dnk=%5Cu65E0%5Cu6CD5%5Cu6446%5Cu8131%5Cu4F602012; _nk_=%5Cu65E0%5Cu6CD5%5Cu6446%5Cu8131%5Cu4F602012; cookie17=W89MXAb8ajng; tg=0; thw=cn; mt=ci=99_1; uc1=cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&cookie21=VT5L2FSpczFp&cookie15=UIHiLt3xD8xYTw%3D%3D&existShop=false&pas=0&cookie14=UoTfL8nNDBNqQQ%3D%3D&tag=8&lng=zh_CN; isg=BEJCOLtvrW7tCbEhukqVkJRHk0hku0aut8HH1Ixbq7Vg3-NZdKDHPWgJiZsGj77F",
    }
    url = 'http://h5api.m.taobao.com/h5/mtop.cainiao.address.ua.global.area.list/1.0/?jsv=2.4.2&appKey=12574478&t=1534313870148&sign=a677552e4506da78c5886fd7fa60428c&api=mtop.cainiao.address.ua.global.area.list&v=1.0&dataType=jsonp&type=jsonp&callback=mtopjsonp1&data=%7B%22sn%22%3A%22suibianchuan%22%7D'
    response = session.get(url, headers=headers, verify=True)
    print(response)
    print(response.text)
    print(session.cookies.items())
    return session.cookies.get('_m_h5_tk'), session.cookies.get('_m_h5_tk_enc')


def parse_cookie():
    cookies = [b'_m_h5_tk=b410201bb15a37b929909201000bebb9_1534325737878;Path=/;Domain=taobao.com;Max-Age=604800',
               b'_m_h5_tk_enc=1efa342115d94d10562a772a35f8ca34;Path=/;Domain=taobao.com;Max-Age=604800']
    data_dic = {}
    for cookie in cookies:
        cookie = cookie.decode('utf-8')
        datas = cookie.split(';')
        for data in datas:
            key, value = data.split('=')[0], data.split('=')[1]
            print(key, value)
            data_dic[key] = value
    print(data_dic)
    return data_dic['_m_h5_tk']
if __name__ == '__main__':
    # _m_h5_tk, _m_h5_tk_enc = get_token()
    # print(_m_h5_tk, _m_h5_tk_enc)
    # get_sign2(_m_h5_tk, _m_h5_tk_enc)
    _m_h5_tk = parse_cookie()
    print(_m_h5_tk)
    pass
