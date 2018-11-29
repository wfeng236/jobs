import json

import redis
from django.http import JsonResponse
from django.shortcuts import render

from job_info_app.my_connect import getMyConn
# from .query_data_count import city_data_query
# Create your views here.
def bar_page(request):
    return render(request,'echarts_pages/柱状图.html')
def pie_page(request):
    return render(request,'echarts_pages/饼图.html')
def map_page(request):
    return render(request,'echarts_pages/地图.html')

# def bar_json(request):
#     rds = redis.Redis(host='wnm1', port=7000)
#     city_info = rds.get('city_info1').decode('utf-8')
#     # a = {"shanghai_count": "19530", "guangzhou_count": "11146", "beijing_count": "15596", "shenzhen_count": "13692"}
#     # b = {"ai_count": "30073", "pachong_count": "1104", "python_count": "6931", "dashuju_count": "14570"}
#     # rds.set('city_info_new',json.dumps(a))
#     # rds.set('key_info_new', json.dumps(b))
#     # print(city_info)
#     city_json = json.loads(city_info)
#     # print(key_info)
#     return JsonResponse({'city_info':''})
def bar_json(request):
    rds = getMyConn().getRedisConn()
    city_info = rds.get('city_info_new').decode('utf-8')
    city_json = json.loads(city_info)
    return JsonResponse({'city_info':city_json})

def pie_json(request):
    rds = getMyConn().getRedisConn()
    key_info = rds.get('key_info_new').decode('utf-8')
    key_json = json.loads(key_info)
    return JsonResponse({'key_info':key_json})
def map_json(request):
    rds = redis.Redis(host='wnm1', port=7000)
    map_info = rds.get('map_info').decode('utf-8')
    map_json = json.loads(map_info)
    return JsonResponse({'map_info':map_json})



