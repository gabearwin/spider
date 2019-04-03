# -*- coding: UTF-8 -*-
import socks
import socket
from urllib import request
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener

def proxy_no_auth():
    proxy = '127.0.0.1:9743'
    proxy_handler = ProxyHandler({
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    })
    opener = build_opener(proxy_handler)
    try:
        response = opener.open('http://httpbin.org/get')
        print(response.read().decode('utf-8'))
    except URLError as e:
        print(e.reason)

def proxy_auth():
    proxy = 'username:password@127.0.0.1:9743'
    proxy_handler = ProxyHandler({
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    })
    opener = build_opener(proxy_handler)
    try:
        response = opener.open('http://httpbin.org/get')
        print(response.read().decode('utf-8'))
    except URLError as e:
        print(e.reason)

def proxy_socks():
    socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 9742)
    socket.socket = socks.socksocket
    try:
        response = request.urlopen('http://httpbin.org/get')
        print(response.read().decode('utf-8'))
    except URLError as e:
        print(e.reason)
