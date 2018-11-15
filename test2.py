#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import requests
import time
import base64
import copy
import random
import datetime


class YiDong(object):
    def __init__(self):
        self.session = requests.session()
        self.detail_dict = {
            '01': '套餐及固定费',
            '02': '通话详单',
            '03': '短信和彩信详单',
            '04': '上网详单',
            '05': '增值业务详单',
            '06': '代收业务详单',
            '07': '其他',
        }

    def login(self):
        url2 = 'https://login.10086.cn/genqr.htm'
        header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'shop.10086.cn',
            'Referer': 'Referer: https://login.10086.cn/login.html?\
            channelID=12003&backUrl=https://shop.10086.cn/i/?f=home',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome\
            /65.0.3325.181 Safari/537.36',
        }
        header.update({'Host': 'login.10086.cn'})
        # 获取二维码图片
        res3 = self.session.get(url=url2, verify=False, headers=header)
        cookies = res3.headers.get("Set-Cookie")
        lgtoken = re.findall(re.compile(r"lgToken=(.*?);"), cookies)
        if lgtoken:
            lgtoken = lgtoken[0]

        # 保存图片
        with open('yidong.png', 'wb') as f:
            f.write(res3.content)
            print('请扫描验证码')

        # 二维码轮询
        url_check = 'https://login.10086.cn/chkqr.htm'
        for i in range(33):
            check_response = self.session.post(url=url_check, verify=False, headers=header,
                                               data={"lgToken": lgtoken, 'targetChannelID': '12003',
                                                     'backUrl': 'https://shop.10086.cn/i/?f=home'})

            code = re.findall(re.compile(r'"resultCode":"(\d+)",'), check_response.text)
            try:
                if '0000' in code:
                    print(check_response.text)
                    print('二维码轮询的cookie{}'.format(self.session.cookies))
                    artifact1 = re.findall(re.compile(r'"artifact":"(.*?)"'), check_response.text)
                    if artifact1:
                        artifact = artifact1[0]
                        success_url = 'https://shop.10086.cn/i/v1/auth/getArtifact?backUrl=https://shop.10086.cn/i/?f=home&artifact={}'.format(
                            artifact)
                        header.update({'Host': 'shop.10086.cn'})
                        # 验证1
                        redirect_res0 = self.session.get(url=success_url, headers=header, verify=False,
                                                         allow_redirects=False)
                        redirect_url = redirect_res0.headers['Location']
                        redirect_res1 = self.session.get(url=redirect_url, headers=header, verify=False)

                        # 获取个人信息telephone
                        telephone = self.obtain_telephone(redirect_res1=redirect_res1, header=header)
                        if not telephone:
                            break

                        # 验证查询功能正常不？
                        acoount_url = 'https://shop.10086.cn/i/v1/res/funcavl?_={}'.format(
                            int(time.time() * 1000))
                        acoount_res = self.session.get(url=acoount_url, headers=header, verify=False)
                        if '成功' in acoount_res.text:
                            # 第1次账单的身份认证
                            if '认证成功' in self.auth_user(telephone=telephone, header=header):
                                # 进行解析
                                self.parse_detail(telephone=telephone, header=header)
                            else:
                                # 第2次账单的身份认证
                                time.sleep(60)
                                auth_second = self.auth_user(telephone=telephone, header=header)
                                if '认证成功' in auth_second:
                                    # 进行解析
                                    self.parse_detail(telephone=telephone, header=header)


                        else:
                            print('查询功能不正常')
                            break
                elif '8020' in code:
                    print(check_response.text + "二维码失效！！！")
                    break
                else:
                    time.sleep(2)
                    print('请扫码并确认！！')
            except Exception as e:
                print("出错{}".format(e))

    def auth_image(self, telephone, header):
        # 保存图片，输入图片验证码
        image_url = 'https://shop.10086.cn/i/authImg'
        image_res = self.session.get(url=image_url, headers=header, verify=False)
        with open('yanzheng.png', 'wb') as f:
            f.write(image_res.content)
        yanzheng = input("请输入验证码")

        # 图片验证码的检测
        preckeck_url = 'https://shop.10086.cn/i/v1/res/precheck/{}?captchaVal={}&_={}' \
            .format(telephone, yanzheng, int(time.time() * 1000))
        preckeck_res = self.session.get(url=preckeck_url, headers=header, verify=False)
        print(preckeck_res.text)
        if '输入正确，校验成功' in preckeck_res.text:
            print('图片验证码输入正确!!')
            return yanzheng
        else:
            print('校验失败，请重新输入图片验证码!!')
            self.auth_image(telephone=telephone, header=header)

    def send_message(self, telephone, header):
        duanxin_url = 'https://shop.10086.cn/i/v1/fee/detbillrandomcodejsonp/{}?_={}'
        duanxin_res = self.session.get(url=duanxin_url.format(
            telephone, int(time.time() * 1000)), headers=header, verify=False)
        # 发送短信正常？
        if 'success' in duanxin_res.text:
            print('发送成功！')
            duanxin = input("请输入短信验证码")
            return duanxin
        if '次数过多' in duanxin_res.text:
            print('单位时间内下发短信次数过多，请稍后再使用！')
            time.sleep(60)
            self.send_message(telephone=telephone, header=header)
        else:
            print('发送短信失败,正在重新发送！')
            time.sleep(60)
            self.send_message(telephone=telephone, header=header)

    def obtain_telephone(self, redirect_res1, header):
        # 获取个人信息及return telephone
        referer = redirect_res1.url
        header.update({'Referer': referer})
        ur4 = 'https://shop.10086.cn/i/v1/auth/loginfo?_={}'.format(int(time.time() * 1000))
        successauth_response1 = self.session.get(url=ur4, headers=header, verify=False)
        print("成功验证???{}".format(successauth_response1.text))
        if 'loginValue' in successauth_response1.text:
            telephone = re.findall(re.compile(r'"loginValue":"(\d+)",'), successauth_response1.text)
            if telephone:
                telephone = telephone[0]
                print('這是用户手机号{}'.format(telephone))
                if_url = 'https://shop.10086.cn/i/v1/cust/mergecust/{}?_={}'.format(
                    telephone, int(time.time() * 1000))
                inf0_res = self.session.get(url=if_url, headers=header, verify=False)
                print('這是用户信息{}'.format(inf0_res.text))
                return telephone
            else:
                print('手机号获取失败！2')
                telephone = ''
                return telephone
        else:
            print('手机号获取失败！1')
            telephone = ''
            return telephone

    def auth_user(self, telephone, header):
        # 输入服务密码
        password = input("请输入服务密码:")

        # 输入图片验证码
        yanzheng = self.auth_image(telephone=telephone, header=header)

        # 输入短信验证码
        duanxin = self.send_message(telephone=telephone, header=header)

        # 对服务密码和短信验证码base64加密
        pwdtempsercode = base64.b64encode(bytes(password.encode('utf8')))
        pwdtemprandcode = base64.b64encode(bytes(duanxin.encode('utf8')))
        # 账单的身份认证
        zhangdan_url = 'https://shop.10086.cn/i/v1/fee/detailbilltempidentjsonp/{}?pwdTempSerCode={}&pwdTempRandCode={}&captchaVal={}&_={}'
        zhangdan_res = self.session.get(url=zhangdan_url.format(
            telephone, pwdtempsercode.decode('utf-8'), pwdtemprandcode.decode('utf-8'),
            yanzheng, int(time.time() * 1000)), headers=header, verify=False)
        print(zhangdan_res.text)
        if '认证成功' in zhangdan_res.text:
            print('认证成功！')
            return '认证成功！'
        else:
            print('认证失败！')
            return '认证失败！'

    def parse_detail(self, telephone, header):

        # param bill_type: 01表示套餐及固定费，02表示通话详单,03短信/彩信详单,04上网详情，05表示增值业务详单，06表示代收业务详单，07表示其他

        # 进行解析
        for x in range(1, 8):
            bill_type = '0' + str(x)
            time.sleep(random.randint(2, 3))
            tem1 = int(time.strftime('%Y%m'))
            detail_time = copy.deepcopy(tem1)
            # 循环遍历年月
            for v in range(6):
                zhangdan_url2 = 'https://shop.10086.cn/i/v1/fee/detailbillinfojsonp/{}?curCuror=1&step=1000&qryMonth={}&billType={}&_={}'
                zhangdan_res2 = self.session.get(url=zhangdan_url2.format(
                    telephone, detail_time, bill_type, int(time.time() * 1000)),
                    headers=header, verify=False)
                time.sleep(random.randint(2, 3))
                print('用户的{}月{}信息{}'.format(
                    detail_time, self.detail_dict.get(bill_type), zhangdan_res2.text))
                un_date = (datetime.datetime.now() + datetime.timedelta(days=-365)).date()
                start_date = un_date.strftime('%Y%m%d')
                end_date = datetime.datetime.now().strftime('%Y%m%d')
                detail_time -= 1
                # 访问过于频繁出现的账单身份认证
                if '临时身份凭证不存在' in zhangdan_res2.text:
                    if '认证成功' in self.auth_user(telephone=telephone, header=header):
                        zhangdan_res2 = self.session.get(url=zhangdan_url2.format(
                            telephone, detail_time, bill_type, int(time.time() * 1000)),
                            headers=header, verify=False)
                        if '临时身份凭证不存在' in zhangdan_res2.text:
                            print(zhangdan_res2.text)
                            print('爬虫失败！！！！！！')
                            break
                    else:
                        break
                # 用户缴费记录
                if x == 4:
                    pay_record = self.session.get(
                        url='https://shop.10086.cn/i/v1/cust/his/15934117585?startTime={}&endTime={}&_={}'.format(
                            start_date, end_date, int(time.time() * 1000)
                        ))
                    print('用户缴费记录{}'.format(pay_record.text))


if __name__ == '__main__':
    yi_dong = YiDong()
    yi_dong.login()
