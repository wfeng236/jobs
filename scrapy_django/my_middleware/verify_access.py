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

import time
from django.http import JsonResponse
from django.shortcuts import redirect
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
            time.sleep(300)
            return JsonResponse({'msg': '网络不佳~~~'})

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
                print(banName, '123456')
                return JsonResponse({'msg': '请求次数过多！'})

            name = 'ip:%s'%ip
            count = r.get(name)
            if not count:
                # 第一次访问，设置有效时间 60秒
                self.pipe(r, name, 1, 60)
            elif int(count) > 100:
                # 一分钟访问超过 100次, 封 ip一天
                self.pipe(r, banName, 1, 24 * 60 * 60)
                return JsonResponse({'msg': '出错了！'})
            else:
                # 重新设置name会使过期时间失效，需要重新设置
                self.pipe(r, name, int(count) + 1, int(r.ttl(name) or 0))

    def pipe(self, rd, name, count, time):
        pipe = rd.pipeline(transaction=True)
        pipe.set(name, count)
        # 设置有效时间 time秒
        pipe.expire(name, time)
        pipe.execute()

    def isBrowser(self, user_agent):
        for i in BROWSER_FLAGS:
            if i in user_agent:
                return True
        return False

