# -*- coding: UTF-8 -*-
import csv
import time

import requests

def main():
    response = get(0)
    while response['data']['shopList']:
        for shop in response['data']['shopList']:
            print(shop)
            write_to_file(shop)
        time.sleep(2)
        response = get(response['data']['nextStartIndex'])

def get(startIndex):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Referer': 'http://h5.waimai.meituan.com/waimai/mindex/home',
        'Origin': 'http://h5.waimai.meituan.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'Cookie': 'CNZZDATA1264364596=783432722-1557059232-null%7C1557059232; UM_distinctid=16a882973aa1cc-01dc00800cf00e-2d604637-4a574-16a882973ab930; '
                  'IJSESSIONID=liaiow39mgsdjunb4vlaw8zs; __mta=222180647.1556956876023.1556956876023.1556956876023.1; '
                  '__utma=74597006.1950678341.1557040023.1557040023.1557040023.1; __utmc=74597006; '
                  '__utmz=74597006.1557040023.1.1.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/xing851483876/article/details/81842329;'
                  '_ga=GA1.3.2016723402.1556956873; _lx_utm=utm_source%3D60066; _lxsdk=3F031430D276D5042627AF23D7E16C1F7BD0C810BC10022D989E3C108FA64257; '
                  '_lxsdk_cuid=16a81dbae8cc8-0ce589893dd949-36697e04-1aeaa0-16a81dbae8dc8; _lxsdk_s=16a8810a4de-aa6-b68-804%7C%7C9; au_trace_key_net=default; ci=10; '
                  'cityname=%E4%B8%8A%E6%B5%B7; cna=Wun2FPAT2lUCAdOh+PxvzdfJ; i_extend=C_b1Gimthomepagecategory11H__a; iuuid=xxx; latlng=; '
                  'mt_c_token=xxx; '
                  'openh5_uuid=xxx;token=xxx; '
                  'userId=xxx; '
                  'uuid=xxx; webp=1; wm_order_channel=default'
    }
    data = {
        'startIndex': startIndex,
        'sortId': 0,
        'geoType': 2,
        'uuid': 'xxx',
        'platform': 3,
        'partner': 4,
        'originUrl': 'http://h5.waimai.meituan.com/waimai/mindex/home',
        'riskLevel': 71,
        'optimusCode': 10,
        'wm_latitude': 31200640,
        'wm_longitude': 121638109,
        'wm_actual_latitude': 0,
        'wm_actual_longitude': 0
    }
    url = 'http://i.waimai.meituan.com/openh5/homepage/poilist?_=1557066082093&X-FOR-WITH=AuOxmX3mZnBzmrSs0CtZH1lX2EWeewkuMsW60i' \
          '8mEwqG%2B3nFibVH%2FEAF%2BD3iwkpGvwrLcfUqU66ijvJgFpzFVuHB1pmpItbGFEew5pxpv5k7frIWvOt0jzy5fWQt97b7bkX6eJ77MSQmJkKgT9qWaA%3D%3D'
    response = requests.post(url=url, headers=headers, data=data)
    return response.json()

def write_to_file(content):
    headers = ['mtWmPoiId', 'shopName', 'wmPoiScore', 'monthSalesTip', 'picUrl', 'poiTypeIcon', 'deliveryTimeTip',
               'deliveryType', 'minPriceTip', 'shippingFeeTip', 'origin_shipping_fee_tip', 'status', 'statusDesc',
               'distance', 'averagePriceTip', 'recommendInfo', 'discounts2', 'address', 'shipping_time']
    with open('meituan_waimai.csv', 'a') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writerow(content)

if __name__ == '__main__':
    main()
