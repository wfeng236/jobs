import MySQLdb
import json

import redis

# from job_info_app.models import Hoteljob
import happybase

import MySQLdb
from MySQLdb.cursors import DictCursor


def get_conn():
    return MySQLdb.connect(
        host="172.16.14.36",
        port=3306,
        user="root",
        password="123456",
        db='scrapy_project',
        charset="utf8",
    )


def city_data_query():
    conn1 = get_conn()
    cursor = conn1.cursor()
    sql = "select city  from t_hoteljob where city like %s"
    sql1 = "select job_type  from t_hoteljob where job_type like %s"
    conn = happybase.Connection(host="wnm1", port=9090)
    conn.open()
    table = conn.table('jobs:t_hoteljob1')
    a = ['%北京%', '%上海%', '%广州%', '%深圳%']
    b = []
    c = ['%ython%', '%大数据%', '%AI%', '%爬虫%']
    d = []
    for i in range(4):
        cursor.execute(sql,(a[i],))
        b.append(len(cursor.fetchall()))
        print(b)
    for i in range(4):
        cursor.execute(sql1,(c[i],))
        d.append(len(cursor.fetchall()))
        print(d)
    beijing_mysql = b[0]
    shanghai_mysql = b[1]
    guangzhou_mysql = b[2]
    shenzhen_mysql = b[3]
    python_mysql = d[0]
    dashuju_mysql = d[1]
    ai_mysql = d[2]
    pachong_mysql = d[3]


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
    print(json.dumps(key_info))
    print(json.dumps(key_info))
    rds = redis.Redis(host='wnm1', port=7000)
    rds.set('city_info_new',json.dumps(city_info))
    rds.set('key_info_new', json.dumps(key_info))

def getUserDistribution():
    """
    获取用户的分布数据
    :return:
    """
    sql = 'select city, count(user_id) ucount  from t_users group by city'
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(sql)
    datas = dict(cursor.fetchall())
    cursor.close()
    conn.close()
    print(datas)
    rds = redis.Redis(host="wnm1", port=7000)
    rds.set('map_info', json.dumps(datas))
    print(json.loads(rds.get('map_info').decode('utf-8')))





if __name__ == '__main__':
    city_data_query()
    getUserDistribution()

