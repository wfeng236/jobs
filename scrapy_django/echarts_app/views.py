from django.http import JsonResponse
from django.shortcuts import render
from .query_data_count import city_data_query
# Create your views here.
def bar_page(request):
    return render(request,'echarts_pages/柱状图.html')
def pie_page(request):
    return render(request,'echarts_pages/饼图.html')
def map_page(request):
    return render(request,'echarts_pages/地图.html')

# def bar_json(request):
#     return JsonResponse()
# def pie_json(request):
#     return JsonResponse()
# def map_json(request):
#     return JsonResponse()