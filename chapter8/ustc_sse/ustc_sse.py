# -*- coding: UTF-8 -*-

import pymongo
import requests
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from chapter8.ustc_sse.config import *
from chapter8.ustc_sse.email_util import send_email

# browser = webdriver.Chrome()

# SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
# browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)

wait = WebDriverWait(browser, 10)
client = pymongo.MongoClient(MONGO_URL)
database = client[MONGO_DB]
collection = database[MONGO_COLLECTION]

def login():
    """
    登陆账号密码
    """
    print('正在准备登录...')
    try:
        url = 'http://mis.sse.ustc.edu.cn/default.aspx'
        browser.get(url)
        username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#winLogin_sfLogin_txtUserLoginID')))
        password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#winLogin_sfLogin_txtPassword')))
        validate = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#winLogin_sfLogin_txtValidate')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#ext-gen8')))

        img_link = browser.find_element_by_id('winLogin_sfLogin_ContentPanel3_imgValidateCode') \
            .find_element_by_tag_name('img').get_attribute('src')
        username.clear()
        password.clear()
        validate.clear()
        username.send_keys(SSE_USER)
        password.send_keys(SSE_PASS)
        # print(browser.get_cookie('CheckCode'))
        validate.send_keys(get_code_sum(str(browser.get_cookie('CheckCode').get('value'))))
        submit.click()

        # 确实是跳转到了下一页
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#RegionPanel1_MainRegion')))
        # print(browser.page_source)
        browser.switch_to.frame('MainFrame')
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#global_LeftPanel_UpRightPanel_ContentPanel2_ContentPanel3_content')))
        print("登录成功,准备爬取最新通知")
        # print(browser.get_cookies())
        fetch_all_news()
    except Exception as e:
        print(e.args)
        login()

def get_code_sum(code):
    """
    计算验证码数字之和
    :param code:验证码字符串
    :return: 验证码之和
    """
    sum = 0
    for i in code:
        sum += int(i)
    return sum

def fetch_all_news():
    for item in get_news():
        print(item)
        save_to_mongo(item)

def get_news():
    """
    获取最新通知
    """
    doc = pq(browser.page_source)
    doc.remove_namespaces()  # 不然下面获取不了表格
    tbody = doc('#global_LeftPanel_UpRightPanel_ContentPanel2_ContentPanel3_content').find('tbody')
    for row in tbody.find('tr').items():
        href = str(row.find('td').eq(0).find('a').attr('href'))
        url = 'http://mis.sse.ustc.edu.cn' + href
        yield {
            'id': href[href.find('ID') + 3:],
            'url': url,
            'title': row.find('td').eq(0).text(),
            'teacher': row.find('td').eq(1).text(),
            'time': row.find('td').eq(2).text(),
            'content': get_url_text(url)
        }

def get_url_text(url):
    """
    获取通知正文内容
    :param url: 通知链接
    :return: 通知正文
    """
    headers = {
        'Cookie': 'iflyssesse=' + browser.get_cookie('iflyssesse').get('value')
    }
    html = requests.get(url, headers=headers)
    doc = pq(html.text).remove_namespaces().find('#cx_nav')
    # print(doc.text())
    return doc.text()

def save_to_mongo(news):
    try:
        if collection.find_one({'id': news.get('id')}):
            print('MongoDB中已存在%s这条数据' % news.get('id'))
        else:
            collection.insert_one(news)
            send_email(MAIL_TO, news)
            print('存储到MongoDB成功')
    except Exception as e:
        print('存储到MongoDB失败', e.args)

if __name__ == '__main__':
    login()
