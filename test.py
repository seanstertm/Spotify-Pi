import spotipy
import spotipy.util as util
import sys
import time

client_id=""
client_secret=""
redirect_uri=""
username=""
token_path=""

def getSongInfo():
  scope = 'user-read-currently-playing'
  token = util.prompt_for_user_token(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri ,username=username, scope=scope, cache_path=token_path)
  if token:
      sp = spotipy.Spotify(auth=token)
      result = sp.current_user_playing_track()

      if result is None:
        return "No song"
      else:  
        song = result["item"]["name"]
        imageURL = result["item"]["album"]["images"][0]["url"]
        return [song, imageURL]
  else:
      return "Failed"

print(getSongInfo()[0].encode("utf-8"))
