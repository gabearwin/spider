# -*- coding: UTF-8 -*-

import requests
from lxml import etree

class Login(object):
    def __init__(self):
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Host': 'github.com'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.feed_url = 'https://github.com/dashboard-feed'
        self.profile_url = 'https://github.com/settings/profile'
        self.session = requests.Session()

    def token(self):
        response = self.session.get(self.login_url, headers=self.headers)
        selector = etree.HTML(response.text)
        # 获取第二个 input 的 value 属性
        token = selector.xpath('//div//input[2]/@value')
        print('token:', token)
        return token

    def login(self, email, password):
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token()[0],
            'login': email,
            'password': password
        }
        self.session.post(self.post_url, data=post_data, headers=self.headers)
        # 这里要再次请求一下
        response = self.session.get(self.feed_url, headers=self.headers)
        if response.status_code == 200:
            self.dynamics(response.text)

        response = self.session.get(self.profile_url, headers=self.headers)
        if response.status_code == 200:
            self.profile(response.text)

    def dynamics(self, html):
        selector = etree.HTML(html, etree.HTMLParser(encoding='utf-8'))
        for item in selector.xpath('//body/div/div'):
            item = item.xpath('.//div[@class="d-flex flex-column width-full"]/div[1]//text()')
            news = ' '.join([s.replace('\n', '').replace(' ', '') for s in item]).strip()
            print(news)

    def profile(self, html):
        selector = etree.HTML(html)
        name = selector.xpath('//input[@id="user_profile_name"]/@value')[0]
        email = selector.xpath('//select[@id="user_profile_email"]/option[@value!=""]/text()')
        print(name, email)

if __name__ == "__main__":
    login = Login()
    login.login(email='gabear@outlook.com', password='password')
