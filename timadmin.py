"""
  Copyright (c) , donnie <donnie4w@gmail.com>
  All rights reserved.
  https://github.com/donnie4w/tim

  Use of this source code is governed by a BSD-style
  license that can be found in the LICENSE file.

  it is the test interface for tim administrator
  这是tim管理员的后台操作接口python示例
"""

import http.client
import json
import ssl
import pytest
import base64


def JEncode(data) -> bytes:
    return json.dumps(data).encode('ISO-8859-1')


def JDecode(loadstr) -> str:
    return json.loads(loadstr)


def httpPost(isSSL, data, host, port, uri, username, pwd) -> bytes:
    if isSSL:
        conn = http.client.HTTPSConnection(host, port=port, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))
    else:
        conn = http.client.HTTPConnection(host, port=port)
    # username and password of the management platform
    # 管理后台的用户名密码
    # 'content-type': 'application/json'      : Send data in json format .e.g. {'name':'test','pwd':'123456'}
    # 'content-type': 'x-www-form-urlencoded' : Send data in form format .e.g. name=test&pwd=123456
    headers = {'content-type': 'application/json', 'username': username, 'password': pwd}
    conn.request('POST', uri, data, headers=headers)
    response = conn.getresponse()
    r = response.read()
    return r


# get token for login
# 获取登录的token
def test_timToken():
    data = {'name': 'jerry', 'domain': 'tlnet.top'}
    bs = httpPost(False, JEncode(data), "192.168.2.11", 6144, "/timToken", 'admin', '123')
    print(JDecode(bs))


# send the system message to user  发送系统信息给用户
# format of data  数据格式
#
#   'nodes': {'nodelist': ['d4RCZD2bxiW']}
#   message: {           # message 是 TimMessage对象的json序列化格式
#    'dataString':'11111',
#    'udtype':1,
#    'udshow':'2222',
#    'extend': {'aaa':'111'}
#   }
def test_timMessage():
    data = {'nodes': {'nodelist': ['d4RCZD2bxiW']},
            'message': {
                'dataString': "Hello, World!",
                'udtype': 1,
                'extend': {'aaa': '222'}
            }
            }
    bs = httpPost(False, JEncode(data), "192.168.2.11", 8001, "/timMessage", 'admin', '123')
    print(bs)


# register
# 从后台注册
def test_timRegister():
    data = {'username': 'test1', 'password': '123', 'domain': 'tlnet.top'}
    bs = httpPost(False, JEncode(data), "192.168.2.11", 8001, "/timRegister", 'admin', '123')
    print(bs)  # server return {"ok":true,"timType":0,"n":"d4RCZD2bxiW"}


# block list
# 拉黑用户列表
def test_timBlockList():
    bs = httpPost(False, None, "192.168.2.11", 8001, "/timBlockList", 'admin', '123')
    print(bs)  # print {"d4RCZD2bxiW":1699539665}


# block the account of user
# 拉黑账号
def test_timBlockUser():
    data = {'account': 'd4RCZD2bxiW', 'time': 30}
    bs = httpPost(False, JEncode(data), "192.168.2.11", 8001, "/timBlockUser", 'admin', '123')
    print(bs.decode('utf-8'))  # {"ok":true,"timType":0,"n":"d4RCZD2bxiW"}


# get online account
# 获取在线用户账号
def test_timOnline():
    bs = httpPost(False, None, "192.168.2.11", 8001, "/timOnline", 'admin', '123')
    li = JDecode(bs)
    print("length>>", len(li))
    for i in li:
        print(i)  # print: {'node': 'd4RCZD2bxiW', 'domain': 'tlnet.top', 'resource': 'android', 'termtyp': 1}


# reset password
# 重置用户密码
def test_timResetAuth():
    data = {'loginname': 'tim1', 'pwd': '123', 'domain': 'tlnet.top'}
    bs = httpPost(False, JEncode(data), "192.168.2.11", 8001, "/timResetAuth", 'admin', '123')
    print(bs.decode('utf-8'))  # server return {"ok":true,}


def test_timModifyUserInfo():
    data = {"node": "SHqmrYF8jJu",
            "userbean": {
                "name": "tim3",
                "cover": "/img/28.png"
            }
            }
    bs = httpPost(False, JEncode(data), "192.168.2.11", 8001, "/timModifyUserInfo", 'admin', '123')
    li = JDecode(bs)
    print("length>>", len(li))
    print(bs.decode('utf-8'))  # server return {"ok":true}


def test_timModifyUserInfo():
    data = {"unode": "UHuS8PoK2Mi",
            "gnode": "WF5dEbaH14d",
            "roombean": {
                "cover": "/img/28.png"
            }
            }
    bs = httpPost(False, JEncode(data), "192.168.2.11", 8001, "/timModifyRoomInfo", 'admin', '123')
    li = JDecode(bs)
    print("length>>", len(li))
    print(bs.decode('utf-8'))  # server return {"ok":true,"timType":0}
