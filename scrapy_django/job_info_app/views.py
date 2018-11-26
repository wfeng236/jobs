import re

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

code2city = {
    '1': '北京',
    '2': '上海',
    '3': '广州',
    '4': '深圳',
}

code2job = {
    '1': 'Python Web',
    '2': '爬虫',
    '3': '大数据',
    '4': 'AI',
}

def main_page(request):
    return render(request, 'job_pages/main.html')

def introduce_page(request):
    return render(request, 'job_pages/introduce.html')

def menu_page(request):
    """
    数据菜单页
    :param request:
    :return:
    """
    # 1.获取请求参数
    city = code2city.get(request.GET.get('city'))
    key = code2job.get(request.GET.get('key'))
    pn = request.GET.get('pn')
    sk = request.GET.get('sk')
    sc = request.GET.get('sc')
    sa = request.GET.get('sa')
    exp = request.GET.get('exp')
    isasy = request.GET.get('isasy')
    print('params: ', city, key, pn, sk, sc, sa, exp, isasy)
    # 2.查询数据


    # 3. 封装数据 字典格式


    # 4. 响应
    return render(request, 'job_pages/menu.html')

def getDatas(city, key='', pn='', sk='', sc='', sa='', exp='', isasy=False):
    """"""
    # pn<=10, 从mysql获取数据

    # pn>10, 从hbase 获取数据


def getDatasFromMysql():
    """"""




def getDatasFromHbase():
    """"""

def suggest_ajax(request):
    """
    ajax异步接收搜索框传来的数据，并进行正则匹配，将匹配的数据用json返回
    :param request:
    :return:
    """
    # 下拉表单的值：0：未选择；1：城市；2：职位；
    area = request.POST.get("type")
    # 搜索框中的内容
    words = request.POST.get("message")
    # 将搜索框中的字母转为小写
    words = words.lower()
    # 城市匹配数据库
    suggests_city = """
北京
上海
广州
深圳
beijing 
shanghai
guangzhou
shenzhen"""
    # 职位匹配数据库
    suggests_key = """
ai
python web
大数据
dashuju
爬虫
pachong"""
    # 全部匹配
    suggests = """
北京
上海
广州
深圳
beijing 
shanghai
guangzhou
shenzhen
ai
python web
大数据
dashuju
爬虫
pachong"""
    # 匹配城市
    if area == "1":
        rule = re.compile('.*' + words + '.*', re.M)
        result = rule.findall(suggests_city)
    # 匹配职业
    elif area == "2":
        rule = re.compile('.*' + words + '.*', re.M)
        result = rule.findall(suggests_key)
    # 全部匹配
    else:
        rule = re.compile('.*' + words + '.*', re.M)
        result = rule.findall(suggests)
    print(words,result,area)
    return JsonResponse({"result": result})