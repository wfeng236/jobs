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
import happybase
import redis



class MyConnect:
    def __init__(self):
        self.rds = redis.Redis(host='wnm1', port=7000)
        self.hb = happybase.Connection(host='wnm1', port=9090)

    def getRedisConn(self):
        return self.rds

    def getHbaseConn(self):
        return self.hb

my_conn = MyConnect()
print(111)
def getMyConn():
    print(222)
    try:
        global my_conn
        return my_conn
    except:
        return MyConnect()


