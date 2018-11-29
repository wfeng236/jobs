import MySQLdb
import json

import redis

from job_info_app.models import Hoteljob
import happybase
def city_data_query():
    conn = happybase.Connection(host="wnm1", port=9090)
    conn.open()
    table = conn.table('jobs:t_hoteljob1')
    data1 = Hoteljob.objects.filter(city__contains='北京').values('city')
    data2 = Hoteljob.objects.filter(city__contains='上海').values('city')
    data3 = Hoteljob.objects.filter(city__contains='广州').values('city')
    data4 = Hoteljob.objects.filter(city__contains='深圳').values('city')
    data5 = Hoteljob.objects.filter(job_type__contains='ython').values('job_type')
    data6 = Hoteljob.objects.filter(job_type__contains='大数据').values('job_type')
    data7 = Hoteljob.objects.filter(job_type__contains='AI').values('job_type')
    data8 = Hoteljob.objects.filter(job_type__contains='爬虫').values('job_type')
    beijing_mysql = len(list(data1))
    shanghai_mysql = len(list(data2))
    guangzhou_mysql = len(list(data3))
    shenzhen_mysql = len(list(data4))
    python_mysql = len(list(data5))
    dashuju_mysql = len(list(data6))
    ai_mysql = len(list(data7))
    pachong_mysql = len(list(data8))
    print(beijing_mysql)
    query_str1 = "SingleColumnValueFilter ('hide', 'city', =, 'substring:北京')"
    query_str2 = "SingleColumnValueFilter ('hide', 'city', =, 'substring:上海')"
    query_str3 = "SingleColumnValueFilter ('hide', 'city', =, 'substring:广州')"
    query_str4 = "SingleColumnValueFilter ('hide', 'city', =, 'substring:深圳')"
    query1 = table.scan(filter=query_str1)
    query2 = table.scan(filter=query_str2)
    query3 = table.scan(filter=query_str3)
    query4 = table.scan(filter=query_str4)
    beijing_hbase = len(list(query1))
    shanghai_hbase = len(list(query2))
    guangzhou_hbase = len(list(query3))
    shenzhen_hbase = len(list(query4))
    key1 = table.scan(filter="RowFilter(=,'substring:ython')")
    key2 = table.scan(filter="RowFilter(=,'substring:大数据')")
    key3 = table.scan(filter="RowFilter(=,'substring:AI')")
    key4 = table.scan(filter="RowFilter(=,'substring:爬虫')")
    python_hbase = len(list(key1))
    dashuju_hbase = len(list(key2))
    ai_hbase = len(list(key3))
    pachong_hbase = len(list(key4))

    beijing_count = int(beijing_mysql) + int(beijing_hbase)
    shanghai_count = int(shanghai_mysql) + int(shanghai_hbase)
    guangzhou_count = int(guangzhou_mysql) + int(guangzhou_hbase)
    shenzhen_count = int(shenzhen_mysql) + int(shenzhen_hbase)
    python_count = int(python_mysql) + int(python_hbase)
    dashuju_count = int(dashuju_mysql) + int(dashuju_hbase)
    ai_count = int(ai_mysql) + int(ai_hbase)
    pachong_count = int(pachong_mysql) + int(pachong_hbase)

    print(beijing_count)
    print(shanghai_count)
    print(guangzhou_count)
    print(shenzhen_count)
    print(python_count)
    print(dashuju_count)
    print(ai_count)
    print(pachong_count)
    city_info = {
       'beijing_count':str(beijing_count),
        'shanghai_count':str(shanghai_count),
        'guangzhou_count':str(guangzhou_count),
        'shenzhen_count':str(shenzhen_count)
    }
    key_info = {
        'python_count': str(python_count),
        'dashuju_count': str(dashuju_count),
        'ai_count': str(ai_count),
        'pachong_count': str(pachong_count)
    }
    rds = redis.Redis(host='wnm1', port=7000)
    rds.set('city_info',city_info)
    rds.set('key_info', key_info)
if __name__ == '__main__':
    city_data_query()
