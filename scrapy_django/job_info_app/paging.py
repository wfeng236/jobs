#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: wf
@contact: wf17719390964@163.com
@software: pycharm
@file: paging.py
@time: 2018/11/26 20:15
@desc:
'''
from django.core.paginator import Paginator

# 获取返回列表res
# 从请求中获取分页面数目per_page
# 从请求中获取当前页面current_page
# 对原始结果集进行分页的处理函数
def paginator(object_list, per_page, current_page):
    # print('paginator')
    # p = Paginator(object_list, per_page)
    # contacts = p.page(current_page)
    contacts = Paginator(object_list, per_page).page(current_page)
    # print(contacts.object_list)
    # for p in contacts.object_list:
    #     print(p)
    # print(type(contacts.number))
    # print(type(contacts.paginator.num_pages))
    # print(type(contacts.has_next()))
    # print(type(contacts.has_previous()))
    # print(type(contacts.next_page_number() if contacts.has_next() else 0))
    # print(type(contacts.previous_page_number() if contacts.has_previous() else 0))
    # print(type(contacts.object_list))

    return {
        "number"    : contacts.number,
        "num_pages" : contacts.paginator.num_pages,
        'has_next'  : contacts.has_next(),
        'has_prev'  : contacts.has_previous(),
        'next_page' : contacts.next_page_number() if contacts.has_next() else 0,
        'prev_page' : contacts.previous_page_number() if contacts.has_previous() else 0,
        'objects'   : contacts.object_list,
        'page_list' : list(contacts.paginator.page_range),
    }

