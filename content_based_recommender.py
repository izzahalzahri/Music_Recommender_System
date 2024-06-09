from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
from spotify_integration import get_track_details, search_spotify

def extract_features(data):
    features = data[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']]
    return features

def recommend_songs_by_keyword(data, keyword, n_recommendations=5):
    spotify_tracks = search_spotify(keyword, type='track')
    spotify_artists = search_spotify(keyword, type='artist')

    if not spotify_tracks and not spotify_artists:
        return pd.DataFrame()  # Return an empty DataFrame if no matches are found

    spotify_results = spotify_tracks + spotify_artists

    recommendations = []
    for item in spotify_results:
        if 'track' in item['type']:
            track = item
            details = get_track_details(track_name=track['name'], artist_name=', '.join([artist['name'] for artist in track['artists']]))
            if details:
                recommendations.append({
                    'name': details['name'],
                    'artists': ', '.join(details['artists']),
                    'popularity': details['popularity'],
                    'url': details['url'],
                    'album_cover': details['album_cover']
                })

    recommendations = sorted(recommendations, key=lambda x: x['popularity'], reverse=True)

    return pd.DataFrame(recommendations)

def personalized_recommendations_by_user_profile(data, user_profile, n_recommendations=5):
    user_profile_features = data[data['user_id'] == user_profile]

    if user_profile_features.empty:
        return pd.DataFrame()  # Return an empty DataFrame if no data is found for the user profile
    scaler = StandardScaler()
    features = extract_features(data)
    data_scaled = scaler.fit_transform(features)

    user_indices = user_profile_features.index.tolist()
    user_vectors = data_scaled[user_indices]

    similarities = cosine_similarity(user_vectors, data_scaled)
    avg_similarities = np.mean(similarities, axis=0)

    indices = np.argsort(avg_similarities)[-n_recommendations:]
    recommended_songs = data.iloc[indices]

    recommendations = []
    for _, row in recommended_songs.iterrows():
        details = get_track_details(row['name'], row['artists'])
        if details:
            recommendations.append({
                'name': row['name'],
                'artists': ', '.join(details['artists']),
                'popularity': details['popularity'],
                'url': details['url'],
                'album_cover': details['album_cover']
            })

    return pd.DataFrame(recommendations)

