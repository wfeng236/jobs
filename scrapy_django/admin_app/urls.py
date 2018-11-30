"""scrapy_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('register/', include(([
        #注册跳转路径
        path('page/',views.register_page, name='page'),
        #异步验证用户名路径
        path('ajax_username/',views.ajax_username, name='ajax_username'),
        #异步验证用户名路径
        path('ajax_phone/',views.ajax_phone, name='ajax_phone'),
        #异步验证邮箱路径
        path('ajax_emailyz/',views.ajax_emailyz,name='ajax_emailyz'),
        #邮箱确认路径
        path('emailyz/',views.register_emailyz,name='emailyz'),
        #注册接收路径
        path('logic/',views.register_logic,name='logic'),
        #注册成功路径
        path('ok/',views.register_ok,name='ok')
    ],'register'))),

    path('login/', include(([
        #登录跳转路径
        path('page/',views.login_page, name='page'),
        #生成验证码路径
        path('capshow/',views.get_captcha,name='capshow'),
        #异步验证验证码路径
        path('ajax_yzm/',views.ajax_yzm,name='ajax_yzm'),
        #登录接收路径
        path('logic/',views.login_logic,name='logic')
    ],'login'))),
]
