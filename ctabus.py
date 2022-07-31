import sys
import time
import requests
import spotipy
import spotipy.util as util
import configparser
import os
from PIL import Image
from io import BytesIO
from rgbmatrix import RGBMatrix, RGBMatrixOptions

route = 152
stop = 12472

client_id="8e5305d6cf78494fb913b3dafbfc01d9"
client_secret="d662bf3ba5534526966970ee327fca7b"
redirect_uri="http://127.0.0.1:8080/callback"
# redirect_uri="http://127.0.0.1/callback?code=AQACDh03u5rqq2tgR0UL4kSZt08rWwIrvXYbYZxNQYNNXNHSqPvmwzMrExb_PsPFXUXaTePoeYRXOL_OVlTaRTpXOBihkoaXd6WDj5hAeKQLCq9oVfLtCgTB8t0o_fDss647b2zYh-Q1wg6xgC97hhvaIuUwdnF_iZI6YGk9chky-svzwK8MpuctnzyV1GdlSonpsIBSQDc1dw"
username="seanstertm"
token_path=".cache"

prevTime = ""
nowTime = ""

prevSong = ""
nowSong = ""

dir = os.path.dirname(__file__)
filename = os.path.join(dir, 'options.ini')
config = configparser.ConfigParser()
config.read(filename)

errorImage = os.path.join(dir, "warning.png")

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
        if config['MAIN']['mode'] == 'cta':
            try:
                response = requests.get(f"http://ctabustracker.com/bustime/api/v2/getpredictions?key=Yr9nbHrDBVbxtdC4j8BTw5R3z&rt={route}&stpid={stop}&format=json")
                bus_json = response.json()
                if "error" in bus_json['bustime-response']:
                    nowTime = "No busses in the next 30 minutes"
                else: 
                    nowTime = bus_json['bustime-response']['prd'][0]['prdctdn']
                if prevTime != nowTime:
                    image = Image.open(errorImage)
                    image.thumbnail((32, 32), Image.ANTIALIAS)
                    matrix.SetImage(image.convert('RGB'))
                    prevTime = nowTime
                time.sleep(5)
            except Exception as e:
                image = Image.open(errorImage)
                image.thumbnail((32, 32), Image.ANTIALIAS)
                matrix.SetImage(image.convert('RGB'))
                time.sleep(1)
        elif config['MAIN']['mode'] == 'spotify':
            try:
                imageUrl = getSongInfo()[1]
                nowSong = imageUrl
                if prevSong != nowSong:
                    result = requests.get(nowSong)
                    image = Image.open(BytesIO(result.content))
                    image.thumbnail((32, 32), Image.ANTIALIAS)
                    matrix.SetImage(image.convert('RGB'))
                    prevSong = nowSong
                time.sleep(1)
            except Exception as e:
                nowSong = "No song playing"
                if prevSong != nowSong:
                    image = Image.open(errorImage)
                    image.thumbnail((32, 32), Image.ANTIALIAS)
                    matrix.SetImage(image.convert('RGB'))
                    prevSong = nowSong
                time.sleep(1)
except KeyboardInterrupt:
    print("stopping...")
    sys.exit(0)

