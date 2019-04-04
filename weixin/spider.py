from urllib.parse import urlencode

import requests
from pyquery import PyQuery as pq
from requests import ReadTimeout, ConnectionError
from requests import Session

from weixin.config import *
from weixin.db_mysql import MySQL
from weixin.db_redis import RedisQueue
from weixin.request import WeixinRequest

class Spider(object):
    base_url = 'https://weixin.sogou.com/weixin'
    keyword = '程序员'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'SUV=1550993900621087; SMYUV=1550993900622945; UM_distinctid=1691e70c5081a5-018721d77c368-36647105-1aeaa0-1691e70c50a7fe; IPLOC=CN3100; SUID=16D568DF2D18960A000000005CA4D088; ABTEST=0|1554305167|v1; SNUID=3DFE43F42A2EAE8AF57439F82B01F736; weixinIndexVisited=1; sct=1; JSESSIONID=aaaZ8R3juvpPqbQkr2CNw; ppinf=5|1554305218|1555514818|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozNjolRTglQUYlOUQlRTYlQUQlQUElRTQlQjklOEIlRTUlOUMlQjB8Y3J0OjEwOjE1NTQzMDUyMTh8cmVmbmljazozNjolRTglQUYlOUQlRTYlQUQlQUElRTQlQjklOEIlRTUlOUMlQjB8dXNlcmlkOjQ0Om85dDJsdUlaODZqOG84QzRFSDdYclcwMkU2U01Ad2VpeGluLnNvaHUuY29tfA; pprdig=FeE-UoQE9Qt06Q91C1ZARJ78y67ir67WagkI6CogNhuVgKA5YdTNRAnqtae0JIyDIBVFnbzYrpK8OoGl-44mhQXaf873Uu8e5ba0Qs_vpRhyztNIzKI-SKz3_YkODsmQFpvacSDBc1Wq9Y2P-MRJNlAD8HH1OPNLq2xBfehOFUU; sgid=13-39919407-AVyk0MK6laCx3DuUhCp7aH4; ppmdig=155430521800000087b854fcfd6a6a5d34b9952aa03cd398',
        'Host': 'weixin.sogou.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    session = Session()
    queue = RedisQueue()
    mysql = MySQL()

    def get_proxy(self):
        """
        从代理池获取代理
        :return:一个代理IP:Port
        """
        try:
            response = requests.get(PROXY_POOL_URL)
            if response.status_code == 200:
                print('Get Proxy', response.text)
                return response.text
            return None
        except requests.ConnectionError:
            return None

    def start(self):
        """
        初始化工作
        """
        # 全局更新Headers
        self.session.headers.update(self.headers)
        start_url = self.base_url + '?' + urlencode({'query': self.keyword, 'type': 2})
        weixin_request = WeixinRequest(url=start_url, callback=self.parse_index, need_proxy=True, headers=self.headers)
        # 调度第一个请求
        self.queue.add(weixin_request)

    def schedule(self):
        """
        调度请求
        """
        while not self.queue.empty():
            weixin_request = self.queue.pop()
            callback = weixin_request.callback
            print('Schedule', weixin_request.url)
            response = self.request(weixin_request)
            print(response.text)
            if response and response.status_code in VALID_STATUSES:
                results = list(callback(response))
                if results:
                    for result in results:
                        print('New Result', type(result))
                        if isinstance(result, WeixinRequest):
                            self.queue.add(result)
                        if isinstance(result, dict):
                            self.mysql.insert('weixin', result)
                else:
                    self.error(weixin_request)
            else:
                self.error(weixin_request)

    def request(self, weixin_request):
        """
        执行请求
        :param weixin_request: 请求
        :return: 响应
        """
        # time.sleep(3)
        try:
            if weixin_request.need_proxy:
                proxy = self.get_proxy()
                if proxy:
                    proxies = {
                        'http': 'http://' + proxy,
                        'https': 'https://' + proxy
                    }
                    return self.session.send(weixin_request.prepare(), timeout=weixin_request.timeout, allow_redirects=True, proxies=proxies, verify=False)
            return self.session.send(weixin_request.prepare(), timeout=weixin_request.timeout, allow_redirects=True, verify=False)
        except (ConnectionError, ReadTimeout) as e:
            print(e.args)
            return False

    def parse_index(self, response):
        """
        解析索引页
        :param response: 响应
        :return: 新的响应
        """
        doc = pq(response.text)
        items = doc('.news-box .news-list li .txt-box h3 a').items()
        for item in items:
            url = item.attr('href')
            if not str(url).startswith('http'):
                url = 'https://weixin.sogou.com' + url
            weixin_request = WeixinRequest(url=url, callback=self.parse_detail)
            yield weixin_request
        next = doc('#sogou_next').attr('href')
        if next:
            url = self.base_url + str(next)
            weixin_request = WeixinRequest(url=url, callback=self.parse_index, need_proxy=True)
            yield weixin_request

    def parse_detail(self, response):
        """
        解析详情页
        :param response: 响应
        :return: 微信公众号文章
        """
        doc = pq(response.text)
        data = {
            'title': doc('.rich_media_title').text(),
            'content': doc('.rich_media_content').text(),
            'date': doc('#publish_time').text(),
            'nickname': doc('#js_profile_qrcode > div > strong').text(),
            'wechat': doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        }
        yield data

    def error(self, weixin_request):
        """
        错误处理
        :param weixin_request: 请求
        """
        weixin_request.fail_time = weixin_request.fail_time + 1
        print('Request Failed', weixin_request.fail_time, 'Times', weixin_request.url)
        if weixin_request.fail_time < MAX_FAILED_TIME:
            self.queue.add(weixin_request)

    def run(self):
        """
        入口
        """
        self.start()
        self.schedule()

if __name__ == '__main__':
    spider = Spider()
    spider.run()
