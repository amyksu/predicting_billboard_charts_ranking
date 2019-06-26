## Code to scrape Spotify API

# Import libraries
import re
import os
import csv
import itertools
import collections
import argparse
import pprint
import sys

import subprocess
import unicodedata
import json
import spotipy
import spotipy.util as util
import pandas as pd
import numpy as np

import coloredlogs, logging
from spotipy.oauth2 import SpotifyClientCredentials

# Log progress of scrape
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

#
# Helper function to grab first/main artist from a string.
# 

def get_main_artist(artists):
    if "Featuring" in artists:
        return artists.split("Featuring")[0].strip()
    if "With" in artists:
        return artists.split("With")[0].strip()
    if "," in artists:
        return artists.split(",")[0].strip()
    if "&" in artists:
        # Add exceptions.
        if "Mumford & Sons" in artists:
            return "Mumford & Sons"
        return artists.split("&")[0].strip()
    if "Featuring" in artists:
        return artists.split("Featuring")[0].strip()
    return artists.lower()

#
# Helper function to remove featuring information within parentheses
#
def get_song_title(spotify_song):
    if "Featuring" in spotify_song:
        return re.sub("[\(\[].*?[\)\]]", "", spotify_song).lower()
    if "feat." in spotify_song:
        return re.sub("[\(\[].*?[\)\]]", "", spotify_song).lower()
    return spotify_song.lower()
    # if "Featuring" in spotify_song:
    #     return re.sub(r'\([^()]*\)', '', spotify_song).lower()
    #     # return re.sub("[\(\[].*?[\)\]]", "", spotify_song).lower()
    # elif "feat." in spotify_song:
    #     return re.sub(r'\([^()]*\)', '', spotify_song).lower()
    #     # return re.sub("[\(\[].*?[\)\]]", "", spotify_song).lower()
    # else:
    #     return spotify_song

# File to write
file = csv.writer(open("song_features_allx.csv", "w+", encoding="utf-8"))

# Spotify credentials
client_id = '0e3b405d805945b4b225138b154c0d5b'
client_secret = '361374bbe04c423e82e4e6c5489a4a8f'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

# Create spotify client.
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API

# Parse web scrape CSV and find audio features as listed on Spotify API 
with open('billboard_2012_2019_high.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    headers = next(reader, None)
    feature_set = {
        'danceability': 0.746,
        'energy': 0.873,
        'key': 7,
        'loudness': -3.803,
        'mode': 1,
        'speechiness': 0.128,
        'acousticness': 0.0244, 
        'instrumentalness': 0, 
        'liveness': 0.354,
        'valence': 0.817, 
        'tempo': 148.075, 
        'type': 'audio_features', 
        'id': '2d8JP84HNLKhmd6IYOoupQ', 
        'uri': 'spotify:track:2d8JP84HNLKhmd6IYOoupQ', 
        'track_href': 'https://api.spotify.com/v1/tracks/2d8JP84HNLKhmd6IYOoupQ', 
        'analysis_url': 'https://api.spotify.com/v1/audio-analysis/2d8JP84HNLKhmd6IYOoupQ', 
        'duration_ms': 222093, 
        'time_signature': 4
    }

    headers = headers + list(feature_set.keys())
    file.writerow(headers)

    songs_without_a_match = 0
    songs_with_match = 0
    for i, line in enumerate(reader):
        logger.info("Reading row #{i} out of 3133".format(i=i))

		# Grab song title and artist
        song_title = line[2].lower()

        # Grab artist(s)
        # print("Artist from CSV is.....", line[4])
        # print("Main artist is.........", get_main_artist(line[4]))
        artist = get_main_artist(line[3])
        artist = artist.lower()

		# Search based on song title
        results = sp.search(q=song_title, limit=20)

        track_id = ''
        # Iterate through results and grab the right song!
        for i, t in enumerate(results['tracks']['items']):
            spotify_title = get_song_title(t['name'])
            logger.info('Checking song title.')
            logger.info('song title...{song_title}'.format(song_title=song_title))
            logger.info('name.........{name}'.format(name=spotify_title))
            if spotify_title not in song_title:
                logger.warning('song title is not in the name')
                continue

            artist_name = t['artists'][0]['name'].lower()
            logger.info('Checking artist name.')
            logger.info('artist.......{artist}'.format(artist=artist))
            logger.info('artist_name..{artist_name}'.format(artist_name=artist_name))
            if artist not in artist_name:
                logger.warning('artist is not in the artist name')
                continue

    		# Get track id
            logger.info('Found a match!')
            track_id = t['id']
            break

        # Get audio feature by track id
        features = sp.audio_features(track_id)

        try:
            line.append(features[0]['danceability'])
            line.append(features[0]['energy'])
            line.append(features[0]['key'])
            line.append(features[0]['loudness'])
            line.append(features[0]['mode'])
            line.append(features[0]['speechiness'])
            line.append(features[0]['acousticness'])
            line.append(features[0]['instrumentalness'])
            line.append(features[0]['liveness'])
            line.append(features[0]['valence'])
            line.append(features[0]['tempo'])
            line.append(features[0]['type'])
            line.append(features[0]['id'])
            line.append(features[0]['uri'])
            line.append(features[0]['track_href'])
            line.append(features[0]['analysis_url'])
            line.append(features[0]['duration_ms'])
            line.append(features[0]['time_signature'])

            logger.info("Writing {song_title} by {artist} to file".format(song_title=song_title, artist=artist))
            songs_with_match += 1

        except TypeError:
            logger.warning("Could not find the song in spotify!")
            line.append(np.nan)
            line.append(np.nan)
            line.append(np.nan)
            line.append(np.nan)
            line.append(np.nan)
            line.append(np.nan)
            line.append(np.nan)
            line.append(np.nan)
            line.append(np.nan)
            line.append(np.nan)
            line.append(np.nan)
            line.append(np.nan)
            line.append(np.nan)
            line.append(np.nan)
            line.append(np.nan)
            line.append(np.nan)
            line.append(np.nan)
            line.append(np.nan)

            songs_without_a_match += 1

        logger.info("Matched songs to unmatched songs is {matched}:{unmatched}".format(matched=songs_with_match, unmatched=songs_without_a_match))

        # Write audio feature data to csv
        file.writerow(line)


## if statement - save the information and the number and break
## 