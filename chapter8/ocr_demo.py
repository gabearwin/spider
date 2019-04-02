# -*- coding: UTF-8 -*-

import tesserocr
from hashlib import md5

import requests
from PIL import Image
from requests import codes

def ocr_redirect():
    # 识别概率不高，容易受到线条、模糊化干扰
    print(tesserocr.file_to_text("pic/code.jpg"))

    image = Image.open("pic/code2.jpg")
    print(tesserocr.image_to_text(image))

def ocr_clean():
    # 经过转灰度和二值化等操作识别概率更高
    # image = Image.open('pic/code.jpg')
    image = Image.open('pic/495f5107252a6bbd335eac9e185a2543.jpg')

    image = image.convert('L')
    # image = image.convert('1')
    threshold = 50
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table, '1')
    image.show()

    result = tesserocr.image_to_text(image)
    print(result)

ocr_clean()

def ocr_remote_link():
    url = "https://raw.githubusercontent.com/Python3WebSpider/CrackImageCode/master/code2.jpg"
    resp = requests.get(url)
    if codes.ok == resp.status_code:
        file_name = 'pic/' + str(md5(resp.content).hexdigest()) + '.jpg'
        with open(file_name, 'wb') as f:
            f.write(resp.content)
        print(tesserocr.file_to_text(file_name))

# ocr_remote_link()
