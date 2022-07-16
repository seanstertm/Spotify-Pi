import spotipy
import spotipy.util as util

def getSongInfo(username, token_path):
  scope = 'user-read-currently-playing'
  token = util.prompt_for_user_token(client_id="8e5305d6cf78494fb913b3dafbfc01d9", client_secret="d662bf3ba5534526966970ee327fca7b", redirect_uri="http://127.0.0.1/callback" ,username=username, scope=scope, cache_path=token_path)
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

getSongInfo("seanstertm", ".cache")