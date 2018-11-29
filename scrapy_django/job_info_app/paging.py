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

class MyPaginator(Paginator):
    def __init__(self, object_list, per_page=10, orphans=0,
                 allow_empty_first_page=True):
        super(MyPaginator, self).__init__(object_list[:300], per_page, orphans, allow_empty_first_page)
        self.total_count = len(object_list)

    def pageDict(self, cur_page):
        contacts = self.page(cur_page)
        return {
            "number"        :   contacts.number,
            "num_pages"     :   contacts.paginator.num_pages,
            'has_next'      :   contacts.has_next(),
            'has_prev'      :   contacts.has_previous(),
            'next_page'     :   contacts.next_page_number() if contacts.has_next() else 0,
            'prev_page'     :   contacts.previous_page_number() if contacts.has_previous() else 0,
            'objects'       :   list(contacts.object_list),
            'page_list'     :   list(contacts.paginator.page_range),
            'total_count'   :   self.total_count,
        }

