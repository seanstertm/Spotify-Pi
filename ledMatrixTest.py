from cgi import test
from PIL import Image
import os

dir = os.path.dirname(__file__)
testImage = os.path.join(dir, "testImage.jpg")

print(testImage)

image = Image.open(testImage)
image.thumbnail((32, 32), Image.ANTIALIAS)
