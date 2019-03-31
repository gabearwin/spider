# -*- coding: UTF-8 -*-

import requests
import re

def get():
    data = {
        'name': 'gabear',
        'age': 18
    }
    proxies = {
        'http': 'http://10.10.1.10:3128',
        'https': 'http://user:password@10.10.1.10:1080'
    }
    response = requests.get('https://httpbin.org/get', params=data, proxies=proxies, timeout=10)
    response.encoding = 'utf-8'
    print(type(response))
    print(response.status_code)
    print(response.text)
    print(response.cookies)
    print(response.headers)

# get()

def post():
    file = {'file': open('favicon.ico', 'rb')}
    response = requests.post('https://httpbin.org/post', files=file)
    print(response.text)

def get_text():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    response = requests.get('https://www.zhihu.com/explore', headers=headers)
    pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.S)
    titles = re.findall(pattern, response.text)
    print(titles)

def get_picture():
    response = requests.get('http://github.com/favicon.ico')
    with open('favicon.ico', 'wb') as f:
        f.write(response.content)

# get_picture()

def cookie():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Host': 'www.zhihu.com',
        'Cookie': '_zap=0d523171-d861-40fd-9f55-2c704373d0cb; d_c0="AAAkkLKpAw-PTn2mx8hOuRk-rd96ElH81WU=|1550723849"; '
                  'z_c0=Mi4xNEQ0WUFnQUFBQUFBQUNTUXNxa0REeGNBQUFCaEFsVk5ONTFiWFFBM1B3Sk5TdXR3V2Y5WnRPVmJZeE1iZDRnQ3JB|1550733111|a40716861b559358'
                  '87adb2c63325edd9436e1b64; tst=r; __utma=51854390.1778329819.1552875157.1552875157.1552875157.1; __utmz=51854390.1552875157.1.'
                  '1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/64055675/answer/560820303; __utmv=51854390.100--|2=regis'
                  'tration_date=20150915=1^3=entry_date=20150915=1; _xsrf=efdd0bcf-062e-4c63-b922-1934f3d4f13a; q_c1=faefde5e256a4d5980ef12df563d1'
                  'b1e|1553871110000|1550899532000; tgw_l7_route=060f637cd101836814f6c53316f73463'
    }
    response = requests.get('https://www.zhihu.com', headers=headers)
    print(response.text)

# cookie()

def sessions():
    session = requests.session()
    session.get('http://httpbin.org/cookies/set/number/123456')
    response = session.get('http://httpbin.org/cookies')
    print(response.text)

# sessions()

def proxy_auth():
    proxies = {
        'http': 'http://10.10.1.10:3128',
        'https': 'http://user:password@10.10.1.10:1080'
    }
    response = requests.get('https://httpbin.org/get', proxies=proxies, auth=('username', 'password'))
    print(response.status_code)

def request_pre():
    url = 'https://httpbin.org/post'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    data = {
        'name': 'gabear'
    }
    s = requests.session()
    req = requests.Request('POST', url, headers=headers, data=data)
    prepare = s.prepare_request(req)
    response = s.send(prepare)
    print(response.text)

request_pre()