# -*- coding: UTF-8 -*-

import zipfile

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def phantomjs_no_auth():
    service_args = [
        '--proxy=127.0.0.1:9743',
        '--proxy-type=http'
    ]
    browser = webdriver.PhantomJS(service_args=service_args)
    browser.get('http://httpbin.org/get')
    print(browser.page_source)

def phantomjs_auth():
    service_args = [
        '--proxy=127.0.0.1:9743',
        '--proxy-type=http',
        '--proxy-auth=username:password'
    ]
    browser = webdriver.PhantomJS(service_args=service_args)
    browser.get('http://httpbin.org/get')
    print(browser.page_source)

def chrome_no_auth():
    proxy = '127.0.0.1:9743'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=http://' + proxy)
    chrome = webdriver.Chrome(chrome_options=chrome_options)
    chrome.get('http://httpbin.org/get')

def chrome_auth():
    ip = '127.0.0.1'
    port = 9743
    username = 'foo'
    password = 'bar'

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        }
    }
    """

    background_js = """
    var config = {
        mode: "fixed_servers",
        rules: {
            singleProxy: {
                scheme: "http",
                host: "%(ip)s",
                port: %(port)s
            }
        }
    }
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%(username)s",
                password: "%(password)s"
            }
        }
    }
    chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {urls: ["<all_urls>"]},
        ['blocking']
    )
    """ % {'ip': ip, 'port': port, 'username': username, 'password': password}

    plugin_file = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(plugin_file, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_extension(plugin_file)
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get('http://httpbin.org/get')
