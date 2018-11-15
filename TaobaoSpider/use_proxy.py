import requests
import json
import redis
from .settings import REDIS_HOST, REDIS_PORT, REDIS_DB_PROXY, REDIS_DB_KEY, USE_PROXY


class ProxyPoolInfo(object):
    def __init__(self):
        pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_PROXY, )
        self.redis_conn = redis.Redis(connection_pool=pool,)

    # 获取代理IP
    def create_proxy(self):
        while True:
            if USE_PROXY:
                # 判断代理池中是否有可用IP
                redis_ip = self.redis_conn.scard(REDIS_DB_KEY)  # 获取代理池中代理的长度
                if redis_ip:
                    # 从代理池随机取IP并返回
                    proxy_ip_port = self.redis_conn.spop(REDIS_DB_KEY).decode('utf-8')  # 获取任意一个元素
                else:
                    proxy_url = "http://api.xdaili.cn/xdaili-api/greatRecharge/getGreatIp" \
                                "?spiderId=d882f2dedc1741e087d228c208060a36" \
                                "&orderno=YZ20181087213QEydHG" \
                                "&returnType=2" \
                                "&count=1"
                    proxy_resp = requests.get(proxy_url)
                    print("代理ip：{}".format(proxy_resp.text))
                    procy_text = json.loads(proxy_resp.text)
                    proxy_ip = procy_text["RESULT"][0]["ip"]
                    proxy_port = procy_text["RESULT"][0]["port"]
                    proxy_ip_port = proxy_ip + ":" + proxy_port
                    # 将取到的IP放入到Redis池
                    self.redis_conn.sadd(REDIS_DB_KEY, proxy_ip_port)  # 新获取到的代理放入代理池
            else:
                proxy_ip_port = ""
            return proxy_ip_port

    # 移除不可用代理IP
    def remove_proxy(self, proxy):
        self.redis_conn.srem(REDIS_DB_KEY, proxy)
