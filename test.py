import spotipy
import spotipy.util as util
import sys
import time
import requests
from PIL import Image
from io import BytesIO
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import configparser
import os

client_id="8e5305d6cf78494fb913b3dafbfc01d9"
client_secret="d662bf3ba5534526966970ee327fca7b"
redirect_uri="http://127.0.0.1:8080/callback"
username="seanstertm"
token_path=".cache"

dir = os.path.dirname(__file__)
filename = os.path.join(dir, 'options.ini')
config = configparser.ConfigParser()
config.read(filename)

options = RGBMatrixOptions()
options.rows = 32
options.cols = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "regular"
options.gpio_slowdown = 0
options.brightness = int(config['MAIN']["brightness"])
options.limit_refresh_rate_hz = 60

matrix = RGBMatrix(options = options)

def getSongInfo():
  scope = 'user-read-currently-playing'
  token = util.prompt_for_user_token(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri ,username=username, scope=scope, cache_path=token_path)
  if token:
      sp = spotipy.Spotify(auth=token)
      result = sp.current_user_playing_track()
    
      if result is None:
        return None
      else:  
        song = result["item"]["name"]
        imageURL = result["item"]["album"]["images"][0]["url"]
        return [song, imageURL]
  else:
      return None

try:
    while True:
        try:
            imageURL = getSongInfo()[1]
            result = requests.get(imageURL)
            image = Image.open(BytesIO(result.content))
            image.thumbnail((32, 32), Image.ANTIALIAS)
            matrix.SetImage(image.convert("RGB"))
            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(1)
except KeyboardInterrupt:
    print("stopping")
    sys.exit

