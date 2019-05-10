# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import csv
import time
import json
import requests
import re
import random

# 微信公众号账号
USERNAME = "username"
# 微信公众号密码
PASSWORD = "password"
# 设置要爬取的公众号列表
GZHLIST = ['爱学习的乔治']

# 登录微信公众号，获取登录之后的cookies信息，并保存到本地文本中
def get_cookie():
    browser = webdriver.Chrome()
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # browser = webdriver.Chrome(chrome_options=chrome_options)
    wait = WebDriverWait(browser, 20)

    print("启动浏览器，打开微信公众号登录界面...")
    browser.get('https://mp.weixin.qq.com/')
    username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#header > div.banner > div > div > form > '
                                                                           'div.login_input_panel > div:nth-child(1) > div > span > input')))
    password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#header > div.banner > div > div > form > '
                                                                           'div.login_input_panel > div:nth-child(2) > div > span > input')))

    print("正在输入微信公众号登录账号和密码...")
    username.clear()
    username.send_keys(USERNAME)
    password.clear()
    password.send_keys(PASSWORD)

    remember_me = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#header > div.banner > div > div > form > '
                                                                              'div.login_help_panel > label')))
    login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#header > div.banner > div > div > form > '
                                                                               'div.login_btn_panel > a')))
    remember_me.click()
    login_button.click()

    print("请拿手机扫码二维码登录公众号...")
    time.sleep(20)
    print("登录成功...")

    # 重新载入公众号登录页，登录之后会显示公众号后台首页，从这个返回内容中获取cookies信息
    browser.get('https://mp.weixin.qq.com/')
    cookie_items = browser.get_cookies()
    cookie_dict = {}
    # 获取到的cookies是列表形式，将cookies转成json形式并存入本地名为cookie的文本中
    for cookie_item in cookie_items:
        cookie_dict[cookie_item['name']] = cookie_item['value']
    cookie_str = json.dumps(cookie_dict)
    with open('gzh_cookie.txt', 'w+', encoding='utf-8') as f:
        f.write(cookie_str)
    print("cookies信息已保存到本地")

# 爬取微信公众号文章，并存在本地文本中
def get_content(gzh):
    header = {
        "HOST": "mp.weixin.qq.com",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }

    with open('gzh_cookie.txt', 'r', encoding='utf-8') as f:
        cookie = f.read()
    cookies = json.loads(cookie)

    token = get_token(cookies, header)
    fakeid = get_gzh_fakeid(gzh, token, cookies, header)
    get_gzh_article(fakeid, token, cookies, header)

def get_token(cookies, header):
    url = 'https://mp.weixin.qq.com'
    # 登录之后的微信公众号首页url变化为：https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=1849751598，从这里获取token信息
    response = requests.get(url=url, cookies=cookies, headers=header)
    token = re.findall(r'token=(\d+)', str(response.url))[0]
    return token

def get_gzh_fakeid(gzh, token, cookies, header):
    # 搜索微信公众号的接口地址
    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
    # 搜索微信公众号接口需要传入的参数，有三个变量：微信公众号token、随机数random、搜索的微信公众号名字
    query_gzh_param = {
        'action': 'search_biz',
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'query': gzh,
        'begin': '0',
        'count': '5'
    }
    # 打开搜索微信公众号接口地址，需要传入相关参数信息如：cookies、params、headers
    search_response = requests.get(search_url, cookies=cookies, headers=header, params=query_gzh_param)
    # 取搜索结果中的第一个公众号
    gzh = search_response.json().get('list')[0]
    # 获取这个公众号的fakeid，后面爬取公众号文章需要此字段
    fakeid = gzh.get('fakeid')
    return fakeid

def get_gzh_article(fakeid, token, cookies, header):
    file_name = gzh + '.csv'
    file_head = ['aid', 'appmsgid', 'cover', 'digest', 'item_show_type', 'itemidx', 'link', 'title', 'update_time']
    with open(file_name, 'a', encoding='utf-8') as f:
        f_csv = csv.DictWriter(f, file_head)
        f_csv.writeheader()

    # 微信公众号文章接口地址
    appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
    # 搜索文章需要传入几个参数：登录的公众号token、要爬取文章的公众号fakeid、随机数random
    begin = 0
    while True:
        print("正在获取第{}到{}条".format(begin + 1, begin + 5))
        query_gzh_article_param = {
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': '{}'.format(str(begin)),
            'count': '5',
            'query': '',
            'fakeid': fakeid,
            'type': '9'
        }
        # 打开搜索的微信公众号文章列表页
        appmsg_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_gzh_article_param)
        msg_list = appmsg_response.json().get('app_msg_list')
        for msg in msg_list:
            print(msg)
        with open(file_name, 'a', encoding='utf-8') as f:
            f_csv = csv.DictWriter(f, file_head)
            f_csv.writerows(msg_list)
        # 获取文章总数
        max_num = appmsg_response.json().get('app_msg_cnt')
        if (begin + 5) >= max_num:
            break
        begin += 5
        time.sleep(2)

if __name__ == '__main__':
    try:
        get_cookie()
        for gzh in GZHLIST:
            print("开始爬取公众号：" + gzh)
            get_content(gzh)
            print("公众号{}爬取完成".format(gzh))
    except Exception as e:
        print(str(e))
