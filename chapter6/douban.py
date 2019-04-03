# -*- coding: UTF-8 -*-
import csv
import time
import requests
from pyquery import PyQuery as pq
from requests import RequestException, codes

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == codes.ok:
            parse_one_page(response.text)
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    ul = pq(html).find('ul.subject-list')
    for li in ul.items('li'):
        yield {
            'url': li.find('.pic a').attr('href'),
            'picture': li.find('.pic a img').attr('src'),
            'name': li.find('.info h2 a').text().replace(' ', ''),
            'press': li.find('.info .pub').text().replace(' ', ''),
            'rate': li.find('.info .star').text().replace(' ', ''),
            'info': li.find('.info p').text()
        }

def write_to_file(content):
    headers = ['url', 'picture', 'name', 'press', 'rate', 'info']
    with open('douban.csv', 'a') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writerow(content)

def main(tag, start):
    url = 'https://book.douban.com/tag/{}?start={}&type=T'.format(tag, start)
    print('正在爬取', url)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    tag = '名著'
    for i in range(5):
        main(tag, start=i * 20)
        time.sleep(1)
