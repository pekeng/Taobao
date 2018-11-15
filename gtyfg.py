#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import base64
password = '021794'
print(base64.b64encode(bytes(password.encode('utf8'))))