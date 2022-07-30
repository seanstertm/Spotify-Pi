from PIL import Image
import os
import time
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions

dir = os.path.dirname(__file__)
testImage = os.path.join(dir, "testImage.jpg")

options = RGBMatrixOptions()
options.rows = 32
options.cols = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "regular"
options.gpio_slowdown = 0
options.brightness = 50
options.limit_refresh_rate_hz = 60

matrix = RGBMatrix(options = options)

image = Image.open(testImage)
image.thumbnail((32, 32), Image.ANTIALIAS)

matrix.SetImage(image.convert('RGB'))

try:
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)