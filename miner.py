import json
import requests
import base64
import logging
import time
import http.client as http_client
from config import CLIENT_ID, CLIENT_SECRET
from utils import remove_dup_names, scramble_txt

VIPER_SPOTIFY_ID = "5gQB07Vco4zBCUNbf8SBx4"
SPOTIFY_GET_ARTIST_ALBUMS_URL_TEMPLATE = "https://api.spotify.com/v1/artists/{}/albums"
SPOTIFY_GET_TRACKS_IN_ALBUM_URL_TEMPLATE = "https://api.spotify.com/v1/albums/{}/tracks"
SPOTIFY_API_TOKEN_URL = "https://accounts.spotify.com/api/token"

# this needs to be refreshed every hourish - but since this application isn't long standing we should
# be okay with just fetching once and using it for our session 
TOKEN = None

def _get_auth_token(client_id, client_secret):
    data = {"grant_type": "client_credentials"}
    encoded_client = base64.b64encode("{}:{}".format(client_id, client_secret).encode())
    
    headers = {"Authorization": "Basic {}".format(encoded_client.decode())}
    r = requests.post(SPOTIFY_API_TOKEN_URL, headers=headers, data=data)
    content = json.loads(r.content)
    return content.get("access_token")


def get_albums_request(spotify_artist_id, offset=0):
    global TOKEN
    url = SPOTIFY_GET_ARTIST_ALBUMS_URL_TEMPLATE.format(spotify_artist_id)
    if not TOKEN:
        TOKEN = _get_auth_token(CLIENT_ID, CLIENT_SECRET)
    params = {
        "market": "US",
        "limit": 50,
        "offset": offset
    }
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(TOKEN),
        "Content-Type": "application/json",
    }
    r = requests.get(url, params=params, headers=headers)
    return json.loads(r.content)
   
def get_tracks_in_album_request(album_id, offset=0):
    global TOKEN
    url = SPOTIFY_GET_TRACKS_IN_ALBUM_URL_TEMPLATE.format(album_id)
    if not TOKEN:
        TOKEN = _get_auth_token(CLIENT_ID, CLIENT_SECRET)
    params = {
        "market": "US",
        "limit": 50,
        "offset": offset,
    }
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(TOKEN),
        "Content-Type": "application/json",
    }
    # super naive retry
    for x in range(0, 5):
        try:
            r = requests.get(url, params=params, headers=headers)
            if r:
                return json.loads(r.content)
        except:
            time.sleep(2 ** x)
            continue
    return None


def get_all_viper_albums():
    offset = 0
    with open("data.json", "w") as outfile:
        with open("names.txt", "w") as names_outfile:
            while True:
                items = get_albums_request(VIPER_SPOTIFY_ID, offset=offset).get("items")
                if not items or items == []:
                    break
                json.dump(items, outfile)

                for album_item in items:
                    names_outfile.write(album_item.get("name")+"\n")

                offset += 50
                time.sleep(5)
    remove_dup_names("names.txt")
    scramble_txt("names.txt")

def get_all_viper_album_ids():
    offset = 0
    with open("album_ids.txt", "w") as outfile:
        while True:
            items = get_albums_request(VIPER_SPOTIFY_ID, offset=offset).get("items")
            if not items or items == []:
                break

            for album_item in items:
                outfile.write(album_item.get("id") + "\n")

            offset += 50
            time.sleep(3)

def get_all_viper_tracks_from_album_ids(album_ids):
    with open("track_names.txt", "w") as outfile:
        for i in album_ids:
            print(i)
            tracks = get_tracks_in_album_request(i).get("items")
            for t in tracks: 
                name = t.get("name")
                print(name)
                outfile.write(name + "\n")
            time.sleep(2)


def activate_debug():
    http_client.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


ids = []
f = open("album_ids.txt", "r")
for l in f:
    ids.append(l.strip())
f.close()
get_all_viper_tracks_from_album_ids(ids)
