import spotipy
import spotipy.util as util
import sys
import time

client_id="3631fe86bb204356b6f83ee2fb0a9299"
client_secret="82e80b6fca4643d29621346203e77885"
redirect_uri="http://127.0.0.1:8080/callback"
username="sofaking2004"
token_path=".cache"

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
