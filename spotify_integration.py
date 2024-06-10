import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv(spotify.env)

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

def get_all_genres():
    return sp.recommendation_genre_seeds()['genres']

def get_track_details(track_name, artist_name):
    results = sp.search(q=f'track:{track_name} artist:{artist_name}', type='track')
    tracks = results['tracks']['items']
    if tracks:
        track = tracks[0]
        album_cover = track['album']['images'][0]['url'] if track['album']['images'] else None
        track_url = track['external_urls']['spotify']
        popularity = track['popularity']
        return album_cover, track_url, popularity
    return None, None, None

def search_tracks(keyword, n_recommendations=20):
    results = sp.search(q=keyword, type='track', limit=n_recommendations)
    tracks = results['tracks']['items']
    recommendations = []
    for track in tracks:
        name = track['name']
        artists = ", ".join([artist['name'] for artist in track['artists']])
        album_cover = track['album']['images'][0]['url'] if track['album']['images'] else None
        track_url = track['external_urls']['spotify']
        popularity = track['popularity']
        recommendations.append({
            'name': name,
            'artists': artists,
            'album_cover': album_cover,
            'url': track_url,
            'popularity': popularity
        })
    return pd.DataFrame(recommendations)

def recommend_tracks_by_genre(genre, n_recommendations=20):
    results = sp.recommendations(seed_genres=[genre], limit=n_recommendations)
    tracks = results['tracks']
    recommendations = []
    for track in tracks:
        name = track['name']
        artists = ", ".join([artist['name'] for artist in track['artists']])
        album_cover = track['album']['images'][0]['url'] if track['album']['images'] else None
        track_url = track['external_urls']['spotify']
        popularity = track['popularity']
        recommendations.append({
            'name': name,
            'artists': artists,
            'album_cover': album_cover,
            'url': track_url,
            'popularity': popularity
        })
    # Sort by popularity descending
    recommendations = sorted(recommendations, key=lambda x: x['popularity'], reverse=True)
    return pd.DataFrame(recommendations)

def recommend_playlists_by_track(track_name, n_recommendations=5):
    results = sp.search(q=f'track:{track_name}', type='playlist', limit=n_recommendations)
    playlists = results['playlists']['items']
    playlist_recommendations = []
    for playlist in playlists:
        playlist_recommendations.append({
            'name': playlist['name'],
            'url': playlist['external_urls']['spotify'],
            'image': playlist['images'][0]['url'] if playlist['images'] else None,
            'description': playlist['description']
        })
    return playlist_recommendations

def get_suggestions(keyword, n_suggestions=10):
    results = sp.search(q=keyword, type='track', limit=n_suggestions)
    tracks = results['tracks']['items']
    suggestions = []
    for track in tracks:
        name = track['name']
        artists = ", ".join([artist['name'] for artist in track['artists']])
        album_cover = track['album']['images'][0]['url'] if track['album']['images'] else None
        suggestions.append({
            'name': name,
            'artists': artists,
            'album_cover': album_cover
        })
    return suggestions
