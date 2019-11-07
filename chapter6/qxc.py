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
            return response.text
        return None
    except RequestException:
        print('请求 URL 出错：', url)
        return None

def parse_one_page(html):
    trs = pq(html).find('.result tbody')
    for tr in trs.items('tr'):
        yield {
            'id': tr.find('td:nth-child(1)').text(),
            'number': tr.find('td:nth-child(2)').text(),
            'bonus': tr.find('td:nth-child(17)').text(),
            'date': tr.find('td:nth-child(18)').text()
        }

def init_file():
    headers = ['id', 'number', 'bonus', 'date']
    with open('qxc.csv', 'a') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()

def write_to_file(content):
    headers = ['id', 'number', 'bonus', 'date']
    with open('qxc.csv', 'a') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writerow(content)

def main(page):
    url = 'http://www.lottery.gov.cn/historykj/history_{}.jspx?_ltype=qxc'.format(page)
    print('正在爬取第{}页'.format(page), url)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    init_file()
    for i in range(1, 11):
        main(page=i)
        time.sleep(1)
