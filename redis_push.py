#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import redis


def main():
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    # 提取1到100页的url
    r.lpush("taobao", 'jianjian')


if __name__ == '__main__':
    main()
