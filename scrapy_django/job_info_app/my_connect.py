#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: wf
@contact: wf17719390964@163.com
@software: pycharm
@file: my_connect.py
@time: 2018/11/28 10:20
@desc:
'''
import json

import happybase
import redis

class MyConnect:
    def __init__(self):
        self.rdp = redis.ConnectionPool(host='wnm1', port=7000)
        # self.rds = redis.Redis(host='wnm1', port=7000)
        self.rdc = redis.StrictRedis(connection_pool=self.rdp)
        self.hb = happybase.Connection(host='wnm1', port=9090)

    def getRedisConn(self):
        return self.rdc

    def getHbaseConn(self):
        return self.hb

    def getRedisData(self, key):
        """
        从redis获取数据，并反序列化
        :param key:
        :return:
        """
        byteDatas = self.rdc.get(key)
        print('key: ', key, 'bytes: ', byteDatas)
        return json.loads(byteDatas.decode("utf-8")) if byteDatas else ''

    def save2Redis(self, key, val):
        """
        将数据序列化后,存入redis中
        :param key:
        :param val:
        :return:
        """
        return self.rdc.set(key, json.dumps(val))


my_conn = MyConnect()
print(111)
def getMyConn():
    print(222)
    try:
        global my_conn
        return my_conn
    except:
        print('new connect')
        return MyConnect()

if __name__ == '__main__':
    json.loads(b'1'.decode("utf-8"))
