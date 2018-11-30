#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

NEED_CHECK = ('menu',)


class LoginCheckMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """
        view处理请求前执行
        :param request:
        :return:
        """
        curPath = request.path
        if curPath == '/':
            return redirect('user:login:page')
        pn = int(request.GET.get('pn') or 1)
        print(curPath)

        if self.isNeedCheck(curPath) and pn>10:
            if request.session.get('login_user'):
                print("已登录")
            else:
                print("未登录")
                return JsonResponse({'result': 2})

    def isNeedCheck(self, cur_path):
        for i in NEED_CHECK:
            if i in cur_path:
                return True
        return False


