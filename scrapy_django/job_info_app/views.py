import json
import re

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from job_info_app.models import Hoteljob
from job_info_app.my_log import MyLog
from job_info_app.my_utils import sortData
from job_info_app.paging import MyPaginator
from job_info_app.my_connect import getMyConn

#
code2city = {
    '1': '北京',
    '2': '上海',
    '3': '广州',
    '4': '深圳',
}

code2job = {
    '1': 'Web',
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
    # 城市
    city = code2city.get(request.GET.get('city') or '1')
    # 职业
    key = code2job.get(request.GET.get('key') or '3')
    # 页号
    pn = int(request.GET.get('pn') or 1)
    # 搜索类型
    sk = request.GET.get('sk')
    # 搜索内容
    sc = request.GET.get('sc')

    # 是否是异步请求
    isasy = request.GET.get('isasy')
    print('params: ', city, key, pn, sk, sc, isasy)

    # request.session['sortdict'] = {'sa': '', 'exp': '',}
    login_user = request.session.get('login_user')
    return deal_menu_page(request, city, key, pn, sk, sc, isasy, login_user)


@MyLog
def deal_menu_page(request, city, key, pn, sk, sc, isasy, login_user):
    """

    :param request:
    :param city:
    :param key:
    :param pn:
    :param sk:
    :param sc:
    :param isasy:
    :param login_user:
    :return:
    """
    # sk=='1'('2') 表示搜索类型为城市(职位)，搜索内容为sc
    if sk == '1':
        city = sc
        key = ''
    elif sk == '2':
        key = sc
        city = ''

    # 2.查询数据
    sf, sd = request.session.get('sort_rule', ('0', '0'))
    dataName = '%s:%s:%s:%s'%(city, key, sf, sd)
    # 获取缓存数据
    # rdc = getMyConn().getRedisConn()
    # # pagesBytes = b'' and rdc.get(dataName)
    # byteDatas = rdc.get(dataName)
    datas = getMyConn().getRedisData(dataName)
    print('xxxxx',datas)
    # pages = request.session.get(pageName)
    # 如果没有缓存
    if not datas:

        # datas = getDatas(city, key, login_user)
        # request.session['datas'] = datas

        datas = sortData(getDatas(city, key, login_user), sf, sd)
        # rdc.set(dataName, json.dumps(datas, default=None))
        getMyConn().save2Redis(dataName, datas)
        request.session['data_name'] = dataName

    # 3. 分页 封装数据 字典格式
    pages = MyPaginator(datas)
    # request.session[pageName] = pages
    # request.session['total_count'] = len(datas)

    request.session['pn'] = pn
    resp = {
        'result': 1,
        'page': pages.pageDict(pn),
        'params': {'city': city, 'key': key},
    }
    print(resp)

    # 4. 响应
    if isasy:
        return JsonResponse(resp)
    else:
        return render(request, 'job_pages/menu.html', resp)



def dataSort(request):
    """

    :param request:
    :return:
    """
    # 排序字段 1：salary 2：experience
    sf = request.GET.get('sf') or '0'
    # 排序方向 1：asc 2：desc
    sd = request.GET.get('sd') or '0'
    print('dataSort: ', sf, sd)
    dataName = request.session.get('data_name')
    # rdc = getMyConn().getRedisConn()
    # datas = rdc.get(dataName)
    datas = getMyConn().getRedisData(dataName)
    pn = request.session.get('pn', 1)
    request.session['sort_rule'] = (sf, sd)
    resp = {
        'result': 1,
        'page': MyPaginator(sortData(datas, sf, sd)).pageDict(pn),
    }

    return JsonResponse(resp)


def getDatas(city, key, login_user='1'):
    """
    查询数据
    :param city:
    :param key:
    :param login_state:
    :return:
    """
    # 如果未登录，只能看10页, 从mysql获取数据
    datas = list(getDatasFromMysql(city, key))
    hbasedatas = []
    # 登录了，全查, 从hbase 获取数据
    if login_user:
        hbasedatas = getDatasFromHbase(city, key)
        # hbasedatas = [{k.replace('show:', ''): v for k, v in d.items()} for d in hbasedatas if hbasedatas]

    print('mysqldatas: ', datas)
    print('hbasedatas: ', hbasedatas)
    # for d in alldatas:
    #     for k,v in d.items():
    #         print(k, v)
    datas.extend(hbasedatas)

    return datas


def getDatasFromMysql(city, key):
    """
    从mysql中查询数据
    :param city:
    :param key:
    :return:
    """
    return Hoteljob.objects.filter(city__icontains=city, job_type__icontains=key).values('job_title', 'company_name', 'salary', 'job_description', 'experience', 'degree', 'company_address', 'format_salary', 'format_experience')


def getDatasFromHbase(city, key):
    """
    从hbase中查询数据
    :param city:
    :param key:
    :return:
    """
    # 'wnm1'是域名，需要在计算机中配置
    # 获取连接
    conn = getMyConn().getHbaseConn()
    # 获取表对象
    table = conn.table('jobs:t_hoteljob1')
    # 查询数据
    try:
        return [{k1.decode('utf-8').replace('show:', ''): v1.decode('utf-8') for k1, v1 in v.items()} for k, v in
            table.scan(filter="RowFilter(=,'regexstring:\.*%s.*%s.*/')" % (city, key), columns=('show',), limit=1)]
    except:
        return []


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
    print(words, result, area)
    return JsonResponse({"result": result})
