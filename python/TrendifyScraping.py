# import spotipy
# import spotipy.util as util
# scope = 'user-library-read'
# token = util.prompt_for_user_token("UnduePeej", scope, client_id="7a90865bc671479797914d96ba7d3021", client_secret="0abdd042f90e41adb88dd064c0c3f444", redirect_uri="http://localhost:6942/callback/")
# spy = spotipy.Spotify(auth=token)
# print(results)

import spotipy
import pprint
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id="7a90865bc671479797914d96ba7d3021", client_secret="0abdd042f90e41adb88dd064c0c3f444")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
artist = "Calvin Harris"
results = sp.search(q="artist:" + artist, type="artist")
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(results)
# parsed = json.loads(results)
# print(json.dumps(parsed, indent=4, sort_keys=True))