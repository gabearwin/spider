# -*- coding: UTF-8 -*-
import time

import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from pymongo import MongoClient

base_url = 'https://m.weibo.cn/api/container/getIndex?'
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/5054194713',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'X-Requested-With': 'XMLHttpRequest',
}
client = MongoClient('mongodb://localhost:27017/')
db = client['weibo']
collection = db['weibo']
max_page = 10

def get_page(page: int):
    params = {
        'type': 'uid',
        'value': '5054194713',
        'containerid': '2304135054194713',
        'page': page
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # print(response.json())
            return response.json(), page
    except requests.ConnectionError as e:
        print('Error', e.args)

# get_page(0)

def parse_page(json, page: int):
    if json:
        items = json.get('data').get('cards')
        for index, item in enumerate(items):
            if page == 1 and index == 1:
                continue
            else:
                item = item.get('mblog', {})
                # print(item)
                weibo = {}
                weibo['id'] = item.get('id')
                weibo['text'] = pq(item.get('text')).text()
                weibo['attitudes'] = item.get('attitudes_count')
                weibo['comments'] = item.get('comments_count')
                weibo['reposts'] = item.get('reposts_count')
                weibo['source'] = item.get('source')
                # 把多条结果汇集成一条的生成器
                yield weibo

def save_to_mongo(result):
    if collection.insert_one(result):
        print('Saved to Mongo')

if __name__ == '__main__':
    for page in range(1, max_page + 1):
        json = get_page(page)
        results = parse_page(*json)
        for result in results:
            print(result)
            # save_to_mongo(result)
        time.sleep(1)
