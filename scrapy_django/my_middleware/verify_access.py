#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: wf
@contact: wf17719390964@163.com
@software: pycharm
@file: verify_access.py
@time: 2018/11/28 17:33
@desc:
'''
from pprint import pprint
from django.utils.deprecation import MiddlewareMixin

from job_info_app.my_connect import getMyConn

BROWSER_FLAGS = ('MSIE', '360SE', 'SE', 'MetaSr', 'Chrome', 'Android', 'Linux', 'MobileSafari', 'Safari', 'TencentTraveler', 'QQBrowser', 'Firefox', 'TheWorld', 'Maxthon', 'Opera', 'UCWEB')
NEED_CHECK = ('menu',)

def isNeedCheck(cur_path):
    for i in NEED_CHECK:
        if i in cur_path:
            return True
    return False

class VeryfyAccessMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        """"""
        super(VeryfyAccessMiddleware, self).__init__(get_response)

    def process_request(self, request):
        """
        view处理请求前执行
        :param request:
        :return:
        """
        # pprint(request.META['HTTP_REFERER'])
        # pprint(request.META['HTTP_USER_AGENT'])
        if not self.isBrowser(request.META['HTTP_USER_AGENT']):
            return

        curPath = request.path
        print(curPath)
        if isNeedCheck(curPath):
            ip = request.META.get('REMOTE_ADDR')
            print(ip)
            r = getMyConn().getRedisConn()
            # 判断 ip是否被封
            banName = 'ban:%s'%ip
            if r.get(banName):
                # 被封了
                return

            name = 'ip:%s'%ip
            count = r.get(name)
            if not count:
                r.set(name, 1)
                # 设置有效时间 60秒
                r.expire(name, 60)
            elif count > 60:
                # 一分钟访问超过 60次, 封 ip一天
                r.set(banName, 1)
                r.expire(banName, 24*60*60)

            else:
                r.set(name, int(count) + 1)


    def isBrowser(self, user_agent):
        for i in BROWSER_FLAGS:
            if i in user_agent:
                return True
        return False

