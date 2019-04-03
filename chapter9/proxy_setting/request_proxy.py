# -*- coding: UTF-8 -*-
import socket

import requests
import socks

def proxy_no_auth():
    proxy = '127.0.0.1:9743'
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy,
    }
    try:
        response = requests.get('http://httpbin.org/get', proxies=proxies)
        print(response.text)
    except requests.exceptions.ConnectionError as e:
        print('Error', e.args)

def proxy_auth():
    proxy = 'username:password@127.0.0.1:9743'
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy,
    }
    try:
        response = requests.get('http://httpbin.org/get', proxies=proxies)
        print(response.text)
    except requests.exceptions.ConnectionError as e:
        print('Error', e.args)

def proxy_socks():
    proxy = '127.0.0.1:9742'
    proxies = {
        'http': 'socks5://' + proxy,
        'https': 'socks5://' + proxy
    }
    try:
        response = requests.get('http://httpbin.org/get', proxies=proxies)
        print(response.text)
    except requests.exceptions.ConnectionError as e:
        print('Error', e.args)

def proxy_all_socks():
    """
    全局代理，下面所有的请求都会被代理
    """
    socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 9742)
    socket.socket = socks.socksocket
    try:
        response = requests.get('http://httpbin.org/get')
        print(response.text)
    except requests.exceptions.ConnectionError as e:
        print('Error', e.args)
