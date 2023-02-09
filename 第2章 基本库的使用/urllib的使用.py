# _*_ coding: utf-8 _*_
# @Time: 2023/2/9 15:05
# @Author: lemon
# @File: urllib的使用
# @Project: WebCrawlerDevelopment
import socket
import urllib.request
import urllib.parse
import urllib.error

"""
urllib的4个模块:
* request: 最基本的http请求模块，可以模拟请求的发送。
* error: 异常处理模块。
* parse: 工具模块，提供了许多URL的处理方法，如拆分、解析、合并等。
* robotparser: 识别网站的robots.txt文件，不常用。
"""


# urllib.request.urlopen()的使用
def use_urlopen():
    # 发送请求
    resp = urllib.request.urlopen('https://www.python.org')
    print('type of response: ', type(resp))
    print('response status', resp.status)
    print('response headers', resp.getheaders())

    # data参数
    # 可选，传递此参数时请求方法为POST，参数需要转码成bytes类型
    data = bytes(urllib.parse.urlencode({'name': 'lemon'}), encoding='utf-8')
    resp = urllib.request.urlopen('https://www.httpbin.org/post', data=data)
    print(resp.read().decode('utf-8'))

    # timeout参数
    # 用于设置超时时间，单位为秒
    try:
        resp = urllib.request.urlopen('https://www.httpbin.org/get', timeout=0.1)
        print(resp.read())
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            print('Catch Exception: Time out.')


# urllib.request.Request的使用
def use_request():
    url = 'https://www.httpbin.org/post'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78',
        'Host': 'www.httpbin.org'
    }
    data = urllib.parse.urlencode({'name': 'lemon'})
    req = urllib.request.Request(url=url, data=bytes(data, encoding='utf-8'), headers=headers, method='POST')
    req.add_header('referer', 'https://www.baidu.com')
    resp = urllib.request.urlopen(req)
    print(resp.read().decode('utf-8'))


# urllib.parse常用方法
def use_parse():
    # url_parse()
    # URL识别和分段
    url = 'https://www.baidu.com/index.html;user?id=5#comment'
    result = urllib.parse.urlparse(url)
    print(result)

    # url_join()
    # URL的合并生成，此方法会分析base_url的scheme、netloc、path三个内容，并对新链接缺失的部分进行补充
    print(urllib.parse.urljoin('https://www.baidu.com', 'FAQ.html'))
    print(urllib.parse.urljoin('https://www.baidu.com', 'https://cuiqingcai.com/FAQ.html'))

    # urlencode()
    # 将字典类型转化成GET请求参数
    params = {
        'name': 'lemon',
        'age': 24
    }
    print(urllib.parse.urlencode(params))
    pass


if __name__ == '__main__':
    # use_request()
    use_parse()
    pass
