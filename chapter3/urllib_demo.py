# -*- coding: UTF-8 -*-
import json
import socket
import urllib.request
import urllib.parse
import urllib.error
import urllib.robotparser
from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener, ProxyHandler
import http.cookiejar

def urlopen():
    response = urllib.request.urlopen("https://www.python.org")
    # http.client.HTTPResponse 可以看这个对象的源码，看看有什么方法和用法
    print(type(response))
    print(response.getcode())
    print(response.getheaders())
    print(response.getheader("Server"))
    # print(response.read().decode("utf-8"))

def urlopen_data():
    # 将参数转码
    data = bytes(urllib.parse.urlencode({'word': 'hello'}), encoding='utf8')
    response = urllib.request.urlopen("http://httpbin.org/post", data=data)
    print(json.loads(response.read()))

def urlopen_timeout():
    try:
        # 设置超时时间为0.1S
        response = urllib.request.urlopen("http://httpbin.org/get", timeout=0.1)
        print(json.loads(response.read()))
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            print("time out")

# urlopen()
# urlopen_data()
# urlopen_timeout()

def request():
    url = "http://httpbin.org/post"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Host': 'http://httpbin.org'
    }
    data = bytes(urllib.parse.urlencode({'name': 'gabear'}), encoding='utf8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    response = urllib.request.urlopen(req)
    print(json.loads(response.read()))
    # print(json.dumps(json.loads(response.read()), indent=2))

# request()

def auth():
    """
    用于处理需要验证账号密码的情况
    """
    username = 'username'
    password = 'password'
    url = 'http://localhost:5000/'

    p = HTTPPasswordMgrWithDefaultRealm()
    # 添加需要认证的账号密码
    p.add_password(None, url, username, password)
    # 构建BasicAuthHandler然后构建opener
    auth_handler = HTTPBasicAuthHandler(p)
    opener = build_opener(auth_handler)

    try:
        response = opener.open(url)
        print(response.read().decode('utf-8'))
    except urllib.request.URLError as e:
        print(e.reason)

def proxy():
    """
    使用代理访问
    """
    proxy_handler = ProxyHandler({
        'http': 'http://127.0.0.1:9743',
        'https': 'https://127.0.0.1:9743'
    })
    opener = build_opener(proxy_handler)
    try:
        response = opener.open('https://www.baidu.com')
        print(response.read().decode('utf-8'))
    except urllib.request.URLError as e:
        print(e.reason)

def cookie():
    """
    获取所有 cookie 值
    """
    cookies = http.cookiejar.CookieJar()
    cookie_handler = urllib.request.HTTPCookieProcessor(cookies)
    opener = build_opener(cookie_handler)
    response = opener.open('http://www.baidu.com')
    for item in cookies:
        print(item.name + "=" + item.value)

# cookie()

def cookie_save():
    filename = 'cookies.txt'
    # 可以保存为Mozilla或者LWP格式
    cookies = http.cookiejar.MozillaCookieJar(filename)
    cookie_handler = urllib.request.HTTPCookieProcessor(cookies)
    opener = build_opener(cookie_handler)
    response = opener.open('http://www.baidu.com')
    cookies.save(ignore_discard=True, ignore_expires=True)

def cookie_save_load():
    # 存储
    filename = 'cookies.txt'
    cookies = http.cookiejar.LWPCookieJar(filename)
    cookie_handler = urllib.request.HTTPCookieProcessor(cookies)
    opener = build_opener(cookie_handler)
    response = opener.open('http://www.baidu.com')
    cookies.save(ignore_discard=True, ignore_expires=True)
    # 读取
    cookies = http.cookiejar.LWPCookieJar()
    cookies.load('cookies.txt', ignore_discard=True, ignore_expires=True)
    cookie_handler = urllib.request.HTTPCookieProcessor(cookies)
    opener = build_opener(cookie_handler)
    response = opener.open('http://www.baidu.com')
    print(response.read().decode('utf-8'))

# cookie_save_load()


def error_hand():
    try:
        urllib.request.urlopen('https://github.com/0/1')
        # 因为HTTPError是URLError的子类
    except urllib.error.HTTPError as e:
        print(e.reason, e.code, e.headers, sep='\n')
    except urllib.error.URLError as e:
        print(e.reason)
    else:
        print('Request successful.')

# error_hand()

def parse():
    result = urllib.parse.urlparse('http://www.baidu.com/index.html;user?id=5#comment')
    print(result.scheme, result.netloc, result.path, result.params, result.query, result.fragment)
    # http www.baidu.com /index.html user id=5 comment

    # 需要按照顺序指定6个参数
    data = ['http', 'www.baidu.com', 'index.html', 'user', 'a=6', 'comment']
    print(urllib.parse.urlunparse(data))
    # http://www.baidu.com/index.html;user?a=6#comment

    result = urllib.parse.urlsplit('http://www.baidu.com/index.html;user?id=5#comment')
    print(result)
    # SplitResult(scheme='http', netloc='www.baidu.com', path='/index.html;user', query='id=5', fragment='comment')

    data = ['http', 'www.baidu.com', 'index.html', 'a=6', 'comment']
    print(urllib.parse.urlunsplit(data))
    # http://www.baidu.com/index.html?a=6#comment

    # 使用 join 随意组合
    print(urllib.parse.urljoin('http://www.baidu.com', 'faq.html'))
    print(urllib.parse.urljoin('http://www.baidu.com', 'http://github.com/0'))
    print(urllib.parse.urljoin('http://www.baidu.com/about.html', 'http://github.com/0'))
    print(urllib.parse.urljoin('http://www.baidu.com/about.html', 'http://github.com/0?tab=new'))
    print(urllib.parse.urljoin('http://www.baidu.com?wd=abc', 'http://github.com/0'))
    print(urllib.parse.urljoin('http://www.baidu.com', '?category=2#comment'))
    print(urllib.parse.urljoin('www.baidu.com', '?category=2#comment'))
    print(urllib.parse.urljoin('www.baidu.com#comment', '?category=2'))
    # http://www.baidu.com/faq.html
    # http://github.com/0
    # http://github.com/0
    # http://github.com/0?tab=new
    # http://github.com/0
    # http://www.baidu.com?category=2#comment
    # www.baidu.com?category=2#comment
    # www.baidu.com?category=2

    params = {
        'name': 'gabear',
        'age': '18'
    }
    url = 'http://www.baidu.com?' + urllib.parse.urlencode(params)
    print(url)
    # http://www.baidu.com?name=gabear&age=18

    query = 'name=gabear&age=18'
    print(urllib.parse.parse_qs(query))
    # {'name': ['gabear'], 'age': ['18']}
    print(urllib.parse.parse_qsl(query))
    # [('name', 'gabear'), ('age', '18')]

    keyword = '编码'
    print('http://www.baidu.com/s?wd=' + urllib.parse.quote(keyword))
    # http://www.baidu.com/s?wd=%E7%BC%96%E7%A0%81

    url = 'http://www.baidu.com/s?wd=%E7%BC%96%E7%A0%81'
    print(urllib.parse.unquote(url))
    # http://www.baidu.com/s?wd=编码

# parse()

def robot():
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url('https://www.jianshu.com/robots.txt')
    rp.read()
    # rp.parse(urllib.request.urlopen('https://www.jianshu.com/robots.txt').read().decode('utf-8').split('\n'))
    print(rp.can_fetch('*', 'https://www.jianshu.com/p/3201475a5ee2'))
    print(rp.can_fetch('*', 'https://www.jianshu.com/search?q=python&page=1&type=note'))

robot()

# https://docs.python.org/zh-cn/3/library/urllib.request.html