#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: wf
@contact: wf17719390964@163.com
@software: pycharm
@file: my_utils.py
@time: 2018/11/27 15:29
@desc:
'''
import uuid
from operator import itemgetter, attrgetter
import functools

fieldDict = {
    '1': 'format_salary',
    '2': 'format_experience'
}

# def mycmp(x):
#     # print(x)
#     if not x:
#         return '-1'
#     if '不限' in x or '无' in x:
#         # 经验不限，无工作经验
#         # '-2' > '-1'
#         return '-2'
#     if '经验' in x and '年' in x:
#         # 经验3-5年
#         return x.replace('经验', '')
#     return x.strip()

def sortData(data, field, direction=''):
    '''
    数据排序
    :param data: 要排序的数据, 结构: [{},{},{}]
    :param field: 排序依据的字段 1：salary，2：experience
    :param direction: 排序的方向 1：升序， 2：降序
    :return:
    '''
    print('sortData: ', field, direction)
    if field == direction == '0':
        return data
    return sorted(data, key=lambda x: float(itemgetter(fieldDict[field])(x)), reverse=(direction=='2'))


# def cmp_desc(a, b):
#     """
#     降序
#     :param a:
#     :param b:
#     :return:
#     """
#     if b < a:
#         return -1
#     if a < b:
#         return 1
#     return 0
#
# def cmp_asc(a, b):
#     """
#     升序
#     :param a:
#     :param b:
#     :return:
#     """
#     if b < a:
#         return 1
#     if a < b:
#         return -1
#     return 0
# a = [1, 2, 5, 4, 3, 6, 4, 3]
#
# m = sorted(a, key=functools.cmp_to_key(cmp_desc))
# n = sorted(a, key=functools.cmp_to_key(cmp_asc))
# # print(m, n)
#
# # cmp_to_key源码
# def cmp_to_key(mycmp):
#     """Convert a cmp= function into a key= function"""
#     class K(object):
#         __slots__ = ['obj']
#         def __init__(self, obj):
#             self.obj = obj
#         def __lt__(self, other):
#             return mycmp(self.obj, other.obj) < 0
#         def __gt__(self, other):
#             return mycmp(self.obj, other.obj) > 0
#         def __eq__(self, other):
#             return mycmp(self.obj, other.obj) == 0
#         def __le__(self, other):
#             return mycmp(self.obj, other.obj) <= 0
#         def __ge__(self, other):
#             return mycmp(self.obj, other.obj) >= 0
#         __hash__ = None
#     return K


if __name__ == '__main__':
    ''
    # q=[{'salary': '30k-45k', 'job_title': '22989', 'experience': '5-10年'},
    #    {'salary': '30k-45k','job_title': '22989','experience': '5-10年'},
    #    {'salary': '30k-45k', 'job_title': '22989', 'experience': '5-10年'},
    #    {'salary': '20k-30k', 'job_title': '22989', 'experience': '1-3年'},
    #    {'salary': '25k-35k','job_title': '22989','experience': '经验不限'},
    #    {'salary': '20k-30k', 'job_title': '22989', 'experience': '1-3年'},
    #    {'salary': '30k-45k', 'job_title': '22989', 'experience': '5-10年'},
    #    {'salary': '20k-30k', 'job_title': '23671', 'experience': '3-5年'},
    #    {'salary': '30k-45k','job_title': '23674','experience': '无工作经验'},
    #    {'salary': '30k-45k', 'job_title': '23674', 'experience': '5-10年'},
    #    {'salary': '30k-45k', 'job_title': '25663', 'experience': '5-10年'},
    #    {'salary': '25k-35k', 'job_title': '25663', 'experience': '经验3-5年'},
    #    {'salary': '30k-45k', 'job_title': '26711', 'experience': '经验5-10年'},
    #    {'salary': '80k-100k','job_title': 'AI解','experience': '1-3年'},
    #    {'salary': '20k-30k', 'job_title': 'CSIG', 'experience': '1-3年'},
    #    {'salary': '30k-45k','job_title': 'CSIG16','experience': '5-10年'},
    #    {'salary': '20k-30k', 'job_title': 'CSIG16', 'experience': '1-3年'},
    #    {'salary': '15k-20k', 'job_title': 'Java', 'experience': '3-5年'},
    #    {'salary': '20k-25k','job_title': 'Java','experience': '3-5年'},
    #    {'salary': '17k-25k', 'job_title': 'Java','experience': '3-5年'}]
    # for i in sortData(q, '2', '2'):
    #     print(i)
    # a = {'salary': 100000}
    # print(itemgetter(fieldDict['1'])(a))
    # print(sorted(['1', '6', 'a', 'A', 'Z', 'd', '-', '+', '三', '年','-23', '-33']))
    # print(str(uuid.uuid4()).replace('-', ''), type(uuid.uuid4()))


