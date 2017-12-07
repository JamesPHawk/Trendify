# import spotipy
# import spotipy.util as util
# scope = 'user-library-read'
# token = util.prompt_for_user_token("UnduePeej", scope, client_id="7a90865bc671479797914d96ba7d3021", client_secret="0abdd042f90e41adb88dd064c0c3f444", redirect_uri="http://localhost:6942/callback/")
# spy = spotipy.Spotify(auth=token)
# print(results)

import spotipy
import pprint
from flask import Flask, render_template, request, url_for
from flask_s3 import FlaskS3
from spotipy.oauth2 import SpotifyClientCredentials
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
import pymongo

client_credentials_manager = SpotifyClientCredentials(client_id="7a90865bc671479797914d96ba7d3021", client_secret="0abdd042f90e41adb88dd064c0c3f444")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
# artist = "Views"
# results = sp.search(q="album:" + artist, type="album")
# top = sp.artist_top_tracks(artist_id="2YZyLoL8N0Wb9xBt1NhZWg", country="US")
# track = sp.audio_features(tracks="spotify:track:7vkPu9wwdUpB6dPmWBNcPv")
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(results)
# pp.pprint(top)
#pp.pprint(track)
# parsed = json.loads(results)
# print(json.dumps(parsed, indent=4, sort_keys=True))

#get songid
def getSongID(song, artist):
    results = sp.search(q="track:" + song, type="track")
    count = 0
    for i in results.get('tracks').get('items'):
        #print(results.get('tracks').get('items')[count].get('album').get('artists')[0].get('name'))
        if ((results.get('tracks').get('items')[count].get('album').get('artists')[0].get('name')) != artist):
            count = 1 + count
        #print(count)
        else:
            break

    val = (results.get('tracks').get('items')[count].get('id'))
    print(val)
    return val



#--------TRACK-----------#
#params: song id and returns specific attributes about a song
def trackAttributes(id):
    track = sp.audio_features(tracks="spotify:track:" + id)
    acoustic = track[0].get("acousticness")
    danceability = track[0].get("danceability")
    valence = track[0].get("valence")
    energy = track[0].get("energy")
    liveness = track[0].get("liveness")
    loudness = track[0].get("loudness")

    track_dict = {'acoustic': acoustic, 'danceability':danceability, 'valence':valence, 'energy':energy,
                  'liveness':liveness, 'loudness':loudness}
    for i in sorted(track_dict):
        print(i, track_dict[i])
        return track_dict[i]


#--------ALBUM-----------#
#param: album and artist and returns available markets
def albumAttributes(album, artist):
    results = sp.search(q="album:" + album, type="album")
    count = 0
    for i in results.get('albums').get('items'):
        if((results.get('albums').get('items')[count].get('artists')[0].get('name')) != artist):
            count = count + 1
        else:
            break
    val = results.get('albums').get('items')[count].get('available_markets')
    album_dict = {'Available markets for album: ' : val}
    print(album_dict)
    return album_dict



#--------ARTIST-----------#\
#param artist and return artist popularity and genres associated with artist
def artistAttributes(artist):
    results = sp.search(q="artist:" + artist, type="artist")
    genres = results.get('artists').get('items')[0].get('genres')
    popularity = results.get('artists').get('items')[0].get('popularity')
    artist_dict = {'Genres associated with artist:': genres, 'Artist popularity:':popularity}

    for i in artist_dict:
        print(i, artist_dict[i])
        return artist_dict[i]


client = MongoClient('mongodb://localhost:27017')

csu = "http://128.210.106.73"
port = 5000
app = Flask(__name__)
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/result.html', methods=['POST'])
def my_link():
    print("In here")
    song = request.form['Song']
    artist = request.form['Artist']
    album = request.form['Album']
    if song is None and album is None:
        return artistAttributes(artist)
    elif album is None:
        getSongID(song, artist)
        return trackAttributes(artist)
    elif song is None:
        return albumAttributes(album, artist)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)