# -*- coding: utf-8 -*-
"""
Docs:
https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/
https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/

https://api.spotify.com/v1/browse/new-releases

 Client ID
  Client Secret

https://open.spotify.com/user/?si=6lecnf0nTv6eXwzC5C2M2g

https://open.spotify.com/album/3Gq2Dme9nesdgoqNNlcN8O
r = requests.get(url="https://api.spotify.com/v1/browse/new-releases", headers=headers)

>>> import requests
>>> response = requests.get(
... 'https://website.com/id', headers={'Authorization': 'access_token myToken'})
"""
import json

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class SpotifyAPI(object):
    def __init__(self, CLIENT_ID, CLIENT_SECRET):

        grant_type = "client_credentials"
        body_params = {"grant_type": grant_type}

        url = "https://accounts.spotify.com/api/token"
        response = requests.post(url, data=body_params, auth=(CLIENT_ID, CLIENT_SECRET))

        token_raw = json.loads(response.text)
        token = token_raw["access_token"]
        self.headers = {"Authorization": "Bearer {}".format(token)}

        retry = Retry(connect=3, backoff_factor=0.5)
        self.adapter = HTTPAdapter(max_retries=retry)

    def get_playlists(self, USER_ID):
        # Second step – make a request tox any of the playlists endpoint. Make sure to set a valid value for <spotify_user>.

        r = requests.get(
            url="https://api.spotify.com/v1/users/{}/playlists".format(USER_ID),
            headers=self.headers,
        )
        return json.loads(r.text)

    def get_playlist_items(self, playlist_id, limit=100, offset=1):

        r = requests.get(
            url=f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit={limit}&offset={offset}",
            headers=self.headers,
        )
        return json.loads(r.text)

    def get_track_info(self, track, artist, limit=4):

        r = requests.get(
            url=f"https://api.spotify.com/v1/search?q=track:{track}%20artist:{artist}&limit={limit}&type=track",
            headers=self.headers,
        )
        return json.loads(r.text)

    def get_artist_info(self, ID):

        r = requests.get(
            url=f"https://api.spotify.com/v1/artists/{ID}", headers=self.headers
        )
        return json.loads(r.text)

    def get_audio_features_url(self, ID):
        return f"https://api.spotify.com/v1/audio-features/{ID}"

    def search_track_url(self, track, artist=None):
        if not artist:
            artist = ""
        return f"https://api.spotify.com/v1/search?q=track:{track} artist:{artist}&type=track"

    def get_request(self, url: str):
        """_summary_

        Args:
            url (str): _description_

        Returns:
            _type_: _description_
        """
        with requests.Session() as session:
            session.mount("https://", self.adapter)
            r = session.get(url=url, headers=self.headers)
        return json.loads(r.text)

    def get_audio_analysis(self, ID):
        r = requests.get(
            url=f"https://api.spotify.com/v1/audio-analysis/{ID}", headers=self.headers
        )
        return json.loads(r.text)

    def post_url(self, url):
        r = requests.get(url=url, headers=self.headers)
        return json.loads(r.text)

    def search_track(self, track, artist=None):

        if not artist:
            artist = ""

        url = f"https://api.spotify.com/v1/search?q=track:{track} artist:{artist}&type=track"

        r = requests.get(url=url, headers=self.headers)
        return json.loads(r.text)

    def get_track_id(self, r):

        try:
            return r["tracks"]["items"][0]["id"]
        except (IndexError, KeyError):
            return None
