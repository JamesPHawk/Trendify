import spotipy
import spotipy.util as util
scope = 'user-library-read'
token = util.prompt_for_user_token("UnduePeej", scope, client_id="7a90865bc671479797914d96ba7d3021", client_secret="0abdd042f90e41adb88dd064c0c3f444", redirect_uri="trendify://callback/")
spy = spotipy.Spotify(auth=token)
name = "Kendrick Lamar"
results = spy.search(q='artist:' + name, type='artist')
print(results)