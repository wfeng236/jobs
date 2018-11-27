#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: wf
@contact: wf17719390964@163.com
@software: pycharm
@file: my_log.py
@time: 2018/11/27 21:47
@desc:
'''
import uuid
from datetime import datetime
from pprint import pprint

from job_info_app.get_city_of_ip import get_city
from job_info_app.my_utils import getHbaseConn


class MyLog:
    def __init__(self,fun):
        self.fun=fun
        print('fname: ', fun.__name__)
    def __call__(self, *args):
        if self.fun.__name__ == 'deal_menu_page':
            req, city, key, _, _, _, _, login_user = args
            # pprint(req.META)
            ip = req.META.get('REMOTE_ADDR')
            print(ip)
            if not login_user:
                login_user = ip
            login_city = get_city(ip)
            # 哪个用户 在 哪个城市 什么时间 访问了 哪个城市 的 哪个职位
            self.save2hbase(login_user, login_city, city, key)
        return self.fun(*args)

    def save2hbase(self, user, login_city, city, job):
        conn = getHbaseConn()
        # 获取表对象
        table = conn.table('jobs:t_logs')
        curtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        table.put(
            row=uuid.uuid4(),
            data={
                'log:user': user,
                'log:login_city': login_city,
                'log:time': curtime,
                'log:city': city,
                'log:job': job,
            }
        )


@MyLog   # funA(funC)()
def funC(a):
    print('C', a)
# funC('123')

# a = funC
# print(a.__name__)
