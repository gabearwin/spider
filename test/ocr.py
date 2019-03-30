# -*- coding: UTF-8 -*-

import tesserocr

from PIL import Image

image = Image.open("/Users/gaxiong/Downloads/image.png")
print(tesserocr.image_to_text(image))

print(tesserocr.file_to_text("/Users/gaxiong/Downloads/image.png"))