import time
import requests
import re
import os


def parse_js():
    url0 = 'https://v4.passport.sohu.com/i/cookie/common'
    time_l1 = int(time.time() * 1000)
    time_l2 = int(time.time() * 1000)
    url1 = 'https://v4.passport.sohu.com/i/jf/code?callback=passport403_cb{}&type=0&_={}'.format(time_l1, time_l2)
    url2 = 'https://v4.passport.sohu.com/i/login/101305'
    login_headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://mail.sohu.com/fe/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    session = requests.session()
    cookies = {
        'a': '123',
        't': ''.format(int(time.time() * 1000)),
        'reqtype': 'pc',
    }
    print(url0)
    res0 = session.get(url=url0, headers=login_headers, cookies=cookies)
    print(res0.text)
    login_headers.update({'Host': 'v4.passport.sohu.com'})
    res1 = session.get(url=url1, headers=login_headers, cookies=cookies)
    aa = re.findall(re.compile(r'\("(.*?)"\)'), res1.text)[0].strip()
    with open('hhhh.js', 'w', encoding='utf8') as e:
        e.write("console.log(eval('")
    with open('hhhh.js', 'a', encoding='utf8') as e:
        e.write(aa)
    with open('hhhh.js', 'a', encoding='utf8') as e:
        e.write("'));phantom.exit();")
    r = os.popen("PhantomJS hhhh.js")
    r = r.read()
    jv = re.findall(re.compile(r"jv=(.*?);"), r)
    print(jv)
    form_data = {
        'userid': 'wwinsongsong@sohu.com',
        'password': 'ec10af4b5533157fa30ac31ffc7ef441',
        'appid': '101305',
    }
    cookies.update({'jv': jv[0]})
    print(cookies)
    res2 = session.post(url=url2, headers=login_headers, cookies=cookies, data=form_data)
    print(res2.text)
    print(session.cookies)


if __name__ == '__main__':
    parse_js()
