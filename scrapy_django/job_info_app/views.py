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
