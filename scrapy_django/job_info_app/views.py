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
    # 如果没有登录的情况下想访问10页后的内容，不让访问
    # if pn>10 and not request.session.get('login_state'):
    #     return JsonResponse({'result': 0, 'msg': '请登录后再访问!!!'})

    # 2.查询数据
    # sk=='1'('2') 表示搜索类型为城市(职位)，搜索内容为sc
    if sk == '1':
        city = sc
        key = ''
    elif sk == '2':
        key = sc
        city = ''

    datas = getDatas(city, key, login_user)
    request.session['datas'] = datas
    request.session['pn'] = pn
    sf, sd = request.session.get('sort_rule', ('0', '0'))
    datas = sortData(datas, sf, sd)

    # 3. 分页 封装数据 字典格式
    resp = pages(datas, pn)
    print(resp)
    resp.update({'params': {'city': city, 'key': key}})
    print(len(datas))

    # 4. 响应
    if isasy:
        return JsonResponse(resp)
    else:
        return render(request, 'job_pages/menu.html', resp)


def pages(datas, pn):
    page = MyPaginator(datas[:300], 10).pageDict(pn)
    return {
        'result': 1,
        'page': page,
        'total_count': len(datas),
    }


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
    datas = request.session.get('datas')
    pn = request.session.get('pn', 1)
    request.session['sort_rule'] = (sf, sd)

    return JsonResponse(pages(sortData(datas, sf, sd), pn))

# def getSortedData(sf, sd, pn):


def getDatas(city, key, login_user=''):
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
        hdatas = getDatasFromHbase(city, key)
        hbasedatas = [{k.replace('show:', ''): v for k, v in d.items()} for d in hdatas if hdatas]

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
    return Hoteljob.objects.filter(city__icontains=city, job_type__icontains=key).\
        values('job_title', 'company_name', 'salary', 'job_description', 'experience', 'degree', 'company_address')


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
    # city = ''
    # key = '大数据'
    # if city and key:
    #     restr = '.*'.join((city, key))
    # elif city:
    #     restr = city
    # else:
    #     restr = key
    return [{k1.decode('utf-8'): v1.decode('utf-8') for k1, v1 in v.items()} for k, v in
            table.scan(filter="RowFilter(=,'regexstring:\.*%s.*%s.*/')" % (city, key), columns=('show',))]


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
    print(words, result, area)
    return JsonResponse({"result": result})
