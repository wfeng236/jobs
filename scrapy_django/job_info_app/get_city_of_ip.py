"""
根据用户访问页面时的ip来确定他的省份和城市
"""
import requests
from lxml import etree


def get_city(ip):
    """
    根据ip，向ip查询网站发送请求，获得该ip的城市信息
    :param ip: 正确的ip,字符串类型
    :return: 该ip的城市
    """
    # 请求头
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'pgv_pvi=5913526272; pgv_si=s7162642432; ASPSESSIONIDCCSCSCSS=EMCHKLLBIABEAINJJGKLHKPN; ASPSESSIONIDSCTCSACT=HHEHIOMBBPPMFPLBOAJNEMLC',
        'Host': 'www.ip138.com',
        'Referer': 'http://www.ip138.com/ips1388.asp?ip=180.110.5.172&action=2',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }
    # 将ip拼接到url上，发送请求
    resp = requests.get(url='http://www.ip138.com/ips1388.asp?action=2&ip='+str(ip), headers=headers)
    # 指定编码格式，佛则会乱码
    resp.encoding = 'gbk'
    # 将得到的html文档进行解析
    html = etree.HTML(resp.text)
    # 使用xpath解析出指定的信息
    data = html.xpath('//ul[@class="ul1"]/li[1]/text()')[0]
    # 将得到的字符串进行切割，得到有用的信息
    city = data.split('：')[1]
    # 将城市信息返回
    return city.split()[0]

if __name__ == '__main__':
    print(get_city('120.26.199.103'))