import json
import requests
import base64
import logging
import time
import http.client as http_client
from config import CLIENT_ID, CLIENT_SECRET
from utils import remove_dup_names

VIPER_SPOTIFY_ID = "5gQB07Vco4zBCUNbf8SBx4"
SPOTIFY_GET_ARTIST_ALBUMS_URL_TEMPLATE = "https://api.spotify.com/v1/artists/{}/albums"
SPOTIFY_API_TOKEN_URL = "https://accounts.spotify.com/api/token"

def _get_auth_token(client_id, client_secret):
    data = {"grant_type": "client_credentials"}
    encoded_client = base64.b64encode("{}:{}".format(client_id, client_secret).encode())
    
    headers = {"Authorization": "Basic {}".format(encoded_client.decode())}
    r = requests.post(SPOTIFY_API_TOKEN_URL, headers=headers, data=data)
    content = json.loads(r.content)
    return content.get("access_token")


def get_albums_request(spotify_artist_id, offset=0):
    url = SPOTIFY_GET_ARTIST_ALBUMS_URL_TEMPLATE.format(spotify_artist_id)
    token = _get_auth_token(CLIENT_ID, CLIENT_SECRET)
    params = {
        "market": "US",
        "limit": 50,
        "offset": offset
    }
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json",
    }
    r = requests.get(url, params=params, headers=headers)
    return json.loads(r.content)
    
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

def activate_debug():
    http_client.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

# print(get_albums_request(VIPER_SPOTIFY_ID, offset=0).get("items")[0].get("name"))
get_all_viper_albums()